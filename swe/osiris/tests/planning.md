# Testing: Planning

> Load when the request is to plan, assess, or prioritize tests — not when writing a narrow test.

---

## Test Plan Contract

A plan without scope, risk, and exit criteria is a wish list. Every plan states:

- **Scope / out of scope** — surfaces, modules, environments covered and explicitly excluded.
- **Repo profile + evidence** — flags from SKILL.md with `path:line` proof for each claim.
- **Risk register** — impact × likelihood × detectability, owner, blast radius per risk.
- **Test levels** — unit / integration / contract / e2e / perf / security / exploratory, with one-line rationale each.
- **Traceability** — Downstream: every requirement → test(s); untested requirement = GAP. Upstream: every code element → requirement; unasked code = GAP or delete. One tag in spec clause, code, test; two greps.
- **Environments & data** — what is real, faked, seeded, or unavailable.
- **Entry criteria** — build green, deps available, baseline recorded, baseline frozen (informal → baseline transition before build).
- **Exit criteria** — all Critical gaps closed; no new High unowned; mutation threshold met; flake rate bounded; changed-line coverage; perf/security thresholds; no quarantined test without owner + expiry; every requirement has normal + robustness evidence.
- **Deliverables** — plan, test files, judgment report, unverified list.

---

## N/A Discipline

Every unchecked checklist item is either a **GAP** (with a test to write) or **N/A** (with a one-line reason). No silent skips. "Not applicable" is a verdict with evidence, not an excuse.
Untestable code gets a WRITTEN per-line justification (default cases, defensive code, init/shutdown, language artifacts, unused lib code). Justifications migrate when code moves; stale ones are discarded. Silence about an uncovered line is a process bug.

---

## Two Passes Per Requirement

Normal range (intended function, complies) and robustness (full equivalence-class range, abnormal conditions, faults) are SEPARATE mandatory proofs. Works-when-used-right never covers doesn't-misbehave-when-abused.

---

## Verification Method Check

Pre-work desk review, before building: every spec clause gets a named method — Test, Review, or Analysis (mutation, coverage, deletion). A clause with no method is a plan gap; work doesn't start.

---

## Depth Modes

| Mode | Scope | When |
|---|---|---|
| Quick | smoke + top 3 risks, ~30 min | triage, small change |
| Standard | core + relevant leaves, full lenses | default |
| Rigorous | all applicable leaves + mutation + perf + chaos | release-critical |

Better to judge few areas thoroughly than all areas superficially.
