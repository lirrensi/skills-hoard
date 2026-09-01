#!/usr/bin/env python3
"""Validate the curated roster (docs/ROSTER.md by default).

The roster is the hand-maintained map of everything the project has and uses.
Unlike INDEX.md it is NOT auto-generated — it is curated deliberately, and the
rule is: creating a resource REQUIRES adding its roster entry in the same change.

This script enforces that the map stays honest:

  R1. Every roster entry's link resolves to an existing file or directory.
  R2. Every doc with `node_type: resource` appears in the roster.
  R3. The roster file itself has `node_type: roster` in frontmatter.

It does NOT enforce style (one-line summaries, emoji, ordering) — that is
curation judgment. It enforces structure, so the map cannot silently lie.

## Usage

    python scripts/check-roster.py                        # default: docs/ROSTER.md
    python scripts/check-roster.py --roster docs/resources/ROSTER.md
    python scripts/check-roster.py --no-fail              # report only, exit 0
    python scripts/check-roster.py --verbose              # show every entry checked

Exit codes:
    0 — clean (or `--no-fail`)
    1 — violations found
    2 — wrong usage / missing docs folder
"""

import re
import sys
from pathlib import Path

from _ontology import (
    parse_frontmatter,
    find_project_root,
    resolve_href,
    walk_docs,
)

# Roster entry shape: - [Name](/abs/path.md) — one-line summary [🟢 status]
_ENTRY_RE = re.compile(r"^\s*-\s*\[([^\]]+)\]\(([^)]+)\)")


def is_external(href: str) -> bool:
    """True if the href is an external URL (allowed, not existence-checked)."""
    lowered = href.lower()
    return "://" in lowered or lowered.startswith("mailto:") or lowered.startswith("tel:")


def extract_entries(text: str) -> list[tuple[str, str, int]]:
    """Parse roster entries from body text.

    Returns list of (display_name, href, line_number). Skips frontmatter.
    """
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) < 3:
            return []
        body_lines = parts[2].splitlines()
    else:
        body_lines = text.splitlines()

    entries: list[tuple[str, str, int]] = []
    for i, line in enumerate(body_lines, start=1):
        match = _ENTRY_RE.match(line)
        if match:
            name = match.group(1)
            href = match.group(2)
            if name is not None and href is not None:
                entries.append((name.strip(), href.strip(), i))
    return entries


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print((__doc__ or "check-roster — validate the curated roster.").strip())
        sys.exit(0)

    no_fail = "--no-fail" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    args = [a for a in sys.argv[1:] if not a.startswith("--") and not a.startswith("-")]
    docs_root = None
    if args:
        root_arg = Path(args[0]).resolve()
        # Accept either the docs dir itself or the project root
        docs_root = root_arg if root_arg.name == "docs" else (root_arg / "docs")
    else:
        script_dir = Path(__file__).resolve().parent
        project = find_project_root(script_dir)
        docs_root = (project / "docs") if project else (Path.cwd() / "docs")

    if not docs_root or not docs_root.is_dir():
        print(f"Error: docs folder not found at {docs_root}.")
        sys.exit(2)

    # Optional custom roster location
    roster_path = None
    for i, a in enumerate(sys.argv):
        if a == "--roster" and i + 1 < len(sys.argv):
            roster_path = Path(sys.argv[i + 1]).resolve()
            break
    if roster_path is None:
        roster_path = docs_root / "ROSTER.md"

    total_violations = 0
    findings: list[str] = []

    # Discover all resource docs
    resource_docs = [
        (fp, fm) for fp, fm in walk_docs(docs_root) if fm.get("node_type") == "resource"
    ]
    if verbose:
        print(f"  resource docs found: {len(resource_docs)}")

    # ── R3: roster file must exist and be typed roster ──────────────
    if not roster_path.exists():
        if resource_docs:
            findings.append(f"  ❌ roster file missing: {roster_path.relative_to(docs_root.parent)}")
            findings.append(f"       but {len(resource_docs)} resource doc(s) exist — every resource MUST be rostered")
            print()
            print("  Roster check found issues:")
            for f in findings:
                print(f)
            print()
            if no_fail:
                return
            sys.exit(1)
        print(f"  ℹ️  no roster at {roster_path.relative_to(docs_root.parent)} and no resource docs — nothing to roster. Skipped.")
        print()
        return

    try:
        text = roster_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ❌ could not read roster: {e}")
        sys.exit(1)

    fm = parse_frontmatter(text) or {}
    if fm.get("node_type") != "roster":
        total_violations += 1
        findings.append(
            f"  ❌ {roster_path.relative_to(docs_root.parent)} — node_type must be 'roster' (found: {fm.get('node_type', 'missing')})"
        )

    entries = extract_entries(text)
    if verbose:
        print(f"  roster entries parsed: {len(entries)}")

    # ── R1: every entry resolves to an existing target ──────────────
    resolved_targets: set[Path] = set()
    for name, href, line in entries:
        if is_external(href):
            if verbose:
                print(f"  ✓ line {line}: {name} → {href}  (external, skipped)")
            continue
        target = resolve_href(href, roster_path, docs_root)
        if target is None or not target.exists():
            total_violations += 1
            findings.append(f"  ❌ line {line}: '{name}' → {href}  (broken: target not found)")
        else:
            resolved_targets.add(target.resolve())
            if verbose:
                print(f"  ✓ line {line}: {name} → {target.relative_to(docs_root.parent)}")

    # ── R2: every resource doc must be rostered ─────────────────────
    for fp, rfm in resource_docs:
        if fp.resolve() not in resolved_targets:
            total_violations += 1
            rel = fp.relative_to(docs_root)
            findings.append(f"  ❌ resource not rostered: {rel} — add it to {roster_path.name}")

    # ── Summary ─────────────────────────────────────────────────────
    print()
    if findings:
        print("  Roster check found issues:")
        for f in findings:
            print(f)
    else:
        print(f"  ✅ Roster clean: {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}, "
              f"{len(resource_docs)} resource doc{'s' if len(resource_docs) != 1 else ''} all covered.")
    print()

    if total_violations > 0 and not no_fail:
        sys.exit(1)


if __name__ == "__main__":
    main()