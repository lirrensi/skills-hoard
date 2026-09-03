#!/usr/bin/env python3
"""Micro-capture — append-only inbox for use *while working*.

Append a smol bit now, consolidate later via `learn`.
Nothing here is curated — `pending.md` is the inbox, `learn` promotes it.

Usage:
    python skills/memory-bank/scripts/capture.py "fixed auth cookie, was parent-domain" --tags code,auth,gotcha
    python skills/memory-bank/scripts/capture.py "deploy failed: migrate first" --type failure
    python skills/memory-bank/scripts/capture.py "idea: SEED should list blockers" --type idea

Reads nothing, needs no deps, runs in ~50ms.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

MEMORY_DIR = Path("./memory")
PENDING_PATH = MEMORY_DIR / "pending.md"

HEADER = """# Pending Inbox

> Append-only micro-capture. One line per thought, newest at bottom.
> Consolidate via `learn` (end-of-session): promote lines into episodic/semantic/procedural, then delete promoted lines.
> Do not curate here — capture fast, judge later.

"""


def ensure_pending() -> None:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    if not PENDING_PATH.exists():
        PENDING_PATH.write_text(HEADER, encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Append one line to memory/pending.md")
    ap.add_argument("text", help="the smol bit to remember")
    ap.add_argument("--tags", default="", help="comma-separated tags, e.g. code,deploy,gotcha")
    ap.add_argument(
        "--type",
        default="note",
        help="note|failure|idea|fact|todo (just a hint for later triage, default: note)",
    )
    args = ap.parse_args()

    text = (args.text or "").strip()
    if not text:
        print("Error: empty text, nothing captured.", file=sys.stderr)
        sys.exit(1)

    # Single-line it — inbox stays scannable. Newlines become semicolons.
    text = " ".join(text.split())
    tags = ",".join(t.strip().lower().replace(" ", "-") for t in args.tags.split(",") if t.strip())
    kind = args.type.strip().lower() or "note"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tag_suffix = f" #{tags.replace(',', ' #')}" if tags else ""
    line = f"- [{ts}] ({kind}) {text}{tag_suffix}\n"

    ensure_pending()
    with PENDING_PATH.open("a", encoding="utf-8") as f:
        f.write(line)
    print(f"Captured → {PENDING_PATH} ({kind})")


if __name__ == "__main__":
    main()
