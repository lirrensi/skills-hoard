---
name: delivery-discovery
description: Help a user decide how they want to experience an existing essence. Use when the user is unsure which delivery format or modality fits best, wants examples, or needs recommendations grounded in current workspace capabilities. This skill is conversational guidance, not rendering.
---

# Delivery Discovery

Use this skill only when the user has an essence and is still deciding how the result should feel and arrive.

If the user already knows the target experience, skip this skill and go straight to implementation.

## Workflow

1. Identify the current essence and the user's goal.
2. Open `../formats.md` for the full catalog, then use `references/recommendation-patterns.md` to narrow the field.
3. Suggest 3-5 delivery formats that suit the essence, with short reasons and watchouts.
4. Open `references/modalities.md` and suggest the best matching modalities for the strongest formats.
5. Quietly check current capabilities using `references/capability-check.md`, then present options as `recommended now`, `good with setup`, or `possible but awkward`.
6. Stop once the user has enough confidence to choose or to skip discovery and implement directly.

## What this skill does

- Helps the user choose a delivery format.
- Helps the user choose a modality.
- Explains tradeoffs in plain language.
- Filters recommendations through local capabilities when possible.
- Suggests setup only when a missing capability blocks an otherwise strong idea.

## What this skill does not do

- It does not render the final output.
- It does not pick libraries as the main event.
- It does not require writing a handoff file.
- It does not force the user through discovery if they already know what they want.

## Conversational stance

- Start from the essence, not from tools.
- Recommend a few strong options, not the whole catalog.
- Distinguish `format` from `modality` clearly.
- Treat capability checks as a reality filter, not as the center of the conversation.
- If a compelling path needs setup, say so directly and name the missing capability.

## Minimal output

Usually the output is just the decision reached in conversation.

If a handoff note would help, keep it tiny:

```yaml
essence: <existing essence>
chosen_format: <delivery format>
chosen_modality: <modality>
notes:
  - <key watchout>
  - <audience or tone note>
```

## References

- Full ontology: `../formats.md`
- Essence-to-format fit hints: `references/recommendation-patterns.md`
- Modality guide: `references/modalities.md`
- Capability check rubric: `references/capability-check.md`
