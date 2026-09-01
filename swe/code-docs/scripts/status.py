#!/usr/bin/env python3
"""Documentation health dashboard — structural issues, coverage, staleness, freshness.

Usage:
    python scripts/status.py              # full health report
    python scripts/status.py --short       # summary only, no detail
    python scripts/status.py docs/         # specify docs path
"""

import re
import sys
from pathlib import Path
from datetime import date, timedelta
from collections import Counter, defaultdict
from statistics import mean, median

from _ontology import (
    STATUS_EMOJI,
    walk_docs,
    read_doc,
    is_load_bearing,
    resolve_links,
    collect_index_links,
    find_project_root,
    build_graph,
    build_reverse,
    today_str,
)


def status_emoji(status: str) -> str:
    return STATUS_EMOJI.get(status, "")


# ── Report generators ─────────────────────────────────────────────


def header(text: str) -> str:
    return f"\n  {text}\n  {'─' * len(text)}"


def build_index_lookup(index_files: dict[Path, list[Path]]) -> set[Path]:
    """Build a set of all .md files referenced by any INDEX.md."""
    linked = set()
    for targets in index_files.values():
        linked.update(targets)
    return linked


def build_incoming_links(docs: list[tuple[Path, dict]], index_files: dict[Path, list[Path]]) -> dict[Path, list[tuple[Path, str]]]:
    """Build reverse index using shared graph utilities."""
    graph = build_graph(docs, index_files)
    return build_reverse(graph)


def check_orphans(docs: list[tuple[Path, dict]], incoming: dict[Path, list]) -> list[Path]:
    """Find load-bearing docs with no incoming links."""
    orphans = []
    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        resolved = fp.resolve()
        if resolved not in incoming or not incoming[resolved]:
            orphans.append(fp)
    return orphans


def check_broken_links(docs: list[tuple[Path, dict]], index_files: dict[Path, list[Path]]) -> list[tuple[Path, str, Path]]:
    """Find links pointing to non-existent .md files.

    Returns list of (source, link_type, broken_target).

    Only checks targets that are markdown (`.md` / `.markdown`). Code
    targets (TypeScript, Python, etc.) are NOT checked here — those are
    `documents` / `implemented_by` claims about assets, not navigation
    links. Sync mode is the right place to verify code paths.
    """
    broken = []
    all_existing = {fp.resolve() for fp, _ in docs}
    # Also include INDEX.md files as existing
    all_existing.update(idx.resolve() for idx in index_files)

    for src_path, fm in docs:
        resolved = resolve_links(src_path, fm)
        for link_type, targets in resolved.items():
            for target in targets:
                # Only check markdown targets; skip code/data assets
                if target.suffix.lower() not in (".md", ".markdown"):
                    continue
                if target not in all_existing:
                    broken.append((src_path, link_type, target))
    return broken


# ── Inline body link detection ────────────────────────────────────
#
# Walks the markdown BODY (not frontmatter) of every .md file, extracts
# markdown links `[text](href)`, ignores external URLs / anchors / mailto,
# ignores links inside fenced code blocks, and resolves relative paths
# against the doc's own directory. Anything that doesn't exist on disk
# is a broken body link.
#
# Why: frontmatter `links:` is the *typed* graph, but agents and humans
# also write inline links in prose. Those are just as load-bearing and
# need the same orphan/broken treatment.

_FENCE_RE = re.compile(r"^\s*```", re.MULTILINE)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _strip_code_fences(text: str) -> str:
    """Remove fenced code blocks so we don't false-positive on example links."""
    # Walk through, toggle in_fence on ``` boundaries, drop fenced regions.
    out = []
    in_fence = False
    for line in text.splitlines():
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def _strip_frontmatter(text: str) -> str:
    """Return the body of the markdown (everything after the closing ---)."""
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return ""
    return parts[2]


