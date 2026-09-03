---
name: memory-bank
description: "Use this skill to save, recall, or organize memories across conversations. Trigger on: 'remember this', 'save this', 'note this', 'what did we discuss about...', 'check your notes', 'do you remember', 'recall'. Also use proactively when the user seems to be resuming previous work, referencing past decisions, or when you discover something genuinely worth preserving for future sessions. This skill is NOT limited to code — use it for business decisions, personal notes, meeting recaps, research, project management, creative work, client history, anything."
---

# Agent Memory Bank

A persistent memory system for storing knowledge that survives across conversations — for any domain: code, business, personal, research, creative work, client management, and more.

Universal and env-agnostic: works in any repo, any domain. How you wire it (alias, hotkey, auto-inject, parallel runner) is yours to decide — the skill only guarantees the scripts work from project root. Default use is **session end** via `learn`; orientation at session start is one command (`get_mem.py`).

**Default location:** `./memory/` (create if it doesn't exist; scripts accept an explicit path — root-agnostic, you set it)

**Default structure:**
- `./memory/episodic/` — active events (last 7 days, then auto-archive)
- `./memory/semantic/` — durable facts and current state
- `./memory/procedural/` — repeatable workflows and how-tos
- `./memory/pending.md` — append-only inbox for micro-capture while working
- `./memory/SEED.md` — hand-curated bootstrap, injected at session start
- `./memory/INDEX.md` — auto-maintained living map (never hand-edit)
- `./memory/CHANGES.md` — auto-generated newest-first feed (never hand-edit)
- `./memory/archive/` + `summaries/` — auto-managed compression

---

## When to Use

- User says `remember this`, `save this`, `note this`, `learn`, `crystallize`, `dream`, `what did we learn?`, `what did we discuss about...`, `do you remember`, `recall`
- User resumes prior work, references a past decision, or you are about to re-research something familiar
- You just figured out something painful (debug, gotcha, failed approach) that future sessions will need
- Session is ending and the trigger checklist in Learn Pass hits (otherwise save nothing — empty is success)

---

## Core Philosophy

- **Three memory types, one system**: `episodic` (what happened), `semantic` (what is true), `procedural` (what works next time). Details + kinds (`failed_approach`, `gotcha`, `convention`, `external_ref`) → `references/memory-types.md`.
- **Episodic = diary. Semantic & Procedural = wiki.** Dated entries vs living pages updated over time, not duplicated per session.
- **Use the shape that matches future retrieval**: save by how you'll want to find it later.
- **Prefer history over rewrites**: preserve dated records rather than erasing what came before.
- **But don't spam**: update living records for current state/instructions. Conserve writes — most sessions change little.
- **Never delete memory files** — mark outdated ones with `status: superseded` instead.
- **Write for resumption**: self-contained notes a zero-context future session still understands.
- **Bias toward usefulness**: save what is easy to forget but annoying to rediscover. Failures > wins.
- **Tags are first-class**: short, stable, lowercase (`code`, `proj-auth`, `failed-approach`, `scope-global`). Full vocabulary → `references/frontmatter.md`.
- **Once vs often**: `is this for once or for every damn time?` Cold stays procedural; hot + stable + cross-project proposes a local skill. `runbook == skill`, no extra entity. Full rules → `references/procedural-vs-skill.md`.
- **Learn closes the loop**: end-of-session pass saves episodic, updates canon, proposes skills. Propose, don't auto-create.
- **Generated files are build output**: `INDEX.md`, `CHANGES.md`, `summaries/` — fix sources, rerun `index.py`, never hand-edit.

---

## Quick Routing Cheat Sheet

- Ask: **what will future-you want back?**
- **what happened?** -> save `episodic`
- **what is true now?** -> save or update `semantic`
- **how do we do this?** -> save or update `procedural`
- Short version: **episodic = what happened, semantic = what is true, procedural = what works next time**
- More than one ONLY if each would be retrieved differently (usually one file is enough)

Mini examples:
- "We had a nasty auth incident today" -> `episodic`
- "The client prefers weekly async updates" -> `semantic`
- "Here is the release checklist" -> `procedural`
- "The user dislikes meetings when hungry" -> `semantic`; "avoid scheduling important meetings when they're hungry" -> `procedural`
- "A failed deploy taught us a safer rollout order" -> `episodic` + `procedural`

Do **not** overfit one weak moment into a lasting fact or rule too quickly. Full examples + create-vs-update + contradiction rules → `references/routing.md`.

---

## When to Check Memories

Default use is **session end** (`learn`). For orientation at session start, run `get_mem.py` — no other loading ritual.

A system prompt may override when to check (always / only-when-asked) — follow it. Otherwise: orient via `get_mem.py`, pick the type matching the question (`episodic` = what happened, `semantic` = what is true, `procedural` = how to), search summaries/tags, open 2–3 files for detail. Bodies stay lazy.

---

## Scripts

Helper scripts live in `skills/memory-bank/scripts/`. Run them from the project root.

> **YAML / uv — copy-paste so first attempt works.** `index.py` prefers `pyyaml` but ships a fallback parser, so plain `python` never crashes. `doctor.py` / `get_mem.py` / `capture.py` / `init.py` run on stdlib alone.

```bash
# first attempt, every time (from project root):
uv run --with pyyaml python skills/memory-bank/scripts/get_mem.py
uv run --with pyyaml python skills/memory-bank/scripts/doctor.py --short
uv run --with pyyaml python skills/memory-bank/scripts/index.py
# no uv? plain python works too:
python skills/memory-bank/scripts/get_mem.py
python skills/memory-bank/scripts/index.py
# permanent instead of per-run:
uv add pyyaml   # or: pip install pyyaml
# NOTE: don't bother with `uvx` — it isolates cwd and these scripts
# expect `./memory` relative to YOUR project root. `uv run ...` keeps cwd.
```

| Script | Purpose |
|---|---|
| `scripts/init.py` | Scaffold `./memory/` with core folders, `pending.md` inbox, `SEED.md` bootstrap, starter `INDEX.md` |
| `scripts/get_mem.py` | One command to read it all — SEED + ~100-line brief of every memory + pending + candidates |
| `scripts/index.py` | Rebuild `INDEX.md` + `CHANGES.md`, compress episodic to weekly/monthly digests |
| `scripts/capture.py` | Micro-capture while working — append one line to `pending.md`, no ceremony |
| `scripts/doctor.py` | Health dashboard — counts, inbox, candidates, broken links, age signals. Read-only. |

**Load — one command to read all (session start):**

```bash
python skills/memory-bank/scripts/get_mem.py
```

SEED + one line per memory + pending + candidates, capped at ~100 lines (`--full` uncaps).

**Micro-capture while working (not at consolidate time):**

```bash
python skills/memory-bank/scripts/capture.py "fixed auth cookie, was parent-domain" --tags code,auth,gotcha
python skills/memory-bank/scripts/capture.py "deploy failed: migrate first" --type failure --tags code,deploy
python skills/memory-bank/scripts/capture.py "idea: SEED should list blockers" --type idea
```

Appends to `pending.md` (ignored by index, drained at `learn`). Failures welcome.

**Doctor (stats, read-only):**

```bash
python skills/memory-bank/scripts/doctor.py
python skills/memory-bank/scripts/doctor.py --short
```

Counts, pending, candidates/promoted, untagged/missing-summary/tentative, broken `related`/`skill_ref`, age buckets (descriptive — old is not stale), SEED + INDEX freshness. No edits, no LLM.

**After creating or updating memories, rebuild the index:**

```bash
python skills/memory-bank/scripts/index.py
```

**Never update `INDEX.md` / `CHANGES.md` by hand.** Fix the memory files, rerun the script. Details → `references/index-maintenance.md`.

---

## Templates

Templates live in `skills/memory-bank/templates/`. Copy the matching one into `memory/<type>/` with a meaningful filename, fill frontmatter + body, run `index.py`. Use only the sections that fit.

| Template | Use when |
|---|---|
| `templates/episodic.md` | Event, session, incident (also `failed_approach` first sightings; has Dead Ends section) |
| `templates/semantic.md` | Durable facts, constraints, `convention` norms (has `version`) |
| `templates/procedural.md` | Workflow, checklist, `gotcha` trap, behavioral guidance (has `reuse`, `skill_ref`, parallel note) |
| `templates/decision.md` | Architectural/strategic decision, ADR style |
| `templates/person.md` | Client, colleague, contact profile |
| `templates/project.md` | Project state, risks, milestones |
| `templates/external_ref.md` | External doc pointer — link + paraphrased takeaways, never a copy |

Naming: `episodic` = `YYYY_MM_DD_name.md` (many per day ok); `semantic`/`procedural` = stable names updated over time. Full naming + YAML field docs → `references/frontmatter.md`.

### Dream / background maintenance

For recurring/background consolidation ("dream mode"), see `references/dream-mode.md`: retrieval-first pass, queue/access/boundary first, sort into the three types, update canon instead of duplicating. Normal templates and rules apply.

---

## Learn Pass (End-of-Session)

Trigger: user says `learn`, `crystallize`, `dream`, or `what did we learn?`. Mostly session end — same session writes its own files. No env wiring encoded; parallel or sequential is the user's setup to choose.

**Should I save anything? (if none hit, save nothing and say why):**
- repeated failure just happened
- reusable tactic / workflow emerged or improved
- user corrected behavior that should persist
- durable fact, preference, or constraint changed
- validation shows an existing memory is wrong
- open blocker / next step future-you will need

Do this in order:

0. **Drain pending inbox** — read `pending.md`, promote each line (or drop with reason), delete promoted lines.
1. **Save episodic** — one dated file: decisions, findings, failed attempts, next steps. Include Dead Ends. Tag `failed-approach`/`gotcha` when apt.
2. **Update semantic** — only if durable truth changed. Search-then-update canon, bump `updated` (+ `version` + one line why), never silently overwrite on conflict — surface it, preserve uncertainty.
3. **Update procedural** — only if a repeatable method emerged/improved. Mark `reuse: once|often` (default `once`). Fact → semantic, method → procedural, hot stable method → propose skill. Behavioral stays procedural forever.
4. **Propose skills** — `reuse: often` + stable 2–3x + validated + cross-project value. Say `Candidate: <file> -> .agents/skills/<name>/ because <evidence>`, wait for approval. Local-only (`./.agents/skills/`), never global unless asked to share.
5. **Refresh SEED + rebuild index** — update `Where you left off` in `SEED.md`, run `index.py` (rebuilds `INDEX.md` + `CHANGES.md`).

Validation gate — reject before writing: one-off noise / unsupported hypotheses / transient output → drop. One weak incident stays episodic. `tentative` stays tentative until re-validated.

Rules: most sessions propose **zero** skills (success). Behavioral never proposes. Delegation never required — optional one-line `Parallelizable:` note when steps were independent and workload heavy. No skill tooling? Still mark `reuse: often` for later.

Mini example:
```text
learned: deploy takes 4 manual steps, same 3rd time, stable
-> update procedural/how_to_deploy.md (reuse: often)
-> propose: how_to_deploy.md -> deploy-skill (ran 3x, stable, cross-project)
```

---

## Procedural vs Skill (summary)

`runbook == skill` — no extra entity. Procedural = cheap cold storage in `memory/procedural/`; skill = hot testable artifact in `./.agents/skills/`, linked via `skill_ref`. `once` stays, `often` + stable + validated + cross-project proposes. Behavioral never promotes. Promotion checklist + classic skill protocol (lean SKILL.md, `references/` on demand, verification command) → `references/procedural-vs-skill.md`.

---

## File Organization

By default, organize memory by type:
- `./memory/episodic/` — active events (auto-archive after 7 days)
- `./memory/semantic/` — durable facts and state
- `./memory/procedural/` — workflows and how-tos
- `./memory/pending.md` — micro-capture inbox (drained at `learn`)
- `./memory/SEED.md` — session bootstrap (refresh `Where you left off` at `learn`)
- `./memory/CHANGES.md` — auto-generated feed (never hand-edit)
- `./memory/archive/` + `summaries/` — auto-managed

Microservices, subfolders, `threads`-as-semantic → `references/file-organization.md`. New `memory_type` values auto-catalog anywhere — consistency over depth.

---

## Reference Files — Load on Demand

Load these **only** when the task needs them. Do not load them all upfront.

| File | Load when |
|---|---|
| `references/memory-types.md` | Deciding episodic vs semantic vs procedural, or using `failed_approach`/`gotcha`/`convention`/`external_ref` |
| `references/routing.md` | Unsure create-vs-update, what is worth saving, handling contradictions with evidence |
| `references/frontmatter.md` | Writing a file — tag vocabulary, filename shape, every YAML field |
| `references/search.md` | `get_mem.py` isn't enough and you need surgical `rg` recipes |
| `references/index-maintenance.md` | INDEX/CHANGES look wrong, or you want compression mechanics |
| `references/cleanup.md` | User asked to organize, consolidate, or review memories |
| `references/procedural-vs-skill.md` | A procedural feels hot and may earn a full skill |
| `references/file-organization.md` | Flat layout bursts — microservices, sagas, subfolders |
| `references/dream-mode.md` | Background/recurring consolidation pass, backfill triage |
