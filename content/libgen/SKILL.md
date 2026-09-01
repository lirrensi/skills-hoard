---
name: libgen
description: >-
  Search, download, and manage books from Library Genesis (LibGen).
  Mirror auto-discovery, hybrid HTML+JSON API search, format conversion
  with calibre, and reading list scanning.
tags: [libgen, library-genesis, books, downloads, ebooks, research, calibre]
category: research
trigger: search (for|in)? libgen|download (from|on) libgen|libgen search|find book (on|via) libgen|grab (a|the) book from libgen|scan (my|the) reading list|libgen mirrors|convert ebook|batch download
---

# LibGen Skill — Library Genesis Tool Suite

Portable scripts for searching, downloading, and managing books from
Library Genesis. Designed to be shared — no hardcoded paths, everything
is configurable via CLI arguments.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/libgen_mirrors.py` | Mirror discovery (Wikidata + health check) |
| `scripts/libgen_search.py` | Search via hybrid HTML + JSON API enrichment |
| `scripts/libgen_download.py` | Download by MD5 with format conversion |
| `scripts/libgen_convert.py` | Standalone calibre format converter |
| `scripts/libgen_scan.py` | Reading list scanner + batch download |

**Legacy scripts** (old single-mirror approach, kept for reference):
- `scripts/search_libgen.py` — HTML-only search
- `scripts/download_libgen.py` — Basic download by MD5

## Quick Reference

```bash
cd /path/to/libgen/scripts/

# Mirror discovery
python3 libgen_mirrors.py                      # Show cached mirrors
python3 libgen_mirrors.py --discover            # Force fresh discovery
python3 libgen_mirrors.py --best                # Return best mirror URL
python3 libgen_mirrors.py --test https://...    # Test a specific URL

# Search
python3 libgen_search.py "query"
python3 libgen_search.py "query" --limit 20 --format epub
python3 libgen_search.py "query" --json         # Machine-readable output

# Download
python3 libgen_download.py MD5_HASH
python3 libgen_download.py MD5 --format epub --output ./books/
python3 libgen_download.py MD5 --keep-original  # Don't delete source after conversion

# Convert
python3 libgen_convert.py book.mobi --to epub
python3 libgen_convert.py book.pdf --to epub --output ./converted/

# Reading list scan
python3 libgen_scan.py ~/reading-list.md
python3 libgen_scan.py ~/reading-list.md --format epub
python3 libgen_scan.py ~/reading-list.md --batch-download --output ./books/
python3 libgen_scan.py ~/reading-list.md --category Politics --max 5
```

## Architecture

### Mirror Discovery (`libgen_mirrors.py`)

```
1. Wikidata SPARQL query → official mirrors (libgen.is, etc.)
2. Hardcoded known list → libgen.li, .rs, .is, .st, .gs, .lc, .pm
3. Health-check each from current location (connectivity, APIs)
4. Cache results to references/mirrors.json
5. On failure → re-discover automatically
```

Key features:
- Queries Wikidata entity Q22017206 (Library Genesis) via SPARQL
- Tests each mirror for: HTTP connectivity, search endpoint, JSON API, ads.php
- Sorts by capability score (has JSON API > has search > has ads) + latency
- Caches results so subsequent calls are instant

### Search (`libgen_search.py`) — Hybrid Approach

```
Search(query)
  │
  ├─ HTML scrape (index.php?req=...) → extract file_ids + md5 + basic metadata
  │    libgen.li has <br> inside HTML attributes — uses regex, NOT an HTML parser
  │
  └─ JSON API (json.php?object=f&ids=...) → enrich with clean metadata
       extension, filesize_bytes, cover_exists, broken status, time_added
       
  Returns structured results with both HTML-scraped and JSON-enriched data
```

**Why not pure JSON?** LibGen's JSON API (`json.php`) only accepts file IDs —
there's no search-via-JSON endpoint. The HTML search page is the only way to
find books by query. Once we have IDs, we enrich with JSON for cleaner data.

### Download (`libgen_download.py`)

```
1. Lookup MD5 → ads.php → extract metadata (title, author, year, extension)
2. Extract download link (get.php?md5=HASH&key=KEY)
3. Download via curl (handles CDN redirects better than urllib)
4. Optional: convert to preferred format with calibre (installed on demand)
5. Output: path to downloaded file
```

**Format preference:**
- `--format epub` — download file, convert to epub if different format
- `--keep-original` — keep the source file after conversion
- Falls back gracefully if no format match is found

### Reading List Scanner (`libgen_scan.py`)

```
1. Parse markdown reading list → extract unchecked items
2. For each unchecked book:
   a. Generate search queries (title, author, title+author)
   b. Search LibGen via hybrid approach
   c. Score results by title similarity + author match + format preference
   d. Report availability with format/size/cover info
3. Optional: batch download matched books with format conversion
```

**Reading list format support:**
```
## Category Header (optional)
- [ ] Book Title — Author
- [x] Completed Book
- [ ] Book Title (with author in parens)
- [ ] Author — Book Title
```

### Format Conversion (`libgen_convert.py`)

Standalone calibre wrapper. Installs calibre on demand via official
installer (falls back to pip if that fails).

```bash
python3 libgen_convert.py input.mobi --to epub
python3 libgen_convert.py input.pdf --to epub --keep-original
python3 libgen_convert.py input.azw3 --to epub --output ./converted/
```

Supports all calibre formats: epub, mobi, pdf, azw3, docx, txt, html,
rtf, lit, fb2, pdb, lrf, odt, cbr, cbz, djvu, and more.

## Mirror Status

Checked automatically via `libgen_mirrors.py`. Current best mirror cached
in `references/mirrors.json`. To re-check:

```bash
python3 scripts/libgen_mirrors.py --discover
```

## Workflow Examples (for me to use)

### Searching for a book
```bash
python3 scripts/libgen_search.py "dictator's handbook" --format epub
```
→ Returns structured results with MD5 hashes, format, size, cover indicator.

### Downloading a book
```bash
python3 scripts/libgen_download.py $MD5 --format epub --output ~/Books/Politics/
```

### Scanning + batch downloading reading list
```bash
python3 scripts/libgen_scan.py ~/Books/reading-list.md \
  --format epub \
  --batch-download \
  --output ~/Books/ \
  --category "Politics" \
  --max 5
```

### Converting a downloaded book
```bash
python3 scripts/libgen_convert.py ~/Books/book.mobi --to epub
```

## Pitfalls

- **Mirrors go down frequently** — always use `--discover` if downloads fail
- **libgen.is/Wikidata says it's up but may not work from your location** — always test from your own server
- **HTML parsing required** — no JSON search API exists; HTML has `<br>` inside attribute values so regex is the only reliable approach (see `references/html-quirks.md`)
- **CDN timeouts** — urllib often times out on CDN servers; curl handles them better (download script uses curl)
- **`&` in output paths** — bash treats `&` as background operator; use single quotes or Python subprocess with list args
- **Calibre install** — requires `sudo` for the official installer; falls back to `pip3 install calibre --break-system-packages`
- **Rate limiting** — some mirrors throttle; use `--delay` in scan (default 1s)
- **Reading list parsing** — only works with markdown format (`- [ ]` checkboxes); plain lists won't parse

## Legacy Scripts

The old `search_libgen.py` and `download_libgen.py` are kept for reference
but are superseded by the new _libgen_*.py_ suite. The legacy scripts only
use `libgen.li` with pure HTML parsing and no format conversion.