def extract_body_links(filepath: Path, docs_root: Path | None = None) -> list[tuple[Path, str]]:
    """Extract local-file markdown links from a doc's body.

    Returns list of (resolved_target_path, raw_href). External URLs
    (http://, https://, mailto:, etc.) are skipped — we don't probe them.
    Same for pure anchors (#section) and empty hrefs.

    Resolution rules (mirrors _ontology.resolve_href):
      - Leading `/` → absolute, scope by extension (.md → docs_root, else project root)
      - Known top-level docs folder → docs-root relative
      - Plain relative → relative to this doc's directory (legacy)

    The raw_href returned is the EXACT string the author wrote (e.g.
    "/overview/product.md" or "../foo/bar.md") so reports show what the
    doc actually says, not a re-serialised absolute path.
    """
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception:
        return []

    body = _strip_frontmatter(text)
    body = _strip_code_fences(body)

    out: list[tuple[Path, str]] = []
    for match in _LINK_RE.finditer(body):
        href = match.group(2).strip()
        if not href:
            continue
        # Skip non-file schemes
        lowered = href.lower()
        if "://" in lowered or lowered.startswith("mailto:") or lowered.startswith("tel:"):
            continue
        # Skip pure in-page anchors like "#section"
        if href.startswith("#"):
            continue
        # Drop query / fragment for filesystem check
        href_clean = href.split("#", 1)[0].split("?", 1)[0]
        if not href_clean:
            continue
        # We only care about .md links. Code/config links in body are
        # also valid, but their broken-ness is out of scope for status.py
        # (resolve_links + sync handles them). Keep .md focus here.
        if not href_clean.endswith(".md") and not href_clean.endswith(".markdown"):
            continue
        # Resolve using the same rules as the ontology resolver
        target = _resolve_body_href(href_clean, filepath, docs_root)
        if target is not None:
            out.append((target, href))
    return out


def _resolve_body_href(href_clean: str, filepath: Path, docs_root: Path | None) -> Path | None:
    """Resolve a body link href to an absolute Path using the unified rules."""
    # Local import to avoid circular import at module load
    from _ontology import _resolve_one, _find_docs_root
    if docs_root is None:
        docs_root = _find_docs_root(filepath)
    project_root = docs_root.parent if docs_root else None
    return _resolve_one(href_clean, filepath.parent, docs_root, project_root)


def check_broken_body_links(docs: list[tuple[Path, dict]], index_files: dict[Path, list[Path]], docs_root: Path | None = None) -> list[tuple[Path, str, Path]]:
    """Find inline markdown links in body text pointing to non-existent .md files.

    Returns list of (source_doc, raw_href, resolved_target). The raw_href is
    the EXACT string the author wrote (e.g. "/overview/product.md") so reports
    show what the doc actually says, not a re-serialised absolute path."""
    broken: list[tuple[Path, str, Path]] = []
    all_existing = {fp.resolve() for fp, _ in docs}
    all_existing.update(idx.resolve() for idx in index_files)

    for fp, _fm in docs:
        for target, raw in extract_body_links(fp, docs_root=docs_root):
            if target not in all_existing:
                broken.append((fp, raw, target))
    return broken


# ── Broken INDEX.md checker ──────────────────────────────────────
#
# INDEX.md files are auto-generated by index.py, but a hand-edited or
# stale INDEX.md can reference files that no longer exist (or, less
# commonly, omit files that do). We verify every INDEX.md target
# resolves to a real file on disk.

def check_broken_index_links(index_files: dict[Path, list[Path]]) -> list[tuple[Path, Path]]:
    """Find INDEX.md entries pointing to non-existent files.

    Returns list of (index_file, missing_target)."""
    broken: list[tuple[Path, Path]] = []
    for idx_path, targets in index_files.items():
        for target in targets:
            if not target.exists():
                broken.append((idx_path, target))
    return broken


