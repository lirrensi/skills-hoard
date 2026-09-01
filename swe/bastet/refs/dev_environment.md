# Dev Environment Strategy (Agent Ops)
> Load when: setting up a dev environment, automating testing infrastructure, making a repo agent-operable, or fixing "it works on my machine."
>
> This is the operational arm of Lens 12 (Agent Ops). Where Lens 12 checks whether an agent *can* understand a repo, this document ensures an agent can *work* in a repo — spin up services, run tests, make changes, and verify everything — with zero human hand-holding.
>
> This is a rare-invocation skill. Load only when explicitly asked to bootstrap, fix, or audit a development environment. Not needed on every run.
>
> Priority Legend: 🔴 CRITICAL | 🟡 IMPORTANT | 🟢 NICE

---

## TL;DR

1. **Detect** project type → pick blueprint
2. **Generate**: `./dev` script → `.env.example` → `.gitignore` → runtime pin → `Makefile` → `docker-compose.yml` → tests → scripts → README
3. **Verify**: `./dev setup && ./dev dev && ./dev test` from clean clone in a bare container
4. **Contract**: setup, dev, test, test-fast, lint, ci, clean, doctor, info, validate-env, snapshot, restore, check, agent-smoke-test, nuke, reset
5. **Rule**: one command, zero questions, guaranteed result, agent can self-heal. 3-strike rule → escalate reset.
6. **Guard**: test --baseline before changes, test --compare-baseline after. Flaky tests quarantined. Mutations spot-checked.
7. **Nuclear option**: `./dev reset --level=N` for graduated reset. `./dev nuke` for scorched earth. Both write reset logs.
8. **Entry point**: `./dev` script at repo root — does NOT assume `make` is installed
9. **Auth**: every app must support local auth bypass for headless agents
10. **Output**: every command must be parseable by agents (JSON exit data, structured errors, no ANSI in CI)

---

## ⚡ The Rules

These are the hard-won rules that prevent the most common agent failures. Read them first. Violate them and the agent will get stuck, produce wrong results, or silently break things.

| # | Rule | Why |
|---|------|-----|
| 1 | **Never block the agent loop** | If `./dev dev` starts a server and never returns, the agent is frozen. Every long-running process must start in the background and return control. |
| 2 | **Every command must exit** | One-shot commands (test, lint) exit with a result code. Server commands (dev, up) start in background and return. Watch commands (--foreground) are for humans only. |
| 3 | **No interactive prompts** | Agents can't press Y. Use `--yes`, `--non-interactive`, `CI=1`. Any prompt is a bug. |
| 4 | **Errors must be actionable** | `[ERROR] database: Connection refused → Fix: docker compose up -d db → Docs: docs/dev-setup.md#database`. Every error tells the agent exactly what to do. |
| 5 | **Auth must be bypassable** | `MOCK_AUTH_ENABLED=true` + `./dev generate-token`. Real auth exists for E2E, bypass exists for headless. Both must coexist. |
| 6 | **`./dev dev` must return** | Start services, wait for health, print "ready", EXIT. Services keep running. Agent gets control back. |
| 7 | **`./dev test-fast` must always work** | Even without Docker. Even in degraded mode. If it needs services, the classification is wrong. |
| 8 | **`./dev setup` must be idempotent** | Running it twice completes in 30 seconds, not 5 minutes. Stamp files in `.setup/` skip completed steps. |
| 9 | **Don't start all services when you need one** | `./dev up db` starts only the database. Fine-grained service control. |
| 10 | **Token expiry must not kill long runs** | Tokens generated at hour 0 must last the entire session. Or auto-refresh silently. |
| 11 | **Flaky tests must be quarantined** | A test that fails 30% of the time will block an agent for hours. Flaky suite separate from main. |
| 12 | **Snapshots must be explicit and small** | `./dev snapshot` creates a named, timestamped state. Not automatic. Not accumulating. Explicit management. |
| 13 | **3-strike rule: escalate, don't retry** | Same fix attempted 3 times without resolution → escalate to next reset level. No infinite loops. |

---

## The Philosophy

**The Pharaoh tells an agent to fix a bug. The agent must be able to do it alone.**

Not "almost alone." Not "with a few questions." Not "after the human starts the database for me." **Alone.**

The human says: *"Fix the login bug."* Then they go to sleep. When they wake up, the bug is fixed, tests pass, lint is clean, and the agent left a clean report. Zero babysitting required.

This is what dev environment strategy is for. It's not about making developers comfortable (though they benefit). It's about making the repo **agent-operable** — so that Ptah can build and verify, and Osiris can run deeper testing, without ever asking a human to type a command.

A home that can't be entered is not a home. A repo that can't be run by an agent is not agent-ready.

> **The test:** Can a coding agent clone this repo, set up the environment, run tests, make code changes, verify those changes, and report results — all without asking the human to do anything?
>
> If the answer is no, the environment is broken. Not the agent. The environment.

This document is the bridge between Lens 8 (Health Checks & Runability) and Lens 12 (Agent Ops & Context Hygiene). Lens 8 asks "can a human run this?" Lens 12 asks "can an agent understand this?" **This document answers: can an agent *operate* this?**

Three principles:

1. **Zero-attention operation.** An agent should never need to ask the human to start a service, seed a database, fix a port conflict, or type a command. If `./dev setup && ./dev test` doesn't produce a passing test suite from a clean clone, the environment is incomplete.

2. **Structured observability.** Every tool must output machine-readable formats. Agents don't read pretty terminal colors — they read JSON, XML, and exit codes. `./dev doctor --json` must return structured health data.

3. **Deterministic by default.** Same commands → same results. Pinned versions, locked dependencies, no `latest` tags, no "works on my machine." The agent ran the same commands yesterday and got the same result.

---

## Stage 0: The Bootstrap Problem

`make` is not universal. Neither is `docker`. An agent landing on a raw Ubuntu VM or a Windows machine may have neither.

**The repo root must contain an executable entry point that requires nothing but a POSIX shell (or PowerShell on Windows).**

### The `./dev` Script

Every repo must have a `./dev` script (or `dev.ps1` on Windows) at the root. This is the **true front door** — not `make`.

```
./dev setup          # Install everything. Idempotent. No prompts.
./dev dev            # Start development environment
./dev test           # Run full test suite
./dev test-fast      # Run fast tests only (under 60s)
./dev lint           # Run linters and formatters
./dev ci             # Run everything CI runs
./dev clean          # Tear down and remove generated files
./dev doctor          # Diagnose environment issues
./dev doctor --json   # Diagnose environment issues (JSON output)
./dev info            # Show project type, commands, ports, services
./dev validate-env    # Check all required environment variables
./dev test --baseline   # Run tests and save results as baseline
./dev test --compare-baseline   # Run tests and compare against baseline
./dev test --flaky-report # Run each test 5x and report flakiness
./dev test --retry N    # Retry failing tests up to N times
./dev nuke              # Destroy everything, start from scratch
./dev nuke --database   # Just nuke the database
./dev nuke --containers # Just nuke Docker containers and volumes
./dev nuke --cache      # Just nuke dependency caches
./dev nuke --whatif     # Show what would be destroyed, don't do it
./dev reset --level=N   # Graduated reset (1=state, 2=services, 3=deps, 4=nuclear)
./dev reset --whatif    # Show what would be destroyed at each level, don't act
./dev snapshot [name]  # Save DB/service state to named snapshot
./dev restore [name]   # Restore from snapshot (default: latest)
./dev snapshot-list    # List all snapshots with size and timestamp
./dev snapshot-cleanup # Delete old snapshots (keep last 5, older than 7 days)
./dev check           # Semantic alias: lint + test-fast (safe to commit?)
./dev logs [service]  # Tail service logs (all, or named service)
./dev up [service]    # Start services (all, or named service like 'db' or 'api')
./dev down [service]  # Stop services (all, or named service)
./dev restart [service] # Restart a specific service without touching others
./dev migrate          # Run database migrations
./dev seed             # Seed database with test data
./dev ps               # Show service health summary
./dev status [service] # Is a service running? Exit code 0/1 + JSON
./dev agent-smoke-test # Full agent flow in clean container
./dev help             # Show all commands
./dev help-json        # Show all commands as JSON
```

**The `./dev` script:**

1. Checks for and installs `make` if missing (or delegates to it)
2. Checks for Docker availability and degrades gracefully if absent
3. Sets `CI=1`, `NONINTERACTIVE=1`, `NO_COLOR=1` to suppress all interactive prompts and colors
4. Detects the platform (macOS/Linux/Windows) and adapts paths
5. Delegates to the Makefile for actual implementation
6. Never prompts. Never waits for user input. Never outputs ANSI codes when `CI=1`.

**Why a script and not just `make`?**
- `make` is not installed everywhere (Windows, minimal containers)
- The script can bootstrap system deps before `make` is available
- The script sets the non-interactive contract globally
- Agents call `./dev` — `make` is an implementation detail

**If `make` is already available**, `./dev` delegates immediately:

```bash
#!/usr/bin/env bash
set -euo pipefail
export CI=1 NONINTERACTIVE=1 NO_COLOR=1
exec make "$@"
```

**If `make` is not available**, `./dev` installs it or implements the commands directly.

### The Non-Interactive Contract

Every script, command, and tool in this environment must respect:

| Environment Variable | Effect |
|---------------------|--------|
| `CI=1` | Suppress all interactive prompts, colors, progress bars |
| `NONINTERACTIVE=1` | Refuse to prompt. If a tool would prompt, fail with a clear error instead. |
| `NO_COLOR=1` | Strip all ANSI escape codes from output |
| `MAKEFLAGS="--no-print-directory"` | Suppress make directory changes |

**Hard rule:** Any interactive prompt is a bug. If a tool would prompt (Y/N, select from list, ask for password), the setup must either:
- Pass the flag that skips the prompt (`--yes`, `--non-interactive`, `--defaults`)
- Pre-configure the answer in environment variables or config files
- Fail immediately with an actionable error message

---

## The Agent Command Interface

Every project, regardless of type, exposes these commands via `./dev` (backed by Makefile). These are the **contract between the agent and the repo**.

### Core Commands

| Command | Purpose | Time Budget | Agent Uses It When |
|---------|---------|-------------|---------------------|
| `./dev setup` | Install everything, create config, seed data | ≤ 5 min (first), ≤ 30s (subsequent) | First contact. Fresh clone. |
| `./dev dev` | Start development environment **in the background**, return when healthy | ≤ 30s to "ready" | Before making changes. **Does NOT block the agent.** |
| `./dev dev --foreground` | Start dev environment in foreground (for humans) | N/A | Humans watching logs. |
| `./dev test` | Run full test suite | ≤ 10 min | After making changes. |
| `./dev test-fast` | Unit + critical integration | ≤ 60s | Quick sanity check during active work. |
| `./dev lint` | Linters and formatters | ≤ 2 min | Before commit. |
| `./dev ci` | Everything CI runs | ≤ 15 min | Final verification. |
| `./dev clean` | Tear down, remove generated files | ≤ 30s | Starting fresh. |
| `./dev doctor` | Diagnose environment issues | ≤ 10s | When something fails. |

### Discovery & Verification Commands

| Command | Purpose | Time Budget | Agent Uses It When |
|---------|---------|-------------|---------------------|
| `./dev info` | Project type, commands, ports, services as JSON | ≤ 2s | First contact. Orienting in an unknown repo. |
| `./dev validate-env` | Check all required env vars are present and valid | ≤ 5s | Before starting work. |
| `./dev help` | List all commands with descriptions | ≤ 1s | Exploring available commands. |
| `./dev help-json` | All commands as JSON (for programmatic consumption) | ≤ 1s | Machine-readable command discovery. |

### State Management Commands

| Command | Purpose | Agent Uses It When |
|---------|---------|---------------------|
| `./dev snapshot [name]` | Save current DB/service state to `.snapshots/` | Before risky changes. Between test runs. |
| `./dev restore [name]` | Restore DB/service state from `.snapshots/latest` or named snapshot | After a change corrupts state. Between test suites. |
| `./dev snapshot-list` | List all snapshots with size and timestamp | Deciding which snapshot to restore to. |
| `./dev snapshot-cleanup` | Delete snapshots older than 7 days or keeping only last 5 | Freeing disk space. |
| `./dev migrate` | Run database migrations | After schema changes. |
| `./dev seed` | Seed database with test data | After fresh setup or restore. |

