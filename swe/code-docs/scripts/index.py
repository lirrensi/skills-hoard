#!/usr/bin/env python3
"""Generate INDEX.md files for every folder in docs/.

Scans docs/ recursively, reads YAML frontmatter from each .md file,
and writes an INDEX.md in each folder with:
- Links to every .md file with title + status emoji
- Graph annotations: outgoing links (→) and incoming links (←) per doc
- A generated folder registry with hierarchy and file counts
- A tags section aggregating all tags

Usage:
    python scripts/index.py           # scan docs/ and rebuild all INDEX.md
    python scripts/index.py --dry-run  # show what would be generated
    python scripts/index.py docs/spec  # rebuild only docs/spec/ and below
"""

import sys
from pathlib import Path
from collections import defaultdict

from _ontology import (
    STATUS_EMOJI,
    parse_frontmatter,
    get_title,
    find_project_root,
    resolve_links_with_raw,
    build_reverse,
    log_operation,
    today_str,
    get_git_commit,
    get_git_branch,
)


def display_label_for_doc(target: Path, docs_root: Path) -> str:
    """Display a target doc path as `/path/within/docs/` for human reading.

    Mirrors the absolute-link convention: leading `/` means "absolute,
    scope by extension". For markdown targets, that's docs-root.

    Falls back to a folder-relative path for targets outside docs/ (rare).
    """
    try:
        rel = target.relative_to(docs_root)
        return "/" + str(rel).replace("\\", "/")
    except ValueError:
        # Target is outside docs/ — show the project-relative form
        try:
            rel = target.relative_to(docs_root.parent)
            return "/" + str(rel).replace("\\", "/")
        except ValueError:
            return target.name


def format_links(filepath: Path, docs_root: Path, reverse: dict, all_docs: dict) -> str:
    """Build a multi-line link annotation block for a single document.

    One arrow per line — outgoing (→) first, then incoming (←). Each
    line is indented 2 spaces so it continues the markdown list item
    visually, and you can copy/paste a single edge without snipping
    through a wall of `·` separators.

    For **outgoing** links: displays the raw href the author wrote
    (e.g. "/overview/product.md", "/src/auth/") — never a re-serialised
    relative path. This is the absolute-link convention: the display
    matches what's in the source.

    For **incoming** links: displays the doc path as `/path/within/docs/`
    so the convention is consistent across both directions.

    Returns empty string if no links.
    """
    resolved_fp = filepath.resolve()
    out_links_raw = resolve_links_with_raw(filepath, all_docs.get(resolved_fp, {}))
    in_links = reverse.get(resolved_fp, [])

    if not out_links_raw and not in_links:
        return ""

    parts = []

    # Outgoing: → <raw href> (type)  — uses the author's original text
    for link_type in ["depends_on", "documents", "implements", "supersedes", "relates_to", "part_of", "implemented_by"]:
        targets = out_links_raw.get(link_type, [])
        for resolved_target, raw_href in targets:
            parts.append(f"→ {raw_href} ({link_type})")

    # Incoming: ← <doc path as /abs> (type)
    seen = set()
    for src, link_type in in_links:
        if src == resolved_fp:
            continue
        key = (src, link_type)
        if key in seen:
            continue
        seen.add(key)
        label = display_label_for_doc(src, docs_root)
        parts.append(f"← {label} ({link_type})")

    if not parts:
        return ""

    # One arrow per line, 2-space indent to continue the markdown list item.
    # Leading "\n  " so the first continuation is on its own line, indented
    # to match the rest.
    return "\n  " + "\n  ".join(parts)


def get_summary(filepath: Path, docs_root: Path, reverse: dict, all_docs: dict):
    """Get a one-line summary: title + status emoji, with graph annotations.
    Returns (display_string, tags_set)."""
    try:
        text = filepath.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        title = fm.get("title", "")
        status = fm.get("status", "active")
        emoji = STATUS_EMOJI.get(status, "")
        display = title or filepath.stem.replace("-", " ").replace("_", " ").title()
        if emoji:
            display = f"{display} {emoji}"

        # Build link annotation line
        link_line = format_links(filepath, docs_root, reverse, all_docs)

        tags = set(fm.get("tags", [])) if isinstance(fm.get("tags"), list) else set()
        return display, tags, link_line
    except Exception:
        return filepath.stem, set(), ""


