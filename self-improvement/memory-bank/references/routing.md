# Routing & Saving (full)

> Companion to `SKILL.md` → Quick Routing + Learn Pass. Load this when unsure where a piece of knowledge belongs, whether to create or update, or what is worth saving at all.

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
- When information conflicts, **cry loudly, don't stupidly overwrite**: say `CONTRADICTION: <file> says X, new evidence says Y` in your reply, keep both visible until resolved. You change a canonical file only when you can cite evidence (`source:`, session date, pending line, URL, or re-validation). No evidence → keep old text, add a `## Pending Review` note with the specific claim + what would prove it, drop `confidence` to `tentative`. Newer wins only when credible + evidenced; otherwise preserve uncertainty.

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

Do **not** overfit one weak moment into a lasting fact or rule too quickly.

## When to Save

No strict rules — use judgment. Good candidates:
- Something that took real effort to figure out (research, debugging, negotiation, comparison)
- A decision with non-obvious reasoning — why X over Y
- Information that would be painful to reconstruct if this conversation ended
- Anything the user explicitly wants remembered
- A preference, profile, or constraint likely to matter again
- A workflow, checklist, or behavioral pattern you'll likely reuse
- A bug, config detail, or environment-specific gotcha that could bite again later
- Behavioral guidance — how to approach a situation, tone rules, interaction patterns that work well with this user or context

Not worth saving:
- Easily googleable facts
- Transient scratchpad work
- Anything the user will obviously remember themselves

## Proactive Saving (failures first-class)

Since this skill is loaded, memory is clearly valued here — lean into it. Save without being asked when you encounter the candidates above, plus:

- Dead ends and failed approaches — saves future sessions from repeating them. Failures > wins: record what NOT to do, the gotcha, the wrong turn, with tags `failed-approach`, `gotcha`.
- In-progress work with clear next steps.

Failures are first-class: a `failure` capture (`capture.py "..." --type failure`) or an episodic `Dead Ends` section is often more valuable than a success story. Don't polish — record the ugly bit while working, curate at `learn`.

Applies to any domain — code, business, personal, creative, research, client work, anything.
