#!/usr/bin/env python3
"""Scaffold a new Power Research folder.

Usage:
    uv run python scripts/init.py <topic-slug> [--mode breadth|balanced|depth]

Creates:
    research/<topic-slug>/
    ├── BRIEF.md
    ├── PLAN.md
    ├── sources/
    ├── topics/
    ├── gaps.md
    └── contradictions.md
"""

import argparse
import shutil
import sys
from datetime import date
from pathlib import Path

# Resolve the skill directory (where this script lives relative to templates/)
SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"


def slugify(name: str) -> str:
    """Convert a name to a filesystem-safe slug."""
    return name.lower().replace(" ", "-").replace("_", "-")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new Power Research folder")
    parser.add_argument("topic", help="Topic name or slug")
    parser.add_argument(
        "--mode",
        choices=["breadth", "balanced", "depth"],
        default="balanced",
        help="Research mode (default: balanced)",
    )
    args = parser.parse_args()

    slug = slugify(args.topic)
    root = Path.cwd() / "research" / slug

    if root.exists():
        print(f"Error: {root} already exists.")
        sys.exit(1)

    # Create directories
    (root / "sources").mkdir(parents=True)
    (root / "topics").mkdir(parents=True)
    print(f"  Created: {root}/")
    print(f"  Created: {root}/sources/")
    print(f"  Created: {root}/topics/")

    # Copy templates
    today = date.today().isoformat()

    template_map = {
        "BRIEF.md": "BRIEF.md",
        "PLAN.md": "PLAN.md",
        "gaps.md": "gaps.md",
        "contradictions.md": "contradictions.md",
    }

    for src_name, dst_name in template_map.items():
        src = TEMPLATES_DIR / src_name
        dst = root / dst_name
        if src.exists():
            shutil.copy2(src, dst)
            # Fill in basic placeholders
            content = dst.read_text(encoding="utf-8")
            content = content.replace("<Topic>", args.topic)
            content = content.replace("<topic>", slug)
            content = content.replace("YYYY-MM-DD", today)
            dst.write_text(content, encoding="utf-8")
            print(f"  Created: {dst}")
        else:
            print(f"  Warning: template not found: {src}")

    print()
    print(f"Done. Research folder ready at: research/{slug}/")
    print()
    print("Next steps:")
    print(f"  1. Edit research/{slug}/BRIEF.md with your research goal")
    print(f"  2. Edit research/{slug}/PLAN.md to add initial search tracks")
    print(f"  3. Run `uv run python scripts/index.py` from research/{slug}/ to build INDEX.md")


if __name__ == "__main__":
    main()
