#!/usr/bin/env python3
"""
libgen-search.py — Search Library Genesis via hybrid HTML + JSON API.

1. Searches libgen.li (or chosen mirror) via HTML
2. Extracts file IDs from the search results
3. Enriches with clean metadata from the JSON API
4. Returns structured results with format/size/md5

Usage:
  python3 libgen-search.py "dictator's handbook"
  python3 libgen-search.py "thinking fast and slow" --limit 20 --format epub
  python3 libgen-search.py "hayek" --json
  python3 libgen-search.py "queen" --mirror https://libgen.li
"""

import html as html_mod
import json
import os
import re
import sys
import urllib.request
import urllib.parse

# Import mirror discovery from sibling
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
try:
    import libgen_mirrors as mirrors
except ImportError:
    # Fallback: inline mirror logic
    mirrors = None


def find_best_mirror():
    """Get the best available mirror URL."""
    if mirrors:
        import libgen_mirrors as m
        registry = m.load_cache()
        if registry:
            return m.get_best_mirror(registry)
    return "https://libgen.li"


def search_html(query, mirror=None, limit=10):
    """Search LibGen via HTML and extract basic metadata + file IDs.

    Returns list of dicts with: title, author, publisher, year, language,
    pages, size, format, md5, file_id, cover_exists.
    """
    base = (mirror or find_best_mirror()).rstrip("/")
    url = f"{base}/index.php?req={urllib.parse.quote(query)}"

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as r:
        html_content = r.read().decode("utf-8", errors="replace")

    # Strip newlines — libgen has <br> inside attribute values
    html_content = html_content.replace("\n", " ").replace("\r", " ")

    # Find table body
    tbody = re.search(r"<tbody>(.*?)</tbody>", html_content, re.DOTALL)
    if not tbody:
        return []

    rows = re.findall(r"<tr>(.*?)</tr>", tbody.group(1), re.DOTALL)
    results = []

    for row in rows:
        cols = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        if len(cols) < 8:
            continue

        col0 = cols[0]

        # Title: find edition.php link
        title = ""
        for m in re.finditer(
            r'href="edition\.php[^"]*">(.*?)</a>', col0, re.DOTALL
        ):
            text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
            text = html_mod.unescape(text)
            if not re.match(r"^[\d\s;,:]+$", text) and text:
                title = text
                break

        # File ID and edition ID from links
        edition_id = None
        em = re.search(r"edition\.php\?id=(\d+)", col0)
        if em:
            edition_id = em.group(1)

        file_id = None
        fm = re.search(r"/file\.php\?id=(\d+)", row)
        if fm:
            file_id = fm.group(1)

        # MD5 from mirrors column (last col)
        md5 = None
        for col in cols:
            md5_m = re.search(r"md5=([a-f0-9]{32})", col)
            if md5_m:
                md5 = md5_m.group(1)
                break

        results.append(
            {
                "title": title,
                "author": html_mod.unescape(
                    re.sub(r"<[^>]+>", "", cols[1]).strip()
                ),
                "publisher": html_mod.unescape(
                    re.sub(r"<[^>]+>", "", cols[2]).strip()
                ),
                "year": re.sub(r"<[^>]+>", "", cols[3]).strip(),
                "language": re.sub(r"<[^>]+>", "", cols[4]).strip(),
                "pages": re.sub(r"<[^>]+>", "", cols[5]).strip(),
                "size": re.sub(r"<[^>]+>", "", cols[6]).strip(),
                "format": re.sub(r"<[^>]+>", "", cols[7]).strip().lower(),
                "md5": md5,
                "file_id": file_id,
                "edition_id": edition_id,
                "mirror": base,
            }
        )
        if len(results) >= limit:
            break

    return results


def enrich_json(results):
    """Enrich search results with clean metadata from JSON API.

    Uses the file_id to fetch extension, filesize in bytes, cover_exists, etc.
    Modifies results in-place and returns them.
    """
    # Collect all valid file_ids
    file_ids = [
        r["file_id"] for r in results if r.get("file_id") and r["md5"]
    ]
    if not file_ids:
        return results

    base = results[0]["mirror"]
    ids_str = ",".join(file_ids)
    json_url = f"{base}/json.php?object=f&ids={ids_str}"

    try:
        req = urllib.request.Request(json_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception:
        return results  # Fall back to HTML-only data

    if not isinstance(data, dict):
        return results

    # Map file_id -> enriched data
    for r in results:
        fid = r.get("file_id")
        if fid and fid in data:
            rec = data[fid]
            r["filesize_bytes"] = rec.get("filesize")
            if rec.get("extension"):
                r["format"] = rec["extension"].lower()
            if rec.get("cover_exists") == "1":
                r["cover_exists"] = True
            if rec.get("pages") and rec["pages"] != "0":
                r["pages"] = rec["pages"]
            if rec.get("time_added"):
                r["time_added"] = rec["time_added"]
            if rec.get("broken") == "Y":
                r["broken"] = True

    return results


def format_results(results):
    """Format results for human-friendly display (for me to present to user)."""
    if not results:
        return "No results found~ 😿"

    lines = []
    for i, r in enumerate(results, 1):
        # Format size nicely
        size_str = r.get("size", "?")
        try:
            b = int(r.get("filesize_bytes", 0))
            if b > 0:
                if b > 1024 * 1024:
                    size_str = f"{b / (1024*1024):.1f} MB"
                else:
                    size_str = f"{b / 1024:.0f} kB"
        except (ValueError, TypeError):
            pass

        # Year
        year = r.get("year", "")
        y = re.search(r"(\d{4})", year)
        year_str = y.group(1) if y else year[:4] if year else "?"

        # Title
        title = r.get("title", "?")[:60]

        # Author
        author = r.get("author", "?")
        if len(author) > 30:
            author = author[:27] + "..."

        # Format badge
        fmt = r.get("format", "?").upper()
        broken = " 💀" if r.get("broken") else ""
        cover = " 🖼️" if r.get("cover_exists") else ""

        lines.append(
            f"  {i}. {title}  \n"
            f"     {r['md5'][:8]}…  {year_str}  {fmt:4}  {size_str:>8}  {author}{broken}{cover}"
        )

    return "\n\n".join(lines)


def filter_by_format(results, preferred_format):
    """Filter results by preferred format, with smart matching.

    Preferred format can be: epub, pdf, mobi, djvu, or None (no filter).
    If preferred format produces no results, returns all.
    """
    if not preferred_format or preferred_format == "any":
        return results

    pref = preferred_format.lower().strip()
    filtered = [r for r in results if r.get("format", "").lower() == pref]

    # Return filtered results even if empty — caller knows what to do
    return filtered


# ─── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Search Library Genesis")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--limit", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--format", type=str, default=None, help="Preferred format (epub/pdf/mobi)")
    parser.add_argument("--mirror", type=str, default=None, help="Specific mirror URL")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not args.query:
        # Interactive mode
        args.query = input("🔍 Search: ").strip()
        if not args.query:
            print("No query provided.")
            sys.exit(1)

    # Search
    results = search_html(args.query, mirror=args.mirror, limit=args.limit)
    results = enrich_json(results)

    # Filter by format
    if args.format:
        filtered = filter_by_format(results, args.format)
        if filtered:
            results = filtered
        # If no results in preferred format, keep all (user sees what's available)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(format_results(results))