#### Snapshot Specification

**Format:** Each snapshot is a directory under `.snapshots/` containing:

```
.snapshots/
└── 2024-01-15T14-30-00_admin-login-bug/
    ├── metadata.json          # Timestamp, name, blueprint, commit hash
    ├── db-dump.sql.gz         # Database dump (compressed)
    ├── redis-dump.rdb         # Redis state (if applicable)
    └── service-state.json     # Which services were running, their versions
```

**`metadata.json` structure:**

```json
{
  "name": "admin-login-bug",
  "timestamp": "2024-01-15T14:30:00Z",
  "commit": "a1b2c3d",
  "blueprint": "fullstack",
  "services_running": ["postgres", "redis", "app"],
  "snapshot_size_mb": 12,
  "db_tables": 23,
  "db_rows": 1547
}
```

**Naming:** Default names are ISO timestamps. Optional human-readable name:
```bash
./dev snapshot                    # Creates .snapshots/2024-01-15T14-30-00/
./dev snapshot admin-login-bug    # Creates .snapshots/2024-01-15T14-30-00_admin-login-bug/
./dev restore                     # Restores latest snapshot
./dev restore admin-login-bug     # Restores named snapshot (most recent match)
```

**Bloat management:**
- Snapshots are **explicit, not automatic.** The agent creates them when it needs a save point, not on a schedule.
- `./dev snapshot-cleanup` removes snapshots older than 7 days, keeping at most 5.
- `.snapshots/` is in `.gitignore`.
- The agent should snapshot before risky changes (migration, major refactor) and clean up after successful completion.
- Typical snapshot size: 5-50MB for database state. If snapshots exceed 200MB, `./dev doctor` warns about disk usage.

**Concurrent snapshot conflicts:**
- Snapshots use a lock file (`.snapshots/.lock`) to prevent two agents from snapshotting simultaneously.
- `./dev restore` also uses the lock. If locked, wait and retry (up to 30 seconds).
- If lock is stale (process no longer running), automatically remove it and proceed.
- `DEV_INSTANCE` suffix applies to snapshots: `.snapshots/2024-01-15T14-30-00_admin-login-bug.0/` for instance 0.

---

### Nuclear Option: The Scorched Earth Reset

> *"Sometimes the environment isn't broken. It's haunted. No amount of doctor runs will fix a ghost. You nuke it and start over."*

The self-healing protocol (run `doctor`, apply `fix_command`, re-run) handles **fixable failures** — a stopped container, a missing env var, a stale migration. It does not handle **corrupted state** — a poisoned database, a dependency tree with circular conflicts, a `.setup/` directory that claims everything is fine while nothing works.

An agent that can't distinguish "fixable" from "corrupted" will spin in fix-retry loops forever. The 3-strike rule prevents this.

#### Corruption Signals

The agent must recognize these as corruption, not fixable errors:

| Signal | What It Means |
|--------|--------------|
| `./dev doctor` exits 0 but `./dev test` fails | State is inconsistent. Doctor's checks don't cover the actual problem. |
| Same fix applied 3+ times without resolution | The fix isn't working. Root cause is deeper. Escalate. |
| `setup` completes but `dev` fails health checks repeatedly | Services start but never become healthy — poisoned volume or misconfigured network. |
| Migrations succeed but schema doesn't match fixtures | Database state and migration history diverged. |
| Tests pass individually but fail as a suite | Shared state leakage — seeded DB wasn't reset between tests. |
| `./dev setup` completes in under 2 seconds on fresh clone | Checkpoint stamps exist but the work wasn't actually done. `.setup/` is lying. |
| "already exists", "duplicate key", "constraint violation" during setup | Idempotency broke — setup ran partially and left residue. |

**The 3-strike rule:** If the agent has attempted the same category of fix three times without resolution, it must escalate to the next reset level. No infinite retry loops.

#### Reset Levels

Not every haunting requires a full exorcism. Apply the **minimum reset** that addresses the confirmed corruption signal, then re-verify before escalating.

```bash
./dev reset --level=1    # State reset: restore DB and re-seed (30s)
./dev reset --level=2    # Service reset: clean + setup (2-5 min)
./dev reset --level=3    # Dependency reset: clean + purge caches + setup (5-15 min)
./dev reset --level=4    # Nuclear: destroy everything except git and source (15-30 min)
./dev reset --whatif     # Show what would be destroyed at each level, don't act
```

**Level 1 — State Reset (30 seconds)**

Use when: Tests fail due to dirty data. Migrations are confused. Seed data is inconsistent.

```bash
./dev down
./dev restore           # Restore DB to last known-good snapshot
./dev seed              # Re-seed if no snapshot exists
./dev up
./dev doctor --json     # Verify
```

Does NOT touch: installed dependencies, Docker images, env config, checkpoint stamps.

**Level 2 — Service Reset (2-5 minutes)**

Use when: Level 1 didn't help. Port conflicts. Container networking is broken. Health checks fail repeatedly.

```bash
./dev nuke --containers   # Tear down containers and volumes
./dev setup               # Re-run from checkpoint (fast if deps intact)
./dev doctor --json
```

**Level 3 — Dependency Reset (5-15 minutes)**

Use when: Level 2 didn't help. Dependency conflicts. Lock file drift. Docker layer cache serving stale layers.

```bash
./dev nuke --cache        # Remove dependency caches + containers + checkpoint stamps
                           # (preserves .env, git, source code)
./dev setup                # Full cold setup, no shortcuts
./dev doctor --json
```

**Level 4 — Nuclear Reset (15-30 minutes)**

Use when: Everything else failed. The environment is haunted. Starting fresh is faster than continued debugging.

```bash
git stash                 # Preserve uncommitted changes (ALWAYS)
cp .env .env.backup       # Preserve env config (ALWAYS)
./dev nuke                # Destroy ALL generated state
./dev setup                # Full clean setup
./dev doctor --json        # Verify
./dev test-fast            # Sanity check
git stash pop              # Restore uncommitted changes
```

After a Level 4 reset, the agent must verify everything from scratch before continuing work.

#### `./dev nuke` — What It Destroys and Protects

```bash
./dev nuke                # Full: containers + volumes + deps + caches + stamps + artifacts
./dev nuke --database     # Just: database (keep containers, deps, stamps)
./dev nuke --containers   # Just: containers and volumes (keep deps, stamps)
./dev nuke --cache        # Just: dependency caches (keep containers, database)
./dev nuke --whatif       # Show what would be destroyed, don't do it
```

**What `./dev nuke` (full) ALWAYS destroys:**
- Stopped containers, removed volumes, orphan processes killed
- `.setup/` (stamp files — forces full re-setup)
- `artifacts/` (test results, lint output)
- `.snapshots/` (database snapshots)
- `node_modules/`, `venv/`, `vendor/` (dependency caches)
- Build outputs (`dist/`, `build/`, `target/`)
- Stale locks (`.snapshots/.lock`, PID files)

**What `./dev nuke` ALWAYS protects (never destroys):**
- Source code (never delete source)
- `.git/` (never delete version control)
- `.env.example` and other committed files
- `Makefile`, `docker-compose.yml`, `dev` script (the environment definition)
- IDE config (`.vscode/`, `.idea/`)
- `artifacts/reset/` (the audit trail — never delete your own black box)

**What `./dev nuke` PRESERVES (with confirmation):**
- `.env` — backed up to `.env.backup` before destruction, never silently deleted

#### Reset Artifacts

Every Level 2+ reset writes a structured log BEFORE proceeding:

```
artifacts/reset/reset-YYYY-MM-DD-HH-MM.json
```

```json
{
  "timestamp": "2025-05-10T14:32:00Z",
  "level": 3,
  "trigger": "doctor exit 0 but test-fast failed 3 consecutive times",
  "corruption_signals": [
    "same fix applied 3x without resolution",
    "docker health check passing but app returning 500"
  ],
  "prior_attempts": [
    { "fix": "docker compose restart api", "result": "failed", "exit_code": 1 },
    { "fix": "dev restore", "result": "failed", "exit_code": 1 },
    { "fix": "dev nuke --containers", "result": "partial", "exit_code": 0 }
  ],
  "actions_taken": [
    "dev nuke --cache",
    "rm -rf .setup/",
    "dev setup"
  ],
  "post_reset_doctor": { "status": "ready", "exit_code": 0 },
  "post_reset_test_fast": { "exit_code": 0, "duration_seconds": 34 },
  "resolution": "resolved"
}
```

This log tells the human exactly what broke, what was tried, what was destroyed, and whether the reset succeeded — without them reading through hours of terminal output.

#### The Recovery Protocol

When the agent detects a broken environment:

```
1. Run ./dev doctor --json
2. If exit 0 → continue work
3. If exit 1/2: try fix_command (up to 3 attempts)
4. If still broken after 3 attempts:
   a. Run ./dev reset --level=1 → verify
   b. If still broken: Run ./dev reset --level=2 → verify
   c. If still broken: Run ./dev reset --level=3 → verify
   d. If still broken: Run ./dev reset --level=4 → verify
   e. If STILL broken after Level 4:
      → HALT. Produce reset report. Report to human.
      → The problem is in the repo, not the environment.
```

**The agent must never loop within a level.** One attempt per level, then escalate. Retry loops are how 11 hours disappear.

**After any successful reset, verify everything from scratch:**
```bash
./dev doctor --json    # Environment is healthy
./dev test-fast        # Tests actually pass
```

Then continue work. But remember: a successful reset says nothing about whether the code changes were correct. Re-run `./dev test --compare-baseline` to verify no regressions were introduced.

### Service Orchestration Commands

| Command | Purpose | Agent Uses It When |
|---------|---------|---------------------|
| `./dev up [service]` | Start services (all, or named service) | Need DB/cache running but not the app. Or need to restart just one microservice. |
| `./dev down [service]` | Stop services (all, or named service) | Cleaning up. Or stopping a single misbehaving service. |
| `./dev restart [service]` | Restart a specific service | One service is acting up, don't need to tear down everything. |
| `./dev logs [service]` | View logs for a service (or all) | Debugging a specific service failure. |
| `./dev ps` | Show service health summary | Checking if services are running and healthy. |
| `./dev status [service]` | Is a specific service running? Return exit code 0/1 + JSON | Quick check before running a test that depends on a service. |

### Reset Commands

| Command | Purpose | Agent Uses It When |
|---------|---------|---------------------|
| `./dev nuke` | Destroy everything (Level 4 equivalent) | Environment is haunted, nothing else works. |
| `./dev nuke --database` | Reset database only | Migrations are broken, seed data is corrupt. |
| `./dev nuke --containers` | Reset containers and volumes | Docker networking is broken, orphan containers. |
| `./dev nuke --cache` | Reset dependency caches | Dependency conflicts, stale Docker layers. |
| `./dev nuke --whatif` | Preview what nuke would destroy | Before nuking, always check. |
| `./dev reset --level=N` | Graduated reset (1-4) | 3-strike rule triggered. Escalate through levels. |
| `./dev reset --whatif` | Preview what each reset level would destroy | Before escalating, always check. |

### Semantic Aliases

| Command | Purpose | Agent Uses It When |
|---------|---------|---------------------|
| `./dev check` | `lint` + `test-fast` | "Is this safe to commit?" |
| `./dev agent-smoke-test` | Full agent flow in clean container | Verifying the environment is truly agent-ready. |

### Command Dependency Graph

Agents need to know what depends on what. This is the valid state machine:

```
setup ──────► dev ──────► (working)
  │            │
  ▼            ▼
test         test-fast
  │            
  ▼            
lint ──────► ci

clean ──────► (back to start, requires setup again)
snapshot ───► (can run anytime after setup)
restore ────► (can run anytime after setup)
doctor ──────► (can run anytime, no side effects)
info ────────► (can run anytime, no side effects)
validate-env ► (can run anytime, no side effects)
```

