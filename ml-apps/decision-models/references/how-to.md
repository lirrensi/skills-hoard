# How to use decision models — correctly

This is the deep reference. `SKILL.md` has the summary; everything below is the how and the why.

## The request contract

```http
POST /v1/systemone
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "state": "<string | object | array>",     # required — the content to judge
  "model": "jev-latest",                    # required — which decision model
  "questions": {                             # required — 1..256, keys are yours
    "<id>": { "type": "noul|choice|score", "instructions": ..., "criteria": ... }
  }
}
```

`state` is the material you'd put in front of a panel of experts. It can be a plain string, a JSON object (named fields, related records), or an array (a message sequence). Use an **object** for most real work so each part is named and its relationships are clear.

`instructions` may itself be a string, object, or array — break a long question into fields and refer to data by name in backticks:

```json
"instructions": {
  "potential_duplicate": {"name": "John Smith", "location": "Oakland"},
  "question": "Is the resume for the same person as `potential_duplicate`?"
}
```

### Question types in detail

**Noul** — a yes/no question; optional `criteria` describing what yes/no mean.
```json
"is_urgent": { "type": "noul", "instructions": "Does this convey urgency?",
               "criteria": { "true": "Explicitly time-sensitive", "false": "No urgency expressed" } }
```
Answer: `{ "type": "noul", "noul": 0.95 }` — `noul` is P(yes). No `confidence` field.

**Choice** — pick one option from a map of option → rubric description (use `null` when an option needs no extra detail). 1–255 options.
```json
"department": { "type": "choice", "instructions": "Which team should handle this?",
                "criteria": { "billing": "Payments, invoicing, refunds",
                              "technical": "Bugs, outages, integrations",
                              "sales": "Pricing, upgrades, new accounts" } }
```
Answer: `{ "type": "choice", "choice": "billing", "probabilities": {...}, "confidence": 0.81 }`.

**Score** — an *ordered array* of level descriptions. 2–10 levels, lowest first.
```json
"frustration": { "type": "score", "instructions": "How frustrated is the customer?",
                 "criteria": ["Calm", "Frustrated", "Very angry"] }
```
Answer: `{ "type": "score", "score": 1.05, "legend": {"0": "Calm", "1": "Frustrated", "2": "Very angry"}, "probabilities": {...}, "confidence": 0.92 }`.

### Limits (hosted Jev 1.13)

- Questions per request: **1–256**. Choice options: **1–255**. Score levels: **2–10**.
- Context: **32k tokens** for `state` + the single longest question; **64k** for `state` + all questions combined.
- Input text only (a string, JSON object, or array of text). No images/audio/video on the hosted model.
- `state` is counted **once** per request — that's why batching many questions is cheap.

## Writing good questions (this is 90% of the quality)

