---
name: decision-models
description: "Return typed, calibrated answers with probabilities in a single forward pass."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags:
      [
        decision-models,
        jev,
        system-one,
        typesafe,
        structured-output,
        classification,
        routing,
        local-inference,
        llm-serving,
      ]
    related_skills:
      [local-llm-inference, llm-judge-evaluation, serving-llms-vllm]
---

# Decision Models (System One / Jev)

## Overview

A **decision model** takes a piece of `state` (text, or JSON) plus a set of **typed questions**, and returns one **typed answer per question** with **calibrated probabilities** — in a _single forward pass_. It never generates text, never reasons in the open, and never returns a value outside the options you gave it. There is no completion to parse, no JSON to repair, and effectively no prompt-injection surface in the output: the shape _is_ the API contract.

This is a distinct model **category**, not a provider. TypeSafe AI's **Jev** created it ("System One" models); Jev is the reference implementation, and the `/v1/systemone` wire format is now served by a whole ecosystem — OpenRouter, Ollama, llama.cpp, vLLM, SGLang, ONNX runtimes, and dozens of open checkpoints (see `references/where-to-get.md`).

**This space is moving weekly — check what you already have first.** New providers add decision-model endpoints as we speak, and inference platforms that never used the word a month ago are quietly exposing a `decisions` / `systemone` / `classify` route. Before shopping for a model, look at the AI provider you **already pay for**: it may already ship one, or a similar typed-decision concept, and you'd only need to change a base URL. If it doesn't have the word "decision" anywhere, ask whether it has a constrained/structured classification endpoint — that's usually the same idea wearing a different name. (Concretely: OpenRouter's default model list **omits** decision models; they only appear when you filter by output modality — `?output_modalities=decisions` — which is how its site shows the _Decisions_ tab.)

**The mental model:** you are not asking a model to _write_ a decision, you are asking it to _score_ pre-defined options. Milliseconds on a CPU, sub-cent on an API.

### The three primitives (this is the whole API)

| Type       | Question it answers          | Returns                                                                                                     |
| ---------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Noul**   | Is this true? (yes/no)       | `noul` — P(yes) from 0 to 1. No confidence field.                                                           |
| **Choice** | Which one of these options?  | `choice` (top option), `probabilities` (per option, sum to 1), `confidence`                                 |
| **Score**  | Where on this ordered scale? | `score` (probability-weighted position, can fall _between_ levels), `legend`, `probabilities`, `confidence` |

One request carries **1–256 questions**; every question sees the same `state` and is evaluated **independently and in parallel**. Adding questions costs tokens, not meaningful latency. Combine the answers in your own code.

## When to Use

Reach for a decision model when the task is **one snap judgment a knowledgeable person makes in a second given the right context**:

- **Classification** — intent, topic, department, risk type, entity type
- **Detection** — spam, fraud, urgency, jailbreak, PII, policy violation
- **Scoring** — severity, relevance, quality, frustration, suitability, difficulty
- **Routing** — which handler, which model, which queue, which tool, escalate-or-not
- **Search / retrieval / ranking** — score query-to-candidate relevance, rerank, select RAG context
- **Verification** — does this citation support the claim, did the tool call work, is this output on-policy
- **Feature extraction** — turn free text into numeric features for a downstream classical model
- **Real-time loops** — computer use, game agents, UI decisions where 150 ms is too slow for an LLM

### When to prefer a decision model over a plain LLM with structured output

Use a decision model when **all** of these hold:

1. The answer space is **closed** — you can enumerate the options or the scale up front.
2. You want **probability + confidence**, not just a label — so you can _gate_ (act / confirm / escalate to a human) instead of guessing.
3. You need **speed or cost** — thousands of decisions per dollar, milliseconds per call, or you need to run offline / air-gapped / on a laptop.
4. You want **guaranteed shape** — no retries from malformed JSON, no label drift.

Prefer a **general LLM** when you need to _produce_ something (a reply, a summary, a document), when the task needs multi-step reasoning or chaining, or when the output shape genuinely can't be enumerated. Prefer a **classical classifier** when you have thousands of labelled examples and a single fixed label set — a decision model is zero-shot with your rubric in the prompt.

### Limitations (know these before you commit)

