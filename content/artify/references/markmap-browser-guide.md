# Markmap Browser Guide

Use this guide when the user wants a Markdown-first mind map that opens in the browser.

This file turns the field manual into a Markdown reference plus template training so the skill can generate, explain, and render Markmap outputs directly.

## 1. What Markmap Is

Markmap turns a Markdown outline into an interactive browser-rendered mind map.

Mental model:

- source: Markdown outline
- renderer: small browser script
- result: pan-and-zoom SVG mind map

Use Markmap when the source begins as notes, prose, headings, summaries, or a structured document.

## 2. Easiest Workflow

1. Start from a document, notes page, transcript, or generated summary.
2. Convert it into a nested Markdown outline.
3. Put that outline into a Markmap HTML template.
4. Open the HTML file in the browser.

That is the whole pipeline.

## 3. Syntax You Actually Need

You do not need a custom graph language. Write normal Markdown with good structure.

### Headings create the main hierarchy

```md
# Product Launch
## Goals
## Audience
## Risks
```

### Nested bullets create child branches

```md
# Product Launch
## Goals
- Validate the concept
- Get first 100 beta users
  - Designers
  - Product managers
- Reduce onboarding friction
```

### Keep labels short

Good:

```md
# User Onboarding
## Goals
- Faster signup
- First success in 3 minutes
```

Bad:

```md
# User onboarding should be designed in such a way that the average first-time user can understand every single feature without reading external documentation
```

### Useful Markdown that works well

- `**bold**` for emphasis
- `*italic*` for lighter emphasis
- `` `inline code` `` for terms and commands
- `[links](https://example.com)` for references
- `- [x]` and `- [ ]` when task state helps

## 4. A Good Markmap Example

```md
---
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 2
  maxWidth: 260
---

# Research Project
## Purpose
- Understand the market
- Find unmet needs
## Users
- Small teams
- Agencies
- Operations leads
## Opportunities
- Faster reporting
- Lower setup cost
- Better visibility
## Risks
- Weak source data
- Feature sprawl
- Slow adoption
```

## 5. Frontmatter Options That Matter

| Option | What it does | Good starting value |
|---|---|---|
| `colorFreezeLevel` | Keeps branch colors stable past a depth | `2` |
| `initialExpandLevel` | Controls how much is open on load | `2` or `3` |
| `maxWidth` | Wraps long labels | `220` to `320` |
| `duration` | Changes fold animation speed | `300` to `600` |
| `zoom` | Enables zooming | `true` |
| `pan` | Enables panning | `true` |
| `spacingHorizontal` | Changes horizontal spacing | `80` to `100` |
| `spacingVertical` | Changes sibling spacing | `5` to `12` |
| `lineWidth` | Adjusts branch stroke width | `1.5` to `2.5` |

Example:

```md
---
markmap:
  colorFreezeLevel: 2
  initialExpandLevel: 2
  maxWidth: 260
  spacingHorizontal: 100
  spacingVertical: 8
  lineWidth: 2
---
```

## 6. Folding Nodes

Use Markmap magic comments to collapse parts of the map on load.

```md
# Plan
## Research <!-- markmap: fold -->
- Market scan
- Interviews

## Delivery <!-- markmap: foldAll -->
- Sprint 1
  - Setup
  - Core features
- Sprint 2
  - Testing
  - Launch
```

- `fold` collapses the current node
- `foldAll` collapses the current node and descendants

## 7. Transformation Recipe

When converting a long document into Markmap-ready Markdown:

1. Set the document title as the single `#` root heading.
2. Convert major sections into `##` headings.
3. Convert section highlights into bullets.
4. Convert details or evidence into nested bullets.
5. Trim sentence-heavy text into signpost-like labels.

Good output shape:

```md
# Contract Summary
## Parties
- Vendor
- Client
## Timeline
- Kickoff: April
- Delivery: June
## Risks
- Scope drift
- Approval delays
## Actions
- Confirm budget
- Finalize milestones
```

## 8. Browser Rendering Paths

### Option A: Markmap Editor Workspace

Use `templates/markmap.html` when the user wants a ready-to-edit browser page.

Replace:

- `{{TITLE}}`
- `{{DESCRIPTION}}`
- `{{INITIAL_MARKDOWN}}`

This template gives you:

- a left-side Markdown editor
- a render button
- a sample loader
- a clear-and-reset flow
- a browser-rendered map on the right

Best for interactive refinement.

