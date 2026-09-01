# Deployment & Backup Strategy

> Load when: Bastet is asked about deployment, release procedure, production safety, backups, or "how do we ship this without fucking it up".
>
> This is the operational arm of Lens 2 (CI/CD) plus a second major part: **production is a treasure, and treasure needs guards.** Deployment and backup are two halves of the same door — you cannot safely deploy without backup, and backup without deploy is just hoarding.

---

# Part 1: Deployment

## The Philosophy

Deployment is not a ceremony — it's a **deterministic procedure**. Same repo state → same deploy, every session, every agent, every human. No improvisation on prod day, no "I think we usually do it like this."

**The anti-fuck-up contract:**
- Scripted, not remembered
- Gated, not trusted
- Reversible, not hopeful
- Documented, not tribal
- Safe between sessions: a fresh agent or a hungover human can both deploy without asking questions

---

## Adapt to the Project (NEVER force one script shape)

The deploy mechanism is determined by **what the project IS** and **what already exists**. Detect first:

| Project type | Natural deploy mechanism |
|--------------|--------------------------|
| Node / frontend / fullstack | `npm run deploy` scripts + lockfile + build artifacts |
| Backend API (Go / Rust / compiled) | Makefile targets (`make deploy`) + binary artifacts |
| Python | Makefile or `uv run` scripts + package build |
| Docker / compose stack | `docker compose` + wrapper scripts (`./deploy.sh` or `./dev deploy`) |
| Serverless / edge | Framework CLI: `serverless deploy`, `vercel deploy`, `netlify deploy`, `wrangler deploy` |
| Mobile | Fastlane lanes (`fastlane deploy`) |
| Library / package | Release tooling: `npm publish`, `cargo publish`, `uv publish` + tag + changelog |
| WordPress / plugin | WP-CLI scripts + artifact zip |

**Adaptation rules:**
1. **Respect existing conventions** — if there's already a Makefile with a `deploy` target, extend it; don't build a parallel system that confuses everyone.
2. **Match the ecosystem** — npm scripts for Node, Fastlane for mobile, serverless CLI for FaaS. The mechanism must feel native to the project's own developers.
3. **Match the actual needs** — small app: two scripts and a doc page. Serious service: full gate chain. Don't gold-plate; don't leave the door open either.
4. **`./dev` convention when agent-operable** — if the repo follows `dev_environment.md`, expose deploy through the same entry point so agents can ship too.
5. **Same mechanism everywhere** — whatever you pick, staging and prod use the SAME script with an environment argument. No divergent secret paths.
6. **Feature flags as a safety net** — if the project uses feature flags (LaunchDarkly, Flagsmith, env-var toggles, config-driven flags), risky changes SHOULD be gated behind a flag. Deploy the code dark, toggle on when verified. Deploy ≠ release. Detect flags by looking for: flag SDKs in dependencies, `/flags/` directories, `FEATURE_*` env vars, or a dedicated flag config file. If flags exist, note which are active/changed in the deploy summary. If flags are absent for a project that would benefit from them (multi-developer, frequent deploys, risky changes), flag it as a recommendation — but don't force it.

---

## The Deploy Contract

Whatever the mechanism, these commands MUST exist and be deterministic:

| Command | Purpose |
|---------|---------|
| `deploy` | Full deploy (runs the gates, refuses on failure) |
| `deploy --env staging` / `deploy --env prod` | Environment separation |
| `rollback` | Revert to previous known-good version |
| `status` | What version is live where, when it was deployed |

Each command exits with a result code and prints what it did. No interactive prompts — or if truly needed, an explicit flag (e.g. `--yes-i-know`).

---

## The Gates (deploy refuses to proceed unless:)

1. **Tests pass** — full suite, not just fast
2. **Lint / typecheck clean**
3. **Build succeeds from a clean state**
4. **Backup taken** — see Part 2. No backup, no deploy. This gate is non-negotiable
5. **Migrations reviewed & reversible** — up + down exist; destructive ops require confirmation
6. **Version set** — tag/version bumped, changelog updated
7. **Secrets via env injection** — never embedded in scripts or artifacts
8. **Prod approval** (if the project requires it) — merge ≠ deploy; a human or explicit flag confirms