- **No text output, no chain of thought.** If you need a justification, make the decision here and let a chat model explain it, or route low confidence to a human.
- **No images/audio on hosted Jev** (text/JSON only). Some local checkpoints _do_ take images (OpenJev 27B, Valen) — see the references.
- **Independent questions only.** One answer cannot inform another _inside the same request_. If a later judgment needs an earlier answer to even be **constructed**, that's a second request — but that's the exception, not the rule.
- **Not calibrated by default on community checkpoints.** Hosted Jev is RLCD-calibrated; most open models are not. Fit a threshold on your own labels before you trust a number (see `references/how-to.md`).
- **Question language moves accuracy more than data language.** Write `instructions`/`criteria` in English even for non-English `state` — measured on one Russian ticket: Russian questions scored 0.55 (coin flip, wrong) vs 0.95 in English on the same model. Von is English-only.

### Small ≠ good — pick the backbone, not the parameter count

A tiny decision model is **not** a cheap version of a big one. Most models under ~2B are _deliberately limited_: they ship as **bases for your own fine-tuning** or as single-task specialists. They are fast and cheap precisely because they carry little world knowledge, so they miss nuance and are not something to grab off the shelf and hope will work. They _can_ be excellent — but only after you make them yours, or if your task happens to be exactly their specialty.

Where the good ones come from: **take an existing chat model and replace its output head.** That is literally how TypeSafe's System One models are built, and the chat backbone is where the understanding, reasoning, and world knowledge live. The head only forces the answer into your typed shape.

So choose by need:

- **Broad capability, nuance, general or unseen decisions** → an **LLM-backed** decision model (a chat-model backbone: Qwen-class, DiffusionGemma, etc.). This is where the strongest zero-shot results come from.
- **Speed, cost, or scale on a narrow, well-defined decision** → a small encoder or sub-2B model, and expect to **fine-tune it on your own labels** before it earns trust.
- **Either way: measure.** Small models are _specialized_, not uniformly worse — one may nail your exact decision and be hopeless on the next. Try the small one _on your actual case_ before dismissing it (and re-read the calibration section of `references/how-to.md`).

## Quickstart (60 seconds, no signup)

**Option A — OpenRouter (hosted, one key, no waitlist).** Uses the Decisions API:

```bash
export OPENROUTER_API_KEY=...
curl https://openrouter.ai/api/alpha/decisions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "typesafe/jev-1.13",
    "state": {"ticket": "My checkout shows a blank screen after I click Pay."},
    "questions": {
      "is_bug": {"type": "noul",  "instructions": "Is the customer reporting a software defect?",
                 "criteria": {"true": "Broken/unexpected behaviour", "false": "Question or feature request"}},
      "team":   {"type": "choice", "instructions": "Which team owns this?",
                 "criteria": {"payments": "Checkout, billing, refunds", "frontend": "Rendering, layout", "account": "Login, profile"}},
      "urgency":{"type": "score",  "instructions": "How urgent is this?",
                 "criteria": ["Can wait", "This week", "Blocking revenue now"]}
    }
  }'
```

The TypeSafe Python/JS SDK also works against OpenRouter by changing the base URL (`TYPESAFE_BASE_URL=https://openrouter.ai/api`).

**Option B — local, zero network** (llama.cpp / Ollama / Ollaya all speak the same endpoint):

```bash
# llama.cpp (build b11361+): downloads a 4B decision model and serves it
llama serve -hf ggml-org/Kev-4B-GGUF
curl http://localhost:8080/v1/systemone -H 'Content-Type: application/json' -d '{ ...same body as above... }'

# or Ollama 0.35+
ollama pull nimble && curl http://localhost:11434/v1/systemone -d '{ ...}'   # model: "nimble"
```

