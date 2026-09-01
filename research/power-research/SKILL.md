---
name: power-research
description: >
  Two-mode research methodology (Plan + Collect) that builds an interrogable corpus,
  not a dead document. Use when the user wants to research something — investigate,
  gather information, "let's research X", "look into Y", "find out about Z", "I need
  to understand". Trigger on any request that needs sustained information gathering
  and synthesis, especially when the user has a vague goal they want to sharpen first.
  Also triggers on "power research", "research procedure", or when the user references
  the Power Research workflow.
---

# Power Research

*A two-mode research methodology. You plan. I collect. You decide when it's enough.*

## The Core Insight

> **Traditional research produces a *document*. Power Research produces a *corpus*.**

A document is dead — you read it once, then it sits.
A corpus is alive — you interrogate it, dig deeper, challenge it, return to it months later.

The researcher's job isn't "write the answer."
It's **build a library, then give a tour.**

## The Two Modes

```
You arrive empty.
       │
       ▼
┌─────────────────────────────────┐
│  MODE: PLAN                     │
│                                 │
│  You: ~5 sentences, vague idea  │
│  Me:  Alignment → Scope → Plan  │
│       BRIEF.md + PLAN.md        │
│                                 │
│  You: "Looks good. Go."         │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  MODE: COLLECT                  │
│                                 │
│  Internal stages (auto):        │
│  Capability Check →             │
│  Scaffold → Search → Fetch →    │
│  Save (with YAML header) →      │
│  Extract claims → Track gaps →  │
│  Repeat                          │
│                                 │
│  You: "Enough." 🛑              │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│  CHECKPOINT (on demand)         │
│                                 │
│  Verification → Synthesis       │
│  → checkpoint.md                │
│                                 │
│  You: "Continue." / "Dig into." │
│  You: "Done."                   │
└─────────────────────────────────┘
```

## The Artifacts

```
research/<topic-slug>/
│
├── BRIEF.md              ← The seed. User's original intent, framed.
│                            ~5 sentences. The "why." Immutable.
│
├── PLAN.md               ← A seed that grows forever. Start with 2-3 tracks,
│                            append new ones as research reveals angles.
│                            Living to-do list with ✅ done + 📋 todo.
│                            Scope, modes, search tracks, known unknowns.
│
├── INDEX.md              ← ⭐ AUTO-GENERATED. Run the index script.
│                            Source catalog, topic coverage, tag index.
│                            Read this first — always.
│
├── sources/              ← Every page fetched. Flat files, YAML headers.
│   ├── 2026-06-07_001_market-report.md
│   ├── 2026-06-07_002_competitor-analysis.md
│   ├── 2026-06-08_003_architecture-doc.md
│   └── ...
│
├── topics/               ← Claims organized by topic
│   ├── 01_overview.md
│   ├── 02_competitors.md
│   └── ...
│
├── gaps.md               ← What's missing. Open questions. Drives collection.
│
└── contradictions.md     ← Conflicting evidence, tracked and classified.
```

### Key design decisions

- **No session concept.** The same structure works whether it's one 8-hour run, ten resume-and-continue sessions, or five agents dumping into the same folder. Time is encoded in filenames (`YYYY-MM-DD_NNN_slug.md`), not in folder hierarchy.
- **YAML frontmatter on every source.** Every file in `sources/` has metadata that makes it self-describing and searchable. The INDEX.md is built by scanning these headers.
- **Three state files at root** (`PLAN.md`, `INDEX.md`, `gaps.md`) tell you everything you need to resume. Read them, continue. No hidden state.

### Quick start

```bash
# Scaffold a new research folder
uv run python scripts/init.py "my-topic"

# After collecting sources, rebuild the index
uv run python scripts/index.py
```

Templates are in `templates/`. Scripts are in `scripts/`.

---

## PLAN Mode — Sharpening the Vague

The user arrives with a rough idea. Your job: turn it into a plan they can approve.

### Step 1: Alignment

If the user's request is vague, ambiguous, or could mean multiple things, do a quick alignment pass before writing anything:

