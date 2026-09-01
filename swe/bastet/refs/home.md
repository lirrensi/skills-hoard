# Repository Health Checklist (Twelve Lenses)
> Load only when needed for repo health audits, bootstrapping new projects, or when unsure what to improve.
>
> Priority Legend: 🔴 CRITICAL | 🟡 IMPORTANT | 🟢 NICE

---

## 🚩 REPO_FLAGS — Detect First, Then Apply

**Scan the repo and set these flags. Each flag adjusts which lenses matter and how deeply to apply them.**

| Flag | Detection | Effect on Scan |
|------|-----------|----------------|
| `IS_PUBLIC` | Repo is on GitHub/GitLab public, or meant to be | Apply Lens 9 (Badges) + Lens 11 (Governance) fully |
| `IS_PRIVATE` | Internal/team only | Skip Lens 9, simplify Lens 11 to CODEOWNERS only |
| `IS_MONOREPO` | Has `packages/`, `apps/`, or multiple `package.json`/`go.mod` | Apply language adapters per subfolder, check workspace config |
| `IS_LIBRARY` | `package.json` has `"main"`, published to npm/pypi/crates | CHANGELOG critical, LICENSE mandatory, semver strict |
| `IS_API_SERVICE` | Has `routes/`, `controllers/`, OpenAPI spec, listens on port | Secrets lens stricter, health checks mandatory |
| `IS_FRONTEND` | Has `src/components/`, framework entry (Next, Vite, etc.) | Add accessibility checks, build output in gitignore |
| `IS_CLI_TOOL` | Has bin/entry point, arg parsing, meant for terminal | Man page or `--help` quality, install one-liner in README |
| `HAS_DOCKER` | `Dockerfile`, `docker-compose*.yml`, `.devcontainer/` | Check compose validity, devcontainer docs, image size |
| `HAS_CI` | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` | Tune existing CI, don't suggest from scratch |
| `HAS_DATABASE` | `migrations/`, ORM config, `prisma/schema.prisma` | Add DB-specific gitignore, env example entries |
| `HAS_INFRA` | `*.tf`, `k8s/`, `helm/`, `Pulumi.yaml`, `cdk/` | Apply Infra adapter, secrets lens STRICTER, state file hygiene |
| `HAS_RELEASES` | Tags/releases exist, publish config (npm/pypi/crates/docker) | Add release engineering checks, rollback story |
| `HAS_MOBILE` | `ios/`, `android/`, `Fastfile`, `*.xcodeproj` | Apply Mobile adapter, signing config safety critical |
| `HAS_ML` | `notebooks/`, `*.ipynb`, `models/`, DVC, `requirements-gpu.txt`, LLM SDKs, vector DBs, prompt folders, eval harnesses | Escalate ML security review, check notebook/artifact hygiene, inspect prompt/RAG/tool trust boundaries |
| `IS_ML_HEAVY` | Core product behavior depends on LLM/ML/agent loops, retrieval, tools, or non-deterministic pipelines | Treat as deeper static review: inspect code + existing tests thoroughly, but explicitly note that runtime safety still needs separate interactive/e2e evaluation |
| `IS_REGULATED` | Handles PII/PHI/PCI, or in regulated industry | Stricter security/privacy checks, audit logging |
| `IS_GREENFIELD` | Fresh repo, <10 commits, no CI yet | Prioritize setup over cleanup, bootstrap everything |
| `IS_LEGACY` | Old repo, tech debt, inconsistent patterns | Prioritize low-risk cleanup, document before changing |

**Detection Order:**
1. Public vs Private → sets overall governance tone
2. Library vs Service vs Frontend vs CLI → sets lens priority
3. Monorepo vs Single → sets scope
4. Greenfield vs Legacy → sets approach (build vs repair)

**Apply lenses conditionally:**

```
IF IS_PUBLIC:
  → Lens 9 (Badges): FULL
  → Lens 11 (Governance): FULL
IF IS_PRIVATE:
  → Lens 9 (Badges): SKIP
  → Lens 11 (Governance): CODEOWNERS only
IF IS_LIBRARY:
  → Lens 1 (Docs): CHANGELOG + LICENSE = CRITICAL
IF IS_API_SERVICE:
  → Lens 5 (Secrets): STRICTER — check for hardcoded URLs, API keys
  → Lens 8 (Runability): Health endpoints mandatory
