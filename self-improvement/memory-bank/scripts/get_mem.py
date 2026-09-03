#!/usr/bin/env python3
"""One command to read it all — condensed bank in ~100 lines.

First-attempt run (works with or without pyyaml — fallback parser built in):

    uv run --with pyyaml python skills/memory-bank/scripts/get_mem.py
    python skills/memory-bank/scripts/get_mem.py   # plain python also works

Usage:
    python skills/memory-bank/scripts/get_mem.py           # ~100 lines, brief
    python skills/memory-bank/scripts/get_mem.py --full    # no truncation
    python skills/memory-bank/scripts/get_mem.py ./memory  # explicit path

Prints: SEED + counts + recent episodic + semantic + procedural +
skill candidates + pending inbox. Full bodies stay lazy — open files after.
"""

from __future__ import annotations

import re
import sys
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

except ImportError:
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
            if k in ("tags", "related"):
                v = v.strip("[]")
                out[k] = [t.strip() for t in v.split(",") if t.strip()] if v else []
            else:
                out[k] = v
        return out


def _load(root: Path) -> list[tuple[Path, dict]]:
    docs = []
    for fp in sorted(root.rglob("*.md")):
        if fp.name.lower() in ("index.md", "pending.md", "seed.md", "changes.md"):
            continue
        try:
            if fp.relative_to(root).parts[0] == "summaries":
                continue
        except ValueError:
            pass
        try:
            docs.append((fp, _parse_fm(fp.read_text(encoding="utf-8"))))
        except Exception:
            pass
    return docs


def _one_line(fp: Path, fm: dict, root: Path) -> str:
    rel = fp.relative_to(root).as_posix()
    summary = str(fm.get("summary", "")).strip().strip('"').strip("'") or "(no summary)"
    flags = ""
    if str(fm.get("status", "active")).lower() != "active":
        flags += f" [{fm.get('status')}]"
    if str(fm.get("memory_type", "")).lower() == "procedural" and str(fm.get("reuse", "")).lower() == "often":
        flags += " [often]"
    if str(fm.get("confidence", "")).lower() in ("tentative", "deprecated"):
        flags += " [?]"
    return f"  - {rel}{flags} — {summary}"


def main() -> None:
    full = "--full" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]).resolve() if args else Path("./memory").resolve()
    if not root.exists():
        print(f"Error: {root} does not exist. Run init.py first.")
        sys.exit(1)

    docs = _load(root)
    by_type: dict[str, list[tuple[Path, dict]]] = {}
    for fp, fm in docs:
        t = str(fm.get("memory_type", "unknown")).lower() or "unknown"
        by_type.setdefault(t, []).append((fp, fm))

    pending_p = root / "pending.md"
    pending = []
    if pending_p.exists():
        pending = [ln.strip() for ln in pending_p.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("- [")]

    candidates = [
        (fp, fm) for fp, fm in docs
        if str(fm.get("memory_type", "")).lower() == "procedural"
        and str(fm.get("reuse", "once")).lower() == "often"
        and not str(fm.get("skill_ref", "")).strip()
    ]

    lines: list[str] = []
    lines.append("# MEM — whole bank, brief")
    # SEED first: the bootstrap is the orientation
    seed_p = root / "SEED.md"
    if seed_p.exists():
        lines.append("")
        lines.append("## SEED (where you left off)")
        seed_lines = seed_p.read_text(encoding="utf-8").splitlines()
        # Strip the header guidance, keep the meat, cap at 30
        meat = [ln for ln in seed_lines if not ln.strip().startswith(">")]
        lines.extend(meat[:30] if not full else meat)

    lines.append("")
    lines.append(f"## MAP — {len(docs)} memories" + (f", {len(pending)} pending" if pending else ""))
    _known = ("episodic", "semantic", "procedural", "decision", "person", "project", "failed_approach", "gotcha", "convention", "external_ref", "unknown")
    _ordered = [t for t in _known if t in by_type] + sorted(t for t in by_type if t not in _known)
    for t in _ordered:
        items = by_type.get(t, [])
        if not items:
            continue
        lines.append(f"  [{t}] {len(items)}")
        # episodic: newest 8 by filename (dated prefix sorts); others: all up to cap
        ordered = sorted(items, key=lambda x: x[0].name, reverse=(t == "episodic"))
        cap = 10**9 if full else (8 if t == "episodic" else 12)
        for fp, fm in ordered[:cap]:
            lines.append(_one_line(fp, fm, root))
        if len(ordered) > cap:
            lines.append(f"    … +{len(ordered) - cap} more, see INDEX.md")

    if candidates and not full:
        lines.append("")
        lines.append(f"## CANDIDATES — {len(candidates)} (reuse: often, no skill yet)")
        for fp, _ in candidates[:5]:
            lines.append(f"  - {fp.relative_to(root).as_posix()}")
    elif candidates:
        lines.append("")
        lines.append("## CANDIDATES")
        for fp, fm in candidates:
            lines.append(_one_line(fp, fm, root))

    if pending:
        lines.append("")
        lines.append(f"## PENDING — {len(pending)} (drain at learn)")
        show = pending if full else pending[-8:]
        for ln in show:
            lines.append(f"  {ln[:140]}")
        if not full and len(pending) > 8:
            lines.append(f"    … +{len(pending) - 8} older, see pending.md")

    lines.append("")
    lines.append("Next: open 2-3 files above for detail. Bodies stay lazy.")

    # Hard cap ~100 lines unless --full
    if not full and len(lines) > 100:
        lines = lines[:97] + ["  …", "  (truncated at ~100 lines — run with --full or open INDEX.md)"]

    print("\n".join(lines))


if __name__ == "__main__":
    main()
