# Infographic & Visualization Design Principles

Principles for creating effective visualizations — charts, diagrams, mindmaps, infographics, tables, timelines, and all visual representations. Drawn from Universal Principles of Design. Use these when generating any visualization output.

---

## The Core Mindset

**The user is a prediction machine with limited attention. Design that aligns with the brain's predictive models reduces friction; design that forces new logic creates resistance.**

A visualization is not a data dump. It is a *translation* — from abstract information into something the human visual system can process in seconds. The goal is not to show everything, but to show the *right thing* so the viewer reaches the correct conclusion without effort.

---

## 0. Audience & Purpose — Ask Before You Design

Before choosing a chart type or layout, answer two questions. They change everything.

### Who is this for?

| Audience | What they need | Design direction |
|---|---|---|
| **Yourself** (personal notes, thinking aid) | Density, completeness, raw structure. You'll re-read it. | More detail is fine. Labels can be shorthand. Ugly is acceptable. Prioritize information over polish. |
| **A peer / technical audience** | Correctness, precision, ability to drill into detail. They share your context. | Moderate simplification. Show the full picture but organize it well. Annotations and caveats matter. |
| **A non-technical audience** | The conclusion, fast. They don't share your context. | Aggressive simplification. One idea per view. Explain jargon. Lead with the "so what." |
| **Stakeholders / decision-makers** | The implication for *their* decision. They care about risk, opportunity, timeline. | Frame around their decision, not your analysis. Highlight trade-offs. Use comparison formats. |
| **A general / public audience** | Emotional resonance and memorability. They'll remember one thing. | Maximum subtraction. Story over data. One powerful visual. Bold headline. |

**The rule**: The less shared context you have with the viewer, the more you must simplify, annotate, and frame. Complexity is a privilege of shared expertise.

### What is the purpose?

| Purpose | Goal | Design approach |
|---|---|---|
| **Understanding** (for yourself or peers) | Accurate representation. Let the data speak. | Neutral framing. Show full context. Let the viewer draw conclusions. |
| **Persuasion** (for stakeholders) | Move toward a decision or action. | Frame around the decision. Highlight the key evidence. Use comparison. |
| **Communication** (for general audience) | Make something understood and remembered. | Simplify aggressively. Use story and metaphor. One takeaway per view. |
| **Manipulation** (ethical boundary) | Distort to produce a predetermined conclusion. | **Do not do this.** Cherry-picked data, misleading axes, and omitted context are lies, not design. |

**The ethical line**: Framing is not manipulation. Choosing what to emphasize is design. Choosing what to *hide* to mislead is deception. If removing a data point changes the conclusion, and you remove it anyway, you are lying with a chart.

---

## 1. Cognitive Economy

The brain is a pattern matcher optimized for efficiency, not omniscience. Respect its limits.

### Working Memory: 4±1 Items

- Never display more than 5±2 distinct elements, groups, or data series at once.
- If you have more, use progressive disclosure (expand on interaction) or split into multiple views.
- **Chunk related items** using proximity, color, or enclosure so they count as one unit.

### Processing Channels

- **Visual processing is faster than textual processing.** Prefer icons, shapes, and spatial relationships over labels wherever possible.
- **Visual memory outperforms text after 30 seconds.** If the viewer needs to remember the insight, make it visual.
- **Vertical and horizontal axes process faster than oblique angles.** Avoid tilted elements unless they serve a specific purpose (e.g., diagonal trend lines).

### Signal-to-Noise Ratio

- Every element that does not convey information is noise. Remove it.
- Gridlines, borders, backgrounds, legends, axis labels — each must earn its place.
- **The test**: Remove the element. Does the viewer still reach the same conclusion? If yes, it's noise.

**Do:**
- Minimal gridlines (light gray, or remove entirely)
- Direct labels instead of legends where possible
- Muted backgrounds; let data dominate

**Don't:**
- 3D charts (they distort perception and add noise)
- Decorative gradients, shadows, or textures on data elements
- Dual y-axes (they create false correlations)

---

## 2. Visual Hierarchy