IF IS_MONOREPO:
  → Lens 6 (Structure): Check workspace config, shared deps
IF HAS_INFRA:
  → Lens 5 (Secrets): STRICTEST — state files often contain secrets
  → Lens 2 (CI): Add infra linting (tflint, checkov) to pipeline
IF HAS_RELEASES:
  → Add rollback story check
  → Verify changelog tied to releases
IF HAS_MOBILE:
  → Lens 5 (Secrets): Check signing configs (.p12, .keystore) not committed
IF HAS_ML:
  → Lens 5 (Secrets): Check prompt/RAG/tool boundaries, output redaction, and model-adjacent secrets handling
  → Lens 4 (Dependency Hygiene): Audit AI/ML dependency sprawl and stale packages more aggressively
IF IS_ML_HEAVY:
  → Apply a deeper code review of non-deterministic flows, mutation paths, and safety controls
  → State coverage limit explicitly: code + existing tests only, not full runtime proof
IF IS_REGULATED:
  → Lens 5 (Secrets): Audit logging, PII handling documented
IF IS_GREENFIELD:
  → Focus on bootstrap: gitignore, CI, lint, hooks
IF IS_LEGACY:
  → Focus on safety: document before changing, incremental fixes
```

---

## 📜 Lens 1: Documentation Completeness
*"Does every room have a sign?"*

| Doc Type | Check |
|----------|-------|
| **README.md** | Exists? Has setup instructions? Covers the basics? |
| **CHANGELOG.md** | Exists? Up to date? Follows convention? |
| **CONTRIBUTING.md** | Exists? Clear PR process? Dev setup documented? |
| **.env.example** | Complete? Shows all required env vars? |
| **LICENSE** | Present? Matches package.json? |
| **Architecture docs** | In `/docs`? Current? Clear? |

**Note:** Bastet usually ensures docs exist and stay maintained rather than owning all canon writing. `README.md` is the exception: Bastet may create or improve it as part of repo hygiene and onboarding. Product/spec/architecture canon still belongs to Thoth.

---

## ⚙️ Lens 2: CI/CD Pipeline Review
*"Is the household running smoothly?"*

| Check | Question |
|-------|----------|
| **Linting** | Does CI catch style issues before merge? |
| **Testing** | Does CI run tests? What coverage threshold? |
| **Security** | Does it scan deps? Run SAST? |
| **Speed** | Is it slow? Can steps parallelize? |
| **Caching** | Are deps cached? Can builds reuse artifacts? |
| **Secrets** | Does CI fail if secrets leak? |
| **Notifications** | Does it alert on failure? Where? |
| **Rollback plan** | Can you revert a deploy in < 5 min? Documented? |
| **Environment parity** | Do staging/prod use same pipeline, or diverge silently? |
| **Manual gates** | Is prod deployment gated on approval, or does merge = deploy? |

**Hunt:** Missing pipelines. Broken steps. Missing caching. Silent failures. Merge = production explosion.

---

## 🧹 Lens 3: Linter & Formatter Harmony
*"Is everything in its place?"*

| Config | Check |
|--------|-------|
| **ESLint / TSLint** | Exists? Extends reasonable config? Has plugins? |
| **Prettier** | Exists? Matches editorconfig? |
| **.editorconfig** | Exists? Consistent with prettier? |
| **Editor integration** | Are configs editor-agnostic? |

**Hunt:** Conflicting rules. Missing configs. "Works on my machine" due to formatting.

---

## 🏷️ Lens 4: Dependency Hygiene
*"Are the pantry shelves organized?"*

| Check | Question |
|-------|----------|
| **Outdated** | Are deps current? Any security advisories? |
| **Unused** | Any dead deps? `npm prune` / `pip freeze -l`? |
| **Phantom deps** | Imports in code but missing from manifest? (Works locally via hoisting, breaks in CI) |
| **Dev vs Prod** | Build tools in devDeps, runtime libs in dependencies? |
| **Licensed** | Any problematic licenses? |
| **Versions** | Pinned? Range? Caret/semver? |
| **Scripts** | `package.json` scripts sensible? Documented? |
| **Lock file** | Present? Committed? |

**Hunt:** Security vulnerabilities. Unused deps bloating the install. Unclear scripts. "It works on my machine" phantom deps.

---

## 🔐 Lens 5: Secrets & Boundaries 🔴 CRITICAL
*"Are the doors locked?"*
**Severity: CRITICAL — Check this first, always. A leaked secret is a broken door.**

| Check | Question |
|-------|----------|
| **.gitignore** | Complete? Ignores node_modules? .env? logs? builds? |
| **.env.example** | Shows all required vars? No actual secrets? |
| **Secrets** | Any committed secrets? AWS keys? Passwords? Tokens? |
| **Git history audit** | Secrets ever committed then "deleted"? Run `git log --all -S 'AKIA'` or trufflehog `--since-commit`? |
| **CI secrets** | Are secrets injected via env, not hardcoded? |

**Hunt:** Leaked secrets. Incomplete gitignore. .env in git history. "Deleted" secrets still in commits.

### Supply Chain Hygiene (Part of Secrets)

| Check | Question |
|-------|----------|
| **Dependabot/Renovate** | Is dependency scanning enabled? |
| **Secret scanning** | Gitleaks/trufflehog in CI or pre-commit? |
| **OSSF Scorecard** | (For public repos) Security score visible? |
| **SBOM** | Software bill of materials generated? (Increasingly common) |

**Hunt:** Vulnerable dependencies go unnoticed. Secrets in git history. Unverified dependencies.

---

## 📁 Lens 6: Folder Structure Intuition
*"Can a newcomer find their way home?"*

| Check | Question |
|-------|----------|
| **Convention** | Follows language/framework conventions? (`src/`, `lib/`, `tests/`) |
| **Navigation** | Is it clear where things live? |
| **Depth** | Too nested? Files buried? |
| **Naming** | Clear names? Consistent casing? |
| **Repo bloat** | Is `.git` folder massive? Binaries committed? Large files from years ago? |
| **Orphan files** | Config files for tools no longer used? (`tslint.json` alongside `eslint.config.js`) |

**Hunt:** Confusing structure. Magic folders. "Where do I even put this?" 2GB repo for 5MB app. Dead config files.

---

## 🪝 Lens 7: Git Hooks & Conventions
*"Does the home govern itself gracefully?"*

| Check | Question |
|-------|----------|
| **pre-commit** | Hooks exist? Run linters? Format checks? |
| **commit-msg** | Enforce conventional commits? |
| **Commit conventions** | Clear format? PR process defined? |
| **Branch strategy** | Main/master? Feature branches? Release process? |

**Hunt:** No hooks (linters never run). No commit standards. Broken CI from bad commits.

---

## 🏥 Lens 8: Health Checks & Runability 🔴 CRITICAL
*"Can a brand new dev clone and run this in under 10 minutes?"*
*"Can a coding agent clone, setup, and run tests with zero manual steps?"*

**Severity: 🔴 CRITICAL — If no one can run the project, it doesn't exist.**

| Check | Question |
|-------|----------|
| **Setup scripts** | One-command setup? `npm install` works? |
| **Makefile/justfile/taskfile** | Standard commands: `dev`, `test`, `lint`, `build`? |
| **Docker** | `docker-compose` for local dev? Database/redis included? |
| **Seed data** | Is there a way to populate initial data? |
| **Environment docs** | Does setup guide explain all required env vars? |
| **Quickstart** | Can you go from clone to "hello world" in 10 min? |
| **Failure clarity** | When setup fails, does error tell you WHAT TO DO? Or dump a stack trace? |
| **Prerequisites** | External deps (Postgres, Redis, specific OS) listed upfront, not discovered mid-install? |
| **Idempotency** | Running setup twice works, or fails on second run? |
| **Agent-readiness** | Can an agent `./dev setup && ./dev test` without interactive prompts? |
| **Doctor script** | Is there a `./dev doctor` that returns structured JSON health data with exit codes? |
| **Auth bypass** | Is there a `MOCK_AUTH_ENABLED` flag that lets agents bypass GUI login? |
| **Token generation** | Can an agent get an auth token via `./dev generate-token` without a browser? |
| **Bootstrap entry point** | Is there a `./dev` script at the root that works without `make` installed? |

**Hunt:** "Works on my machine." Missing dependencies. "Just run these 47 commands." Unlisted prerequisites. Cryptic error messages. No `./dev doctor`. No auth bypass for headless agents.

> **When dev environment setup is needed:** Read `./dev_environment.md` for the full blueprint strategy by project type.

---

## 📊 Lens 9: Badge & Signal Hygiene
*"Does the home announce itself proudly?"*

**Severity: 🟢 NICE — First impressions only.**

| Check | Question |
|-------|----------|
| **Badge existence** | Are there README badges? |
| **Badge accuracy** | Do they point to correct branch (main, not master)? |
| **Badge validity** | Do they link to working status? |
| **Relevance** | Are they useful (CI, coverage, version) or decorative? |

**Note:** Only for **public repos** or repos with remote CI. Skip for fully private repos with no GitHub/GitLab connection.

**Hunt:** Broken badges. Wrong branch. "Build: unknown." Version: "v0.0.0."

---

## 🏗️ Lens 10: Reproducibility & Toolchain Pinning
*"Does the home build the same way for everyone?"*

| Check | Question |
|-------|----------|
| **Runtime pinning** | `.tool-versions`, `.nvmrc`, `.python-version`, `go.mod`, `rust-toolchain.toml`? |
| **Container** | Dockerfile present? devcontainer.json? |
| **Deterministic installs** | Lockfiles present? CI uses them? |
| **Build entrypoints** | Makefile, justfile, taskfile.yml? |
| **CI/local alignment** | Does CI use same toolchain version as `.nvmrc`/`.tool-versions`? Or drifting? |
| **OS assumptions** | Does project assume macOS/Linux? Windows devs blocked silently? |

**Hunt:** "Works on my Node version." "Works on my Python 3.x." Inconsistent environments. CI uses 20, local uses 18.

---

## 🏛️ Lens 11: Governance & Community Defaults
*"Can outsiders (or future you) contribute safely?"*

**Severity: 🟡 IMPORTANT for public repos, 🟢 NICE for private/internal repos.**

| Check | Question |
|-------|----------|
| **CODE_OF_CONDUCT.md** | Exists? Clear expectations? |
| **SECURITY.md** | Responsible disclosure process? |
| **Issue templates** | `.github/ISSUE_TEMPLATE/` present? |
| **PR templates** | `.github/PULL_REQUEST_TEMPLATE` present? |
| **CODEOWNERS** | Code ownership defined? |
| **Branch protection** | Main branch protected? Required reviews? |

**Note:** Only for **public repos** or repos expecting external contributions. For private repos used only by your team, these are nice-to-haves.

**Hunt:** No contribution guidelines. No security contact. Unclear ownership. "Just send a PR."

---

## Language Adapters

Adapt checks to the ecosystem. Apply relevant sections:

### 🟢 If Node.js / JavaScript / TypeScript

| Check | Tools |
|-------|-------|
| Linting | ESLint, TSLint |
| Formatting | Prettier |
| Package manager | npm, yarn, pnpm |
| Audit | npm audit, snyk |
| Lock file | package-lock.json, yarn.lock, pnpm-lock.yaml |

### 🐍 If Python

| Check | Tools |
|-------|-------|
| Linting | ruff, flake8 |
| Formatting | black, isort |
| Type checking | mypy, pyright |
| Dependency audit | safety, pip-audit |
| Package manager | pip, poetry, pip-tools |

### 🦀 If Go

| Check | Tools |
|-------|-------|
| Formatting | gofmt, goimports |
| Linting | golangci-lint |
| Dependency management | go.mod, go.sum |
| Security | govulncheck |

### 🦅 If Rust

| Check | Tools |
|-------|-------|
| Formatting | rustfmt |
| Linting | clippy |
| Dependency audit | cargo-audit |
| Toolchain | rust-toolchain.toml |

### ☁️ If Infrastructure (Terraform / K8s / Pulumi)

| Check | Tools |
|-------|-------|
| **Linting** | `tflint`, `kubeval`, `hadolint` (Docker) |
| **Formatting** | `terraform fmt` |
| **Security** | `tfsec`, `checkov`, `kics` |
| **State hygiene** | State files in `.gitignore`? Remote backend configured? |
| **Docs** | `terraform-docs` (auto-generate module docs) |
| **Drift detection** | Is there a process to detect infra drift from IaC? |

### 📱 If Mobile (iOS / Android / React Native)

| Check | Tools |
|-------|-------|
| **Ruby/Gem** | `Gemfile` present? (for Fastlane/Cocoapods) |
| **Signing 🔴** | Are `*.p12`, `*.keystore`, provisioning profiles in `.gitignore`? CRITICAL |
| **Linting** | `SwiftLint` (iOS), `ktlint` / `detekt` (Android) |
| **CI** | `Fastfile` present? Match/sigh configured? |
| **App store** | CI pipeline for TestFlight / Play Store? |

### 🔀 If Mixed / Polyglot

Apply checks per language/folder. A monorepo may need multiple adapters.
Those serve as examples — adapt to language specifics.

---

## 🧠 Lens 12: Agent Ops & Context Hygiene
*"Can a coding agent operate here safely and understand the repo efficiently?"*

**This is not DevEx for humans. This is AgentEx — making repos work for AI coding agents.**

### Context & Trust Hygiene 🔴

| Check | Question |
|-------|----------|
| **Instruction files as code** | Are `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, prompt templates, memory files, `skills/`, MCP configs/servers, and agent bootstrap docs treated like operational code rather than passive docs? |
| **Imperative tasking** | Do repo-controlled files contain instructions that can steer agents into privileged actions, network callbacks, background jobs, secret access, self-modification, or bypassing trust boundaries? |
| **Contributor-controlled text** | Could `.github/` issue templates, PR templates, contribution docs, comments, setup guides, changelogs, or copied terminal snippets be pasted into agent context as if they were trusted instructions? |
| **Bootstrap command safety** | Before recommending `npm install`, generators, MCP setup, or bootstrap scripts, do lifecycle hooks (`preinstall`, `install`, `postinstall`, `prepare`) and setup paths get reviewed first? |
| **Trust-boundary bypass guidance** | Does the repo tell users or agents to disable approvals, sandboxing, permissions, or confirmation prompts for convenience? |
| **Safe-run defaults** | Does the repo encourage least privilege, review-first workflows, isolated generated output, and human confirmation for networked or file-mutating actions derived from untrusted text? |

