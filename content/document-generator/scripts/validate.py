"""Validate DOCX/PPTX structure.

Usage:
    python scripts/validate.py <unpacked_dir> <original_file>
"""

import sys
from pathlib import Path


def validate(unpacked_dir: str, original_file: str) -> dict:
    """Basic validation - checks for common issues."""
    unpacked = Path(unpacked_dir)
    original = Path(original_file)

    issues = []

    # Check required files exist
    if not unpacked.exists():
        return {"valid": False, "error": "Directory not found"}

    # Check XML validity
    for xml_file in unpacked.rglob("*.xml"):
        try:
            content = xml_file.read_text(encoding="utf-8")
            if content.count("<") != content.count(">"):
                issues.append(f"Malformed XML: {xml_file.name}")
        except Exception as e:
            issues.append(f"Error reading {xml_file.name}: {e}")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "file_count": len(list(unpacked.rglob("*"))),
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python scripts/validate.py <unpacked_dir> <original_file>")
        sys.exit(1)

    result = validate(sys.argv[1], sys.argv[2])
    import json

    print(json.dumps(result, indent=2))
