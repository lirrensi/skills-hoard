# Gaps and unknowns

This essence documents what is missing, contradictory, or still uncertain. Use it when the value lies in showing incomplete understanding rather than pretending certainty.

## Use when

- The biggest truth in the source is what is still unresolved, contested, or blocked.
- Decision quality depends on keeping uncertainty explicit instead of polishing it away.

## Do not use when

- The source already contains actionable commitments that belong in `action-items`.
- The main job is to record supported conclusions rather than open questions and uncertainty.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve impact, blockers, and the source of uncertainty, but do not convert gaps into research plans, roadmap sections, or risk-slide formatting here.

## Best editable shape

Prefer YAML.

```yaml
essence: gaps-and-unknowns
gaps:
  - question: <what is unknown>
    type: missing|contradiction|uncertainty|assumption
    impact: high|medium|low
    blocked_decisions:
      - <what this affects>
    next_step: <how to reduce the gap>
```

## What good gaps-and-unknowns content does

- Makes uncertainty usable instead of vague.
- Shows exactly what is missing, contested, or unknowable right now.
- Connects each gap to the decision or conclusion it affects.

## Common failure modes

- Generic notes like "needs more research."
- Mixing absence of evidence with evidence of absence.
- Hiding scope limits or access constraints.

## Preserve from the source

- The exact unanswered question and why it remains open.
- Confidence level, cause of uncertainty, and practical impact.
- Any next step that could reduce the gap.

## Pre-save checks

- Each gap is specific enough to act on or reason about.
- The source of uncertainty is named.
- The implications for downstream conclusions are visible.
