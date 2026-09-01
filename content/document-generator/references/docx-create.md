# DOCX Creation

## Setup
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        ImageRun, Header, Footer, HeadingLevel, BorderStyle, WidthType,
        ShadingType, PageOrientation } = require('docx');

const doc = new Document({ sections: [{ children: [] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

## Critical Rules

⚠️ **Always follow these or documents will break:**

1. **Page size**: Set explicitly (US Letter: 12240×15840 DXA)
2. **Never unicode bullets**: Use `LevelFormat.BULLET` with numbering config
3. **Never `\n`**: Use separate Paragraph elements
4. **Table widths**: Always use `WidthType.DXA`, never PERCENTAGE
5. **Table dual-widths**: Set both table `width` AND cell `width`, plus `columnWidths`
6. **Shading**: Use `ShadingType.CLEAR`, never SOLID
7. **ImageRun**: Must include `type` parameter (png/jpg/etc)

## Page Setup
```javascript
sections: [{
  properties: {
    page: {
      size: { width: 12240, height: 15840 },  // US Letter
      margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
    }
  },
  children: []
}]
```

## Text & Formatting
```javascript
// Paragraphs
new Paragraph({ children: [new TextRun({ text: "Bold", bold: true })] })

// Headings
new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] })

// Lists - NEVER unicode bullets
numbering: {
  config: [
    { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•" }] }
  ]
}
new Paragraph({ numbering: { reference: "bullets", level: 0 }, children: [...] })
```

## Tables (Critical)
```javascript
new Table({
  width: { size: 9360, type: WidthType.DXA },  // US Letter content width
  columnWidths: [4680, 4680],
  rows: [new TableRow({
    children: [new TableCell({
      width: { size: 4680, type: WidthType.DXA },
      borders: { top: border, bottom: border, left: border, right: border },
      shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 120, right: 120 },
      children: [new Paragraph("Cell")]
    })]
  })]
})
```

## Images
```javascript
new Paragraph({
  children: [new ImageRun({
    type: "png",  // REQUIRED
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" }
  })]
})
```

## Headers/Footers
```javascript
sections: [{
  headers: { default: new Header({ children: [new Paragraph("Header")] }) },
  footers: { default: new Footer({ children: [new Paragraph({ children: [
    new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })
  ]})] }) },
  children: []
}]
```

## Validation
After creating:
```bash
python scripts/office/validate.py doc.docx
```
If fails: unpack → fix XML → pack
