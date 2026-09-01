#!/usr/bin/env python3
"""
libgen-scan.py — Scan a reading list against Library Genesis.

Reads markdown reading list files (like `- [ ] Book Title — Author`),
searches each unchecked item on LibGen, reports availability, and
optionally batch-downloads with format preference.

Usage:
  python3 libgen-scan.py ~/reading-list.md
  python3 libgen-scan.py ~/reading-list.md --format epub
  python3 libgen-scan.py ~/reading-list.md --batch-download --output ./books/
  python3 libgen-scan.py ~/reading-list.md --json
  python3 libgen-scan.py ~/reading-list.md --category Politics
  python3 libgen-scan.py ~/reading-list.md --delay 2  # Seconds between searches
"""

import json
import os
import re
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

# Import sibling modules
try:
    import libgen_search as search_mod
except ImportError:
    search_mod = None

try:
    import libgen_download as download_mod
except ImportError:
    download_mod = None

try:
    import libgen_convert as convert_mod
except ImportError:
    convert_mod = None


def parse_reading_list(filepath):
    """Parse a markdown reading list file.

    Returns list of dicts with: title, author, line, checked
    Handles formats like:
      - [ ] Book Title — Author
      - [ ] Book Title
      - [x] Completed Book
      - [ ] Author — Book Title
    Also extracts category from headers (e.g., ## Politics & Philosophy)
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return []

    items = []
    current_category = "General"

    with open(filepath, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line_stripped = line.strip()

            # Track category headers
            header_match = re.match(r"^##+\s+(.+)$", line_stripped)
            if header_match:
                current_category = header_match.group(1).strip()
                continue

            # Match checkbox items: - [ ] or - [x] or * [ ]
            checkbox_match = re.match(
                r"^[-*]\s*\[(.)\]\s*(.+)", line_stripped
            )
            if not checkbox_match:
                continue

            checked = checkbox_match.group(1).lower() == "x"
            text = checkbox_match.group(2).strip()

            # Split title and author
            title = text
            author = ""

            # Try "Title — Author" (em dash)
            em_match = re.split(r"\s*—\s*|\s*–\s*|\s*—\s*", text, maxsplit=1)
            if len(em_match) == 2:
                # Heuristic: if the second part looks like a name (not too long)
                if len(em_match[1]) < 60:
                    title = em_match[0].strip()
                    author = em_match[1].strip()

            # Try "Title (Author)" or "Title [Author]"
            if not author:
                paren_match = re.match(r"(.+?)\s*[\(\[][^\)\]]*?[\)\]]\s*$", text)
                if paren_match:
                    title = paren_match.group(1).strip()
                    # Author-paren: "Title (Author Name)" 
                    inner = re.search(r"\(([^)]+)\)\s*$", text)
                    if inner and len(inner.group(1)) < 60:
                        author = inner.group(1).strip()
                        title = text[:text.index("(")].strip()

            # Try "Author — Title" pattern
            if not author:
                # Maybe it's "Author — Title" format
                if re.search(r"^\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*[—–]\s+", text):
                    parts = re.split(r"\s*[—–]\s*", text, maxsplit=1)
                    author = parts[0].strip()
                    title = parts[1].strip() if len(parts) > 1 else title

            items.append({
                "line": line_num,
                "checked": checked,
                "title": title,
                "author": author,
                "raw": text,
                "category": current_category,
            })

    return items


def extract_search_terms(item):
    """Extract best search terms from a reading list item.

    Returns a list of query strings to try, ordered by specificity.
    """
    title = item["title"]
    author = item["author"]

    queries = []

    # Exact title quote search
    if title:
        queries.append(title)

    # Title + author
    if title and author:
        queries.append(f"{title} {author}")

    # Author search if we got nothing
    if author:
        # Try main part of author name (last name)
        last_name = author.split(",")[0].strip().split()[-1] if "," in author else author.split()[-1]
        if last_name and len(last_name) > 2:
            queries.append(f"{last_name} {title}")

    # Shorter version of title
    if title and len(title) > 30:
        short = title[:40].rsplit(" ", 1)[0]
        queries.append(short)

    return queries


def search_book(item, mirror=None, limit=5, format_pref=None):
    """Search LibGen for a book from the reading list.

    Returns dict with match info or None.
    """
    queries = extract_search_terms(item)
    title_lower = item["title"].lower().strip()
    author_lower = item["author"].lower().strip()

    for query in queries[:3]:  # Try up to 3 queries
        try:
            results = search_mod.search_html(query, mirror=mirror, limit=limit)
            results = search_mod.enrich_json(results)
        except Exception as e:
            print(f"    [warn] Search failed: {e}", file=sys.stderr)
            continue

        if not results:
            continue

        # Filter by format preference
        if format_pref:
            filtered = search_mod.filter_by_format(results, format_pref)
            if filtered:
                results = filtered

        if not results:
            continue

        # Score results by title similarity
        scored = []
        for r in results:
            score = 0
            r_title = r.get("title", "").lower().strip()
            r_author = r.get("author", "").lower().strip()

            # Title match (fuzzy — check if words overlap)
            title_words = set(title_lower.split())
            r_words = set(r_title.split())
            overlap = len(title_words & r_words)
            if overlap > 0:
                score += overlap * 10

            # Exact title match is best
            if r_title == title_lower or r_title.startswith(title_lower):
                score += 50

            # Author match bonus
            if author_lower and r_author:
                if author_lower in r_author or r_author in author_lower:
                    score += 20
                # Last name match
                author_last = author_lower.split()[-1] if author_lower else ""
                if author_last and author_last in r_author:
                    score += 10

            # Prefer EPUB
            if r.get("format", "").lower() == "epub":
                score += 5

            # Prefer books with cover
            if r.get("cover_exists"):
                score += 2

            # Prefer non-broken
            if not r.get("broken"):
                score += 3

            scored.append((score, r))

        # Return highest-scored result
        scored.sort(key=lambda x: x[0], reverse=True)
        best = scored[0]
        if best[0] > 5:  # Minimum threshold
            return {**best[1], "match_score": best[0], "search_query": query}

    return None


def format_scan_results(book, result):
    """Format a scan result as a single-line summary."""
    if not result:
        return f"  ❌ {book['title'][:50]:50} — not found"

    # Size
    size_str = result.get("size", "?")
    try:
        b = int(result.get("filesize_bytes", 0))
        if b > 0:
            size_str = f"{b / 1024:.0f} kB" if b < 1024 * 1024 else f"{b / (1024*1024):.1f} MB"
    except (ValueError, TypeError):
        pass

    fmt = result.get("format", "?").upper()
    md5_short = result["md5"][:10] if result.get("md5") else "??????????"
    cover = " 🖼️" if result.get("cover_exists") else ""

    return (
        f"  ✅ {book['title'][:50]:50}  "
        f"{fmt:4}  {size_str:>8}  {md5_short}{cover}"
    )


def batch_download(items_with_results, output_dir="./downloaded", format_pref="epub"):
    """Download a list of matched books."""
    import libgen_download as dl

    os.makedirs(output_dir, exist_ok=True)
    dl_results = []

    for book, result in items_with_results:
        if not result or not result.get("md5"):
            dl_results.append({"title": book["title"], "status": "skipped", "reason": "no md5"})
            continue

        md5 = result["md5"]
        print(f"\n  📥 Downloading: {book['title'][:50]}...", file=sys.stderr)

        try:
            # Get download URL
            dl_url = dl.get_download_url(md5, mirror=result.get("mirror"))
            if not dl_url:
                dl_results.append({"title": book["title"], "status": "failed", "reason": "no download link"})
                continue

            # Determine extension
            ext = result.get("format", "epub")
            filename = f"{md5[:16]}.{ext}"
            filepath = os.path.join(output_dir, filename)

            # Download
            if dl.download_file(dl_url, filepath):
                # Convert if needed
                final_path = filepath
                if format_pref and format_pref.lower() != ext.lower():
                    converted = dl.convert_format(filepath, format_pref.lower())
                    if converted:
                        final_path = converted
                        os.remove(filepath)

                size = os.path.getsize(final_path) / 1024
                dl_results.append({
                    "title": book["title"],
                    "status": "success",
                    "path": final_path,
                    "size_kb": size,
                })
                print(f"    ✅ {os.path.basename(final_path)} ({size:.0f} kB)", file=sys.stderr)
            else:
                dl_results.append({"title": book["title"], "status": "failed", "reason": "download error"})

            # Rate limiting
            time.sleep(1)

        except Exception as e:
            dl_results.append({"title": book["title"], "status": "error", "reason": str(e)})
            print(f"    ❌ Error: {e}", file=sys.stderr)

    return dl_results


# ─── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Scan a reading list against Library Genesis"
    )
    parser.add_argument("reading_list", help="Path to markdown reading list file")
    parser.add_argument("--format", default=None, help="Preferred format (epub/pdf/mobi)")
    parser.add_argument("--output", "-o", default="./downloaded", help="Download directory")
    parser.add_argument("--batch-download", action="store_true", help="Download matched books")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between searches")
    parser.add_argument("--mirror", default=None, help="Specific mirror URL")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--category", default=None, help="Only scan this category")
    parser.add_argument("--limit", type=int, default=5, help="Search results per book")
    parser.add_argument("--max", type=int, default=0, help="Max books to scan (0 = all)")

    args = parser.parse_args()

    # Ensure search module is available
    if search_mod is None:
        print("Error: libgen_search.py not found in same directory", file=sys.stderr)
        sys.exit(1)

    # Parse reading list
    items = parse_reading_list(args.reading_list)
    unchecked = [i for i in items if not i["checked"]]

    if args.category:
        unchecked = [i for i in unchecked if i["category"] == args.category]

    if not unchecked:
        print("No unchecked items found in the reading list! 🎉", file=sys.stderr)
        sys.exit(0)

    print(f"📋 Reading list: {len(items)} items, {len(unchecked)} unchecked", file=sys.stderr)
    if args.category:
        print(f"   Category: {args.category}", file=sys.stderr)

    # Apply max AFTER printing stats
    if args.max and args.max > 0:
        print(f"   Scanning first {args.max}", file=sys.stderr)
        unchecked = unchecked[:args.max]

    print()

    # Scan each unchecked book
    matched = []
    not_found = []

    for i, book in enumerate(unchecked, 1):
        print(
            f"[{i}/{len(unchecked)}] {book['title'][:50]}...",
            end=" ",
            file=sys.stderr,
        )

        try:
            result = search_book(
                book,
                mirror=args.mirror,
                limit=args.limit,
                format_pref=args.format,
            )
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            result = None

        if result:
            matched.append((book, result))
            print("✅", file=sys.stderr)
            print(format_scan_results(book, result), file=sys.stderr)
        else:
            not_found.append(book)
            print("❌", file=sys.stderr)

        # Rate limiting
        if i < len(unchecked):
            time.sleep(args.delay)

    # Summary
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Results: {len(matched)} found, {len(not_found)} not found", file=sys.stderr)

    # Batch download
    if args.batch_download and matched:
        print(f"\n📥 Batch downloading {len(matched)} book(s) to {args.output}...", file=sys.stderr)
        dl_results = batch_download(matched, args.output, args.format)

        success = sum(1 for r in dl_results if r["status"] == "success")
        failed = sum(1 for r in dl_results if r["status"] != "success")
        print(f"\n   Downloaded: {success}, Failed: {failed}", file=sys.stderr)

        if args.json:
            output = {
                "summary": {"found": len(matched), "not_found": len(not_found)},
                "matched": [
                    {"book": b, "libgen": r}
                    for b, r in matched
                ],
                "not_found": not_found,
                "downloads": dl_results,
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
    elif args.json:
        output = {
            "summary": {"found": len(matched), "not_found": len(not_found)},
            "matched": [
                {"book": b, "libgen": r}
                for b, r in matched
            ],
            "not_found": not_found,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