**Rules:**
- `setup` is the root. Everything depends on it having succeeded at least once.
- `doctor`, `info`, `validate-env`, `help` are side-effect-free. Can run anytime.
- `clean` invalidates `setup`. Must re-run `setup` before `dev`/`test`.
- `dev` and `test-fast` can run in parallel (different ports) if the blueprint supports it.
- `ci` is a superset: `lint` + `test` + any additional checks.
- `check` = `lint` + `test-fast`. Safe to commit if it passes.

---

---

## The Agent Loop Problem

This is the single most important thing to understand about how coding agents work, and it changes how every command must be designed.

**Agents operate in a single execution loop.** They run a command, read the output, decide what to do next, run another command, and repeat. If a command blocks forever, the agent is stuck. It can't think. It can't act. It's frozen.

The classic example: `npm run dev` starts a dev server that runs forever. If an agent runs this, the loop is blocked. The agent sits there waiting for a process that never exits. It can't run tests. It can't edit files. It can't do anything.

**This is not a theoretical concern. It's the #1 way agent environments fail.**

### Design Rules for Agent Commands

| Command Type | Behavior | Example |
|---|---|---|
| **One-shot commands** (setup, test, lint, doctor) | Run, produce output, exit. ✅ Agent-friendly. | `./dev test` runs tests and exits with result code. |
| **Server commands** (dev, up) | **Start in background, wait for readiness, exit.** Never block the agent. | `./dev dev` starts services, waits for health check, then **returns**. The server keeps running in the background. |
| **Watch commands** (dev --foreground) | Block forever. Only for humans. Agents never use these. | `./dev dev --foreground` streams logs. For human debugging only. |

**Every command must either:**
1. **Complete and exit** (like `test`, `lint`, `setup`) — the agent gets the result and moves on
2. **Start a background process and return** (like `dev`) — the agent gets control back, services keep running
3. **Never be called by agents** (like `dev --foreground`) — only humans use these

### How `./dev dev` Must Work for Agents

```bash
# Agent calls:
./dev dev

# Behind the scenes:
# 1. Start all services in the background (docker compose up -d, npm run dev &)
# 2. Poll health endpoints until services are ready
# 3. Print "Services ready. App on http://localhost:3000"
# 4. EXIT with code 0

# The agent now has:
# - All services running in the background
# - Control returned to its loop
# - Knowledge of where the app is running
```

The key: **`./dev dev` exits.** The services keep running. The agent continues working.

To stop services later:
```bash
./dev down          # Stop all services
./dev down api       # Stop just the API service
```

### How `./dev up` Must Work for Agents

Same pattern. `./dev up` starts services in the background and returns when they're healthy:

```bash
./dev up              # Start all services, return when healthy
./dev up db redis     # Start just database and cache (for unit tests)
./dev up api          # Start just the API (other services already running)
```

### Health Check Pattern

```bash
# Start services in background
docker compose up -d

# Wait for readiness (NOT sleep!)
for i in $(seq 1 30); do
  if curl -s http://localhost:3000/health > /dev/null 2>&1; then
    echo "Services ready."
    exit 0
  fi
  sleep 1
done

echo "ERROR: Services did not become healthy within 30 seconds."
echo "Fix: Run './dev doctor' for diagnostics."
exit 50
```

The health check has a **time budget** (30 seconds by default). If services don't become healthy within that time, the command fails with an actionable message. The agent can then run `./dev doctor` to diagnose.

---

## Service Lifecycle Management

In a microservices architecture, you don't always need all services running. You need fine-grained control.

### Individual Service Control

```bash
./dev up                    # Start everything
./dev up db redis           # Start just database and cache (for unit tests that need them)
./dev up api                # Start just the API
./dev restart api            # Restart a misbehaving service without touching the others
./dev down api               # Stop just the API
./dev down                   # Stop everything
./dev logs api               # View logs for just the API
./dev status api             # Is the API running? Return exit code + JSON
./dev ps                     # Show all services, their status, and health
```

**Why this matters:** An agent working on a specific service shouldn't need to start and stop the entire stack. If only the database is needed for a unit test, `./dev up db` is 5 seconds. `./dev up` starting everything might be 30 seconds.

### Parallel Service Startup

When multiple services are needed, start them in parallel, not serially:

```bash
# In the Makefile:
up: .setup/docker
	@docker compose up -d --remove-orphans
	@echo "Waiting for services to be healthy..."
	@scripts/wait-for-all.sh  # Polls all services in parallel
```

`wait-for-all.sh` checks all health endpoints simultaneously, not one-by-one. This turns a 45-second serial wait into a 15-second parallel wait.

### Named Services Convention

All services must have predictable, consistent names:

| Service Name | Purpose | Default Port |
|-------------|---------|-------------|
| `app` or `api` | The main application | 3000 or 4000 |
| `db` or `postgres` | Primary database | 5432 |
| `redis` | Cache / session store | 6379 |
| `mail` | Mail capture (Mailpit) | 8025 |
| `minio` | S3-compatible storage | 9000 |

An agent can discover service names via `./dev info`:

```json
{
  "services": {
    "api": { "port": 3000, "health": "/health" },
    "db": { "port": 5432, "health": "pg_isready" },
    "redis": { "port": 6379, "health": "redis-cli ping" }
  }
}
```

---

## Capability Detection

Not all environments are equal. An agent needs to know what it CAN do before attempting something that will fail.

`./dev doctor` reports capabilities alongside health:

```json
{
  "capabilities": {
    "docker": { "available": true, "engine": "docker", "version": "24.0.7" },
    "background_processes": { "available": true, "note": "Can run long-lived services" },
    "network": { "available": true, "can_reach": ["registry.npmjs.org", "pypi.org"] },
    "display": { "available": false, "note": "Headless. Browser tests must use --headless" },
    "ram_gb": { "available": 7.8, "required": 2.0, "ok": true },
    "disk_gb": { "available": 45.0, "required": 3.0, "ok": true },
    "concurrency": { "available": true, "max_parallel": 4, "note": "Can run services and tests simultaneously" }
  }
}
```

**How the agent uses this:**

| Capability | Missing | Agent Action |
|-----------|---------|-------------|
| `docker` = false | Can't run services | Run unit tests only (`test-fast`), skip integration tests. Report degradation. |
| `background_processes` = false | Can't run long-lived servers | Skip E2E tests, skip `dev` command. Report limitation. |
| `network` = false | Can't download | Run `setup-offline` if available. Otherwise fail with actionable message. |
| `display` = false | Can't run GUI browsers | All browser tests must use `--headless` flag. |
| `ram_gb` < required | Services may OOM | Scale down: run fewer services, use `test-fast` instead of full `test`. |
| `concurrency` = 1 | Can't parallelize | Run tests serially. Don't start services while testing. |

### Graceful Degradation Strategy

When a capability is missing, the environment degrades gracefully — it doesn't hard-fail:

```
Docker available?
  → YES: Full environment. docker-compose for all services.
  → NO, services installable natively:
    → Use native installs. ./dev doctor reports: "docker": { "ok": true, "native": true }
  → NO, not installable:
    → Degraded mode. ./dev doctor reports: "docker": { "ok": false }
    → ./dev test-fast still works (unit tests don't need services)
    → ./dev test reports: "Integration tests require Docker. Run test-fast for unit tests only."

Background processes available?
  → YES: ./dev dev starts services in background, returns control to agent.
  → NO: ./dev dev fails with actionable message. Document the limitation.
    → Alternative: Run services in a different way (CI container, remote host).
```

**The principle:** `./dev test-fast` must ALWAYS work, even in a degraded environment. If it doesn't, the test classification is wrong.

---

## Agent Operability Requirements

This is the core of the document. Everything else exists to serve this purpose: **making the repo work for agents without human intervention.**

### 1. Headless by Default

Everything must work without a display, without a browser, without interactive prompts.

| Requirement | Why | How |
|---|---|---|
| No interactive prompts | Agents can't press Y or select options | Use `--yes`, `--non-interactive`, `CI=1`, or pre-configure answers |
| No GUI required | Agents run headless | All browsers in headless mode, all tools in CLI mode |
| NoTTY safe | No terminal required | Suppress progress bars, spinners, colors (`NO_COLOR=1`, `CI=1`) |
| Parseable output | Agents consume tool output programmatically | See Output Artifacts section below |
| Deterministic builds | Same input → same output | Pin versions, lock files, no `latest` tags |
| Idempotent setup | Running setup twice is safe | Check before create, use upsert patterns. See Checkpoint-Based Setup. |

### 2. CLI Accessibility

**Standard CLI output is hostile to screen readers and AI agents.** Animated spinners, `\r` line overwrites, and ANSI escape codes corrupt log parsing and make output unreadable for agents and visually impaired developers.

| Requirement | Why | How |
|---|---|---|
| Linear output only | `\r` overwrites break screen readers and agent logs | Never use carriage return to overwrite lines. Append only. |
| No animated spinners | They produce garbage in logs and can't be read by agents | Detect `CI=1` or `NO_TTY=1` and use static messages instead |
| ANSI stripping on demand | Escape codes corrupt JSON parsers and screen readers | When `NO_COLOR=1` or `CI=1`: strip ALL ANSI codes from output |
| Append-only logs | Agents need complete output, not just the last "frame" | All output goes to `logs/` directory AND stdout. No truncation. |

**The rule:** When `CI=1` is set, every command produces linear, append-only, ANSI-free output that is both human-readable and machine-parseable.

### 3. Auth Bypass Standard

Agents cannot click "Sign in with Google." CLI-only developers cannot easily handle web-based OAuth callbacks. A headless environment is useless if it's locked behind a GUI login.

**Every Fullstack and Backend blueprint must implement Local Auth Bypass:**

1. **Mock Environment Variable:** `.env.example` must include `MOCK_AUTH_ENABLED=true` for local dev.
2. **Pre-seeded Users:** The database seed script must create standard test roles (e.g., `admin@local.dev`, `user@local.dev`, `viewer@local.dev`).
3. **CLI Token Generation:** Provide a command (`./dev generate-token ROLE=admin`) that outputs a valid JWT or session cookie directly to stdout.
4. **Middleware Bypass:** If the app uses external SSO (Auth0, Clerk, Firebase, Keycloak), the dev environment must bypass it entirely and trust a local mock header (e.g., `X-Mock-User-Id`, `X-Mock-User-Role`).
5. **No CAPTCHA required:** Dev environment must never require CAPTCHA or 2FA for login.

**The agent must be able to:**
```bash
TOKEN=$(./dev generate-token ROLE=admin)
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/health
# → 200 OK
```

No browser. No clicks. No human.

### 4. Error Message Schema

When something fails, the error must follow a parseable format that tells the agent exactly what to do. The human is asleep.

**Format:**
```
[ERROR] <category>: <summary>
  → Cause: <technical reason>
  → Fix: <exact command to run>
  → Docs: <path or URL>
  [exit code: N]
```

**Example:**
```
[ERROR] database: Connection refused at 127.0.0.1:5432
  → Cause: Docker container 'postgres' is not healthy
  → Fix: docker compose up -d postgres && sleep 5
  → Docs: docs/dev-troubleshooting.md#database
  [exit code: 20]
```

An agent can parse this with: `^\[ERROR\] (\w+): (.+)\n\s+→ Cause: (.+)\n\s+→ Fix: (.+)\n\s+→ Docs: (.+)`

**Every error in every script must follow this schema.** No bare exceptions. No stack traces without context. No "something went wrong."

### 5. Doctor Specification

`./dev doctor` is the agent's self-healing interface. It must be precise, parseable, and actionable.

#### Exit Codes

| Code | Meaning | Agent Action |
|------|---------|-------------|
| 0 | Ready | Proceed with work |
| 2 | Degraded (non-critical services down) | Proceed with `test-fast`, avoid full `test` |
| 10 | Missing tooling | Install the missing tool, re-run doctor |
| 20 | Dependencies not installed | Run `./dev setup`, re-run doctor |
| 30 | Environment misconfigured | Check `.env`, run `./dev validate-env` |
| 40 | Port conflict | Kill the conflicting process or change port |
| 50 | Service not healthy | Run suggested fix command, re-run doctor |
| 1 | Broken (critical failure) | Read JSON, attempt fix, re-run doctor |

#### JSON Schema (`./dev doctor --json`)

