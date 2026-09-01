#!/usr/bin/env python3
"""Rebuild memory/INDEX.md and compress old episodic memories into weekly/monthly summaries."""

import re
import shutil
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

MEMORY_DIR = Path("./memory")
INDEX_PATH = MEMORY_DIR / "INDEX.md"
EPISODIC_DIR = MEMORY_DIR / "episodic"
ARCHIVE_DIR = MEMORY_DIR / "archive"
WEEKLY_DIR = MEMORY_DIR / "summaries" / "episodic" / "weekly"
MONTHLY_DIR = MEMORY_DIR / "summaries" / "episodic" / "monthly"

TYPE_ORDER = ["episodic", "semantic", "procedural", "decision", "person", "project", "unknown"]
ARCHIVE_DAYS = 7


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


def relative_link(full_path: Path) -> str:
    """Return a relative markdown link from memory root."""
    rel = full_path.relative_to(MEMORY_DIR).as_posix()
    return f"[{full_path.stem}]({rel})"


def gather_memories() -> list[dict]:
    """Walk memory/ and collect metadata from every .md file (except INDEX.md and summaries)."""
    memories = []
    if not MEMORY_DIR.exists():
        return memories

    for path in sorted(MEMORY_DIR.rglob("*.md")):
        if path.name.lower() == "index.md":
            continue
        # Skip auto-generated summaries — they are navigational, not memories
        try:
            rel = path.relative_to(MEMORY_DIR)
            if rel.parts[0] == "summaries":
                continue
        except ValueError:
            pass

        text = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(text)
        memories.append(
            {
                "path": path,
                "meta": meta,
                "body": body,
                "summary": str(meta.get("summary", "")).strip().strip('"').strip("'"),
                "memory_type": str(meta.get("memory_type", "unknown")).lower().strip(),
                "tags": meta.get("tags", []) or [],
                "status": str(meta.get("status", "active")).lower().strip(),
                "updated": str(meta.get("updated", "")),
            }
        )
    return memories


