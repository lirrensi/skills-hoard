# Observations and signals

This essence captures raw findings, anomalies, symptoms, and weak signals before they are fully synthesized. Use it when the material is still exploratory and the honest job is to preserve what was noticed.

## Use when

- The source is messy discovery material: research notes, field observations, bug reports, interviews, monitoring notes, or exploratory analysis.
- You need to preserve what was seen, heard, or noticed before upgrading it into themes or conclusions.

## Do not use when

- Cross-source synthesis has already matured into recurring themes.
- The main value is unknowns and blockers rather than observed signals.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve signal, source, and implication, but do not add chart assumptions, report framing, or polished insights language here.

## Best editable shape

Prefer YAML.

```yaml
essence: observations-and-signals
observations:
  - signal: <what was noticed>
    type: finding|anomaly|symptom|pattern-candidate|risk-signal
    source: <where it came from>
    confidence: high|medium|low
    implication: <why it might matter>
    follow_up:
      - <next check>
```

## What good observations-and-signals content does

- Preserves real findings before they get overinterpreted.
- Keeps weak signals visible without pretending they are settled themes.
- Connects each observation to a source and possible implication.

## Common failure modes

- Smuggling conclusions into what should still be observational.
- Recording generic notes with no source or relevance.
- Hiding uncertainty because the findings feel messy.

## Preserve from the source

- What was observed, where it came from, how strong it looks, and why it might matter.
- Contradictory or outlier signals that complicate the picture.
- Follow-up checks that could strengthen or weaken the signal.

## Pre-save checks

- Each observation is specific and attributable.
- Confidence is honest, not performative certainty.
- Findings stay as findings instead of pretending to be final conclusions.
