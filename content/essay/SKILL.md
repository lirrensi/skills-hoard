---
name: essay
description: Essay finishing orchestrator for messy notes, partial drafts, and nearly-done essays. Use when the user already has substantial material and wants it finalized, reviewed, or polished while following shared editorial principles from EDITING.md and optional voice guidance from VOICE.md. Optimized for emotionally resonant, broadly accessible essays rather than academic-sounding prose.
---

# Essay Orchestrator

This skill is the orchestrator.

It does not contain the full editorial brain inside every step file.

- The **project root `EDITING.md`** is the canonical editorial principles file for that folder.
- The **project root `VOICE.md`** is the optional voice file for that folder.
- The bundled `EDITING.md` and `VOICE.md` inside this skill are reference templates and fallbacks, not the preferred working source.
- `steps/` contains lightweight workflows for each mode.

## Required startup behavior

When this skill is invoked:

1. **Check the project root for `EDITING.md`.** This should be the main editorial principles file for the folder.
2. **If root `EDITING.md` exists, read it first.** If it does not exist, offer to create it from the bundled template/reference before proceeding, or temporarily fall back to the bundled `EDITING.md` if the user prefers.
3. **Check the project root for `VOICE.md`.**
4. **If root `VOICE.md` exists, use it.** If it does not exist, treat voice as undefined-but-important: infer from the user's material for the current pass, and when the task involves substantial rewriting/finalizing, ask whether the user wants to create `VOICE.md` for future consistency.
5. **Inspect the user's actual material**:
   - notes
   - fragments
   - draft files
   - links
   - feedback
6. **Classify the current state**:
   - messy notes
   - rough draft
   - working draft
   - almost-finished draft
   - draft with feedback
7. **Route to the lightest useful mode.**

## Main modes

- **finalize** — default mode; turn messy substantial material into a structured finished piece
- **review** — diagnose argument, structure, dead zones, and finishability
- **polish** — line-level cleanup once the essay already works

## Support modes

- **brief** — extract the essay's core intent when the spine is unclear
- **outline** — recover or propose structure explicitly
- **draft** — build a full draft from rougher material
- **revise** — edit a specific section or passage

## Routing guidance

- If the user already has a lot of material, prefer **finalize**.
- If the user wants a tough diagnosis before editing, use **review**.
- If the structure already works and the request is mostly sentence-level, use **polish**.
- Use support modes only when the main modes are not enough.

## Rules

- Treat root `EDITING.md` as the editable principles file for the folder.
- Treat root `VOICE.md` as the editable voice file for the folder when it exists.
- Do not scatter editorial principles across step files if they already belong in `EDITING.md`.
- Do not override voice guidance from `VOICE.md`.
- If no `VOICE.md` exists, infer voice from the user's text, say what you are preserving, and offer to create `VOICE.md` when useful.
- Prefer the smallest effective intervention.
- Keep the workflow practical and lightweight.
- Default to intelligent broad-reader clarity unless the user clearly wants something more specialized.
- Prefer direct, conversational prose over academic framing or prestige-sounding diction.
- If the user wants accessibility, optimize for first-read comprehension and felt force, not formal sophistication.

## Step routing

| User says | Load |
|-----------|------|
| `finalize` or "help me finish this" | `steps/finalize.md` |
| `review` | `steps/review.md` |
| `polish` | `steps/polish.md` |
| `brief` | `steps/brief.md` |
| `outline` | `steps/outline.md` |
| `draft` | `steps/draft.md` |
| `revise` | `steps/revise.md` |
