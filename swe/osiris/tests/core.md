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

## Smoke and Regression

- [ ] CRITICAL IF the code is runnable or deployable -> THEN keep a smoke suite that proves startup, essential config, and primary health checks
- [ ] CRITICAL IF a bug was fixed or is being discussed -> THEN add a regression test that fails on the broken behavior and passes only when the bug is truly blocked
- [ ] HIGH IF the code has public exports, commands, or endpoints -> THEN test the most important contract boundaries before testing internal details
- [ ] HIGH IF outputs are complex but stable -> THEN prefer golden or approval-style regression checks over vague assertions

---

## Mutation and Deletion Pressure

- [ ] CRITICAL IF tests pass but meaningful behavior is still doubtful -> THEN mutate conditions, return values, constants, and null handling to prove the tests can detect real damage
- [ ] HIGH IF removing a function, branch, or dependency causes no test to fail -> THEN the behavior is undefended and needs a real test
- [ ] HIGH IF line or branch coverage is used as a success claim -> THEN challenge it with deletion or mutation before trusting it

---

## Test Hygiene

- [ ] CRITICAL IF tests share mutable state, persistent fixtures, or order dependencies -> THEN isolate them until they pass in any order
- [ ] CRITICAL IF tests hit network, real databases, or real third-party systems unintentionally -> THEN move those concerns out of unit scope and into the right higher-level suite
- [ ] HIGH IF factories or fixtures hide critical assumptions -> THEN make the tested scenario explicit in the test body
- [ ] HIGH IF a flaky test exists -> THEN treat it as broken, not as an acceptable warning

---

## Quality Gates

- [ ] CRITICAL IF the repo has a typechecker, linter, or build validation -> THEN run it in CI and fail on violation
- [ ] CRITICAL IF secrets can enter the repo or build logs -> THEN run secrets scanning in CI and block merges on hits
- [ ] HIGH IF static analysis is available for the stack -> THEN use it to catch classes of failures that tests miss
- [ ] HIGH IF the suite is too slow to run locally -> THEN keep a fast core path so developers can verify behavior before commit

---

## Bootstrap, Docs, and Suite Health

- [ ] CRITICAL IF the product has setup docs, bootstrap scripts, or sample config -> THEN prove a fresh install works from documented steps only on a clean machine or container
- [ ] CRITICAL IF examples such as `README` snippets, sample commands, or `.env.example` files exist -> THEN execute or validate them so documentation drift fails fast
- [ ] CRITICAL IF CI runs the suite -> THEN fail on focused tests such as `.only`, and require skipped or quarantined tests to have an explicit owner and expiry
- [ ] HIGH IF the suite is mature or slow -> THEN track runtime regression, flake rate, and orphaned fixtures, snapshots, or golden files as health signals
