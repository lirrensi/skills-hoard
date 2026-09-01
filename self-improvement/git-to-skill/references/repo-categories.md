# Repository Categories

Taxonomy of project types with detection heuristics. Used in Phase 1 (Scout & Recon)
to determine the extraction strategy for Phase 3.

---

## Category Tree

```
Any Repo
├── 1. CLI Tool         → Has CLI entry point, exposes commands
├── 2. Library          → Importable API, no standalone entry point
├── 3. Application      → Runs as a service, has config + deploy
├── 4. Monorepo         → Multiple independent packages
├── 5. Template         → Scaffolding / boilerplate generator
├── 6. Config/Dotfile   → User configuration (rc files, editor config)
├── 7. Plugin/Extension → Extends another tool (VS Code, neovim, etc.)
├── 8. Documentation    → Mostly markdown, minimal code
└── 9. Unknown          → Fallback: structural extraction only
```

---

## Detection Heuristics

### 1. CLI Tool

**Primary signals (any one is enough):**
- `package.json` has a `bin` field (object or string)
- `pyproject.toml` has `[project.scripts]` or `[tool.poetry.scripts]`
- `setup.py` / `setup.cfg` has `entry_points={"console_scripts": [...]}`
- `Cargo.toml` has `[[bin]]` section
- Top-level `main.go` / `cmd/` directory with `main.go`
- `cli.py`, `__main__.py` at package root
- `bin/` directory at repo root with executable scripts
- `Makefile` installs to a `bin/` directory

**Secondary signals:**
- README shows `$ <name> <command>` style examples
- Repository name matches an installable binary
- Has man pages (`man/`) or shell completions (`completions/`)

**Extraction strategy:** See `cli-extraction.md`

---

### 2. Library

**Primary signals:**
- `package.json` has no `bin` field but has `main` / `exports`
- `pyproject.toml` without `[project.scripts]` but with `[project.entry-points]`
- `Cargo.toml` has `[lib]` section without `[[bin]]`
- `go.mod` with package name that doesn't contain `cmd/`
- `src/lib.rs`, `src/index.ts`, `src/<name>.py` as main entry

**Secondary signals:**
- README shows `import <name>` or `require('<name>')` examples
- Has API documentation (typedoc, sphinx, rustdoc configs)
- Contains `__init__.py` at root
- Test files import the package

**Extraction strategy:** See `library-extraction.md`

---

### 3. Application

**Primary signals:**
- Has `Dockerfile` and/or `docker-compose.yml`
- Contains `config/` or `config.yaml` / `config.json` at root
- Has `.env.example` or `.env.sample`
- Contains `server.js`, `app.py`, `main.go`, `main.rs` at root or `cmd/`
- Has `Procfile`, `fly.toml`, `render.yaml`, `vercel.json`, `netlify.toml`
- Has `systemd/` unit files

**Secondary signals:**
- README mentions deployment, hosting, or infrastructure
- Has database migration files (`migrations/`, `alembic/`, `prisma/`)
- Contains health check endpoints or monitoring config
- Has `docker/` or `deploy/` directory

**Extraction strategy:** See `general-extraction.md`

---

### 4. Monorepo

**Primary signals:**
- `package.json` at root with `workspaces` field
- `pnpm-workspace.yaml` exists
- `lerna.json` exists
- `turbo.json` exists
- `nix` flake with multiple outputs
- `Cargo.toml` with `[workspace]` section
- `go.work` file exists
- Multiple packages/ directories (`packages/`, `apps/`, `libs/`, `modules/`)

**Secondary signals:**
- More than one `package.json` / `Cargo.toml` / `pyproject.toml` in subdirectories
- README mentions "monorepo" or "workspace"

**Extraction strategy:** Recurse into each sub-package. Generate a parent skill
that delegates to sub-skills or includes per-package reference files.

---

### 5. Template / Boilerplate

**Primary signals:**
- `cookiecutter.json` exists
- Has template variables (`{{ }}`, `<% %>`, `${ }`) in files
- README describes itself as a template or starter
- Has `template/` or `scaffold/` directory
- `package.json` has a `create-` prefix name