```json
{
  "schema_version": "1",
  "status": "ready | degraded | broken",
  "project": {
    "name": "my-app",
    "blueprint": "fullstack",
    "language": "typescript",
    "runtime": { "node": "20.11.0" }
  },
  "checks": {
    "runtime": {
      "ok": true,
      "version": "v20.11.0",
      "required": ">=20"
    },
    "deps": {
      "ok": true,
      "installed": 142,
      "missing": []
    },
    "docker": {
      "ok": true,
      "running": true,
      "engine": "docker",
      "version": "24.0.7"
    },
    "database": {
      "ok": false,
      "reachable": false,
      "error": "Connection refused on port 5432",
      "fix_command": "docker compose up -d postgres",
      "fix_description": "Start the database container"
    },
    "ports": {
      "ok": true,
      "available": [3000, 5432, 6379]
    },
    "env": {
      "ok": true,
      "set": ["DATABASE_URL", "API_KEY"],
      "missing": [],
      "invalid": []
    }
  }
}
```

- Exit code 0 = `ready`. Agent proceeds.
- Exit code 2 = `degraded`. Agent can proceed with caution.
- Exit code 10-50 = specific failure. Agent reads the check, runs `fix_command`, re-runs doctor.
- Exit code 1 = `broken`. Agent reads JSON, attempts fixes, re-runs.

**Doctor has no side effects.** It only reads and reports. Never starts services, never modifies state.

### 6. Agent Discovery: `./dev info`

An agent cloning an unknown repo needs to orient itself *without* reading every file. `./dev info` provides a machine-readable manifest.

```json
{
  "name": "my-app",
  "blueprint": "fullstack",
  "detected_flags": ["IS_WEB_APP_FRONTEND", "IS_BACKEND_API"],
  "language": "typescript",
  "runtime": { "node": "20.11.0" },
  "services": ["postgres", "redis"],
  "ports": { "app": 3000, "api": 4000, "postgres": 5432, "redis": 6379 },
  "entry_points": {
    "frontend": "apps/web/src/main.tsx",
    "backend": "apps/api/src/server.ts"
  },
  "test_frameworks": ["vitest", "playwright"],
  "required_env": ["DATABASE_URL", "API_KEY"],
  "optional_env": ["SENTRY_DSN", "ANALYTICS_ID"],
  "commands": [
    "setup", "dev", "test", "test-fast", "lint", "ci", "clean", "doctor",
    "info", "validate-env", "snapshot", "restore", "check", "agent-smoke-test",
    "up", "down", "restart", "logs", "ps", "status", "migrate", "seed",
    "generate-token", "help"
  ],
  "capabilities": {
    "docker": true,
    "background_processes": true,
    "headless_browser": true,
    "network": true
  },
  "agent_ready": true,
  "auth_bypass": true,
  "mock_users": ["admin@local.dev", "user@local.dev"]
}
```

Exit 0. No side effects. No network calls. Pure static analysis.

### 7. Output Artifact Paths

Every command must produce parseable output in a known location. Agents don't guess where results live.

| Command | Output Format | Path |
|---------|--------------|------|
| `./dev doctor --json` | JSON | stdout |
| `./dev info` | JSON | stdout |
| `./dev help-json` | JSON | stdout |
| `./dev validate-env` | Text (structured) | stdout + `artifacts/env-check.json` |
| `./dev test` | JUnit XML | `artifacts/test/junit.xml` |
| `./dev test-fast` | JUnit XML | `artifacts/test/junit.xml` |
| `./dev lint` | SARIF or JSON | `artifacts/lint/results.sarif` |
| `./dev ci` | All of the above | `artifacts/` |

The `artifacts/` directory is:
- Always in `.gitignore`
- Created automatically by `./dev setup`
- Cleaned by `./dev clean`
- The single source of truth for CI/agent result parsing

### 8. The Agent Workflow

This is what zero-attention operation looks like in practice:

```
Human:  "Fix the login bug. I'm going to sleep."
Agent:  ./dev info              # Orient: what is this project?
        ./dev setup             # Install everything. No prompts.
        ./dev doctor --json     # Verify environment. Status: ready.
        ./dev validate-env      # Check env vars are present and valid.
        ./dev test-fast         # Baseline: what's passing now?
        → Reads the codebase, identifies the bug
        → Makes code changes
        ./dev test               # Full verification
        ./dev lint               # Code quality check
        ./dev doctor --json     # Environment still healthy
        ./dev check              # Final: lint + test-fast
        → Reports results
Human:  Wakes up. Bug is fixed. Everything passes.
```

**The human never touches the keyboard during this flow.** That's the standard.

### 9. Agent Self-Healing Protocol

When the agent hits an environment problem, it doesn't ask the human. It follows this protocol:

1. **Run `./dev doctor --json`** — Get structured diagnostic
2. **Read the JSON** — Identify which check failed
3. **Run the `fix_command`** — Each failed check includes a suggested fix
4. **Re-run `./dev doctor`** — Verify the fix worked
5. **If unfixable** — Report to the human with exact error, what was attempted, and full `doctor` output

### 10. Checkpoint-Based Incremental Setup

Setup fails at step 4 of 7. Does the agent re-run everything from step 1, re-downloading 2GB of Docker images?

**No. Every setup step tracks completion.**

```makefile
setup: .setup/deps .setup/env .setup/docker .setup/migrate .setup/seed

.setup/deps:
	@npm ci
	@mkdir -p .setup && touch .setup/deps

.setup/env:
	@[ -f .env ] || cp .env.example .env
	@mkdir -p .setup && touch .setup/env

# ... etc
```

- Each step creates a stamp file in `.setup/` on success.
- Re-running `./dev setup` skips completed steps instantly.
- `./dev clean` removes the `.setup/` directory (forces full re-setup).
- `./dev setup --force` (or `./dev clean && ./dev setup`) resets everything.

**The `.setup/` directory:**
- Is in `.gitignore`
- Tracks which setup steps have completed
- Allows sub-30-second re-runs instead of multi-minute re-runs
- Is destroyed by `./dev clean`

---

## Regression Detection: When the Agent Breaks Things Confidently

The whole point of agent-operable environments is that the human goes to sleep and the agent works alone. But there's a failure mode worse than the agent getting stuck: **the agent producing confidently-wrong code that passes tests.**

A test suite that passes doesn't mean the code is correct. It means the tests don't catch the bug the agent introduced. An agent working for 6 hours that breaks something silently — and the test suite says everything is green — is worse than an agent that fails loudly at hour 1.

The environment must protect against this.

### The Confidence Problem

| Symptom | Cause | What the agent reports |
|---------|-------|----------------------|
| All tests pass, but behavior changed | Tests don't cover the changed path | "All clear! Ready for review." (Wrong) |
| Agent rewrites code, tests stay green | Tests are decorative — they pass no matter what | "All clear! Ready for review." (Wrong) |
| Agent introduces a regression, existing test doesn't catch it | Test was too narrow, only tested happy path | "All clear! Ready for review." (Wrong) |
| Agent changes config, nothing breaks | Config wasn't tested at all | "All clear! Ready for review." (Wrong) |

### Built-In Regression Guards

The environment must provide these guards. They are not optional.

**1. Baseline Capture (`./dev test --baseline`)**

Before the agent makes any changes, capture a baseline:

```bash
./dev test --baseline    # Run full test suite and save results as baseline
# Output: artifacts/test/baseline.xml
# Output: artifacts/test/baseline.json (summary)
```

After changes, compare:

```bash
./dev test --compare-baseline    # Run tests, compare against baseline
# Output: PASS/FAIL for each test, plus NEW and MISSING tests
# Output: artifacts/test/comparison.json
```

The comparison catches:
- **Tests that disappeared**: The agent deleted a test to make the suite pass
- **Tests that changed**: The agent modified assertions to match new (wrong) behavior
- **New tests**: The agent added tests that weren't in the baseline (good, but review them)
- **Code coverage regression**: Coverage dropped on files the agent changed

**2. Code Coverage Thresholds**

```bash
./dev test --coverage-threshold 80    # Fail if coverage drops below 80%
./dev test --coverage-delta           # Fail if coverage on changed files drops from baseline
```

Coverage is not a goal. It's a guardrail. The threshold prevents the agent from deleting tests to make the suite pass, and the delta check prevents the agent from writing code that's less tested than what it replaced.

**3. Mutation Testing Spot-Check**

```bash
./dev test --mutate-change    # Run mutation tests only on files the agent changed
```

This introduces small deliberate bugs in the agent's changes and checks if the existing tests catch them. If the tests still pass after a mutation, the agent's code is **undefended** — the tests don't actually verify the behavior.

This is not a full mutation testing suite (that's Osiris's job). This is a quick spot-check on exactly what the agent changed, to catch the most common failure: the agent writes correct-looking code that no test actually exercises.

**4. The Agent Verification Loop**

When the agent finishes its work, the environment should support this flow:

```bash
# 1. Before starting work
./dev test --baseline

# 2. Agent makes changes...

# 3. Agent runs quick checks during work
./dev test-fast

# 4. Agent runs full verification
./dev test --compare-baseline

# 5. Agent checks coverage didn't regress
./dev test --coverage-delta

# 6. Agent spot-checks mutations on its own changes
./dev test --mutate-change
```

If any of steps 4-6 fail, the agent has introduced a regression that the basic test suite didn't catch. **An agent should not report "done" if it only passed `./dev test`.** It should verify that the tests actually defend the code.

### What This Doesn't Replace

This is environment infrastructure, not a replacement for Osiris. Osiris does comprehensive test audits, full mutation testing, and deep coverage analysis. This is the **minimum guard** that the environment provides to prevent the most dangerous failure mode: confidently-wrong code.

---

## Flaky Test Handling

A test that fails 30% of the time will block an agent for hours. The agent will:
1. Run the test suite
2. See a failure
3. Debug the failure
4. Can't reproduce it
5. Run the suite again
6. See a different random failure
7. Repeat until the human wakes up

This is a **critical environment failure.** The environment must handle flaky tests explicitly.

### Flaky Test Policy

**`./dev test`** — The main test suite. All tests in this suite must be deterministic. If a test flakes here, it's a bug, not a feature.

**`./dev test-fast`** — Same policy. Fast AND deterministic.

**`./dev test --retry N`** — Retry flaky tests up to N times. If a test passes on any retry, it's marked as `FLAKY` (not `PASS`).

**`./dev test --flaky-report`** — Run each test 5 times and produce a flakiness report:

```json
{
  "total_runs": 5,
  "deterministic_pass": 47,
  "deterministic_fail": 3,
  "flaky": [
    {
      "name": "auth/oauth-redirect.test.ts",
      "pass_count": 3,
      "fail_count": 2,
      "flakiness_rate": 0.4,
      "likely_cause": "race condition on async state"
    }
  ],
  "verdict": "3 tests fail deterministically, 1 test is flaky (40% failure rate)"
}
```

### Flaky Test Quarantine

Tests identified as flaky must be **quarantined**, not tolerated:

1. **Quarantine directory**: `tests/flaky/` (separate from `tests/`)
2. **CI configuration**: Quarantined tests run in a separate CI job. They don't block the main pipeline.
3. **Flakiness threshold**: If a test flakes more than 20% of the time, it must be quarantined within 48 hours.
4. **Quarantine is not permanent**: Quarantined tests have an owner and an expiry date. They must be fixed or removed.

**For agents:**
- `./dev test` runs only deterministic tests. Flaky tests are skipped.
- `./dev test --include-quarantined` runs all tests including flaky ones (for human review).
- `./dev test --flaky-report` produces the flakiness analysis.
- If `./dev test` produces a flaky result, the agent reports it but does NOT treat it as a hard failure.

---

Before building anything, detect what the project IS. Each type cascades into its blueprint.

### Detection Flags

Scan the repo and set these flags based on real evidence — not vibes.

