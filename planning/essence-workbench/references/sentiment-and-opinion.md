# Sentiment and opinion

This essence captures how people feel, what stance they take, and how strongly they express it. Use it when tone, preference, or attitude is a meaningful signal.

## Use when

- Attitude, tone, or stance is itself evidence worth preserving.
- The reader will need attribution, strength, and nuance of opinion rather than only factual content.

## Do not use when

- The main job is to audit factual claims or map neutral entities and relationships.
- The source should stay as a formal argument structure instead of an opinion landscape.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve speaker, target, strength, and hedging, but do not turn tone into character acting notes, narration style, or audience messaging strategy here.

## Best editable shape

Prefer YAML.

```yaml
essence: sentiment-and-opinion
opinions:
  - speaker: <person or group>
    stance: positive|negative|mixed|neutral
    topic: <subject>
    strength: strong|moderate|weak
    evidence:
      - <quote or paraphrase>
    nuance: <qualification>
```

## What good sentiment-and-opinion content does

- Separates stance, intensity, attribution, and rationale.
- Preserves voice without confusing opinion with fact.
- Captures mixed or conditional attitudes honestly.

## Common failure modes

- Flattening everything into positive or negative.
- Losing who holds the view or what the view is about.
- Smoothing away hedging, ambiguity, or emotional charge.

## Preserve from the source

- Speaker, target, quoted wording, and reasons given.
- Hedging, confidence signals, and ambivalence.
- Evidence basis for the opinion when present.

## Pre-save checks

- A reader can tell who holds the view and how strongly.
- Tone and stance are grounded in source language.
- Mixed sentiment remains mixed where the source is mixed.