def build_index(memories: list[dict]) -> str:
    """Render INDEX.md content."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Memory Index",
        "",
        f"> Last rebuilt: {now}  ",
        "> Run `python skills/memory-bank/scripts/index.py` to refresh.",
        "",
        "---",
        "",
    ]

    by_type = defaultdict(list)
    for m in memories:
        by_type[m["memory_type"]].append(m)

    lines.append("## Contents")
    lines.append("")
    for t in TYPE_ORDER:
        if t in by_type:
            count = len(by_type[t])
            label = t.capitalize()
            noun = "memory" if count == 1 else "memories"
            lines.append(f"- [{label}](#{label.lower()}) — {count} {noun}")
    lines.append("- [Tag Index](#tag-index)")
    lines.append("")
    lines.append("---")
    lines.append("")

    for t in TYPE_ORDER:
        if t not in by_type:
            continue
        label = t.capitalize()
        lines.append(f"## {label}")
        lines.append("")
        for m in by_type[t]:
            link = relative_link(m["path"])
            summary = m["summary"] or "*No summary*"
            status_badge = ""
            if m["status"] != "active":
                status_badge = f" `[{m['status']}]`"
            updated = f" _updated {m['updated']}_" if m["updated"] else ""
            lines.append(f"- {link}{status_badge} — {summary}{updated}")
        lines.append("")

    tag_map = defaultdict(list)
    for m in memories:
        for tag in m["tags"]:
            tag_map[str(tag)].append(m)

    lines.append("## Tag Index")
    lines.append("")
    if tag_map:
        for tag in sorted(tag_map.keys(), key=str.lower):
            entries = tag_map[tag]
            lines.append(f"### {tag}")
            lines.append("")
            for m in entries:
                link = relative_link(m["path"])
                summary = m["summary"] or "*No summary*"
                lines.append(f"- {link} — {summary}")
            lines.append("")
    else:
        lines.append("_No tags found yet._")
        lines.append("")

    return "\n".join(lines)


# ── Compression helpers ─────────────────────────────────────────────


def parse_date_from_filename(filename: str) -> date | None:
    """Extract YYYY_MM_DD from the start of a filename."""
    match = re.match(r"(\d{4})_(\d{2})_(\d{2})_", filename)
    if match:
        year, month, day = map(int, match.groups())
        return date(year, month, day)
    return None


def iso_week_label(d: date) -> str:
    """Return ISO week string like 2026-W20."""
    cal = d.isocalendar()
    return f"{cal.year}-W{cal.week:02d}"


def week_range(d: date) -> tuple[date, date]:
    """Return (monday, sunday) for the ISO week containing d."""
    monday = d - timedelta(days=d.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday


# ── Weekly compression ──────────────────────────────────────────────


def rebuild_weekly_summary(week_label: str):
    """Rebuild a weekly summary from ALL archived files in that ISO week."""
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    for path in sorted(ARCHIVE_DIR.glob("*.md")):
        file_date = parse_date_from_filename(path.name)
        if not file_date or iso_week_label(file_date) != week_label:
            continue

        text = path.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(text)
        items.append(
            {
                "filename": path.name,
                "date": file_date,
                "summary": str(meta.get("summary", "")).strip().strip('"').strip("'"),
                "status": str(meta.get("status", "active")).lower().strip(),
                "tags": meta.get("tags", []) or [],
            }
        )

    weekly_path = WEEKLY_DIR / f"{week_label}.md"

    if not items:
        if weekly_path.exists():
            weekly_path.unlink()
            print(f"  Removed empty weekly summary: summaries/episodic/weekly/{week_label}.md")
        return

    monday, sunday = week_range(items[0]["date"])
    period = f"{monday} – {sunday}"

    lines = [
        f"# Week {week_label} Summary",
        "",
        f"**Period:** {period}",
        "",
        f"**Memories archived this week:** {len(items)}",
        "",
        "## Archived Memories",
        "",
    ]
    all_tags = set()
    for item in items:
        link = f"[{item['filename']}](../../../archive/{item['filename']})"
        summary = item["summary"] or "*No summary*"
        status = f" `[{item['status']}]`" if item["status"] != "active" else ""
        lines.append(f"- {link}{status} — {summary}")
        all_tags.update(str(t) for t in item["tags"])

    if all_tags:
        lines.append("")
        lines.append("## Tags")
        lines.append("")
        lines.append(", ".join(sorted(all_tags, key=str.lower)))

    weekly_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Rebuilt weekly summary: summaries/episodic/weekly/{week_label}.md ({len(items)} memories)")


def compress_episodic():
    """Move old episodic files to archive/ and rebuild affected weekly summaries."""
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    cutoff = date.today() - timedelta(days=ARCHIVE_DAYS)
    affected_weeks = set()

    if not EPISODIC_DIR.exists():
        return affected_weeks

    for path in sorted(EPISODIC_DIR.glob("*.md")):
        file_date = parse_date_from_filename(path.name)
        if not file_date:
            continue
        if file_date >= cutoff:
            continue

        dest = ARCHIVE_DIR / path.name
        if dest.exists():
            print(f"  Warning: {dest.name} already in archive. Skipping.")
            continue

        shutil.move(str(path), str(dest))
        print(f"  Archived: {path.name} -> archive/")
        affected_weeks.add(iso_week_label(file_date))

    for week in sorted(affected_weeks):
        rebuild_weekly_summary(week)

    # Also refresh any existing weekly summaries that may have stale links
    if WEEKLY_DIR.exists():
        for wpath in WEEKLY_DIR.glob("*.md"):
            week = wpath.stem
            if week not in affected_weeks:
                rebuild_weekly_summary(week)

    return affected_weeks


def rebuild_all_weekly_summaries():
    """Ensure every week represented in archive/ has a fresh weekly summary."""
    all_weeks = set()
    for path in ARCHIVE_DIR.glob("*.md"):
        file_date = parse_date_from_filename(path.name)
        if file_date:
            all_weeks.add(iso_week_label(file_date))
    for week in sorted(all_weeks):
        rebuild_weekly_summary(week)


# ── Monthly compression ─────────────────────────────────────────────


def compress_monthly():
    """Roll completed-month weekly summaries into monthly digests."""
    MONTHLY_DIR.mkdir(parents=True, exist_ok=True)
    if not WEEKLY_DIR.exists():
        return

    weekly_files = sorted(WEEKLY_DIR.glob("*.md"))
    if not weekly_files:
        return

    # Group weeklies by the month they belong to (based on the week's Monday)
    monthly_buckets = defaultdict(list)
    for wpath in weekly_files:
        week_label = wpath.stem
        try:
            year_str, week_str = week_label.split("-W")
            year = int(year_str)
            week_num = int(week_str)
        except ValueError:
            continue

        try:
            monday = date.fromisocalendar(year, week_num, 1)
        except ValueError:
            continue

        month_key = monday.strftime("%Y-%m")
        monthly_buckets[month_key].append(
            {
                "path": wpath,
                "week_label": week_label,
                "monday": monday,
            }
        )

    current_month = date.today().strftime("%Y-%m")

    for month_key, weeklies in monthly_buckets.items():
        if month_key >= current_month:
            # Current month — keep weeklies alive, no monthly digest yet
            continue

        month_path = MONTHLY_DIR / f"{month_key}.md"
        month_name = datetime.strptime(month_key, "%Y-%m").strftime("%B %Y")

        lines = [
            f"# {month_name} Summary",
            "",
            f"**Weekly digests:** {len(weeklies)}",
            "",
            "## Weeks",
            "",
        ]
        for w in sorted(weeklies, key=lambda x: x["monday"]):
            monday, sunday = week_range(w["monday"])
            lines.append(
                f"- [{w['week_label']}](weekly/{w['week_label']}.md) — {monday} – {sunday}"
            )

        month_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(
            f"  Rebuilt monthly summary: summaries/episodic/monthly/{month_key}.md ({len(weeklies)} weeks)"
        )

    # Clean up stale monthly summaries for months that no longer have weeklies
    valid_months = set(monthly_buckets.keys())
    for stale in MONTHLY_DIR.glob("*.md"):
        if stale.stem not in valid_months:
            stale.unlink()
            print(f"  Removed stale monthly summary: summaries/episodic/monthly/{stale.name}")


# ── Main ────────────────────────────────────────────────────────────


def main():
    if not MEMORY_DIR.exists():
        print(f"Error: {MEMORY_DIR} does not exist. Run init.py first.")
        sys.exit(1)

    print("Compressing episodic memories...")
    affected = compress_episodic()
    if affected:
        print(f"  Archived across {len(affected)} week(s)")
    else:
        print("  Nothing to archive")

    print("\nRefreshing weekly summaries...")
    rebuild_all_weekly_summaries()

    print("\nBuilding monthly summaries...")
    compress_monthly()

    print("\nBuilding INDEX.md...")
    memories = gather_memories()
    content = build_index(memories)
    INDEX_PATH.write_text(content, encoding="utf-8")
    print(f"  Rebuilt {INDEX_PATH} ({len(memories)} memories indexed)")

    print("\nDone.")


if __name__ == "__main__":
    main()
