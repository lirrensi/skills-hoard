# Memory Types (full)

> Companion to `SKILL.md` → Quick Routing. Load this when deciding what shape a memory should take, or when you need the cross-domain examples.

These three types are universal — they work for code, business, personal life, creative work, research, and any domain where you need to remember things. The examples below span many contexts to show that flexibility.

## Episodic

Use for events, moments, decisions-in-context, meetings, incidents, milestones, discoveries, failed attempts, and progress snapshots.

This answers: **what happened?**

Examples across domains:
- *Code:* A debugging session that revealed the root cause
- *Business:* A client call and the decisions made during it
- *Personal:* A travel day where something went wrong
- *Creative:* A songwriting session where the chorus finally clicked
- *Research:* A lab experiment that produced an unexpected result
- *Relationship:* A conversation that clarified a misunderstanding

## Semantic

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

## Procedural

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

## Multiple types from one interaction

An interaction might span multiple memory types — but **don't force it**. Usually, one well-chosen file is enough.

Example of when multiple files are warranted:
- An incident happens -> save an `episodic` note (the event)
- It reveals a durable constraint different from the event -> also update a `semantic` note (the constraint)
- It teaches a better workflow -> also update a `procedural` note (the procedure)

If the same takeaway can be captured in one file, stop there. Multiple files are only useful when retrieval differs materially.

## New Kinds (retrieval flavors, no new folders required)

Beyond episodic/semantic/procedural + decision/person/project. Use as `memory_type` when the *question you'll ask later* differs. Index auto-catalogs any type; folders optional (`memory/<kind>/` or alongside — consistency wins).

- **`failed_approach`** — what NOT to do. The wrong turn with evidence it failed. *Answers: what should I avoid?* Example: `2026_08_20_migrate_after_workers_failed.md` (workers raced migration, had to re-run). Tags: `failed-approach`. Promotes to semantic constraint only when durable. Template: reuse `episodic.md` (it IS history first).
- **`gotcha`** — sharp edge that bites once you forget it. One-liner-friendly, high reuse value despite small size. *Answers: what's the trap?* Example: `cookie_domain_must_be_parent.md`. Tags: `gotcha`. Template: reuse `procedural.md` pitfalls section.
- **`convention`** — we always do X this way here. Team/project norm, not universal truth. *Answers: what's our agreed way?* Example: `conventional_commits_with_scope.md`. Tags: `convention`, `proj-<name>` if scoped. Template: reuse `semantic.md`. Bump `version` like any living page.
- **`external_ref`** — pointer, don't copy. Link + 3-line why-it-matters + what section to read. *Answers: where's the real doc?* Synthesize, never reproduce: notes ABOUT the source, no verbatim beyond a short quoted phrase (copyright line). Template: `templates/external_ref.md`.

Kind is the retrieval hook; template is just scaffolding.
