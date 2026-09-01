#!/usr/bin/env python3
"""Test the compression engine end-to-end: archive moves, weekly/monthly summaries, and INDEX.md."""

import os
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

MEMORY_DIR = Path("./memory")
EPISODIC_DIR = MEMORY_DIR / "episodic"
ARCHIVE_DIR = MEMORY_DIR / "archive"
WEEKLY_DIR = MEMORY_DIR / "summaries" / "episodic" / "weekly"
MONTHLY_DIR = MEMORY_DIR / "summaries" / "episodic" / "monthly"
INDEX_PATH = MEMORY_DIR / "INDEX.md"

TEST_FILES_DIR = Path("./test_files_ephemeral")

passed = 0
failed = 0


def ok(msg: str):
    global passed
    passed += 1
    print(f"  ✅ {msg}")


def no(msg: str):
    global failed
    failed += 1
    print(f"  ❌ {msg}")


# ── Helpers ─────────────────────────────────────────────────────────


def make_episodic(filename: str, summary: str, date_str: str, tags: list[str]):
    """Create an episodic test memory file."""
    content = f"""---
summary: "{summary}"
created: {date_str}
updated: {date_str}
memory_type: episodic
tags: [{', '.join(tags)}]
status: active
---

# Test: {filename}
"""
    path = EPISODIC_DIR / filename
    path.write_text(content, encoding="utf-8")
    return path


def count_files(path: Path) -> int:
    return len(list(path.glob("*.md"))) if path.exists() else 0


