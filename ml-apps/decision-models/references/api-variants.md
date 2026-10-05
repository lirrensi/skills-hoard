# API variants — same three primitives, different surfaces

Every implementation below serves the **same three question types** (`noul`, `choice`, `score`) with the **same answer shapes**, because they all follow the System One wire format. What differs is the URL, the auth, the optional fields, the limits, the error codes, and how `confidence` is computed. This file is the diff table.

## The invariant (true everywhere)

Request keys: `state` (required), `model` (required on hosted; optional with a single local model loaded), `questions` (required, 1..N, keys chosen by you).

Answer shape per question type:

```json
"noul":   { "type": "noul",   "noul": 0.94 }
"choice": { "type": "choice", "choice": "billing", "probabilities": {"...": 0.0}, "confidence": 0.81 }
"score":  { "type": "score",  "score": 1.05, "legend": {"0": "..."}, "probabilities": {"0": 0.0}, "confidence": 0.92 }
```

`noul` has **no** `confidence`. `choice`/`score` always carry `probabilities` summing to 1 and a `confidence`. `usage.output_tokens` is normally **0** — a decision model generates no tokens.

## Surface-by-surface

### TypeSafe AI (reference implementation)
- `POST https://api.typesafe.ai/v1/systemone` · `Authorization: Bearer <key>`
- Response: `{ model, answers, usage: { input_tokens, output_tokens } }`. No `id`, no `cost` (billing is on your account).
- `model` in the response is the **resolved versioned id** (e.g. `jev-1.13.0`) even when you sent an alias.
- Aliases: `jev-latest`, `jev-preview`. Pin the versioned id once you tune thresholds.
- Limits: 1–256 questions; Choice 1–255 options; Score 2–10 levels; 32k state+longest question, 64k total; text only.
- Errors: `401`, `422`, `429`, `529`. SDKs retry `429`/`529` with backoff.

### OpenRouter (two surfaces, one key)
- **Decisions API** — `POST https://openrouter.ai/api/alpha/decisions`. Body = the standard shape **plus** `provider` (`{allow_fallbacks}`), `session_id`, `trace`, `user`. Response **adds** `id` (e.g. `gen-dec-...`), `provider`, and `usage.cost` (billed in USD). Path is `api/alpha/...`; also mirrored for their TS/Python/Go SDKs.
- **System One API** — `POST https://openrouter.ai/api/v1/systemone`. Wire-compatible with the TypeSafe SDKs (point `TYPESAFE_BASE_URL=https://openrouter.ai/api`). Bare ids (`jev-1.13`, `jev-latest`) are mapped onto the `typesafe/` namespace.
- Models: `typesafe/jev-1.13`, `~typesafe/jev-latest`; `typesafe/jev-router` is a **chat** router, not a decision endpoint.
- `usage.cost` present; output free.

### Vercel AI Gateway
- Reaches Jev with a Vercel AI Gateway key, no separate TypeSafe signup. Same System One shape.

### Codiv
- `POST https://api.codiv.ai/v1/systemone` — hosts **OpenJev** (DiffusionGemma). Free tier 100M input tokens. Accepts `jev-latest`/`jev-preview` aliases so SDK defaults work.

### Liquid AI · Upstage · OpenAI
- **Liquid `d1`** — hosted, accepts the TypeSafe request shape.
- **Upstage Solar Decide** — beta `/v1/systemone`; reads decisions from single-token label logits; **max 26 options** per question (vs 255 elsewhere). Also listed on OpenRouter.
- **OpenAI Decisions API** — limited preview on GPT-6 Luna, fixed answer sets, text or image context. No public schema/pricing; **a different product** from OpenRouter's Decisions API. Don't assume wire compatibility.

