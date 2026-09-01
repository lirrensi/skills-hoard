# D3.js Browser Guide

Custom data visualizations in the browser using D3.js. One HTML file, no build step. Use this when the user wants charts, infographics, interactive data viz, or custom visual representations that go beyond what Mermaid or Chart.js can do.

**Read `references/infographic-design-principles.md` before generating any visualization.** Design principles apply before technical execution.

---

## CDN Setup

```html
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
```

Load D3 before any script that uses it.

---

## The Core Mental Model

D3 works in three steps, every time:

1. **Select** — grab a DOM element (or create an SVG container)
2. **Bind** — attach your data array to the selection
3. **Enter** — for each data point, create a new element and set its attributes

```js
const data = [40, 80, 60, 120, 90];

d3.select("#chart")         // 1. Select SVG container
  .selectAll("rect")        // 2. Declare what we want to create
  .data(data)               // 3. Bind data
  .enter()                  //    For each new data point...
  .append("rect")           //    ...append a <rect>
  .attr("x", (d, i) => i * 60)
  .attr("y", d => 200 - d)  // flip: SVG origin is top-left
  .attr("width", 40)
  .attr("height", d => d)
  .attr("fill", "#22c55e");
```

---

## Scales — The Most Important Concept

Scales map your data domain (raw values) to a visual range (pixels, colors). Always define scales before drawing anything.

### Linear scale — numbers → pixels

```js
const y = d3.scaleLinear()
  .domain([0, 100])   // data range
  .range([400, 0]);   // pixel range (flipped: 0 data = bottom)

y(50)  // → 200
```

### Band scale — categories → bar positions

```js
const x = d3.scaleBand()
  .domain(["Jan", "Feb", "Mar", "Apr"])
  .range([0, 600])
  .padding(0.3);

x("Feb")        // → start x of Feb bar
x.bandwidth()   // → width of each bar
```

### Time scale — dates → pixels

```js
const x = d3.scaleTime()
  .domain([new Date("2024-01-01"), new Date("2024-12-31")])
  .range([0, 600]);
```

### Color scale — values → colors

```js
const color = d3.scaleSequential()
  .domain([0, 100])
  .interpolator(d3.interpolateViridis);

color(0)    // → dark purple
color(100)  // → yellow
```

### Useful scale utilities

```js
d3.max(data, d => d.value)         // maximum value
d3.min(data, d => d.value)         // minimum value
d3.extent(data, d => d.value)      // [min, max]
d3.scaleLinear().nice()            // round domain to nice numbers
```

---

## Margins & The Translated Group

Always create a margin object and draw inside a translated `<g>` group. This is the standard D3 pattern — axes live in the margin space, data lives inside.

```js
const margin = { top: 20, right: 20, bottom: 40, left: 50 };
const W = 700, H = 400;
const w = W - margin.left - margin.right;
const h = H - margin.top - margin.bottom;

const svg = d3.select("#chart").attr("width", W).attr("height", H);

// All drawing goes inside this translated group
const g = svg.append("g")
  .attr("transform", `translate(${margin.left},${margin.top})`);
```

---

## Axes

```js
// Bottom axis
g.append("g")
  .attr("transform", `translate(0,${h})`)
  .call(d3.axisBottom(x));

// Left axis
g.append("g")
  .call(d3.axisLeft(y).ticks(5));

// Customize tick format
g.append("g")
  .attr("transform", `translate(0,${h})`)
  .call(d3.axisBottom(x).tickFormat(d3.timeFormat("%b")));
```

---

## Chart Recipes

### Bar chart

```js
g.selectAll(".bar")
  .data(data)
  .enter().append("rect")
  .attr("x", d => x(d.label))
  .attr("y", d => y(d.value))
  .attr("width", x.bandwidth())
  .attr("height", d => h - y(d.value))
  .attr("fill", "#f97316")
  .attr("rx", 4);   // rounded top corners
```

### Horizontal bar chart

```js
const x = d3.scaleLinear().domain([0, d3.max(data, d => d.value)]).range([0, w]);
const y = d3.scaleBand().domain(data.map(d => d.label)).range([0, h]).padding(0.3);

g.selectAll(".bar")
  .data(data)
  .enter().append("rect")
  .attr("x", 0)
  .attr("y", d => y(d.label))
  .attr("width", d => x(d.value))
  .attr("height", y.bandwidth())
  .attr("fill", "#3b82f6")
  .attr("rx", 4);
```

### Line chart

```js
const line = d3.line()
  .x(d => x(d.date))
  .y(d => y(d.value))
  .curve(d3.curveCatmullRom.alpha(0.5));  // smooth curve

g.append("path")
  .datum(data)          // single path for the whole dataset
  .attr("fill", "none")
  .attr("stroke", "#3b82f6")
  .attr("stroke-width", 2.5)
  .attr("d", line);
```

### Area chart

