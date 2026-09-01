# Examples and cases

This essence collects concrete examples that make an abstract point easier to understand. Use it when the source teaches through instances, stories, or case studies.

## Use when

- Concrete cases are the best way to preserve the lesson, constraint, or pattern in the material.
- The reader will need illustrative situations, not just abstract statements.

## Do not use when

- The main value is cross-source synthesis that belongs in `patterns-and-themes`.
- The source is better captured as a taxonomy, summary, or procedure instead of example-driven learning.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve context, outcome, and takeaway, but do not convert cases into storyboard panels, slide examples, or polished case-study copy here.

## Best editable shape

Prefer YAML.

```yaml
essence: examples-and-cases
cases:
  - name: <case>
    demonstrates:
      - <concept or lesson>
    context: <situation>
    outcome: <result>
    takeaway: <why it matters>
```

## What good examples-and-cases content does

- Makes abstract ideas concrete enough to reason about.
- Uses cases that teach interpretation, not just formatting.
- Helps readers generalize by showing why the example matters.

## Common failure modes

- Toy examples that ignore real constraints.
- Happy-path cases only, with no boundary behavior.
- Leaving the lesson implicit.

## Preserve from the source

- Triggering context, relevant constraints, outcome, and tradeoffs.
- Contrasting successful and failing cases when useful.
- The explicit takeaway the case supports.

## Pre-save checks

- The set covers typical and edge scenarios.
- Each case teaches a clear lesson.
- A reader could generalize from the examples without overfitting to them.
