# Where to get a decision model

Everything below speaks (or converts to) the `POST /v1/systemone` wire format, so the request/response code in `how-to.md` is portable across all of it. You change one base URL and one model name.

> **Check your existing provider before anything else.** Decision models are being added to new providers constantly, and this list goes stale fast. If you already use an inference platform (OpenRouter, Vercel, Together, Fireworks, a cloud, a gateway, a local server), check whether it exposes a `decisions`, `systemone`, or `classify` endpoint — or any constrained typed-classification concept — before adopting a new dependency. It's often already there.

## 1. Hosted APIs (get a key, send HTTP)

| Source | Endpoint | Models | Notes |
| - | - | - | - |
| **TypeSafe AI** | `POST https://api.typesafe.ai/v1/systemone` | `jev-latest`, `jev-preview`, `jev-1.13.0` | The reference. Waitlist / console key. `$0.042` per M input tokens, output free. Best calibration. English-first. |
| **OpenRouter** | `POST https://openrouter.ai/api/alpha/decisions` (Decisions API) **or** `POST https://openrouter.ai/api/v1/systemone` (System One API, SDK-compatible) | **13 decision models** — Jev, Perplexity Decider, Liquid D1, Cloudflare Clef / Clef-flash, Together Tev1, Upstage Solar Decide, Inception Mercury Decide, Respan Span-01, Kev 4B (full list below) | Same OpenRouter key, no separate signup or waitlist. The TypeSafe Python/JS SDK works by setting its base URL. Every response carries `usage.cost`. |
| **Vercel AI Gateway** | `.../ai-gateway/models/jev` | Jev | Reachable with a Vercel AI Gateway key. |
| **Codiv** | `POST https://api.codiv.ai/v1/systemone` | `openjev-latest` (DiffusionGemma) | Hosts OpenJev. Free tier: 100M input tokens, no card. |
| **Liquid AI** | hosted `d1` | `d1` | Hosted decision model; accepts the TypeSafe request shape. |
| **Upstage** | `POST /v1/systemone` | Solar Decide (Solar Mini 4) | Beta. Reads decisions from label logits. Up to 26 options per question. Listed on OpenRouter too. |
| **OpenAI Decisions API** | limited preview | GPT-6 Luna | Fixed answer sets, text or image context. No public schema/pricing yet. **Not** the same product as OpenRouter's Decisions API. |

### OpenRouter's Decisions category (live — 13 listings)

**Gotcha:** OpenRouter's default model list **omits** decision models entirely. `GET https://openrouter.ai/api/v1/models` returns the text/image/audio models and *zero* decisions; they appear only when you filter by output modality:

```bash
curl 'https://openrouter.ai/api/v1/models?output_modalities=decisions'
```

The site shows the same set under its **Decisions** tab. Verified live:

| Model id | Name | Ctx | Inputs | In $/M |
| - | - | - | - | - |
| `typesafe/jev-1.13` | TypeSafe: Jev 1.13 | 32k | text | $0.042 |
| `~typesafe/jev-latest` | TypeSafe: Jev Latest (alias) | 32k | text | $0.042 |
| `perplexity/pplx-decider-v1-27b` | Perplexity: Decider V1 27B | 262k | text+image | $0.04 |
| `liquid/d1` | LiquidAI: D1 | 65k | text | $0.04 |
| `cloudflare/clef-flash` | Cloudflare: Clef Flash (9B, Qwen3.5-9B FT) | 65k | text+image | $0.09 |
| `cloudflare/clef` | Cloudflare: Clef (27B multimodal, Qwen3.8-27B FT) | 65k | text+image | $0.24 |
| `togethercomputer/tev1-4b-experimental` | Together: Tev1 4B (choice over 2–24 options) | 32k | text | $0.042 |
| `upstage/solar-decide` | Upstage: Solar Decide (Solar Mini 4) | 524k | text | $0.05 |
| `inception/mercury-decide:free` | Inception: Mercury Decide (free) | 32k | text | free |
| `respan/span-01` | Respan: Span-01 (behaviour scoring) | — | text | $0.02 |
| `respan/span-01-lite` / `:free` | Respan: Span-01 Lite (free tier) | — | text | free |
| `jaredpalmer/kev-4b` | Jared Palmer: Kev 4B (LoRA + pointer head on Qwen3.5-4B-Base) | 8k | text | $0.042 |

Every entry bills **$0/M output tokens** — input price is the entire cost. Note `typesafe/jev-router` sits under **chat**, not decisions (it routes prompts to other models), which is why it never shows in this category.

## 2. Local runtimes (run it on your own box)

