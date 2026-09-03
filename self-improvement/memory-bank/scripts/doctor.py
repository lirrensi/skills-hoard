#!/usr/bin/env python3
"""Memory health dashboard — counts, inbox, candidates, broken links, age signals.

Borrowed swagger from code-docs `status.py`: read-only reporter, never edits.
Age is a *signal*, not a gate — a month-old file on a monthly project is fresh.

First-attempt run (works with or without pyyaml — fallback parser built in):

    uv run --with pyyaml python skills/memory-bank/scripts/doctor.py --short
    python skills/memory-bank/scripts/doctor.py --short   # plain python also works

Usage:
    python skills/memory-bank/scripts/doctor.py              # full report
    python skills/memory-bank/scripts/doctor.py --short      # summary only
    python skills/memory-bank/scripts/doctor.py ./memory     # explicit path
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

try:
    import yaml  # type: ignore

    def _parse_fm(text: str) -> dict:
        if not text.startswith("---"):
            return {}
        parts = text.split("---", 2)
        if len(parts) < 3:
            return {}
        try:
            data = yaml.safe_load(parts[1])
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

except ImportError:  # fallback: tiny regex parser, no deps
    _KV_RE = re.compile(r"^([A-Za-z_]+):\s*(.*)$")

    def _parse_fm(text: str) -> dict:  # type: ignore[misc]
        if not text.startswith("---"):
            return {}
        parts = text.split("---", 2)
        if len(parts) < 3:
            return {}
        out: dict = {}
        for line in parts[1].splitlines():
            m = _KV_RE.match(line.strip())
            if not m:
                continue
            k, v = m.group(1), m.group(2).strip().strip('"').strip("'")
            if k == "tags":
                v = v.strip("[]")
                out[k] = [t.strip() for t in v.split(",") if t.strip()] if v else []
            elif k == "related":
                v = v.strip("[]")
                out[k] = [t.strip() for t in v.split(",") if t.strip()] if v else []
            else:
                out[k] = v
        return out


def header(text: str) -> str:
    return f"\n  {text}\n  {'─' * len(text)}"


def walk_memories(root: Path) -> list[tuple[Path, dict]]:
    out = []
    for fp in sorted(root.rglob("*.md")):
        name = fp.name.lower()
        if name in ("index.md", "pending.md", "seed.md", "changes.md"):
            continue
        try:
            rel = fp.relative_to(root)
            if rel.parts and rel.parts[0] == "summaries":
                continue
        except ValueError:
            pass
        try:
            fm = _parse_fm(fp.read_text(encoding="utf-8"))
        except Exception:
            continue
        out.append((fp, fm))
    return out


def count_pending(root: Path) -> tuple[int, list[str]]:
    p = root / "pending.md"
    if not p.exists():
        return 0, []
    lines = [ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("- [")]
    return len(lines), lines


def main() -> None:
    short = "--short" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path("./memory").resolve()
    if not root.exists():
        print(f"Error: {root} does not exist. Run init.py first.")
        sys.exit(1)

    docs = walk_memories(root)
    type_counts = Counter(str(fm.get("memory_type", "unknown")).lower() or "unknown" for _, fm in docs)
    status_counts = Counter(str(fm.get("status", "active")).lower() or "active" for _, fm in docs)
    pending_n, pending_lines = count_pending(root)

    candidates = [
        fp for fp, fm in docs
        if str(fm.get("memory_type", "")).lower() == "procedural"
        and str(fm.get("reuse", "once")).lower() == "often"
        and not str(fm.get("skill_ref", "")).strip()
    ]
    promoted = [fp for fp, fm in docs if str(fm.get("skill_ref", "")).strip()]

    untagged = [fp for fp, fm in docs if not fm.get("tags")]
    no_summary = [fp for fp, fm in docs if not str(fm.get("summary", "")).strip()]
    tentative = [fp for fp, fm in docs if str(fm.get("confidence", "")).lower() in ("tentative", "deprecated")]

    # Broken related / skill_ref links — resolve against memory root + project root
    by_name = {fp.name: fp.resolve() for fp, _ in docs}
    broken_related: list[tuple[Path, str]] = []
    broken_skill: list[tuple[Path, str]] = []
    for fp, fm in docs:
        rel = fm.get("related", []) or []
        if isinstance(rel, str):
            rel = [rel]
        for r in rel:
            r = str(r).strip()
            if not r:
                continue
            # filename match OR relative path from memory root
            if Path(r).name in by_name:
                continue
            if (root / r).exists():
                continue
            broken_related.append((fp, r))
        sr = str(fm.get("skill_ref", "")).strip()
        if sr:
            # skill lives outside memory/ — resolve against project root (parent of memory/)
            proj = root.parent
            if not (proj / sr).exists() and not (root / sr).exists() and Path(sr).name not in by_name:
                broken_skill.append((fp, sr))

    # Age buckets — descriptive only. Old != stale on monthly projects.
    ages: list[int] = []
    for _, fm in docs:
        u = str(fm.get("updated", "")).strip()
        if not u:
            continue
        try:
            ages.append((date.today() - date.fromisoformat(u)).days)
        except ValueError:
            pass
    buckets = {
        "0-30": sum(1 for a in ages if a <= 30),
        "31-90": sum(1 for a in ages if 31 <= a <= 90),
        "91-180": sum(1 for a in ages if 91 <= a <= 180),
        "181+": sum(1 for a in ages if a > 180),
    }

    seed_ok = (root / "SEED.md").exists()
    index_p = root / "INDEX.md"
    index_note = "missing — run index.py"
    if index_p.exists() and docs:
        try:
            idx_mtime = index_p.stat().st_mtime
            newest = max(fp.stat().st_mtime for fp, _ in docs)
            index_note = "fresh" if idx_mtime >= newest else "stale — run index.py"
        except OSError:
            pass

    # ── Output ──
    print("\n  MEMORY HEALTH")
    print("  ═════════════")
    print(f"\n  {len(docs)} memories across {len({fp.parent for fp, _ in docs})} folders")
    print("  " + "  ".join(f"{t}: {c}" for t, c in sorted(type_counts.items())))
    print("  " + "  ".join(f"{s}: {c}" for s, c in sorted(status_counts.items())))
    print(f"  pending inbox: {pending_n} line(s)  ·  skill candidates: {len(candidates)}  ·  promoted: {len(promoted)}")
    print(f"  SEED.md: {'✅' if seed_ok else '⚠️ missing (optional bootstrap)'}  ·  INDEX.md: {index_note}")

    if short:
        total = len(untagged) + len(no_summary) + len(broken_related) + len(broken_skill)
        print(f"\n  📋 {total} soft issue(s). Run without --short for detail.\n")
        return

    if pending_n:
        print(header("PENDING INBOX (capture now, judge at learn)"))
        for ln in pending_lines[:10]:
            print(f"     • {ln[:120]}")
        if pending_n > 10:
            print(f"     … +{pending_n - 10} more in pending.md")

    if candidates:
        print(header("SKILL CANDIDATES (reuse: often, no skill_ref)"))
        for fp in candidates:
            print(f"     • {fp.relative_to(root)}")

    issues = bool(untagged or no_summary or tentative or broken_related or broken_skill)
    if issues:
        print(header("SOFT ISSUES (signals, not alarms)"))
    if untagged:
        print(f"\n  ⚠️  {len(untagged)} untagged")
        for fp in untagged[:10]:
            print(f"     • {fp.relative_to(root)}")
    if no_summary:
        print(f"\n  ⚠️  {len(no_summary)} missing summary")
        for fp in no_summary[:10]:
            print(f"     • {fp.relative_to(root)}")
    if tentative:
        print(f"\n  🟡 {len(tentative)} tentative/low-confidence (verify before promoting)")
        for fp in tentative[:10]:
            print(f"     • {fp.relative_to(root)}")
    if broken_related:
        print(f"\n  ❌ {len(broken_related)} broken related link(s)")
        for src, r in broken_related[:10]:
            print(f"     • {src.relative_to(root)} → {r}")
    if broken_skill:
        print(f"\n  ❌ {len(broken_skill)} broken skill_ref(s)")
        for src, r in broken_skill[:10]:
            print(f"     • {src.relative_to(root)} → {r}")

    if ages:
        print(header("AGE DISTRIBUTION (descriptive — old is not stale)"))
        total = max(len(ages), 1)
        for label, count in buckets.items():
            filled = int(round(count / total * 20))
            bar = "▮" * filled + "▯" * (20 - filled)
            print(f"    {label:>7}d  {bar}  {count:>3}")
        print("\n  ℹ️  Monthly-return project? 90d+ is normal. Only")
        print("     `tentative` + old + never-verified deserves a glance.")

    print()
    if not issues and not candidates and pending_n == 0:
        print("  ✨  Quiet bank. Nothing to triage!")
    else:
        print("  📋  Next: `learn` to promote pending, `index.py` to refresh map.")
    print()


if __name__ == "__main__":
    main()