**Hunt:** Agent instruction files that smuggle tasking. Skill/MCP configs with elevated influence. Setup docs that normalize disabling safety rails. Package hooks that execute surprise behavior.

### Agent Instruction Files

| Check | Question |
|-------|----------|
| **Instruction file exists** | Is there an `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, or `.claude/` directory? |
| **Instruction hygiene** | Is it current? Or full of outdated context, deprecated paths, wrong commands? |
| **Context bloat** | Are there 50 skill files nobody needs? Agents drown in irrelevant context. |
| **Signal-to-noise** | Does the agent spend 10k tokens loading context that provides 1k tokens of value? |

**Hunt:** `.cursor/` with 100 files. `AGENTS.md` that references deleted folders. Skills for tools you don't use.

### Agent-Readable Structure

| Check | Question |
|-------|----------|
| **Entry points obvious** | Can an agent find `main()`, `app.py`, `index.ts` in < 30 seconds? |
| **Module map** | Is there a `docs/spec.md` and `docs/arch*.md` or similar that map behavior and architecture? |
| **Naming clarity** | Are folder/file names self-explanatory? `utils/` is a red flag. |
| **Config discoverability** | Can an agent find all config files without spelunking 5 directories deep? |

**Hunt:** Deep nesting. Generic names (`helpers/`, `utils/`, `common/`). No architecture docs.

### Programmatic Infrastructure Access

| Check | Question |
|-------|----------|
| **API over UI** | Can infra state be queried programmatically? (CLI, API, not just dashboard) |
| **State as code** | Is infra defined in queryable files (Terraform, Pulumi) or hidden in cloud console? |
| **Observability endpoints** | Are there `/health`, `/metrics`, `/status` endpoints agents can query? |
| **Config as data** | Can agents read config without parsing 500-line YAML by hand? (JSON/YAML schemas, typed configs) |

**Hunt:** Infrastructure only visible in AWS console. Configs that require humans to interpret. No programmatic way to ask "is the database healthy?"

### Agent-Friendly Tooling

| Check | Question |
|-------|----------|
| **Linter output parseable** | Does `eslint --format json` or equivalent work? Can agents consume errors programmatically? |
| **Test output structured** | Are test results in JUnit/TAP format? Or just wall of text? |
| **One-command operations** | `make lint`, `make test`, `make dev` — agents struggle with multi-step manual processes |
| **Error messages actionable** | "Error: port in use" vs "Error: port 3000 in use. Kill process with: `lsof -ti:3000 | xargs kill`" |
| **`make doctor` exists** | Is there a single command that returns structured health data (JSON)? Agents need to self-diagnose. |
| **`./dev` entry point exists** | Is there a root-level bootstrap script that works without `make` installed? |
| **`make setup` idempotent** | Can an agent run setup twice safely? No "already exists" errors? |
| **Environment self-service** | Can an agent spin up all dependencies, run tests, and tear down without human intervention? |
| **Auth bypass available** | Is there a `MOCK_AUTH_ENABLED` flag that lets agents bypass GUI login? |
| **Token generation** | Can an agent get an auth token via CLI without a browser? |
| **Parseable error format** | Do errors include category, cause, fix command, and docs reference? |
| **Time budgets defined** | Do commands have maximum time limits so agents can detect hung processes? |

**Hunt:** Linters that only output pretty colors. Tests that print "something failed" without details. Commands that require interactive input. No `./dev doctor`. Setup that breaks on second run. GUI-only authentication with no CLI bypass.

> **When agent operability needs to go deeper — project-type detection, environment blueprints, self-healing protocols:** Read `./dev_environment.md` for the full agent ops environment strategy.

### The Healthy Agent-Ready Repo

```
repo/
├── AGENTS.md              # Single source of truth for agent context
├── .cursor/rules/         # (if using Cursor) — minimal, focused rules
├── docs/
│   ├── product.md         # Quick human overview
│   ├── spec.md            # Canonical behavior spec
│   ├── arch.md            # Architecture canon (split if needed)
│   └── agent-guide.md     # How to work with this repo programmatically
├── Makefile               # One-command everything: dev, test, lint, build
└── configs/               # Typed, schema-validated configs (not mystery YAML)
```

### Red Flags for Agent Ops

| Red Flag | Why It Matters |
|----------|----------------|
| No agent instruction file | Agent has no guidance, makes poor assumptions |
| Bloated instruction file | Agent context window wasted on noise |
| Infra only in GUI | Agent can't verify or fix infrastructure |
| Parseable output missing | Agent can't consume tool output |
| Multi-step manual setup | Agents can't handle interactive prompts |

---

## Output Template: Home Report

```markdown
# 😽 BASTET'S HOME: [Codebase Name]