All of these expose `/v1/systemone`, so existing clients work by changing the base URL. Point the TypeSafe SDK at them with `TYPESAFE_BASE_URL`, `TYPESAFE_API_KEY` (any non-empty value), `TYPESAFE_DEFAULT_MODEL`, and `NO_PROXY=localhost,127.0.0.1`.

| Runtime | Endpoint / port | Model source | Notes |
| - | - | - | - |
| **llama.cpp** (build b11361+) | `llama serve` → `:8080/v1/systemone` | HF GGUFs (`ggml-org/*`) | `llama serve -hf ggml-org/Kev-4B-GGUF`. Router mode loads models on demand; `/v1/models` lists ids. Errors `400`, `501`. |
| **Ollama** (v0.35+) | `:11434/v1/systemone` | `nimble` (9B Bespoke), `tev1` (4B), `tev1:0.8b` | `ollama pull nimble`. Local only for now. Also serves via the TypeSafe Python SDK (`TYPESAFE_API_KEY=ollama`). |
| **Ollaya** | daemon `:11435` → `/v1/systemone`, `/v1/decisions`, `/v1/models`, native `/api/decide` | pulls `winnow:e4b`, `laya`, `decider:2b`(+vision), NLI, GLiClass | "Ollama for decision models." Rust single binary, ONNX Runtime + llama.cpp for GGUF. Wire-identical to TypeSafe (SDK 0.7.1 works unchanged). `NO_PROXY=localhost,127.0.0.1`. |
| **vLLM via OpenJev** | `:8080/v1/systemone` | `openjev-latest` = DiffusionGemma 26B-A4B (NVFP4) | NVIDIA GPU (24GB+) or MLX on Apple silicon. `docker compose up`. Extensions: `images`, `steps`, `samples`, `think`, `sequential`. Apache-2.0. |
| **vLLM Jev** | `:8000/v1/systemone` | Valen, Open-Jev-2B, Laya, Tiny-Jev… | Native vLLM (Linux NVIDIA) + MLX/MPS (Mac preview). Selects a protocol per checkpoint. |
| **SGLang (openjev-sglang)** | `:30000/v1/systemone` | Qwen3.6-35B-A3B (prefill/logprob read) | TypeSafe-compatible endpoint over an existing model. |
| **von-sdk** | `von serve` → `/v1/systemone` | Von (395M, Apache-2.0) | Non-autoregressive encoder. CPU via OpenVINO, plus CUDA/ROCm/MPS. Python + TS SDK, real tokenizer counts, `von calibrate` to refit on your labels. |
| **ONNX Runtime** | in-process | Laya, von | Run from Node/TypeScript (Laya via ONNX Runtime) with no server. |
| **TurboLLM** | gateway `/v1/systemone` | Jev/NLI checkpoints | Runs Jev models as vLLM classifiers (`--runner pooling --convert classify`). Windows via WSL2. |
| **OpenDecisions (OneJev)** | `/v1/decisions`, `/v1/systemone` | OneJev (PyTorch or llama.cpp) | Can route low-confidence questions to hosted Jev. |
| **simple-jev (Featherless)** | `/v1/systemone` | any open LLM | Converts any open model into a typed classifier via next-token logits; no fine-tuning. Also `litjev`, `LLM2Jev`, `SemIf` (WebGPU), `llamajev` (wrapper on unmodified llama-server). |

**Rule of thumb:** on a laptop CPU, encoder models (Laya 421M, Von 395M, Verdict ~151M, Julia-1 144M) answer in **tens of ms**; 4B models (Kev, lev, Tev1) in **~100–400 ms**; a 26B diffusion model wants a GPU and gives **sub-100 ms per request** because it's non-autoregressive.

## 3. Open checkpoint catalog

Open decision models (mostly System One–compatible encoders or LoRA recipes). Sizes and licences where known — verify the licence at the source before commercial use.

**Read the backbone, not just the size.** Encoder checkpoints (mmBERT / ModernBERT / DeBERTa, roughly 150–400M) are speed anchors: deliberately narrow, best treated as fine-tuning bases or single-task specialists rather than general-purpose decision engines. Assume anything under ~2B is *intentionally limited* until proven otherwise on your task. The strongest zero-shot models are built by taking an existing chat model and **replacing its output head** — that backbone supplies the world knowledge and nuance. Rule of thumb: **broad or unseen → LLM-backed; narrow, fast, or at scale → small encoder, then fine-tune on your labels.** And don't write off a small model by size alone — test it on your exact decision first; the specialization cuts both ways.

