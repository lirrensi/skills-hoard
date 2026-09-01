# Mirror Discovery Research — May 18, 2026

## Sources for Finding Live Mirrors

### 1. Wikidata SPARQL Query (Primary)

Libgen has a Wikidata entity at `Q22017206`. The `P856` property holds official website URLs.

**Query:**
```sparql
SELECT ?urls WHERE {
  { wd:Q22017206 p:P856 [wikibase:rank wikibase:NormalRank; ps:P856 ?urls]. }
}
```

**Endpoint:** `https://query.wikidata.org/sparql?format=json`

**Result (May 2026):** Only `https://libgen.is` is listed.

**Limitation:** Wikidata only shows "official" mirrors and may lag behind. It's a starting point, not comprehensive.

### 2. whereislibgen.vercel.app (Aggregator)

A lightweight Next.js app that wraps the Wikidata query. Runs on Vercel.

**Endpoints:**
- `GET /api` → JSON array of mirror URLs: `["https://libgen.is"]`
- `GET /go` → 302 redirect to the current best mirror
- `GET /` → HTML page with mirror info

**Source:** https://github.com/rvnproject/whereislibgen (Node.js/Express, last updated Dec 2022)

**How it works:** Queries Wikidata SPARQL, sorts results (HTTPS domains first, then HTTPS IPs, then HTTP domains, then HTTP IPs). Returns the first URL as "current."

### 3. Articles/Proxy Lists (Fallback)

Various websites publish LibGen proxy lists:
- `geekchamp.com/libgen-proxy-mirror-sites-list`
- `privacyaffairs.com/unblock-libgen`
- `techyorker.com/libgen-proxy-mirror-sites-list`
- `victoryhub.cc/en/tools/libgen-monitor` (Next.js site with real-time monitoring)

These are less reliable — often outdated or SEO-bait. Use only as last resort.

## Known Mirror List (Hardcoded Fallback)

| Domain | Status (May 2026) | Notes |
|--------|-------------------|-------|
| `libgen.li` | ✅ Alive | HTTPS works. JSON API works. Only currently responsive mirror from our server. |
| `libgen.is` | ❌ Timed out | Listed by Wikidata. Probably blocked/geofenced from our server. |
| `libgen.rs` | ❌ DNS/resolve timeout | Historical main mirror. Sometimes works on port 80. |
| `libgen.st` | ❌ Timed out | Intermittently operational. |
| `libgen.gs` | ❌ Timed out | Tested but no response. |
| `libgen.lc` | ❌ Not resolved | DNS didn't resolve. |
| `libgen.pm` | ❌ Not resolved | DNS didn't resolve. |

## Connectivity Testing

Always test FROM THE SERVER that will be doing the work. A mirror that works globally may be unreachable from specific networks.

**Quick test:**
```bash
for m in libgen.li libgen.rs libgen.is libgen.st libgen.gs libgen.lc libgen.pm; do
  http_code=$(curl -sI --connect-timeout 5 "https://$m/" -o /dev/null -w "%{http_code}" 2>/dev/null || echo "FAIL")
  echo "$m: $http_code"
done
```

**Full capability test (also tests JSON API):**
```bash
for m in libgen.li libgen.rs libgen.is libgen.st; do
  http=$(curl -sI --connect-timeout 5 "https://$m/" -o /dev/null -w "%{http_code}" 2>/dev/null || echo "FAIL")
  json=$(curl -sS --connect-timeout 5 "https://$m/json.php?object=f&ids=1" 2>/dev/null || echo "FAIL")
  # Check if JSON response is valid
  echo "$m -> HTTP:$http JSON:$(echo "$json" | python3 -c "
import sys,json; d=json.load(sys.stdin)
print('OK' if isinstance(d,dict) and '1' in d else 'FAIL')
" 2>/dev/null || echo 'FAIL')"
done
```

## JSON API Details (libgen.li)

### Endpoint
`https://libgen.li/json.php?object=f&ids=FILE_ID1,FILE_ID2,...`

### Parameters
- `object`: table to query. `f` = files table (works). `b` = books table (does NOT accept `ids` param — returns error).
- `ids`: comma-separated file IDs

### Response Format (per file)
```json
{
  "md5": "61edf906ae7bcf0dfe18d1590e8a1740",
  "extension": "epub",
  "filesize": "702648",
  "pages": "0",
  "cover_exists": "1",
  "broken": "N",
  "time_added": "2015-07-05 16:32:31",
  "time_last_modified": "2023-07-01 09:27:59",
  "visible": "",
  "locator": "V:\\path\\to\\file.epub",
  "editions": "",
  "libgen_id": "0",
  "topic": "c"
}
```

### Limitations
- **Does NOT contain** title, author, publisher, year — those are in the `object=b` (books) table which has no JSON API
- **No search endpoint** — `json.php` only accepts `ids=` param, not `req=`
- File IDs are different from edition IDs. Edition ID (`edition.php?id=X`) ≠ file ID (`json.php?object=f&ids=Y`)
- File IDs can be extracted from HTML rows by finding `file.php?id=NUMBER` links

## HTML → ID Extraction (from search results)

### Links found in each HTML search row
| Link pattern | Purpose | Used for |
|---|---|---|
| `edition.php?id=N` | Edition/book details page | Edition ID |
| `author.php?id=N` | Author page | Not directly used |
| `file.php?id=N` | File details page | **File ID** (pass to json.php) |
| `ads.php?md5=HASH` | Download page | MD5 (for download) |

### Quick ID/MD5 extraction
```python
import re

# After getting HTML
row_html = "..."  # single <tr>...</tr> from search results

# Edition ID
ed_id = re.search(r'edition\.php\?id=(\d+)', row_html)

# File ID
file_id = re.search(r'file\.php\?id=(\d+)', row_html)

# MD5
md5 = re.search(r'md5=([a-f0-9]{32})', row_html)

# Author IDs
author_ids = re.findall(r'author\.php\?id=(\d+)', row_html)
```

## UX Presentation Style

When presenting search results to the user, use this format:
```
📖 Results for "query":
1. Title (Author) — Year, format, size, MD5 available
2. ...
```

Keep it compact and scannable. The user prefers agent-presented results over CLI tools for search exploration.

## Tactics Summary

| Goal | Method |
|---|---|
| Find mirrors | Wikidata SPARQL → whereislibgen API → known list → connectivity test |
| Search books | HTML scrape (no JSON search endpoint) |
| Get clean metadata | JSON API enrichment after scraping IDs |
| Download | Extract MD5 → scrape ads.php for get.php URL → curl with -L |
| Preferred format | epub > others; convert if needed (calibre not installed yet) |
| Reading list | Parse `~/Books/reading-list.md`, match against search results |
