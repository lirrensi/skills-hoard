# PPTX Creation (From Scratch)

## Setup
```javascript
const pptxgen = require("pptxgenjs");

let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';  // 10" × 5.625"
pres.author = 'Name';
pres.title = 'Title';

let slide = pres.addSlide();
slide.addText("Hello!", { x: 0.5, y: 0.5, fontSize: 36 });

pres.writeFile({ fileName: "presentation.pptx" });
```

## Layout Dimensions
- `LAYOUT_16x9`: 10" × 5.625" (default)
- `LAYOUT_16x10`: 10" × 6.25"
- `LAYOUT_4x3`: 10" × 7.5"

## Text
```javascript
slide.addText("Title", {
  x: 0.5, y: 0.3, w: 9, h: 0.6,
  fontSize: 36, fontFace: "Arial", bold: true,
  color: "363636", align: "center"
});
```

## Lists (Never Unicode Bullets)
```javascript
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true } }
], { x: 0.5, y: 1.5, w: 8, h: 2 });
```

## Shapes
```javascript
slide.addShape(pres.shapes.RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FF0000" },
  line: { color: "000000", width: 2 }
});

slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "FFFFFF" },
  rectRadius: 0.1
});
```

## Images
```javascript
slide.addImage({ path: "image.png", x: 1, y: 1, w: 5, h: 3 });
// or
slide.addImage({ data: "image/png;base64,...", x: 1, y: 1, w: 5, h: 3 });
```

## Charts
```javascript
slide.addChart(pres.charts.BAR, [{
  name: "Sales", labels: ["Q1","Q2","Q3"], values: [100,200,300]
}], {
  x: 0.5, y: 1, w: 9, h: 4,
  chartColors: ["0D9488", "14B8A6"],
  showValue: true
});
```

## Common Pitfalls

⚠️ **Critical rules:**
1. **Never `#` in hex colors** — use `"FF0000"`, NOT `"#FF0000"`
2. **Never opacity in hex** — use `{ transparency: 50 }`, NOT `"FF000080"`
3. **Never unicode bullets** — use `{ bullet: true }`
4. **Fresh option objects** — don't reuse shadow objects between calls
5. **ROUNDED_RECTANGLE + accent borders** — use RECTANGLE instead

## Icons (via react-icons)
```javascript
const sharp = require("sharp");
// Generate icon PNG, then add to slide
slide.addImage({ data: iconPngBase64, x: 1, y: 1, w: 0.5, h: 0.5 });
```