- Restate what you think they mean
- Name the main possible interpretations
- Ask 1-2 targeted questions to resolve ambiguity
- Show a tiny sketch of what the research would cover

Examples of when to align:

- vague phrasing ("I want to know about AI")
- overloaded request ("look into the market")
- multiple plausible meanings
- unclear target, scope, or goal
- user says something broad that could mean overview, comparison, or implementation

Move on when the target is clear enough that searching the wrong thing is unlikely. The user confirms the direction, or the prompt is already clear enough.

### Step 2: Scope

Define what's being researched and how wide the net should be. Record:

- **Question** — what we're actually trying to answer
- **User goal** — what they'll do with this
- **In scope** — what belongs
- **Out of scope** — what doesn't
- **Mode** — one of: `breadth`, `balanced`, `depth` (default: `balanced`)

**Research modes:**
- `breadth` — map the space, cover major angles, compare options. Use when the user wants overview, landscape, options, comparison, market scan.
- `depth` — settle a narrow claim, maximize precision. Use when the user wants the truth, verify a fact, settle a dispute, confirm a number.
- `balanced` — default. Enough coverage plus enough verification.

### Step 3: Generate Plan

Write two files:

**`BRIEF.md`** — The seed. Capture the user's intent in their own words. ~5 sentences. The "why" of this research. See `templates/BRIEF.md`.

**`PLAN.md`** — The expansion. Start small — just 2-3 initial search tracks. The plan grows *organically*: when a track is done and there's nothing more to find, you add a new track. When you resume after a week, you add more. After weeks of research, it may naturally reach hundreds of lines. Never generate a massive plan upfront.

The plan contains:
- **Scope** — question, goal, in/out of scope, mode
- **Search tracks** — distinct angles, started small, appended as needed
- **Living checklist** — each track with checkbox, grows forever
- **What we already know** — starting assumptions to avoid rewalking

Template at `templates/PLAN.md`. Start with 2 tracks. Add more when tracks run dry.

---

## COLLECT Mode — The Endless Loop

When the user says "collect" or "go", enter the collection loop. Internally, follow these stages.

### Stage 0: Capability Check

Before any search, check what tools are available:

- **Search** — mandatory. If no search tool exists, stop and tell the user.
- **Fetch/read-web** — strongly preferred. Without it, rely on search snippets and local material.
- **File persistence** — mandatory. If findings can't be saved to files, stop.
- **Parallel spawn** — optional. Use it when work naturally splits.

### Stage 1: Scaffold

Create or reuse the research folder. If resuming, read `PLAN.md`, `INDEX.md`, and `gaps.md` to orient yourself. Do not rebuild from scratch.

### Stage 2: The Collection Loop

```
① Read PLAN.md — pick next unexplored todo
② Read gaps.md — prioritize if gaps exist
③ Search (vary queries: orientation → angle → verification → adversarial)
④ Fetch every result in full
⑤ Save to sources/ with YAML frontmatter — ALWAYS, useful or not
⑥ Extract claims → topics/ (with source link, snippet, why it matters)
⑦ Update gaps.md — new gaps found, old gaps closed
⑧ Check for contradictions → contradictions.md
⑨ Mark done in PLAN.md
⑩ Run index script to rebuild INDEX.md
⑪ Repeat from ①
```

### Source File Format

Every file in `sources/` MUST use this YAML frontmatter format (borrowed from memory-bank):

```markdown
---
summary: "One line — what this source says, specific enough to know if it's useful"
created: 2026-06-07
source: "https://..."
tags: [market, competitors, growth]
topics: [overview, competitive-landscape]
confidence: high
---
# Full Title of the Source

... full fetched content ...
```

| Field | Required | Why |
|---|---|---|---|
| `summary` | ✅ | One-line description. Shows up in INDEX.md. |
| `created` | ✅ | Date fetched. Enables chronological sorting. |
| `source` | ✅ | URL or origin. Traceability. |
| `tags` | ✅ | Search keywords. Cross-cutting retrieval. Also feeds **evidence graph** — entities in tags become nodes in the entity→documents map. |
| `topics` | ✅ | Which PLAN topics this feeds. Links back to plan. |
| `confidence` | ❌ | Signal reliability: `certain` / `likely` / `tentative` / `deprecated`. |
| `importance` | ❌ | Priority signal: `essential` / `supporting` / `background` / `tangential`. Controls ordering in checkpoints and INDEX.md. |

