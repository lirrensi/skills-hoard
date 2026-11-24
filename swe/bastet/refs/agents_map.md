# AGENTS.md Cartography Guide

> Load when Bastet is asked to create, rewrite, review, or polish `AGENTS.md`
> (or `CLAUDE.md`, `.cursorrules`, sibling instruction files).
>
> Goal: the instruction file works as a MAP first, rules second.
> An agent told "go fix the X block" must know what X is and where it lives in < 30 seconds.

---

## Core idea

Every repo writes the easy parts: project name, purpose, stack, rules. All useful. All insufficient.

The hard part — the part that's always missing — is **cartography**: where things live,
what the domain words point at, where to read for a given task.

**MAP IS SOP priority.** When touching any agent instruction file: map first, commands second,
rules third, purpose last. Most instruction files get this exactly backwards —
purpose first, rules second, no map at all. Flip it.

An `AGENTS.md` with perfect rules and no map leaves the agent asking:
"you say fix the auth block — what the fuck is the auth block and where is it?"
A map answers that before it's asked.

---

## Priority order (SOP)

| Priority | Section | Job |
|----------|---------|-----|
| 1 — MAP | Block locator + reading paths | Where is X? Where do I read for task T? |
| 2 | Commands | How do I run / test / verify here? |
| 3 | Rules + traps | What must I never do? What's surprising? |
| 4 — LAST | Purpose | What is this project? (one paragraph, max) |

If the file grows long, cut from the bottom. Never cut the map.

---

## The map: three components

### 1. Block locator — "what the fuck is this block"

A table mapping DOMAIN WORDS (the words humans use in tasks) to PATHS (where that thing lives).
The single highest-value section in the whole file.

| Block (task word) | Lives at | Entry point |
|-------------------|----------|-------------|
| auth | `src/auth/` | `src/auth/middleware.ts` |
| billing | `src/billing/`, `migrations/014_*` | `src/billing/invoice.ts` |
| ingest job | `src/jobs/ingest/` | `src/jobs/ingest/run.ts` |

Rules:

- One row per concept a task-giver would name. If someone says "fix the X", X gets a row.
- Paths must be real and current — a stale locator is worse than none (the agent trusts it, then wastes 10 minutes).
- Entry point = the ONE file to open first, not a directory dump.

### 2. Reading paths — "where do I go read for T"

Task-shaped pointers. 3–6 rows cover most repos.

| Task | Start here (in order) |
|------|-----------------------|
| fix a bug in X | locator row for X → `tests/X/` → `docs/spec.md#X` |
| add an endpoint | `src/routes/` → `src/auth/middleware.ts` → `docs/arch.md#api` |
| change config | `src/config.ts` → `.env.example` → `docs/ops/runbook.md` |

### 3. Entry points + vocabulary

- **Entry points:** `main()` / app boot / config load / test command — one line each, with a path.
  If it takes > 30 seconds to find `main()`, write it down.
- **Vocabulary:** repo-specific terms that collide with generic words (`block`, `job`, `run`, `node`) —
  one line each: what it means HERE.

---

## Shapes

### Root AGENTS.md (map-first)

```markdown
# {Repo} — agent map

## Where things live (read this first)

{block locator table}

## Reading paths

{task → files table}

## Run / verify

{3–5 copy-pasteable commands}

## Rules

{constraints and traps — short}

## What this is

{1 paragraph — purpose goes LAST}
```

Keep the whole file scannable in ~1 minute. Depth lives in `docs/` — link it, don't paste it.

### If Thoth canon exists (code-docs `docs/`)

- The root essence block (between `docs-essence` markers) stays untouched — tooling owns that shape.
  The map goes OUTSIDE the markers, around it.
- Locator rows SHOULD point at canon first (`docs/spec.md#X`, `docs/arch/...`), code second.
- Don't duplicate `INDEX.md` listings — point at `docs/INDEX.md` for the full inventory.
  The locator keeps only what the index can't say: task-words → entry points, taste, reading order.

### Subfolder instruction files

One mini-map per folder with its own vocabulary: what's here, the 1–2 files to read first,
neighbors, traps. Matches the code-docs `agents-folder.md` shape — reuse it, don't invent a second one.

---

## The fix-the-block test (validation)

Before calling any `AGENTS.md` done:

1. Pick 3 domain words a human would use in a task ("auth block", "billing", "ingest job").
2. For each: can a fresh agent say WHAT it is and WHERE it lives from the instruction file alone, in < 30 seconds?
3. If any answer is "grep and hope" — the map is incomplete. Add the row.

Also: every path in the file must exist. Check them.
`AGENTS.md` that references deleted folders is the classic rot.

---

## Slop vs map

| Slop (rules-only file) | Map (what Bastet wants) |
|------------------------|-------------------------|
| 3 paragraphs of purpose, stack, vision | 1 paragraph of purpose, LAST |
| "Follow clean code principles" | "Entry: `src/main.ts`; config: `src/config.ts`" |
| "Tests live in the repo" | "`tests/` mirrors `src/`; run `make test`" |
| No file paths at all | Every claim has a path |
| 200 lines of lint rules | Link the lint config; keep 3 trap-lines max |

---

## Refresh rhythm

- **Touch the map** when folders rename, features move, entry points change,
  or a new domain word enters task vocabulary.
- **Audit paths** on every repo visit: stale paths are the #1 `AGENTS.md` rot.
- **Cut from the bottom**: file growing? Shrink purpose first, then rules. The map never shrinks.

---

*The map is the gift. Rules are the wrapping. — Bastet* 😽