def format_subfolder_entry(folder: Path) -> str:
    """Build the existing navigational subfolder entry."""
    return f"- [{folder.name}/]({folder.name}/INDEX.md)"


def is_indexed_folder(folder: Path) -> bool:
    """Return whether the generator will create an INDEX.md for a folder."""
    if not folder.is_dir():
        return False
    has_docs = any(
        child.is_file() and child.suffix == ".md" and child.name != "INDEX.md"
        for child in folder.iterdir()
        if not child.name.startswith(".")
    )
    has_subfolders = any(
        child.is_dir() and not child.name.startswith(".")
        for child in folder.iterdir()
    )
    return has_docs or has_subfolders


def folder_stats(folder: Path) -> tuple[int, int, int]:
    """Return direct file count, direct folder count, and recursive file count."""
    direct_files = sum(
        1
        for child in folder.iterdir()
        if child.is_file() and child.suffix == ".md" and child.name != "INDEX.md"
    )
    direct_folders = sum(
        1
        for child in folder.iterdir()
        if child.is_dir() and not child.name.startswith(".") and is_indexed_folder(child)
    )
    recursive_files = sum(
        1
        for child in folder.rglob("*.md")
        if child.name != "INDEX.md"
    )
    return direct_files, direct_folders, recursive_files


def format_folder_registry_entry(folder: Path, docs_root: Path, indent: int = 0) -> list[str]:
    """Render one folder and all indexed descendants, without listing files."""
    direct_files, direct_folders, recursive_files = folder_stats(folder)
    relative = folder.relative_to(docs_root)
    label = "docs/" if not relative.parts else f"{relative.as_posix()}/"
    index_state = "INDEX.md"
    prefix = "  " * indent
    lines = [
        f"{prefix}- `{label}` — {direct_files} direct files, "
        f"{direct_folders} direct subfolders, {recursive_files} files recursively; {index_state}"
    ]
    children = sorted(
        (
            child for child in folder.iterdir()
            if child.is_dir() and not child.name.startswith(".") and is_indexed_folder(child)
        ),
        key=lambda path: path.name.lower(),
    )
    for child in children:
        lines.extend(format_folder_registry_entry(child, docs_root, indent + 1))
    return lines


def folder_registry(docs_root: Path) -> list[str]:
    """Build the root index's complete indexed-folder tree."""
    if not is_indexed_folder(docs_root):
        return []
    return format_folder_registry_entry(docs_root, docs_root)


