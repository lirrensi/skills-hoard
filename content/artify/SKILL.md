---
name: artify
description: Build self-contained, single-file HTML artifacts and serve them with the artify CLI. Use for visualizations, interactive tools, presentations, living documents, forms and quizzes that return structured data via artify snapshot, and any browser-native replacement for static files. Prefer adapting starters when there is a close fit; otherwise build from scratch. No install required — the CLI runs via uv against the bundled standalone package.
version: 3
---

# HTML Artifact Skill

Build complete browser-native artifacts as single HTML files.

The browser is not just a preview. It is the surface. And when the artifact is interactive, the browser is also the input.

> **Standalone & install-free.** This skill is fully self-contained. The `artify`
> CLI lives in [`cli/`](cli/) as its own tiny Python package that declares its own
> requirements. It is **not** part of `agent-sommelier` and needs no global install.
> Run it via the bundled launcher, which uses `uv run --project` to resolve the
> deps into a throwaway environment on demand.

## Running the CLI (no install required)

The skill ships a launcher that wires the CLI up without installing anything globally. From the skill's own folder:

- **Windows (PowerShell):** `.\scripts\artify.ps1 <command> [args...]`
- **macOS / Linux (shell):** `./scripts/artify <command> [args...]`

You only need `uv` on PATH (or set `ARTIFY_UV` to its location). The launcher calls:

```bash
uv run --project <skill>/cli artify <command> [args...]
```

which makes `uv` read `cli/pyproject.toml` and create a per-project environment
with the CLI's declared deps (`click`, `rich`, `psutil`, `watchdog`) the first time.
Every command below is invoked through this mechanism — never via a globally
installed `artify`.

## What This Skill Is

A web artifact is a self-contained HTML file that:

- opens directly in a browser
- includes its own styles and scripts
- works without a build step
- is easy to share, copy, inspect, and version
- can be served live with `artify serve` so edits reload without ceremony
- can be queried with `artify snapshot` so the page becomes a structured input

Use this skill for:

- **Visual explanation** — when a chart, diagram, or layout says more than console text can
- **Presentations and slide-like experiences** — when a deck is the right shape for the message
- **Interactive tools** — calculators, generators, dashboards with controls the user manipulates
- **Forms, quizzes, surveys, and editors** — anything the user fills in and the agent reads back via `artify snapshot`
- **Living documents** that replace static files
- **Any request that is better as a browser experience than a dead document or a long CLI interview**

## Core Thesis

Console text is descriptive, not experiential. When the user needs to *see* something — a chart, a layout, a flow, a comparison — the right answer is not a longer markdown block. It is a page.

And when the user needs to *interact* with something — fill a form, answer a quiz, drag a slider, click a toggle — the right answer is not a CLI prompt. It is a page. The browser is not a preview. It is the surface.

The same page is also the *input*. Build a form, a quiz, or an interactive dashboard, let the user fill it in, then run `artify snapshot <port>` to read the state back as JSON. The HTML becomes both the interface and the data source. That collapses a lot of "I need to ask the user twenty questions in a loop" into "build one page, snapshot it."

Treat old office formats as outdated containers, not ideal outputs.

- A resume should not need Word.
- A report should not be trapped in PDF.
- A calculator should not live in a spreadsheet.
- A deck does not always need to be a deck.
- A form does not need a long CLI interview.
- A dashboard does not need a dozen follow-up questions.

Many things that used to become `.docx`, `.pdf`, `.pptx`, or `.xlsx` — or twenty sequential CLI prompts — are better as living HTML pages: searchable, interactive, responsive, easy to revise, easy to present, easy to query.

## Three Modes of Operation

The `artify` CLI gives you three modes. Pick the lightest one that does the job.

### `artify open` — Offline, no server, just a file

`artify open FILE.html` opens the file in the default browser via `file://`. No server, no reload, no state.

Use this when:
- The artifact is finished and the user just wants to see it
- The artifact is fully self-contained and will not iterate
- The user is going to read or print, not interact

### `artify serve` — Live iteration, addressable instance

`artify serve FILE.html` starts a local HTTP server on a random port, opens the page in a browser, watches the file for changes, and live-reloads the tab whenever you save. The port is the instance's ID — stable for as long as the instance runs.

Use this when:
- You are building the artifact and want to see changes as you save
- The user is going to interact with the page
- You will need to query the page state (`artify snapshot`)
- You want a stable URL to point someone at

`artify serve FILE.html --webview` opens in a chromeless native window instead of a browser tab. Useful for focused, fullscreen-ish views and presentations.

Manage running instances:

```
artify list              # show all running instances (PORT, PID, FILE, STATUS, URL)
artify kill <port>       # kill an instance, clean up its registry entry
artify restart <port>    # kill and re-serve the same file on a new port
```

For long-running or detached use, wrap with the existing `bg` tool: `bg run "artify serve report.html"`.

### `artify snapshot` — Query the page

`artify snapshot <port>` asks the running instance to collect its current state and returns it as JSON. The page is already polling for snapshot commands (alongside the live-reload check); when the CLI triggers one, the page collects the form fields (or calls `window.__artify_collect__` if defined) and posts them back. The CLI blocks until the page responds, then prints.

Use this when:
- The page is a form, quiz, survey, or editor and you need the user's answers
- The page is a dashboard with interactive controls (sliders, toggles, selections) and you need the current configuration
- The page has custom state captured by `window.__artify_collect__`

