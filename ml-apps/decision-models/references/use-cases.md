# Use cases — what people actually build

A catalogue to mine for ideas. Every entry maps to one of the primitives (Noul / Choice / Score) and usually one of the four patterns in `SKILL.md`.

## The thesis: most business logic is a classifier

Roughly **half of business logic — some argue up to 80% — is nothing but "stupid classifiers"**: is this spam, which queue, is it urgent, does this match, is it safe. Traditionally that logic is a pile of hand-written rules, regexes and `if` chains that rot the moment reality gets weird. A decision model *is* that layer, done properly: the same stupid classifier your code always wanted, except it reads language, returns a probability, and doesn't need you to enumerate every case by hand.

The scoping consequence is the useful part: **find the `if` whose condition is a judgment about text, and hand that one condition to a decision model.** Leave control flow, permissions and side effects in code. That single move is where most of the value sits — not in replacing the workflow, and not in "an AI agent", but in one conditional.

## The six workflow surfaces (a starting taxonomy)

A second, smaller framing of the same architecture — useful as a checklist of where a first deployment goes:

| Surface | Decision to make | Typical action | First question |
| - | - | - | - |
| **Inbox triage** | which queue, priority, escalation path fits | route, prioritize, ask for missing info | "Which approved queue owns this case?" |
| **Model & tool routing** | which capability should run next | select a path or a safe fallback | "Which capability is sufficient for this request?" |
| **Prompt safety** | is the next instruction allowed, risky, conflicting | allow, review, block | "Should this request pass the policy gate?" |
| **Answer quality** | is the answer grounded, relevant, complete | return, revise, escalate | "Does the answer meet the release criteria?" |
| **Agent reliability** | did the agent finish the task with evidence | accept, retry, request human review | "Is the task complete and instruction-compliant?" |
| **Knowledge grounding** | is retrieved context sufficient to answer | generate, retrieve more, abstain | "Is there enough evidence for a supported answer?" |

All six are the **same architecture** with a different state and a different action — start where an approved action space already exists (triage, severity, routing), and leave payments, deletion and privileged changes for last.

## Decision shapes → reach for it when

| Shape | When | Examples |
| - | - | - |
| **Classification** | one known category should win | intent, topic, department, risk type, entity type |
| **Detection** | you need P(a property is present) | spam, fraud, urgency, jailbreak, sensitive data |
| **Scoring** | the answer belongs on an ordered rubric | severity, relevance, quality, frustration, suitability |
| **Routing** | a category selects the next code path | tool use, escalation, model routing, support queues |
| **Search** | find items matching a natural-language query | semantic search, document discovery, candidate generation |
| **Retrieval** | a workflow needs the most relevant context | RAG context, evidence retrieval, knowledge lookup |
| **Ranking** | items must be ordered by relevance/quality | search results, recommendations, prioritization |
| **Verification** | an artifact must be checked for failure modes | citation support, policy violations, tool-call errors |
| **ML feature extraction** | a downstream classical model needs semantic signals | purchase intent, churn signals, competitive pressure |
| **Structured data extraction** | known fields must be recovered from unstructured input | attributes, order fields, document labels |

## Industries (from TypeSafe's use-case map)

- **Customer support** — classify tickets by issue/product/intent; detect urgency, frustration, churn risk, refund requests; route to team/queue; verify responses against policy.
- **Moderation & trust & safety** — apply nuanced company-specific criteria; combine severity × confidence to allow / warn / review / block; detect toxicity, spam, fraud, unsafe advice, PII exposure, opt-outs.
- **LLM guardrails** — screen every input, output, and tool call at a fraction of the LLM cost; detect jailbreaks, prompt injection, policy violations, tool-call errors; log structured probabilities.
- **Model routing / harness engineering** — classify intent, domain, difficulty, risk; choose which LLM gets the prompt; escalate only what needs the expensive model.
- **Search, retrieval, ranking** — rerank with pairwise comparisons; select RAG context; semantic search + ranking at scale.
- **Scientific discovery** — screen papers against inclusion/exclusion criteria; label passages by theme; check whether cited passages support claims; flag missing methodological detail; build research knowledge graphs.
- **Recruiting & lead gen** — score evidence for competencies; match candidates to roles; score ICP fit, buyer relevance, purchase intent.
- **Insurance, financial crime, risk** — classify claims/transactions/KYC docs; detect fraud indicators; score severity; prioritize and route.
- **Legal & compliance** — classify contracts/filings/claims; detect missing clauses and prohibited claims; verify against requirements.
- **E-commerce** — normalize product catalogs; extract attributes; detect counterfeits, review abuse, prohibited listings.
- **Advertising, gaming, demand forecasting** — brand safety, creative quality, ad-to-landing alignment; chat moderation and player-support routing; semantic demand signals feeding forecasts.
- **Graphs / knowledge graphs** — classify relationships and entity types; detect contradictions; probabilistic traversal.
- **Semantic code linting** — encode team conventions/guidelines as questions and run them in CI.