### Option B: Minimal Markmap Viewer

Use `templates/markmap-minimal.html` when you want one small file that opens straight into a map.

Replace:

- `{{TITLE}}`
- `{{INITIAL_MARKDOWN}}`

Best for one-shot output.

## 9. Starter Files

Use these when you want a fast Markmap structure without inventing the outline from scratch:

| File | Use for |
|---|---|
| `starters/markmap/meeting-notes.md` | Meeting outputs |
| `starters/markmap/research-brief.md` | Research findings |
| `starters/markmap/document-summary.md` | Reports and long documents |
| `starters/markmap/product-roadmap.md` | Roadmaps and phased plans |
| `starters/markmap/topic-breakdown.md` | General concept overviews |

Workflow:

1. Pick the closest starter.
2. Replace headings and bullets with the real content.
3. Trim long labels.
4. Render in `templates/markmap.html` or `templates/markmap-minimal.html`.

## 10. Minimal Browser Template Example

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>My Markmap</title>
  <style>
    body { margin: 0; font-family: system-ui, sans-serif; }
    .markmap { height: 100vh; }
    .markmap > svg { width: 100%; height: 100%; }
  </style>
  <script>
    window.markmap = { autoLoader: { toolbar: true } };
  </script>
  <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@latest"></script>
</head>
<body>
  <div class="markmap">
    <script type="text/template">
---
markmap:
  initialExpandLevel: 2
  maxWidth: 240
---

# My Topic
## Branch A
- Item 1
- Item 2
## Branch B
- Item 3
- Item 4
    </script>
  </div>
</body>
</html>
```

## 11. Template Training Notes

### For `templates/markmap.html`

- Put starter Markdown into `{{INITIAL_MARKDOWN}}`
- Keep it outline-shaped, not paragraph-shaped
- Use `{{DESCRIPTION}}` to explain the purpose of the workspace
- Escape `</script>` if you inject directly into a template script block

Example replacement:

```python
render_template('markmap.html', {
    'TITLE': 'Research Map',
    'DESCRIPTION': 'Paste Markdown on the left, then render the map.',
    'INITIAL_MARKDOWN': '''# Research Map
## Goals
- Validate need
- Interview users
## Risks
- Weak signal
- Scope drift'''
})
```

### For `templates/markmap-minimal.html`

- Put complete Markdown into `{{INITIAL_MARKDOWN}}`
- Use this when the user wants a clean single-file map without the editing panel

## 12. Best Practices

- Use one root heading only
- Prefer structure over prose
- Keep labels compact
- Limit depth to 3 or 4 levels
- Group by meaning, not by sentence order
- Split crowded maps into multiple focused maps

## 13. Common Problems and Fixes

| Problem | Likely cause | Fix |
|---|---|---|
| Nothing renders | CDN failed or content is not inside the Markmap container | Check script URL and placement |
| Map is tiny or invisible | SVG has no height | Set container height and make SVG fill it |
| Map is too wide | Labels are too long | Shorten labels and use `maxWidth` |
| Map is too busy | Too many nodes open at once | Lower `initialExpandLevel` or use fold comments |
| Raw HTML breaks the page | Browser parsed content before Markmap | Put Markdown inside `script type="text/template"` |

## 14. Rapid Repair

If a Markmap render feels wrong, try these in order:

1. Reduce the source to one root, a few `##` branches, and short bullets.
2. Switch to the closest file in `starters/markmap/`.
3. Cut sentence-like labels into noun phrases.
4. Lower `initialExpandLevel` if the map opens too busy.
5. Move to `templates/markmap.html` if the user wants to edit live.

## 15. Copy-Paste Prompts

### Turn a document into Markmap-ready Markdown

```text
Turn the following document into Markmap-ready Markdown.
Rules:
- Use exactly one # root heading.
- Use ## for major branches.
- Use bullets for subpoints.
- Keep node labels short, clear, and scannable.
- Prefer 3 to 4 levels maximum.
- Avoid long sentences.
- Return Markdown only.
```

### Compress a messy map

```text
Rewrite this Markmap Markdown to make it cleaner.
Rules:
- Shorten long labels.
- Merge repetitive siblings.
- Keep the same meaning.
- Reduce visual clutter.
- Return Markdown only.
```

## 16. Final Checklist

- The map uses one root heading.
- Headings and bullets form a real outline.
- Labels are short.
- Frontmatter is reasonable.
- The chosen template matches the user's need: editor or minimal viewer.