```js
const area = d3.area()
  .x(d => x(d.date))
  .y0(h)               // baseline = bottom of chart
  .y1(d => y(d.value))
  .curve(d3.curveCatmullRom.alpha(0.5));

g.append("path")
  .datum(data)
  .attr("fill", "#f97316")
  .attr("fill-opacity", 0.15)
  .attr("d", area);

// then draw the line on top for the edge
g.append("path")
  .datum(data)
  .attr("fill", "none")
  .attr("stroke", "#f97316")
  .attr("stroke-width", 2)
  .attr("d", line);
```

### Scatter plot

```js
g.selectAll(".dot")
  .data(data)
  .enter().append("circle")
  .attr("cx", d => x(d.x))
  .attr("cy", d => y(d.y))
  .attr("r", 5)
  .attr("fill", d => color(d.category))
  .attr("opacity", 0.75);
```

### Bubble chart

```js
const size = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.size)])
  .range([3, 30]);

g.selectAll(".bubble")
  .data(data)
  .enter().append("circle")
  .attr("cx", d => x(d.x))
  .attr("cy", d => y(d.y))
  .attr("r", d => size(d.size))
  .attr("fill", d => color(d.category))
  .attr("opacity", 0.7)
  .attr("stroke", "#fff")
  .attr("stroke-width", 1);
```

### Stacked bar chart

```js
const stack = d3.stack()
  .keys(["series1", "series2", "series3"]);

const series = stack(data);

g.selectAll(".layer")
  .data(series)
  .enter().append("g")
  .attr("fill", (d, i) => ["#3b82f6", "#f97316", "#22c55e"][i])
  .selectAll("rect")
  .data(d => d)
  .enter().append("rect")
  .attr("x", d => x(d.data.label))
  .attr("y", d => y(d[1]))
  .attr("height", d => y(d[0]) - y(d[1]))
  .attr("width", x.bandwidth());
```

### Donut chart

```js
const radius = Math.min(W, H) / 2 - 20;
const arc = d3.arc().innerRadius(radius * 0.5).outerRadius(radius);
const pie = d3.pie().value(d => d.value).sort(null);

const g = svg.append("g")
  .attr("transform", `translate(${W/2},${H/2})`);

g.selectAll("path")
  .data(pie(data))
  .enter().append("path")
  .attr("d", arc)
  .attr("fill", (d, i) => color(i))
  .attr("stroke", "#fff")
  .attr("stroke-width", 2);
```

---

## Transitions & Animation

```js
// Bars grow up from the baseline on load
g.selectAll("rect")
  .data(data)
  .enter().append("rect")
  .attr("x", d => x(d.label))
  .attr("width", x.bandwidth())
  .attr("y", h)          // start at bottom
  .attr("height", 0)     // start at zero height
  .attr("fill", "#22c55e")
  .transition()
  .duration(800)
  .delay((d, i) => i * 80)   // stagger each bar
  .ease(d3.easeCubicOut)
  .attr("y", d => y(d.value))
  .attr("height", d => h - y(d.value));
```

### Common easing functions

| Function | Feel |
|----------|------|
| `d3.easeLinear` | Constant speed |
| `d3.easeCubicOut` | Fast start, slow end (most natural) |
| `d3.easeElasticOut` | Bouncy |
| `d3.easeBounceOut` | Bouncy ball |
| `d3.easeSinInOut` | Smooth ease in and out |

---

## Tooltips

```js
// Create a hidden tooltip div
const tooltip = d3.select("body").append("div")
  .style("position", "absolute")
  .style("background", "#1a1a2e")
  .style("color", "#fff")
  .style("padding", "8px 12px")
  .style("border-radius", "6px")
  .style("font-size", "13px")
  .style("pointer-events", "none")
  .style("opacity", 0);

// Add events to any selection
bars
  .on("mouseover", (event, d) => {
    tooltip.style("opacity", 1)
           .html(`<strong>${d.label}</strong><br/>${d.value}`)
           .style("left", event.pageX + 12 + "px")
           .style("top",  event.pageY - 28 + "px");
  })
  .on("mouseout", () => tooltip.style("opacity", 0));
```

---

## Responsive Charts

```js
const container = document.getElementById("chart-wrap");
const W = container.clientWidth || 700;
const H = Math.round(W * 0.5);  // 2:1 aspect ratio

const svg = d3.select("#chart")
  .attr("viewBox", `0 0 ${W} ${H}`)  // use viewBox, not fixed width/height
  .attr("width", "100%");
```

---

## Direct Labels (No Legends)

Legends force the eye to travel back and forth. Direct label the data instead.

```js
// Label at the end of each line
g.selectAll(".label")
  .data(data)
  .enter().append("text")
  .attr("x", w + 5)
  .attr("y", d => y(d.values[d.values.length - 1].value))
  .attr("dy", "0.35em")
  .attr("font-size", "12px")
  .attr("fill", d => color(d.name))
  .text(d => d.name);

// Or label above each bar
g.selectAll(".bar-label")
  .data(data)
  .enter().append("text")
  .attr("x", d => x(d.label) + x.bandwidth() / 2)
  .attr("y", d => y(d.value) - 6)
  .attr("text-anchor", "middle")
  .attr("font-size", "12px")
  .attr("fill", "#fff")
  .text(d => d.value);
```