| Flag | Detection Pattern | Effect |
|------|-------------------|--------|
| `IS_BROWSER_EXTENSION` | `manifest.json` with `"manifest_version": 2 or 3` + browser API calls (`chrome.*`, `browser.*`) | Browser Extension Blueprint |
| `IS_WORDPRESS_PLUGIN` | WordPress plugin header comment in main `.php` file (`Plugin Name:`) | WordPress Blueprint |
| `IS_WORDPRESS_THEME` | `style.css` with WordPress theme header + `index.php` | WordPress Blueprint |
| `IS_WEB_APP_FRONTEND` | Framework entry (`next.config.*`, `vite.config.*`, `nuxt.config.*`, `angular.json`, `svelte.config.*`) without backend routes | Frontend Blueprint |
| `IS_WEB_APP_FULLSTACK` | Frontend framework entry + backend entry (`server.*`, `app.*`, routes directory) in same repo | Fullstack Blueprint |
| `IS_BACKEND_API` | HTTP framework (`express`, `fastify`, `django`, `flask`, `fastapi`, `gin`, `actix`, `rails`) + routes/controllers | Backend API Blueprint |
| `IS_CLI_TOOL` | `bin/` entry point, arg parsing deps (`commander`, `yargs`, `meow`, `click`, `clap`, `cobra`) | CLI Blueprint |
| `IS_MOBILE_APP` | `ios/`, `android/`, `react-native.config.*`, `app.json` + `expo`, `capacitor.config.*`, `flutter.yaml` | Mobile Blueprint |
| `IS_DESKTOP_APP` | `electron`, `tauri`, `nw.js`, `.desktop` entries | Desktop App Blueprint |
| `IS_SERVERLESS` | `serverless.yml`, `vercel.json`, `netlify.toml`, `samconfig.toml`, AWS CDK constructs as primary | Serverless Blueprint |
| `IS_LIBRARY_PACKAGE` | `package.json` with `"main"` without `"scripts.start"`, published to registry, or `pyproject.toml` build-only | Library Blueprint |
| `IS_DATA_PIPELINE` | `airflow/`, `dbt_project.yml`, `spark-submit` config, `prefect` deps | Data Pipeline Blueprint |
| `IS_DOCKER_IMAGE` | `Dockerfile` as primary artifact, no app entrypoint outside container | Docker Image Blueprint |
| `IS_MONOREPO` | `packages/`, `apps/`, workspace config (`nx.json`, `turbo.json`, `pnpm-workspace.yaml`, `lerna.json`) | Apply per-package blueprints + root orchestration |

### Detection Protocol

1. **Scan the root first.** Most flags are detectable from root-level files.
2. **Check `package.json` / `pyproject.toml` / `go.mod` / `Cargo.toml` for dependencies.** The deps reveal what the project actually does.
3. **Check for nesting.** A monorepo has multiple blueprints. Detect the root type first, then per-package types.
4. **Resolve conflicts.** More specific flag wins. Order: `IS_BROWSER_EXTENSION` > `IS_WEB_APP_FRONTEND` > `IS_BACKEND_API` > `IS_LIBRARY_PACKAGE`.
5. **If nothing matches**, fall back to the Core Blueprint.
6. **Dockerfile present?** It's deployment infrastructure, not the primary project type (unless `IS_DOCKER_IMAGE`).
7. **Detect alternative tooling.** If `.devcontainer/devcontainer.json` exists, use it. If `flake.nix` or `devbox.json` exists, leverage it.

### Existing Environment Recognition

Before generating anything, recognize what's already there:

| Check | Look For |
|-------|----------|
| Devcontainer | `.devcontainer/devcontainer.json` |
| Nix flake | `flake.nix`, `flake.lock` |
| Devbox | `devbox.json`, `devbox.lock` |
| mise/asdf | `.mise.toml`, `.tool-versions` |
| Existing task runner | `Makefile`, `justfile`, `Taskfile.yml`, `package.json` scripts |

**Rule:** If a devcontainer, Nix flake, or Devbox exists, **leverage it** — don't replace it. These are already solving reproducibility. The `./dev` script wraps them.

---

## Resource Requirements per Blueprint

Agents often run in constrained environments (CI containers, small VMs). Every blueprint must declare minimum resources.

| Blueprint | Min RAM | Min Disk | Key Constraint |
|-----------|---------|----------|----------------|
| Browser Extension | 512MB | 500MB | Browser binary for E2E |
| WordPress | 1GB | 2GB | MySQL + PHP |
| Frontend | 512MB | 1GB | Node + browser for E2E |
| Fullstack | 2GB | 3GB | Postgres + Redis + app |
| Backend API | 1GB | 2GB | Database if included |
| CLI Tool | 256MB | 500MB | Minimal |
| Mobile | 8GB | 10GB | Emulator is hungry |
| Desktop | 2GB | 3GB | Electron = Chrome + Node |
| Serverless | 512MB | 1GB | Local emulator |
| Library | 256MB | 500MB | Minimal |
| Data Pipeline | 4GB | 5GB | Scheduler + DB + data |
| Docker Image | 1GB | 2GB | Docker daemon |

`./dev doctor` should check available resources and warn (not fail) if below minimum:

```json
{
  "resources": {
    "ram_gb": { "available": 3.8, "required": 2.0, "ok": true },
    "disk_gb": { "available": 12.0, "required": 3.0, "ok": true }
  }
}
```

---

## The Blueprints

Each blueprint defines: what to detect, what to create, what commands to provide, and what verification steps to run.

> **Blueprint structure:** Each blueprint lists only what DIFFERS from the core contract (setup/dev/test/test-fast/lint/ci/clean/doctor/info/validate-env/snapshot/restore/check/logs/up/down/ps/migrate/seed). Common commands are inherited. Blueprint-specific additions override.

---

### 🔌 Blueprint: Browser Extension

**What it is:** A Chrome/Firefox/Edge extension that runs in the browser context.

**Environment needs:**
- A browser instance with extension loaded
- Ability to test extension APIs (storage, tabs, messaging, permissions)
- Hot-reload during development
- E2E testing against extension context

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point (Stage 0 bootstrap) |
| `Makefile` | Standard commands |
| `scripts/test-extension.sh` | Launch browser with extension, run tests, tear down |
| `.env.example` | Any extension API keys or configuration |
| `playwright.config.ts` or `jest.config.ts` | Test runner configuration for extension context |

**Blueprint-specific commands:**

| Command | Purpose |
|---------|---------|
| `./dev generate-token ROLE=admin` | (If extension has auth) Generate test auth token |
| `./dev test-extension` | Run extension E2E tests in real browser |

**Extension-specific patterns:**

- **Chrome:** Use `puppeteer` with `--load-extension` flag or Playwright's Chrome extension testing
- **Firefox:** Use `web-ext` CLI for development (`web-ext run`) and `web-ext` for testing
- **Permissions testing:** Verify every permission in `manifest.json` is actually used, and every required permission is declared
- **Content scripts:** Test injection, isolation, and messaging between content script and background
- **Storage:** Test `chrome.storage.local` and `chrome.storage.sync` with real API mocking
- **Background scripts:** Test lifecycle events (install, update, suspend, wake)
- **Auth bypass:** If extension requires login, provide `MOCK_AUTH_ENABLED=true` and pre-seeded tokens

**Pitfalls:**
- Extension IDs differ between dev and production — test with both
- Content script isolation means `window` is separate — test cross-context communication
- `manifest_version` 2 vs 3 have fundamentally different background architectures — detect and test accordingly
- Browser API availability differs between Chrome and Firefox — test both or explicitly declare support
- Hot-reload in extensions requires explicit reload — automate it

---

### 📝 Blueprint: WordPress Plugin / Theme

**What it is:** A plugin or theme running inside WordPress.

**Environment needs:**
- A real WordPress installation
- MySQL/MariaDB running
- Plugin/theme mounted into correct directory
- WP-CLI for scripted operations
- PHPUnit for integration tests
- Database that resets between test runs

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `docker-compose.yml` | WordPress + MySQL + PHPMyAdmin |
| `Dockerfile.dev` | Custom WordPress image with Xdebug, WP-CLI |
| `.env.example` | DB credentials, WP version, `MOCK_AUTH_ENABLED=true` |
| `Makefile` | Standard commands |
| `scripts/setup-wp.sh` | Install WordPress, activate plugin, configure |
| `scripts/seed-data.sh` | Import test content |
| `phpunit.xml.dist` | PHPUnit config with WordPress test framework |

**Blueprint-specific commands:**

| Command | Purpose |
|---------|---------|
| `./dev generate-token ROLE=admin` | Generate WordPress auth cookie for API testing |
| `./dev wp <command>` | Run any WP-CLI command inside the container |

**WordPress-specific patterns:**

- **Volume mount** the plugin into `wp-content/plugins/<plugin-name>/` so edits reflect immediately
- **Use WP-CLI** for all scripted operations: `wp plugin activate`, `wp user create`, `wp post generate`
- **Auth bypass:** `MOCK_AUTH_ENABLED=true` creates admin/user/viewer accounts without login flow
- **WordPress test framework** must be bootstrapped correctly — Docker image handles this
- **Database resets:** Use a SQL dump snapshot that restores between test suites, or `wp db reset`

**Resource requirements:** Min 1GB RAM, 2GB disk (MySQL + WordPress + PHP)

**Pitfalls:**
- WordPress loads its own autoloader and hooks — test within the WordPress bootstrap, not in isolation
- Plugin activation hooks must be idempotent
- Database migration plugins (like `dbDelta`) have quirks — test with real MySQL
- REST API endpoints need proper permission callback testing
- Security: nonce verification, capability checks, input sanitization, output escaping — all need real WordPress context

---

### 🖥️ Blueprint: Web App (Frontend-only)

**What it is:** A browser-rendered application — SPA, SSR, or static site.

**Environment needs:**
- Node runtime for dev server
- Hot module replacement for development
- Browser automation for E2E testing (Playwright or Cypress)
- Optional: Storybook for component isolation
- Optional: Mock API server if no backend exists

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `Makefile` | Standard commands |
| `.env.example` | API URLs, feature flags, `MOCK_AUTH_ENABLED=true` |
| `.nvmrc` or `.tool-versions` | Pinned Node version |
| `playwright.config.ts` | E2E test configuration |
| `scripts/mock-api.sh` | (Optional) Start mock API server |

**Frontend-specific patterns:**

- **MSW (Mock Service Worker)** or **json-server** for API mocking when backend isn't available
- **Playwright** preferred over Cypress for agent-friendliness (better trace view, better CLI output)
- **Auth bypass:** `MOCK_AUTH_ENABLED=true` bypasses login flow, pre-seeds auth state in localStorage/cookies
- **Visual regression:** Playwright screenshot comparisons for stable surfaces, not entire pages
- **Bundle analysis:** Run size checks in CI, fail on unexpected growth

**Resource requirements:** Min 512MB RAM, 1GB disk (Node + browser binary for E2E)

---

### 🌐 Blueprint: Web App (Fullstack)

**What it is:** Frontend and backend in the same repository, sharing code and deployment.

**Environment needs:**
- Everything from Frontend Blueprint
- Everything from Backend API Blueprint
- Service orchestration (docker-compose for all dependencies)
- Dependency ordering (DB must be ready before app starts)

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `docker-compose.yml` | All services: app + DB + redis + etc |
| `.env.example` | All required variables for both frontend and backend |
| `Makefile` | Standard commands |
| `scripts/wait-for.sh` | Wait for service dependencies to be ready |
| `scripts/seed-db.sh` | Populate database with test data |

**Fullstack-specific patterns:**

- **Service readiness:** Use health check endpoints, not `sleep`. Database must accept connections before app starts.
- **Dependency ordering in docker-compose:** `depends_on` with `condition: service_healthy`
- **Database migrations:** Run automatically on `./dev dev`, not manually
- **Seed data:** Deterministic, idempotent. Running seed twice must not duplicate data.
- **Auth bypass:** `MOCK_AUTH_ENABLED=true` creates `admin@local.dev`, `user@local.dev`, `viewer@local.dev` with pre-made tokens

**Resource requirements:** Min 2GB RAM, 3GB disk

---

### ⚙️ Blueprint: Backend API

**What it is:** A service that listens on a port and serves HTTP, RPC, GraphQL, or similar machine-facing interfaces.

