#!/usr/bin/env python3
"""
make-offline.py — Embed CDN resources into HTML for fully offline usage.

Takes an HTML file with external <script src="..."> and <link rel="stylesheet" href="...">
tags, fetches those resources, and replaces them with inline <script> and <style> blocks.

Usage:
    python make-offline.py input.html                    # modifies in place
    python make-offline.py input.html -o output.html     # write to new file
    python make-offline.py input.html --backup           # keep .bak copy
    python make-offline.py input.html --dry-run          # show what would change
    python make-offline.py input.html --clear-cache      # clear fetch cache first
"""

import re
import sys
import os
import argparse
import urllib.request
import urllib.error
import hashlib
import time
from pathlib import Path

# Cache directory for fetched resources (avoids re-fetching)
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")


def get_cache_path(url: str) -> str:
    """Generate a cache file path for a URL."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
    ext = ".js" if url.endswith(".js") else ".css" if url.endswith(".css") else ".txt"
    return os.path.join(CACHE_DIR, f"{url_hash}{ext}")


def fetch_url(url: str, timeout: int = 15, use_cache: bool = True) -> str:
    """Fetch URL content, with local file caching (24h TTL)."""
    cache_path = get_cache_path(url)

    if use_cache and os.path.exists(cache_path):
        age_hours = (time.time() - os.path.getmtime(cache_path)) / 3600
        if age_hours < 24:
            with open(cache_path, "r", encoding="utf-8") as f:
                return f.read()

    print(f"  Fetching: {url}")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "html-artifact-offline-tool/1.0",
            "Accept": "*/*",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} fetching {url}: {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error fetching {url}: {e.reason}")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch {url}: {e}")

    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(content)

    return content


def make_offline(html_content: str, timeout: int = 15, dry_run: bool = False) -> tuple:
    """
    Process HTML content: replace external script/link tags with inline content.
    Returns (modified_html, num_resources_inlined).
    """
    count = 0
    dry_run_count = 0

    def script_replacer(match):
        nonlocal count, dry_run_count
        full_tag = match.group(0)
        attrs = match.group(1)

        src_match = re.search(r"""src\s*=\s*['"]([^'"]+)['"]""", attrs)
        if not src_match:
            return full_tag

        url = src_match.group(1)
        if not url.startswith(("http://", "https://")):
            return full_tag

        is_module = 'type="module"' in attrs or "type='module'" in attrs
        is_defer = "defer" in attrs
        is_async = "async" in attrs

        if dry_run:
            print(f"  [DRY RUN] Would inline script: {url}")
            dry_run_count += 1
            return full_tag

        try:
            content = fetch_url(url, timeout)
        except RuntimeError as e:
            print(f"  WARNING: {e}", file=sys.stderr)
            return full_tag

        extra_attrs = []
        if is_module:
            extra_attrs.append('type="module"')
        if is_defer:
            extra_attrs.append("defer")
        if is_async:
            extra_attrs.append("async")
        attr_str = (" " + " ".join(extra_attrs)) if extra_attrs else ""

        count += 1
        return f"<!-- inlined from: {url} -->\n<script{attr_str}>\n{content}\n</script>"

    def link_replacer(match):
        nonlocal count, dry_run_count
        full_tag = match.group(0)

        if "stylesheet" not in full_tag:
            return full_tag

        href_match = re.search(r"""href\s*=\s*['"]([^'"]+)['"]""", full_tag)
        if not href_match:
            return full_tag

        url = href_match.group(1)
        if not url.startswith(("http://", "https://")):
            return full_tag

        media_match = re.search(r"""media\s*=\s*['"]([^'"]+)['"]""", full_tag)
        media_attr = f' media="{media_match.group(1)}"' if media_match else ""

        if dry_run:
            print(f"  [DRY RUN] Would inline style: {url}")
            dry_run_count += 1
            return full_tag

        try:
            content = fetch_url(url, timeout)
        except RuntimeError as e:
            print(f"  WARNING: {e}", file=sys.stderr)
            return full_tag

        count += 1
        return f"<!-- inlined from: {url} -->\n<style{media_attr}>\n{content}\n</style>"

    # Process <script> tags: <script src="..."></script> (empty body)
    html_content = re.sub(
        r"<script\s+([^>]*?)>\s*</script>",
        script_replacer,
        html_content,
        flags=re.DOTALL,
    )

    # Process <link> tags: <link rel="stylesheet" href="...">
    html_content = re.sub(
        r"<link\s+[^>]*?[/\s]?>",
        link_replacer,
        html_content,
        flags=re.DOTALL,
    )

    return html_content, count if not dry_run else dry_run_count


def main():
    parser = argparse.ArgumentParser(
        description="Embed CDN resources into HTML for offline usage.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s index.html                    # modify in place
  %(prog)s index.html --backup           # keep .bak
  %(prog)s index.html -o offline.html    # write to new file
  %(prog)s index.html --dry-run          # preview changes
  %(prog)s index.html --clear-cache      # clear fetch cache first
        """,
    )
    parser.add_argument("input", help="Input HTML file")
    parser.add_argument("-o", "--output", help="Output file (default: modify in place)")
    parser.add_argument(
        "--backup", action="store_true", help="Keep .bak backup of original"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without modifying",
    )
    parser.add_argument(
        "--timeout", type=int, default=15, help="Fetch timeout in seconds (default: 15)"
    )
    parser.add_argument(
        "--clear-cache", action="store_true", help="Clear the fetch cache first"
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if args.clear_cache and os.path.exists(CACHE_DIR):
        import shutil

        shutil.rmtree(CACHE_DIR)
        print("Cache cleared.")

    print(f"Reading: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Count external resources before processing
    scripts = re.findall(
        r'<script\s+[^>]*?src\s*=\s*["\']https?://[^"\']+["\'][^>]*>\s*</script>',
        html_content,
        re.DOTALL,
    )
    links = re.findall(
        r'<link\s+[^>]*?rel\s*=\s*["\']stylesheet["\'][^>]*?href\s*=\s*["\']https?://[^"\']+["\'][^>]*>',
        html_content,
        re.DOTALL,
    )
    # Also match <link> where href comes before rel
    links2 = re.findall(
        r'<link\s+[^>]*?href\s*=\s*["\']https?://[^"\']+["\'][^>]*?rel\s*=\s*["\']stylesheet["\'][^>]*>',
        html_content,
        re.DOTALL,
    )
    # And links with just stylesheet in the tag
    links3 = re.findall(
        r'<link\s+[^>]*?href\s*=\s*["\']https?://[^"\']+["\'][^>]*?stylesheet[^>]*>',
        html_content,
        re.DOTALL,
    )
    total = len(scripts) + max(len(links), len(links2), len(links3))

    print(
        f"Found {len(scripts)} external script(s), ~{max(len(links), len(links2), len(links3))} external stylesheet(s)"
    )

    if total == 0:
        print("No external CDN resources found. Nothing to do.")
        sys.exit(0)

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Processing...")
    modified, count = make_offline(
        html_content, timeout=args.timeout, dry_run=args.dry_run
    )

    if args.dry_run:
        print(f"\n[DRY RUN] Would inline {count} resource(s). No files modified.")
        sys.exit(0)

    print(f"\nInlined {count} resource(s).")

    if count == 0:
        print("No resources were successfully inlined.")
        sys.exit(1)

    # Determine output path
    output_path = Path(args.output) if args.output else input_path

    # Backup if requested
    if args.backup and output_path == input_path:
        backup_path = input_path.with_suffix(input_path.suffix + ".bak")
        import shutil

        shutil.copy2(input_path, backup_path)
        print(f"Backup saved: {backup_path}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(modified)

    print(f"Written: {output_path}")

    original_size = len(html_content.encode("utf-8"))
    new_size = len(modified.encode("utf-8"))
    print(
        f"Size: {original_size:,} -> {new_size:,} bytes ({new_size - original_size:+,})"
    )


if __name__ == "__main__":
    main()