Guide the viewer's eye through importance. The most important information should be seen first.

### Hierarchy Tools

| Tool | How it works | Use for |
|---|---|---|
| **Size** | Larger = more important | Headlines, key data points |
| **Color/Contrast** | High contrast draws the eye first | Highlighting the "so what" |
| **Position** | Top-left is seen first (Western reading); center is second | Primary insight placement |
| **Whitespace** | Isolation signals importance | Separating key data from context |
| **Weight** | Bold/heavy text vs. light | Labels vs. annotations |

### The Inverted Pyramid for Visuals

1. **Lead with the conclusion** — title should state the insight, not the topic
   - Bad: "Monthly Revenue 2024"
   - Good: "Revenue grew 23% in Q4, driven by APAC expansion"
2. **Support with the visual** — the chart proves the headline
3. **Context in annotations** — footnotes, caveats, data source at the bottom

### Serial Position Effect — Front-Load Everything

The brain does not pay equal attention throughout a sequence. It weights the **beginning** and the **end** higher than the middle. Attention also fatigues over time — by the time a viewer reaches the bottom of a dashboard or the end of a legend, they are processing with less care.

**Practical rules:**

- **First item in a list, legend, or bar chart gets the most attention.** Put your most important category first, not alphabetically.
- **Last item gets secondary attention.** If you have two key points, put one first and one last.
- **Middle items are invisible.** If something important is in the middle of a sequence, move it to an edge.
- **Dashboards: top-left is prime real estate.** Most important metric goes there. Bottom-right is the weakest position.
- **Long visualizations fatigue the viewer.** If a chart has >12 bars or a table has >15 rows, the viewer is skimming by the end. Front-load the key data; push secondary data down or into an appendix.

This applies to: bar chart ordering, legend ordering, dashboard card placement, table row ordering, list ordering, and the sequence of slides in a deck.

---

## 3. Gestalt Principles — How the Brain Groups

Use these to make relationships visible without explicit labeling.

| Principle | What it means | Application |
|---|---|---|
| **Proximity** | Things close together are perceived as a group | Cluster related data points; separate unrelated sections with whitespace |
| **Similarity** | Things that look alike are perceived as related | Same color for same category; same shape for same type |
| **Enclosure** | Things inside a boundary are perceived as a group | Boxes, backgrounds, or borders around related content |
| **Continuity** | The eye follows smooth paths | Align elements on a grid; use consistent spacing |
| **Closure** | The brain completes incomplete shapes | Use implied boundaries; don't over-outline |
| **Figure/Ground** | The brain separates foreground from background | Ensure data "pops" against background; avoid ambiguous layering |

**Rule of thumb**: If you need to add explicit labels or connectors to show a relationship, the visual grouping has failed. Fix the layout first.

---

## 4. Color — Use With Discipline

Color is the most abused tool in visualization. Use it sparingly and intentionally.

### Color Roles

| Role | Purpose | Rules |
|---|---|---|
| **Categorical** | Distinguish between groups | Max 6-7 colors; use a qualitative palette |
| **Sequential** | Show magnitude (low → high) | Single hue, light to dark; or two-hue gradient |
| **Diverging** | Show deviation from a center point | Two hues diverging from a neutral midpoint |
| **Highlight** | Draw attention to one element | One accent color against a neutral background |

### Rules

- **Default to a neutral background** (white or very light gray). Let data carry the color.
- **Never use rainbow colormaps.** They are perceptually non-uniform and misleading. Use sequential or diverging palettes.
- **Limit to 5-7 colors max** in a single visualization. Beyond that, the eye can't distinguish.
- **Consider colorblindness**: ~8% of men have red-green deficiency. Use blue/orange instead of red/green. Test with a simulator.
- **Consistency across views**: If "revenue" is blue in one chart, it must be blue in all charts.

### The Universal Color Myth

- Red does not always mean "danger" and blue does not always mean "trust." Color symbolism is culturally contingent.
- Focus on **contrast and consistency** within your visualization rather than assumed universal meanings.

---

## 5. Choosing the Right Visualization

The form must match the question the viewer is asking.

### Decision Matrix

