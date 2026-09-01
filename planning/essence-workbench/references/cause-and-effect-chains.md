# Cause and effect chains

This essence models how one condition leads to another across a chain. Use it when the source explains mechanisms, failures, escalation, or root causes.

## Use when

- The reader needs to understand how one condition produces another across linked steps.
- Mechanism, escalation, or root cause matters more than date order alone.

## Do not use when

- The source mainly needs a chronology of events rather than a modeled mechanism.
- The main structure is dependency order, not actual causal explanation.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve mechanism, confidence, and boundary conditions, but do not add visual flow layout, slide sequence, or explainer pacing here.

## Best editable shape

Prefer YAML.

```yaml
essence: cause-and-effect-chains
chains:
  - cause: <starting condition>
    leads_to: <next effect>
    because: <mechanism>
    confidence: high|medium|low
    evidence:
      - <source note>
```

## What good cause-and-effect content does

- Explains not just what happened next, but how one condition led to another.
- Makes the mechanism visible step by step.
- Shows where certainty is strong and where it becomes inferential.

## Common failure modes

- Jumping from correlation to causation.
- Skipping mediating steps or external drivers.
- Treating every link as equally certain.

## Preserve from the source

- Sequence, mechanism, assumptions, and boundary conditions.
- Confounders or external factors that may change the chain.
- Evidence supporting each link.

## Pre-save checks

- Each step answers "how," not just "what followed."
- Direct causes are distinguished from enabling conditions.
- The chain stops where support stops.
