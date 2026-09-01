# Reveal.js Browser Guide

Zero-compile presentation framework. One HTML file, no Node, no bundlers, no build step. Use this when the user wants to create slides, presentations, or decks rendered in the browser.

**Read `references/slides-design-principles.md` before generating any deck.** Design principles apply before technical execution.

---

## CDN Setup

Paste these into `<head>` — that's the entire install:

```html
<!-- Stylesheet (required) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">

<!-- Theme (swap "black" for any name below) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css">

<!-- Script, just before </body> -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
<script>Reveal.initialize({ hash: true });</script>
```

**Built-in themes:** `black` · `white` · `league` · `beige` · `sky` · `night` · `serif` · `simple` · `solarized` · `moon` · `dracula`

---

## Slide Structure

Every slide is a `<section>` inside `.reveal > .slides`. Nest sections for vertical stacks.

```html
<div class="reveal">
  <div class="slides">

    <!-- Horizontal slide -->
    <section>
      <h2>Slide title</h2>
      <p>Content here</p>
    </section>

    <!-- Vertical stack (press ↓ to descend) -->
    <section>
      <section><h2>Parent</h2></section>
      <section><h2>Child 1</h2></section>
      <section><h2>Child 2</h2></section>
    </section>

  </div>
</div>
```

---

## Initialization Options

```js
Reveal.initialize({
  hash:            true,       // slide number in URL → shareable links
  transition:      "fade",     // none | fade | slide | convex | concave | zoom
  transitionSpeed: "default",  // default | fast | slow
  controls:        true,       // arrow UI in corner
  progress:        true,       // progress bar at bottom
  slideNumber:     true,       // show slide number
  center:          false,      // vertical-center content (disable for long slides)
  width:           1100,       // design width in px
  height:          650,        // design height in px
  margin:          0.04,       // slide edge margin (fraction)
  autoAnimate:     true,       // auto-animate matching elements across slides
});
```

---

## Fragments — Reveal One Item at a Time

Add `class="fragment"` to any element to make it appear on its own keypress.

```html
<ul>
  <li class="fragment">First point</li>
  <li class="fragment">Second point</li>
  <li class="fragment">Third point</li>
</ul>

<!-- Fragment styles -->
<p class="fragment fade-in">Fades in</p>
<p class="fragment fade-up">Rises up while fading in</p>
<p class="fragment highlight-red">Highlights red when reached</p>
<p class="fragment strike">Struck through when reached</p>
```

---

## Speaker Notes

Add `<aside class="notes">` inside any slide. Press **S** to open the speaker view — it shows current slide, next slide, notes, and a timer.

```html
<section>
  <h2>Revenue Q4</h2>
  <aside class="notes">
    Mention that Q4 spike was driven by the holiday campaign.
    Audience will likely ask about CAC — prepared on next slide.
  </aside>
</section>
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `→` / `↓` / `Space` | Next slide |
| `←` / `↑` | Previous slide |
| `F` | Fullscreen |
| `S` | Speaker view |
| `O` | Slide overview grid |
| `B` | Blackout screen |
| `Esc` | Exit overview / fullscreen |
| `?` | Show all shortcuts |

---

## Auto-Animate

Add `data-auto-animate` to two consecutive slides and Reveal will smoothly tween any elements that share a `data-id`. No JS required.

```html
<!-- Slide A -->
<section data-auto-animate>
  <h2 data-id="title">Before</h2>
  <p data-id="sub" style="font-size:1em">Small text</p>
</section>

<!-- Slide B — Reveal tweens both elements between states -->
<section data-auto-animate>
  <h2 data-id="title" style="font-size:3em;color:#22c55e">After</h2>
  <p data-id="sub" style="font-size:0.6em;opacity:0.4">Small text</p>
</section>
```

---

## Backgrounds

```html
<!-- Solid color -->
<section data-background-color="#1a1a2e">...</section>

<!-- Image -->
<section data-background-image="photo.jpg"
         data-background-size="cover"
         data-background-opacity="0.4">
  <h2>Text over dimmed image</h2>
</section>

<!-- Gradient -->
<section data-background-gradient="linear-gradient(135deg,#0f0c29,#302b63,#24243e)">
  <h2>Gradient slide</h2>
</section>

<!-- Looping video -->
<section data-background-video="loop.mp4"
         data-background-video-loop="true"
         data-background-video-muted="true">
</section>
```

---

## Exporting to PDF

Add the print stylesheet, open in **Chrome** with `?print-pdf` in the URL, then File → Print → Save as PDF.

```html
<!-- Add after the reveal.js script tag -->
<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/print/pdf.css"
  media="print">

