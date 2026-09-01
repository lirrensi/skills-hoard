# PDF Advanced Features

## Rendering to Images

### pypdfium2 (Fast, Recommended)
```python
import pypdfium2 as pdfium
from PIL import Image

pdf = pdfium.PdfDocument("document.pdf")
page = pdf[0]
bitmap = page.render(scale=2.0)
img = bitmap.to_pil()
img.save("page_1.png")
```

## JavaScript Libraries

### pdf-lib (Create/Modify PDFs)
```javascript
const { PDFDocument, rgb, StandardFonts } = require('pdf-lib');

async function createPDF() {
    const pdfDoc = await PDFDocument.create();
    const page = pdfDoc.addPage([595, 842]);
    
    const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
    page.drawText('Hello', { x: 50, y: 700, size: 18, font });
    
    const bytes = await pdfDoc.save();
    fs.writeFileSync('output.pdf', bytes);
}
```

### Merge with pdf-lib
```javascript
const pdf1 = await PDFDocument.load(fs.readFileSync('doc1.pdf'));
const pdf2 = await PDFDocument.load(fs.readFileSync('doc2.pdf'));
const merged = await PDFDocument.create();

const pages1 = await merged.copyPages(pdf1, pdf1.getPageIndices());
pages1.forEach(p => merged.addPage(p));

const bytes = await merged.save();
```

## OCR for Scanned PDFs
```python
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = ""
for image in images:
    text += pytesseract.image_to_string(image)
```

## Advanced Table Extraction
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    page = pdf.pages[0]
    settings = {
        "vertical_strategy": "lines",
        "horizontal_strategy": "lines",
        "snap_tolerance": 3
    }
    tables = page.extract_tables(settings)
```

## Performance Tips

- **Large PDFs**: Process pages individually, use streaming
- **Text extraction**: `pdftotext -bbox-layout` for fastest plain text
- **Image extraction**: `pdfimages` is much faster than rendering
- **Memory**: Use chunked processing for files > 100 pages

## Troubleshooting

- **Encrypted**: Use `reader.decrypt("password")`
- **Corrupted**: Run `qpdf --check file.pdf` to diagnose
- **No text**: Likely scanned - use OCR