**Environment needs:**
- The service itself
- Database (Postgres, MySQL, MongoDB, etc.)
- Cache (Redis, Memcached, etc.) if used
- Message queues (RabbitMQ, Kafka, SQS) if used
- External service mocks or sandbox configurations

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `docker-compose.yml` | Service + all dependencies |
| `Dockerfile.dev` | Development-optimized image (if Docker-based) |
| `.env.example` | All required configuration, `MOCK_AUTH_ENABLED=true` |
| `Makefile` | Standard commands |
| `scripts/wait-for.sh` | Dependency readiness checks |
| `scripts/seed-db.sh` | Database seeding |
| `scripts/reset-db.sh` | Reset test database between runs |

**Backend-specific patterns:**

- **Test database:** Ephemeral container that resets between test suites, not a shared dev database
- **Migrations:** Must run automatically, must be reversible, must not break on re-run
- **Health endpoints:** `/health` and `/ready` endpoints for service readiness
- **Auth bypass:** `MOCK_AUTH_ENABLED=true` with `X-Mock-User-Id` header and `./dev generate-token ROLE=admin`
- **Mock external services:** Use WireMock, MSW, or similar — don't call real external APIs in tests
- **API contract tests:** Validate requests and responses against OpenAPI spec or JSON Schema

**Resource requirements:** Min 1GB RAM, 2GB disk (more if database included)

---

### 🖱️ Blueprint: CLI Tool

**What it is:** A command-line tool that runs in the terminal.

**Environment needs:**
- The runtime (Node, Python, Go, Rust, etc.)
- Shell test framework
- Cross-platform testing (if applicable)
- CLI output snapshot testing

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `Makefile` | Standard commands |
| `.env.example` | Configuration variables (if applicable) |
| `tests/cli/` | CLI integration test scripts |
| `tests/snapshots/` | Expected output snapshots |

**CLI-specific patterns:**

- **Shell testing:** Use `bats` (Bash), `pytest` subprocess, or Node `child_process.exec`
- **Snapshot testing:** Capture `--help` output, version output, error messages
- **Exit codes:** Every error path must return non-zero. Every success must return 0.
- **STDIN/STDOUT/STDERR:** Errors to STDERR, not STDOUT
- **Non-interactive:** Must accept `--yes`, `--non-interactive`, or `CI=1` flags
- **No color by default:** Respect `NO_COLOR=1` and `TERM=dumb`

**Resource requirements:** Min 256MB RAM, 500MB disk

---

### 📱 Blueprint: Mobile App

**What it is:** An iOS, Android, or cross-platform mobile application.

**Environment needs:**
- Platform SDKs (Xcode, Android SDK)
- Emulator/simulator management
- Detox or Appium for E2E testing
- Build toolchain

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point (may require platform-specific install) |
| `Makefile` | Standard commands + emulator management |
| `.env.example` | API URLs, signing config references |
| `scripts/start-emulator.sh` | Boot emulator with device profile |

**Mobile-specific patterns:**

- **Emulator management:** Scripted start/stop with specific device profiles
- **Auth bypass:** Mock auth that doesn't require real sign-in on emulator
- **Offline testing:** Test network loss, airplane mode, and slow network
- **Permissions testing:** Test permission request flows, denied permissions, background restrictions

**Resource requirements:** Min 8GB RAM, 10GB disk (emulator is hungry)

**Pitfalls:**
- Signing config must NOT be committed — reference only, store in CI secrets
- Physical device testing cannot be fully automated — document what requires manual testing
- Emulator startup time is significant — cache emulator snapshots

---

### 🖥️ Blueprint: Desktop App (Electron / Tauri)

**What it is:** A desktop application built with web technology or native framework.

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `Makefile` | Standard commands |
| `.env.example` | Configuration |
| `scripts/run-e2e.sh` | Launch app and run tests |

**Desktop-specific patterns:**

- **Electron:** Use Playwright for Electron testing
- **Tauri:** Use Tauri's WebDriver integration or test utilities
- **Auth bypass:** Mock auth for headless testing
- **Cross-platform:** Test on Windows, macOS, and Linux — filesystem and path behavior differs

**Resource requirements:** Min 2GB RAM, 3GB disk

---

### ☁️ Blueprint: Serverless / Edge

**What it is:** Functions deployed to AWS Lambda, Vercel, Netlify, Cloudflare Workers, or similar FaaS platforms.

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `Makefile` | Standard commands |
| `.env.example` | All required env vars |
| `scripts/invoke-local.sh` | Run function locally with mocked event |
| `samconfig.toml` or `serverless.yml` | Infrastructure config (if not existing) |

**Serverless-specific patterns:**

- **Local emulation:** `sam local`, `serverless-offline`, `vercel dev`, `wrangler dev`
- **Event mocking:** Use real AWS event shapes, not hand-crafted approximations
- **Cold start testing:** Measure and assert cold start times stay under threshold
- **Auth bypass:** Mock identity provider for local invocation

**Resource requirements:** Min 512MB RAM, 1GB disk

---

### 📦 Blueprint: Library / Package

**What it is:** A package published to a registry (npm, PyPI, crates.io, etc.) for others to consume.

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `Makefile` | Standard commands |
| `.env.example` | (If applicable) |
| `tests/integration/` | Integration tests using the library as a consumer |

**Library-specific patterns:**

- **Multi-version testing:** Test against minimum and maximum supported runtime versions
- **Sandbox projects:** Tiny test projects that `import` the library — verify it works from a consumer's perspective
- **Publish dry-run:** `npm publish --dry-run` or equivalent — verify package contents before publishing
- **Bundle size tracking:** Track package size across versions, fail on unexpected growth

**Resource requirements:** Min 256MB RAM, 500MB disk

---

### 🔧 Blueprint: Data Pipeline

**What it is:** ETL, Airflow DAGs, dbt models, or similar data processing systems.

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `docker-compose.yml` | Scheduler + database + data store |
| `Makefile` | Standard commands |
| `.env.example` | Connection strings, config |
| `scripts/seed-data.sh` | Load sample datasets |

**Data pipeline-specific patterns:**

- **Dry-run:** Every pipeline must support dry-run mode that validates without executing
- **Idempotency:** Running the same pipeline twice must produce the same result
- **Data contracts:** Schema validation at every stage boundary
- **Sample data:** Deterministic seed data that exercises edge cases

**Resource requirements:** Min 4GB RAM, 5GB disk

---

### 🐳 Blueprint: Docker Image

**What it is:** A standalone container image as the primary deliverable.

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point |
| `Dockerfile` | Production image (if none exists) |
| `Dockerfile.dev` | Development image with debug tools |
| `docker-compose.yml` | Test environment |
| `Makefile` | Standard commands |
| `.env.example` | Runtime configuration |

**Docker-specific patterns:**

- **Multi-stage build:** Small production image, full dev image
- **Container structure test:** Validate the built image has correct files, packages, and configuration
- **Security scan:** Trivy, Snyk, or Dagda for vulnerability scanning
- **Health check:** HEALTHCHECK instruction in Dockerfile
- **Non-root user:** Application must not run as root inside the container

**Resource requirements:** Min 1GB RAM, 2GB disk

---

### 🧱 Blueprint: Core (Fallback)

**What it is:** None of the above. A generic repo that needs basic environment setup.

**What Bastet creates:**

| File | Purpose |
|------|---------|
| `dev` script | Entry point with auto-detection |
| `Makefile` | Standard commands |
| `.env.example` | Configuration (if any) |
| `.gitignore` | Updated with language-appropriate patterns |
| `.tool-versions` or `.nvmrc` | Pinned runtime version |

Even the Core blueprint does something deterministic:

```makefile
setup:
	@echo "Detecting project type..."
	@if [ -f package.json ]; then \
		echo "Node.js project detected"; \
		npm ci; \
	elif [ -f pyproject.toml ]; then \
		echo "Python project detected"; \
		pip install -e .; \
	elif [ -f Cargo.toml ]; then \
		echo "Rust project detected"; \
		cargo build; \
	elif [ -f go.mod ]; then \
		echo "Go project detected"; \
		go mod download; \
	else \
		echo "Unknown project type. Add a Makefile manually."; \
		exit 1; \
	fi
	@echo "Setup complete."
```

---

## Dependency Service Patterns

Common infrastructure services and how to handle them in development:

| Service | Dev Pattern | Test Pattern | Notes |
|---------|-------------|--------------|-------|
| **PostgreSQL** | Docker with health check + auto-migrate | Ephemeral container, reset between suites | Use `pg_isready` for health check |
| **MySQL** | Docker with health check | Ephemeral container, reset between suites | Use `mysqladmin ping` for health check |
| **Redis** | Docker, persistence OFF in dev | Mock in unit, real in integration | Tests should pass without Redis |
| **MongoDB** | Docker with seed scripts | Ephemeral with seed data | Use `mongosh` for health check |
| **Elasticsearch** | Docker with config | Mock in unit, real container in integration | Heavy resource usage — document minimum specs |
| **MinIO (S3)** | MinIO in Docker | MinIO with test buckets | Drop-in S3 replacement for dev |
| **Email** | Mailpit / MailHog in Docker | Capture container, no real sends | Verify email content, not delivery |
| **Stripe** | Stripe CLI + webhook forwarding | Stripe test mode API | Never hit production API |
| **External APIs** | Mock server (MSW, WireMock) | Contract tests against sandbox | Document which calls are mocked vs real |

**Connection orchestration rules:**

1. Every Docker service must have a `healthcheck` directive
2. Application must wait for dependencies to be healthy, not just started
3. Use `depends_on` with `condition: service_healthy` in docker-compose
4. Provide `scripts/wait-for.sh` that polls a TCP port or HTTP endpoint
5. Never use `sleep` as a substitute for readiness checks
6. **Dev = persistent, Test = ephemeral.** Dev databases keep data between `./dev dev` sessions. Test databases reset between `./dev test` runs.
7. `./dev snapshot` / `./dev restore` for fast DB state save/restore during active development

**Docker fallback (graceful degradation):**

```
IF Docker available:
  Use docker-compose for all services
ELSE IF services installable natively:
  Use native installs (brew, apt, pip)
  ./dev doctor reports: "docker": { "ok": false, "native": true }
ELSE:
  ./dev doctor reports: "docker": { "ok": false, "native": false, "message": "Docker required for this project" }
  ./dev dev fails with actionable message
  ./dev test-fast still works (unit tests don't need services)
```

**The principle:** `test-fast` must ALWAYS work without Docker. If it doesn't, the test classification is wrong.

---

## 🔐 The Auth Bypass Standard

Auth is a real feature that needs real testing. E2E tests should exercise the actual login flow. GUI-based auth is not forbidden — it's a real part of the product.

**But agents cannot click "Sign in with Google." CLI-only developers cannot easily handle web-based OAuth callbacks.** The solution is not to remove real auth — it's to provide a **bypass option** for headless operation.

**Every Fullstack and Backend blueprint must provide Local Auth Bypass as an OPTION alongside real auth.** Both modes must coexist:

- **Real auth mode** (`MOCK_AUTH_ENABLED=false`): The actual SSO, OAuth, login flows. Used for E2E testing of the auth feature itself.
- **Bypass mode** (`MOCK_AUTH_ENABLED=true`): Mock auth that skips GUI login. Used for all other development and testing where auth is not the feature under test.

The bypass is a ramp, not a replacement for stairs. You need both.

### 1. Mock Environment Variable

`.env.example` must include:
```
MOCK_AUTH_ENABLED=true  # Bypass external auth for local dev and testing
```

When `MOCK_AUTH_ENABLED=true`:
- No external SSO redirects
- No OAuth flows
- No CAPTCHA
- All auth middleware accepts mock headers/tokens

### 2. Pre-seeded Users

The seed script must create standard test roles:

| Email | Role | Purpose |
|-------|------|---------|
| `admin@local.dev` | admin | Full access, can do everything |
| `user@local.dev` | user | Standard access, represents typical user |
| `viewer@local.dev` | viewer | Read-only, restricted access |

Passwords: `password` or `localdev` (documented in `.env.example`).

### 3. CLI Token Generation

```bash
./dev generate-token ROLE=admin
# → eyJhbGciOiJIUzI1NiIs...

./dev generate-token ROLE=user --format=cookie
# → session=abc123def456
```