<!-- Open: your-file.html?print-pdf in Chrome -->
<!-- File → Print → Destination: Save as PDF   -->
<!-- Margins: None  |  Background graphics: ✓  -->
```

> **Always use Chrome for PDF export.** Firefox and Safari do not correctly apply Reveal's print stylesheet.

### PDF Export Button (optional)

```html
<button onclick="exportPDF()" style="position:fixed;bottom:1rem;right:1rem;z-index:9999">
  Export PDF
</button>

<script>
function exportPDF() {
  const url = new URL(window.location.href);
  url.searchParams.set("print-pdf", "");
  const win = window.open(url.toString(), "_blank");
  win.onload = () => setTimeout(() => win.print(), 1200);
}
</script>
```

---

## Embedding D3 Charts in Slides

Reveal.js and D3.js work together in a single HTML file. Three rules govern the integration.

### Rule 1 — Load D3 before Reveal.js

```html
<!-- D3 first, Reveal second -->
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
```

### Rule 2 — Draw charts inside `Reveal.on("ready", ...)`

SVG elements inside hidden slides have no dimensions until Reveal has run layout. The `ready` event fires once that's done.

```js
Reveal.initialize({ hash: true, transition: "fade", width: 1100, height: 650 });

Reveal.on("ready", () => {
  drawBarChart();
  drawLineChart();
});
```

### Rule 3 — Use `viewBox` for responsive charts

Reveal scales slides with CSS transforms. A fixed-width SVG won't scale with the slide — use `viewBox + width="100%"` instead.

```js
const svg = d3.select("#chart")
  .attr("viewBox", `0 0 ${W} ${H}`)
  .attr("width", "100%");
```

### Animate Charts on Slide Enter

```js
Reveal.on("slidechanged", event => {
  // Fire D3 transition when slide index 1 becomes active
  if (event.indexh === 1) {
    d3.selectAll("#bar-chart rect")
      .transition()
      .duration(700)
      .delay((d, i) => i * 80)
      .ease(d3.easeCubicOut)
      .attr("y", d => y(d.value))
      .attr("height", d => h - y(d.value));
  }
});
```

### Animate on Fragment Show

```js
Reveal.on("fragmentshown", event => {
  // event.fragment is the DOM element that just appeared
  const target = event.fragment.getAttribute("data-chart");
  if (target === "bar") drawBarChart();
});
```

### Prevent Variable Collisions

Multiple charts share variable names (`x`, `y`, `g`, `svg`). Wrap each one in an IIFE:

```js
// Chart 1
(function barChart() {
  const svg = d3.select("#bar-chart");
  const x = d3.scaleBand()...
  const y = d3.scaleLinear()...
})();

// Chart 2 — its own x, y, svg — no conflicts
(function lineChart() {
  const svg = d3.select("#line-chart");
  const x = d3.scaleTime()...
  const y = d3.scaleLinear()...
})();
```

---

## Full Boilerplate (Reveal + D3)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My Deck</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/print/pdf.css" media="print">
</head>
<body>

  <div class="reveal">
    <div class="slides">
      <section><h1>Title Slide</h1></section>
      <section>
        <h2>Monthly Data</h2>
        <svg id="bar-chart"></svg>
      </section>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script>
    Reveal.initialize({ hash: true, transition: "fade", width: 1100, height: 650 });

    Reveal.on("ready", () => { drawBarChart(); });

    function drawBarChart() { /* D3 code here */ }
  </script>

</body>
</html>
```

---

## Quick Reference

| What you want | How |
|---------------|-----|
| New slide | Add a `<section>` inside `.slides` |
| Vertical sub-slide | Nest `<section>` inside `<section>` |
| Animate in | `class="fragment"` on any element |
| Speaker notes | `<aside class="notes">text</aside>` |
| Auto-tween between slides | `data-auto-animate` on both + `data-id` on elements |
| Full-bleed image bg | `data-background-image="url" data-background-size="cover"` |
| Per-slide color | `data-background-color="#hex"` on the section |
| Export PDF | Append `?print-pdf` to URL → Chrome print dialog |
| Presenter mode | Press `S` |
| Overview grid | Press `O` |
| Embed D3 chart | `<svg id="chart"></svg>` in slide, draw in `Reveal.on("ready")` |
| Animate chart on enter | `Reveal.on("slidechanged")` + check `event.indexh` |
| Prevent name collisions | Wrap each chart in `(function name() { ... })()` |