### Ollama (v0.35+)
- `POST http://localhost:11434/v1/systemone` · `model`, `state`, `questions`.
- Models: `nimble` (9B, Bespoke), `tev1` (4B) / `tev1:0.8b` (Together). `ollama pull nimble`.
- Works with the TypeSafe Python SDK: `TYPESAFE_BASE_URL=http://localhost:11434`, `TYPESAFE_API_KEY=ollama`, `TYPESAFE_DEFAULT_MODEL=nimble`.
- Nuance: `tev1` is **choice-only** in the catalog — its `noul`/`score` shapes come from Ollama's candidate scoring, not the model's training.

### Ollaya ("Ollama for decision models")
- `POST http://localhost:11435/v1/systemone`; also `/v1/decisions` (alias), `/v1/models`, and a **native** `/api/decide`.
- Native extras (ignored by `/v1/*`): `keep_alive`, `extras` (`["laya"]` adds extra confidence/act fields), `images` (vision model), `preset`, plus routing/timings on `/api/decide` (`total_duration`, `load_duration`, `eval_duration`).
- Wire-identical to TypeSafe — the official SDK 0.7.1 runs unchanged. A key is required by the SDK but any value works unless the server sets `OLLAYA_API_KEY`.
- Nuance: tiny models have **short contexts** (e.g. 512–1024 tokens including the questions). Oversize state → `422 STATE_TRUNCATED` on `/v1/*`; `/api/decide` truncates and flags `state_truncated` instead.
- Nuance: `model` in the response may differ from what you sent (a router resolves, e.g. `laya` → `laya:en`).

### llama.cpp (build b11361+)
- `llama serve -hf ggml-org/<Model>-GGUF` → `POST :8080/v1/systemone`.
- Single model loaded ⇒ the `model` field is **ignored**. Router mode ⇒ pick per request; `/v1/models` lists ids.
- Extra: `images` (base64 / `data:` URLs), and `state` may be a list of chat messages where any `image_url` part is read as an image (needs `--mmproj`).
- Errors differ from hosted: **`400`** invalid request, **`501`** unsupported model/image config. Do not retry these as if they were congestion.
- Probabilities are a softmax over option-label logits — **not** RLCD-calibrated.

### vLLM · OpenJev
- `POST :8080/v1/systemone`; DiffusionGemma 26B-A4B read as a diffusion canvas (one denoise step, logprobs at each answer slot).
- Extra fields (OpenJev additions; a request without them behaves exactly like Jev): `images`, `steps` (1–8), `samples` (1–32), `think` (0–4096 tokens), `sequential`. `think`/`sequential` require a text state.
- Aliases `jev-latest`/`jev-preview` accepted; a **pinned** id like `jev-1.13.0` returns `400 Unknown model`.
- Errors mirror Jev: `422` validation, `400` plain-text reason / `api_usage_error`, `429`, `529`; auth errors as `{"detail": {"error_type", "message"}}`.
- `Server-Timing` header per response; many questions are read in parallel chunks (~12/read).

### von (`von-sdk`)
- `von serve` → `/v1/systemone`, byte-compatible with the spec; SDKs switch via `VON_BASE_URL`.
- Extras beyond the spec (clients may ignore): real tokenizer `usage.input_tokens`, a `truncation` field + `X-Von-Truncated`/`Warning` headers on middle-truncated state; `--on-overflow refuse` returns `422` instead of truncating.
- `VON_API_KEY` enables bearer auth (clients fall back to `TYPESAFE_API_KEY`).
- Nuance: `noul` is returned in a **fixed band**; the pre-band `noul_raw` is what carries gate signal. `von calibrate` refits the confidence map on your labels.

### SGLang · TurboLLM · OpenDecisions · litjev / simple-jev
- **openjev-sglang** — `/v1/systemone` over Qwen via prefill/logprob read.
- **TurboLLM** — its **own** `/v1/systemone` implementation (not proxied to an engine). `model` is required; `jev-latest` alias resolves to the loaded/verified Jev model. Also `POST /v1/classify` (premise + hypotheses) and `POST /v1/rerank` (Cohere/Jina shape). Errors: `400 not_a_jev_model`, `422 invalid_request`, `503 model_not_loaded`. Needs vLLM (Linux or WSL2).
- **OpenDecisions (OneJev)** — `/v1/decisions`, `/v1/systemone`; can route low-confidence to hosted Jev.
- **litjev / simple-jev / LLM2Jev / SemIf / llamajev** — wrappers that read option-letter logits from a frozen LLM; uncalibrated by default.