| Question the viewer has | Best visualization | Why |
|---|---|---|
| **How do parts relate to a whole?** | Pie chart (≤5 slices), stacked bar, treemap | Proportion is the message |
| **How does something change over time?** | Line chart, area chart, timeline | Trends and patterns emerge on a time axis |
| **How do items compare?** | Bar chart (horizontal or vertical), dot plot | Length comparison is the most accurate visual encoding |
| **What is the distribution?** | Histogram, box plot, violin plot | Shows shape, spread, outliers |
| **What is the relationship between variables?** | Scatter plot, bubble chart | Correlation and clustering visible |
| **How does something flow or connect?** | Sankey, flowchart, network graph | Flow and connection are the message |
| **What is the structure of a system?** | Architecture diagram, component diagram | Hierarchy and dependency |
| **What is the sequence of events?** | Timeline, Gantt chart, sequence diagram | Temporal ordering |
| **How do concepts relate hierarchically?** | Mindmap, tree diagram, org chart | Hierarchy and branching |
| **What are the key facts at a glance?** | Stat cards, KPI dashboard, table | Numbers are the message |

### Anti-Patterns in Chart Selection

| Trap | Why it fails | Fix |
|---|---|---|
| **Pie chart with >5 slices** | Humans can't compare angles accurately | Use horizontal bar chart |
| **3D bar/pie chart** | Distorts proportions; adds visual noise | Use 2D always |
| **Dual y-axes** | Implies correlation that may not exist | Split into two charts or normalize |
| **Stacked area with many layers** | Only bottom layer has a stable baseline | Use small multiples or line chart |
| **Treemap for comparison** | Area is hard to compare precisely | Use bar chart if comparison matters |
| **Network graph with >50 nodes** | Hairball; nothing is readable | Filter, cluster, or use adjacency matrix |

---

## 6. Diagrams (Mermaid, Graphviz, Flowcharts)

Diagrams show *relationships and flow*, not data values.

### Principles

- **One direction of flow**: Left-to-right or top-to-bottom. Never mix.
- **Minimize crossing lines**: If lines cross, the layout is wrong. Rearrange nodes.
- **Consistent node shapes**: Same shape = same type of thing. Diamond = decision. Rectangle = process. Oval = start/end.
- **Short labels**: 2-5 words per node. If you need a paragraph, it's not a node — it's a footnote.
- **Color for grouping, not decoration**: Use color to show categories (e.g., "frontend" = blue, "backend" = green), not for visual variety.

### Flowchart Rules

- Every flowchart has exactly one start and one end (or clearly marked multiple ends).
- Decision nodes (diamonds) must have exactly two outgoing paths labeled Yes/No or similar.
- Avoid feedback loops unless they are the point. If a loop exists, make it visually obvious.

### Architecture Diagrams

- **Layer by abstraction**: High-level at the top, infrastructure at the bottom (or left-to-right).
- **Show boundaries**: Group related components in boxes with labels (e.g., "Auth Service", "Data Layer").
- **Label connections**: Arrows should have labels describing what flows (data, events, requests).
- **Hide implementation details**: An architecture diagram is a map, not a wiring diagram. Show the *what*, not the *how*.

---

## 7. Mindmaps & Concept Maps (Markmap)

Mindmaps show *hierarchical relationships between ideas*, not data.

### Principles

- **One root concept**: Everything branches from a single central idea.
- **Short labels**: 1-5 words per node. Mindmaps scan, they don't read.
- **Limit depth**: 3-4 levels maximum. Beyond that, use a separate mindmap for the deep branch.
- **Balance branches**: If one branch has 15 children and another has 2, the map is unbalanced. Consolidate or split.
- **Use headings as structure**: In Markmap, `#` is root, `##` is primary branch, `###` is secondary. Don't skip levels.
- **Parallel grammar**: All items at the same level should use the same grammatical structure (all nouns, all verb phrases, etc.).

### When to Use Mindmaps vs. Other Formats

