# Prerequisites and dependencies

This essence captures what must exist first and what relies on what. Use it when order, readiness, or unlock logic matters.

## Use when

- The reader needs to know what must exist first, what unlocks what, or where work becomes blocked.
- Readiness, dependency direction, and gating conditions matter more than narrative or causal explanation.

## Do not use when

- The source is mainly a causal mechanism and should be modeled as `cause-and-effect-chains`.
- The main value is a step-by-step operating procedure rather than dependency structure.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve dependency type, readiness checks, and blocked consequences, but do not add roadmap visualization, course pacing, or gantt-style layout instructions here.

## Best editable shape

Prefer YAML.

```yaml
essence: prerequisites-and-dependencies
items:
  - name: <item>
    requires:
      - <dependency>
    unlocks:
      - <downstream item>
    notes:
      - <constraint or detail>
```

## What good prerequisites/dependencies content does

- Makes readiness and order immediately visible.
- Distinguishes what is required from what is merely helpful.
- Shows how blocked items affect downstream work.

## Common failure modes

- Buried prerequisites or unclear dependency direction.
- Optional inputs mislabeled as mandatory.
- Missing consequences of unmet dependencies.

## Preserve from the source

- Dependency type, sequence constraints, ownership, and blockers.
- Failure symptoms or readiness checks.
- Cycles, conflicts, or hidden coupling when they appear.

## Pre-save checks

- It is obvious what comes first and what depends on it.
- Required vs optional is explicit.
- A reader can tell how to verify readiness.
