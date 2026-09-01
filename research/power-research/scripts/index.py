#!/usr/bin/env python3
"""Rebuild INDEX.md by scanning sources/ for YAML frontmatter in markdown files.

Usage:
    uv run python scripts/index.py

Run this after every collection loop iteration, before ending a session,
or whenever sources/ changes meaningfully.
"""

import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: uv pip install pyyaml")
    sys.exit(1)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and remaining body from markdown text."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        data = {}
    return data, match.group(2)


def relative_link(full_path: Path, root: Path) -> str:
    """Return a relative markdown link from the research root."""
    rel = full_path.relative_to(root).as_posix()
    name = full_path.stem
    return f"[{name}]({rel})"


def gather_sources(research_root: Path) -> list[dict]:
    """Walk sources/ and collect metadata from every .md file."""
    sources_dir = research_root / "sources"
    sources = []

    if not sources_dir.exists():
        return sources

    for path in sorted(sources_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)

        # Normalize fields
        summary = str(meta.get("summary", "")).strip().strip('"').strip("'")
        created = str(meta.get("created", "")).strip()
        source_url = str(meta.get("source", "")).strip()
        tags = meta.get("tags", []) or []
        topics = meta.get("topics", []) or []
        confidence = str(meta.get("confidence", "")).strip()
        importance = str(meta.get("importance", "")).strip()

        sources.append({
            "path": path,
            "summary": summary,
            "created": created,
            "source": source_url,
            "tags": [str(t).strip() for t in tags if t],
            "topics": [str(t).strip() for t in topics if t],
            "confidence": confidence,
            "importance": importance,
        })

    return sources


def gather_topic_files(research_root: Path) -> dict[str, list[Path]]:
    """Walk topics/ and group files by topic-slug from filename."""
    topics_dir = research_root / "topics"
    topics: dict[str, list[Path]] = defaultdict(list)

    if not topics_dir.exists():
        return topics

    for path in sorted(topics_dir.glob("*.md")):
        # Extract topic name from slug: "01_overview.md" -> "overview"
        name = path.stem
        # Strip leading numbers like "01_"
        clean = re.sub(r"^\d+_", "", name)
        topics[clean].append(path)

    return topics


def build_index(research_root: Path, sources: list[dict]) -> str:
    """Render INDEX.md content."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    topic_files = gather_topic_files(research_root)

    # Count gaps
    gaps_path = research_root / "gaps.md"
    gap_count = 0
    if gaps_path.exists():
        text = gaps_path.read_text(encoding="utf-8")
        gap_count = text.count("- [ ]")  # Count unchecked items

    lines = [
        "# Research Index",
        "",
        f"> Last rebuilt: {now}  ",
        "> Run `uv run python scripts/index.py` to refresh.",
        "",
        "---",
        "",
    ]

    # ── Quick stats ──
    lines.append("## Quick Stats")
    lines.append("")
    lines.append(f"- **Sources:** {len(sources)}")
    lines.append(f"- **Topics with claims:** {len(topic_files)}")
    lines.append(f"- **Open gaps:** {gap_count}")
    lines.append("")

    # ── Topic coverage ──
    if topic_files:
        lines.append("## Topic Coverage")
        lines.append("")
        for topic_name in sorted(topic_files.keys()):
            files = topic_files[topic_name]
            links = []
            for f in files:
                links.append(relative_link(f, research_root))
            link_str = ", ".join(links)
            count_suffix = f" ({len(files)} file{'s' if len(files) > 1 else ''})"
            lines.append(f"- **{topic_name}**{count_suffix} — {link_str}")
        lines.append("")

    # ── Source catalog ──
    if sources:
        lines.append("## Source Catalog")
        lines.append("")
        lines.append("| Date | Summary | Tags | Topics | Import | Conf |")
        lines.append("|------|---------|------|--------|--------|------|")
        for s in sources:
            link = relative_link(s["path"], research_root)
            date_display = s["created"] or "—"
            summary = s["summary"] or "*No summary*"
            tags_str = ", ".join(f"`{t}`" for t in s["tags"][:5])
            if len(s["tags"]) > 5:
                tags_str += f" +{len(s['tags']) - 5}"
            topics_str = ", ".join(s["topics"][:3])
            if len(s["topics"]) > 3:
                topics_str += f" +{len(s['topics']) - 3}"
            imp = s["importance"] or "—"
            conf = s["confidence"] or "—"
            lines.append(f"| {date_display} | {link} — {summary} | {tags_str} | {topics_str} | {imp} | {conf} |")
        lines.append("")

    # ── Evidence graph (tags as entities) ──
    tag_map: dict[str, list[dict]] = defaultdict(list)
    for s in sources:
        for tag in s["tags"]:
            tag_map[tag].append(s)

    if tag_map:
        lines.append("## Evidence Graph")
        lines.append("")
        lines.append("Tags function as entity nodes. Bridge entities appear in multiple sources;")
        lines.append("singletons appear in one — potential leads for deeper search.")
        lines.append("")

        # Split into bridges (2+ sources) and singletons (1 source)
        bridges = {t: docs for t, docs in tag_map.items() if len(docs) >= 2}
        singletons = {t: docs for t, docs in sorted(tag_map.items(), key=lambda x: x[0].lower()) if len(docs) == 1}

        if bridges:
            lines.append("### Bridge Entities (2+ sources)")
            lines.append("")
            for tag in sorted(bridges.keys(), key=str.lower):
                docs = bridges[tag]
                doc_names = ", ".join(
                    relative_link(d["path"], research_root) for d in docs
                )
                lines.append(f"- **{tag}** — {len(docs)} sources: {doc_names}")
            lines.append("")

        if singletons:
            lines.append("### Singleton Entities (1 source — leads)")
            lines.append("")
            for tag in sorted(singletons.keys(), key=str.lower):
                docs = singletons[tag]
                link = relative_link(docs[0]["path"], research_root)
                summary = docs[0]["summary"] or "*No summary*"
                lines.append(f"- **{tag}** — {link} — {summary}")
            lines.append("")
    else:
        lines.append("## Evidence Graph")
        lines.append("")
        lines.append("_No tags found yet. Add tags to source files to build the evidence graph._")
        lines.append("")

    return "\n".join(lines)


def main():
    cwd = Path.cwd()

    # Determine research root: look for sources/ dir or use cwd
    research_root = cwd
    if not (research_root / "sources").exists():
        print(f"Error: No sources/ directory found in {research_root}")
        print("Run this script from inside a research/<topic-slug>/ directory.")
        sys.exit(1)

    print(f"Scanning {research_root / 'sources'}...")
    sources = gather_sources(research_root)
    print(f"  Found {len(sources)} source file(s)")

    print("Building INDEX.md...")
    content = build_index(research_root, sources)

    index_path = research_root / "INDEX.md"
    index_path.write_text(content + "\n", encoding="utf-8")
    print(f"  Rebuilt {index_path}")

    print("Done.")


if __name__ == "__main__":
    main()