## The full range of possibilities — the community taxonomy (~570 entries)

The best single place to browse what people actually build is the community index **`yibie/awesome-jev`** (ranked, sourced, one entry per category; its README aggregates every category file, and it's mirrored by several sibling `awesome-jev` lists — AnotiaWang, cobanov, heyjunpenn, AbdelStark, logicrw). Its 15 categories are the cleanest map of the space, and the entry counts show where the energy is:

| Category | Entries | What lives there |
| - | - | - |
| **Infra / SDKs / Integrations** | 102 | servers, SDKs, wrappers, MCP connectors, harness plumbing |
| **Related Practices / Discussions** | 102 | threads, interviews, blog posts — practice signals with no standalone repo |
| **Classification & Routing** | 62 | document/entity/intent classification; model and queue routing |
| **Agent Decisions** | 60 | agent loops, tool gating, memory, context OS, permission prompts |
| **Calibration & Research** | 50 | open reproductions, calibration studies, training recipes |
| **Verification & Guardrails** | 47 | citation checks, injection screening, policy enforcement |
| **Scoring & Ranking** | 40 | rubric scoring, rerankers, relevance/quality judges |
| **Evaluation & Benchmarking** | 35 | harnesses, leaderboards, playgrounds |
| **Game & Simulation** | 25 | GameBoy / Mario / Doom agents, simulation controllers |
| **Adaptive & Realtime UI** | 10 | interfaces that reshape themselves as you type; live adblock-style decisions |
| **Data Labeling & Curation** | 10 | using decisions to align and curate datasets |
| **Robotics & Physical** | 9 | embodied controllers, physical harnesses |
| **Finance & Trading** | 8 | per-block trading decisions, market tooling |
| **Content Moderation** | 8 | moderation bots, spam evals |
| **Compliance & Legal** | 2 | policy engines, legal forecasting — **the emptiest room in the house** |

Two axes that are easy to miss and worth a look: **Adaptive & Realtime UI** (a decision model fast enough to restructure a form or screen *as you type*) and **Robotics & Physical**. And **Compliance & Legal** sits at 2 entries — the least-explored corner, i.e. where the opportunity is.

*Caution:* these indexes apply **inclusion rules only** — public, citable, genuinely uses a decision model. A listing is not an endorsement of code quality, security, or whether the thing runs at all. Read the entry, then check the repo.

## Real shipped projects (with reported numbers)

The public ecosystem is large (the `jevusers.com` catalogue tracks 250+ projects; the `awesome-jev` lists index 1000+). A representative slice:

**Cost/latency wins**
- **Tax document classifier** — page classifier across 261 IRS forms, reported **100% strict accuracy**, **~$0.001/page**.
- **Computer use** — OCR the screen, then let the model pick the click target from a fixed action set: **~$0.0002/step**, which is what makes high-frequency UI automation viable (`Sac-Y/Jev-cu`).
- **Browser agents** — `browser-use/jev-ultrafast`: the decision model picks action + DOM element; a small model fills text only. Google Flights demo finishes in seconds.
- **Parallel questions cookbook** — a 13-question regulatory briefing over one document: **12.2× cheaper and 10× faster** batched into one call, identical answers.
- **Verified cascade** — decision model as a cheap verifier in front of a big model to cut LLM cost.

**Agents & coding harnesses**
- **Tool-call gating** — `pi-jev`: a measured tool-call gate plus `jev_ask` for typed answers inside the Pi coding agent.
- **Permission prompts** — auto-approve coding-agent permission prompts via cheap typed decisions (OpenRouter cookbook).
- **Model routing** — `gargpratyush/jev-router`, `vexjoy-agent`: pick cheaper vs stronger model per task; cut agent inference cost.
- **Context compaction** — `tamaratran/fast-jev-compaction` decides which tool calls/results are stale and deletes them; `jev-pruner` trims long Bash output before the model sees it.
- **Drift detection** — `thruwire/foreman` watches Codex/OpenCode for drift, stalls, missing tests, premature exits, then decides continue / verify / retry / escalate.
- **Code review** — `devagrawal09/jev-review` reviews a diff or codebase for correctness, security, compatibility, coverage.
- **Deterministic skill/route selection** — pick at most one skill for a turn out of a large catalogue (rank all, then re-check the top few against their full text).

**Verification & RAG**
- **Citation checking** — does the quoted context actually support the claim? One Choice; catches hallucinated citations.
- **RAG passage gating** — Score each retrieved passage in one request, then decide in code which reach the answering model.
- **Reranking** — 30-passage BM25 shortlists for 40 legal queries: one question per query-candidate pair raised top-1 from **5% → 18%** and top-10 from **38% → 62%**.
- **Line-by-line semantic search** — score 218 line ids against a plain-language query in a single request.
- **Semantic grep** — `uehaj/jev-semgrep`: score every line against a meaning; combine meanings with AND/OR/NOT.

**Structured data & extraction**
- **Date extraction** — extract the parts, resolve and validate in code with confidence-based review.
- **Pre-parsed value extraction** — regex finds candidate emails/phones/amounts; the model selects the requested span so code normalizes a verbatim value.
- **Hierarchical classification** — parallel beam search over Choice probabilities through deep patent/product/biomedical hierarchies.
- **Structure recovery** — reconstruct markdown from plain text: one request stitches hard-wrapped lines, another classifies each block (heading/list/code/callout).
- **Entity alignment** — match 450 candidate pairs from two product catalogues with a Score plus companion Nouls that surface which fields disagree.
- **Function calling** — map natural-language requests to ordinary typed functions by turning names and closed-set arguments into confidence-aware questions.

**Data-science / ML**
- **Feature extraction** — turn free text into probabilistic features, then train a classical model (CatBoost) on them; an autoresearch loop proposes questions and prunes by predictive value.
- **Big-data map-reduce** — classify or score giant corpora (agent traces, documents) far more cheaply than per-doc LLM calls.
- **Confidence-driven taxonomy** — classify SEC filings into 75 industry groups; when the answer is unsure, report the broader parent division instead.

**Perception / control loops**
- **Games** — Von plays Doom from a text rendering of the depth buffer, one forward pass per action; TypeSafe-Mario plays SMB from structured emulator state; Minecraft agents use a decision-model controller.
- **Mobile / desktop agents** — `droidrun/mobile-jev` decides each phone step; chat-overlay assistants read the screen (local OCR) and propose reply candidates.
- **Trading / real-time** — a decision per Monad block on a DEX; streaming ASR word-by-word judging.

**Perception → decisions without ASR**
- **Prosodia** — audio-native, Jev-shaped decisions processed directly from audio, no text decode.

## Agent-harness decisions — the richest vein (measured)

The biggest payoff is making the agent's **own** machinery cheap: the decisions it makes about itself, thousands of times a day. Real numbers from an open MIT skill pack that wires a decision model into an agent (Hermes / Claude Code / Codex) across **11 skills** (`kerpopule/hermes-jev-skills`, ~1k stars):

| Decision | What the model decides | Measured |
| - | - | - |
| **Model routing** | which model is good enough for this turn | ~0.4 s/turn |
| **Search** | which results to open, whether the evidence answers the question, which query to try next | ~1.9 s/round (2 requests) |
| **Memory** | which retrieved passages are worth reading, and which carry hidden instructions | 60 passages/request, up to 480/call |
| **Compaction** | which turns to keep when a transcript must be cut to size | 71 turns in 0.95 s; beat recency 11 questions to 4 |
| **Skill selection** | which installed skill this turn needs, or none | 377 skills in ~2.8 s |
| **Triage** | urgency, kind, and whether a person must see it | ~0.4 s, **$0.00006**/message |
| **Mailbox sorting** | which lane a message belongs in; worth a person's attention | ~0.44 s p50, **$0.00002** each |
| **Computer use** | the next GUI action, from a table of pre-vetted actions | ~0.5 s/decision |
| **Browser use** | the next page action, same contract | ~0.4 s/step |
| **Web screening** | which parts of a fetched page carry instructions aimed at the agent — withheld before it reads them | **70 of 79** planted attacks caught vs 11 for the host's own pattern scan; **0 of 1,520** clean chunks withheld; ~0.2 s/result |

Juicy takeaways worth stealing:

- **Fail open, always.** No key, timeout, rate limit, bad reply, or low confidence → keep the current model, return the original list, drop nothing, suggest nothing. A decision layer must never be able to block the turn; the worst case is the time budget (a few seconds).
- **Rails that don't depend on the model being right.** Risk words (production, delete, migration, security, payment, legal) never route to the cheapest tier; a large context never switches to a cheaper model mid-session; a turn is only dropped on a *confident* answer; and the model may only ever return an action id **you** put in the table.
- **Start in shadow mode.** Decide and *log* (tier, model, confidence, latency) without switching anything — a day costs almost nothing and risks nothing. Promote when the log looks right, but remember a *quiet* log proves nothing: bound the trial by the clock, not by a request count.
- **A negative result, honestly reported.** A handoff summary built from the model's keep/summarize/drop digest recalled **less** than one written from the plain transcript (37.5% → 58.7%, or 68.3% → 75.0% with one search). Not every decision belongs to the model — the shipped version sends the whole dialogue plus a way back.
- **Prompt-injection defense is a decision, not a regex.** One cheap request per fetched page caught 70/79 planted attacks where a pattern scan caught 11, and withheld nothing from 1,520 clean chunks.
- **Cheap enough to run on everything.** At $0.00002–$0.00006 per decision, the economics flip from "sample it" to "classify all of it" — every message, every turn, every passage.

**Where to browse more:** `yibie/awesome-jev` (~570 entries in 15 categories — the best organised), `ayautomate.com/jev-builds` (**1,305 public builds** from launch week, each scored by the model itself on specificity / real-build / verifiability / hype / exaggeration), `jevusers.com` (ranked project index), `modelsystem.one` (catalogues + benchmark), the sibling `awesome-jev` lists (AnotiaWang, cobanov, heyjunpenn, AbdelStark, logicrw), the HuggingFace practical guide to typed decisions, OpenRouter's Jev cookbooks, and TypeSafe's own cookbooks (guardrails, rerank, citation check, SDE cascade, hierarchical classification, autoresearch feature discovery, classification-using-confidence).

### Launch-week numbers (posters' own claims — nobody re-ran them)

Unusually for this ecosystem, the aggregate page publishes its **counterpoints** alongside the wins. Both kinds, attributed:

- **1,018 AI research papers classified for $0.08 total**, 256 ms median per paper — the *summaries* cost $3.99. Author's takeaway: "different models for different parts of the workflow."
- **PostgreSQL `jev()`**: 129 rows judged in ~1 s for **$0.0009**; 6 ms on the cached second run.
- **Rerank (LlamaIndex)**: nDCG@5 **0.340 → 0.396** at ~$0.0003/query (author cautions the first-stage retriever was weak).
- **Browser agent**: found flights in **7 s for $0.0039** — a new action space each step, small LLM fallback for typing.
- **Ad-tech eval vs a frontier model**: claimed **64× lower cost, 5.4× lower latency**; few-shot quality similar, zero-shot mixed (synthetic data, per the author).
- **Traffic simulation**: ~350 ms per junction decision, ~**$0.001 per minute** of simulated traffic.
- **Rubik's cube**: 94 moves (a human beginner method, not the 22-move optimum), ~250 ms/decision, ~4 s of model time total.
- **Counterpoint — memory relevance check**: same accuracy and much faster (708 ms vs 5,690 ms) but the fallback route made it **27% costlier**.

Read that last one twice: a decision model bolted in front of a fallback can be **faster but more expensive** than the thing it replaced. Measure cost, not just latency.
