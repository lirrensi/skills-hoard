#!/usr/bin/env python3
"""Scaffold a docs/ tree and wire the AGENTS.md docs pointer.

Usage:
    python scripts/init.py                  # scaffold ./docs + ensure AGENTS.md pointer
    python scripts/init.py /path/to/project # scaffold elsewhere

Creates:
    docs/{overview,spec,architecture,verification,guides,reference,ops,changes,archive,stories}/
    docs/overview/product.md      (from templates/overview.md)
    docs/verification/strategy.md (from templates/verification.md)

AGENTS.md contract (see SKILL.md):
    - init.py MAY create a minimal root AGENTS.md if none exists.
    - index.py only ever patches an existing AGENTS.md, never creates one.
    - The pointer line is idempotent: re-running is a safe no-op.
"""

import sys
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

DOCS_POINTER_MARKER = "docs/INDEX.md"
DOCS_POINTER_LINE = "> 📚 Canonical docs live in `docs/` — start with `docs/INDEX.md` (then `docs/ROSTER.md` if present)."


def ensure_docs_pointer_local(project_root: Path) -> str:
    """Create-or-patch AGENTS.md pointer without importing _ontology (no yaml dep)."""
    agents = Path(project_root) / "AGENTS.md"
    if not agents.exists():
        agents.write_text("# Agent Context\n\n" + DOCS_POINTER_LINE + "\n", encoding="utf-8")
        return "created"
    try:
        text = agents.read_text(encoding="utf-8")
    except Exception:
        return "missing"
    if DOCS_POINTER_MARKER in text:
        return "ok"
    if not text.strip():
        agents.write_text(DOCS_POINTER_LINE + "\n", encoding="utf-8")
    else:
        agents.write_text(text.rstrip("\n") + "\n\n" + DOCS_POINTER_LINE + "\n", encoding="utf-8")
    return "patched"
FOLDERS = [
    "overview",
    "spec",
    "architecture",
    "verification",
    "guides",
    "reference",
    "ops",
    "changes",
    "archive",
    "stories",
]

STARTERS = {
    "overview/product.md": "overview.md",
    "verification/strategy.md": "verification.md",
}


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__.strip())
        sys.exit(0)
    project = Path(args[0]).resolve() if args else Path.cwd().resolve()
    docs = project / "docs"
    docs.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    for folder in FOLDERS:
        (docs / folder).mkdir(parents=True, exist_ok=True)
        print(f"  + docs/{folder}/")

    for dst_rel, template_name in STARTERS.items():
        dst = docs / dst_rel
        if dst.exists():
            continue
        src = SKILL_DIR / "templates" / template_name
        if not src.exists():
            print(f"  ! template missing: {src}")
            continue
        text = src.read_text(encoding="utf-8").replace("YYYY-MM-DD", today)
        if dst_rel == "verification/strategy.md":
            # Fresh scaffold: /spec + /architecture INDEX.md files don't exist yet
            # (empty folders get no INDEX). Scope starter links to what exists.
            text = text.replace(
                "  depends_on: [/overview/product.md, /spec/INDEX.md, /architecture/INDEX.md]\n  verifies: [/spec/INDEX.md]",
                "  depends_on: [/overview/product.md]",
            )
        dst.write_text(text, encoding="utf-8")
        print(f"  + docs/{dst_rel} (starter)")

    state = ensure_docs_pointer_local(project)
    if state == "created":
        print("  + AGENTS.md (minimal, with docs pointer)")
    elif state == "patched":
        print("  ✓ AGENTS.md — docs pointer appended")
    else:
        print("  ✓ AGENTS.md — docs pointer already present")

    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from _ontology import log_operation
        log_operation(docs, "init", "scaffolded docs tree + AGENTS.md pointer")
    except Exception:
        pass
    print("\nDone. Next: run `python scripts/index.py` to build INDEX.md files.")


if __name__ == "__main__":
    main()
