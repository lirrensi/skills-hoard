---
name: document-generator
description: "Use this skill whenever the user wants to create, read, edit, or convert any document file. This includes: PDFs (.pdf), Word documents (.docx), Excel/spreadsheets (.xlsx, .csv), PowerPoint presentations (.pptx), and other office formats. Triggers on any request involving document files — creating new documents from scratch or templates, extracting content, merging/splitting files, filling forms, converting between formats, or any document manipulation task. Do NOT use for database operations, API calls, or non-document file handling."
license: Proprietary. LICENSE.txt has complete terms
---

# Document Generator Skill

## Quick Reference

| Document Type | Read/Extract | Create | Edit |
|---------------|-------------|--------|------|
| PDF | `markitdown` or `pdfplumber` | `reportlab` | Unpack → XML → pack |
| DOCX | `pandoc` or unpack | `docx-js` | Unpack → XML → pack |
| XLSX | `pandas` or `openpyxl` | `openpyxl` | `openpyxl` |
| PPTX | `markitdown` | `pptxgenjs` | Unpack → XML → pack |

## Common Workflows

### 1. Read/Extract Content
```bash
# Universal: markitdown for text extraction
python -m markitdown document.pdf
python -m markitdown document.docx
python -m markitdown document.pptx

# PDF tables specifically
python -c "import pdfplumber; ..."

# Excel data analysis
python -c "import pandas as pd; df = pd.read_excel('file.xlsx')"
```

### 2. Create New Document
- **PDF**: Use `reportlab` (Python) — see [references/pdf-basic.md](references/pdf-basic.md)
- **DOCX**: Use `docx-js` (JavaScript) — see [references/docx-create.md](references/docx-create.md)
- **XLSX**: Use `openpyxl` (Python) — see [references/xlsx-create.md](references/xlsx-create.md)
- **PPTX**: Use `pptxgenjs` (JavaScript) — see [references/pptx-create.md](references/pptx-create.md)

### 3. Edit Existing Document
All office formats follow: unpack → edit XML → pack

```bash
# Unpack any office file
python scripts/unpack.py input.ext unpacked/

# For PDFs: use pypdf directly
python -c "from pypdf import PdfReader, PdfWriter; ..."

# Pack back to office format
python scripts/pack.py unpacked/ output.ext
```

### 4. Convert Between Formats
```bash
# Office → PDF (via LibreOffice)
python scripts/soffice.py --headless --convert-to pdf input.docx

# PDF → Images
python scripts/pdf_to_images.py input.pdf output_dir/
```

## Document-Specific Guides

### PDF Operations
- **Basic operations** (merge, split, rotate, extract): See [references/pdf-basic.md](references/pdf-basic.md)
- **Forms** (fillable fields): See [references/pdf-forms.md](references/pdf-forms.md)
- **Advanced** (rendering, JavaScript libraries): See [references/pdf-advanced.md](references/pdf-advanced.md)

**Quick PDF commands:**
```bash
# Check if fillable
python scripts/pdf_check.py form.pdf

# Extract field info
python scripts/pdf_extract_fields.py form.pdf fields.json

# Convert to images
python scripts/pdf_to_images.py document.pdf images/
```

### DOCX Operations
- **Creation**: See [references/docx-create.md](references/docx-create.md)
- **Editing**: See [references/docx-edit.md](references/docx-edit.md)
- **Critical rules**: Always use DXA units, never percentage for tables; never unicode bullets

### XLSX Operations
- **Creation & editing**: See [references/xlsx-create.md](references/xlsx-create.md)
- **Financial models**: Zero formula errors required; use formulas not hardcoded values
- **Recalculation**: Run `python scripts/recalc.py file.xlsx` after creating formulas

### PPTX Operations
- **Create from scratch**: See [references/pptx-create.md](references/pptx-create.md)
- **Edit template**: See [references/pptx-edit.md](references/pptx-edit.md)

## Essential Scripts

| Script | Purpose |
|--------|---------|
| `scripts/unpack.py` | Extract and pretty-print any office file |
| `scripts/pack.py` | Repack edited files |
| `scripts/soffice.py` | LibreOffice headless for conversions |
| `scripts/recalc.py` | Recalculate Excel formulas |
| `scripts/thumbnail.py` | Create PPTX thumbnail grid |
| `scripts/add_slide.py` | Add/duplicate slides in PPTX |
| `scripts/clean.py` | Remove orphaned PPTX files |
| `scripts/accept_changes.py` | Accept all tracked changes in DOCX |
| `scripts/validate.py` | Validate DOCX/PPTX structure |
| `scripts/pdf_check.py` | Check if PDF has fillable fields |
| `scripts/pdf_extract_fields.py` | Extract form field info |
| `scripts/pdf_to_images.py` | Convert PDF to images |
| `scripts/pdf_fill.py` | Fill PDF forms |

> Note: `scripts/comment.py` is not yet implemented (requires templates).

## Quality Assurance

**Always verify output:**

1. **Content QA**: Extract text and check for missing content
   ```bash
   python -m markitdown output.ext
   ```

2. **Visual QA** (for presentations):
   ```bash
   python scripts/soffice.py --headless --convert-to pdf output.pptx
   python scripts/pdf_to_images.py output.pdf images/
   ```

3. **Formula QA** (Excel):
   ```bash
   python scripts/recalc.py output.xlsx
   # Fix any #REF!, #DIV/0!, #VALUE! errors
   ```

## Dependencies

- **Python**: `pip install pandas openpyxl reportlab pypdf pdfplumber "markitdown[all]"`
- **JavaScript**: `npm install -g docx pptxgenjs`
- **System**: LibreOffice, Poppler (pdftoppm)
