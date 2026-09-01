# Stakeholders and positions

This essence captures who cares, what they want, what they resist, and how much leverage they have. Use it when politics, incentives, alignment, or conflict matter as much as the underlying facts.

## Use when

- The source involves decision-makers, affected parties, sponsors, critics, or groups with different incentives.
- You need to preserve stance, interest, concern, and influence instead of just mapping neutral entities.

## Do not use when

- The main job is to describe a neutral system map, org chart, or domain graph.
- The source is mostly sentiment without strategic implications or stakeholder conflict.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve incentives, concerns, and leverage, but do not add stakeholder map visuals, comms strategy, or meeting choreography here.

## Best editable shape

Prefer YAML.

```yaml
essence: stakeholders-and-positions
stakeholders:
  - name: <person or group>
    role: <why they matter>
    wants:
      - <goal>
    concerns:
      - <fear or objection>
    stance: supportive|opposed|mixed|neutral|unknown
    influence: high|medium|low
    leverage:
      - <source of power>
    evidence:
      - <source note>
```

## What good stakeholders-and-positions content does

- Makes incentives and alignment legible.
- Separates stakeholder identity from stance and leverage.
- Keeps conflict and dependency visible without moralizing it away.

## Common failure modes

- Treating all stakeholders as equally important.
- Recording names with no actual position or incentive.
- Confusing sentiment with strategic leverage.

## Preserve from the source

- Stakeholder role, incentives, concerns, stance, influence, and dependencies.
- Evidence for non-obvious positions or leverage.
- Areas of alignment, conflict, and unresolved tension.

## Pre-save checks

- A reader can tell who matters and why.
- Stance and leverage are not blurred together.
- Conflict, alignment, and uncertainty are all explicit.