def read_or(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def run_index():
    import subprocess
    result = subprocess.run(
        [sys.executable, "skills/memory-bank/scripts/index.py"],
        capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


# ── Tests ────────────────────────────────────────────────────────────


def test_basic_compression():
    """Create 5 episodic files at various ages and verify the pipeline."""
    print("\n━━━ Test: Basic Compression ━━━")
    today = date.today()

    # Files at specific ages
    files = [
        ("2026_05_12_redis_caching.md", "Redis caching layer", str(today - timedelta(days=4)), ["code", "redis"]),
        ("2026_05_08_bug_triage.md", "Bug triage session notes", str(today - timedelta(days=8)), ["code", "debugging"]),
        ("2026_05_06_q2_okr.md", "Q2 OKR planning meeting", str(today - timedelta(days=10)), ["business", "planning"]),
        ("2026_04_28_auth_incident.md", "Auth cookie domain incident", str(today - timedelta(days=18)), ["code", "auth", "incident"]),
        ("2026_04_01_tech_spike.md", "Tech spike on analytics DB", str(today - timedelta(days=45)), ["code", "database"]),
    ]

    for fname, summary, fdate, tags in files:
        make_episodic(fname, summary, fdate, tags)
    print(f"  Created {len(files)} test episodic files")

    # Run the index script
    rc, out, err = run_index()
    if rc != 0:
        no(f"index.py failed: {err}")
        return
    print(f"  index.py ran OK")

    # ── Check episode: active files stayed in episodic/ ──
    active_stems = {p.stem for p in EPISODIC_DIR.glob("*.md")}
    expected_active = {"2026_05_12_redis_caching"}
    actual_active = active_stems & expected_active
    if actual_active == expected_active:
        ok("Recent file stayed in episodic/")
    else:
        no(f"Expected active files {expected_active}, got {actual_active}")

    # ── Check episode: old files moved to archive/ ──
    archive_stems = {p.stem for p in ARCHIVE_DIR.glob("*.md")}
    expected_archived = {"2026_05_08_bug_triage", "2026_05_06_q2_okr", "2026_04_28_auth_incident", "2026_04_01_tech_spike"}
    if expected_archived <= archive_stems:
        ok("All old files moved to archive/")
    else:
        missing = expected_archived - archive_stems
        no(f"Archived files missing: {missing}")

    # ── Check episode: WEEKLY summaries exist ──
    weekly_stems = {p.stem for p in WEEKLY_DIR.glob("*.md")}
    # These files span multiple weeks — verify at least one weekly summary was generated
    if len(weekly_stems) >= 2:
        ok(f"Weekly summaries generated: {', '.join(sorted(weekly_stems))}")
    else:
        no(f"Expected ≥2 weekly summaries, got {len(weekly_stems)}: {weekly_stems}")

    # ── Check episode: MONTHLY summary for older complete months ──
    monthly_stems = {p.stem for p in MONTHLY_DIR.glob("*.md")}
    # We had files in April — there should be at least one monthly for a past month
    if len(monthly_stems) >= 1:
        ok(f"Monthly summaries generated: {', '.join(sorted(monthly_stems))}")
    else:
        no("Expected at least 1 monthly summary")

    # ── Check episode: weekly summary content links ──
    for weekly in WEEKLY_DIR.glob("*.md"):
        content = weekly.read_text(encoding="utf-8")
        # Links should be ../../../archive/...
        if "../../../archive/" not in content:
            no(f"Weekly {weekly.stem}: missing archive link prefix")
            continue
        # Should have at least one archived file linked
        archive_links = re.findall(r"\[.*?\]\(\.\./\.\./\.\./archive/.*?\)", content)
        if len(archive_links) >= 1:
            ok(f"Weekly {weekly.stem}: {len(archive_links)} archived links")
        else:
            no(f"Weekly {weekly.stem}: no archive links found")

    # ── Check episode: monthly summary content links ──
    for monthly in MONTHLY_DIR.glob("*.md"):
        content = monthly.read_text(encoding="utf-8")
        # Should link to weekly files
        weekly_links = re.findall(r"\[.*?\]\(weekly/.*?\)", content)
        if len(weekly_links) >= 1:
            ok(f"Monthly {monthly.stem}: {len(weekly_links)} weekly links")
        else:
            no(f"Monthly {monthly.stem}: no weekly links found")

    # ── Check episode: INDEX.md shows archive/ paths ──
    index_content = INDEX_PATH.read_text(encoding="utf-8")
    archive_in_index = re.findall(r"\[.*?\]\(archive/.*?\)", index_content)
    episodic_in_index = re.findall(r"\[.*?\]\(episodic/.*?\)", index_content)
    archived_count = len(archive_in_index)
    active_count = len(episodic_in_index)
    if archived_count >= 1 and active_count >= 1:
        ok(f"INDEX.md: {archived_count} archive/ + {active_count} episodic/ paths")
    else:
        no(f"INDEX.md paths — archive: {archived_count}, episodic: {active_count}")


def test_idempotency():
    """Running the script twice should not break anything."""
    print("\n━━━ Test: Idempotency ━━━")

    state_before = {
        "episodic": sorted(p.name for p in EPISODIC_DIR.glob("*.md")),
        "archive": sorted(p.name for p in ARCHIVE_DIR.glob("*.md")),
        "weekly": sorted(p.name for p in WEEKLY_DIR.glob("*.md")),
        "monthly": sorted(p.name for p in MONTHLY_DIR.glob("*.md")),
    }

    rc, out, err = run_index()
    if rc != 0:
        no(f"Second run failed: {err}")
        return

    state_after = {
        "episodic": sorted(p.name for p in EPISODIC_DIR.glob("*.md")),
        "archive": sorted(p.name for p in ARCHIVE_DIR.glob("*.md")),
        "weekly": sorted(p.name for p in WEEKLY_DIR.glob("*.md")),
        "monthly": sorted(p.name for p in MONTHLY_DIR.glob("*.md")),
    }

    if state_before == state_after:
        ok("Second run — no duplicate files, no regressions")
    else:
        no("Second run changed state")
        for k in state_before:
            if state_before[k] != state_after[k]:
                print(f"    {k} changed: before={state_before[k]}, after={state_after[k]}")


def test_empty_memory():
    """Run index.py with no files at all — should not crash."""
    print("\n━━━ Test: Empty Memory ━━━")
    rc, out, err = run_index()
    if rc == 0:
        ok("index.py handles empty memory gracefully")
    else:
        no(f"index.py crashed on empty memory: {err}")


def test_cleanup():
    """Remove all test artifacts from memory/."""
    print("\n━━━ Cleanup ━━━")
    for path in list(EPISODIC_DIR.glob("*.md")):
        path.unlink()
    for path in list(ARCHIVE_DIR.glob("*.md")):
        path.unlink()
    for path in list(WEEKLY_DIR.glob("*.md")):
        path.unlink()
    for path in list(MONTHLY_DIR.glob("*.md")):
        path.unlink()
    rc, out, err = run_index()
    if rc == 0:
        ok("Cleanup + index rebuild OK")
    else:
        no(f"Cleanup failed: {err}")


# ── Main ────────────────────────────────────────────────────────────


def main():
    global passed, failed

    print("=" * 50)
    print("memory-bank Compression Test Suite")
    print(f"Date: {date.today()}")
    print("=" * 50)

    test_empty_memory()
    test_basic_compression()
    test_idempotency()
    test_cleanup()
    test_empty_memory()

    print(f"\n{'=' * 50}")
    print(f"Results: {passed} passed, {failed} failed out of {passed + failed} total")
    print(f"{'=' * 50}")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
