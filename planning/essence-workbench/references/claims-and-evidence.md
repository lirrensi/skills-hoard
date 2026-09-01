# Claims and evidence

This essence separates what is being asserted from what actually supports it. Use it when the source makes arguments, recommendations, or conclusions that need grounding.

## Use when

- The main job is to audit whether assertions are supported, weak, overstated, or still open.
- You need an evidence-first structure that keeps claims reviewable later.

## Do not use when

- The source is mainly a debate between positions and needs objections and rebuttals as the core structure.
- A fast orientation summary is enough and a full evidence ledger would be overkill.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve qualifiers, support, and gaps, but do not reshape the file into persuasion copy, a debate script, or speaker-ready talking points here.

## Best editable shape

Prefer YAML.

```yaml
essence: claims-and-evidence
claims:
  - claim: <assertion>
    evidence:
      - <supporting fact>
    confidence: high|medium|low
    counterpoints:
      - <qualifier or objection>
    gaps:
      - <missing support>
```

## What good claims-and-evidence content does

- States each claim in bounded, checkable language.
- Connects support to the claim instead of dumping evidence nearby.
- Makes strength, weakness, and contestability visible.

## Common failure modes

- Mixing evidence, interpretation, and opinion in one field.
- Claims that are too broad for the support provided.
- Confirmation bias that hides counterevidence or thin support.

## Preserve from the source

- The reasoning link between evidence and claim.
- Counterpoints, limitations, and source credibility signals.
- Exact qualifiers that control how strong the claim really is.

## Pre-save checks

- Every claim has support that is specific enough to review.
- Confidence matches the actual strength of the evidence.
- Contradictions and gaps remain visible.