**Secondary signals:**
- Has `answers.json`, `prompts.json`, or `.template.json`
- Minimal source code, heavy on placeholder content

**Extraction strategy:**
- List all customizable variables and their defaults
- Document the scaffolding command or process
- Generate a skill that guides the user through creating a new project from the template

---

### 6. Config / Dotfiles

**Primary signals:**
- Top-level files like `.zshrc`, `.bashrc`, `.vimrc`, `.gitconfig`, `.tmux.conf`
- Directory names like `dotfiles/`, `config/`, `settings/`
- Has install script linking configs to `$HOME`

**Secondary signals:**
- README says "my dotfiles" or "personal config"
- Has `Brewfile`, `setup.sh`, `bootstrap.sh`

**Extraction strategy:**
- Document each config file's purpose and available options
- Generate a skill that can install / update the configs
- Include bootstrap instructions

---

### 7. Plugin / Extension

**Primary signals:**
- `package.json` has `"vscode:prepublish"` or `"extensionDependencies"`
- Has `plugin.json`, `extension.json`, `manifest.json` for extension metadata
- Directory structure matches known plugin patterns:
  - VS Code: `.vscode/`, `extension.js`
  - Neovim: `plugin/`, `lua/` with `nvim` imports
  - Obsidian: `manifest.json` with `minAppVersion`
  - Chrome/Firefox: `manifest.json` at root
  - IntelliJ: `META-INF/plugin.xml`
- README says "plugin for" or "extension for"

**Secondary signals:**
- Depends on a parent tool's API (vscode types, discord.py, jupyter)
- Has screenshots/gallery in README

**Extraction strategy:**
- Document installation method (marketplace, manual, plugin manager)
- Map available commands, settings, keybindings
- Generate a skill that helps configure and use the extension

---

### 8. Documentation

**Primary signals:**
- Mostly `.md`, `.rst`, `.txt` files (>90% of repo by file count)
- Has `docs/`, `wiki/`, `site/`, `book/` directory at root
- Uses documentation generators (mdbook, docusaurus, gitbook, sphinx)
- Contains `mkdocs.yml`, `docusaurus.config.js`, `book.toml`

**Secondary signals:**
- `README.md` is the only significant file
- No `.py`, `.js`, `.rs`, `.go`, `.ts` source files

**Extraction strategy:**
- Build a search-and-retrieve skill over the documentation content
- Index the document structure (table of contents, cross-references)
- Generate a skill that answers questions based on the docs

---

### 9. Unknown

**Fallback when no category matches.** This happens with:
- Mixed-purpose repos
- Very small repos (a single script)
- Binary/proprietary tools with no source
- Repos that are primarily data or assets

**Extraction strategy:**
- Structural analysis only (directory tree, file types by count)
- README-based extraction (what does the author say it does?)
- Generate a minimal skill with setup notes and directory map
- Flag as "unknown category — may need manual refinement"

---

## Override Rules

If multiple categories match, use this priority (highest wins):

1. Monorepo — always takes precedence (contains multiple categories inside)
2. CLI Tool — if it has a CLI, prioritize CLI docs even if it's also a library
3. Application — if it serves something, prioritize operations
4. Plugin — if it extends something, prioritize integration
5. Library / Template / Config / Docs — user's goal determines

**The "ask" rule:** If the top two categories are close (e.g., CLI Tool vs Library),
defer to the user in Phase 2:

> This project looks like it could be a **CLI Tool** or a **Library**. Which
> perspective do you want the skill to focus on?

---

## Category Output Format

Phase 1 must produce this structured output:

```yaml
category:
  primary: <category slug>
  confidence: <0.0-1.0>
  alternatives:
    - <other matching categories>
  signals:
    - <specific files/configs that triggered the match>
  language:
    primary: <language>
    frameworks: [<detected frameworks>]
  build:
    system: <detected>
    test: <detected>
    package_manager: <detected>
  complexity: simple | moderate | complex
```
