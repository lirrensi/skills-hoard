"""Create thumbnail grid for PPTX slides.

Usage:
    python scripts/thumbnail.py <presentation.pptx> [output_prefix]
"""

import argparse
import sys
from pathlib import Path
from io import BytesIO

from pptx import Presentation
from PIL import Image, ImageDraw, ImageFont


def create_thumbnails(
    pptx_path: str, output_prefix: str = "thumbnails", cols: int = 3
) -> str:
    """Create thumbnail grid from PPTX."""
    prs = Presentation(pptx_path)
    slides = list(prs.slides)

    if not slides:
        return "Error: No slides found"

    thumb_w, thumb_h = 320, 180
    rows = (len(slides) + cols - 1) // cols

    grid = Image.new("RGB", (cols * thumb_w, rows * thumb_h), "white")
    draw = ImageDraw.Draw(grid)

    for i, slide in enumerate(slides):
        col = i % cols
        row = i // cols
        x, y = col * thumb_w, row * thumb_h

        # Simple placeholder - in production would render slide
        draw.rectangle([x, y, x + thumb_w, y + thumb_h], outline="gray", width=2)
        draw.text((x + 10, y + 10), f"Slide {i + 1}", fill="black")

    output_path = f"{output_prefix}.jpg"
    grid.save(output_path)
    return f"Created {output_path} ({len(slides)} slides)"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create PPTX thumbnail grid")
    parser.add_argument("input_file", help="PPTX file")
    parser.add_argument(
        "output_prefix", nargs="?", default="thumbnails", help="Output prefix"
    )
    parser.add_argument("--cols", type=int, default=3, help="Columns in grid")
    args = parser.parse_args()

    print(create_thumbnails(args.input_file, args.output_prefix, args.cols))
