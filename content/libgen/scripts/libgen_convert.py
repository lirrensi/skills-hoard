#!/usr/bin/env python3
"""
libgen-convert.py — Convert ebooks between formats using calibre.

Installs calibre on demand if not found. Supports any format calibre
handles: epub, mobi, pdf, azw3, docx, txt, html, rtf, and many more.

Usage:
  python3 libgen-convert.py book.mobi --to epub
  python3 libgen-convert.py book.pdf --to epub --output ./converted/
  python3 libgen-convert.py book.epub --to mobi --keep-original
"""

import os
import subprocess
import sys


def find_calibre():
    """Find calibre's ebook-convert binary. Returns path or None."""
    result = subprocess.run(
        ["which", "ebook-convert"], capture_output=True, text=True, timeout=5
    )
    path = result.stdout.strip()
    if path:
        return path

    # Also check common locations
    for candidate in [
        "/usr/bin/ebook-convert",
        "/usr/local/bin/ebook-convert",
        os.path.expanduser("~/calibre/ebook-convert"),
    ]:
        if os.path.isfile(candidate):
            return candidate
    return None


def install_calibre():
    """Install calibre. Tries official installer, then pip as fallback."""
    print("Installing calibre...", file=sys.stderr)

    # Method 1: Official static binary installer
    result = subprocess.run(
        [
            "bash", "-c",
            "wget -q -O- https://download.calibre-ebook.com/linux-installer.sh "
            "| sudo bash /dev/stdin",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode == 0:
        print("  calibre installed via official installer", file=sys.stderr)
        return find_calibre()

    # Method 2: pip install
    print("  Official installer failed, trying pip...", file=sys.stderr)
    result = subprocess.run(
        ["pip3", "install", "calibre", "--break-system-packages"],
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode == 0:
        print("  calibre installed via pip", file=sys.stderr)
        return find_calibre()

    print("  Failed to install calibre!", file=sys.stderr)
    return None


def get_formats():
    """Return list of known ebook formats for display."""
    return [
        "epub", "mobi", "pdf", "azw3", "docx", "txt",
        "html", "rtf", "lit", "fb2", "pdb", "lrf",
        "odt", "cbc", "cbr", "cbz", "djvu",
    ]


def convert(input_path, target_format, output_dir=None, keep_original=False):
    """Convert an ebook file to the target format.

    Args:
        input_path: Path to the source ebook file
        target_format: Target format extension (e.g., 'epub', 'mobi')
        output_dir: Output directory (default: same as input)
        keep_original: If True, don't delete the original file

    Returns:
        Path to the converted file, or None on failure.
    """
    if not os.path.exists(input_path):
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        return None

    source_ext = os.path.splitext(input_path)[1].lstrip(".").lower()
    target_format = target_format.lower().strip().lstrip(".")

    if source_ext == target_format:
        print(f"Source is already {target_format.upper()}, nothing to do", file=sys.stderr)
        return input_path

    # Ensure calibre is available
    calibre = find_calibre()
    if not calibre:
        calibre = install_calibre()
        if not calibre:
            print(
                "Error: calibre not available and installation failed",
                file=sys.stderr,
            )
            return None

    # Build output path
    base = os.path.splitext(input_path)[0]
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        out_name = os.path.basename(base) + f".{target_format}"
        output_path = os.path.join(output_dir, out_name)
    else:
        output_path = f"{base}.{target_format}"

    # Run conversion
    print(
        f"  Converting {source_ext.upper()} → {target_format.upper()}...",
        file=sys.stderr,
    )

    result = subprocess.run(
        [calibre, input_path, output_path],
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        print(f"  Conversion failed: {result.stderr[:300]}", file=sys.stderr)
        return None

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        print("  Converted file is empty or missing!", file=sys.stderr)
        return None

    size_kb = os.path.getsize(output_path) / 1024
    print(f"  ✅ Converted → {os.path.basename(output_path)} ({size_kb:.0f} kB)", file=sys.stderr)

    # Optionally remove original
    if not keep_original:
        os.remove(input_path)
        print(f"  Removed original: {os.path.basename(input_path)}", file=sys.stderr)

    return output_path


# ─── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert ebook formats using calibre")
    parser.add_argument("input", help="Input ebook file path")
    parser.add_argument("--to", dest="target_format", required=True, help="Target format (e.g., epub, mobi, pdf)")
    parser.add_argument("--output", "-o", dest="output_dir", default=None, help="Output directory")
    parser.add_argument("--keep-original", action="store_true", help="Keep the original file")
    parser.add_argument("--list-formats", action="store_true", help="List supported formats")

    args = parser.parse_args()

    if args.list_formats:
        print("Supported formats:", ", ".join(get_formats()))
        sys.exit(0)

    result = convert(
        args.input,
        args.target_format,
        output_dir=args.output_dir,
        keep_original=args.keep_original,
    )

    if result:
        print(result)  # Print final path for piping
    else:
        sys.exit(1)
