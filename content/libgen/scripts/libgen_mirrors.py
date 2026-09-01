#!/usr/bin/env python3
"""
libgen-mirrors.py — Discover and test LibGen mirrors.

Queries Wikidata for official mirrors, falls back to known list,
health-checks each one from your location, and caches results.

Usage:
  python3 libgen-mirrors.py              # Show cached/known mirrors
  python3 libgen-mirrors.py --discover   # Force fresh discovery
  python3 libgen-mirrors.py --test URL   # Test a specific URL
  python3 libgen-mirrors.py --json       # Output as JSON
  python3 libgen-mirrors.py --best       # Return single best mirror URL
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse

# ─── Known mirrors (fallback if Wikidata fails) ───────────────────────────
KNOWN_MIRRORS = [
    "https://libgen.li",
    "https://libgen.is",
    "https://libgen.rs",
    "https://libgen.st",
]

WIKIDATA_SPARQL = (
    "https://query.wikidata.org/sparql?format=json&query="
    + urllib.parse.quote(
        "SELECT ?urls WHERE {"
        "  { wd:Q22017206 p:P856 [wikibase:rank wikibase:NormalRank; ps:P856 ?urls]. }"
        "}"
    )
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SCRIPT_DIR, "..", "references", "mirrors.json")


def fetch_wikidata_mirrors():
    """Query Wikidata for official LibGen mirror URLs."""
    try:
        req = urllib.request.Request(
            WIKIDATA_SPARQL,
            headers={"User-Agent": "libgen-mirrors/1.0 (portable)"},
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8"))
        urls = [
            b["urls"]["value"]
            for b in data.get("results", {}).get("bindings", [])
        ]
        return urls
    except Exception as e:
        print(f"  [warn] Wikidata query failed: {e}", file=sys.stderr)
        return []


def test_mirror(url):
    """Test if a mirror is reachable and what it supports.

    Returns a dict with capabilities, or None if unreachable.
    """
    result = {
        "url": url.rstrip("/"),
        "reachable": False,
        "has_search": False,
        "has_json_api": False,
        "has_ads": False,
        "latency_ms": None,
        "error": None,
    }

    t0 = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            result["reachable"] = True
            result["latency_ms"] = int((time.time() - t0) * 1000)
    except Exception as e:
        result["error"] = str(e)
        return result

    # Test search endpoint
    search_url = f"{url}/index.php?req=test"
    try:
        req = urllib.request.Request(search_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            html = r.read().decode("utf-8", errors="replace")
            if "tablelibgen" in html or "<tbody>" in html:
                result["has_search"] = True
    except Exception:
        pass

    # Test JSON API
    json_url = f"{url}/json.php?object=f&ids=1"
    try:
        req = urllib.request.Request(json_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode("utf-8"))
            if isinstance(data, dict) and "1" in data:
                result["has_json_api"] = True
    except Exception:
        pass

    # Test ads.php (download pages)
    ads_url = f"{url}/ads.php?md5=00000000000000000000000000000000"
    try:
        req = urllib.request.Request(ads_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            result["has_ads"] = True
    except Exception:
        pass

    return result


def discover():
    """Discover working mirrors from all sources."""
    # Step 1: Wikidata
    wikidata_urls = fetch_wikidata_mirrors()
    if wikidata_urls:
        print(f"  Wikidata: {len(wikidata_urls)} mirror(s) found", file=sys.stderr)
    else:
        print("  Wikidata: no mirrors returned (network or timeout?)", file=sys.stderr)

    # Step 2: Combine with known list (deduplicated)
    all_urls = list(dict.fromkeys(wikidata_urls + KNOWN_MIRRORS))
    print(f"  Testing {len(all_urls)} unique mirror(s)...", file=sys.stderr)

    # Step 3: Test each
    results = []
    for url in all_urls:
        print(f"    {url} ...", end=" ", flush=True, file=sys.stderr)
        r = test_mirror(url)
        status = "✅" if r["reachable"] else "❌"
        extras = []
        if r.get("has_search"):
            extras.append("search")
        if r.get("has_json_api"):
            extras.append("json")
        if r.get("has_ads"):
            extras.append("ads")
        extra_str = f" ({', '.join(extras)})" if extras else ""
        print(f"{status}{extra_str}  {r.get('latency_ms', '?')}ms", file=sys.stderr)
        results.append(r)

    # Step 4: Build registry
    registry = {
        "discovered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources": {"wikidata": wikidata_urls, "known": KNOWN_MIRRORS},
        "mirrors": results,
    }

    # Cache
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(registry, f, indent=2)

    return registry


def load_cache():
    """Load cached mirror list, or None."""
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def get_best_mirror(registry=None):
    """Get the URL of the best working mirror."""
    if registry is None:
        registry = load_cache() or discover()

    working = [
        m for m in registry.get("mirrors", [])
        if m.get("reachable") and m.get("has_search")
    ]
    if not working:
        working = [
            m for m in registry.get("mirrors", [])
            if m.get("reachable")
        ]

    if not working:
        # Last resort: try known list directly
        return KNOWN_MIRRORS[0]

    # Sort by latency (fastest first), then by capability score
    def score(m):
        s = 0
        if m.get("has_json_api"):
            s += 10
        if m.get("has_ads"):
            s += 5
        if m.get("has_search"):
            s += 5
        # Penalize slow latency
        lat = m.get("latency_ms", 9999) or 9999
        return s * 1000 - lat

    working.sort(key=score, reverse=True)
    return working[0]["url"]


# ─── CLI ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Discover and test LibGen mirrors")
    parser.add_argument("--discover", action="store_true", help="Force fresh discovery")
    parser.add_argument("--test", type=str, metavar="URL", help="Test a specific URL")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--best", action="store_true", help="Return single best mirror URL")

    args = parser.parse_args()

    if args.test:
        result = test_mirror(args.test)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            status = "✅" if result["reachable"] else "❌"
            print(f"{args.test} {status} ({result.get('latency_ms','?')}ms)")
        sys.exit(0 if result["reachable"] else 1)

    if args.discover:
        registry = discover()
    else:
        registry = load_cache()
        if not registry:
            print(
                "No cached mirrors found. Running discovery...",
                file=sys.stderr,
            )
            registry = discover()

    if args.best:
        print(get_best_mirror(registry))
    elif args.json:
        print(json.dumps(registry, indent=2))
    else:
        print(f"\nDiscovered: {registry['discovered_at']}")
        print(f"Sources: Wikidata({len(registry['sources']['wikidata'])}) + Known({len(registry['sources']['known'])})")
        print()
        for m in registry["mirrors"]:
            icon = "✅" if m["reachable"] else "❌"
            extras = []
            if m.get("has_search"):
                extras.append("🔍search")
            if m.get("has_json_api"):
                extras.append("📦json")
            if m.get("has_ads"):
                extras.append("⬇️ads")
            extra_str = " ".join(extras) if extras else ""
            lat = f"{m.get('latency_ms', '?')}ms" if m.get('latency_ms') else "?"
            print(f"  {icon} {m['url']:35} {lat:8} {extra_str}")
        print()
        print(f"Best: {get_best_mirror(registry)}")
