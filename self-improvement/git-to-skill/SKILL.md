---
name: git-to-skill
description: 'Converts any git repository into an executable skill package — CLI references, usage guides, automation scripts, and shell integrations. Triggers on: "turn this repo into a skill", "git-to-skill", "make a skill from this repo", "generate skill from GitHub", "create a skill for this project", "skillify this repo", "repo-to-skill". NOT for analyzing code quality or reviewing PRs — use code-review or audit skills for that.'
metadata:
  version: 1.0.0
  category: build
  tags: [git, github, gitlab, repository, skill-generation, cli-extraction, automation, onboarding]
  difficulty: advanced
  phase: build
---

# Git-to-Skill Pipeline

Transform any git repository into a production-grade skill package that captures how
to use, build, and operate the project. The pipeline scouts the repo, categorizes its
nature, clarifies the user's goal, and generates a structured skill package — with
reference docs, convenience scripts, and usage guides — tailored to *that* specific
project.

This closes the loop between "I found a cool repo" and "I know how to use it
fluently." One command turns `curl https://github.com/something` into an executable
skill that lives in your skill store.

## Reference Files

| File                                      | Contents                                                    | Load When               |
| ----------------------------------------- | ----------------------------------------------------------- | ----------------------- |
| `references/repo-categories.md`           | Taxonomy of project types and detection heuristics          | Phase 2 (Analysis)      |
| `references/cli-extraction.md`            | Patterns for extracting CLI commands, flags, subcommands    | Phase 4 (if CLI tool)   |
| `references/library-extraction.md`        | Patterns for extracting API surfaces, exports, signatures   | Phase 4 (if library)    |
| `references/general-extraction.md`        | Patterns for apps, services, configuration-heavy projects   | Phase 4 (if app/service)|

## Prerequisites

- `gh` CLI (GitHub CLI) — for authenticating with GitHub repos
- `git` — obvious, baby
- `uv` or `node` / `pnpm` — for running extraction scripts on Node/Python projects
- A working temp directory: `$env:TEMP` or `/tmp`
- The `skill-creator` skill (for packaging the final output)

## Workflow

### Phase 0: Trigger & Intake

Accept the repository in any supported format:

| Input Format              | Action                                                                |
| ------------------------- | --------------------------------------------------------------------- |
| `github.com/owner/repo`   | Parse owner/repo, clone via `gh repo clone owner/repo` (preferred) or `git clone` |
| Full git URL              | `git clone <url>` to temp dir                                          |
| Local file path           | Use as-is (copy to temp if needed)                                    |
| `owner/repo` shorthand    | Assume GitHub, `gh repo clone owner/repo`                             |
| npm/PyPI package name     | Resolve to repo via package metadata, then clone                      |

