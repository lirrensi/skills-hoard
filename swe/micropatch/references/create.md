# Create Mode

Use this mode when the user has an existing fork and wants to capture its intentional
customizations as one or more MicroPatches.

## Goal

Turn fork-specific code into durable, feature-level specs that can later be applied to
new upstream versions.

## Workflow

### 1. Gather the changes

Use whichever source best explains the fork:

- `git log <upstream-default-branch>..HEAD --oneline`
- `git diff <upstream-default-branch>..HEAD`
- a clean folder diff against a fresh upstream clone

Do not assume the whole fork is one feature.

### 2. Split changes into coherent patches

Group unrelated customizations into separate MicroPatches. A good MicroPatch represents
one coherent feature, fix, or intentional modification.

If grouping is ambiguous, ask the user.

### 3. Gather or infer intent

Learn what the change was trying to accomplish:

- What problem does it solve?
- Why does it live outside upstream?
- What behavior must remain true later?
- What assumptions or non-goals matter?

The diff shows what changed; the user explains why it matters.

### 4. Write the patch spec

Create `micropatch.md` using the required sections from `SKILL.md`.

Important rules:

- include enough real implementation to reproduce the feature
- use `files/` for large new files or bulky artifacts
- write `Definition of Done` so the agent can verify the result later
- write `Anchors` as file plus purpose plus likely integration point
- include upstream-overlap clues in `Notes for Future Re-application` when possible

### 5. Add `hints.diff` only if useful

If a trimmed diff would help orient future re-application, save one. Keep it curated and
small. It is only a search aid, not the source of truth.

### 6. Save and version

Use a descriptive folder name such as `micropatch-jwt-auth/` and start with `version: 1`.

## Creation Output

When create mode is complete, provide:

- the MicroPatch folders created
- how changes were grouped and why
- the generated `micropatch.md` content
- any optional `hints.diff` or `files/` artifacts created
- unresolved questions about intent, scope, or assumptions
