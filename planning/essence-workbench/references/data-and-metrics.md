# Data and metrics

This essence captures the numbers, dimensions, and trends that matter. Use it when the source includes measurements, tables, reports, or quantitative claims.

## Use when

- Numbers, units, periods, formulas, or trend direction are central to the meaning.
- The reader will need metrics that stay interpretable, comparable, and auditable later.

## Do not use when

- The source is mostly qualitative and the numbers are only supporting texture.
- The main value lies in argument structure, story, or category logic rather than quantitative shape.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve units, periods, denominators, and lineage, but do not add chart types, dashboard cards, or infographic layout ideas here.

## Best editable shape

Prefer YAML.

```yaml
essence: data-and-metrics
metrics:
  - name: <metric>
    value: <number or text>
    unit: <unit>
    period: <time window>
    trend: up|down|flat|mixed|unknown
    note: <context>
    evidence:
      - <source note>
```

## What good data-and-metrics content does

- Makes each number interpretable, comparable, and auditable.
- Puts business meaning next to the value instead of assuming it.
- Shows whether the metric is observed, derived, or estimated.

## Common failure modes

- Missing units, denominators, or time windows.
- Definitions that drift away from how the number is computed.
- Reporting values without context, caveats, or lineage.

## Preserve from the source

- Exact metric definitions, formulas, and source lineage.
- Granularity, period, assumptions, and structural breaks.
- Notes that explain why a number moved or should be treated carefully.

## Pre-save checks

- Definition and formula agree.
- Units and time scope are explicit.
- A reader could trace the metric back to its source system.
