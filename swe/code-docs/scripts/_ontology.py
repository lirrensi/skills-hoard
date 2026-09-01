"""Shared ontology utilities — frontmatter parsing and doc discovery.

Used by index.py, status.py, and map.py.
Single source of truth for YAML parsing, emoji mapping, and doc walking.
"""

import yaml
from pathlib import Path
from typing import Optional
from datetime import date


STATUS_EMOJI = {
    "active": "🟢",
    "draft": "🟡",
    "deprecated": "🔴",
    "archived": "⚫",
}

LINK_TYPES = {
    "depends_on", "documents", "implemented_by",
    "supersedes", "relates_to", "part_of", "implements",
}


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown text. Returns empty dict if none found or invalid."""
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        result = yaml.safe_load(parts[1])
        return result if isinstance(result, dict) else {}
    except yaml.YAMLError:
        return {}


def read_doc(filepath: Path) -> Optional[dict]:
    """Read a markdown file and return its parsed frontmatter, or None if unreadable."""
    try:
        text = filepath.read_text(encoding="utf-8")
        return parse_frontmatter(text)
    except Exception:
        return None


def walk_docs(root: Path) -> list[tuple[Path, dict]]:
    """Walk docs/ recursively, return sorted list of (filepath, frontmatter). Skips INDEX.md files."""
    results = []
    for f in sorted(root.rglob("*.md")):
        if f.name == "INDEX.md":
            continue
        fm = read_doc(f)
        if fm is not None:
            results.append((f, fm))
    return results


def get_title(filepath: Path, fm: dict) -> str:
    """Extract display title: frontmatter title > filename stem."""
    title = fm.get("title", "")
    if title:
        return title
    return filepath.stem.replace("-", " ").replace("_", " ").title()


def find_project_root(start: Path) -> Optional[Path]:
    """Walk up from start until we find a docs/ folder. Returns project root or None."""
    candidate = start.resolve()
    while candidate != candidate.parent:
        if (candidate / "docs").is_dir():
            return candidate
        candidate = candidate.parent
    return None


def resolve_links(filepath: Path, fm: dict, docs_root: Optional[Path] = None) -> dict[str, list[Path]]:
    """Extract typed links from frontmatter, resolving each path to an absolute target.

    ## Path resolution rules

    A link target is resolved in this order:

    1. **Leading `/`** — absolute. Scope is inferred from the extension:
       - `.md` (or any markdown file) → relative to `docs_root` (so
         `/overview/product.md` is `docs_root/overview/product.md`).
       - anything else (code, configs, etc.) → relative to the project
         root (the parent of `docs_root`). So `/src/auth/index.ts` is
         `project_root/src/auth/index.ts`.
       This is the **recommended** form. It's stable when files are
       moved within their folder, stable when the referrer is moved,
       and works for both docs and code with one syntax.

    2. **Repo-root relative** (no leading `/`, but path starts with a
       known top-level folder like `src/`, `services/`, `infra/`) →
       treated as relative to the project root. Lets you write
       `src/auth/index.ts` from anywhere.

    3. **Docs-root relative** (path starts with a known top-level docs
       folder like `overview/`, `spec/`, `architecture/`, etc.) → treated
       as relative to `docs_root`. Lets you write `overview/product.md`
       from anywhere inside docs/.

    4. **Plain relative** (e.g. `sibling.md`, `./foo.md`) → relative to
       the doc's own directory. The legacy form. Works but is fragile
       on move.

    If `docs_root` is None, the resolver infers it by walking up from
    `filepath` until it finds a folder named `docs`.

    Returns {link_type: [resolved_target_paths]}.
    Handles both string values and lists of strings.
    """
    links = fm.get("links", {})
    if not isinstance(links, dict):
        return {}

    if docs_root is None:
        docs_root = _find_docs_root(filepath)

    project_root = docs_root.parent if docs_root else None
    base = filepath.parent
    resolved = {}
    for link_type, targets in links.items():
        if link_type not in LINK_TYPES:
            continue
        if isinstance(targets, str):
            targets = [targets]
        if not isinstance(targets, list):
            continue
        paths = []
        for t in targets:
            if not isinstance(t, str):
                continue
            target = _resolve_one(t, base, docs_root, project_root)
            if target is not None:
                paths.append(target)
        if paths:
            resolved[link_type] = paths
    return resolved


# Top-level folder names that are conventionally *under* docs/.
_DOCS_TOP_LEVEL = frozenset({
    "overview", "spec", "specs", "architecture", "components",
    "decisions", "verification", "guides", "ops", "reference", "changes", "archive",
    "stories",
})

# Top-level folder names that are conventionally *outside* docs/ (i.e. code).
_CODE_TOP_LEVEL = frozenset({
    "src", "lib", "services", "apps", "packages", "modules",
    "components", "pages", "routes", "api", "internal", "cmd",
    "test", "tests", "scripts", "tools", "bin",
    "infra", "deploy", "k8s", "helm", "terraform",
    "docs",  # yes, sometimes you self-reference
})


def _find_docs_root(start: Path) -> Optional[Path]:
    """Walk up from start until we find a folder named `docs`."""
    candidate = start.resolve() if start.is_dir() else start.parent.resolve()
    while candidate != candidate.parent:
        if candidate.name == "docs" and candidate.is_dir():
            return candidate
        candidate = candidate.parent
    return None


def _resolve_one(href: str, base: Path, docs_root: Optional[Path], project_root: Optional[Path]) -> Optional[Path]:
    """Resolve a single link target to an absolute Path, or None if unresolvable."""
    href = href.strip()
    if not href:
        return None

    # Rule 1: leading `/` — absolute, scope by extension
    if href.startswith("/"):
        body = href.lstrip("/")
        # Drop fragment / query for filesystem lookup
        body = body.split("#", 1)[0].split("?", 1)[0]
        if not body:
            return None
        is_markdown = body.endswith(".md") or body.endswith(".markdown")
        if is_markdown and docs_root is not None:
            return (docs_root / body).resolve()
        if project_root is not None:
            return (project_root / body).resolve()
        # No roots known — fall back to (base / body) for safety
        return (Path("/") / body).resolve() if Path(body).is_absolute() else (Path.cwd() / body).resolve()

    # Strip fragment / query
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return None

    first_segment = clean.split("/", 1)[0]

    # Rule 2: known code top-level → project root
    if first_segment in _CODE_TOP_LEVEL and project_root is not None:
        return (project_root / clean).resolve()

    # Rule 3: known docs top-level → docs root
    if first_segment in _DOCS_TOP_LEVEL and docs_root is not None:
        return (docs_root / clean).resolve()

    # Rule 4: plain relative → doc's own directory (legacy form, still supported)
    return (base / clean).resolve()


def resolve_href(href: str, source_file: Path, docs_root: Optional[Path] = None) -> Optional[Path]:
    """Public helper: resolve a single inline body link or frontmatter href.

    Mirrors `_resolve_one`'s rules. Used by status.py for body links and
    by any future tool that needs to walk a single href.
    """
    if docs_root is None:
        docs_root = _find_docs_root(source_file)
    project_root = docs_root.parent if docs_root else None
    return _resolve_one(href, source_file.parent, docs_root, project_root)


def resolve_links_with_raw(filepath: Path, fm: dict, docs_root: Optional[Path] = None) -> dict[str, list[tuple[Path, str]]]:
    """Like `resolve_links` but also returns the raw href the author wrote.

    Returns {link_type: [(resolved_target_path, raw_href_string), ...]}.

    Useful for tools that need to *display* the original link text
    (e.g. INDEX.md link annotations) rather than a re-serialised path.

    Resolution rules are identical to `resolve_links` — see its docstring.
    """
    links = fm.get("links", {})
    if not isinstance(links, dict):
        return {}

    if docs_root is None:
        docs_root = _find_docs_root(filepath)

    project_root = docs_root.parent if docs_root else None
    base = filepath.parent
    resolved: dict[str, list[tuple[Path, str]]] = {}
    for link_type, targets in links.items():
        if link_type not in LINK_TYPES:
            continue
        if isinstance(targets, str):
            targets = [targets]
        if not isinstance(targets, list):
            continue
        pairs: list[tuple[Path, str]] = []
        for t in targets:
            if not isinstance(t, str):
                continue
            target = _resolve_one(t, base, docs_root, project_root)
            if target is not None:
                pairs.append((target, t))
        if pairs:
            resolved[link_type] = pairs
    return resolved


def is_load_bearing(fm: dict) -> bool:
    """A doc is load-bearing if it has a valid node_type and isn't deprecated/archived."""
    nt = fm.get("node_type", "")
    status = fm.get("status", "active")
    return bool(nt) and status not in ("deprecated", "archived")


