# libgen.li HTML Quirks

## `<br>` Inside Attribute Values

LibGen's HTML contains invalid markup where `<br>` appears *inside* HTML attribute values:

```html
<a data-toggle="tooltip" data-placement="right" data-html="true"
   title="Add/Edit : 2016-01-05/2025-09-20; ID: 2811353<br>Smith - The Dictator's Handbook.epub"
   href="edition.php?id=143872741">The Dictator's Handbook... <i></i></a>
```

This breaks every standard HTML parser in the known universe — `html.parser`, `lxml`, `BeautifulSoup`, etc. all crash or produce garbage.

### Why It Breaks Parsers

The HTML spec says `title="..."` should be treated as literal text, so `<br>` inside it is just characters. But the `<br>` closing `>` is indistinguishable from a tag-closing `>` at the parser level. Python's `html.parser` emits a `handle_starttag('br', [])` event for it, fragmenting the `<a>` element into pieces.

### Solution: Regex-Only Parsing

Always use raw regex on unfiltered HTML from libgen.li:

```python
# Strip newlines first to simplify patterns
html_content = html_content.replace('\n', ' ').replace('\r', ' ')
```

Key patterns that work:

| Target | Pattern | Notes |
|---|---|---|
| Table body | `<tbody>(.*?)</tbody>` | |
| Rows | `<tr>(.*?)</tr>` | |
| Columns | `<td[^>]*>(.*?)</td>` | Works because the `<br>` is *inside* a `<td>`, not in its attributes |
| Title link | `href="edition\.php[^"]*">(.*?)</a>` | First matching `<a>` with non-ISBN text |
| MD5 hash | `md5=([a-f0-9]{32})` | Found in the mirrors column (last `<td>`) |
| Year | `(\d{4})` | Matched within stripped column 3 |

### JSON API Enrichment (Recommended)

After extracting file IDs from HTML, use the JSON API for clean metadata:

```python
# Fetch clean file metadata for known IDs
curl -sS "https://libgen.li/json.php?object=f&ids=ID1,ID2,ID3"
```

The JSON API returns: `extension`, `filesize` (bytes), `md5`, `cover_exists`,
`time_added`, `broken` status, `pages`, `dpi`, and more. Use this to replace
the messy HTML-scraped values for format, size, and pages.

**References:** `scripts/libgen_search.py` for the full hybrid implementation.

## ads.php Metadata Format

The download page (`ads.php?md5=HASH`) uses **plain text labels** (not `<b>`
tags) for book metadata:

```
Title: The Dictator's Handbook: Why Bad Behavior is Almost Always Good Politics
Series:
Author(s): Smith, Alastair
Publisher: PublicAffairs
Year: 2011
ISBN: 9781610390453; 1610390458; 1992113114; 9781992113114
```

Note: `Extension:`, `Size:`, and `Pages:` are NOT present on this page —
those live in the search results table. The JSON API is the best source.

**References:**
- `scripts/libgen_download.py` — `lookup_json()` function
- `scripts/libgen_search.py` — `enrich_json()` for search result enrichment

## URL Encoding Variations

### `&amp;` vs `&` in get.php Links

The download URL from `ads.php` can appear in two forms:

```
href="get.php?md5=HASH&amp;key=KEY"   # HTML-encoded
href="get.php?md5=HASH&key=KEY"      # raw URL
```

Always normalize: `url.replace('&amp;', '&')`

### Shell `&` Problem

The `&` in the download URL is a background operator in bash. Never interpolate a `get.php` URL directly into a shell command without quoting:

```bash
# WRONG - & backgrounds the process
curl -L -o book.epub "$(get_url)"   # UNLESS double-quoted

# RIGHT
curl -L -o book.epub "https://libgen.li/get.php?md5=HASH&key=KEY"
```

## Table Column Layout

The search results table has 9 columns (0-indexed):

| Index | Content | Extraction |
|---|---|---|
| 0 | Title + badges | `href="edition.php…">TITLE</a>` |
| 1 | Author(s) | Strip HTML, unescape entities |
| 2 | Publisher | Strip HTML, unescape entities |
| 3 | Year | Regex `(\d{4})` after stripping HTML |
| 4 | Language | Plain text after stripping |
| 5 | Pages | Plain text after stripping |
| 6 | Size | Plain text after stripping (e.g. "686 kB") |
| 7 | Format | Plain text after stripping (e.g. "epub") |
| 8 | Mirrors | Badge links with MD5 hashes |

## Ad Injection

libgen.li injects ad-serving JavaScript. The most common is:

```html
<script type='text/javascript' src='//inopportunefable.com/28/4b/51/...'></script>
```

These appear in page HTML but don't affect the table content. Ignore them.