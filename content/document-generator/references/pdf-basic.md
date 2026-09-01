# PDF Basic Operations

## Read & Extract

### Text Extraction
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
for i, page in enumerate(reader.pages):
    print(f"--- Page {i+1} ---")
    print(page.extract_text())
```

### Tables Extraction
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

## Modify & Create

### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()
page = reader.pages[0]
page.rotate(90)  # Clockwise
writer.add_page(page)
with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Create PDFs with ReportLab

### Basic Document
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Title", styles['Title']))
story.append(Spacer(1, 12))
story.append(Paragraph("Body text here.", styles['Normal']))

doc.build(story)
```

### With Tables
```python
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

data = [
    ['Header 1', 'Header 2'],
    ['Cell 1', 'Cell 2']
]
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
```

## Command Line Tools

### qpdf (Recommended)
```bash
# Merge
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf

# Rotate
qpdf input.pdf output.pdf --rotate=+90:1
```

### poppler-utils
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract to images
pdftoppm -png -r 300 input.pdf output

# Extract images
pdfimages -j input.pdf output_prefix
```

## Quick Reference

| Task | Tool | Command/Code |
|------|------|--------------|
| Merge | pypdf | `writer.add_page(page)` |
| Split | pypdf | One page per writer |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create | reportlab | Canvas or Platypus |
| CLI merge | qpdf | `qpdf --empty --pages ...` |