---

## Gridlines

```js
// Horizontal gridlines only (lighter than axes)
g.append("g")
  .attr("class", "grid")
  .call(d3.axisLeft(y).ticks(5).tickSize(-w).tickFormat(""))
  .selectAll("line")
  .attr("stroke", "#333")
  .attr("stroke-dasharray", "2,2");

// Remove the domain line from the grid group
g.select(".grid .domain").remove();
```

---

## Color Palettes

D3 ships with perceptually uniform color interpolators. Use these instead of inventing your own.

### Sequential (low → high)

```js
d3.interpolateViridis    // blue → yellow (best default)
d3.interpolateMagma      // black → yellow → white
d3.interpolatePlasma     // purple → yellow
d3.interpolateBlues      // light blue → dark blue
d3.interpolateGreens     // light green → dark green
d3.interpolateOranges    // light orange → dark orange
```

### Diverging (negative → center → positive)

```js
d3.interpolateRdBu       // red → white → blue
d3.interpolatePiYG       // pink → yellow → green
d3.interpolateBrBG       // brown → white → teal
```

### Categorical (distinct groups)

```js
d3.schemeTableau10        // 10 colors, best general-purpose categorical
d3.schemeSet2             // 8 colors, softer
d3.schemePastel1          // 9 colors, muted
```

Usage:
```js
// Sequential
const color = d3.scaleSequential(d3.interpolateViridis).domain([0, 100]);

// Categorical
const color = d3.scaleOrdinal(d3.schemeTableau10).domain(categories);
```

---

## Full Boilerplate (Standalone D3)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>D3 Chart</title>
  <style>
    body { margin: 0; background: #0f0f0f; display: flex; justify-content: center; padding: 2rem; }
    #chart { max-width: 800px; }
  </style>
</head>
<body>

  <svg id="chart"></svg>

  <script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
  <script>
    const data = [
      { label: "Jan", value: 40 },
      { label: "Feb", value: 80 },
      { label: "Mar", value: 60 },
      { label: "Apr", value: 120 },
      { label: "May", value: 90 },
    ];

    const margin = { top: 20, right: 20, bottom: 40, left: 50 };
    const W = 700, H = 400;
    const w = W - margin.left - margin.right;
    const h = H - margin.top - margin.bottom;

    const svg = d3.select("#chart")
      .attr("viewBox", `0 0 ${W} ${H}`)
      .attr("width", "100%");

    const g = svg.append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
      .domain(data.map(d => d.label))
      .range([0, w])
      .padding(0.3);

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.value)])
      .nice()
      .range([h, 0]);

    // Axes
    g.append("g").attr("transform", `translate(0,${h})`).call(d3.axisBottom(x));
    g.append("g").call(d3.axisLeft(y).ticks(5));

    // Bars with animation
    g.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("x", d => x(d.label))
      .attr("width", x.bandwidth())
      .attr("y", h)
      .attr("height", 0)
      .attr("fill", "#f97316")
      .attr("rx", 4)
      .transition()
      .duration(800)
      .delay((d, i) => i * 80)
      .ease(d3.easeCubicOut)
      .attr("y", d => y(d.value))
      .attr("height", d => h - y(d.value));

    // Direct labels
    g.selectAll(".label")
      .data(data)
      .enter().append("text")
      .attr("x", d => x(d.label) + x.bandwidth() / 2)
      .attr("y", d => y(d.value) - 6)
      .attr("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("fill", "#fff")
      .text(d => d.value);
  </script>

</body>
</html>
```

---

## Quick Reference

| What you want | D3 snippet |
|---------------|------------|
| Linear scale | `d3.scaleLinear().domain([min,max]).range([0,px])` |
| Category scale | `d3.scaleBand().domain(arr).range([0,px]).padding(0.3)` |
| Time scale | `d3.scaleTime().domain([d1,d2]).range([0,px])` |
| Color scale (sequential) | `d3.scaleSequential(d3.interpolateViridis).domain([0,100])` |
| Color scale (categorical) | `d3.scaleOrdinal(d3.schemeTableau10).domain(arr)` |
| Max in data | `d3.max(data, d => d.value)` |
| Min + max | `d3.extent(data, d => d.value)` |
| Nice domain rounding | `scale.nice()` |
| Draw a line | `d3.line().x(d=>x(d.x)).y(d=>y(d.y))` |
| Filled area | `d3.area().x(...).y0(h).y1(d=>y(d.v))` |
| Pie/donut layout | `d3.pie().value(d=>d.value)` |
| Arc generator | `d3.arc().innerRadius(r1).outerRadius(r2)` |
| Stack layout | `d3.stack().keys(["a","b","c"])` |
| Animate | `.transition().duration(600).ease(d3.easeCubicOut)` |
| Add axis | `g.append("g").call(d3.axisLeft(y).ticks(5))` |
| Responsive SVG | `viewBox="0 0 W H"` + `width="100%"` |
| Tooltip | Create div, `.on("mouseover", ...)` on selection |
