# Testing: Core

> Load for every repo. No exceptions.
>
> These are the baseline expectations for behavior, confidence, and discipline.

---

## Unit Behavior

- [ ] CRITICAL IF code contains logic, parsing, validation, transforms, or state transitions -> THEN write behavior-focused unit tests for happy paths and failure paths
- [ ] CRITICAL IF a function has boundary conditions -> THEN test zero, one, empty, null-like, max/min, malformed, and overflow-style values where relevant
- [ ] CRITICAL IF the code depends on time, randomness, env, filesystem, or process state -> THEN isolate those dependencies rather than letting unit tests rely on ambient state
- [ ] HIGH IF several cases differ only by input/output pairs -> THEN parameterize them instead of cloning near-identical tests
- [ ] HIGH IF tests contain loops, branching, retries, or hidden logic -> THEN simplify them until each test proves one behavior clearly

---

## Test Design Techniques

Derive cases — don't just flood values. Pick the technique that fits the shape of the code:

| Technique | Derive cases from | Use when |
|---|---|---|
| Equivalence partitioning | valid / invalid input classes; one member per class | any typed input — class count is interface-design feedback, shrink interfaces to shrink verification cost |
| Boundary value analysis | min−1, min, max, max+1, 0, 1, empty | ranges, lengths, pagination |
| Decision table | every condition combination | multi-condition branching |
| State transition | states × events × guards | workflows, status machines |
| Pairwise / combinatorial | 2-way parameter combinations | config matrices, option flags |
| Cause–effect | input causes → expected effects | validation rules, permissions |
| Property-based | invariants over generated inputs | parsers, math, serialization |

## Choosing the Oracle

Every test names where its expected value comes from. No oracle, no test — record it as a blocker instead:

| Oracle | Expected value comes from | Fails when |
|---|---|---|
| Spec-derived | documented requirement | spec silent or ambiguous |
| Invariant | property that must always hold (balance ≥ 0) | invariant unstated |
| Metamorphic | relation between runs (encode→decode round-trip; sort twice = sort once) | relation not identified |
| Differential | old vs new, or two implementations on one corpus | no second implementation |
| Golden / approval | reviewed stable artifact | output churns |
| Human judgment | explicit reviewer decision | must be escalated, never guessed |

---

## Smoke and Regression

- [ ] CRITICAL IF the code is runnable or deployable -> THEN keep a smoke suite that proves startup, essential config, and primary health checks
- [ ] CRITICAL IF a bug was fixed or is being discussed -> THEN add a regression test that fails on the broken behavior and passes only when the bug is truly blocked
- [ ] HIGH IF the code has public exports, commands, or endpoints -> THEN test the most important contract boundaries before testing internal details
- [ ] HIGH IF outputs are complex but stable -> THEN prefer golden or approval-style regression checks over vague assertions

### Failing-First Proof

A regression test that never failed proves nothing. For every bug-driven test:

1. Run the new test against current code; capture the failure output.
2. Verify the failure is the **intended assertion** — not import, fixture, collection, or environment failure.
3. Apply the fix; the test passes.
4. Revert the fix (or mutate the guarded line); the test fails again.
5. Record the red-phase evidence in the report.

A test that passes before the change is not a regression test. A test that fails for the wrong reason is not evidence.

---

## Mutation and Deletion Pressure

- [ ] CRITICAL IF tests pass but meaningful behavior is still doubtful -> THEN mutate conditions, return values, constants, and null handling to prove the tests can detect real damage
- [ ] HIGH IF removing a function, branch, or dependency causes no test to fail -> THEN the behavior is undefended and needs a real test
- [ ] HIGH IF line or branch coverage is used as a success claim -> THEN challenge it with deletion or mutation before trusting it

## Generative Tests

Optional and scoped — reach for these when example-based cases can't cover the input space:

- [ ] HIGH IF the code parses, serializes, encodes, or computes over wide inputs -> THEN add property-based tests: state the invariant (round-trip, idempotence, commutativity, conservation), generate inputs, shrink on failure
- [ ] HIGH IF parsers, auth, uploads, or network boundaries face hostile input -> THEN fuzz them with a seed corpus; minimize crashing inputs and keep them as regression tests
- [ ] MEDIUM IF generative tests exist -> THEN bound them: fixed seed for repro, time/iteration budget so CI stays green, shrinking enabled
- [ ] MEDIUM IF state machines or protocols are complex -> THEN consider model-based tests: model states/transitions, generate walks, assert the implementation never leaves the model

---

## Test Hygiene