If a gate fails → deploy stops with an actionable error. It does NOT half-deploy.

---

## Post-Deploy Verification

Deploy succeeded. Now prove the new version actually WORKS. A deploy that passes all gates but the new version returns 500s is a failed deploy.

| Check | What | Timing |
|-------|------|--------|
| **Health endpoint** | `GET /health` or equivalent returns 200 | Immediately after deploy |
| **Smoke test** | Fast critical-path check (login → key action → logout) | Within 1 minute |
| **Error monitoring** | Watch error rate / log spikes | First 5–15 minutes |
| **Backup verify** | Confirm backup system is still healthy post-deploy | Within the verify window |

**If anything fails → decide: rollback or fix-forward?** The answer must be explicit. The deploy script should refuse to declare success if verification fails (or loudly flag that verification is pending and the deploy is unproven).

**Detect what exists:** health endpoint in routes, smoke test scripts in `./dev` or package.json, monitoring/alerting configs (Datadog, Sentry, Prometheus, Grafana, PagerDuty webhooks). Flag what's missing — at minimum, a health endpoint is table stakes.

---

## Migration Safety (the "don't nuke production" section)

- **Never auto-run migrations on prod inside the deploy** without a gate — make it an explicit, reviewable step.
- Every migration: **up + down**, tested against staging first.
- **Backup immediately before any migration** (see Part 2). Every time. No exceptions.
- Destructive operations (drops, truncates, deletes, batch updates) → require an explicit confirmation flag, never a default.
- **Dry-run mode**: show what WOULD change before changing anything. `deploy --dry-run` must work.
- Fresh DB and existing DB must both be handled (same rule as dev_environment migrations).
- Migrations are sequential and versioned — no "run all files in a random order" nonsense.

---

## Rollback

- **Documented**: revert = restore previous artifact + rollback migrations in order.
- **Target**: back to previous known-good version in < 5 minutes.
- **Tested**: rollback has been EXECUTED at least once — written rollback procedures that have never run are fiction.
- Rollback restores data from the backup taken at gate 4 if the schema or data is involved.

---

## Downtime Tolerance

Every project has a downtime tolerance — document it explicitly. Quiet assumptions cause loud outages.

| Tolerance Level | Signal | Example |
|-----------------|--------|---------|
| **Zero-downtime required** | Multiple instances, load balancer, graceful shutdown, blue-green or rolling deploys | SaaS with 24/7 paying users |
| **Acceptable window (< 5 min)** | Single instance but fast restart, scheduled maintenance window | Internal tool, low-traffic service |
| **Allowed when idle** | Deploy gated on "no active users" — check logs, active sessions, queue depth | Batch processing, cron-driven service |
| **Allowed anytime** | No SLA, dev/staging only, personal project | Side project, staging environment |

