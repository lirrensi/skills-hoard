# Comparison

Comparison essence lines options up against the same criteria so tradeoffs become visible. Use it when the source discusses choices, alternatives, or competing approaches.

## Use when

- Several options need to be compared on a shared rubric.
- Tradeoffs, conditions, and decision context matter more than narrative flow.

## Do not use when

- The source mostly argues a single claim and needs an evidence audit instead.
- The material is chronological, procedural, or taxonomic rather than option-based.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve criteria, conditions, and uncertainty, but do not turn the comparison into a deck outline, scorecard design, or side-by-side page layout here.

## Best editable shape

Prefer YAML.

```yaml
essence: comparison
options:
  - name: <option>
    strengths:
      - <advantage>
    weaknesses:
      - <drawback>
    best_for:
      - <use case>
criteria:
  - <shared criterion>
recommendation:
  winner: <option or none>
  rationale: <why>
```

## What good comparison content does

- Makes tradeoffs visible on shared criteria.
- Separates description from recommendation.
- Helps a reader see when each option wins or loses.

## Common failure modes

- Uneven criteria that quietly favor one option.
- Persuasive tone disguised as neutral comparison.
- Assumptions filling evidence gaps.

## Preserve from the source

- Evaluation context, source-backed evidence, and uncertainty.
- Differences that materially affect a decision.
- Conditions under which each option is strongest.

## Pre-save checks

- Every option is compared on the same rubric.
- Unknowns are labeled as unknown.
- Any recommendation can be defended from the recorded evidence.