**Ask for one snap judgment per question.** "Does this message convey urgency?" — good. "Analyze this and determine the best course of action" — bad (that's slow reasoning; break it up and compose in code).

**Describe what each answer means.** A Choice option description and a Score level are the model's rubric. "Very angry" is weak; "Hostile language or threatens to cancel" is strong. Rubrics beat instructions.

**Give structure, not vibes.** Prefer `{"what": ..., "signals": [...], "examples": [...]}` inside a criterion over a bare adjective.

**Say what is *required* versus merely *preferred*.** Measured on a live agent: one sentence drawing that distinction roughly **doubled** accuracy on the same decision. Preconditions, exclusions and negations belong in the question — stated, not implied.

**Write `instructions` and `criteria` in English — even when `state` is not.** Measured on one Russian ticket (`is_bug`): Russian questions on clef-flash scored 0.55 (coin flip, wrong); the same questions in English scored 0.95. frida-decisions in Russian scored 0.83, jev in Russian 0.96 — same inputs, three identical repeats, so this is prompt sensitivity, not noise. The question language matters more than the data language; `state` can stay in the original language.

**Always add an `other` option** to a Choice when the input space may exceed your set — otherwise the model is forced into the closest listed option even when none fit. (`other`/`none` should have a description too.)

**Keep order meaningful.** For a Choice, pass criteria as an **ordered list** of `{key, description}` pairs when order matters; a Score is always an ordered array. Options are seen in the order you declare them.

**Ask in one request.** Independent questions are answered in parallel. Do not chain them one at a time.

**Only split into a second request when construction genuinely depends on the first answer** — you need it to fetch more state, to choose the next question's *options*, or to define what the state even is. That's the rare case (skill suggestion, structure recovery, hierarchical classification).

## State design

- Put **all related material in one object** when the decision requires comparing the parts (message + records + policy → one `state`).
- Keep **content in `state`** and **judgments in `questions`.** Don't smuggle the question into the state.
- Pre-process non-text (OCR, transcription, parse to fields) before sending to a text-only model.
- Remember the 32k/64k budget: long tool results and full histories fill it fastest. Compact or summarize *before* the call.

## Confidence, probabilities, and gating

`confidence` measures how peaked the distribution is on the winner, from 0 (torn) to 1 (dominates). It is **not** "probability this is correct" and it is not a calibration promise.

```python
# Choice: how far the top sits above an even split 1/n
def choice_confidence(probabilities):
    n = len(probabilities)
    return (max(probabilities) - 1 / n) / (1 - 1 / n)

# Score: distance of probability mass from the most likely level, vs an even spread
def score_confidence(probabilities):
    n = len(probabilities)
    m = probabilities.index(max(probabilities))
    spread = sum(p * abs(i - m) for i, p in enumerate(probabilities))
    even_spread = sum(abs(i - (n - 1) / 2) for i in range(n)) / n
    return max(0.0, 1 - spread / even_spread)
```

Two simpler signals, often better in practice: **top probability** `p_max` (set the threshold per question — 0.5 is weak among 2 options, strong among 10) and **top-to-second ratio** `p_max / p_second`.

### Confidence-gated routing (the safe way to act automatically)

```python
action = response.answers["intent"]

if action.confidence < 0.60:                 # floor: genuinely uncertain → a human
    route_to_support_agent(account_id)
elif action.choice == "check_balance":       # low stakes: 0.6 is enough
    show_balance(account_id)
elif action.choice == "approve_transfer":
    if action.confidence > 0.85:             # high stakes: demand certainty
        approve_transfer(account_id)
    else:
        ask_user_to_confirm("Just to confirm: approve this transfer?")
```

The **floor catches anything uncertain; each action gets its own threshold by consequence.** This is the single most important idea for reliability.

## The four patterns, with code

### 1. Speculative fan-out
Ask everything the decision tree might need in one call; ignore what the chosen branch doesn't use.

```python
# One request, five questions. bug_severity only matters if category == bug_report.
q = {
  "category":   Choice("Broad category of this ticket",
                       bug_report="Broken/erroring", billing="Charges, refunds",
                       feature_request="New functionality", account="Login/security"),
  "bug_severity": Score("How severe is the issue",
                        ["Cosmetic", "Degraded, workaround exists", "Blocking, no workaround"]),
  "has_repro":   Noul("The user gives steps to reproduce"),
  "refund":      Noul("The user explicitly asks for a refund or credit"),
  "frustration": Score("How frustrated is the user", ["Calm", "Frustrated but civil", "Very angry"]),
}
a = client.system_one(state=ticket, questions=q).answers

if a["category"].choice == "bug_report":
    if a["bug_severity"].score > 1.5 and a["has_repro"].noul > 0.6:
        escalate_to_engineering(ticket_id)
    else:
        add_to_bug_backlog(ticket_id)
elif a["category"].choice == "billing":
    route_to_billing(ticket_id, refund_likely=a["refund"].noul >= 0.7)

if a["frustration"].score > 1.5:            # useful regardless of category
    flag_for_priority_response(ticket_id)
```

### 2. Confidence-gated routing
See above — answer = *what*, confidence = *whether to act*.

### 3. Composite scoring
Break a fuzzy judgment into atomic Scores, normalize, weight in code.

```python
py, lead, arch = (a["python_depth"].score / 4, a["team_leadership"].score / 4, a["system_design"].score / 4)
ic_score = 0.40*py + 0.10*lead + 0.40*arch           # senior IC
em_score = 0.15*py + 0.40*lead + 0.20*arch           # engineering manager
```
Change priorities by changing weights — never by rewriting a prompt.

### 4. Intent routing
```python
intent = client.system_one(state=user_text, questions={
    "intent": Choice("What does the user want?",
                     checkout="Pay or buy", support="Get help", other="Anything else")}).answers["intent"]
if intent.confidence < 0.6:        escalate_to_human()
elif intent.choice == "checkout":  deterministic_checkout()
else:                              route_to_llm_or_human()
```
Route each request to the **cheapest sufficient** handler: deterministic code → specialist LLM → human.

## Operational discipline: shadow first, fail open

Two rules that decide whether a decision layer helps or hurts in production.

- **Shadow mode first.** Run the decision and *log* it (tier/model/confidence/latency) **without acting on it**. A day of decisions costs almost nothing and risks nothing. Promote to live only when the log looks right — and remember a *quiet* log proves nothing, so bound the trial by wall-clock, not by a request count.
- **Fail open.** No key, timeout, rate limit, malformed reply, or low confidence must never block the caller: keep the current model, return the original list, drop nothing, suggest nothing. The worst case should be the time budget (a few seconds), never a stalled turn.
- **Rails independent of the model's correctness.** Deterministic pre-rules run first (risk words never take the cheap path; a large context never downshifts; a turn is dropped only on a confident answer), and the model may only ever return an **id you defined** — never a free-form action.

## Errors & retries

| Status | Meaning | Action |
| - | - | - |
| `401` | Missing/invalid key | Fix auth. |
| `422` | Request failed validation (bad field, malformed question) | Fix the request — do **not** retry. |
| `400` / `501` | (llama.cpp / local servers) bad request / unsupported model or image config | Fix — do not retry. |
| `429` | Rate limited | Retry with exponential backoff; honour `retry-after`. |
| `529` | Provider overloaded | Retry with backoff. |

SDKs retry `429`/`529` automatically. **Never retry a capability mismatch as if it were congestion.**

## Calibrating and testing

- Hosted Jev is calibrated with RLCD; the same weights serve everyone, shaped only by your `state`, `instructions`, and `criteria`. You customize through the request, not fine-tuning.
- **Open checkpoints are usually not calibrated.** Fit a threshold on your own labelled sample: `von calibrate labels.jsonl` writes a `marker_calibration.json` and reports NLL/ECE for raw vs fitted. Temperature changes *certainty*, never the *answer*.
- Build a small labelled set, sweep thresholds, and pick the cutoff that keeps your target accuracy on the items you auto-act on. Gate on `noul_raw` (the pre-band probability) where a model wraps `noul` in a fixed band, since the wrapped value carries no gate signal.
- Put **questions and all thresholds in one file** so a human can review the whole policy in one place.
- When you're ready to compare models, run the **Decision Index** against any `/v1/systemone` server (`--engine http --option base_url=...`).

## Cost & speed intuition

- Hosted Jev: `$0.042` per **million input tokens**, **output free**. Because one request evaluates many questions and the state is counted once, real workloads land at fractions of a cent: reported figures include ~`$0.001` per document page and ~`$0.0002` per computer-use step.
- Batching is the whole game: one 13-question request was measured **12.2× cheaper and 10× faster** than 13 separate calls, with no change in answers.
- Local encoder models answer in tens of milliseconds on a CPU; a 4B in a few hundred ms; DiffusionGemma-class wants a GPU for sub-100 ms.

## Pitfalls (the short list)

1. Compound questions — split them.
2. No `other` option on a Choice.
3. Unordered criteria where order matters.
4. `noul ≈ 0.5` read as "medium" — gate it.
5. Ripe questions chained into extra requests instead of one fan-out.
6. Raw confidence from an uncalibrated open checkpoint.
7. Images to a text-only model.
8. Missing `NO_PROXY=localhost,127.0.0.1` for local SDK calls.
9. Using a moving alias after tuning thresholds — pin the version.
10. Retrying a `4xx`/`501` validation error.
11. Treating `confidence` as "probability correct" instead of "peakedness of this distribution".
12. Forgetting that questions in one request **cannot see each other's answers**.
