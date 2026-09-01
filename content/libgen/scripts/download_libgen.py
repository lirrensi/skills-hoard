#!/usr/bin/env python3
"""Download a book from LibGen by MD5 hash. Uses curl (more reliable than urllib for CDNs).

Usage: python3 download_libgen.py MD5_HASH output_path

The CDN servers (cdn*.booksdl.lc) are slow and can time out Python's urllib.
curl handles slow connections, retries, and large files more robustly.
"""
import sys, re, subprocess, urllib.request

md5 = sys.argv[1]
out_path = sys.argv[2]

# Step 1: Get download URL from ads.php
ads_url = f"https://libgen.li/ads.php?md5={md5}"
req = urllib.request.Request(ads_url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=15) as r:
    html = r.read().decode("utf-8", errors="replace")

m = re.search(r'href="([^"]*get\.php[^"]*)"', html)
if not m:
    print("ERROR: Could not find download link in ads.php")
    sys.exit(1)

dl_url = "https://libgen.li/" + m.group(1).replace("&amp;", "&")
print(f"Found download URL, fetching via curl...", flush=True)

# Step 2: Download via curl (handles CDN redirects and slow servers better)
result = subprocess.run(
    ["curl", "-L", "-o", out_path, "--connect-timeout", "15",
     "--max-time", "180", "-H", "User-Agent: Mozilla/5.0",
     dl_url],
    capture_output=True, text=True, timeout=200
)

if result.returncode == 0:
    import os
    size = os.path.getsize(out_path)
    print(f"Downloaded {size:,} bytes to {out_path}")
else:
    print(f"curl failed (exit {result.returncode}): {result.stderr}")
    sys.exit(1)