## Nuance checklist (the things that actually bite)

1. **Model naming.** Hosted: alias or versioned id. OpenRouter: `typesafe/` namespace, bare ids mapped. Local: server-specific ids; some accept `jev-latest`, some reject pinned ids. Always read back the `model` field — it tells you what really answered.
2. **Option order matters.** Criteria are shown to the model in declaration order; on some servers a different order can flip a decision. Use ordered lists, not maps, where it matters.
3. **Option/level/question ceilings differ.** 255 options (Jev) vs 26 (Solar Decide) vs 24 (Verdict); 256 questions/request vs 64; Score is 2–10 levels on hosted, other servers may differ.
4. **Context budget.** Jev: 32k state+longest question / 64k total. Tiny encoders: 512–1024 tokens *including the questions*. Oversize → truncation (flagged) or an error, depending on server.
5. **Extra modality.** Hosted Jev is text-only. llama.cpp / OpenJev / Ollaya accept `images` when the checkpoint supports vision.
6. **Confidence provenance.** Hosted Jev is calibrated (RLCD). Wrappers use entropy (`1 − H/ln K`) or raw softmax — treat as relative, not absolute, until calibrated on your data.
7. **Error codes are not universal.** Hosted `422`; llama.cpp `400`/`501`; Ollaya `422 STATE_TRUNCATED`; OpenJev `400`/`422`/`429`/`529`. Only `429`/`529` are retryable.
8. **`usage` fields vary.** `input_tokens`/`output_tokens` are standard; `cost` is OpenRouter-only; `output_tokens` is 0 on decision models unless a `think` extension runs.
9. **Aliases move.** `jev-latest`/`~typesafe/jev-latest` track releases; pin the versioned id if your thresholds depend on a specific model.
10. **Chat-completions SDKs don't work.** These are not OpenAI-compatible chat endpoints — use the decision SDKs, the OpenRouter Decisions SDKs, or raw HTTP.
11. **Backbone, not size.** Parameter count is not quality. Most sub-2B models are deliberately limited (fine-tuning bases or single-task specialists); the strongest zero-shot decision models are chat models with the output head replaced. Broad/unseen → LLM-backed; narrow/fast → small encoder plus your own labels.
12. **Aggregators hide decision models.** OpenRouter's default `GET /api/v1/models` returns **zero** decisions — you must filter: `?output_modalities=decisions`. Anything that lists "models by modality" may put decisions in a category you didn't know existed. Check the *decisions* bucket, not just the provider list.

## Framework integrations (same wire, typed at the edges)

- **Pydantic AI** — `TypeSafeModel` (subclass of `DecisionModel`). Give an agent an output type; each field becomes a question (docstring = the question, `Enum` member docstrings = option meanings, `BoolCriteria` = a noul's meaning). Answers arrive as values of the type, each with its own confidence; `FallbackModel` sends the fields Jev can't answer to a language model. `decision_boolean_threshold` / `decision_route_threshold` control gating. No sampling knobs; `extra_body`/`extra_headers` forwarded.
- **Haystack** — `TypeSafeDocumentClassifier` (answers stored under `meta[field]`, failed docs flagged) and `TypeSafeTextRouter` (one Choice over labels, optional `min_confidence` → `low_confidence` output). `api_base_url` points at Ollaya or any compatible server.
- **Spring AI (Java)** — `TypeSafeClient`, `systemOne` overloads for text/object/array, concurrent batch API, per-request key resolution, retries, typed exceptions, `x-typesafe-request-id` header.