- [ ] CRITICAL IF tests share mutable state, persistent fixtures, or order dependencies -> THEN isolate them until they pass in any order
- [ ] CRITICAL IF tests hit network, real databases, or real third-party systems unintentionally -> THEN move those concerns out of unit scope and into the right higher-level suite
- [ ] HIGH IF factories or fixtures hide critical assumptions -> THEN make the tested scenario explicit in the test body
- [ ] HIGH IF a flaky test exists -> THEN treat it as broken, not as an acceptable warning

### Flake Forensics

Reproduce → classify → isolate → fix cause → quarantine only with owner, expiry, and issue:
1. Reproduce: repeat N times; alone vs full suite; vary seed and order.
2. Classify: clock, order dependence, shared state, network, resource contention, async race, external service.
3. Isolate: run alone; bisect suite and fixtures to find the polluter.
4. Fix the cause: inject the clock, use unique data, poll a condition, explicit teardown.
5. Quarantine only with owner, expiry, and tracking issue. Never silent retry.

### Test Data

- [ ] HIGH IF tests need domain objects -> THEN use builders or factories with sensible defaults; each test states only fields relevant to its behavior
- [ ] HIGH IF fixtures exist -> THEN use representative data, not only happy fixtures; include malformed and extreme records
- [ ] CRITICAL IF data resembles production users -> THEN never use prod PII; anonymize or synthesize
- [ ] HIGH IF tests share a database -> THEN seed deterministically and clean up; no test depends on another test's data
- [ ] HIGH IF parallel workers share a database -> THEN isolate by transaction rollback, truncate, or schema-per-worker; document the parallel-safety choice
- [ ] MEDIUM IF golden or snapshot files exist -> THEN assign ownership, review policy, and a refresh command

## The Anatomy of a Killing Test

Every test Osiris writes passes these 8 checks:

1. One behavior, one reason to fail.
2. Name states behavior + condition (`rejects duplicate email with 409`, not `works`).
3. Arrange / Act / Assert visually separated.
4. Assert observable outcome, not private internals.
5. Exact expected value over truthiness.
6. Failure message distinguishes actual vs expected.
7. Deterministic: clock, randomness, network, filesystem injected.
8. Fast enough to run on every save.

## Test Doubles

| Double | Use for | Rule |
|---|---|---|
| Stub | canned responses | at owned boundaries |
| Spy | verify interaction | only when the interaction IS the contract |
| Fake | working in-memory implementation | external services, DB |
| Mock | expectation verification | never the unit under test |
| Real | domain logic, pure functions | default — prefer real |

Mock at owned seams. Fake external systems. Never mock the thing you are testing. Never mock what you don't own.

### Bad → Good

| 💀 Decorative | ✅ Killing |
|---|---|
| `expect(result).toBeTruthy()` | `expect(result).toEqual({id: 7, status: "active"})` |
| mock every collaborator | real domain logic + fake at the boundary |
| `it("works")` | `it("rejects duplicate email with 409")` |

---

## Quality Gates

- [ ] CRITICAL IF the repo has a typechecker, linter, or build validation -> THEN run it in CI and fail on violation
- [ ] CRITICAL IF secrets can enter the repo or build logs -> THEN run secrets scanning in CI and block merges on hits
- [ ] HIGH IF static analysis is available for the stack -> THEN use it to catch classes of failures that tests miss
- [ ] HIGH IF the suite is too slow to run locally -> THEN keep a fast core path so developers can verify behavior before commit
- [ ] HIGH IF PRs change behavior -> THEN gate on changed-line coverage and mutation on changed files, not whole-repo thresholds
- [ ] MEDIUM IF the suite is sharded or parallel -> THEN pin the shard policy and require failure artifacts (traces, videos, logs) on every red run
- [ ] MEDIUM IF branch protection exists -> THEN make the gates required checks, not advisory

---

## Bootstrap, Docs, and Suite Health

- [ ] CRITICAL IF the product has setup docs, bootstrap scripts, or sample config -> THEN prove a fresh install works from documented steps only on a clean machine or container
- [ ] CRITICAL IF examples such as `README` snippets, sample commands, or `.env.example` files exist -> THEN execute or validate them so documentation drift fails fast
- [ ] CRITICAL IF CI runs the suite -> THEN fail on focused tests such as `.only`, and require skipped or quarantined tests to have an explicit owner and expiry
- [ ] HIGH IF the suite is mature or slow -> THEN track runtime regression, flake rate, and orphaned fixtures, snapshots, or golden files as health signals

## Runner Capabilities

Framework-agnostic checklist — verify the runner can do these before promising the suite can:

- Parameterized cases, fake timers / injected clock, network interception, snapshots or approvals, coverage merge across shards, a mutation tool that runs on diffs.
