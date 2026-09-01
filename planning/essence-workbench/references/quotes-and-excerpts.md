# Quotes and excerpts

This essence preserves verbatim wording that matters. Use it when exact phrasing, voice, legal wording, emotional charge, or source credibility would be weakened by paraphrase.

## Use when

- The original wording itself carries meaning, tone, evidence, or persuasive force.
- The source includes interviews, testimony, research passages, policy wording, or high-value lines that must stay exact.

## Do not use when

- Faithful paraphrase is enough and exact wording does not materially change meaning.
- The main value is stance classification rather than preserving the actual quote.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve attribution, context, and why the wording matters, but do not add callout styling, pull-quote layout, or narration performance notes here.

## Best editable shape

Prefer YAML.

```yaml
essence: quotes-and-excerpts
quotes:
  - excerpt: <verbatim text>
    speaker_or_source: <who said or wrote it>
    context: <where it appears>
    why_it_matters: <why this wording matters>
    tags:
      - <theme>
    evidence:
      - <citation or source note>
```

## What good quotes-and-excerpts content does

- Protects meaning that would be weakened by paraphrase.
- Keeps attribution and context attached to each quote.
- Makes later thematic work easier without losing source voice.

## Common failure modes

- Collecting quotable lines with no context or reason.
- Trimming quotes so hard that meaning shifts.
- Mixing paraphrase and verbatim text without labeling the difference.

## Preserve from the source

- Exact wording, attribution, surrounding context, and citation trail.
- Important emphases, hedges, and emotionally charged phrasing.
- Why each excerpt is worth carrying forward.

## Pre-save checks

- Each excerpt earns its place.
- Attribution and context are explicit.
- A future reader can tell what is verbatim and why it matters.
