"""Extract PDF form field information.

Usage:
    python scripts/pdf_extract_fields.py <input.pdf> <output.json>
"""

import json
import sys
from pypdf import PdfReader


def get_field_id(annotation):
    """Get full field ID from annotation hierarchy."""
    parts = []
    ann = annotation
    while ann:
        name = ann.get("/T")
        if name:
            parts.append(name)
        ann = ann.get("/Parent")
    return ".".join(reversed(parts)) if parts else None


def make_field(field, field_id):
    """Create field dict from pypdf field."""
    result = {"field_id": field_id}
    ft = field.get("/FT")

    if ft == "/Tx":
        result["type"] = "text"
    elif ft == "/Btn":
        result["type"] = "checkbox"
        states = field.get("/_States_", [])
        if len(states) == 2:
            result["checked_value"] = states[0] if states[0] != "/Off" else states[1]
            result["unchecked_value"] = "/Off"
    elif ft == "/Ch":
        result["type"] = "choice"
        result["choice_options"] = [
            {"value": s[0], "text": s[1]} for s in field.get("/_States_", [])
        ]
    else:
        result["type"] = f"unknown ({ft})"

    return result


def extract_fields(pdf_path: str) -> list:
    """Extract all form fields from PDF."""
    reader = PdfReader(pdf_path)
    fields = reader.get_fields() or {}

    field_info = {}
    radio_names = set()

    for fid, field in fields.items():
        if field.get("/Kids"):
            if field.get("/FT") == "/Btn":
                radio_names.add(fid)
            continue
        field_info[fid] = make_field(field, fid)

    for page_num, page in enumerate(reader.pages):
        for ann in page.get("/Annots", []):
            fid = get_field_id(ann)
            if fid in field_info:
                field_info[fid]["page"] = page_num + 1
                field_info[fid]["rect"] = ann.get("/Rect")
            elif fid in radio_names:
                # Handle radio groups
                pass  # Simplified

    return [f for f in field_info.values() if "page" in f]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/pdf_extract_fields.py <input.pdf> <output.json>")
        sys.exit(1)

    fields = extract_fields(sys.argv[1])
    with open(sys.argv[2], "w") as f:
        json.dump(fields, f, indent=2)

    print(f"Wrote {len(fields)} fields to {sys.argv[2]}")
