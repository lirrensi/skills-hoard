# Verification Strategy Standard

This reference defines how to document the project's proof strategy. Load it whenever a project verification strategy is created, updated, audited, or reconciled with code.

## Terms

- **Check:** A repeatable activity that produces a result, such as a test, lint command, browser journey, protocol probe, manual checklist, or deployment smoke check.
- **Test:** A check that executes a controlled assertion against a unit, component, integration, contract, or system.
- **Verification:** Evidence that an implementation satisfies a defined requirement, invariant, protocol, or operational expectation.
- **Validation:** Evidence that the verified behavior solves the intended user or product problem. Validation may require human judgment, realistic data, exploratory use, or stakeholder acceptance.
- **Evidence:** An inspectable result of a check: exit status, assertion report, coverage report, screenshot, trace, log, metric, protocol capture, approval, or linked artifact.

Do not use “tested” and “verified” as synonyms. A test can pass while exercising the wrong behavior, an obsolete fixture, or an overly narrow path.

## Canonical Document

Every maintained project has one discoverable entry point:

```text
docs/verification/strategy.md
```

The document MUST have `node_type: verification` and MUST link to the product overview, relevant specs, architecture, CI configuration, and test/tooling locations when those assets exist. If a project uses another path, the root documentation index MUST link to it and explain the deviation.

## Required Strategy Content

The strategy MUST make these facts obvious to a new contributor:

1. **Scope and intent** — what correctness means for this project, including the difference between automated verification and product validation.
2. **System surfaces** — backend/API, data, workers/CLI, UI, integrations, infrastructure, and other applicable surfaces.
3. **Toolchain** — exact tools and versions where relevant: test runners, browser automation, linters, formatters, type checkers, static analyzers, contract tools, fakes/mocks, and reporting tools.
4. **Verification taxonomy** — which layers exist and what each layer proves.
5. **Suite tiers** — commands, runtime expectations, prerequisites, and cadence for fast, standard, long, and release checks.
6. **Traceability matrix** — important product goals/spec requirements mapped to checks, commands, and evidence.
7. **Environments and data** — local/CI/staging/production-like conditions, fixtures, service dependencies, secrets policy, and reset/isolation rules.
8. **Failure interpretation** — how to triage failures and decide whether the problem is implementation, documentation, test infrastructure, or an invalid expectation.
9. **Coverage gaps and risks** — missing layers, manual-only areas, flaky checks, known blind spots, and compensating controls.
10. **Maintenance trigger** — when behavior, tools, commands, CI, environments, or architecture changes, this document MUST be reviewed.

If a category does not apply, state that explicitly with the reason. Never leave readers guessing whether a layer was forgotten.

## Verification Taxonomy

Use the smallest set of layers that gives credible evidence. Name the project's actual tools in the strategy; the examples below are categories, not assumptions about the toolchain.

| Layer | What it can prove | Typical evidence |
|---|---|---|
| Static / quality | Syntax, formatting, types, lint rules, dependency or security policies | Tool report and exit status |
| Unit | Isolated decision logic and invariants | Assertions, mutation/coverage signal where useful |
| Component / service | One component with its real boundary behavior | Component test report, serialized output, logs |
| Integration | Collaboration with databases, queues, files, services, or adapters | Integration report, seeded data, protocol/log evidence |
| Contract / API | Request/response schemas, headers, errors, compatibility, and message protocols | Contract report, schema validation, captured exchange |
| UI / end-to-end | User-perceivable journeys across the running system | Browser assertions, screenshots, traces, video, console/network logs |
| Manual / exploratory | Ambiguous, novel, visual, accessibility, or product-quality behavior not safely automated | Checklist, notes, screenshots, approval, linked issue |
| Operational / release | Startup, migrations, health, deployment, rollback, performance, resilience, and observability expectations | Command output, metrics, logs, alerts, rollback evidence |

Do not claim that unit coverage verifies an end-to-end journey, or that a UI smoke check proves backend edge-case coverage. State the boundary of each layer.

## Suite Tiers

Every documented command belongs to an execution tier:

| Tier | Purpose | Expectations |
|---|---|---|
| Fast / smoke | Immediate local feedback and pre-commit/PR gate | Minimal prerequisites; short and deterministic |
| Standard | Normal PR or merge confidence | Covers changed behavior and key integrations |
| Long / exhaustive | Broader integration, UI, performance, resilience, or compatibility evidence | May require services, seeded data, browsers, or more time |
| Release / production-like | Final acceptance and operational confidence | Runs in a representative environment with explicit approval/gates |

Record approximate runtime only when it is known; otherwise mark it `[UNDECIDED]` rather than inventing a number.

## Traceability Rules

Each important product goal, requirement, protocol contract, and user journey MUST have at least one named verification check or an explicit documented gap. Use stable IDs such as `V-AUTH-001` and link from specs to the strategy with `verified_by` when the ontology supports it.

A traceability row should answer:

| Claim | Check ID | Layer | Tool / command | Environment | Evidence | Status |
|---|---|---|---|---|---|---|
| What behavior is claimed? | Stable identifier | What boundary is checked? | Exact executable command | Where it runs | What proves the result? | verified / partial / missing / blocked |

When a check passes but the behavior still does not match intent, record the discrepancy. The green result is not permission to rewrite the requirement silently.

## UI and Backend Guidance

- For backend-only projects, document endpoint/message coverage, schema and error cases, persistence/queue boundaries, integration prerequisites, and whether contract or protocol checks exist.
- For UI projects, document the user journeys covered by browser automation, the browser/device/environment matrix, accessibility and visual checks, network mocking policy, and what remains manual.
- For mixed systems, map UI journeys to the backend contracts they exercise; do not treat a single browser happy path as coverage of every API failure mode.
- Name tools only when they are actually used. “Playwright” is an example, not a default requirement.

## Verification Status

Use these status labels in matrices and reports:

- `verified` — the documented check currently passes and its evidence supports the claim.
- `partial` — only part of the claim or one environment/path is covered.
- `missing` — no credible check is documented.
- `blocked` — a check exists but cannot currently produce evidence.
- `drifted` — the command, tool, behavior, or expected result no longer matches reality.
