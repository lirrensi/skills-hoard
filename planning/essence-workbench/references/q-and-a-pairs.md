# Q&A pairs

Q&A pairs turn source material into grounded questions with direct answers. Use them when the audience will search, browse, or learn through explicit prompts.

## Use when

- The material naturally breaks into questions a reader would realistically ask.
- The future reader will browse, search, or study by prompt rather than by linear section order.

## Do not use when

- Sequence, argument flow, or story progression matters more than isolated questions.
- The source depends heavily on long-form explanation that would break if chopped into pairs.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Keep the Q&A set free of UI assumptions, scripted dialogue, or final channel formatting.

## Best editable shape

Prefer YAML.

```yaml
essence: q-and-a-pairs
confidence: medium
pairs:
  - question: <what the reader would ask>
    answer: <grounded answer>
    evidence:
      - <source note>
    follow_up_questions:
      - <gap or next question>
```

## What good Q&A content does

- Uses real questions a reader would actually ask.
- Gives answers that stand on their own without surrounding context.
- Breaks knowledge into clean, searchable units.

## Common failure modes

- Questions that are really headings, not questions.
- Answers that depend on hidden context or ambiguous pronouns.
- Bundling multiple topics into one pair.

## Preserve from the source

- Exact terminology, conditions, and exceptions.
- Source-specific meanings that prevent overgeneralization.
- Important unresolved follow-up questions.

## Pre-save checks

- Each pair still makes sense when moved out of context.
- The answer fully answers the question being asked.
- Near-duplicate questions have been merged or separated cleanly.