The flow is: build a form, let the user fill it in, run `artify snapshot <port>`, get the JSON. One round-trip, no waiting, no blocking from your side. If the user is mid-edit, snapshot just returns what is currently in the fields — there is no "submit" gate. The page is the source of truth.

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
- the artifact is a form or query with field shapes that don't match any starter

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
- forms, quizzes, surveys, and editors: pages the user fills in, read back via `artify snapshot`
- interactive dashboards: controls the user manipulates, read back via `artify snapshot`

When choosing a starter, inspect only the most relevant family under `starters/`. Do not wander the whole library unless the fit is genuinely unclear.

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
- make forms, quizzes, and editors immediately obvious — the user should never wonder what to fill in
- make dashboard controls obviously interactive — sliders look like sliders, toggles look like toggles, clickable regions look clickable

## Snapshot Principle

`artify snapshot <port>` is the bridge between the page and the agent. Build a page, let the user interact with it, snapshot it.

A snapshot automatically collects the current state of every form field that has a `name` or `id` — inputs, textareas, selects, checkboxes, radios. Disabled fields are skipped. Submits, buttons, and resets are skipped.

For anything the default collector cannot see — Alpine or Preact component state, scroll position, computed values, multi-step progress, custom widgets — define a function on the page:

```html
<script>
  window.__artify_collect__ = function() {
    return {
      fields: collectStandardFormFields(),
      scrollY: window.scrollY,
      selectedTheme: app.theme,
      currentStep: wizard.currentStep,
      computedTotal: cart.total()
    };
  };
</script>
```

The function is called every time a snapshot is requested. Return whatever JSON shape you want. The CLI prints it verbatim.

Three rules for snapshot pages:
- Every field the agent needs must have a `name` or `id` (or be returned by your custom collector). The collector cannot guess intent.
- Disable fields you do not want to capture (`disabled` attribute on inputs, `disabled` attribute on options in selects).
- For multi-step flows, return the current step in your custom collector so the agent can see progress, not just the final answer.

The default 30s timeout covers the polling latency plus a generous pause for the user. Override with `--timeout` if the form is large or the user might walk away.

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

If the artifact will be snapshotted, every interactive element should have a stable identifier. `name` for form fields, `id` for anything else. Treat field names as the data contract with the agent.

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

If the artifact behaves like a form, quiz, survey, or editor, optimize for:
- clear labels and obvious inputs — never make the user guess what to fill in
- one question per field, one field per question
- visible feedback for selections, validations, and state changes
- keyboard navigability — tab order must be sensible
- the data you return is structured and predictable — avoid free-form blobs when discrete fields will do
- the user must be able to see the whole form without scrolling on a laptop screen

If the artifact behaves like a dashboard with interactive controls, optimize for:
- controls that obviously look interactive
- visible state for every control (selected / unselected, current value, slider position)
- the user can configure and inspect in one view
- the snapshotted state is a complete record of the configuration — no "I forgot to mention..."

## Hybrid Brief Principle

If the same content should work both as a document and a presentation, prefer a hybrid brief approach:
- `Read` mode for scrolling
- `Focus` mode for one-screen section viewing
- `Slides` mode for keyboard-driven presentation

This is often the right answer for briefs, status updates, roadmaps, approvals, meeting docs, launch plans, and evidence-heavy narratives.

## Output Location

All artifact files live in the current working directory. Do not write into home directories or global temp locations.

The `artify` CLI manages its own runtime state in `~/.artify/instances/`. You do not need to think about it — `artify serve` writes a registry entry, `artify list` shows them, `artify kill` cleans them up.

## Default Workflow

1. Decide whether this is visual, interactive, a form, a presentation, or a document.
2. If it is a form, quiz, or interactive query, decide what data you need back. Plan the field names, types, and validation. If you need data the form fields cannot capture, plan the `window.__artify_collect__` shape.
3. If it is visual or presentation-heavy, load the relevant design principles first.
4. If it uses a specialized renderer, load only that technical reference.
5. Adapt the closest starter, or build from scratch.
6. Produce a complete HTML artifact.
7. If you will iterate: `artify serve FILE.html` and edit in your editor. The tab reloads as you save.
8. If the user just wants to see it: `artify open FILE.html`.
9. If you need data back: serve, let the user interact, then `artify snapshot <port>`.
10. If the user iterates, keep the file stable and editable. Do not move it.

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
- quiz, survey, intake form, or structured questionnaire -> custom HTML + JS with named fields, snapshotted when done
- interactive dashboard with sliders, toggles, selectors -> custom HTML + JS or Alpine, snapshotted for the configuration

## When To Ignore Starters

Do not hunt for a starter just because starters exist.

Ignore starters and build directly when the request is:
- highly art-directed
- tightly branded
- structurally unusual
- a mashup of multiple families
- easier to write cleanly from scratch than to retrofit
- a form or query with very specific field shapes that don't match any starter

## Success Criteria

The artifact should:
- open immediately in a browser (`artify open` or `artify serve`)
- feel intentional, not boilerplate
- match the audience and task
- be easy for the user to copy and modify
- use the browser as a real medium, not a fake PDF wrapper
- if a snapshot is in the loop: every field the agent needs must be captured, the data shape must be predictable, and `artify snapshot` must return it without ceremony

## Final Note

Prefer the browser-native answer.

If a request sounds like "make a file," ask what the file should actually do. If it sounds like "ask the user twenty questions," ask whether the user could answer them all at once on a page you snapshot.

Very often, the right answer is not another static document — and it is not a long CLI interview either. Build the page, let the user interact with it, snapshot it.
