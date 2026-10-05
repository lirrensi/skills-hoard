# Shortlist — real building blocks people have already built

Curated from the community index (`yibie/awesome-jev`: **Infra / SDKs / Integrations — 102 entries**, **Agent Decisions — 60 entries**). Grouped by *job to be done*, so you can find the thing you need without reading 162 links. Almost all of it is small, MIT, and copyable.

## Self-hosted runtimes & servers

| Project | What it is |
| - | - |
| **Ollaya** | Daemon serving open decision models behind a wire-identical `/v1/systemone` (ONNX + llama.cpp). "Ollama for decision models." |
| **llama.cpp** | Native `/v1/systemone` for GGUF decision models (Laya, Julia-1, Kev-4B, lev, OpenJev). |
| **simple-jev** (Featherless) | Turns any open model into a Jev-compatible classifier endpoint. |
| **FastJev** / **jev-style** / **Qwev** | Self-hosted Python SDK + compat API; `pip install jev-style[torch\|mlx]`; training-free Jev-style from dense Qwen checkpoints. |
| **jeff** (logan-markewich) | Self-hosted drop-in replacement on GLiFormer. |
| **stuntd** / **djev-run** / **cu-Jev** | Jev-compatible local server on Laya; DiffusionGemma-Jev on Cloud Run GPU; CUDA-native System One API. |
| **laya-mlx** / **laya-Ascend** / **intern-decision-mlx** | Platform ports: Apple MLX, Ascend NPU, and an open 0.8B *vision* decision model. |
| **jev-switch** / **rotom** / **Jevview** / **Tiltmeter** | Routers, OpenAI/Anthropic-compatible gateways, a live visualizer, and a monitoring proxy that records every decision. |
| **jevcache** / **GPTCache** | Memoize decisions — a repeated question is served from cache (6 ms vs ~1 s). |

## SDKs by language

Official: **Python** (`typesafe-sdk`, `system-one-adapter-python`), **JS/TS** (`@typesafe-ai/sdk`), **Rust**, **Pydantic AI**, **Spring AI / Spring Boot starter**, **LlamaIndex adapter**, **Vercel AI SDK (Python + CLI + `eve`)**.

Community, by language: **Go** (×2), **Rust** (×2), **Elixir** (GenServer), **Ruby** (×3 — incl. `hunch`: `if Hunch.likely?("fraudulent", ...)`), **Java/Kotlin/Scala** (JVM ×4), **PHP** (Laravel + Symfony), **Swift** (incl. Apple Foundation Models bridge), **C++** (C++20 with compile-time enum schemas), **.NET** (×2), **Clojure**, **PowerShell**, **Effect** (TS), **Clojure**, **`discern`** (Effect), **`JevFlow`** (composing decisions into deterministic flows).

**Interop and trust:** `jevcompat` — a **48-requirement spec of the `POST /v1/systemone` wire contract**, each requirement tested. `jev-trust` — middleware that logs every typed decision and measures trust. `decision-gate` — routes every request in a loop through cost/rate control. `metajev` — keeps the full distribution behind each answer.

## MCP servers (drop a decision layer into any agent)

`jev-mcp` (×4 forks, ~11 judgment tools), `jev-use` (Claude Code / Codex / Pi), `typesafe-mcp` (Go), `decide-mcp` (bias-profile routing), `openrouter-jev-mcp`, `Jevbridge` (ACP + MCP for Codex/Claude/Grok), `jev-mobile` (Android control loop).

## Databases & data platforms

`jev4pg`, `pg-jev` (PostgreSQL predicate extensions), `duckdb-jev`, `sqlite-jev` (loadable C extension), `mysql-ailike`, `jevql` (**run plain SQL on a vanilla Postgres with no schema change**), `Databricks AI Decide` (`ai_decide` as an AI Function), **Milvus Model** (batch candidate Noul questions → ranked list).