Tags are first-class. Use them generously — they do double duty as search keywords **and** as the building blocks of the evidence graph (see below). Good tag categories:

- domain: `market`, `technical`, `regulatory`, `competitive`
- entity: `competitor-x`, `product-y`, `framework-z`
- type: `report`, `docs`, `news`, `analysis`, `primary-source`
- signal: `key-insight`, `contradiction`, `datapoint`

### Claims Format (topics/)

Claims in `topics/` are **simple markdown lists** — just facts with source links. No heavy schema, no extra YAML. The value is in the link back to the source and the contradictions file.

```markdown
## Claims

- Market grew 23% YoY [[source]](../sources/2026-06-07_001_market-report.md)
- X is the market leader [[source]](../sources/2026-06-07_001_market-report.md)
- Y is gaining share in Asia [[source]](../sources/2026-06-07_002_competitor-analysis.md)
```

That's it. A claim is just:
- **The statement** (what we believe to be true)
- **A source link** (back to the raw file in `sources/`)
- **Optional contradiction** (cross-reference to `contradictions.md`)

If a claim is contradicted, add a note and link to the contradiction entry. The power is in the trail — from claim → source → contradiction → resolution.

### Evidence Graph (auto-generated)

The INDEX.md script automatically builds an **evidence graph** from the `tags` field in every source file. Tags serve double duty: they're search keywords AND entity nodes in a cross-document graph.

**How it works:**
- Every source has `tags: [entity-A, entity-B, ...]`
- The index script scans all sources and builds: entity → list of documents mentioning it
- **Bridge entities** appear in multiple documents → potential connection points
- **Singleton entities** appear in one document → potential leads for follow-up search

The evidence graph is rendered in INDEX.md as a tag index with document counts:

```markdown
## Evidence Graph

### Bridge entities (appear in 2+ sources)
- **competitors** → 3 sources — connects market-report, competitor-analysis, pricing
- **market-growth** → 2 sources — connects market-report, industry-overview
- **asia** → 2 sources — connects competitor-analysis, regional-report

### Singleton entities (1 source each — leads for deeper search)
- **regulatory** → 1 source — only in policy-doc
- **open-source** → 1 source — only in tech-report
```

**Why this matters:** The evidence graph reveals connections you'd miss reading linearly. A bridge entity like `competitors` linking 3 sources means those sources together give you the full competitive picture. A singleton like `open-source` means you've only scratched that angle — it's a gap to explore.

This is directly inspired by Harness-1's evidence graph, adapted to work with our YAML tag system instead of regex entity extraction. The principle is the same: **make cross-document structure visible without rereading everything.**

### Collection Rules

- **Save everything.** Every link, every page. Text is cheap; lost context is expensive. The YAML header and INDEX.md make it navigable even at scale.
- **Never rewalk.** The plan tracks explored paths. If it's marked done, don't revisit unless the user explicitly redirects.
- **Gap-driven search.** `gaps.md` is your steering fuel. No gaps → loop idles until the user updates the plan.
- **No synthesis during collection.** Pure accumulation. Don't summarize, don't conclude, don't filter. Just gather and catalog.
- **Vary queries.** Don't repeat the same phrasing. Progress through: orientation → angle-specific → verification → adversarial.
- **Prefer primary sources.** Official docs, research papers, filings, reports, direct evidence over commentary.

### Search Guidance

**Good query habits:**
- Include the actual topic, not vague shorthand
- Include current year when recency matters
- Include exact entity, product, date, claim or metric
- Search from multiple angles, not one phrasing repeated
- Prefer terms that surface primary sources and direct evidence

**Bad query habits:**
- One vague query then immediate synthesis
- Only searching confirmatory phrasing
- Using broad hype words without the actual subject
- Never varying wording when results are weak
- Treating search snippets as if they were evidence