def check_unsynced(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find docs where sync_status is unchecked or absent."""
    unsynced = []
    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        sync = fm.get("sync_status", "")
        if sync in ("", "unchecked"):
            unsynced.append(fp)
    return unsynced


def check_drifted(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find docs where sync_status is drifted."""
    return [fp for fp, fm in docs if fm.get("sync_status") == "drifted"]


def check_untagged(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find load-bearing docs with no tags."""
    return [fp for fp, fm in docs if is_load_bearing(fm) and not fm.get("tags")]


def check_missing_dod(docs: list[tuple[Path, dict]]) -> list[Path]:
    """Find spec docs that might be missing Definition of Done."""
    missing = []
    for fp, fm in docs:
        nt = fm.get("node_type", "")
        if nt != "spec":
            continue
        try:
            text = fp.read_text(encoding="utf-8")
            if "Definition of Done" not in text and "Definition of working" not in text:
                missing.append(fp)
        except Exception:
            pass
    return missing


def check_missing_verification_strategy(root: Path, docs: list[tuple[Path, dict]]) -> bool:
    """Return whether a maintained project lacks a discoverable verification strategy.

    The canonical location is docs/verification/strategy.md. A verification
    node elsewhere is accepted as an explicitly linked equivalent; the audit
    mode can still flag weak discoverability or incomplete content.
    """
    if not any(is_load_bearing(fm) for _, fm in docs):
        return False
    canonical = root / "verification" / "strategy.md"
    if canonical.exists():
        try:
            text = canonical.read_text(encoding="utf-8")
            if "node_type: verification" in text.split("---", 2)[1]:
                return False
        except (OSError, IndexError):
            pass
    return not any(fm.get("node_type") == "verification" for _, fm in docs)


def check_staleness(docs: list[tuple[Path, dict]]) -> tuple[list[tuple[Path, str, int]], Path | None, int]:
    """Return (stale_docs_list, oldest_path, oldest_days). Stale = untouched > 90 days.

    NOTE: This is a *signal*, not a health gate. A 6-month-old doc that is
    still accurate is not "bad." Use this section to spot things that
    might need a glance, not to trigger alarms.
    """
    stale = []
    oldest_path = None
    oldest_days = 0
    cutoff = date.today() - timedelta(days=90)

    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        updated_str = fm.get("updated", "")
        if not updated_str:
            continue
        try:
            d = date.fromisoformat(updated_str)
            days = (date.today() - d).days
            if days > oldest_days:
                oldest_days = days
                oldest_path = fp
            if d < cutoff:
                stale.append((fp, updated_str, days))
        except (ValueError, TypeError):
            pass

    return stale, oldest_path, oldest_days


def layer_coverage(docs: list[tuple[Path, dict]]) -> dict[str, int]:
    """Count load-bearing docs per top-level folder under docs/."""
    coverage = Counter()
    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        # Get top-level folder: docs/overview/... → overview
        parts = fp.parts
        try:
            docs_idx = parts.index("docs")
            if len(parts) > docs_idx + 1:
                top = parts[docs_idx + 1]
                coverage[top] += 1
        except ValueError:
            pass
    return dict(coverage)


# ── Freshness score (informational, NOT an alarm) ────────────────
#
# The freshness score is a single 0–100 number summarising the *signal
# density* of the doc corpus. It is intentionally:
#   - NOT a pass/fail health gate
#   - NOT a "global stale" alarm on day one of a freshly-cloned repo
#   - NOT based on absolute age alone (a 6-month-old overview can be
#     totally accurate; a 2-week-old spec can be totally drifted)
#
# It is built from soft signals:
#   - drift ratio (sync_status: drifted / load-bearing)
#   - broken-link ratio (frontmatter + body links / load-bearing)
#   - untagged ratio (load-bearing with no tags / load-bearing)
#   - missing-DoD ratio (specs without DoD / specs)
#   - orphan ratio (load-bearing with no incoming links / load-bearing)
#   - sync coverage (docs with sync_status: verified / load-bearing)
#
# We weight them, clamp to 0–100, and present the breakdown alongside
# the number. A high score = lots of soft signal noise. A low score =
# quiet, well-typed corpus.

_FRESHNESS_WEIGHTS = {
    "drift_ratio": 25,        # most important: explicit drift
    "broken_link_ratio": 20,  # broken links are loud errors
    "orphan_ratio": 15,       # undiscoverable docs
    "unsynced_ratio": 10,     # never checked
    "missing_dod_ratio": 10,  # specs missing a completion contract
    "untagged_ratio": 5,      # discoverability
    # Sync coverage is a *positive* signal: more verified = better.
    # Implemented below as a small bonus.
}


def compute_freshness(
    docs: list[tuple[Path, dict]],
    drifted: list[Path],
    broken_links: list[tuple[Path, str, Path]],
    broken_body_links: list[tuple[Path, str, Path]],
    orphans: list[Path],
    unsynced: list[Path],
    untagged: list[Path],
    missing_dod: list[Path],
) -> dict:
    """Compute a 0–100 freshness score with a per-signal breakdown.

    Returns a dict with:
      - score: int 0–100 (higher = more noise)
      - signals: dict[str, {"ratio": float 0-1, "count": int, "denom": int, "weight": int}]
      - load_bearing: int
      - tier: "quiet" | "warm" | "noisy" (purely descriptive, not an alarm)
    """
    load_bearing = sum(1 for _, fm in docs if is_load_bearing(fm))
    spec_count = sum(1 for _, fm in docs if fm.get("node_type") == "spec")
    verified_count = sum(1 for _, fm in docs if fm.get("sync_status") == "verified")

    def ratio(n: int, d: int) -> tuple[float, int, int]:
        if d == 0:
            return 0.0, 0, 0
        return n / d, n, d

    drift_r, drift_n, drift_d = ratio(len(drifted), load_bearing)
    bl_r, bl_n, bl_d = ratio(
        len(broken_links) + len(broken_body_links), load_bearing
    )
    orphan_r, orphan_n, orphan_d = ratio(len(orphans), load_bearing)
    unsynced_r, unsynced_n, unsynced_d = ratio(len(unsynced), load_bearing)
    untagged_r, untagged_n, untagged_d = ratio(len(untagged), load_bearing)
    dod_r, dod_n, dod_d = ratio(len(missing_dod), max(spec_count, 1))

    signals = {
        "drift_ratio": {
            "ratio": drift_r,
            "count": drift_n,
            "denom": drift_d,
            "weight": _FRESHNESS_WEIGHTS["drift_ratio"],
            "label": "drifted",
        },
        "broken_link_ratio": {
            "ratio": bl_r,
            "count": bl_n,
            "denom": bl_d,
            "weight": _FRESHNESS_WEIGHTS["broken_link_ratio"],
            "label": "broken links",
        },
        "orphan_ratio": {
            "ratio": orphan_r,
            "count": orphan_n,
            "denom": orphan_d,
            "weight": _FRESHNESS_WEIGHTS["orphan_ratio"],
            "label": "orphans",
        },
        "unsynced_ratio": {
            "ratio": unsynced_r,
            "count": unsynced_n,
            "denom": unsynced_d,
            "weight": _FRESHNESS_WEIGHTS["unsynced_ratio"],
            "label": "unsynced",
        },
        "missing_dod_ratio": {
            "ratio": dod_r,
            "count": dod_n,
            "denom": dod_d,
            "weight": _FRESHNESS_WEIGHTS["missing_dod_ratio"],
            "label": "specs missing DoD",
        },
        "untagged_ratio": {
            "ratio": untagged_r,
            "count": untagged_n,
            "denom": untagged_d,
            "weight": _FRESHNESS_WEIGHTS["untagged_ratio"],
            "label": "untagged",
        },
    }

    # Weighted noise
    noise = sum(sig["ratio"] * sig["weight"] for sig in signals.values())

    # Sync coverage bonus: a small reduction in noise for verified docs.
    # Capped at -5 so it never overwhelms the actual signal.
    if load_bearing > 0:
        coverage = verified_count / load_bearing
        sync_bonus = min(5.0, coverage * 5.0)
    else:
        coverage = 0.0
        sync_bonus = 0.0

    score = max(0, min(100, int(round(noise - sync_bonus))))

    if score < 15:
        tier = "quiet"
    elif score < 40:
        tier = "warm"
    else:
        tier = "noisy"

    return {
        "score": score,
        "tier": tier,
        "load_bearing": load_bearing,
        "verified": verified_count,
        "specs": spec_count,
        "signals": signals,
        "sync_coverage": coverage,
    }


def compute_age_stats(docs: list[tuple[Path, dict]]) -> dict:
    """Compute age statistics for load-bearing docs that have an `updated:` field.

    Returns dict with: count, mean_days, median_days, p90_days, max_days,
    buckets (0-30 / 31-90 / 91-180 / 181-365 / 365+).
    """
    ages: list[int] = []
    for fp, fm in docs:
        if not is_load_bearing(fm):
            continue
        updated_str = fm.get("updated", "")
        if not updated_str:
            continue
        try:
            d = date.fromisoformat(updated_str)
            ages.append((date.today() - d).days)
        except (ValueError, TypeError):
            pass

    if not ages:
        return {
            "count": 0, "mean_days": 0, "median_days": 0, "p90_days": 0,
            "max_days": 0, "buckets": {},
        }

    sorted_ages = sorted(ages)
    p90_idx = max(0, int(len(sorted_ages) * 0.9) - 1)

    buckets = {
        "0-30": sum(1 for a in ages if a <= 30),
        "31-90": sum(1 for a in ages if 31 <= a <= 90),
        "91-180": sum(1 for a in ages if 91 <= a <= 180),
        "181-365": sum(1 for a in ages if 181 <= a <= 365),
        "365+": sum(1 for a in ages if a > 365),
    }

    return {
        "count": len(ages),
        "mean_days": int(mean(ages)),
        "median_days": int(median(ages)),
        "p90_days": sorted_ages[p90_idx],
        "max_days": max(ages),
        "buckets": buckets,
    }


# ── Main ───────────────────────────────────────────────────────────


def main():
    short = "--short" in sys.argv

    # Determine docs root
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        root = Path(args[0]).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        project = find_project_root(script_dir)
        root = (project / "docs") if project else (Path.cwd() / "docs")

    if not root.exists():
        print(f"Error: {root} does not exist.")
        sys.exit(1)

    # Collect data
    docs = walk_docs(root)
    index_files = {
        idx: collect_index_links(idx)
        for idx in sorted(root.rglob("INDEX.md"))
    }
    incoming = build_incoming_links(docs, index_files)

    # Counts
    status_counts = Counter(fm.get("status", "active") for _, fm in docs)
    type_counts = Counter(fm.get("node_type", "?") for _, fm in docs if fm.get("node_type"))
    load_bearing = sum(1 for _, fm in docs if is_load_bearing(fm))

    # Issues
    orphans = check_orphans(docs, incoming)
    broken = check_broken_links(docs, index_files)
    broken_body = check_broken_body_links(docs, index_files, docs_root=root)
    broken_index = check_broken_index_links(index_files)
    unsynced = check_unsynced(docs)
    drifted = check_drifted(docs)
    untagged = check_untagged(docs)
    missing_dod = check_missing_dod(docs)
    missing_verification = check_missing_verification_strategy(root, docs)
    stale, oldest_path, oldest_days = check_staleness(docs)
    coverage = layer_coverage(docs)

    # Freshness + age stats (informational, not errors)
    freshness = compute_freshness(
        docs, drifted, broken, broken_body, orphans, unsynced, untagged, missing_dod
    )
    age_stats = compute_age_stats(docs)

    # ── Output ───────────────────────────────────────────────

    print(f"\n  DOCUMENTATION HEALTH — {today_str()}")
    print(f"  {'═' * 50}")

    # Counts
    print(f"\n  {len(docs)} documents ({load_bearing} load-bearing) across {len(set(fp.parent for fp, _ in docs))} folders")

    status_line = "  ".join(
        f"{status_emoji(s)} {s}: {c}" for s, c in sorted(status_counts.items())
    )
    print(f"  {status_line}")

    if not short:
        type_line = "  ".join(f"{t}: {c}" for t, c in sorted(type_counts.items()))
        print(f"  {type_line}")

    # ── Freshness Dashboard (informational) ─────────────────

    if not short:
        print(header("FRESHNESS"))
        score = freshness["score"]
        tier = freshness["tier"]
        # Visualise: 20-char bar of "█" filled proportional to score
        bar_len = 20
        filled = int(round(score / 100 * bar_len))
        bar = "█" * filled + "░" * (bar_len - filled)
        # Tier emoji (descriptive, not an alarm)
        tier_emoji = {"quiet": "🟢", "warm": "🟡", "noisy": "🔴"}[tier]
        print(f"\n  Score: {score}/100  {tier_emoji} {tier}")
        print(f"  [{bar}]")
        print(f"  {freshness['load_bearing']} load-bearing · {freshness['verified']} verified · {freshness['specs']} specs")
        print(f"  sync coverage: {freshness['sync_coverage'] * 100:.0f}%")
        print()
        print("  Signal breakdown (informational, not a health gate):")
        for name, sig in freshness["signals"].items():
            pct = sig["ratio"] * 100
            # Per-signal bar (5 chars)
            mini_filled = int(round(sig["ratio"] * 5))
            mini_bar = "▮" * mini_filled + "▯" * (5 - mini_filled)
            print(f"    {mini_bar} {sig['label']:<20} {sig['count']:>3}/{sig['denom']:<3}  weight {sig['weight']:>2}")
        print()
        print("  ℹ️  Score weights soft signals (drift, broken links, orphans,")
        print("     untagged, missing DoD, unsynced). Higher = more noise to look")
        print("     at. Pure age is intentionally NOT a signal — a 6-month-old")
        print("     doc that is still accurate is not bad.")

    # ── Structural Issues ────────────────────────────────────

    issues_found = bool(
        orphans
        or broken
        or broken_body
        or broken_index
        or drifted
        or untagged
        or missing_dod
        or missing_verification
    )

    if issues_found:
        print(header("STRUCTURAL ISSUES"))

    if orphans:
        print(f"\n  ❌ {len(orphans)} orphan{'s' if len(orphans) > 1 else ''} (no incoming links)")
        for fp in orphans:
            print(f"     • {fp.relative_to(root)}")

    if broken:
        print(f"\n  ❌ {len(broken)} broken frontmatter link{'s' if len(broken) > 1 else ''}")
        for src, lt, target in broken:
            src_rel = src.relative_to(root)
            target_rel = target.relative_to(root) if target.is_relative_to(root) else str(target)
            print(f"     • {src_rel} → ({lt}) → {target_rel}  (not found)")

    if broken_body:
        print(f"\n  ❌ {len(broken_body)} broken inline body link{'s' if len(broken_body) > 1 else ''}")
        for src, raw, target in broken_body:
            src_rel = src.relative_to(root)
            target_rel = target.relative_to(root) if target.is_relative_to(root) else str(target)
            print(f"     • {src_rel} → {raw}  →  {target_rel}  (not found)")

    if broken_index:
        print(f"\n  ❌ {len(broken_index)} broken INDEX.md entr{'ies' if len(broken_index) > 1 else 'y'}")
        for idx_path, target in broken_index:
            idx_rel = idx_path.relative_to(root)
            target_rel = target.relative_to(root) if target.is_relative_to(root) else str(target)
            print(f"     • {idx_rel} → {target_rel}  (INDEX lists a missing file)")

    if drifted:
        print(f"\n  ⚠️  {len(drifted)} doc{'s' if len(drifted) > 1 else ''} drifted (sync_status: drifted)")
        for fp in drifted:
            print(f"     • {fp.relative_to(root)}")

    if untagged:
        print(f"\n  ⚠️  {len(untagged)} doc{'s' if len(untagged) > 1 else ''} with no tags")
        if not short:
            for fp in untagged:
                print(f"     • {fp.relative_to(root)}")

    if missing_dod:
        print(f"\n  ⚠️  {len(missing_dod)} spec{'s' if len(missing_dod) > 1 else ''} missing Definition of Done")
        if not short:
            for fp in missing_dod:
                print(f"     • {fp.relative_to(root)}")

    if missing_verification:
        print("\n  ⚠️  verification strategy missing or not discoverable")
        print("     • expected docs/verification/strategy.md (node_type: verification)")

    # ── Sync Status ─────────────────────────────────────────

    if unsynced:
        print(header("SYNC STATUS"))
        print(f"\n  ⚠️  {len(unsynced)} doc{'s' if len(unsynced) > 1 else ''} never synced (sync_status: unchecked)")
        if not short:
            for fp in unsynced:
                print(f"     • {fp.relative_to(root)}")

    # ── Staleness (informational, separate from score) ──────

    if oldest_path and not short:
        print(header("AGE DISTRIBUTION"))
        if age_stats["count"] == 0:
            print("\n  No load-bearing docs have an `updated:` date yet.")
        else:
            print(f"\n  {age_stats['count']} load-bearing docs with `updated:` date")
            print(f"  mean age: {age_stats['mean_days']}d  ·  median: {age_stats['median_days']}d  ·  p90: {age_stats['p90_days']}d  ·  max: {age_stats['max_days']}d")
            print()
            b = age_stats["buckets"]
            total = max(age_stats["count"], 1)
            for label, count in b.items():
                pct = count / total * 100
                # 20-char bar for the bucket
                filled = int(round(count / total * 20))
                bar = "▮" * filled + "▯" * (20 - filled)
                print(f"    {label:>8}d  {bar}  {count:>3}  ({pct:>4.0f}%)")
            print()
            print("  ℹ️  This is descriptive, not a health gate. Old docs that are")
            print("     still accurate are fine. Use the FRESHNESS section above")
            print("     to spot signal noise, and glance at the top of the p90")
            print("     bucket if you want a place to start reviewing.")

    # ── Layer Coverage ──────────────────────────────────────

    if coverage:
        print(header("LAYER COVERAGE"))
        expected = {"overview", "spec", "architecture", "verification", "guides", "ops", "reference", "changes", "archive"}
        for layer in sorted(expected | set(coverage.keys())):
            count = coverage.get(layer, 0)
            mark = "✅" if count > 0 else "⚠️ "
            print(f"  {mark}  {layer}/  — {count} doc{'s' if count != 1 else ''}")

    # ── Summary ─────────────────────────────────────────────

    total_issues = (
        len(orphans)
        + len(broken)
        + len(broken_body)
        + len(broken_index)
        + len(drifted)
        + len(untagged)
        + len(unsynced)
        + len(missing_dod)
        + int(missing_verification)
    )
    print()
    if total_issues == 0:
        print("  ✨  No issues found. Docs are healthy!")
    else:
        print(f"  📋  {total_issues} issues to investigate. Run with --short to hide details.")
        print(f"       Freshness score: {freshness['score']}/100 ({freshness['tier']}) — informational only.")
    print()


if __name__ == "__main__":
    main()
