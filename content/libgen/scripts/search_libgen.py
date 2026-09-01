#!/usr/bin/env python3
"""
libgen-search — Search Library Genesis via libgen.li
Usage: python3 search_libgen.py "query" [limit=10]

Relies on regex against raw HTML from libgen.li.
Note: libgen.li has <br> inside HTML attribute values (invalid HTML),
so no HTML parser can handle it correctly. We use targeted regex.
"""
import sys, json, html as html_mod, re, urllib.request, urllib.parse


def search(query, limit=10):
    """Search LibGen and return structured results directly from raw HTML."""
    url = f"https://libgen.li/index.php?req={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    
    with urllib.request.urlopen(req, timeout=15) as r:
        html_content = r.read().decode("utf-8", errors="replace")
    
    # Strip newlines to simplify regex
    html_content = html_content.replace('\n', ' ').replace('\r', ' ')
    
    # Find the table body
    tbody = re.search(r'<tbody>(.*?)</tbody>', html_content, re.DOTALL)
    if not tbody:
        return []
    
    # Split into individual <tr> blocks
    rows = re.findall(r'<tr>(.*?)</tr>', tbody.group(1), re.DOTALL)
    results = []
    
    for row in rows:
        # Split row into column blocks (raw HTML of each <td>)
        cols = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
        if len(cols) < 8:
            continue
        
        col0 = cols[0]  # title column
        
        # --- Title: find edition.php link ---
        # Match: href="edition.php...">CAPTURE_THIS</a>
        # Among multiple such links, pick the one that's NOT just an ISBN
        title = ""
        for m in re.finditer(r'href="edition\.php[^"]*">(.*?)</a>', col0, re.DOTALL):
            text = m.group(1)
            text = re.sub(r'<[^>]+>', '', text).strip()
            text = html_mod.unescape(text)
            if not re.match(r'^[\d\s;,:]+$', text) and text:
                title = text
                break
        
        # --- MD5 ---
        # MD5 lives in the last column (mirrors badges)
        md5 = None
        for col in cols:
            md5_m = re.search(r'md5=([a-f0-9]{32})', col)
            if md5_m:
                md5 = md5_m.group(1)
                break
        
        # --- Author ---
        author = html_mod.unescape(re.sub(r'<[^>]+>', '', cols[1]).strip())
        
        # --- Publisher ---
        publisher = html_mod.unescape(re.sub(r'<[^>]+>', '', cols[2]).strip())
        
        # --- Year ---
        year_raw = re.sub(r'<[^>]+>', '', cols[3]).strip()
        y_m = re.search(r'(\d{4})', year_raw)
        year = y_m.group(1) if y_m else ""
        
        # --- Language ---
        lang = re.sub(r'<[^>]+>', '', cols[4]).strip()
        
        # --- Pages ---
        pages = re.sub(r'<[^>]+>', '', cols[5]).strip()
        
        # --- Size ---
        size = re.sub(r'<[^>]+>', '', cols[6]).strip()
        
        # --- Format ---
        fmt = re.sub(r'<[^>]+>', '', cols[7]).strip()
        
        results.append({
            'title': title, 'author': author, 'publisher': publisher,
            'year': year, 'language': lang, 'pages': pages,
            'size': size, 'format': fmt, 'md5': md5
        })
        if len(results) >= limit:
            break
    
    return results


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else input("Search: ")
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    results = search(q, limit)
    print(json.dumps(results, indent=2, ensure_ascii=False))