The `jev()` pattern is the headline: `WHERE jev(people, 'could work from home')` — **129 rows judged in ~1 s for $0.0009**, second run 6 ms from cache.

## Retrieval, RAG & reranking

**LlamaIndex Jev** (Score each retrieved passage), **JevRerank** (`nDCG@5 0.340 → 0.396` at ~$0.0003/query), **Milvus bootcamp notebooks**, `discern`, and `advocaat` (ask questions about a dataset).

## Agent-harness patterns (the richest seam)

The same handful of jobs, implemented dozens of times for Claude Code, Codex, Pi, Cursor, OpenCode, DeepSeek Harness, OpenClaw:

- **Context / compaction** — `fast-jev-compaction` (Claude Code), `fast-dev-compaction` (Codex), `pi-fast-jev-compaction`, `opencode-jev-compaction`, `jev-compaction`, `jev-pruner` (trim long Bash output), `yoshi` (judge which conversation turns matter), `Hermes JIT Context OS` (System 1 epistemic gate + domain router).
- **Skill / tool selection** — `jev-skill-suggester`, `SkillRanker` (Rust), `jev-superpowers`, `pi-jev`, `pi-typesafe-router`, `dsh-jev-decide`, `jev-judgment`, `jev-opus`, `oh-my-claudecode`.
- **Permission & stopping gates** — `jev-auto-approve` (PreToolUse Noul on shell commands), `dsh-auto-mode`, `jev-belay` (Stop hook that checks the transcript for evidence), `limpet` (stops the agent finishing too early), `wakegate` (before resuming a sleeping agent), `super-jev` (turn an answer into a *bounded action*).
- **Browser & computer use** — `Jev Ultrafast` (browser-use), `fastbrowse`, `Jev Browser`, `Jev for Chrome`, `jev-desktop` (Codex Computer Use), `Yappy` (macOS voice, one Choice per step), `jev-browser-use`, `Jev-cu`, `WebJev` (Qwen3.5-35B-A3B fine-tune), `Sedum`, `GUI JEV Harness` (recursive screenshot grid grounding), `BrowserClaw`, `public-browser`, `laya-browser-agent`, `mobile-jev`, `jev-browser-bridge`.
- **Loop / runtime control** — `Atomic`, `jcode`, `JevLoop` (×2), `AutoGPT`, `Eliza`, `JarvisCore` (multi-agent runtimes with first-class decision providers).
- **Judgment & evidence** — `DeepSearcher stopping-policy` (Noul on accumulated evidence), `neo4jev` (hop-by-hop graph navigation), `DataJev` (LLM analyses, decisions read the compressed result), `Visual-JEV` (image input, no OCR step).
- **Language surface** — `hono-jev-router` (route HTTP by meaning), `grev` (grep by meaning: `grev 'is a vegan menu item'`), `SemDecide` (decisions in shell pipelines and CI).

## Tooling for the work itself

- **`jevkit`** — Rust CLI that **validates Choice/Score/Noul question sets** (13 checks). Use it before shipping a policy.
- **`jevify`** — an agent skill that *finds where a codebase could hand a decision over* and designs the typed questions.
- **`jev-architect`** — finds, designs and evaluates decision loops.
- **`typesafe-ai/skills`** + **`Building with TypeSafe Jev`** — installable skills for Claude Code / Codex marketplaces.
- **`Jev Showcase`**, **`jev-usecases`**, **`Jev AI Tools`**, **`jev-experiments`** (22 latency-focused apps) — runnable pattern galleries.
- **`Jev by Example`**, **`Learn Jev end to end`** (12-notebook Python course) — teaching material.

## How to use this list

1. Find the **job** (compaction, gating, routing, browser, DB search, RAG).
2. Read the one project that does it — most are a single file or one hook.
3. Copy the *pattern*, not the dependency: they all reduce to **state → typed question → code acts**.
4. Validate your question set (`jevkit`), fit a threshold on your own labels, then run it in shadow mode (see `how-to.md`).
