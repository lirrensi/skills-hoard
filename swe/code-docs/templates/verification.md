---
node_type: verification
title: Project Verification Strategy
status: active
updated: YYYY-MM-DD
tags: [verification, testing]
links:
  depends_on: [/overview/product.md, /spec/INDEX.md, /architecture/INDEX.md]
  verifies: [/spec/INDEX.md]
  documents: []
---

# Project Verification Strategy

## Purpose and Scope

{Explain what “works” means for this project and how verification differs from a test result or product validation.}

## System Surfaces

| Surface | What must be verified | Primary evidence |
|---|---|---|
| Backend / API | {endpoints, messages, errors, state, persistence} | {reports, protocol captures, logs} |
| UI / user journeys | {user-perceivable outcomes} | {browser assertions, traces, manual checks} |
| Workers / CLI / integrations | {jobs, commands, external boundaries} | {output, fixtures, integration evidence} |
| Operations / release | {startup, deploy, migration, rollback, health} | {logs, metrics, command output} |

{Remove surfaces that do not apply, but say why they are absent.}

## Toolchain

| Tool | Version / source | Purpose | Evidence produced |
|---|---|---|---|
| {test runner} | {version or package manifest} | {what it checks} | {report / exit status} |
| {browser / static / contract tool} | {version or package manifest} | {what it checks} | {artifact} |

## Verification Taxonomy

| Layer | What it proves here | What it does not prove | Tool / entry point |
|---|---|---|---|
| Static / quality | {claim} | {boundary} | `{command}` |
| Unit / component | {claim} | {boundary} | `{command}` |
| Integration / contract | {claim} | {boundary} | `{command}` |
| UI / end-to-end | {claim} | {boundary} | `{command}` |
| Manual / exploratory | {claim} | {boundary} | {checklist or process} |
| Operational / release | {claim} | {boundary} | `{command}` |

## Suite Tiers

| Tier | Command | Prerequisites | Approx. runtime | Cadence / gate | Evidence |
|---|---|---|---|---|---|
| Fast / smoke | `{exact command}` | {none / setup} | {time or [UNDECIDED]} | {local / pre-commit / PR} | {report} |
| Standard | `{exact command}` | {services / fixtures} | {time or [UNDECIDED]} | {PR / merge} | {report} |
| Long / exhaustive | `{exact command}` | {services / browser / data} | {time or [UNDECIDED]} | {scheduled / release} | {artifact} |
| Release | `{exact command}` | {production-like environment} | {time or [UNDECIDED]} | {release gate} | {approval / report} |

## Traceability Matrix

| Claim / requirement | Check ID | Layer | Tool / command | Environment | Evidence | Status |
|---|---|---|---|---|---|---|
| {goal or `/spec/...#anchor`} | `V-{DOMAIN}-001` | {layer} | `{exact command}` | {local / CI / staging} | {artifact or assertion} | verified / partial / missing / blocked |

## Environments and Test Data

- **Local:** {setup, dependencies, reset/isolation}
- **CI:** {workflow, services, secrets policy, artifact retention}
- **Staging / production-like:** {representativeness and restrictions}
- **Fixtures and data:** {creation, cleanup, privacy, determinism}

## Failure Interpretation

1. {How to reproduce and locate the failing check.}
2. {How to distinguish product/spec mismatch from implementation failure.}
3. {How to handle flaky infrastructure or stale fixtures.}
4. {Where evidence and follow-up are recorded.}

## Coverage Gaps and Risks

| Gap / risk | Affected claim | Consequence | Compensating check or next action | Owner / status |
|---|---|---|---|---|
| {untested layer or known blind spot} | {claim} | {risk} | {manual check / planned work} | {status} |

## Maintenance Triggers

Review this strategy when behavior, requirements, architecture, dependencies, test tools, commands, CI workflows, environments, fixtures, or release gates change. Update the traceability matrix and evidence expectations in the same change.