**Small encoders (CPU-friendly, fastest):**
- **Julia-1** — 144M, mmBERT-small, 50+ languages, Apache-2.0, ~3 ms (llama.cpp)
- **Laya** — 421M, ModernBERT-large, English, Apache-2.0, ~5 ms; multilingual router variant
- **Verdict / openJev-verdict-2.0** — ~151M, ModernBERT-base, Apache-2.0
- **Von** — 395M, ModernBERT, Apache-2.0, non-autoregressive, CPU/OpenVINO; supports `von calibrate`
- **open-jev-deberta-v3-large** — DeBERTa-v3-large encoder
- **jeff** — GLiFormer-large (~400M)

**Mid-size (4B-class):**
- **Kev-4B** — 4B, Qwen3.5-4B-Base, Apache-2.0 (~12 ms), and **Kev-0.5B** LoRA variant
- **lev** — 4B, Qwen3.5-4B, Apache-2.0 (~36 ms)
- **Bespoke-Nimble-9B** — 9B LoRA on Qwen3.5-9B (Bespoke Labs); shipped in Ollama
- **Tev1** — 4B and 0.8B experimental (Together AI); choice-only on Ollama
- **reflex**, **openjev** (Qwen3.5-4B NLI), **Jeff 1**, **Decider-2B** (Qwen3.5-2B), **NanoJev** (0.6B + decision heads), **JevK5** (Qwen3.5-4B LoRA), **hopper**

**Large / multimodal:**
- **OpenJev** — 27B, Qwen3.8-27B, **text + images**, CC BY-NC 4.0 (non-commercial), ~43 ms
- **DiffusionGemma 26B-A4B** (NVIDIA/Google) — the base OpenJev uses; reads a diffusion canvas in one pass; Apache-2.0
- **CLM** — Qwen3-8B + contrastive heads; **Valen** (text+image); **Clef** (Cloudflare, hosted); **Winnow e4b** (Ollaya's recommended default); **djev-spark** (DiffusionGemma on DGX Spark)

**Hosted-only (no published weights):** Perplexity **Decider V1 27B**, Liquid **D1**, Upstage **Solar Decide**, Inception **Mercury Decide**, Respan **Span-01 / Span-01 Lite** (behaviour scoring — P(behaviour) per conversation span). Cloudflare's **Clef** and **Clef-flash** are *open-source* fine-tunes of Qwen3.8-27B (multimodal) and Qwen3.5-9B, served on Workers AI and available on OpenRouter.

**Where the catalogues live:** `modelsystem.one/models` (specs + pricing + status), the HF `ggml-org` *Decision models* collection, the `llama.cpp` server README, and the community indexes (`jevusers.com` — top-100 projects; the various `awesome-jev` lists).

## 4. SDKs and client libraries

| Language | Package | Notes |
| - | - | - |
| Python | `typesafe-sdk` (`pip`/`uv`) | Synchronous + async clients, `system_one(state=..., questions=...)`, retries/backoff by default. |
| JavaScript/TypeScript | `@typesafe-ai/sdk` | Typed `noul()` / `choice()` / `score()` helpers. |
| OpenRouter | TS / Python / Go SDKs | `alpha.decisions.create({...})`. |
| Pydantic AI | `TypeSafeModel` / `DecisionModel` | Give an agent an output type; Jev answers each field in one request with its own confidence; `FallbackModel` escalates to an LLM where Jev can't. |
| Haystack | `TypeSafe...` components | `DocumentClassifier`, `TextRouter` (with `min_confidence` → `low_confidence` output). `api_base_url` points at Ollaya/any server. |
| Rust | `typesafe-jev` | Typed client. |
| Elixir | `typesafe_api` | Typed client, concurrent fan-out, test stubs. |
| Java | `spring-ai-typesafe` | `TypeSafeClient`, batch API, per-request key. |

Raw HTTP always works. Note: **a chat-completions SDK will not work** — decision models are not an OpenAI-compatible chat endpoint.

## 5. Benchmarks & evaluation

- **Decision Index** (`github.com/apolinario/decision-index`) — the community benchmark for typed decision engines (40 benchmarks across 5 areas, chance-corrected). Ships a runner with an `http` engine for any `/v1/systemone` server, plus `transformers`. Reproducible locally or as one HF Job.
- **JevBench** — the leaderboard behind several model cards (intelligence / calibration / speed / cost, composite score).
- **Decision Index static page** and the HF Decision-models collection — quick visual comparison.
- Published reference points (verify before quoting): Jev 1.13 latency ~0.65 s p50 on the board; Von 1.2 ~0.34 s p50 on CPU; encoder-class models answer in tens of ms.

**Before trusting any open checkpoint:** fit a threshold on your own labelled sample. Several are explicitly uncalibrated, so a `confidence` of 0.8 is not 80% until you've measured it (von ships `von calibrate labels.jsonl` for exactly this).
