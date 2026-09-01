---
name: html-artifact
description: Build self-contained, single-file HTML artifacts and open them in the browser. Use for visualizations, interactive tools, presentations, living documents, and browser-native replacements for PDF, DOCX, PPTX, and spreadsheets. Prefer adapting starters when there is a close fit; otherwise build from scratch.
version: 1
---

# HTML Artifact Skill

Build complete browser-native artifacts as single HTML files.

The browser is not just a preview. It is the delivery format.

## What This Skill Is

A web artifact is a self-contained HTML file that:

- opens directly in a browser
- includes its own styles and scripts
- works without a build step
- is easy to share, copy, inspect, and version

Use this skill for:

- charts, dashboards, and visual explanations
- interactive tools, calculators, and generators
- presentations and slide-like experiences
- living documents that replace static files
- any request that is better as a browser experience than a dead document

## Core Thesis

Treat old office formats as outdated containers, not ideal outputs.

A resume should not need Word.
A report should not be trapped in PDF.
A calculator should not live in a spreadsheet.
A deck does not always need to be a deck.

Many things that used to become `.docx`, `.pdf`, `.pptx`, or `.xlsx` are better as living HTML pages: searchable, interactive, responsive, easy to revise, and easy to present.

## Working Style

Default to the fastest path that still produces a good artifact.

There are three ways to work:

1. Adapt a starter.
2. Build from scratch.
3. Fill a lightweight template shell.

Prefer starters when there is a clear match. Do not force a starter onto a request that is obviously custom.

## Starter First, But Not Blindly

Use a starter when the request closely matches an existing artifact family and the starter will save time without fighting the brief.

Build from scratch when:

- the request is novel or highly custom
- the layout is unusual or mixed across families
- adapting a starter would require more surgery than writing clean HTML directly
- the user clearly wants a bespoke artifact rather than a starter-flavored one

Use a template shell when the user mostly has content and needs a renderable surface, not a full interactive artifact.

## Artifact Families

Think in families first, not exact files.

- diagrams: Mermaid, Markmap, Graphviz
- presentations: Reveal.js, slideshow, or hybrid brief
- hybrid briefs: long-read documents that can also present one section at a time
- living documents: reports, runbooks, resumes, contracts, letters, calculators, changelogs
- data visualization: D3, Chart.js, dashboards, maps, network views
- tools and apps: Alpine, Preact, Fabric, custom HTML + JS
- exploration: CSV, JSON, interactive tables
- creative/browser-native visuals: SVG, p5, Three.js

When choosing a starter, inspect only the most relevant family under `starters/`.
Do not wander the whole library unless the fit is genuinely unclear.

## References: Keep Hops Low

This skill should usually require only one or two extra reads.

Typical flow:

1. Read this skill.
2. If choosing a starter, read `references/starter-catalog.md` and inspect only the relevant family.
3. If selecting a library, read `references/libraries-cheatsheet.md`.
4. Load only the specific design or technical reference that matters.

Do not load everything.

## Design Principles: Expected, Not Optional

Before generating visual or presentation work, load the right design reference.

- presentations, decks, slide-like experiences -> `references/slides-design-principles.md`
- charts, dashboards, infographics, visual explanations -> `references/infographic-design-principles.md`

Technical correctness is not enough. A chart can be valid and still be ugly, confusing, or cognitively rude.

Design rules:

- simplify aggressively for non-technical audiences
- keep one major idea per view when presenting
- prefer clear hierarchy over decoration
- use motion sparingly and purposefully
- make documents readable first, impressive second
- make presentation views scannable at distance

## Technical References

Load technical references only for the rendering stack you are actually using.

- Mermaid -> `references/mermaid-browser-guide.md`
- Markmap -> `references/markmap-browser-guide.md`
- Graphviz -> `references/graphviz-browser-guide.md`
- Reveal.js -> `references/revealjs-browser-guide.md`
- D3 -> `references/d3-browser-guide.md`

For general library choice, use `references/libraries-cheatsheet.md`.

## Authoring Rules

Every artifact should be a complete HTML file.

- put CDN links in `<head>` when needed
- keep CSS in a `<style>` block unless there is a strong reason not to
- keep JS at the end of `<body>`
- prefer semantic HTML over div soup
- default to responsive layouts
- include print-friendly behavior for document-like artifacts
- include small inline comments only where customization is non-obvious
- if derived from a starter, keep the file readable enough that the user can copy it and understand what is happening

If the artifact behaves like a document, optimize for:

- readability
- navigation
- searchability
- clear states and disclosures
- graceful print/export behavior

If the artifact behaves like a presentation, optimize for:

- one idea per section or slide
- clean contrast and legible type
- keyboard navigation
- presenter notes or appendix only when useful

## Hybrid Brief Principle

If the same content should work both as a document and a presentation, prefer a hybrid brief approach:

- `Read` mode for scrolling
- `Focus` mode for one-screen section viewing
- `Slides` mode for keyboard-driven presentation

This is often the right answer for briefs, status updates, roadmaps, approvals, meeting docs, launch plans, and evidence-heavy narratives.

## Output Location

All state and output files live in the current working directory.

Do not write into home directories or global temp locations unless using quick preview mode.

## Two Delivery Modes

### Quick Mode

Use when the user wants to see something fast and does not clearly need iteration.

- write a temp HTML file
- open it in the browser immediately
- cleanup can be temporary and disposable

### Rich Mode

Use when the user is likely to iterate.

- write to a stable HTML file in the current directory
- overwrite that file on re-run
- open it once, then let the user refresh or reopen as needed

## Default Workflow

1. Decide whether this is starter-fit, scratch-fit, or template-fit.
2. If it is visual or presentation-heavy, load the relevant design principles first.
3. If it uses a specialized renderer, load only that technical reference.
4. Adapt the closest starter or build from scratch.
5. Produce a complete HTML artifact.
6. Open it in the browser immediately.
7. If the user iterates, keep the file stable and editable.

## Minimal Routing

Use these as quick routing heuristics.

- flowcharts, sequences, architecture, ERDs, states -> Mermaid or Graphviz
- mind maps, note maps, concept maps -> Markmap
- decks and talks -> Reveal.js or slideshow
- document that should also present -> hybrid brief family
- charts and custom interactive visuals -> D3 or Chart.js
- multi-chart metric view -> dashboard starter
- maps and geo views -> Leaflet
- forms, calculators, generators, lightweight tools -> Alpine or custom HTML + JS
- small component-style apps -> Preact
- whiteboard or drag/drop canvas -> Fabric
- network maps and relationships -> Cytoscape
- markdown-like readable page -> markdown document starter or scratch HTML
- CSV or JSON exploration -> explorer starters
- spreadsheet-like editing -> table/grid starter
- living document replacing a static file -> match the closest living-document starter or hybrid brief

## When To Ignore Starters

Do not hunt for a starter just because starters exist.

Ignore starters and build directly when the request is:

- highly art-directed
- tightly branded
- structurally unusual
- a mashup of multiple families
- easier to write cleanly from scratch than to retrofit

## Success Criteria

The artifact should:

- open immediately in a browser
- feel intentional, not boilerplate
- match the audience and task
- be easy for the user to copy and modify
- use the browser as a real medium, not a fake PDF wrapper

## Final Note

Prefer the browser-native answer.

If a request sounds like "make a file," ask what the file should actually do.
Very often, the right answer is not another static document.