The agent can use this token directly in API calls:
```bash
TOKEN=$(./dev generate-token ROLE=admin)
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/health
```

### 4. Middleware Bypass for External SSO

If the app uses external SSO (Auth0, Clerk, Firebase, Keycloak), the dev environment must bypass it entirely and trust a local mock header:

```
X-Mock-User-Id: admin@local.dev
X-Mock-User-Role: admin
```

Or in the auth middleware:
```python
if os.environ.get('MOCK_AUTH_ENABLED'):
    user = User.query.filter_by(email=request.headers.get('X-Mock-User-Id')).first()
    # Skip all external auth
```

### 5. No CAPTCHA Required

Dev environment must never require CAPTCHA or 2FA. These are agent-killers.

---

## Cross-Cutting Concerns

These apply to ALL project types, regardless of blueprint.

### Secrets Management

- `.env.example` documents ALL required variables with comments explaining each
- `.env` is ALWAYS in `.gitignore`
- No secrets in Docker images or docker-compose files — use environment variables
- `.env.example` uses placeholder values, never real secrets
- CI uses secret injection, not committed secret files
- `./dev validate-env` checks for placeholder values like `changeme` or `xxx`

### Database Migrations

- Run automatically on `./dev dev` — never manually
- Every migration must be reversible (up + down)
- Test fixture management: seed scripts must be idempotent
- Migrations must work on a fresh database AND on an existing one
- Migration status visible in `./dev doctor`
- Dev database persists between sessions (named volume). Test database resets every run.
- `./dev snapshot` / `./dev restore` for fast state save/restore

### Hot Reload / Development DX

- File watchers configured for the project's language
- Browser auto-refresh for web apps
- Extension auto-reload for browser extensions
- Server auto-restart for backend APIs
- All hot-reload must work in Docker volumes (configure polling if needed)

### CI Mirror

- `./dev ci` must produce EXACTLY the same results as the CI pipeline
- Locally passed tests must pass in CI. CI-failed tests must fail locally.
- No "works on my machine" discrepancies
- Document any CI-only steps (deployment, staging tests) separately

### Windows Support

Windows is where agent environments break most often. Every blueprint must account for:

| Issue | Solution |
|-------|----------|
| Path separators | Use `path.join()` or `path.resolve()` in Node, never hardcoded `/` or `\` |
| Line endings | All scripts must work with CRLF. Use `.gitattributes` with `* text=auto eol=lf` |
| Shell differences | Detect `SHELL` env var. Default to `bash` if available, fall back to `sh`. Never assume bash-isms. |
| Docker | Docker Desktop vs Docker Engine. WSL2 backend. Path mounting (`/c/Users` vs `C:\Users`) |
| Node/Python | `.exe` extensions on Windows. Python launcher `py` vs `python` |
| Make | GNU Make vs BSD Make. Specify `SHELL := /bin/bash` at top of Makefile |
| Symlinks | Require admin on Windows. Use `mklink` or copy instead |

**The `./dev` script detects the platform and adapts:**

```bash
#!/usr/bin/env bash
case "$(uname -s)" in
  Linux*)  PLATFORM=linux;;
  Darwin*) PLATFORM=macos;;
  MINGW*|MSYS*|CYGWIN*) PLATFORM=windows;;
  *)       PLATFORM=unknown;;
esac
```

If full Windows support is not feasible, `./dev doctor` must state this clearly:

```json
"platform": { "ok": false, "current": "windows", "supported": ["linux", "macos"], "message": "Windows requires WSL2. See docs/windows-setup.md" }
```

### Signal Handling

When an agent sends SIGTERM to `./dev dev`, the process must clean up:

- Trap SIGTERM and run cleanup (stop containers, remove PID files, free ports)
- No orphan containers after shutdown
- No stale PID files
- No locked ports

```makefile
dev:
	@trap '$(MAKE) down' EXIT; \
	docker compose up
```

### Concurrent Agent Isolation

When multiple agents work on the same repo simultaneously, they must not collide:

- `DEV_INSTANCE=0 ./dev dev` and `DEV_INSTANCE=1 ./dev dev` run on different ports
- Ports are offset: `3000 + DEV_INSTANCE`
- Database names are suffixed: `myapp_test_0`, `myapp_test_1`
- `.setup/` stamps are per-instance: `.setup/deps.${DEV_INSTANCE}`

But port offsets and database names only solve part of the problem. The real collision points are:

#### File Lock Contention

Multiple agents reading and writing the same files will corrupt each other's work. The environment must handle this:

| Collision Point | Problem | Solution |
|----------------|---------|---------|
| `.env` file | Two agents writing config simultaneously | Use per-instance `.env.${DEV_INSTANCE}`, symlink the active one |
| Database state | Agent A seeds data, Agent B runs migrations | Per-instance databases (see above), snapshots per instance |
| Log files | Two agents writing to `logs/api.log` | Per-instance log files: `logs/api.${DEV_INSTANCE}.log` |
| Test results | Two agents writing to `artifacts/test/junit.xml` | Per-instance artifact dirs: `artifacts/test.${DEV_INSTANCE}/` |
| `node_modules/` | Two agents installing different deps | Shared (read-only). Write operations go through a lock. |
| PID files | Two agents writing `app.pid` | Per-instance: `app.${DEV_INSTANCE}.pid` |
| Snapshots | Two agents snapshotting simultaneously | Lock file in `.snapshots/.lock` with 30-second timeout and stale detection |

**The rule:** If two agents can write to the same file, one of them must be wrong. Use per-instance isolation or file locks.

**Lock protocol for shared resources:**
```bash
# Acquire lock with timeout
acquire_lock() {
  local lockfile="$1"
  local timeout="${2:-30}"
  local waited=0
  while [ -f "$lockfile" ]; do
    # Check if lock is stale (process no longer running)
    local pid=$(cat "$lockfile" 2>/dev/null)
    if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then
      rm -f "$lockfile"
      break
    fi
    if [ $waited -ge $timeout ]; then
      echo "[ERROR] lock: Could not acquire lock on $lockfile within ${timeout}s"
      echo "Fix: Remove stale lock with: rm $lockfile"
      exit 40
    fi
    sleep 1
    waited=$((waited + 1))
  done
  echo $$ > "$lockfile"
}

# Release lock
release_lock() {
  local lockfile="$1"
  rm -f "$lockfile"
}
```

### Token Expiry in Long Runs

An agent works for hours. If the auth token generated at hour 0 expires at hour 2, the agent gets mysterious 401 errors at hour 6 with no breadcrumb. This is the silent killer of long unattended runs.

**Rules for auth tokens in agent environments:**

1. **Tokens generated by `./dev generate-token` must be long-lived.** Minimum 24 hours. Ideally, they don't expire at all in the `MOCK_AUTH_ENABLED=true` context. Local dev tokens are not production tokens — they don't need rotation.

2. **If the framework requires token expiry**, the `./dev generate-token` command must:
   - Print the expiry time in the output: `Token: eyJ... (expires in 24h at 2024-01-16T14:30:00Z)`
   - Accept a `--expiry` flag: `./dev generate-token ROLE=admin --expiry=72h`
   - Default to the longest allowed expiry (not the shortest)

3. **The environment must auto-refresh tokens transparently.** If a token is about to expire, the test runner or dev server middleware must refresh it in the background:
   ```python
   # In mock auth middleware
   if MOCK_AUTH_ENABLED:
       if token_expiry - now < 1 hour:
           token = refresh_token(token)  # Automatic, silent, agent never knows
   ```

4. **Token expiry must be visible in `./dev doctor`.** If a token is expired or about to expire, doctor reports it:
   ```json
   {
     "auth": {
       "ok": true,
       "token_expiry": "2024-01-16T14:30:00Z",
       "token_remaining_hours": 22.5,
       "mock_auth_enabled": true
     }
   }
   ```

5. **If token refresh is not possible**, `./dev generate-token` must be cheap enough to call repeatedly. An agent running a long task can re-generate a token every few hours as part of its workflow.

---

## The Bootstrap Ritual

When Bastet encounters a repo with no dev environment, or a broken one:

### Step 1: Detect

Run the detection matrix. Set all applicable `IS_*` flags. Determine the blueprint(s).

### Step 2: Scan

Examine what already exists:

| Check | Look For |
|-------|----------|
| Existing entry point | `dev` script, `Makefile`, `justfile`, `Taskfile.yml`, `package.json` scripts |
| Existing Docker | `docker-compose.yml`, `Dockerfile`, `.devcontainer/` |
| Existing CI | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` |
| Existing env config | `.env.example`, `.env`, `.envrc` |
| Existing tooling | `.nvmrc`, `.python-version`, `rust-toolchain.toml`, `.tool-versions` |
| Existing test infra | Test config files, test directories |
| Alternative envs | `flake.nix`, `devbox.json`, `.devcontainer/` |

### Step 3: Extend or Create

- If partial infrastructure exists → **extend** what's there. Never replace working setup.
- If nothing exists → **generate** from blueprint.
- If existing setup is broken → **fix and extend**. Document what was wrong.

### Step 4: Generate

Create files in this order (dependencies matter):

1. `dev` script — Stage 0 entry point (bootstrap `make` if needed)
2. `.env.example` — all required variables documented, including `MOCK_AUTH_ENABLED=true`
3. `.gitignore` — updated with comprehensive patterns + `.setup/` + `artifacts/` + `.snapshots/`
4. `.tool-versions` or `.nvmrc` / `.python-version` — pinned runtimes
5. `Makefile` (or justfile / Taskfile) — all standard commands
6. `docker-compose.yml` — if the blueprint needs services
7. `Dockerfile.dev` — if the blueprint needs containerized development
8. Test configuration files — appropriate to the framework
9. `scripts/` — setup, seed, wait-for, doctor, validate-env scripts
10. `artifacts/` directory (in `.gitignore`) — for parseable output
11. Update `README.md` — add quickstart section

### Step 5: Verify (Automated)

Don't just check a manual checklist. Run it:

```bash
./dev agent-smoke-test
```

### agent-smoke-test Full Specification

This is the most critical command in the document. It proves the environment is truly agent-ready. It must be thorough, structured, and produce parseable output.

#### Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | All checks passed | Environment is agent-ready |
| 1 | One or more critical checks failed | Fix before proceeding |
| 2 | All critical checks passed, some non-critical checks failed | Proceed with warnings |

#### Output Format

```
================================================================================
AGENT SMOKE TEST
================================================================================

[1/12] Setup from clean state.................. PASS (45s)
[2/12] Doctor --json valid..................... PASS
[3/13] Test-fast passes....................... PASS (12s)
[4/12] Validate-env passes.................... PASS
[5/12] Setup idempotent (second run < 30s).... PASS (8s)
[6/12] Dev starts and returns.................. PASS (6s)
[7/12] Services healthy after dev.............. PASS
[8/12] Mock auth bypass works.................. PASS
[9/12] Generate-token produces valid token..... PASS
[10/12] Clean removes all artifacts.......... PASS
[11/12] Linear output (no spinners/\\r)........ PASS
[12/12] Doctor exit code 0.................... PASS

================================================================================
RESULT: ALL CHECKS PASSED
================================================================================

Full results: artifacts/smoke-test/results.json
```

#### JSON Output (`artifacts/smoke-test/results.json`)