**Cloning rules:**
- Use `--depth 1` for shallow clone (we don't need history — just the files)
- Clone to a temp directory: `"$(Join-Path $env:TEMP "git-to-skill-$(Get-Random)")"`
- If the repo is massive (>100MB), warn the user and ask if they want to proceed
- If the repo is already local, skip cloning and use the path directly

**Automation helper:** Use `scripts/scout.ps1` (Windows) or `scripts/scout.sh`
(Unix/macOS/WSL) with the repo path to produce a structured JSON project profile.
This handles all of Phase 1 probes automatically and outputs a profile the LLM
can use directly. It's the fastest path through Phase 1 and reduces hallucination.

```powershell
# Windows
.\scripts\scout.ps1 -Path "C:\temp\repo"

# Unix
chmod +x scripts/scout.sh && ./scripts/scout.sh /tmp/repo -o profile.json
```

### Phase 1: Scout & Recon

Analyze the repository to build a comprehensive project profile. Run these probes in
parallel where possible:

**1.1 — Metadata extraction:**
```
- README.md (first 200 lines — elevator pitch, badges, quick start)
- package.json / Cargo.toml / pyproject.toml / setup.py / Gemfile / go.mod
- Dockerfile, docker-compose.yml
- .github/ directory (CI workflows)
- LICENSE
- Makefile / Justfile / Taskfile.yml
- .gitignore
```

**1.2 — Structural analysis:**
```
- Top-level directory listing (depth 1)
- Source code entry points: bin/, cli/, main.go, main.py, index.js, __main__.py
- Test directory presence & framework (jest, pytest, go test, cargo test)
- Config files: .env.example, config/, .eslintrc, tsconfig, etc.
- Documentation: docs/, wiki/, man/, site/
```

**1.3 — Language & framework detection:**
```
Primary language   → from file extensions (heuristic: count lines in tracked files)
Build system       → Makefile, Cargo.toml, package.json scripts, pyproject.toml
Package manager    → pnpm, cargo, uv/pip, go mod, gem, apt, brew
Test framework     → from config files and dev dependencies
```

**1.4 — Categorization (see `references/repo-categories.md`):**
```
Determine the repo's primary category:
  - CLI Tool       → has CLI entry point, bin field, console_scripts
  - Library        → has exports, importable API, no main entry
  - Application    → has Dockerfile, server code, config files
  - Template       → has template variables, cookiecutter, scaffolding
  - Monorepo       → multiple packages, workspaces, sub-projects
  - Config/Dotfile → dotfiles, .rc files, editor config
  - Documentation  → mostly markdown, no significant source code
  - Tool/Plugin    → extends another tool (VS Code extension, neovim plugin, etc.)
  - Unknown        → genuinely can't tell; default to general extraction
```

**1.5 — Complexity assessment:**
```
Simple      → single entry point, no build step, < 500 LOC
Moderate    → build step, tests, 500-5000 LOC, documented
Complex     → monorepo, multi-service, > 5000 LOC, extensive config
```

Output a **project profile** — a structured summary used in the next phase.

### Phase 2: Goal Clarification (The "What For?" Step)

**If the user has NOT specified what they want the output for, ask.** Present the
options clearly:

> I've scouted `<repo>` and here's what I found:
>
> **Project:** `<name>` — `<brief description from README>`
> **Category:** `<CLI Tool / Library / Application / ...>`
> **Language:** `<primary lang>` | **Build:** `<build system>` | **Tests:** `<test framework>`
> **Complexity:** `<Simple / Moderate / Complex>`
>
> What do you want me to generate?
>
> 1. **🧭 Usage Reference** — A skill with CLI docs, API reference, configuration guide, and
>    quick-start cheatsheet. Best for "I want to learn how to use this project."
>
> 2. **⚡ Automation Scripts** — A skill with shell scripts for building, testing, running,
>    deploying, CI integration, and common dev workflows. Best for "I want to operate this
>    project day-to-day."
>
> 3. **📦 Full Skill Package** — Everything: reference docs + automation scripts + setup
>    guide + shell completions. The whole enchilada.
>
> 4. **🎨 Custom** — Tell me what specifically you need and I'll tailor the output.

**If the user DID specify their goal, skip to Phase 3 with their intent.**

### Phase 3: Extraction & Generation

Based on the project category (from Phase 1) and the user's goal (from Phase 2), run
the appropriate extraction pipeline.

#### 3A — CLI Tool Extraction

For projects categorized as **CLI Tool**, load `references/cli-extraction.md` and:

**⚠️ CRITICAL PRE-CHECK — Existing CLI detection:**

Before generating ANY CLI wrapper, check if the project already ships a CLI:

1. **Check published package entry points:**
   - PyPI: `pip install <pkg> 2>/dev/null && python -c "import importlib.metadata as md; dist = md.distribution('<pkg>'); print([e for e in dist.entry_points if e.group == 'console_scripts'])"`
   - npm: `npm view <pkg> bin 2>/dev/null`
   - Cargo: check `[[bin]]` in Cargo.toml
2. **If a CLI already exists:**
   - **DO NOT** generate a wrapper script
   - Instead, generate a **reference doc** documenting the existing CLI's commands,
     flags, and usage patterns
   - Document the CLI as: `` `<command> --help` ``
3. **Only generate a NEW CLI wrapper** if no CLI entry point exists in the published package

**Then enumerate subcommands & entry points:**
   - Run `<command> --help` or `npx <package> --help` if possible
   - Parse `bin` field in package.json, `console_scripts` in setup.py/pyproject.toml
   - Scan for `argparse`, `click`, `typer`, `commander`, `yargs`, `clap`, `cobra` usage
   
2. **Extract command tree:**
   - Top-level commands and subcommands
   - Flags, options, arguments with types and defaults
   - Environment variables that influence behavior
   - Configuration file paths
   - Exit codes and error handling

3. **Generate artifacts:**
   - `references/cli-reference.md` — structured command reference tree
   - `scripts/completions/` — shell completion stubs (bash/zsh/fish) if the project doesn't ship them
   - `scripts/quickstart.sh` — walk-through of the most common usage patterns
   - `SKILL.md` — instructions for invoking CLI commands through the skill

#### 3B — Library Extraction

For projects categorized as **Library**, load `references/library-extraction.md` and:

1. **Map the API surface:**
   - Parse main export file(s)
   - Extract exported functions, classes, types, constants
   - Document signatures with parameters and return types
   - Identify integration points (middleware, plugins, hooks)

2. **Extract usage patterns:**
   - Scan README examples and docs/ folder for common patterns
   - Identify 3-5 canonical usage examples
   - Extract testing patterns from test files

3. **Generate artifacts:**
   - `references/api-reference.md` — structured API documentation
   - `scripts/example-usage/` — runnable example scripts
   - `SKILL.md` — instructions for importing, configuring, and integrating the library

#### 3C — General Application Extraction

For projects categorized as **Application** (or anything that doesn't fit CLI/Library),
load `references/general-extraction.md` and:

1. **Extract setup & configuration:**
   - Environment variables and their purposes
   - Configuration file formats (YAML, JSON, TOML, .env)
   - Docker setup (Dockerfile, compose, volumes, ports)
   - Database schemas or migrations
   - External service dependencies

2. **Extract operational knowledge:**
   - Build and run commands
   - Test suite invocation
   - Debug modes and logging configuration
   - Deployment targets (Docker, k8s, serverless, PM2, systemd)
   - Health checks and monitoring endpoints

3. **Extract architecture overview:**
   - Directory structure explanation
   - Key modules and their responsibilities
   - Data flow (if discernible)
   - Extension/customization points

4. **Generate artifacts:**
   - `references/setup-guide.md` — step-by-step setup with all config options
   - `references/operations.md` — run, test, debug, deploy workflows
   - `scripts/setup.sh` — automated setup script (if no setup script exists)
   - `SKILL.md` — the operational guide for the app as a skill

#### 3D — Monorepo Handling

If the project is a **Monorepo**, loop Phase 1-3 for each significant sub-package.
Generate a parent skill with sub-skills or references for each package.

#### 3E — Template / Config / Documentation

For lighter categories:
- **Template**: Extract customization points, variables, and scaffolding workflow
- **Config/Dotfile**: Document each config file, available options, installation commands
- **Documentation**: Index the doc structure, generate a search-and-retrieve skill

### Phase 3.5 — Companion Test Generation

**Every generated script gets a proof-of-life test.** This is not optional — it's
what turns a collection of scripts into a verifiable, maintainable skill.

**Rules:**

| Script language | Test framework | Always generate? |
|----------------|----------------|------------------|
| Python         | `pytest`       | ✅ Yes           |
| Node.js / TS   | `vitest`       | ✅ Yes           |
| Rust           | `#[test]`      | ✅ Yes           |
| Go             | `go test`      | ✅ Yes           |
| Shell (bash)   | —              | ❌ No (syntax-check only) |
| PowerShell     | `Pester`       | ⚠️ If Pester available |

**Test patterns by artifact type:**

#### For generated CLI wrappers (Python)
Create `tests/test_<script>.py`:
```python
"""Tests for the generated CLI wrapper."""
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"


def test_help_exits_cleanly():
    """--help should exit 0 and show usage."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "wrapper-name"), "--help"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower() or "usage" in result.stderr.lower()


def test_version_flag():
    """--version should show a version string."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "wrapper-name"), "--version"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0


def test_invalid_arg_fails():
    """Invalid arguments should exit non-zero with an error."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "wrapper-name"), "--nonexistent"],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
```

#### For generated Node.js scripts
Create `tests/<script>.test.js`:
```javascript
import { describe, test, expect } from 'vitest';
import { execSync } from 'child_process';
import path from 'path';

const script = path.resolve(__dirname, '../scripts/wrapper-name');

describe('CLI wrapper', () => {
  test('--help shows usage', () => {
    const output = execSync(`node ${script} --help`).toString();
    expect(output.toLowerCase()).toContain('usage');
  });

  test('invalid flag exits non-zero', () => {
    expect(() => execSync(`node ${script} --bogus`)).toThrow();
  });
});
```

#### For existing CLIs (no wrapper needed)
Create a smoke test that verifies the CLI is installed and responds:
```python
"""Smoke test — verifies the existing CLI is installed and functional."""
import subprocess


def test_cli_installed():
    """CLI should be on PATH and respond to --help."""
    result = subprocess.run(
        ["<command>", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0


def test_cli_has_expected_commands():
    """Core subcommands should be listed in help output."""
    result = subprocess.run(
        ["<command>", "--help"], capture_output=True, text=True
    )
    for cmd in ["<subcommand1>", "<subcommand2>"]:
        assert cmd in result.stdout or cmd in result.stderr
```

#### For generated shell scripts
No test generation — but run a syntax check:
```bash
bash -n scripts/setup.sh
```

#### Test execution instructions
Document in the generated skill's SKILL.md how to run the tests:
```markdown
## Running Tests

```bash
# Python tests
uv run pytest tests/ -v

# Node.js tests
npx vitest run

# Shell syntax check
bash -n scripts/*.sh
```
```

**Edge cases:**
- If the script requires external dependencies (GPU, API keys, microphone): wrap in
  `@pytest.mark.skipif` with a clear skip message
- If the wrapper calls a downloadable model: test `--help` only, not actual execution
- For batch/bulk scripts: test the non-destructive flags only
- Test the **interface contract**, not the implementation: what goes in, what comes out

### Phase 4: Skill Packaging

Assemble everything into a consistent skill package:

```
skills/<repo-name>/
├── SKILL.md                    # The generated skill
├── references/
│   ├── project-profile.md      # Full project analysis (always included)
│   ├── cli-reference.md        # CLI docs (if generated)
│   ├── api-reference.md        # API docs (if generated)
│   ├── setup-guide.md          # Setup & config (if generated)
│   └── operations.md           # Run/test/deploy guide (if generated)
├── scripts/
│   ├── setup.sh                # Automated setup / install
│   ├── dev.sh                  # Development workflow
│   ├── completions/            # Shell completions (if CLI)
│   └── example-usage/          # Runable examples (if library)
├── tests/
│   ├── test_cli.py             # CLI smoke tests (pytest/vitest)
│   └── test_scripts.py         # Script-level integration tests (if scripts generated)
├── evals/
│   └── cases.yaml              # Basic test cases for the generated skill
└── attribution.md              # Source repo attribution
```

**SKILL.md generation rules:**
- Frontmatter: `name: <kebab-case-repo-name>`, `source: <repo-url>`, `category: <detected-category>`
- Description: A concise summary of what the skill does (based on the project's own README)
- Body: Instructions for using the skill — commands to run, files to reference, workflows
- Attribution section at the bottom linking back to the original repo

**Script generation rules:**
- Prefer using the project's own build/test/run commands (from Makefile, package.json, etc.)
- If the project has no automation scripts AND the user asked for scripts, create helper scripts
- Scripts must be shell-agnostic where possible (document the shell requirement)
- Scripts must include error handling (`set -e`, meaningful error messages)

**Naming:**
- Skill directory name: kebab-case derived from repo name
- If the name conflicts with an existing skill in the store, append `-<source>` (e.g., `-github`)

### Phase 5: Attribution & Finalization

1. **Attribution section** in the generated SKILL.md:
   ```markdown
   ## Attribution

   This skill was automatically generated from:
   > <repo-name>
   > <repo-url>
   > Generated by git-to-skill on <date>
   ```

2. **Source materials:** If the repo has supplementary materials (docs site, wiki, issues),
   link to them in `references/source-materials.md`

3. **License check:** Read the LICENSE file. If it's a restrictive license, note it in the
   skill's frontmatter under `license: <SPDX-identifier>`

4. **Final validation:** Run the generated tests:
   ```bash
   # Python:  uv run pytest tests/ -v
   # Node.js: npx vitest run
   # Shell:   bash -n scripts/*.sh
   ```
   Then run through the generated skill's instructions to make sure at least the
   first command would work (syntax-check, not full execution)

## Output

The complete skill package at `skills/<repo-name>/` on disk, with:
- A functional `SKILL.md` adapted to the project and the user's goal
- `references/` with extracted knowledge (CLI refs, API docs, setup guides)
- `scripts/` with automation helpers (generated or documented)
- `evals/cases.yaml` with smoke-test assertions
- Full attribution to the source repository

The user can then load this into their skill store and use it whenever they interact
with the project.

## Error Handling

| Error                                  | Resolution                                                    |
| -------------------------------------- | ------------------------------------------------------------- |
| Repo doesn't exist / access denied     | Check the URL, try public clone, suggest user-provided token  |
| Repo is empty                          | Report: no content to extract skill from                      |
| Clone fails (large repo, no network)   | Ask user to provide a local path instead                      |
| Unknown project category               | Default to General Application extraction                     |
| Project has no clear usage pattern     | Fall back to README-based extraction + directory structure map|
| CLI binary requires platform-specific deps | Document deps, generate scripts with preflight checks     |
| Language/framework not recognized      | Fall back to file-based structural analysis without language-specific parsing |
| Generated skill fails validation       | Flag for manual review; include explanations of what failed   |

## Limitations

- Cannot extract skills from private repos without authentication (gh CLI login or token)
- Binary-only repos (no source) produce thin skills — just install + run docs
- Very large monorepos (>20 packages) may need manual splitting
- Language-specific extraction (e.g., parsing AST for API export detection) works best
  for Python, Node/TypeScript, Rust, Go — other languages get file-level extraction
- The generated skill is a *snapshot* — it won't auto-update when the repo changes
- Non-English READMEs are used as-is; no translation step
- Script generation works for POSIX shells (bash/zsh) and PowerShell for Windows tools
