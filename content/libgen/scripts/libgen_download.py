#!/usr/bin/env python3
"""
libgen-download.py — Download a book from Library Genesis by MD5 hash.

Gets the download link from ads.php, downloads via curl (handles CDN
redirects and slow servers better than urllib), and optionally converts
to preferred format with calibre.

Usage:
  python3 libgen-download.py <md5>
  python3 libgen-download.py <md5> --format epub --output ./books/
  python3 libgen-download.py <md5> --format pdf --convert
  python3 libgen-download.py <md5> --mirror https://libgen.li --output ./
"""

import html as html_mod
import json
import os
import re
import subprocess
import sys
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def find_best_mirror():
    """Get best mirror, trying cache first."""
    mirrors_ref = os.path.join(SCRIPT_DIR, "..", "references", "mirrors.json")
    try:
        with open(mirrors_ref) as f:
            reg = json.load(f)
        for m in reg.get("mirrors", []):
            if m.get("reachable") and m.get("has_ads"):
                return m["url"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return "https://libgen.li"


def get_download_url(md5, mirror=None):
    """Fetch the download page (ads.php) and extract the get.php URL.

    Returns the full download URL, or None if not found.
    """
    base = (mirror or find_best_mirror()).rstrip("/")
    ads_url = f"{base}/ads.php?md5={md5}"

    req = urllib.request.Request(ads_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        html = r.read().decode("utf-8", errors="replace")

    # Look for get.php link (handle &amp; vs raw &)
    m = re.search(r'href="([^"]*get\.php[^"]*)"', html)
    if not m:
        return None

    dl_path = m.group(1).replace("&amp;", "&")
    # Handle absolute vs relative URLs
    if dl_path.startswith("http"):
        return dl_path
    return f"{base}/{dl_path}"


def download_file(url, output_path):
    """Download a file using curl.

    Returns True on success, False on failure.
    """
    result = subprocess.run(
        [
            "curl", "-L", "-o", output_path,
            "--connect-timeout", "15",
            "--max-time", "300",
            "-H", "User-Agent: Mozilla/5.0",
            url,
        ],
        capture_output=True,
        text=True,
        timeout=320,
    )
    if result.returncode != 0:
        print(
            f"curl failed (exit {result.returncode}): {result.stderr}",
            file=sys.stderr,
        )
        return False

    if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
        print("Downloaded file is empty or missing!", file=sys.stderr)
        return False

    return True


def convert_format(input_path, target_format):
    """Convert ebook format using calibre's ebook-convert.

    Installs calibre on demand if not found.
    Target format: epub, pdf, mobi, azw3, docx, etc.
    Returns the path to the converted file, or None on failure.
    """
    # Check if calibre exists
    calibre_path = subprocess.run(
        ["which", "ebook-convert"], capture_output=True, text=True
    ).stdout.strip()

    if not calibre_path:
        print("calibre/ebook-convert not found, running installer...", file=sys.stderr)
        install_calibre()
        calibre_path = subprocess.run(
            ["which", "ebook-convert"], capture_output=True, text=True
        ).stdout.strip()
        if not calibre_path:
            print("Failed to install calibre!", file=sys.stderr)
            return None

    base, ext = os.path.splitext(input_path)
    output_path = f"{base}.{target_format}"

    print(f"  Converting {ext[1:].upper()} → {target_format.upper()}...", file=sys.stderr)

    result = subprocess.run(
        ["ebook-convert", input_path, output_path],
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        print(
            f"  Conversion failed: {result.stderr[:200]}",
            file=sys.stderr,
        )
        return None

    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        return output_path

    return None


def install_calibre():
    """Install calibre via the official static binary installer."""
    print("  Downloading calibre installer...", file=sys.stderr)
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
    if result.returncode != 0:
        print("  Trying pip install as fallback...", file=sys.stderr)
        subprocess.run(
            ["pip3", "install", "calibre", "--break-system-packages"],
            capture_output=True,
            text=True,
            timeout=120,
        )


def lookup_json(md5, mirror=None):
    """Look up file metadata by MD5 using the JSON API.

    Returns dict with metadata or None.
    """
    base = (mirror or find_best_mirror()).rstrip("/")
    # We need the file_id first. Try searching by MD5 directly.
    # The JSON API doesn't search by MD5, so we use ads.php metadata instead.
    url = f"{base}/ads.php?md5={md5}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="replace")

        # Try to extract info from the page.
        # ads.php uses plain text labels (not <b> tags): "Title:", "Author(s):", etc.
        info = {"md5": md5}

        # Strip HTML for easier text matching
        text = re.sub(r"<[^>]+>", "\n", html)
        text = re.sub(r"\n\s*\n", "\n", text)

        def extract_field(label):
            """Extract value after 'label:' at the start of a line."""
            m = re.search(
                rf"^{re.escape(label)}:\s*(.*?)(?:\n|$)",
                text, re.MULTILINE | re.DOTALL
            )
            if m:
                val = m.group(1).strip().split("\n")[0].strip()
                return html_mod.unescape(val) if val else None
            return None

        def extract_field_lower(label):
            """Case-insensitive field extraction at start of line."""
            m = re.search(
                rf"^{re.escape(label)}:\s*(.*?)(?:\n|$)",
                text, re.MULTILINE | re.DOTALL | re.IGNORECASE
            )
            if m:
                val = m.group(1).strip().split("\n")[0].strip()
                return html_mod.unescape(val) if val else None
            return None

        title = extract_field("Title") or extract_field_lower("title")
        if title:
            info["title"] = title

        author = extract_field("Author(s)") or extract_field("Author") or extract_field_lower("author")
        if author:
            info["author"] = author

        ext = extract_field("Extension") or extract_field_lower("extension")
        if ext:
            info["extension"] = ext.strip().lower()

        size = extract_field("Size") or extract_field_lower("size")
        if size:
            info["size"] = size

        year = extract_field("Year") or extract_field_lower("year")
        if year:
            info["year"] = year

        pages = extract_field("Pages") or extract_field_lower("pages")
        if pages:
            info["pages"] = pages

        publisher = extract_field("Publisher") or extract_field_lower("publisher")
        if publisher:
            info["publisher"] = publisher

        return info
    except Exception as e:
        print(f"  Metadata lookup failed: {e}", file=sys.stderr)
        return None


# ─── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download a book from Library Genesis")
    parser.add_argument("md5", help="MD5 hash of the file (from search results)")
    parser.add_argument(
        "--format", type=str, default=None,
        help="Preferred output format (epub/pdf/mobi). "
             "Downloads file and converts if needed.",
    )
    parser.add_argument(
        "--output", type=str, default=".",
        help="Output directory (default: current dir)",
    )
    parser.add_argument(
        "--mirror", type=str, default=None,
        help="Specific mirror URL (default: auto)",
    )
    parser.add_argument(
        "--keep-original", action="store_true",
        help="Keep the original file after conversion",
    )
    parser.add_argument(
        "--convert", action="store_true",
        help="Force conversion even if format matches (e.g., normalize)",
    )

    args = parser.parse_args()

    md5 = args.md5.strip().lower()
    if not re.match(r"^[a-f0-9]{32}$", md5):
        print("Error: Invalid MD5 hash (must be 32 hex characters)", file=sys.stderr)
        sys.exit(1)

    # Lookup metadata
    print(f"📖 Looking up {md5[:16]}...", file=sys.stderr)
    meta = lookup_json(md5, mirror=args.mirror)
    if meta:
        title = meta.get("title", "Unknown")
        author = meta.get("author", "")
        ext = meta.get("extension", "")
        print(f"   {title}", file=sys.stderr)
        if author:
            print(f"   by {author}", file=sys.stderr)
        print(f"   Format: {ext.upper()}", file=sys.stderr)

    # Get download link
    print("   Resolving download link...", file=sys.stderr)
    dl_url = get_download_url(md5, mirror=args.mirror)
    if not dl_url:
        print("Error: Could not find download link!", file=sys.stderr)
        sys.exit(1)

    # Determine file extension
    if meta and meta.get("extension"):
        source_ext = meta["extension"]
    elif args.format:
        # Use preferred format as the source format assumption
        source_ext = args.format.lower()
    else:
        # Default to epub (most common on LibGen)
        source_ext = "epub"

    # Build output path
    os.makedirs(args.output, exist_ok=True)
    source_filename = f"{md5[:16]}.{source_ext}"
    source_path = os.path.join(args.output, source_filename)

    # Download
    print(f"   Downloading to {source_filename}...", file=sys.stderr)
    if not download_file(dl_url, source_path):
        print("Download failed!", file=sys.stderr)
        sys.exit(1)

    size_kb = os.path.getsize(source_path) / 1024
    print(f"   ✅ Downloaded ({size_kb:.0f} kB)", file=sys.stderr)

    # Convert if needed
    output_path = source_path
    if args.format and args.format.lower() != source_ext.lower():
        print(f"   Converting {source_ext.upper()} → {args.format.upper()}...", file=sys.stderr)
        converted = convert_format(source_path, args.format.lower())
        if converted:
            output_path = converted
            if not args.keep_original:
                os.remove(source_path)
                print(f"   Removed original {source_ext.upper()}", file=sys.stderr)
            print(f"   ✅ Converted to {args.format.upper()}", file=sys.stderr)
        else:
            print(f"   ⚠️  Conversion failed, keeping original {source_ext.upper()}", file=sys.stderr)

    final_size = os.path.getsize(output_path) / 1024
    file_name = os.path.basename(output_path)

    print(f"\n📚 {file_name}", file=sys.stderr)
    print(f"   Size: {final_size:.0f} kB", file=sys.stderr)
    print(output_path)  # Print final path to stdout for piping
