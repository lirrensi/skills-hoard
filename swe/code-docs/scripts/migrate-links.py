#!/usr/bin/env python3
"""Migrate relative links in a docs/ folder to the absolute leading-/ form.

Walks every .md file under docs/ (recursively, including INDEX.md),
parses YAML frontmatter, and rewrites link targets in both frontmatter
`links:` and inline body prose from a relative form (../foo.md, ./foo.md,
plain-folder-prefix.md) to the leading-/ absolute form.

The script is **idempotent**: running it twice is a no-op. Files that
already use leading-/ links are skipped. Files with no relative links
are skipped.

Usage:
    python scripts/migrate-links.py docs/                 # rewrite in place
    python scripts/migrate-links.py docs/ --dry-run      # show diffs, no writes
    python scripts/migrate-links.py docs/ --verbose       # show every rewrite

The script NEVER touches:
  - external URLs (http://, https://, mailto:, tel:)
  - pure anchors (#section)
  - non-`.md` paths in body text (images, code files in prose)
  - the `proposal.md` / `behavior.md` / `design.md` sibling pattern
    used inside docs/changes/<name>/ folders (those are intentionally
    doc-relative by template convention)

It DOES rewrite:
  - any `../foo/bar.md` and `./foo/bar.md` in frontmatter `links:` and body prose
  - any `<folder>/<file>.md` pattern in frontmatter `links:` and body prose
    when the first segment is a known top-level docs folder (overview/, spec/,
    etc.) — those become `/<folder>/<file>.md`.
"""

import re
import sys
from pathlib import Path
from collections import defaultdict

from _ontology import (
    parse_frontmatter,
    walk_docs,
    find_project_root,
    _find_docs_root,
    _DOCS_TOP_LEVEL,
    _CODE_TOP_LEVEL,
)


# Link and fence patterns (mirrored from status.py to avoid coupling)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_FENCE_RE = re.compile(r"^\s*```", re.MULTILINE)


# ── Path classification ────────────────────────────────────────────


def classify(href: str) -> str:
    """Classify a link href as one of: external, anchor, code-relative,
    docs-relative, doc-relative, absolute-already, or unknown."""
    if not href:
        return "unknown"
    lowered = href.lower()
    if "://" in lowered or lowered.startswith("mailto:") or lowered.startswith("tel:"):
        return "external"
    if href.startswith("#"):
        return "anchor"
    # Drop query / fragment for classification
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return "anchor"
    if clean.startswith("/"):
        return "absolute-already"
    # Plain relative (./, ../, or just a filename)
    if clean.startswith("./") or clean.startswith("../") or "/" not in clean:
        return "doc-relative"
    first = clean.split("/", 1)[0]
    if first in _CODE_TOP_LEVEL:
        return "code-relative"
    if first in _DOCS_TOP_LEVEL:
        return "docs-relative"
    # Fallback: treat unknown top-level as doc-relative
    return "doc-relative"


def to_absolute(href: str, source_file: Path, docs_root: Path | None, project_root: Path | None) -> str | None:
    """Convert a relative href into the leading-/ absolute form.

    Returns the new href string, or None if no conversion applies.
    Preserves any query/fragment that was on the original.
    """
    cls = classify(href)
    if cls in ("external", "anchor", "absolute-already", "unknown"):
        return None

    # Split off query / fragment
    if "#" in href or "?" in href:
        # Reconstruct carefully
        body = href
        frag = ""
        query = ""
        if "#" in body:
            body, frag = body.split("#", 1)
            frag = "#" + frag
        if "?" in body:
            body, query = body.split("?", 1)
            query = "?" + query
    else:
        body = href
        frag = ""
        query = ""

    if cls == "doc-relative":
        # Resolve relative to the source file's directory
        try:
            resolved = (source_file.parent / body).resolve()
        except Exception:
            return None
        trailing_slash = body.endswith("/")
        # Try docs-root first
        if docs_root is not None:
            try:
                rel = resolved.relative_to(docs_root)
                return "/" + str(rel).replace("\\", "/") + ("/" if trailing_slash else "") + query + frag
            except ValueError:
                pass
        # Fall back: maybe it's a code path that resolves under project root
        if project_root is not None:
            try:
                rel = resolved.relative_to(project_root)
                return "/" + str(rel).replace("\\", "/") + ("/" if trailing_slash else "") + query + frag
            except ValueError:
                pass
        return None

    if cls == "docs-relative":
        # `<folder>/<file>.md` already starts at docs root
        if docs_root is None:
            return None
        # Verify the first segment is a known docs folder
        first = body.split("/", 1)[0]
        if first not in _DOCS_TOP_LEVEL:
            return None
        return "/" + body + query + frag

    if cls == "code-relative":
        # `src/foo/...` already starts at project root
        if project_root is None:
            return None
        first = body.split("/", 1)[0]
        if first not in _CODE_TOP_LEVEL:
            return None
        return "/" + body + query + frag

    return None


# ── File rewriting ────────────────────────────────────────────────