**Typical query progression:**
1. Orientation — broad, map the space
2. Angle-specific — narrow on each sub-topic
3. Verification — check key claims
4. Adversarial — try to disprove the obvious answer

### Handling Contradictions

Never average contradictions away. When sources disagree:

1. **Classify the conflict:**
   - Time drift — one source is older
   - Scope mismatch — they measure different things
   - Definition mismatch — same term, different meaning
   - Source-quality mismatch — one is stronger
   - Genuine dispute — evidence really conflicts

2. **Record in `contradictions.md`:**
   - Claim A + source + date
   - Claim B + source + date
   - Likely cause
   - Resolution status: resolved / disputed / needs more checking

3. **Resolution preference order:**
   - Primary or official source
   - More recent source
   - Tighter scope match
   - Broader independent agreement

If nothing clearly wins, mark it **disputed** and keep the answer conditional.

---

## CHECKPOINT — On Demand

When the user asks "what do we know?", "summarize", "checkpoint", or you sense they want a status update:

### Verification (internal)

Before writing the checkpoint, test the collected material:

- Are major claims backed by preserved evidence in `sources/`?
- Are weak points labeled in `gaps.md`?
- Are contradictions addressed in `contradictions.md`?
- Is the coverage appropriate for the mode (breadth/balanced/depth)?
- Could another agent resume from these files?

### Synthesis

Generate `checkpoint.md` containing:
- **What we've found** — key claims with source links back to `topics/`
- **What we haven't found** — open gaps from `gaps.md`
- **What to do next** — suggested next todos from `PLAN.md`
- **Uncertainties** — contradictions, weak spots, caveats

### User Decision

Present the checkpoint. The user can:
- **"Continue"** — back to COLLECT loop
- **"Dig into X"** — update PLAN.md with new direction → back to COLLECT
- **"Update plan"** — you update BRIEF.md / PLAN.md → COLLECT re-targets
- **"Done"** — research complete. The corpus stays for future return.

---

## Resume Model

When resuming an existing research thread:

1. Read `BRIEF.md` — remind yourself why
2. Read `PLAN.md` — what's planned, what's done, what's next
3. Read `INDEX.md` — what sources exist, what claims were extracted
4. Read `gaps.md` — what's still missing
5. Continue from the first incomplete angle in PLAN.md

Do not redo completed work unless it's stale, contradictory, or explicitly reset.

---

## Auto-Generated INDEX.md

The `INDEX.md` file is **not hand-written**. It is generated by scanning all files in `sources/` for YAML frontmatter and building a catalog.

**What INDEX.md contains:**
- Quick stats: total sources, total claims, gaps count
- Source catalog table (date | summary | tags | topics)
- Topic coverage map (what's covered, what's thin)
- Tag index for cross-cutting search

**When to rebuild:**
- After every collection loop iteration
- After batch updates or cleanup
- Before ending a session

**Rebuild command:**
```bash
uv run python scripts/index.py
```

The script lives at `scripts/index.py` inside the skill directory. It reads YAML frontmatter from `sources/`, builds the index, and writes `INDEX.md`. The format mirrors memory-bank's approach — summary lines, tag groupings, status badges.

---

## Principles

| Rule | Why |
|---|---|
| **You plan, I expand** | 5 sentences in → structured research. Low effort in, organized corpus out. |
| **YAML headers on everything** | Self-describing files. INDEX.md is auto-generated from headers. Searchable via `rg`. |
| **Collect everything** | Every link, every page. Text is cheap; lost context is expensive. |
| **Never rewalk** | Plan tracks done paths. Every dead end is marked. No repeated work. |
| **Gap-driven** | `gaps.md` is the fuel. No gaps → loop idles. |
| **Endless accumulation** | The corpus only grows. No deletion. More data is always better. |
| **You decide "enough"** | Not a model, not a budget, not a time-box. You look and say stop. |
| **Checkpoint on demand** | You ask when *you* want a summary. Not when the system decides. |
| **Direction can change** | Update the brief → plan updates → collection re-targets. Nothing is final. |
| **No fake consensus** | Contradictions are preserved, not averaged away. |
| **No session concept** | The same structure works for one long run, ten resumes, or five agents. Time is in filenames. |
