"""Fill PDF forms (fillable or annotation-based).

Usage:
    # For fillable forms:
    python scripts/pdf_fill.py <input.pdf> <values.json> <output.pdf>

    # Values JSON format for fillable:
    [
        {"field_id": "name", "page": 1, "value": "John"},
        {"field_id": "agree", "page": 1, "value": "/On"}
    ]

    # For non-fillable (annotation-based):
    python scripts/pdf_fill_annot.py <input.pdf> <fields.json> <output.pdf>
"""

import json
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def fill_fillable(pdf_path: str, values_path: str, output_path: str) -> str:
    """Fill fillable PDF form fields."""
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(values_path) as f:
        values = json.load(f)

    for item in values:
        field_id = item.get("field_id")
        value = item.get("value")

        if field_id and value:
            try:
                writer.get_field(field_id).update(value)
            except Exception as e:
                print(f"Warning: Could not set {field_id}: {e}")

    with open(output_path, "wb") as f:
        writer.write(f)

    return f"Filled form written to {output_path}"


def fill_annotation(pdf_path: str, fields_path: str, output_path: str) -> str:
    """Fill non-fillable PDF with text annotations."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

    with open(fields_path) as f:
        fields = json.load(f)

    # Get page info
    pages_info = {p["page_number"]: p for p in fields.get("pages", [])}

    # Create overlay PDF
    c = canvas.Canvas(output_path, pagesize=letter)

    for field in fields.get("form_fields", []):
        page_num = field.get("page_number", 1)

        if page_num in pages_info:
            page_info = pages_info[page_num]
            width = page_info.get("pdf_width", 612)
            height = page_info.get("pdf_height", 792)
            c.setPageSize((width, height))

        bbox = field.get("entry_bounding_box")
        if bbox:
            x0, top, x1, bottom = bbox
            y = top - (field.get("entry_text", {}).get("font_size", 10))
            c.drawString(x0, y, field.get("entry_text", {}).get("text", ""))

    c.save()
    return f"Annotations written to {output_path}"


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python scripts/pdf_fill.py <input.pdf> <values.json> <output.pdf>"
        )
        sys.exit(1)

    _, msg = None, fill_fillable(sys.argv[1], sys.argv[2], sys.argv[3])
    print(msg)