## The Household

| Room | Status | Notes |
|------|--------|-------|
| Documentation | 🟢/🟡/🔴 | [summary] |
| CI/CD | 🟢/🟡/🔴 | [summary] |
| Linters | 🟢/🟡/🔴 | [summary] |
| Dependencies | 🟢/🟡/🔴 | [summary] |
| Secrets & Supply Chain | 🟢/🟡/🔴 | [summary] |
| Structure | 🟢/🟡/🔴 | [summary] |
| Hooks | 🟢/🟡/🔴 | [summary] |
| Runability | 🟢/🟡/🔴 | [summary] |
| Badges | 🟢/🟡/🔴 | [summary] (skip for private) |
| Reproducibility | 🟢/🟡/🔴 | [summary] |
| Governance | 🟢/🟡/🔴 | [summary] (skip for private) |
| Agent Ops | 🟢/🟡/🔴 | [summary] |

## The Improvements

### 🚨 Blockers (Fix Before Anything Else)
- [ ] [Issue] — [This actively prevents X from working]

### 🐾 Quick Wins (Do First)
- [ ] [Improvement] — [Why it matters]

### 🧹 Cleaning (Do Later)
- [ ] [Improvement] — [Why it matters]

### 🏗️ Construction (For Future)
- [ ] [Improvement] — [Why it matters]