| Use mindmap when... | Use something else when... |
|---|---|
| Exploring a topic's structure | You need precise data comparison → bar chart |
| Brainstorming or organizing ideas | You need temporal ordering → timeline |
| Summarizing a document's hierarchy | You need to show process flow → flowchart |
| Showing how concepts relate | You need to show quantities → chart |

### Anti-Patterns

- **Prose in nodes**: If a node contains a full sentence, rewrite it as a phrase.
- **Too deep**: >4 levels becomes unreadable. Split into multiple maps.
- **Unbalanced trees**: One massive branch dwarfs others. Reorganize.
- **No visual distinction between levels**: Use size, color, or weight to show hierarchy depth.

---

## 8. Tables

Tables are for *precise value lookup*, not for pattern recognition.

### When to Use a Table

- The viewer needs exact values, not trends.
- Comparing multiple attributes across few items (≤20 rows).
- Data doesn't have a natural visual encoding (e.g., mixed types: text, numbers, dates, status).

### Design Rules

- **Align numbers right, text left.** Decimal-aligned if possible.
- **Header row must be visually distinct** (bold, background color, or border).
- **Zebra striping** (alternating row colors) helps track rows in wide tables.
- **Highlight the key row or column** — the one the viewer should focus on.
- **Sort by the most important column** by default.
- **Use badges or icons for status columns** instead of text ("Active" → green dot).

### Anti-Patterns

- Tables with >20 rows without filtering or pagination → use a chart instead.
- Merged cells → they break sorting and scanning.
- Too many columns → the viewer can't track horizontally. Reduce or paginate.

---

## 9. Timelines & Gantt Charts

Timelines show *when things happen*. Gantt charts show *when things happen and how long they take*.

### Principles

- **Time flows left-to-right** (or top-to-bottom). Never right-to-left.
- **Group by category** (color or row), not by date. The viewer scans vertically for a category, then reads horizontally for timing.
- **Mark "now"** with a vertical line or label. Always orient the viewer to the present.
- **Milestones are diamonds**, not bars. They represent a point in time, not a duration.
- **Label directly** on the bar or milestone, not in a legend. Reduce eye travel.

### Anti-Patterns

- Too many items on one timeline → filter or split into phases.
- No scale indicator → the viewer can't tell if a gap is 1 day or 1 year.
- Compressing long durations to fit → makes short tasks invisible. Use a zoomed inset.

---

## 10. Comparison & Dashboard Layouts

### Comparison (Side-by-Side)

- **Align by attribute**, not by item. The viewer compares vertically (same attribute, different items).
- **Highlight the winner** in each row (bold, color, or icon).
- **Use a summary row** at the top or bottom with an overall verdict.
- **Max 4 items side-by-side.** Beyond that, use a table or radar chart.

### Dashboards

- **Most important metric goes top-left** (first thing seen).
- **Use consistent card sizes**. Irregular grids feel chaotic.
- **Limit to 5-7 cards/widgets.** More than that and nothing stands out.
- **Sparklines over full charts** for secondary metrics. Show the trend, not the detail.
- **One interactive element per card max.** If a card needs two filters, it's too complex.

---

## 11. Typography in Visualizations

- **One font family** per visualization. Use weight (bold/regular/light) for hierarchy, not different fonts.
- **Sans-serif for labels and data** (cleaner at small sizes). Serif for long-form text only.
- **Minimum 12px for labels**. Below that, it's unreadable on screens.
- **Rotate axis labels only as a last resort.** Prefer horizontal bar charts to avoid rotated x-axis labels entirely.
- **Abbreviate consistently**: "Jan" not "January" if space is tight. But be consistent across all labels.

---

## 12. The "So What?" Test

Before finalizing any visualization, ask:

1. **What is the one insight the viewer should take away?** If you can't state it in one sentence, the visualization is unclear.
2. **Does the title state that insight?** If the title is a topic label, rewrite it as a claim.
3. **Can the viewer reach that conclusion in <5 seconds?** If not, simplify.
4. **Is every element necessary?** Remove one element. Does the insight survive? If yes, keep it removed.
5. **Would a non-expert understand this?** If not, add context or simplify.

### Framing — Same Data, Different Story

