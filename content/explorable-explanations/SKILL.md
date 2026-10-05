---
name: explorable-explanations
description: Embed tiny interactive widgets inside prose: sliders, drags, live models.
version: 1
---

# Explorable Explanations

Build **embeddable** interactive widgets — just code pasted inside a document,
not a separate file artifact. Artify makes complete pages. This makes the
little living diagrams *inside* the prose.

An explorable = a visible model + a way to touch it + instant feedback.
Reader changes a parameter, the picture answers back in <100ms.

## Ask for level first

Never guess the ambition. Ask with the `question` tool (or one short line):

1. **L1 demo** — show the graphic itself. Static-but-alive visual, no controls.
   For "just show me what it looks like."
2. **L2 interactive** — a couple of controls that behave. 1–2 sliders / drags /
   toggles wired to a live view. For "let me feel how it works."
3. **L3 quest** — must interact to solve. Predict → try → reveal, stepped
   challenge, win state. For "make me *get* it."

Default to L2 if they won't pick. L1 is a diagram, L2 is a toy, L3 is a game.

## Embed contract (just code, independent, universal)

Output a single paste block: custom element + Shadow DOM + zero-dep vanilla JS.
Why: Shadow DOM scopes CSS so the widget neither leaks nor gets wrecked by the
host page, flows inline with text (no iframe scroll-jail), params come in as
attributes, and it degrades to static fallback where JS is stripped.

Always follow this shape:

```html
<explorable-name param="default">
  <!-- static fallback for no-JS hosts: the takeaway in one sentence + numbers -->
  <p>Fallback: what this shows even with no JS.</p>
</explorable-name>
<script>
(() => {
  if (customElements.get('explorable-name')) return;
  customElements.define('explorable-name', class extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
      // read attrs as params, render <style> + controls + SVG/canvas into shadowRoot
      // wire input -> model -> view synchronously, update on 'input' not 'change'
    }
  });
})();
</script>
```

Rules:

- One paste block only. No external file, no build step, no global CSS/JS.
- `<style>` lives *inside* `shadowRoot`. Start with `:host{display:block;contain:content}`.
- Idempotent guard (`customElements.get` check) — pasting twice must not throw.
- Params as attributes (`rate="7"`), so authors tweak without touching JS.
- Vanilla + inline SVG/canvas first. CDN libs only if the model truly needs them.
- Every control updates on `input` event. If feedback lags, the intuition dies.
- Fallback slot content must still teach the point with JS off.

For dev preview only, paste the snippet into a throwaway artify page and
`artify serve` it. Ship the snippet, not the page.

## How-to: Brilliant-for-visualize principles

Distilled from Brilliant's learn-by-doing house style. Apply every time:

1. **Doing, not reading.** Never explain then show. Show a thing the reader can
   push, then name what just happened. Intuition first, vocabulary second.
2. **Feel the math.** Map the abstract variable to a bodily action: drag the
   weight, scrub time, stretch the curve. One gesture = one variable.
3. **One idea per widget.** If you need two paragraphs to explain the controls,
   split the widget. Brilliant wins on bite-sized, not dashboards.
4. **Predict then reveal.** Before the sim answers, make the reader commit:
   "where will it land?" Then play. Surprise is the glue.
5. **Instant, kind feedback.** Correct → green + celebration micro-motion.
   Wrong → show *why* visually, never just "incorrect." Explanation itself gets
   an interactive re-try, not a text dump.
6. **Ramp + edge cases.** Easy default params that always look good, then let
   them break it: 0, max, negative. Mastery lives at the edges.
7. **Break it down.** Complex system = chain of 2–3 tiny widgets, each owning
   one sub-model, composed in reading order. Never one mega-widget.

## Core examples (in refs/)

Full copy-paste blocks live in `references/examples.md` — read it when building.
Pick 1, adapt the model, keep the contract:

1. **Slider-parameter** (L2 default) — one slider = one variable.
2. **Drag-direct** (L2) — grab the thing, `touch-action:none`, ≥44px target.
3. **Stepper / scrubber** (L1→L2) — `model.at(t)` + `t = k/N` label + Play.
4. **Predict-reveal** (L3 atom) — guess → lock → animate truth → diff.
5. **Sandbox playbox** (L2→L3 closer) — Reset + `0` / `max` preset buttons.
6. **Prose-linked mini** (L1 glue) — `<span data-hl>` ↔ visual, max one per section.

## Workflow

1. Ask level (L1 / L2 / L3). Confirm topic + the single mental model in one line.
2. Pick 1 pattern from `references/examples.md` (compose max 3 for L3 quests).
3. Emit one paste block per widget following the embed contract.
4. State where to paste it ("after paragraph 2") + default params to try first.
5. Never emit a separate `.html` file as the deliverable — the snippet IS the deliverable.