**Response shape** (identical everywhere):

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "is_bug": { "type": "noul", "noul": 0.96 },
    "team": {
      "type": "choice",
      "choice": "payments",
      "probabilities": { "payments": 0.71, "frontend": 0.24, "account": 0.05 },
      "confidence": 0.57
    },
    "urgency": {
      "type": "score",
      "score": 1.99,
      "legend": {
        "0": "Can wait",
        "1": "This week",
        "2": "Blocking revenue now"
      },
      "probabilities": { "0": 0.05, "1": 0.02, "2": 0.93 },
      "confidence": 0.88
    }
  },
  "usage": { "input_tokens": 476, "output_tokens": 0 }
}
```

## Read Your Answer Correctly

- `noul` is **P(yes)**, not a label. Near `0.5` means "coin flip" — that is your escalation signal, not a medium value.
- `choice` is the arg-max option; `probabilities` is the whole distribution. Two distributions with the same winner are **not** equally certain — read the spread, not the label.
- `score` is a **probability-weighted position**, so it can land between levels (`1.99` is "almost exactly level 2"). Normalize it (`score / (n-1)`) before weighting.
- `confidence` is derived from the distribution (0 = torn/uniform, 1 = one option dominates). It is a property of _this_ distribution, **not** a calibration guarantee, and it is **not** the same as "how likely is this correct". Use it as a **gate**.
- Three gate signals exist; pick per question: `confidence`, raw top probability `p_max`, or the **top-to-second ratio** `p_max / p_second` (best when decisions come down to the top two).

## The Four Patterns That Cover Most Uses

1. **Speculative fan-out** — put _every_ question the decision tree might need in **one** request, including ones only relevant on some branches; let code ignore the irrelevant answers. Cheaper and faster than a second round trip.
2. **Confidence-gated routing** — answer tells you _what_; confidence tells you _whether to act_. `confidence < floor → human`; above the floor, each action gets its own threshold by consequence (checking a balance is safe at 0.6; approving a transfer needs 0.85+).
3. **Composite scoring** — break a fuzzy judgment into atomic Scores (e.g. python depth, leadership, design), normalize, and weight them **in code**. Change behaviour by changing weights, not prompts.
4. **Intent routing** — one Choice over intents → route to deterministic logic, a specialist LLM, or a human.

Full worked examples of all four, with code, are in `references/how-to.md`.

## Files

- **`references/where-to-get.md`** — every place to get a decision model: hosted APIs (TypeSafe, OpenRouter, Vercel, Codiv, Liquid, Upstage, OpenAI), local runtimes (llama.cpp, Ollama, Ollaya, vLLM/OpenJev, SGLang, von-sdk, ONNX, TurboLLM), the open checkpoint catalog with sizes and licences, SDKs per language, and benchmarks.
- **`references/api-variants.md`** — every surface side by side: TypeSafe, OpenRouter (two APIs), Vercel, Codiv, Liquid, Upstage, OpenAI, Ollama, Ollaya, llama.cpp, vLLM/OpenJev, SGLang, von, TurboLLM — plus the nuance checklist (model naming, option order, ceilings, error codes, confidence provenance).
- **`references/how-to.md`** — the request/response contract, how to write good questions and `criteria`, state design, confidence math, the four patterns with runnable code, error handling, calibration, and a pitfalls list.
- **`references/shortlist.md`** — a curated shortlist of real building blocks from the agent ecosystem: self-hosted runtimes and servers, SDKs by language, MCP servers, DB/SQL extensions, RAG/rerank adapters, and the agent-harness patterns (compaction, skill selection, permission gates, browser/computer use) with the actual repo names.
- **`references/use-cases.md`** — a big catalogue of decision shapes, industries, and real shipped projects with the numbers people reported.

## Common Pitfalls
1. **Bundling two decisions into one question** ("is this urgent _and_ who owns it"). Split them — you can't gate or route on a compound answer.
2. **No `other` option on a Choice.** Without one, the model is forced into the closest listed option even when none fit. Always include `other` when the set may not cover every input.
3. **Passing Choice criteria as an unordered map** where order matters, or asking a `Score` with <2 or >10 levels. Options are seen in the order you declare them.
4. **Reading `noul` near 0.5 as "medium".** It means the model can't tell; gate it.
5. **Chaining ripe questions into a second request.** If the questions could have been asked against the original state, ask them together.
6. **Trusting a raw confidence from a community checkpoint.** They're often uncalibrated; fit a threshold on your own labels first.
7. **Sending images/non-text to hosted Jev.** It's text-only; pre-process to text, or use a multimodal local checkpoint.
8. **Forgetting `NO_PROXY=localhost,127.0.0.1`** when pointing an SDK at a local server on a box with a system proxy (SDK reports a bogus 502).
9. **Pinning an alias when you've tuned thresholds.** `jev-latest` moves; pin the versioned id (e.g. `jev-1.13.0`) so a release can't silently shift your numbers.
10. **Assuming 400 means retry.** A capability/shape mismatch is `400`/`422` (or `501` on llama.cpp) — fix the request; only `429`/`529` are retry-with-backoff.
11. **Writing questions in the state's language instead of English.** `instructions`/`criteria` in English; `state` can stay native (see `references/how-to.md`).

## Verification Checklist

- [ ] Every question is one atomic judgment a person could make in a second.
- [ ] Choice questions that might not cover all inputs include an `other` option.
- [ ] Compound judgments are split into separate questions and recombined in code.
- [ ] All independent questions are in a single request (fan-out), not sequential calls.
- [ ] A confidence/probability gate exists for any action with real consequences.
- [ ] Questions and threshold constants live in one file for easy review.
- [ ] `instructions` and `criteria` are in English even when `state` is not.
- [ ] If using a self-hosted/open checkpoint, a threshold was fit on your own labelled sample.