def build_index(folder: Path, docs_root: Path, reverse: dict, all_docs: dict, dry_run: bool = False, git_commit: str | None = None, git_branch: str | None = None) -> tuple[int, int]:
    """Build INDEX.md for a single folder. Returns (files_indexed, tags_found)."""
    if not folder.is_dir():
        return 0, 0

    md_files = sorted([f for f in folder.iterdir() if f.suffix == ".md" and f.name != "INDEX.md"])
    subfolders = sorted([d for d in folder.iterdir() if d.is_dir() and not d.name.startswith(".")])

    if not md_files and not subfolders:
        return 0, 0

    entries = []
    all_tags = set()

    # Document entries with graph annotations
    for f in md_files:
        display, tags, link_line = get_summary(f, docs_root, reverse, all_docs)
        entries.append(f"- [{display}]({f.name})")
        if link_line:
            entries.append(link_line)
        all_tags.update(tags)

    # Subfolder entries remain unchanged; the root registry carries the
    # generated folder tree and counts.
    for d in subfolders:
        entries.append(format_subfolder_entry(d))

    # Build content
    today = today_str()
    folder_name = folder.name if folder.name != "docs" else "Documentation"

    lines = [
        "---",
        "node_type: index",
        f"updated: {today}",
        "---",
        "",
        f"# {folder_name} Index",
        "",
    ]

    if entries:
        if folder.resolve() == docs_root.resolve():
            lines.append("## Folder Registry")
            lines.append("")
            lines.extend(folder_registry(docs_root))
            lines.append("")
        lines.append("## Contents")
        lines.append("")
        lines.extend(entries)
        lines.append("")

    if all_tags:
        tag_list = " ".join(f"`{t}`" for t in sorted(all_tags))
        lines.append("## Tags")
        lines.append("")
        lines.append(tag_list)
        lines.append("")

    # Only the root INDEX.md records the git context — this is the
    # single source of truth for drift detection. Subfolder indexes
    # don't need it and would just create unnecessary diffs.
    if folder.resolve() == docs_root.resolve() and git_commit:
        lines.append("## Git Context")
        lines.append("")
        lines.append(f"- **Commit:** `{git_commit}`")
        if git_branch:
            lines.append(f"- **Branch:** `{git_branch}`")
        lines.append("")

    lines.append("---")
    lines.append(f"*Auto-generated. Last rebuilt: {today}*")
    lines.append("")

    content = "\n".join(lines)

    if dry_run:
        print(f"\n--- {folder / 'INDEX.md'} ---")
        print(content)
    else:
        index_file = folder / "INDEX.md"
        index_file.write_text(content, encoding="utf-8")
        print(f"  ✓ {index_file}")

    return len(md_files), len(all_tags)


def build_all(root: Path, dry_run: bool = False):
    """Walk docs/ and build INDEX.md for every folder.

    Processes deepest folders first (depth-first) so parent INDEX.md
    can link to already-generated child INDEX.md files.
    Also computes the full doc graph so entries show incoming/outgoing links.
    """
    # ── First pass: collect all docs and build the graph ──

    all_docs = {}  # resolved_path → frontmatter
    for f in sorted(root.rglob("*.md")):
        if f.name == "INDEX.md":
            continue
        try:
            text = f.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            all_docs[f.resolve()] = fm
        except Exception:
            pass

    # Build graph + reverse index
    from _ontology import build_graph as bg
    docs_list = [(fp, fm) for fp, fm in all_docs.items()]
    graph = bg(docs_list)
    reverse = build_reverse(graph)

    # ── Second pass: generate indexes with link annotations ──

    # Snapshot the current git commit and branch so the root INDEX.md
    # records exactly when the index was generated.
    git_commit = get_git_commit(root.parent)
    git_branch = get_git_branch(root.parent)

    total_files = 0
    total_folders = 0

    # Collect all folders, including docs/ itself, and sort by depth
    # (deepest first) so the root index is generated last.
    folders = [(0, root)]
    for folder in root.rglob("*"):
        if folder.is_dir() and not folder.name.startswith("."):
            depth = len(folder.relative_to(root).parts)
            folders.append((depth, folder))

    folders.sort(key=lambda x: -x[0])

    for depth, folder in folders:
        files, tags = build_index(folder, root, reverse, all_docs, dry_run=dry_run, git_commit=git_commit, git_branch=git_branch)
        if files > 0 or any(
            d.is_dir() for d in folder.iterdir() if not d.name.startswith(".")
        ):
            total_files += files
            total_folders += 1

    print(f"\nIndexed {total_files} files across {total_folders} folders.")

    if not dry_run:
        detail = f"rebuilt {total_files} docs across {total_folders} folders"
        if git_commit:
            detail += f" (at commit {git_commit})"
        log_operation(root, "index", detail)


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        if __doc__:
            print(__doc__.strip())
        sys.exit(0)

    dry_run = "--dry-run" in sys.argv

    # Determine root
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if args:
        root = Path(args[0]).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        project = find_project_root(script_dir)
        root = (project / "docs") if project else (Path.cwd() / "docs")

    if not root.exists():
        print(f"Error: {root} does not exist. Create docs/ first or specify a path.")
        sys.exit(1)

    mode = "DRY RUN" if dry_run else "BUILDING"
    print(f"{mode} INDEX.md files for {root}/")
    build_all(root, dry_run=dry_run)


if __name__ == "__main__":
    main()
