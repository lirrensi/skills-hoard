# Improve Mode

Use this mode when revising an existing skill folder.

## Inputs To Collect

- target skill
- user complaint or weak spot
- local comparison skills
- source material the skill should rely on
- any regression or eval notes

## Workflow

1. Read the target skill first.
2. Compare it against strong neighboring skills.
3. Classify the failure surface:
   - under-triggering
   - over-triggering
   - bloat
   - stale guidance
   - missing decision rules
   - missing recovery paths
   - weak source anchoring
4. Make the smallest change that fixes the root cause.
5. Preserve the skill's identity unless the user asks for a larger shift.
6. Push reusable detail into references instead of expanding `SKILL.md`.
7. Re-evaluate the changed behavior with realistic prompts if the edit matters.

## Good Repairs

- tighten the trigger
- improve routing
- cut ceremony
- add a missing branch or prerequisite
- move repeated logic into a reference
- replace vague advice with source-backed instruction
