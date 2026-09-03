# Dream Mode

## My Vision

Dream mode is a **retrieval-first memory pass**.

It is **not** a new memory type.
It is **not** a special template.

It is just the mode you use when the goal is to:
- review prior sessions or artifacts
- extract what matters
- update memory cleanly
- preserve history without duplicating canon

Use normal memory-bank rules and normal memory templates.

---

## Start Here

Before doing anything else, figure out 3 things:

1. **Queue** — what counts as unprocessed?
2. **Access** — how do you read prior sessions/artifacts in this environment?
3. **Boundary** — what exact time window, cursor, or scope are you reviewing now?

If these are unclear, resolve them first.

---

## What To Focus On

Prioritize:
- repeated patterns
- durable preferences
- stable constraints
- major state changes
- decisions with consequences
- workflow lessons
- corrections to current understanding
- unresolved contradictions

Deprioritize:
- one-off noise
- tiny details with no future value
- facts that only mattered in the original moment

---

## Sort Memory Like This

### Episodic
Use for **what happened**.

Good for:
- events
- discoveries in context
- failed attempts
- milestones
- session-specific developments

### Semantic
Use for **what is true now**.

Think: **semantic stores what is true**.

Upgrade something to semantic when it stops being just part of the story and starts affecting future reasoning.

Good for:
- durable preferences
- stable facts
- current state
- standing constraints
- corrections to prior understanding

### Procedural
Use for **how to do it next time**.

Think: **procedural stores what works**.

This includes both **workflow execution** and **human adaptation**.

Good for:
- workflows
- checklists
- behavior guidance
- reusable response patterns
- user-specific adaptation rules
- calming, escalation, or timing strategies that reliably work
- lessons that should guide future action

Example:
- `semantic`: the user dislikes meetings when hungry
- `procedural`: avoid scheduling important meetings when they are hungry

Mark `reuse: once|often` at write time. `once` = cold one-off, `often` = hot workflow you run every damn time. No `runbooks/` layer — `runbook == skill`, skill lives outside `memory/` and procedural just points via `skill_ref`. Behavioral guidance never promotes.

---

## Update Rules

- `episodic` can grow by new dated entries
- `semantic` should usually update an existing subject file
- `procedural` should usually update an existing how-to/playbook

Rule of thumb:
- **event** -> episodic
- **durable truth** -> semantic
- **repeatable method** -> procedural

Do **not** create a new semantic/procedural file just because a new session happened.
Do **not** overfit one weak incident into a lasting fact or rule too quickly.

---

## Ambiguity Rule

Ask:
- Will I want this later as a **story**, a **truth**, or a **method**?

Default to **one memory type**.
Use multiple only when retrieval truly differs.

---

## Conflict Rule

If information conflicts, **cry loudly — never stupidly overwrite**:
- say what contradicts what, with both sources visible
- you change a canonical file only when you can cite evidence (session date, pending line, URL, re-validation)
- no evidence → keep old text, add `## Pending Review` with the specific claim + what would prove it, set `confidence: tentative`
- newer knowledge takes precedence only when credible + evidenced; otherwise preserve uncertainty
- use `confidence:` / `status:` to mark the doubt, never silent flattening

Rough routing:
- conflict **as fact** -> cautious semantic update + Pending Review note
- conflict **as event** -> episodic (both versions are history, keep both)
- conflict **that changes behavior** -> procedural, old steps stay struck-through until new steps validated

---

## Minor vs Major

Keep it **episodic** when it is:
- local to the moment
- weakly evidenced
- interesting but not durable

Promote to **semantic** when it is:
- durable
- repeated
- confirmed
- a meaningful state change
- a new stable preference or constraint

Promote to **procedural** when it teaches:
- a repeatable step
- a safer method
- a better default behavior
- a reliable way to navigate this user's recurring situations well

Propose a **skill** (don't auto-create) when a procedural is `reuse: often` + stable across 2–3 runs + validated (`confidence: certain|likely`) + cross-project or tool-heavy value. Behavioral guidance never proposes. Say `Candidate: <file> -> .agents/skills/<suggested-skill-name>/ because <evidence>` and wait for approval. New skills are always project-local (`./.agents/skills/`) — never global unless explicitly requested. Most passes propose zero skills — that's success.

Simple promotion rule:
- what happened -> `episodic`
- what is true -> `semantic`
- what works next time -> `procedural`
- what works every damn time + stable -> propose skill (external, linked via `skill_ref`)

---

## Dream Mode Outcome

At the end of a dream pass:
- at least one meaningful memory is created or updated, or one episodic file is created/updated
- history stays meaningful
- semantic stays canonical
- procedural stays reusable with `reuse: once|often` marked
- skill candidates proposed (if any `reuse: often` + stable) or explicitly zero with rationale
- processed scope is clear
- duplicate memory spam is avoided

If memory files changed, rebuild `./memory/INDEX.md` with the script. Do **not** hand-edit `INDEX.md`; it is generated output and manual edits will be wiped on the next rebuild.
