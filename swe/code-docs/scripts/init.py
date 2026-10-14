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
    - init.py MAY create a minimal root AGENTS.md (with the essence block) if none exists.
    - init.py also patches/upgrades an existing AGENTS.md that lacks the block.
    - index.py only ever patches/upgrades an existing AGENTS.md, never creates one.
    - The essence block (between docs-essence markers) is idempotent: re-running is a safe no-op.
"""

import sys
from datetime import date
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

DOCS_POINTER_MARKER = "docs/INDEX.md"
DOCS_POINTER_LINE = "> 📚 Canonical docs live in `docs/` — start with `docs/INDEX.md` (then `docs/ROSTER.md` if present)."

# Mirror of scripts/_ontology.py essence block — keep in sync.
# Kept local so init.py has no yaml dependency (see module docstring).
DOCS_ESSENCE_START = "<!-- docs-essence:start -->"
DOCS_ESSENCE_END = "<!-- docs-essence:end -->"
ROOT_ESSENCE_GROUPS = [
    "`docs/overview/` — why: product, users, non-goals · `docs/spec/` — what: behavior, contracts (`features/` per-feature)",
    "`docs/architecture/` — how: structure, components, decisions · `docs/verification/` — evidence: strategy, suites, gaps",
    "`docs/guides/` how-to · `docs/ops/` runbooks · `docs/reference/` glossary+conventions · `docs/resources/` catalogues",
    "`docs/changes/` proposals · `docs/archive/` history · `docs/stories/` memory",
]


def render_root_block() -> str:
    """Render the full root AGENTS.md essence block (markers + pointer + groups)."""
    lines = [DOCS_ESSENCE_START, DOCS_POINTER_LINE]
    lines += [f"> - {g}" for g in ROOT_ESSENCE_GROUPS]
    lines.append(DOCS_ESSENCE_END)
    return "\n".join(lines) + "\n"


def root_essence_state(text: str) -> str:
    """fat = essence block, thin = legacy pointer line, custom = own words, missing = no mention."""
    if DOCS_ESSENCE_START in text and DOCS_ESSENCE_END in text:
        return "fat"
    if DOCS_POINTER_LINE in text:
        return "thin"
    if DOCS_POINTER_MARKER in text:
        return "custom"
    return "missing"


def ensure_root_essence_local(project_root: Path) -> str:
    """Create-or-patch-or-upgrade the root essence block without importing _ontology (no yaml dep)."""
    agents = Path(project_root) / "AGENTS.md"
    block = render_root_block()
    if not agents.exists():
        agents.write_text("# Agent Context\n\n" + block, encoding="utf-8")
        return "created"
    try:
        text = agents.read_text(encoding="utf-8")
    except Exception:
        return "missing"
    state = root_essence_state(text)
    if state == "fat":
        return "ok"
    if state == "thin":
        new = text.replace(DOCS_POINTER_LINE, block.rstrip("\n"), 1)
        if not new.endswith("\n"):
            new += "\n"
        agents.write_text(new, encoding="utf-8")
        return "upgraded"
    if not text.strip():
        agents.write_text(block, encoding="utf-8")
    else:
        agents.write_text(text.rstrip("\n") + "\n\n" + block, encoding="utf-8")
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

    state = ensure_root_essence_local(project)
    if state == "created":
        print("  + AGENTS.md (minimal, with essence block)")
    elif state == "upgraded":
        print("  ✓ AGENTS.md — thin pointer upgraded to essence block")
    elif state == "patched":
        print("  ✓ AGENTS.md — essence block appended")
    else:
        print("  ✓ AGENTS.md — essence block already present")

    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from _ontology import log_operation
        log_operation(docs, "init", "scaffolded docs tree + AGENTS.md pointer")
    except Exception:
        pass
    print("\nDone. Next: run `python scripts/index.py` to build INDEX.md files.")


if __name__ == "__main__":
    main()