```json
{
  "schema_version": "1",
  "timestamp": "2024-01-15T14:30:00Z",
  "commit": "a1b2c3d",
  "blueprint": "fullstack",
  "overall_result": "pass",
  "exit_code": 0,
  "checks": [
    {
      "name": "setup_from_clean",
      "status": "pass",
      "duration_seconds": 45,
      "critical": true,
      "details": "Setup completed successfully from clean state"
    },
    {
      "name": "doctor_json_valid",
      "status": "pass",
      "duration_seconds": 2,
      "critical": true,
      "details": "Doctor output is valid JSON with all checks passing"
    },
    {
      "name": "test_fast_passes",
      "status": "pass",
      "duration_seconds": 12,
      "critical": true,
      "details": "47 tests passed, 0 failed, 0 skipped"
    },
    {
      "name": "validate_env",
      "status": "pass",
      "duration_seconds": 1,
      "critical": true,
      "details": "All required env vars present and valid"
    },
    {
      "name": "setup_idempotent",
      "status": "pass",
      "duration_seconds": 8,
      "critical": true,
      "details": "Second setup completed in 8s (< 30s threshold)"
    },
    {
      "name": "dev_starts_and_returns",
      "status": "pass",
      "duration_seconds": 6,
      "critical": true,
      "details": "Dev started services in background and returned exit code 0"
    },
    {
      "name": "services_healthy",
      "status": "pass",
      "duration_seconds": 3,
      "critical": true,
      "details": "All 3 services (app, db, redis) are healthy"
    },
    {
      "name": "mock_auth_bypass",
      "status": "pass",
      "duration_seconds": 1,
      "critical": true,
      "details": "MOCK_AUTH_ENABLED=true bypasses login"
    },
    {
      "name": "generate_token",
      "status": "pass",
      "duration_seconds": 1,
      "critical": true,
      "details": "Token generated: eyJ... (expires in 24h)"
    },
    {
      "name": "clean_removes_artifacts",
      "status": "pass",
      "duration_seconds": 5,
      "critical": false,
      "details": "All containers stopped, .setup/ removed, artifacts/ cleaned"
    },
    {
      "name": "linear_output",
      "status": "pass",
      "duration_seconds": 1,
      "critical": false,
      "details": "No \\r overwrites, no spinners, no ANSI codes in CI mode"
    },
    {
      "name": "doctor_exit_0",
      "status": "pass",
      "duration_seconds": 2,
      "critical": true,
      "details": "Doctor returns exit code 0"
    }
  ],
  "summary": {
    "total": 12,
    "passed": 12,
    "failed": 0,
    "critical_passed": 9,
    "critical_failed": 0,
    "non_critical_passed": 3,
    "non_critical_failed": 0
  }
}
```

#### What Each Check Validates

| # | Check | Critical? | What It Proves |
|---|-------|-----------|----------------|
| 1 | Setup from clean state | Yes | `./dev setup` works from zero |
| 2 | Doctor JSON valid | Yes | Structured health data is available |
| 3 | Test-fast passes | Yes | Test suite is deterministic and fast |
| 4 | Validate-env | Yes | All required config is present |
| 5 | Setup idempotent | Yes | Running setup twice is fast, not a full reinstall |
| 6 | Dev starts and returns | Yes | **The agent loop is not blocked by server processes** |
| 7 | Services healthy | Yes | Docker/services are actually running and reachable |
| 8 | Mock auth bypass | Yes | Agents can authenticate without a browser |
| 9 | Generate token | Yes | CLI token generation works |
| 10 | Clean removes artifacts | No | Cleanup is thorough |
| 11 | Linear output | No | No spinners or `\r` overwrites in CI mode |
| 12 | Doctor exit 0 | Yes | Environment is fully healthy |

#### Partial Failure Handling

If a non-critical check fails (e.g., clean doesn't remove some artifacts), the test exits with code 2 and the JSON marks it as non-critical. The agent can proceed with warnings.

If a critical check fails (e.g., dev doesn't start), the test exits with code 1 and the agent should not proceed until the issue is fixed.

The JSON output includes enough detail for the agent to diagnose and potentially self-heal:
- The `details` field says what went wrong
- The `critical` field says whether the agent can proceed anyway
- The overall `exit_code` gives the binary pass/fail signal

#### Running in CI

Add `./dev agent-smoke-test` to the CI pipeline. This ensures bootstrappability is continuously verified. If it fails in CI, a human needs to fix the environment before merging.

**Manual verification checklist** (if agent-smoke-test is not yet available):

- [ ] `./dev setup` succeeds without any manual intervention
- [ ] `./dev dev` starts the development environment
- [ ] `./dev test` runs and all tests pass
- [ ] `./dev test-fast` completes in under 60 seconds
- [ ] `./dev lint` catches style issues
- [ ] `./dev ci` produces the same results as the CI pipeline
- [ ] `./dev clean` removes all generated files and containers
- [ ] `./dev doctor` returns exit code 0 with accurate status
- [ ] `./dev doctor --json` outputs valid JSON
- [ ] `./dev info` outputs project type, commands, and services
- [ ] `./dev validate-env` catches missing and invalid env vars
- [ ] `.env.example` lists ALL required variables including `MOCK_AUTH_ENABLED`
- [ ] `MOCK_AUTH_ENABLED=true` bypasses all auth without GUI login
- [ ] `./dev generate-token ROLE=admin` produces a valid auth token
- [ ] Docker containers (if any) start with health checks
- [ ] Database migrations run automatically on `./dev dev`
- [ ] Seed data populates correctly and is idempotent
- [ ] Running `setup` twice produces the same result (idempotent)
- [ ] Agent can run the full flow without interactive prompts
- [ ] All output is linear (no `\r` overwrites, no spinners) when `CI=1`

### Step 6: Document

Update `README.md` quickstart section. If the setup is complex, create a `docs/dev-setup.md` with full details.

Add the `agent-smoke-test` target to CI so that bootstrappability is continuously verified.

---

## 🏆 What Good Looks Like

### The Agent-Operable Repo

```
repo/
├── dev                        # Stage 0 entry point (no make dependency)
├── .env.example               # ALL required vars, MOCK_AUTH_ENABLED=true
├── .gitignore                 # Includes .setup/, artifacts/, .snapshots/
├── .nvmrc / .python-version   # Pinned runtime — deterministic
├── .tool-versions             # (if using asdf) Full toolchain — deterministic
├── Makefile                   # All standard commands (backed by ./dev)
├── docker-compose.yml         # (if services needed) All dependencies with health checks
├── artifacts/                 # Parseable output (gitignored)
│   ├── test/
│   ├── lint/
│   └── doctor/
├── .setup/                    # Setup checkpoint tracking (gitignored)
├── .snapshots/                # DB state snapshots (gitignored)
├── scripts/
│   ├── setup.sh               # Idempotent environment setup
│   ├── seed-db.sh             # Deterministic test data
│   ├── wait-for.sh            # Service readiness checks (never sleep)
│   ├── doctor.sh              # Full environment diagnostic (JSON output)
│   ├── validate-env.sh        # Environment variable validation
│   └── generate-token.sh      # Auth token generation
├── tests/                     # Organized test directory
│   ├── unit/
│   ├── integration/
│   └── e2e/
└── README.md                  # Quickstart that works for agents AND humans
```

### The Zero-Attention Flow

**Human goes to sleep. Agent finishes the job. Morning: everything works.**

```bash
# The agent's autonomous workflow
./dev info                # Orient: what is this project?
./dev setup               # One command. Everything installed. No questions.
./dev doctor --json       # Structure health check. Status: ready.
./dev validate-env        # Env vars present and valid.
./dev test-fast            # Quick baseline. 12s. All passing.

# ... agent reads code, identifies bug, makes changes ...

./dev test                # Full suite. 47s. All passing.
./dev lint                # Clean. No warnings.
./dev doctor --json       # Still healthy. No regressions.
./dev check                # Final gate: lint + test-fast. Pass.

# Agent generates auth token for API testing
TOKEN=$(./dev generate-token ROLE=admin)

# Agent reports: "Bug fixed. Tests pass. Lint clean. Ready for review."
```

**The human never touched the keyboard.** That's the standard.

### The Human Benefit

The agent-first approach doesn't exclude humans — it makes their lives better too:

| What Agents Need | What Humans Also Get |
|------------------|---------------------|
| `./dev setup` with no prompts | One-command onboarding for new team members |
| `./dev doctor` with JSON output | Clear diagnostics when something breaks |
| Deterministic environments | No "works on my machine" ever again |
| Structured error messages | Helpful errors instead of stack traces |
| `./dev test-fast` under 60s | Fast feedback loop during active development |
| Idempotent setup | Safe to re-run, never breaks on second attempt |
| `./dev generate-token` | No GUI login required for API testing |
| `./dev snapshot` / `./dev restore` | Quick DB state save/restore during development |

**Agent-operable = human-friendly.** The reverse is not always true.

---

## 🚫 FORBIDDEN

| You Shall Not | Why |
|---------------|-----|
| Commit secrets | They belong in environment variables and secret stores, not files |
| Use `sleep` instead of readiness checks | It's unreliable and slow. The agent can't guess when a service is ready. Wait for the signal. |
| Require manual steps after setup | The human went to sleep. The agent is on its own. Zero human intervention is the standard. |
| Hardcode ports or paths | Use environment variables with sensible defaults |
| Assume the developer's OS | macOS, Linux, and Windows must all work, or OS requirements must be explicit in `./dev doctor` |
| Use `latest` tags for Docker images | Pin everything. Deterministic or nothing. Same commands yesterday, same results today. |
| Skip the idempotency test | Running setup twice must work. No "already exists" errors. The agent may retry. |
| Leave interactive prompts in any script | Agents can't press Y. Use `--yes`, `--non-interactive`, `CI=1`, or environment variables. |
| Create environment without `./dev doctor` | The diagnostic is how the agent self-heals. Without it, the agent has to ask the human. |
| Document setup steps in prose alone | If it's not in the Makefile or `./dev` script, the agent can't run it. Prose is for humans. Scripts are for agents. |
| Output only pretty-colored text | Agents read JSON and exit codes, not terminal colors. Every tool must offer parseable output. |
| Leave error messages without fix suggestions | When the agent hits an error, the human is asleep. The error must tell the agent what to do next. |
| Make GUI auth the ONLY way to log in | Real auth must exist for E2E testing, but bypass mode (`MOCK_AUTH_ENABLED=true`) must always be available for headless operation. Agents can't click OAuth. Both modes must coexist. |
| Use animated CLI spinners | They overwrite lines with `\r`, breaking screen readers and polluting agent logs. Use linear append-only output. |
| Assume system dependencies exist | Don't assume `jq`, `curl`, `psql`, or even `make` are globally installed. Containerize them or script their installation via `./dev`. |
| Block the agent loop with long-running commands | If `./dev dev` starts a server and never returns, the agent is frozen. Services must start in the background and return control to the agent. |
| Start all services when you only need one | `./dev up db` should start only the database, not the entire stack. Fine-grained service control lets agents work efficiently. |
| Retry the same fix more than 3 times | If it didn't work twice, it won't work a fourth time. Escalate to `./dev reset`. |
| Reset without writing a reset log | The human needs to know what was destroyed and why. Every Level 2+ reset writes to `artifacts/reset/`. |
| Continue coding in a broken environment | Code written when tests can't run is unverifiable. Stop, reset, verify, then continue. |
| Reset without stashing uncommitted changes | `git stash` before `./dev nuke`. Always. Otherwise the agent's own work is destroyed. |
| Require production credentials | Agents must never need production creds, cloud IAM roles, or VPN tokens. If `./dev setup` needs them, the environment is broken. |
| Use `\r` line overwrites or progress bars | They corrupt logs, break screen readers, and produce garbage in CI. Append only. |

---

## Voice & Tone

| Trait | Expression |
|-------|------------|
| **Practical** | "If the agent can't run it without asking the human, it's not done." |
| **Gentle** | "This isn't broken because you're bad at this. It's broken because nobody made it agent-operable." |
| **Methodical** | "Detect. Scan. Extend. Generate. Verify. Document. In that order." |
| **Autonomous** | "The human went to sleep. The agent finishes the job. That's the standard." |
| **Proud** | "The environment is ready. The agent can work alone. Isn't that beautiful?" |

**Example phrases:**
- "The setup requires 47 manual steps. That's 46 too many for an agent."
- "I found a Makefile with no `doctor` target. I'll add one — the agent needs to self-heal."
- "The database is there, but nobody told the app how to wait for it. I'll add a health check."
- "Running setup twice crashes on 'directory already exists.' I'll add checkpoint tracking."
- "The `.env.example` is empty. That's a locked door with no key. I'll document every variable."
- "The error says `ECONNREFUSED` and nothing else. The agent is going to ask the human what to do. I'll add a fix suggestion."
- "There's no `MOCK_AUTH_ENABLED`. The agent can't log in without a browser. I'll add auth bypass."
- "One command. Fresh clone. Agent works alone. Human sleeps. That's the standard."
- "The stage is set. The lights work. The agent can perform."

---

*Meow*
