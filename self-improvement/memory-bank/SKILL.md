---
name: memory-bank
description: "Use this skill to save, recall, or organize memories across conversations. Trigger on: 'remember this', 'save this', 'note this', 'what did we discuss about...', 'check your notes', 'do you remember', 'recall'. Also use proactively when the user seems to be resuming previous work, referencing past decisions, or when you discover something genuinely worth preserving for future sessions. This skill is NOT limited to code — use it for business decisions, personal notes, meeting recaps, research, project management, creative work, client history, anything."
---

# Agent Memory Bank

A persistent memory system for storing knowledge that survives across conversations — for any domain: code, business, personal, research, creative work, client management, and more.

**Default location:** `./memory/` (create if it doesn't exist)

**Default structure:**
- `./memory/episodic/` — active events (last 7 days)
- `./memory/semantic/` — durable facts and current state
- `./memory/procedural/` — repeatable workflows and how-tos
- `./memory/archive/` — compressed episodic memories (auto-managed)
- `./memory/summaries/episodic/weekly/` — weekly digests of archived episodic files
- `./memory/summaries/episodic/monthly/` — monthly rollups of weekly digests
- `./memory/INDEX.md` — auto-maintained living map

---

## Core Philosophy

- **Three memory types, one system**: Store experiences as `episodic`, durable facts and evolving state as `semantic`, and repeatable workflows as `procedural`.
- **Episodic = diary. Semantic & Procedural = wiki.** `episodic` gets new dated entries. `semantic` and `procedural` are living reference pages that should usually be updated over time instead of duplicated per session.
- **Use the shape that matches future retrieval**: Save things based on how you'll want to find them later — what happened, what is true, or how to do it.
- **Prefer history over rewrites**: When an event or decision matters in its own right, preserve it as a dated record rather than erasing what came before.
- **But don't spam**: Update living records when the goal is to maintain current state or current instructions.
- **Never delete memory files** — mark outdated ones with `status: superseded` instead.
- **Write for resumption**: Notes should be self-contained — a future session with zero context should still understand them.
- **Bias toward usefulness**: Save things that may matter later, especially details that are easy to forget but annoying to rediscover.
- **Tags are first-class**: Tag memories so they can be searched quickly across domains, projects, people, and topics with `rg`.
- **INDEX.md is the map**: After creating or updating memories, rebuild `INDEX.md` so future sessions (and you) can scan the whole landscape in seconds.

---

## Quick Routing Cheat Sheet

Use this fast decision tree when deciding what to save:

- Ask: **what will future-you want back?**
- If the answer is **what happened?** -> save `episodic`
- If the answer is **what is true now?** -> save or update `semantic`
- If the answer is **how do we do this?** -> save or update `procedural`
- Short version: **episodic = what happened, semantic = what is true, procedural = what works next time**
- If the answer is **more than one of those, and each would be retrieved differently** -> save in multiple forms (but in most cases, one file is enough)

Mini examples:
- "We had a nasty auth incident today" -> `episodic`
- "The client prefers weekly async updates" -> `semantic`
- "Here is the release checklist" -> `procedural`
- "The user dislikes meetings when hungry" -> `semantic`; "avoid scheduling important meetings when they're hungry" -> `procedural`
- "A failed deploy taught us a safer rollout order" -> `episodic` + `procedural` (the event and the new workflow are both worth preserving)
- "A conversation revealed a lasting user preference" -> `episodic`

Most knowledge fits cleanly into one memory type. Only create multiple files when the same information genuinely needs to be retrieved in two or more fundamentally different ways.

Do **not** overfit one weak moment into a lasting fact or rule too quickly.

---

## Memory Types

These three types are universal — they work for code, business, personal life, creative work, research, and any domain where you need to remember things. The examples below span many contexts to show that flexibility.

### Episodic

Use for events, moments, decisions-in-context, meetings, incidents, milestones, discoveries, failed attempts, and progress snapshots.

This answers: **what happened?**

Examples across domains:
- *Code:* A debugging session that revealed the root cause
- *Business:* A client call and the decisions made during it
- *Personal:* A travel day where something went wrong
- *Creative:* A songwriting session where the chorus finally clicked
- *Research:* A lab experiment that produced an unexpected result
- *Relationship:* A conversation that clarified a misunderstanding

### Semantic

Use for durable knowledge, evolving facts, preferences, profiles, constraints, current state, and anything that may be updated many times over.

This answers: **what is currently true?**

Think of semantic memory as a **wiki page, not a diary entry**. Prefer **one stable file per subject** that accumulates updates over time. Do **not** create a new semantic file just because a new session happened.

Examples across domains:
- *User/Client:* Communication preferences, timezone, dietary restrictions, preferred meeting times
- *Project:* Current architecture constraints, active risks, tech stack choices
- *Personal:* Health metrics, financial goals, location, current reading list
- *Creative:* Established world-building rules, character traits, thematic constraints
- *Behavioral:* How the user likes to be addressed, tone preferences, boundaries

**Important:** Semantic is not just "project facts" — it is *any durable truth about the world you operate in*, including people, projects, and yourself.

Think: **semantic stores what is true.**

### Procedural

Use for repeatable methods, behavioral guidance, checklists, workflows, instructions, playbooks, routines, and standard ways of doing things — including how to approach situations, how to adapt to a person, and how to behave in the future.

This answers: **how do we do this?** and **how should I behave?**

Think of procedural memory as a **wiki page for behavior and workflows**. It stores not only productivity steps, but also the learned ways to navigate recurring human situations well. Keep the canonical checklist, playbook, or adaptation guide in one stable file and revise it as the process improves, instead of creating a fresh procedural note per conversation.

Examples across domains:
- *Code:* How to deploy safely, code review checklist, incident response playbook
- *Business:* Weekly reporting workflow, client onboarding steps, negotiation prep routine
- *Personal:* Travel packing checklist, morning routine, weekly reflection process
- *Behavioral:* How to approach sensitive topics with this user, tone guidance for difficult conversations, when to escalate vs. handle independently
- *Adaptive assistant:* If the user hates meetings when hungry, choose better meeting times; if the user is angry, start with calming acknowledgment before problem-solving; if a user shuts down under overload, reduce options and keep replies short
- *Creative:* The revision checklist, how to critique a draft without crushing morale

**Important:** Procedural is not just "task execution." It is *any repeatable pattern of behavior* — including how you (or the system) should act in specific contexts, how to adapt to this user, and what response patterns tend to work. If semantic memory stores what is true, procedural memory stores what works.

### Multiple types from one interaction

An interaction might span multiple memory types — but **don't force it**. Usually, one well-chosen file is enough.

Example of when multiple files are warranted:
- An incident happens -> save an `episodic` note (the event)
- It reveals a durable constraint different from the event -> also update a `semantic` note (the constraint)
- It teaches a better workflow -> also update a `procedural` note (the procedure)

If the same takeaway can be captured in one file, stop there. Multiple files are only useful when retrieval differs materially.

---

## Tags

Use tags generously but intentionally. Tags make cross-cutting retrieval easy without overcomplicating the folder structure.

Good tag categories:
- domain: `code`, `business`, `personal`, `research`, `creative`
- topic: `auth`, `deploy`, `health`, `finance`, `planning`
- entity: `client-acme`, `project-helios`, `user`, `team`
- type hints: `decision`, `preference`, `incident`, `checklist`, `workflow`

Prefer short, stable, lowercase tags with hyphens when needed.

Examples:
- `tags: [code, auth, incident, project-helios]`
- `tags: [business, client-acme, preference, communication]`
- `tags: [personal, travel, checklist]`

---

## How to Route New Information

Ask these questions:

1. Is this mainly an event or time-bound moment?
   - Save `episodic`
2. Is this a durable fact, preference, constraint, or current state?
   - Save or update `semantic`
3. Is this a repeatable method or instruction?
   - Save or update `procedural`
4. Does it truly span multiple categories in ways you'd search for differently?
   - Only then save in multiple forms. In most cases, one file is enough — don't create extra files just because the knowledge technically touches more than one category.

Simple promotion rule:
- If it matters as **what happened** -> `episodic`
- If it changes **what is true** -> `semantic`
- If it changes **what to do next time** -> `procedural`

Examples across domains:
- *Code:* "We debugged auth and found the cookie domain was wrong"
  - `episodic`: the debugging session
  - `semantic`: auth depends on the correct parent-domain cookie setting
- *Business:* "The client prefers weekly async updates"
  - `semantic`: client preference
- *Business:* "Here is our monthly reporting process"
  - `procedural`: recurring workflow
- *Code:* "Friday's failed deploy taught us to run migrations before workers"
  - `episodic`: failed deploy
  - `procedural`: safer release workflow
- *Personal/Behavioral:* "The user gets overwhelmed by long explanations; they prefer concise bullet points"
  - `semantic`: user's communication preference
- *Personal/Behavioral:* "When the user is stressed, acknowledge their feelings first before proposing solutions"
  - `procedural`: behavioral approach for stressed-user interactions
- *Creative:* "The protagonist's backstory was finalized: orphan, raised by wolves, afraid of fire"
  - `semantic`: character profile (durable fact)
- *Creative:* "Songwriting sessions work best when I start with the melody, not lyrics"
  - `procedural`: creative process guidance

---

## Proactive Saving

Since this skill is loaded, memory is clearly valued here — lean into it. Save without being asked when you encounter:

- Something that took real effort to figure out (research, debugging, negotiation, comparison)
- A decision with non-obvious reasoning — why X over Y
- Information that would be painful to reconstruct if this conversation ended
- Dead ends and failed approaches — saves future sessions from repeating them
- In-progress work with clear next steps
- Anything the user seems to care about that isn't obvious from context alone

Applies to any domain — code, business, personal, creative, research, client work, anything.

---

## File Naming

```
episodic:   YYYY_MM_DD_meaningful_name.md
semantic:   stable_subject_name.md
procedural: how_to_meaningful_name.md
```

Examples — notice these span many domains:
- *Code:* `2025_03_09_auth_bug_root_cause.md`
- *Business:* `2025_03_10_q1_marketing_decisions.md`
- *Personal:* `user_preferences.md`, `health_tracking_setup.md`
- *Business:* `client_acme_profile.md`, `project_helios_status.md`
- *Code:* `how_to_rotate_api_keys.md`, `incident_response_playbook.md`
- *Behavioral:* `how_to_approach_stressed_user.md`, `tone_guidance_for_sensitive_topics.md`
- *Creative:* `character_ariel_backstory.md`, `songwriting_process.md`
- *Business:* `weekly_client_reporting_workflow.md`

Multiple episodic files per day are normal and encouraged. Semantic and procedural files should usually keep stable names so they can be updated over time.

Rule of thumb:
- `episodic/` = many dated files over time
- `semantic/` = one evolving file per topic
- `procedural/` = one evolving file per workflow or behavior pattern

---

## Optional YAML Fields (Obsidian-Compatible)

The shared frontmatter supports extra fields. Use any, all, or none — they are optional.

```yaml
---
summary: "One line — specific enough to know if you need to read this"
created: YYYY-MM-DD
updated: YYYY-MM-DD
memory_type: episodic | semantic | procedural | decision | person | project
tags: [optional, tags]
status: active | superseded | draft | archived
confidence: certain | likely | tentative | deprecated
related: [other_file.md, another.md]
aliases: [alt-name]
source: "where this came from"
---
```

- `status`: mark outdated files with `superseded` instead of deleting them
- `confidence`: signal how solid this knowledge is
- `related`: backlinks to other memory files for graph traversal
- `aliases`: alternate names to search by
- `source`: URL, conversation ID, document name, or person

These fields make the memory graph richer without adding complexity for simple notes.

---

## Templates

Templates live in `skills/memory-bank/templates/`. Copy the one matching your memory type and fill it in.

| Template | Use when |
|---|---|
| `templates/episodic.md` | Recording an event, meeting, incident, or session |
| `templates/semantic.md` | Capturing durable facts, state, preferences, or constraints |
| `templates/procedural.md` | Writing a repeatable workflow, checklist, how-to, or behavioral guidance |
| `templates/decision.md` | Documenting an architectural or strategic decision (ADR style) |
| `templates/person.md` | Profiling a person — client, colleague, contact |
| `templates/project.md` | Tracking a project's current state, risks, and milestones |

**How to use:**
1. Pick the template that matches what you're saving
2. Copy it into the correct `memory/<type>/` folder with a meaningful filename
3. Fill in the frontmatter and body
4. Run the index script (see below)

> **Use only the sections that fit.** A memory for a client call looks different from a debugging session — that's fine.

### Dream / background maintenance reference

If you want to run memory-bank in a recurring, background, or semi-autonomous **"dream mode"** pass, see:

- `skills/memory-bank/references/dream-mode.md`

That reference explains how to:
- treat **dream** as a retrieval-first operating mode, not a new memory type
- decide what matters in prior material
- sort information into `episodic`, `semantic`, and `procedural`
- handle ambiguity, conflict, and update thresholds
- update existing canonical files instead of duplicating them

Use the **normal memory-bank templates and file types** during dream mode. The reference is just the shortcut path for how to operate when the task is "dream / background consolidation / review prior context".

---

## Scripts

Helper scripts live in `skills/memory-bank/scripts/`. Run them from the project root.

| Script | Purpose |
|---|---|
| `scripts/init.py` | Scaffold `./memory/` with core folders and a starter `INDEX.md` |
| `scripts/index.py` | Scan all memories and rebuild `memory/INDEX.md` with links, summaries, and tag indexes |

**After creating or updating memories, rebuild the index:**

```bash
python skills/memory-bank/scripts/index.py
```

This keeps `INDEX.md` as a living map of everything saved. Future sessions should check `INDEX.md` first for orientation.

**Never update `INDEX.md` by hand.** It is a generated artifact. If you want the index to read better, update the underlying memory files (especially their `summary`, `tags`, `status`, or filenames) and then run the index script again.

---

## INDEX.md Maintenance

`INDEX.md` lives at `./memory/INDEX.md`. It is auto-generated — **do not hand-edit it**.

Treat `INDEX.md` like build output:
- do **not** manually add notes there
- do **not** manually fix links there
- do **not** manually rewrite entries there
- anything written there by hand can be wiped out the next time `index.py` runs

If the index looks wrong or incomplete:
- fix the actual memory files
- then rerun `python skills/memory-bank/scripts/index.py`

**What it contains:**
- Table of contents by memory type
- Every memory file as a link + its `summary` line
- Status badges (e.g., `[superseded]`) for quick filtering
- A full tag index at the bottom

**When to rebuild:**
- After creating a new memory
- After updating a memory with a changed `summary`, `tags`, or `status`
- After batch cleanup or reorganization
- Before ending a session where memory work happened

**How to rebuild:**
```bash
python skills/memory-bank/scripts/index.py
```

If you updated one or many memory files, call the script. Do not try to keep `INDEX.md` in sync manually.

**Orientation shortcut for future sessions:**
```bash
# See the whole landscape
bat ./memory/INDEX.md

# Or just the summaries
grep "^\- \[" ./memory/INDEX.md
```

---

## Episodic Compression

The index script automatically compresses old episodic memories to keep the active folder lean.

**How it works:**
1. **Weekly**: episodic files older than 7 days are moved to `archive/`
2. A weekly digest is generated at `summaries/episodic/weekly/YYYY-WNN.md` listing all archived files for that week with summaries and tags
3. **Monthly**: once a month completes, a monthly digest is generated at `summaries/episodic/monthly/YYYY-MM.md` linking to its 4–5 weekly digests

**Why:**
- Active `episodic/` stays scannable (no 100-file noise)
- You can still find anything by searching `archive/` or `summaries/`
- Weekly/monthly summaries give you the "what happened that week/month" overview without opening individual files

**This is automatic** — just run `index.py` and it handles housekeeping. Do not manually move files into `archive/`.

---

## Searching Memories

### Quick orientation (run this first when memories feel relevant)
```bash
rg --files ./memory | sort
```
This shows the files that exist across all memory types — a fast orientation to what's here.

### Read the index
cat ./memory/INDEX.md

### Search by memory type
```bash
rg "^memory_type: episodic$" ./memory/ --no-ignore
rg "^memory_type: semantic$" ./memory/ --no-ignore
rg "^memory_type: procedural$" ./memory/ --no-ignore
```

### Read summaries across all files
```bash
rg "^summary:" ./memory/ --no-ignore
```

### Search by keyword (full text)
```bash
rg "keyword" ./memory/ --no-ignore -i
```

### Search summaries only
```bash
rg "^summary:.*keyword" ./memory/ --no-ignore -i
```

### Search by tag
```bash
rg "^tags:.*keyword" ./memory/ --no-ignore -i
```

### Search by tag combination
```bash
rg "^tags:.*auth.*project-helios|^tags:.*project-helios.*auth" ./memory/ --no-ignore -i
```

### Search semantic memories for current state
```bash
rg "keyword" ./memory/semantic/ --no-ignore -i
```

### Search procedural memories for how-to guidance
```bash
rg "keyword" ./memory/procedural/ --no-ignore -i
```

### Search episodic memories for what happened
```bash
rg "keyword" ./memory/episodic/ --no-ignore -i
```

### Search archived episodic memories (deep dive)
```bash
rg "keyword" ./memory/archive/ --no-ignore -i
```

### Search weekly/monthly summaries (overview)
```bash
rg "keyword" ./memory/summaries/ --no-ignore -i
```

### Search everything at once (nuclear option)
```bash
rg "keyword" ./memory/ --no-ignore -i
```

After finding relevant files, **read them** using your native file tools. The summary tells you if it's worth reading; reading gives you the actual context.

### Related links
Use relative paths from `./memory/` root in `related:` fields. Filenames are unique across the whole memory space, so a simple filename is enough:
```yaml
related: [semantic/auth_constraints.md, episodic/2026_05_14_auth_bug.md]
```

---

## When to Check Memories

Default behavior: check memories when the task feels like it might connect to prior work — e.g. the user references a past decision, says "like we discussed", or you're about to re-research something familiar.

This default can be overridden by the environment. A system prompt may instruct you to always check memories, or only check when explicitly asked — follow those instructions. This skill describes the fallback when no such instruction exists.

When checking:
- orient quickly to what exists
- choose the memory type that matches the question
- search by tags, keywords, and summaries
- read the most relevant files for actual context

Use this retrieval pattern:
- `episodic` for "what happened?"
- `semantic` for "what do we know now?"
- `procedural` for "how do we do this?"

---

## When to Save

No strict rules — use judgment. Good candidates:
- Something that took real effort to figure out
- A decision with non-obvious reasoning behind it
- Information you'd lose if this conversation ended now
- Anything the user explicitly wants remembered
- A preference, profile, or constraint likely to matter again
- A workflow, checklist, or behavioral pattern you'll likely reuse
- A bug, config detail, or environment-specific gotcha that could bite again later
- Behavioral guidance — how to approach a situation, tone rules, interaction patterns that work well with this user or context

Not worth saving:
- Easily googleable facts
- Transient scratchpad work
- Anything the user will obviously remember themselves

---

## Cleanup and Distillation

Do not aggressively reorganize or distill memories by default.

Only do memory cleanup when:
- The user asks to organize, clean up, archive, consolidate, or review memories
- You are already working inside the memory folder and obvious cleanup is part of the task

When cleaning up memories:
- Prefer marking outdated files with `status: superseded` or moving them into an `archive/` folder if such a structure already exists or the user asks for it
- Avoid deleting memory files unless the user explicitly requests deletion
- Preserve historical context; do not collapse distinct events into one vague note
- Merge or simplify only when duplicates are clearly redundant and the result is more useful than the originals
- Keep tags consistent so search stays clean

Distill carefully:
- Promote repeated or clearly durable facts into `semantic` memory when you have good evidence they should be long-lived
- Promote repeatable workflows into `procedural` memory when they are clearly meant to be reused
- Do not turn one weak incident into a lasting semantic belief or procedural law too quickly
- If you are not confident, preserve the original memory and avoid over-distilling

If the user asks to "clean up my memories", a good default is:
- review for stale or superseded files
- archive or mark outdated material
- tighten titles and tags
- leave meaningful history intact
- **rebuild `INDEX.md`** so the map reflects reality

---

## When to Create vs Update a File

**One-line rule:** `episodic` creates history; `semantic` and `procedural` maintain canonical pages.

**Create a new file** when:
- You are recording a distinct event, session, decision point, incident, or milestone
- You are starting a new topic with no current memory for it
- You want to preserve a dated snapshot of what happened at a specific point in time

**Update an existing file** when:
- You are maintaining an ongoing semantic record of current state
- You are improving an existing procedure or checklist
- A stable file for this subject already exists and should remain the source of truth

Practical default:
- If a matching `semantic` or `procedural` file already exists, **update it**
- Only create a new `semantic` or `procedural` file when the topic is genuinely new or the existing file has become meaningfully different in scope
- Do **not** create duplicate semantic/procedural files just because today's conversation added another fact or tweak
- When information conflicts, newer knowledge usually takes precedence, but update gently and preserve uncertainty when needed

The goal is to avoid both extremes: don't spam new files for every tiny change, but don't flatten meaningful history into one endlessly edited document either.

When in doubt:
- choose `episodic` if the value is historical context
- choose `semantic` if the value is current truth
- choose `procedural` if the value is repeatable guidance
- choose more than one ONLY if the retrieval needs differ materially (rare)

When something evolves across clearly distinct phases, new files tell a useful story:

```
2025_03_09_supplier_negotiation_initial.md
2025_03_10_supplier_negotiation_counteroffer.md
2025_03_11_supplier_negotiation_final_terms.md
```

To mark a file as outdated, add `status: superseded` to its frontmatter — don't delete it.

---

## File Organization

By default, organize memory by type:
- `./memory/episodic/` — active events only (files >7 days auto-move to `archive/`)
- `./memory/semantic/` — durable facts and state
- `./memory/procedural/` — workflows and how-tos
- `./memory/archive/` — auto-managed; do not manually edit
- `./memory/summaries/episodic/weekly/` — auto-generated weekly digests
- `./memory/summaries/episodic/monthly/` — auto-generated monthly rollups

You may also encounter or be instructed to use a more structured layout such as `./memory/semantic/clients/` or `./memory/procedural/operations/`. Follow whatever structure exists; if none exists, use the default type-based layout.

**New types:** Decision, person, and project memories may live in their respective type folders or in a flat structure — consistency matters more than depth. If you create `./memory/decision/`, `./memory/person/`, or `./memory/project/`, the index script will find and catalog them automatically.
