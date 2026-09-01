# Decisions and rationale

This essence captures what was decided, what alternatives were considered, and why the choice was made. Use it when the source contains decision-making, tradeoffs, and justification that should remain auditable later.

## Use when

- The source includes choices, recommendations, approvals, or settled direction.
- Future readers will need to understand why something was chosen, not just what happened next.

## Do not use when

- The main value is a side-by-side evaluation that is still unresolved.
- The source is mostly follow-through tasks rather than the logic behind a decision.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve alternatives, tradeoffs, and consequences, but do not add memo formatting, slide recommendations, or executive polish here.

## Best editable shape

Prefer YAML.

```yaml
essence: decisions-and-rationale
decisions:
  - topic: <decision area>
    status: proposed|accepted|rejected|revisited
    chosen_option: <what was selected>
    rationale:
      - <why>
    alternatives:
      - <option>
    tradeoffs:
      - <cost or consequence>
    evidence:
      - <source note>
```

## What good decisions-and-rationale content does

- Separates the final choice from the reasons supporting it.
- Keeps alternatives and tradeoffs visible so future readers can revisit cleanly.
- Preserves enough context to avoid re-litigating the same issue blindly.

## Common failure modes

- Recording only the outcome and losing why it happened.
- Rewriting history so rejected options disappear.
- Mixing action items into the decision record.

## Preserve from the source

- Decision status, rationale, alternatives, tradeoffs, assumptions, and known consequences.
- Who made or endorsed the decision when that matters.
- Open questions or revisit triggers that could change the choice later.

## Pre-save checks

- A future reader can tell what was chosen and why.
- Rejected or deferred alternatives are still visible.
- Tasks created by the decision are not confused with the decision itself.
