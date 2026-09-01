# Libraries Cheatsheet

Use this file only when choosing a library or CDN.

Prefer the smallest tool that cleanly solves the request.
Do not add a framework just because frameworks exist.

## Quick Picks

| Need                                       | Pick                       |
| ------------------------------------------ | -------------------------- |
| Flows, sequences, ERDs, state diagrams     | Mermaid                    |
| Mind maps from markdown                    | Markmap                    |
| Clustered system graphs, trees, DOT syntax | Graphviz                   |
| Polished slide deck                        | Reveal.js                  |
| Lightweight custom slideshow               | Vanilla slideshow starter  |
| Custom charts and animated data viz        | D3                         |
| Simple charts fast                         | Chart.js                   |
| Multi-chart dashboard                      | Chart.js dashboard starter |
| Geo visualization                          | Leaflet                    |
| Relationship / network graph               | Cytoscape                  |
| Tool, calculator, reactive form            | Alpine.js                  |
| Small component app                        | Preact                     |
| Interactive canvas / whiteboard            | Fabric.js                  |
| CSV parsing                                | PapaParse                  |
| Interactive table editing                  | Tabulator                  |
| Markdown rendering                         | marked.js                  |
| Code highlighting                          | highlight.js               |
| Math rendering                             | KaTeX                      |
| 3D scene                                   | Three.js                   |
| Creative coding sketch                     | p5.js                      |

## Libraries

| Library          | Use for                            | CDN                                                                        |
| ---------------- | ---------------------------------- | -------------------------------------------------------------------------- |
| Tailwind CSS     | Utility-first styling              | `https://cdn.tailwindcss.com`                                              |
| Alpine.js        | Lightweight reactivity             | `https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js`                  |
| Preact           | Small component-based apps         | `https://cdn.jsdelivr.net/npm/preact@10/dist/preact.umd.js`                |
| marked.js        | Markdown to HTML                   | `https://cdn.jsdelivr.net/npm/marked/marked.min.js`                        |
| Fabric.js        | Interactive canvas and whiteboards | `https://cdn.jsdelivr.net/npm/fabric@6/dist/fabric.min.js`                 |
| Cytoscape.js     | Network and node-link diagrams     | `https://cdn.jsdelivr.net/npm/cytoscape@3/dist/cytoscape.min.js`           |
| Tabulator        | Interactive data tables            | `https://cdn.jsdelivr.net/npm/tabulator-tables@6/dist/js/tabulator.min.js` |
| PapaParse        | CSV parsing                        | `https://cdn.jsdelivr.net/npm/papaparse@5/papaparse.min.js`                |
| Mermaid          | Diagram rendering                  | `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js`              |
| Markmap          | Markdown mind maps                 | `https://cdn.jsdelivr.net/npm/markmap-autoloader@latest`                   |
| Viz.js           | Graphviz in browser                | `https://cdn.jsdelivr.net/npm/@viz-js/viz@3.25.0/+esm`                     |
| Chart.js         | Simple charts                      | `https://cdn.jsdelivr.net/npm/chart.js`                                    |
| D3               | Custom data visualization          | `https://cdn.jsdelivr.net/npm/d3@7`                                        |
| Leaflet CSS      | Map styles                         | `https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet.css`                  |
| Leaflet JS       | Interactive maps                   | `https://cdn.jsdelivr.net/npm/leaflet@1/dist/leaflet.js`                   |
| Plotly           | Scientific / heavier charting      | `https://cdn.plot.ly/plotly-latest.min.js`                                 |
| Three.js         | 3D rendering                       | `https://cdn.jsdelivr.net/npm/three@0.160/build/three.min.js`              |
| p5.js            | Creative coding                    | `https://cdn.jsdelivr.net/npm/p5@1/lib/p5.min.js`                          |
| Reveal.js CSS    | Deck framework styles              | `https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css`             |
| Reveal.js Theme  | Deck theme                         | `https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css`        |
| Reveal.js JS     | Deck framework                     | `https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js`              |
| highlight.js CSS | Syntax theme                       | `https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github-dark.min.css`  |
| highlight.js JS  | Syntax highlighting                | `https://cdn.jsdelivr.net/npm/highlight.js@11/highlight.min.js`            |
| KaTeX CSS        | Math styles                        | `https://cdn.jsdelivr.net/npm/katex@0/dist/katex.min.css`                  |
| KaTeX JS         | Math rendering                     | `https://cdn.jsdelivr.net/npm/katex@0/dist/katex.min.js`                   |

## Selection Notes

- use Mermaid when the user already thinks in diagram syntax
- use Graphviz when layout control and clustered structure matter more than animation
- use D3 when interaction is custom or the chart is not a standard chart type
- use Chart.js when speed matters more than full custom control
- use Alpine for reactive documents and tools that do not need a component framework
- use Preact only when the UI is genuinely component-shaped
- use Tabulator when the table is a real interactive grid, not just a pretty table
- use Reveal.js when the artifact is deck-first
- use a hybrid brief starter when the same content must read well and present well

## Sanity Rules

- do not stack multiple heavy libraries unless they clearly add value
- prefer one rendering system per artifact when possible
- keep CDN usage minimal and explicit
- if vanilla HTML/CSS/JS is enough, use it
