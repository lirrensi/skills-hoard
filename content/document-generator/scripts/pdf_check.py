"""PDF utilities - check if PDF has fillable form fields.

Usage:
    python scripts/pdf_check.py <file.pdf>
"""

import sys
from pypdf import PdfReader


def check_fillable(pdf_path: str) -> bool:
    """Check if PDF has fillable form fields."""
    reader = PdfReader(pdf_path)
    return reader.get_fields() is not None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/pdf_check.py <file.pdf>")
        sys.exit(1)

    if check_fillable(sys.argv[1]):
        print("This PDF has fillable form fields")
    else:
        print("This PDF does not have fillable form fields")
