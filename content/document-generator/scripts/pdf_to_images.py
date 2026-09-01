"""Convert PDF to images.

Usage:
    python scripts/pdf_to_images.py <input.pdf> <output_dir/> [--dpi 150]
"""

import argparse
import sys
from pathlib import Path

from pdf2image import convert_from_path


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 150) -> str:
    """Convert PDF pages to images."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(pdf_path, dpi=dpi)

    for i, img in enumerate(images):
        img.save(output_path / f"page_{i + 1:03d}.png", "PNG")

    return f"Converted {len(images)} pages to {output_dir}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDF to images")
    parser.add_argument("input_pdf", help="Input PDF file")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--dpi", type=int, default=150, help="Resolution DPI")
    args = parser.parse_args()

    print(pdf_to_images(args.input_pdf, args.output_dir, args.dpi))