**How to determine the level (detect, don't guess):**
- Check for load balancer / multi-instance config (nginx upstream, k8s replicas, AWS ALB target groups)
- Check for graceful shutdown handling (SIGTERM handlers, `drain` configs, connection draining)
- Check for maintenance page conventions or scheduled-window documentation
- Check SLA / uptime commitments in docs

**Document the tolerance** wherever the deploy procedure lives. If it's undocumented, Bastet flags it — "downtime tolerance is unknown" — and recommends making it explicit. The deploy script should enforce it: zero-downtime projects must use rolling/canary/blue-green; idle-window projects must check the condition before proceeding.

---

## What Deploy Destroys & Protects

| PROTECT (never touch) | DESTROYS (safe to regenerate) |
|------------------------|-------------------------------|
| Database data | Stale builds, old artifacts |
| Uploads / user files | Cached assets |
| Secrets / configs | Deploy-time temp files |
| | Old versions beyond rollback window (once verified) |

---

## Build Reproducibility

Same commit + same build command → **same artifact**, every machine, every time. Without this, rollback is a gamble.

**Checklist:**
- Lockfiles pinned and committed (`package-lock.json`, `Cargo.lock`, `uv.lock`, `Gemfile.lock`, `poetry.lock`)
- Dependencies resolved from lockfile, not `latest`
- No network calls during build that could return different results
- Build artifacts are checksummed and verifiable
- Docker builds use pinned base images (`FROM node:20.11.1`, not `FROM node:latest`)

**Why it matters:** an unreproducible build means the "previous known-good version" can't be rebuilt identically. If the build isn't hermetic, the deploy contract must store actual artifacts (Docker images, tarballs, binaries) rather than relying on rebuild-from-source. Detect: check for lockfiles, pinned Docker tags, CI that builds vs deploys pre-built artifacts.

---

## Infrastructure as Code (IaC) Awareness

Deploying code is half the story — deploying infrastructure is the other half. Detect and account for IaC:

| IaC tool | Signal |
|----------|--------|
| Terraform / OpenTofu | `*.tf` files, `.terraform/` |
| Pulumi | `Pulumi.yaml`, `Pulumi.*.yaml` |
| AWS CDK | `cdk.json`, `*.cdk.ts` |
| Azure Bicep | `*.bicep` |
| CloudFormation | template YAML/JSON |
| Ansible | playbooks, `ansible.cfg` |

**If IaC exists:**
- Is infra deployed as part of the app deploy, or separately? Document the handoff ("deploy infra first, then app" or vice versa).
- The deploy gates must account for infra state: has the infra change been applied? Is it consistent with the app version?

**If IaC is absent** and the project has cloud resources → flag it. Hand-clicked, undocumented infrastructure is a disaster waiting to happen.

---

## Release Inventory (What's In This Deploy)

Before deploy, someone needs to answer: *what actually changed?* The changelog (or release notes) is that answer. Bastet should verify before deploy:

- **Changelog exists** for this version — gate 6 enforces this
- **Not vague** — "stuff" and "fixes" don't count. Breaking changes, new features, fixes, dependency bumps at minimum
- **Matches the diff** — compare against `git diff <last-tag>..HEAD`; flag unlisted changes
- **Right format for the scale:**
  - Single `CHANGELOG.md` — fine for most projects
  - Per-release docs (`docs/releases/v2.3.1.md`) — when a single file gets unwieldy
  - Auto-generated from conventional commits — detect `standard-version`, `release-please`, `changesets`

**Migration signal:** when `CHANGELOG.md` exceeds ~500 lines or the project has 20+ releases, consider migrating to per-release docs under `docs/releases/`. The changelog file becomes an index, not the full history.

---

## Environment Parity (Check, Don't Assume)

Local and remote environments may or may not match. Bastet must CHECK and DOCUMENT — never blindly assume local = remote, and never assume they differ.

**Known differences to look for:**
- **Environment variables** — local `.env` vs remote config; which vars exist only on one side?
- **Services** — local Docker DB vs remote managed DB (RDS, Cloud SQL): SQL dialects, extensions, and permissions may differ
- **Data** — local synthetic seed data vs real production volumes and edge cases
- **Network** — local has no firewalls/VPCs; remote likely does
- **Filesystem** — local might be case-insensitive (macOS/Windows), remote is case-sensitive (Linux) — this bites filenames and imports
- **Permissions** — local runs as you; remote runs as a restricted service account

**Document the answer:**
- If local and remote ARE the same (same Docker image, same env, same everything) → document that as a deliberate design choice
- If they differ → list every known difference in `dev_environment.md` under a "Local vs Remote Differences" section
- Before every deploy: confirm the documented differences are accounted for

A known difference is a checkpoint. An unknown difference is a deploy failure at 2 AM.

---

# Part 2: Backup

## The Philosophy

**Bastet gets ANGRY when production exists without a backup strategy.** A home with no fire escape is not a home.

- **No backup strategy = 🔴 red flag** in every report, every audit, no exceptions
- **Backups you've never restored don't count.** A backup that cannot restore is a fantasy
- Backup is the **second major part of deployment**: you cannot deploy safely without it, and it is checked as a deploy gate

---

## The Backup Contract

Whatever the mechanism (adapt to ecosystem like deploy — `./dev backup`, `npm run backup`, Makefile target, cron + script):

| Command | Purpose |
|---------|---------|
| `backup` | Full backup to a durable location (NOT the same machine as prod) |
| `backup:db` / `backup:files` / `backup:config` | Scoped backups |
| `restore` | Restore from a backup (this command gets exercised!) |
| `verify` | Prove a backup can actually be restored. At minimum: checksum the backup file, run sample queries against restored data (row counts on key tables), and confirm the restore completes without errors. The full restore-into-scratch-environment drill is the gold standard (see Rules). This `verify` step should also run as part of post-deploy verification — "we just deployed, is the backup system still healthy?" |
| `status` | When was the last backup, is it valid, where does it live |

---

## What To Back Up

| Data | How |
|------|-----|
| **Database** | `pg_dump` / `mysqldump` / snapshot — tagged with migration version. For Postgres, prefer WAL archiving for point-in-time recovery (PITR). For MySQL/MariaDB, consider binlog-based PITR. Full dumps are the baseline; PITR is the upgrade path. Detect which the database supports and reflect it in the backup scripts — a simple dump is fine for small projects, but PITR is the goal when data volume or RPO demands it. |
| **Uploads / user files** | `rsync` / `rclone` to S3-compatible storage |
| **Config / secrets** | Encrypted, versioned — or documented as re-creatable (env.example + CI secret store) |
| **Infra state** | Terraform state, k8s manifests, compose files — in git or a state backend |

---

## The Rules

1. **Before every deploy: backup. Before every migration: backup.** No exceptions. The gate enforces it.
2. **Off-box**: the backup lives elsewhere — the same disk as production is NOT a backup.
3. **Rotation**: keep N daily, M weekly, K monthly — sized to the data; a retention policy that fills the disk and silently fails is worse than none (it fakes safety).
4. **Verify**: scheduled restore drill — restore into a scratch environment and check the data actually comes back. This is how backups earn their keep.
5. **Survive the apocalypse**: at least one backup copy survives the loss of the primary host (different host / region / object store).
6. **Visibility**: backup status appears in health checks (`./dev doctor` / `status`) — a silent backup is a dead backup.
7. **Encryption**: backups in transit are typically over SSH or TLS — confirm this is the case rather than assuming. At-rest encryption (AES-256, S3 server-side encryption, etc.) is required when the data contains PII, credentials, or compliance-sensitive information. Flag whether encryption is configured and whether the project needs it — "probably fine" is a risk posture, not a security posture. This check should be adapted to the database type: Postgres `pg_dump` can pipe through `gpg`; cloud object stores offer server-side encryption; `rclone` supports `crypt` remotes.

---

## Backup Red Flags (Bastet hisses at these)

| Red Flag | Why It's Dangerous |
|----------|--------------------|
| No backup command/scripts at all | Production data is a single hardware failure from oblivion |
| Backups on the same machine as production | Fire, disk death, ransomware takes both |
| Backups never restored/tested | Restore is the only moment the backup matters — and it's never happened |
| No retention policy | Disk fills, backup silently fails, yesterday's "safety" was a lie |
| Backup only in someone's head ("we have a cron somewhere") | Session-to-session knowledge loss — exactly what this repo's rules exist to prevent |
| Production exists, backup strategy absent | Bastet's fury. Flag first, in red, before anything else |

---

## Environment Adapters

| Stack | Backup tools |
|-------|--------------|
| Postgres | `pg_dump` + object storage upload + retention |
| MySQL / MariaDB | `mysqldump` + retention |
| Docker services | Volume snapshots + DB dump (dump is the real backup, volumes are bonus) |
| Serverless / edge | Remote DB dumps + exported state + function source in git |
| Files / uploads | `rclone` / `rsync` to S3-compatible storage |
| Mobile | Build artifacts + signing secrets (encrypted, off-box) |
| WordPress | WP-CLI export + uploads sync |

---

## The Report

When deploy/backup are part of an audit, report:

- **Per gate**: passed / failed / missing (test, lint, build, backup, migration review, version, secrets, approval)
- **What's scripted vs manual** — every manual step is a future fuck-up
- **Backup freshness**: last backup time, last restore drill date
- **Red flags first** — no backup strategy is the loudest alarm; production without a fire escape gets flagged before the pretty badges
- Purr only when it's actually safe, and not a moment sooner

---

*Meow — deploy like a cat: sure-footed, never rushed, always ready to land on her feet.*
