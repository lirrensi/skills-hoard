# Rules and constraints

This essence captures what must, must not, or can only happen under conditions. Use it when the source contains policy, law, requirements, guardrails, or system invariants.

## Use when

- The source contains obligations, prohibitions, limits, or invariants that must stay testable.
- Scope, exception handling, and normative wording materially affect meaning.

## Do not use when

- The source is mainly a procedure for execution rather than a set of guardrails.
- The main value is task follow-through, not the rule system itself.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve scope, exception, and obligation strength, but do not convert rules into page layout, checklist visuals, or training script cues here.

## Best editable shape

Prefer YAML.

```yaml
essence: rules-and-constraints
rules:
  - statement: <rule>
    type: requirement|prohibition|limit|invariant
    scope: <where it applies>
    exceptions:
      - <exception>
    source:
      - <where it came from>
```

## What good rules-and-constraints content does

- Makes obligations testable and easy to apply.
- Distinguishes hard requirements from softer guidance.
- Shows who is bound, under what conditions, and with what exceptions.

## Common failure modes

- Vague wording that cannot be checked in practice.
- Multiple rules collapsed into one fuzzy statement.
- Hidden exceptions or undocumented scope boundaries.

## Preserve from the source

- Original obligation strength, authority, scope, and timing.
- Exceptions, approvals, and conditionals.
- Normative wording when it changes meaning.

## Pre-save checks

- Someone could verify compliance from the file alone.
- It is clear who or what the rule applies to.
- Exceptions and non-applicability cases are explicit.
