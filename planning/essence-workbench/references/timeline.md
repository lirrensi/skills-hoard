# Timeline

A timeline orders events so sequence, causality, and pace become easy to inspect. Use it when the source spans multiple moments, milestones, or turning points.

## Use when

- Order in time is the main structure the reader must understand.
- Milestones, phases, turning points, or changing context over time carry the meaning.

## Do not use when

- Mechanism matters more than dates and should be modeled as a causal chain.
- The source is better understood as categories, entities, or a static comparison.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve date precision, turning points, and significance, but do not turn the timeline into slide pacing or storyboard beats here.

## Best editable shape

Prefer YAML.

```yaml
essence: timeline
confidence: medium
events:
  - date: <date or range>
    event: <what happened>
    cause:
      - <why it happened>
    consequence:
      - <what changed after>
    evidence:
      - <source note>
```

## What good timeline content does

- Makes sequence, pace, and turning points easy to inspect.
- Includes events because they matter, not just because they happened.
- Shows what changed after each important moment.

## Common failure modes

- Noisy event lists with no sense of significance.
- Mixed date precision or hidden date conflicts.
- Missing causal bridges between adjacent events.

## Preserve from the source

- Date precision, timezone context, and uncertainty.
- Cause-and-consequence links when the source supports them.
- Related parent-child event structure.

## Pre-save checks

- Chronology is unambiguous from start to finish.
- Approximate or conflicting dates are labeled explicitly.
- Each entry earns its place by explaining why it matters.