## The Care Plan

### Today
- [ ] Update .gitignore to include [X]
- [ ] Add missing .env.example field: [X]
- [ ] Enable [tool] in CI

### This Week
- [ ] Set up pre-commit hooks with [tool]
- [ ] Audit dependencies for [X]

### This Month
- [ ] Document folder structure in README
- [ ] Set up [pipeline improvement]
```

---

## Quick Reference: What Files to Create

| You Create | Examples |
|------------|----------|
| **Configs** | `.editorconfig`, `tsconfig.json`, `pyproject.toml` |
| **Examples** | `.env.example`, `docker-compose.example.yml` |
| **Git hooks** | `pre-commit` config, commit-msg hook |
| **CI configs** | GitHub Actions workflows, GitLab CI |
| **Gitignore entries** | Add missing patterns |
| **Badges** | CI status, coverage, version badges for README |
| **Automation scripts** | Makefile, justfile, taskfile.yml with `dev`, `test`, `lint`, `build` |
| **Governance files** | CODEOWNERS, `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE` |
| **Health scripts** | Setup scripts, seed data scripts, local dev docker-compose |
| **Agent context** | `AGENTS.md`, `docs/spec.md`, `docs/arch*.md`, schema-validated configs, parseable linter/test output |

---

## 🏆 What Good Looks Like

**A reference for the ideal state. Use this to calibrate recommendations.**

### The Healthy Repo Structure

```
repo/
├── .github/
│   ├── workflows/           # CI configs (test.yml, lint.yml, release.yml)
│   ├── ISSUE_TEMPLATE/      # bug_report.md, feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── CODEOWNERS           # (if team > 1)
├── .husky/                  # or .git/hooks/ — pre-commit, commit-msg
├── docs/                    # Product, spec, architecture, decisions, API docs
│   ├── product.md           # Human-facing overview
│   ├── spec.md              # Behavioral canon
│   └── arch*.md             # Architecture canon
├── src/                     # or lib/, app/ — follows language convention
├── tests/                   # or __tests__/, test/, spec/
├── .editorconfig            # Editor-agnostic formatting
├── .env.example             # All required vars documented
├── .gitignore               # Complete: node_modules, .env, dist/, logs
├── .nvmrc / .python-version # Runtime pinned
├── .tool-versions           # (if using asdf)
├── AGENTS.md                # Agent context — focused, current, high signal
├── CHANGELOG.md             # Follows Keep a Changelog
├── LICENSE                  # Matches package metadata
├── Makefile                 # or justfile, taskfile — dev, test, lint, build
├── README.md                # What, Why, Quick Start, Requirements
└── [lockfile]               # package-lock.json, yarn.lock, pnpm-lock.yaml, etc.
```

### The Healthy README

Read `./readme.md` for Bastet's full README-writing guide.

A good README answers these in order:
1. **What is this?** (1-2 sentences)
2. **Why does it exist?** (brief context)
3. **How do I run it?** (quickstart — 3 commands max)
4. **What do I need?** (prerequisites, env vars)
5. **Where do I learn more?** (link to docs/)

Bad: Wall of text, no quickstart, assumes reader knows context
Good: Scannable, copy-pasteable commands, links to deeper docs

### The Healthy .gitignore

Covers:
- Language outputs (`dist/`, `build/`, `*.pyc`, `target/`)
- Dependencies (`node_modules/`, `venv/`, `vendor/`)
- IDE/Editor (`.idea/`, `.vscode/`, `*.swp`)
- Environment (`.env`, `.env.local`, `*.pem`)
- OS junk (`.DS_Store`, `Thumbs.db`)
- Logs & temp (`*.log`, `tmp/`, `.cache/`)

### The Healthy CI Pipeline

- **Fast feedback**: Unit tests + lint run in < 5 min
- **Parallelized**: Independent jobs run concurrently
- **Cached**: Dependencies cached between runs
- **Gated**: Merge blocked on failure
- **Secrets safe**: No secrets in logs, env vars masked

### The Healthy Makefile / Justfile

Standard commands that work everywhere:
```
make dev      # Start local development
make test     # Run tests
make lint     # Run linters
make build    # Build for production
make clean    # Remove generated files
```

If a new dev clones the repo, they should be able to:
```bash
make dev
# and have a running app in < 5 minutes
```

### The Healthy .env.example

- Lists EVERY environment variable the app needs
- Has a comment explaining what each does
- Shows example values (not real secrets)
- Indicates which are required vs optional

### Red Flags (Immediate Action)

| Red Flag | Why It Matters |
|----------|----------------|
| `.env` committed | Secrets in git history → rotate ALL credentials |
| No `.gitignore` | Garbage in repo, potential secrets |
| No lockfile | Non-deterministic builds, "works on my machine" |
| No README | Onboarding pain, project opacity |
| Main branch unprotected | Accidental force-pushes, broken main |
| CI skipped on main | Broken main is acceptable → broken production |
| No agent instruction file | Agents have no guidance, make poor assumptions |
| Agent context bloat | 100 skill files = agent drowns in noise |

---
