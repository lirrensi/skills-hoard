#!/usr/bin/env python3
"""
Gap Analyzer — Compare implied domain capabilities against actual ones.

Usage:
    python gap_analyzer.py --implied implied.txt --actual actual.txt
    python gap_analyzer.py --implied "open,close,navigate,back,forward" --actual "open,close,navigate"
"""

import argparse
import sys
from typing import List, Set


def parse_capabilities(text: str) -> Set[str]:
    """Parse comma-separated or newline-separated capabilities."""
    items = []
    for line in text.replace(",", "\n").split("\n"):
        line = line.strip().lower()
        if line:
            items.append(line)
    return set(items)


def read_file(path: str) -> Set[str]:
    with open(path, "r", encoding="utf-8") as f:
        return parse_capabilities(f.read())


def fuzzy_match(item: str, candidates: Set[str], threshold: float = 0.6) -> bool:
    """Simple substring-based fuzzy match."""
    item = item.lower()
    for candidate in candidates:
        # Direct substring match
        if item in candidate or candidate in item:
            return True
        # Word overlap
        item_words = set(item.split())
        cand_words = set(candidate.split())
        if item_words and cand_words:
            overlap = len(item_words & cand_words) / max(len(item_words), len(cand_words))
            if overlap >= threshold:
                return True
    return False


def find_gaps(implied: Set[str], actual: Set[str]) -> List[str]:
    """Find implied capabilities that are missing from actual."""
    gaps = []
    for item in sorted(implied):
        if not fuzzy_match(item, actual):
            gaps.append(item)
    return gaps


def find_surprises(implied: Set[str], actual: Set[str]) -> List[str]:
    """Find actual capabilities that weren't implied (might be bloat or hidden gems)."""
    surprises = []
    for item in sorted(actual):
        if not fuzzy_match(item, implied):
            surprises.append(item)
    return surprises


def categorize_gaps(gaps: List[str]) -> dict:
    """Categorize gaps by common pattern keywords."""
    categories = {
        "lifecycle": ["create", "delete", "start", "stop", "open", "close", "begin", "end"],
        "navigation": ["back", "forward", "next", "previous", "up", "down", "home"],
        "bulk": ["batch", "bulk", "mass", "all"],
        "safety": ["undo", "redo", "confirm", "backup", "restore", "recover"],
        "visibility": ["list", "search", "filter", "sort", "view", "find"],
        "config": ["setting", "config", "preference", "customize", "option"],
        "help": ["help", "doc", "tutorial", "guide", "example"],
        "integration": ["import", "export", "share", "sync", "webhook", "api"],
        "other": [],
    }

    result = {k: [] for k in categories}
    for gap in gaps:
        placed = False
        for cat, keywords in categories.items():
            if cat == "other":
                continue
            if any(kw in gap for kw in keywords):
                result[cat].append(gap)
                placed = True
                break
        if not placed:
            result["other"].append(gap)

    return result


def main():
    parser = argparse.ArgumentParser(description="Compare implied vs actual capabilities")
    parser.add_argument("--implied", type=str, required=True, help="Comma-separated or path to file")
    parser.add_argument("--actual", type=str, required=True, help="Comma-separated or path to file")
    args = parser.parse_args()

    # Determine if input is a file path or inline list
    implied = read_file(args.implied) if ".txt" in args.implied or ".md" in args.implied else parse_capabilities(args.implied)
    actual = read_file(args.actual) if ".txt" in args.actual or ".md" in args.actual else parse_capabilities(args.actual)

    print(f"Implied capabilities: {len(implied)}")
    print(f"Actual capabilities: {len(actual)}")
    print()

    gaps = find_gaps(implied, actual)
    print(f"=== GAPS ({len(gaps)} missing) ===")
    if gaps:
        categorized = categorize_gaps(gaps)
        for cat, items in categorized.items():
            if items:
                print(f"\n  [{cat.upper()}]")
                for item in items:
                    print(f"    - {item}")
    else:
        print("  No gaps found!")
    print()

    surprises = find_surprises(implied, actual)
    print(f"=== SURPRISES ({len(surprises)} unexpected) ===")
    if surprises:
        for item in surprises:
            print(f"  - {item}")
    else:
        print("  No surprises — actual set is fully covered by implied set.")
    print()

    coverage = len(actual & implied) / len(implied) * 100 if implied else 100
    print(f"Coverage: {coverage:.1f}% of implied capabilities are present")


if __name__ == "__main__":
    main()