def collect_index_links(index_path: Path) -> list[Path]:
    """Parse an INDEX.md to extract which .md files it links to.

    Returns resolved absolute paths for linked markdown files.
    """
    try:
        text = index_path.read_text(encoding="utf-8")
    except Exception:
        return []

    import re
    base = index_path.parent
    targets = []
    # Match markdown links: [text](path.md) or [text](path/INDEX.md)
    for match in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", text):
        href = match.group(2)
        # Resolve relative to the index's directory
        target = (base / href).resolve()
        if target.suffix == ".md" and target != index_path.resolve():
            targets.append(target)
    return targets


def today_str() -> str:
    return date.today().isoformat()


def now_ts() -> str:
    """Return HH:MM timestamp for log entries."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M")


def get_git_commit(project_root: Path) -> Optional[str]:
    """Return the short SHA of the current HEAD commit, or None if git is unavailable.

    Runs `git rev-parse --short HEAD` from the project root.
    Gracefully handles missing git, non-repo directories, and timeouts.
    """
    import subprocess
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None


def get_git_branch(project_root: Path) -> Optional[str]:
    """Return the current branch name, or None if git is unavailable.

    Runs `git rev-parse --abbrev-ref HEAD` from the project root.
    Returns None for detached HEAD (when the command returns "HEAD").
    """
    import subprocess
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            timeout=5,
        )
        branch = result.stdout.strip()
        if result.returncode == 0 and branch and branch != "HEAD":
            return branch
    except Exception:
        pass
    return None


def log_operation(docs_root: Path, operation: str, detail: str = ""):
    """Append a timestamped entry to docs/log.md. Creates the file if needed.

    Usage:
        log_operation(root, "index", "rebuilt 47 docs across 12 folders")
        log_operation(root, "sync", "spec/auth.md — verified, no drift")
        log_operation(root, "curate", "created guides/setup.md")
    """
    log_path = docs_root / "log.md"
    today = today_str()
    ts = now_ts()

    entry = f"- `{ts}` **{operation}** {detail}\n"

    try:
        existing = log_path.read_text(encoding="utf-8")
    except Exception:
        existing = ""

    lines = existing.splitlines()

    # Check if today's heading already exists
    today_header = f"## {today}"
    if today_header in existing:
        # Append to today's section
        new_content = existing.rstrip("\n") + "\n" + entry
    else:
        # Add new day heading
        separator = "\n" if existing and not existing.endswith("\n") else ""
        new_content = existing.rstrip("\n") + separator + f"\n{today_header}\n\n{entry}"

    log_path.write_text(new_content, encoding="utf-8")


def build_graph(docs: list[tuple[Path, dict]], index_files: dict[Path, list[Path]] | None = None) -> dict[Path, list[tuple[Path, str]]]:
    """Build adjacency: doc → list of (target_path, link_type).

    Sources: frontmatter links from all docs, plus INDEX.md links if provided.
    """
    from collections import defaultdict
    graph = defaultdict(list)

    for src_path, fm in docs:
        resolved = resolve_links(src_path, fm)
        for link_type, targets in resolved.items():
            for target in targets:
                graph[src_path.resolve()].append((target, link_type))

    if index_files:
        for index_path, targets in index_files.items():
            for target in targets:
                graph[index_path.resolve()].append((target, "index"))

    return dict(graph)


def build_reverse(graph: dict[Path, list[tuple[Path, str]]]) -> dict[Path, list[tuple[Path, str]]]:
    """Build reverse adjacency: doc → list of (source_path, link_type)."""
    from collections import defaultdict
    rev = defaultdict(list)
    for src, edges in graph.items():
        for target, link_type in edges:
            rev[target].append((src, link_type))
    return dict(rev)
