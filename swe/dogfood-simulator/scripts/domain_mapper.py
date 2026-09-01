#!/usr/bin/env python3
"""
Domain Mapper — Expand a product's capabilities into implied domain verbs.

Given a list of what a product CAN do, this script uses common domain patterns
to suggest what natural actions a user would EXPECT it to also do.

Usage:
    python domain_mapper.py --capabilities "open tab,close tab,navigate" --domain "browser control"
    python domain_mapper.py --from-file capabilities.txt --domain "file management"
"""

import argparse
import sys
from typing import List, Set

# Common lifecycle patterns: if one side exists, the other is often expected
SYMMETRY_PAIRS = [
    ("open", "close"),
    ("start", "stop"),
    ("create", "delete"),
    ("add", "remove"),
    ("import", "export"),
    ("upload", "download"),
    ("connect", "disconnect"),
    ("enable", "disable"),
    ("show", "hide"),
    ("lock", "unlock"),
    ("subscribe", "unsubscribe"),
    ("follow", "unfollow"),
    ("enter", "exit"),
    ("join", "leave"),
    ("push", "pull"),
    ("forward", "back"),
    ("next", "previous"),
    ("maximize", "minimize"),
    ("expand", "collapse"),
    ("activate", "deactivate"),
    ("mount", "unmount"),
    ("install", "uninstall"),
    ("pack", "unpack"),
    ("encode", "decode"),
    ("encrypt", "decrypt"),
    ("serialize", "deserialize"),
    ("compress", "decompress"),
]

# Common bulk/individual patterns: if individual exists, bulk is often expected
BULK_PATTERNS = [
    ("add", "batch add"),
    ("delete", "batch delete"),
    ("update", "batch update"),
    ("create", "bulk create"),
    ("import", "bulk import"),
    ("export", "bulk export"),
    ("send", "mass send"),
    ("apply", "apply to all"),
]

# Common lifecycle stages: products often miss stages in the middle
LIFECYCLE_STAGES = {
    "document": ["create", "draft", "edit", "review", "approve", "publish", "archive", "delete"],
    "user": ["register", "verify", "login", "logout", "update profile", "reset password", "delete account"],
    "item": ["create", "read", "update", "delete", "list", "search", "filter", "sort", "duplicate", "share"],
    "task": ["create", "assign", "start", "pause", "resume", "complete", "cancel", "reopen", "archive"],
    "resource": ["acquire", "configure", "start", "monitor", "scale", "backup", "restore", "release"],
    "message": ["compose", "send", "edit", "delete", "reply", "forward", "archive", "search"],
    "file": ["create", "read", "write", "copy", "move", "rename", "delete", "share", "version"],
    "browser tab": ["open", "close", "switch", "navigate", "back", "forward", "refresh", "duplicate", "pin"],
    "api": ["create key", "revoke key", "rate limit", "monitor", "rotate", "audit"],
    "config": ["read", "set", "unset", "validate", "reload", "reset", "backup", "migrate"],
}

# Common cross-cutting concerns often missed
CROSS_CUTTING = [
    "undo",
    "redo",
    "help",
    "search",
    "filter",
    "sort",
    "preview",
    "history",
    "backup",
    "restore",
    "import",
    "export",
    "share",
    "permissions",
    "settings",
    "customize",
    "template",
    "duplicate",
    "merge",
    "split",
    "compare",
    "diff",
    "sync",
    "clone",
    "migrate",
    "archive",
    "audit log",
    "notifications",
    "keyboard shortcuts",
    "accessibility",
    "dark mode",
    "offline mode",
]


def normalize(text: str) -> str:
    return text.strip().lower()


def expand_symmetry(capabilities: Set[str]) -> List[str]:
    """Find missing symmetric operations."""
    missing = []
    for a, b in SYMMETRY_PAIRS:
        a_present = any(a in cap for cap in capabilities)
        b_present = any(b in cap for cap in capabilities)
        if a_present and not b_present:
            missing.append(f"Missing symmetric: '{b}' (found '{a}')")
        elif b_present and not a_present:
            missing.append(f"Missing symmetric: '{a}' (found '{b}')")
    return missing


def expand_bulk(capabilities: Set[str]) -> List[str]:
    """Find missing bulk operations."""
    missing = []
    for single, bulk in BULK_PATTERNS:
        single_present = any(single in cap and "batch" not in cap and "bulk" not in cap for cap in capabilities)
        bulk_present = any(bulk in cap or (single in cap and ("batch" in cap or "bulk" in cap)) for cap in capabilities)
        if single_present and not bulk_present:
            missing.append(f"Missing bulk: '{bulk}' (found individual '{single}')")
    return missing


def expand_lifecycle(capabilities: Set[str], domain_hint: str = "") -> List[str]:
    """Find missing lifecycle stages."""
    missing = []
    # Try to match domain hint to known lifecycle
    matched_stages = None
    hint = domain_hint.lower()
    for key, stages in LIFECYCLE_STAGES.items():
        if key in hint or any(key in cap for cap in capabilities):
            matched_stages = stages
            break

    if matched_stages:
        for stage in matched_stages:
            if not any(stage in cap for cap in capabilities):
                missing.append(f"Missing lifecycle stage: '{stage}'")

    return missing


def expand_cross_cutting(capabilities: Set[str]) -> List[str]:
    """Find missing cross-cutting concerns."""
    missing = []
    for concern in CROSS_CUTTING:
        if not any(concern in cap for cap in capabilities):
            missing.append(f"Missing cross-cutting: '{concern}'")
    return missing


def main():
    parser = argparse.ArgumentParser(description="Map product capabilities to implied domain verbs")
    parser.add_argument("--capabilities", type=str, help="Comma-separated list of capabilities")
    parser.add_argument("--from-file", type=str, help="File with one capability per line")
    parser.add_argument("--domain", type=str, default="", help="Domain hint (e.g., 'browser control')")
    parser.add_argument("--check-all", action="store_true", help="Run all expansion checks")
    args = parser.parse_args()

    if not args.capabilities and not args.from_file:
        parser.print_help()
        sys.exit(1)

    caps = set()
    if args.capabilities:
        caps.update(normalize(c) for c in args.capabilities.split(","))
    if args.from_file:
        with open(args.from_file, "r", encoding="utf-8") as f:
            caps.update(normalize(line) for line in f if line.strip())

    print(f"Input capabilities ({len(caps)}):")
    for cap in sorted(caps):
        print(f"  - {cap}")
    print()

    print("=== Symmetry Gaps ===")
    for gap in expand_symmetry(caps):
        print(f"  {gap}")
    print()

    print("=== Bulk Operation Gaps ===")
    for gap in expand_bulk(caps):
        print(f"  {gap}")
    print()

    print("=== Lifecycle Gaps ===")
    for gap in expand_lifecycle(caps, args.domain):
        print(f"  {gap}")
    print()

    if args.check_all:
        print("=== Cross-Cutting Concerns ===")
        for gap in expand_cross_cutting(caps):
            print(f"  {gap}")


if __name__ == "__main__":
    main()
