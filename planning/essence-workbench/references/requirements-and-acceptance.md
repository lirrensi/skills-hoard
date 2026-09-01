# Requirements and acceptance

This essence captures what must be true, how success will be checked, and what failure looks like. Use it when the source is a spec, request, scope definition, or product requirement set.

## Use when

- The source defines required behavior, quality expectations, or explicit success conditions.
- Later work will need a testable spec rather than just guardrails or narrative description.

## Do not use when

- The source is mostly policy or invariants and belongs in `rules-and-constraints`.
- The source is mainly a procedure for how to perform work rather than a statement of what must be satisfied.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve requirement wording, scope, and checks, but do not add ticket formatting, UI mock assumptions, or release-plan structure here.

## Best editable shape

Prefer YAML.

```yaml
essence: requirements-and-acceptance
requirements:
  - id: <stable-id>
    statement: <requirement>
    type: functional|nonfunctional|constraint|assumption
    priority: must|should|could
    acceptance_criteria:
      - <observable check>
    failure_conditions:
      - <what counts as failure>
    source:
      - <where it came from>
```

## What good requirements-and-acceptance content does

- Makes success observable instead of hand-wavy.
- Separates requirement statements from how they will later be implemented.
- Preserves scope, priority, and testability.

## Common failure modes

- Vague requirements with no acceptance criteria.
- Mixing implementation ideas into the requirement itself.
- Silent scope drift between the request and the saved spec.

## Preserve from the source

- Exact requirement wording when it changes meaning.
- Priority, scope boundaries, assumptions, and failure conditions.
- Observable checks that show whether the requirement was actually met.

## Pre-save checks

- Each requirement is testable or at least falsifiable.
- Acceptance criteria are concrete enough to verify later.
- Implementation choices are not pretending to be requirements.
