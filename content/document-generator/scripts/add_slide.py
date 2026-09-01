"""Add/duplicate slides in PPTX.

Usage:
    python scripts/add_slide.py <unpacked_dir> <source_slide.xml> [layout]
"""

import argparse
import shutil
import sys
from pathlib import Path


def add_slide(unpacked_dir: str, source_xml: str, layout: str = None) -> str:
    """Add a new slide to the presentation."""
    unpacked = Path(unpacked_dir)
    slides_dir = unpacked / "ppt" / "slides"

    if not slides_dir.exists():
        return "Error: Slides directory not found"

    source = Path(source_xml)
    if not source.exists():
        return f"Error: Source {source_xml} not found"

    # Find next slide number
    existing = list(slides_dir.glob("slide*.xml"))
    max_num = 0
    for f in existing:
        try:
            num = int(f.stem.replace("slide", ""))
            max_num = max(max_num, num)
        except:
            pass

    new_num = max_num + 1
    new_name = f"slide{new_num}.xml"
    dest = slides_dir / new_name

    shutil.copy(source, dest)

    # Would also need to update presentation.xml and relationships
    return f"Created {new_name}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add slide to PPTX")
    parser.add_argument("unpacked_dir", help="Unpacked PPTX directory")
    parser.add_argument("source", help="Source slide XML or layout XML")
    parser.add_argument("layout", nargs="?", help="Layout index (optional)")
    args = parser.parse_args()

    print(add_slide(args.unpacked_dir, args.source, args.layout))
