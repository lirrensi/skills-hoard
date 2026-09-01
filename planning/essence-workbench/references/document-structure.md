# Document structure

This essence preserves the skeleton of a source: sections, nesting, chunk boundaries, and local flow. Use it when the source document's organization matters and should survive before any later compression or reshaping.

## Use when

- The source is a long document, report, book, spec, or transcript whose section structure carries meaning.
- You need a faithful map of what exists and where, before summarizing or reinterpreting it.

## Do not use when

- The main job is compression into the bottom line rather than preserving source structure.
- The source is better modeled as a taxonomy, a timeline, or a set of standalone records.

## Downstream intent note

- If the user already knows a likely later use, let that guide what details must survive, not how the material should be presented.
- Preserve headings, boundaries, and section intent, but do not add slide outline, page design, or navigation UI assumptions here.

## Best editable shape

Prefer Markdown.

```markdown
# <document title>

## Structure map

### <section>
- Purpose: <why this section exists>
- Contains:
  - <subtopic>
- Key transitions:
  - <what it leads into>

### <next section>
- Purpose: <why this section exists>
```

## What good document-structure content does

- Preserves the source skeleton without pretending it is already a summary.
- Makes section purpose and boundaries visible.
- Helps later work find and reshape the right chunks safely.

## Common failure modes

- Flattening all sections into one bland outline.
- Smuggling interpretation into what should be structural mapping.
- Losing nesting, transitions, or chunk boundaries.

## Preserve from the source

- Headings, order, nesting depth, local purpose, and chunk boundaries.
- Repeated section patterns, appendices, and major transitions.
- Source labels or numbering when they matter for traceability.

## Pre-save checks

- A reader can tell how the source is organized without opening the original.
- Section boundaries are explicit and stable.
- The map stays structural instead of turning into a summary blob.