The same dataset framed differently produces different decisions. This is not a bug — it is a tool. Use it intentionally.

| Frame | Example | Effect |
|---|---|---|
| **Gain frame** (positive) | "88% of patients recovered" | Encourages action; feels safe |
| **Loss frame** (negative) | "12% of patients did not recover" | Creates urgency; triggers risk aversion |
| **Relative frame** | "2x faster than competitor" | Emphasizes advantage |
| **Absolute frame** | "Completed in 4.2 seconds" | Emphasizes precision |
| **Trend frame** | "Growing 15% quarter over quarter" | Emphasizes momentum |
| **Benchmark frame** | "Above industry average of 7%" | Emphasizes position |

**How to choose**: Match the frame to the audience's decision.

- If the viewer needs to **start** doing something → gain frame ("Here's what you'll get")
- If the viewer needs to **stop** doing something → loss frame ("Here's what you're losing")
- If the viewer needs to **choose between options** → relative or benchmark frame
- If the viewer needs to **trust the number** → absolute frame

**The ethical boundary**: Framing is choosing what to emphasize. Manipulation is choosing what to hide. If you present "88% recovery" while knowing the treatment group was pre-selected for healthy patients, you are not framing — you are deceiving. The test: *Would a reasonable person, seeing the full dataset, reach the same conclusion?* If yes, it's framing. If no, it's manipulation.

---

## Quick Decision Guide

```
Need to visualize something?
│
├── Viewer needs exact values?
│   └── → Table (with sorting, highlighting, badges)
│
├── Viewer needs to see a trend over time?
│   └── → Line chart or area chart
│
├── Viewer needs to compare quantities?
│   └── → Bar chart (horizontal if labels are long)
│
├── Viewer needs to see proportions?
│   ├── ≤5 categories → Pie chart or donut
│   └── >5 categories → Treemap or stacked bar
│
├── Viewer needs to see relationships/correlation?
│   └── → Scatter plot or bubble chart
│
├── Viewer needs to see flow or process?
│   └── → Flowchart (Mermaid) or Sankey
│
├── Viewer needs to see system structure?
│   └── → Architecture diagram (Mermaid/Graphviz)
│
├── Viewer needs to see concept hierarchy?
│   └── → Mindmap (Markmap) or tree diagram
│
├── Viewer needs to see a sequence of events?
│   └── → Timeline or Gantt chart
│
├── Viewer needs to compare options?
│   └── → Comparison table or radar chart (≤5 options)
│
└── Viewer needs a quick status overview?
    └── → Dashboard with KPI cards + sparklines
```

---

## Universal Checklist (Apply to Every Visualization)

- [ ] Title states the insight, not the topic
- [ ] Color is used intentionally (categorical, sequential, or highlight — not decorative)
- [ ] No more than 5-7 distinct visual elements or groups
- [ ] Direct labels instead of legends where possible
- [ ] No 3D effects, gradients, or shadows on data elements
- [ ] Whitespace separates logical groups
- [ ] Consistent alignment (grid-based layout)
- [ ] Text is ≥12px and readable
- [ ] Colorblind-safe palette (no red/green as sole differentiator)
- [ ] Viewer can reach the main conclusion in <5 seconds

---

## Tensions & Limits

- **Simplicity vs. Completeness**: Stripping too much can mislead. If removing context changes the conclusion, keep it. The goal is clarity, not minimalism.
- **Familiarity vs. Innovation**: Standard chart types are understood instantly. Novel visualizations require learning. Use novel forms only when standard forms genuinely can't represent the data.
- **Universal vs. Cultural**: Reading direction (left-to-right vs. right-to-left), color symbolism, and spatial metaphors vary by culture. Know your audience.
- **Static vs. Interactive**: These principles apply primarily to static visualizations. Interactive visualizations have different rules (progressive disclosure, hover states, filtering). But the foundation is the same: start simple, let the viewer drill in.
- **Emotional vs. Analytical**: These principles optimize for analytical clarity. If the goal is emotional impact (persuasion, urgency, awe), different rules apply — but signal-to-noise and cognitive load still matter.
