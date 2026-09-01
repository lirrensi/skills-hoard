"""Clean unpacked PPTX - remove orphaned files.

Usage:
    python scripts/clean.py <unpacked_dir>
"""

import sys
from pathlib import Path


def clean(unpacked_dir: str) -> str:
    """Remove orphaned files not referenced in presentation.xml."""
    unpacked = Path(unpacked_dir)

    # Read presentation.xml to get list of referenced files
    pres_xml = unpacked / "ppt" / "presentation.xml"
    if not pres_xml.exists():
        return "Error: presentation.xml not found"

    content = pres_xml.read_text(encoding="utf-8")

    # Find all referenced file IDs
    referenced = set()

    # Parse relationships
    for rels_file in unpacked.rglob("_rels"):
        rels_content = rels_file.read_text(encoding="utf-8")
        # Simple extraction - in production would parse XML properly
        for line in rels_content.split("<Relationship"):
            if 'Target="' in line:
                start = line.find('Target="') + 8
                end = line.find('"', start)
                if start > 7 and end > start:
                    target = line[start:end]
                    referenced.add(target)

    # Remove unreferenced files
    removed = 0
    for xml_file in list(unpacked.rglob("*.xml")) + list(unpacked.rglob("*.rels")):
        rel_path = xml_file.relative_to(unpacked)
        if str(rel_path) not in referenced:
            xml_file.unlink()
            removed += 1

    return f"Cleaned {removed} orphaned files"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/clean.py <unpacked_dir>")
        sys.exit(1)

    print(clean(sys.argv[1]))
