# Scenarios and use cases

This essence captures actor-goal situations, triggers, paths, and edge cases. Use it when the source is best preserved as who is trying to do what under what conditions.

## Use when

- The source describes user situations, operational contexts, or journeys through a system.
- The important structure is goal plus context plus path, not just a prescribed procedure.

## Do not use when

- The source is a single recommended workflow that belongs in `steps-and-procedures`.
- The source is mainly illustrative stories that should stay in `examples-and-cases`.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve actor, trigger, outcome, and edge behavior, but do not add wireframes, lesson steps, or storyboard directions here.

## Best editable shape

Prefer YAML.

```yaml
essence: scenarios-and-use-cases
use_cases:
  - name: <use case>
    actor: <person or system>
    goal: <what they want>
    trigger: <what starts it>
    context:
      - <relevant condition>
    main_path:
      - <step>
    edge_cases:
      - <variation>
    outcome: <success result>
```

## What good scenarios-and-use-cases content does

- Preserves realistic situations instead of flattening everything into one ideal path.
- Makes actor intent and triggering context explicit.
- Keeps edge cases and failure branches visible.

## Common failure modes

- Turning every use case into a generic happy path.
- Confusing scenarios with implementation details.
- Losing the context that makes one case different from another.

## Preserve from the source

- Actor, goal, trigger, context, main path, variations, and outcome.
- Preconditions, edge cases, and notable exceptions.
- The condition that makes the scenario worth modeling separately.

## Pre-save checks

- Each use case has a distinct actor-goal combination.
- Edge cases are not hidden inside the main path.
- A reader can tell when to apply one scenario versus another.
