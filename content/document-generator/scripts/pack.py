"""Pack a directory into a DOCX, PPTX, or XLSX file.

Usage:
    python scripts/pack.py <input_directory> <output_file> [--original <file>]

Examples:
    python scripts/pack.py unpacked/ output.docx
    python scripts/pack.py unpacked/ output.pptx --original input.docx
"""

import argparse
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path

import defusedxml.minidom


def pack(
    input_directory: str,
    output_file: str,
    original_file: str | None = None,
) -> tuple[None, str]:
    input_dir = Path(input_directory)
    output_path = Path(output_file)
    suffix = output_path.suffix.lower()

    if not input_dir.is_dir():
        return None, f"Error: {input_dir} is not a directory"

    if suffix not in {".docx", ".pptx", ".xlsx"}:
        return None, f"Error: {output_file} must be a .docx, .pptx, or .xlsx file"

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_content_dir = Path(temp_dir) / "content"
        shutil.copytree(input_dir, temp_content_dir)

        # Condense XML
        for pattern in ["*.xml", "*.rels"]:
            for xml_file in temp_content_dir.rglob(pattern):
                _condense_xml(xml_file)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in temp_content_dir.rglob("*"):
                if f.is_file():
                    zf.write(f, f.relative_to(temp_content_dir))

    return None, f"Successfully packed {input_dir} to {output_file}"


def _condense_xml(xml_file: Path) -> None:
    try:
        with open(xml_file, encoding="utf-8") as f:
            dom = defusedxml.minidom.parse(f)

        for element in dom.getElementsByTagName("*"):
            if element.tagName.endswith(":t"):
                continue

            for child in list(element.childNodes):
                if (
                    child.nodeType == child.TEXT_NODE
                    and child.nodeValue
                    and child.nodeValue.strip() == ""
                ) or child.nodeType == child.COMMENT_NODE:
                    element.removeChild(child)

        xml_file.write_bytes(dom.toxml(encoding="UTF-8"))
    except Exception as e:
        print(f"ERROR: Failed to parse {xml_file.name}: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack directory into Office file")
    parser.add_argument("input_directory", help="Unpacked directory")
    parser.add_argument("output_file", help="Output Office file")
    parser.add_argument("--original", help="Original file for reference", default=None)
    args = parser.parse_args()

    _, message = pack(args.input_directory, args.output_file, args.original)
    print(message)

    if "Error" in message:
        sys.exit(1)