def rewrite_frontmatter_links(text: str, source_file: Path, docs_root: Path | None, project_root: Path | None) -> tuple[str, int]:
    """Rewrite links in YAML frontmatter `links:` block AND the `resource:` field.
    Returns (new_text, count)."""
    if not text.startswith("---"):
        return text, 0
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text, 0
    fm_text = parts[1]
    body = parts[2]

    # We parse links values line-by-line rather than re-serialising the whole YAML
    # to preserve formatting. This is intentionally narrow.
    new_lines = []
    count = 0
    in_links_block = False
    for line in fm_text.splitlines():
        stripped = line.lstrip()

        # Handle `resource:` field — single string value, not a list.
        # Always check this first, regardless of whether we're inside a links
        # block, because `resource:` can legally appear after `links:`.
        m_res = re.match(r"^(\s*)resource:\s*(.+?)\s*$", line)
        if m_res:
            indent, raw_val = m_res.groups()
            # Strip optional surrounding quotes
            val = raw_val.strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            elif val.startswith("'") and val.endswith("'"):
                val = val[1:-1]
            new_val = to_absolute(val, source_file, docs_root, project_root)
            if new_val is not None:
                new_lines.append(f"{indent}resource: {new_val}")
                count += 1
            else:
                new_lines.append(line)
            continue

        if stripped.startswith("links:"):
            in_links_block = True
            new_lines.append(line)
            continue
        if in_links_block:
            # Top-level key (no leading indent, has colon) ends the links block
            if line and not line.startswith((" ", "\t")) and ":" in line and not line.startswith("-"):
                in_links_block = False
            else:
                # Inside a link type entry. Format:
                #   <indent>type: [target, target]
                #   <indent>type:
                #     - target
                m = re.match(r"^(\s*)([a-z_]+):\s*\[(.*)\]\s*$", line)
                if m:
                    indent, link_type, raw = m.groups()
                    targets = [t.strip().strip('"').strip("'") for t in raw.split(",") if t.strip()]
                    new_targets = []
                    changed = False
                    for t in targets:
                        new_t = to_absolute(t, source_file, docs_root, project_root)
                        if new_t is not None:
                            new_targets.append(new_t)
                            changed = True
                            count += 1
                        else:
                            new_targets.append(t)
                    quoted = ", ".join(new_targets)
                    if changed:
                        new_lines.append(f"{indent}{link_type}: [{quoted}]")
                    else:
                        new_lines.append(line)
                    continue
                m2 = re.match(r"^(\s*)- (.+)$", line)
                if m2:
                    indent, raw = m2.groups()
                    t = raw.strip().strip('"').strip("'")
                    new_t = to_absolute(t, source_file, docs_root, project_root)
                    if new_t is not None:
                        new_lines.append(f"{indent}- {new_t}")
                        count += 1
                        continue
        new_lines.append(line)

    if count == 0:
        return text, 0

    new_fm = "\n".join(new_lines)
    return "---\n" + new_fm + "\n---" + body, count


def rewrite_body_links(text: str, source_file: Path, docs_root: Path | None, project_root: Path | None) -> tuple[str, int]:
    """Rewrite inline markdown links in body prose. Returns (new_text, count).

    Preserves the link text and any query/fragment on the href. Skips
    fenced code blocks, frontmatter, and non-`.md` targets.
    """
    if not text.startswith("---"):
        body_full = text
    else:
        parts = text.split("---", 2)
        if len(parts) < 3:
            return text, 0
        body_full = parts[2]

    # We replace inside the body but keep frontmatter untouched.
    frontmatter = text[: len(text) - len(body_full)]

    # Strip code fences to avoid false positives, but remember which lines are fenced
    lines = body_full.splitlines(keepends=True)
    out_lines = []
    in_fence = False
    fence_re = re.compile(r"^\s*```")
    count = 0

    for line in lines:
        if fence_re.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue

        # Find markdown links in this line
        def replace_link(match: re.Match) -> str:
            nonlocal count
            link_text = match.group(1)
            href = match.group(2)
            cls = classify(href)
            if cls not in ("doc-relative", "docs-relative", "code-relative"):
                return match.group(0)
            # Only rewrite .md targets in body (per status.py convention)
            clean = href.split("#", 1)[0].split("?", 1)[0]
            if not (clean.endswith(".md") or clean.endswith(".markdown")):
                return match.group(0)
            new_href = to_absolute(href, source_file, docs_root, project_root)
            if new_href is None:
                return match.group(0)
            count += 1
            return f"[{link_text}]({new_href})"

        out_lines.append(_LINK_RE.sub(replace_link, line))

    if count == 0:
        return text, 0

    new_body = "".join(out_lines)
    return frontmatter + new_body, count


# ── Main ───────────────────────────────────────────────────────────


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print((__doc__ or "").strip())
        sys.exit(0)

    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    args = [a for a in sys.argv[1:] if not a.startswith("--") and not a.startswith("-")]
    if args:
        root = Path(args[0]).resolve()
    else:
        script_dir = Path(__file__).resolve().parent
        project = find_project_root(script_dir)
        root = (project / "docs") if project else (Path.cwd() / "docs")

    if not root.exists():
        print(f"Error: {root} does not exist.")
        sys.exit(1)

    docs_root = root
    project_root = docs_root.parent if docs_root else None

    files_changed = 0
    total_rewrites = 0
    by_type = defaultdict(int)

    # Walk all .md files including INDEX.md (we want consistency)
    md_files = sorted(root.rglob("*.md"))
    for fp in md_files:
        try:
            original = fp.read_text(encoding="utf-8")
        except Exception:
            continue

        new_text, fm_count = rewrite_frontmatter_links(original, fp, docs_root, project_root)
        new_text, body_count = rewrite_body_links(new_text, fp, docs_root, project_root)
        total = fm_count + body_count

        if total == 0:
            continue

        if verbose or dry_run:
            print(f"\n  {fp.relative_to(root)}  ({fm_count} frontmatter, {body_count} body)")

        if not dry_run:
            fp.write_text(new_text, encoding="utf-8")
            files_changed += 1
            total_rewrites += total
        else:
            files_changed += 1
            total_rewrites += total

    print(f"\n  {'DRY RUN — ' if dry_run else ''}Migration complete")
    print(f"  Files touched: {files_changed}")
    print(f"  Total rewrites: {total_rewrites}")
    if dry_run:
        print(f"  Re-run without --dry-run to apply changes.")
    print()


if __name__ == "__main__":
    main()
