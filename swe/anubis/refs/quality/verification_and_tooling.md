# Quality: Verification And Tooling

> Tests, refactor safety, docs drift, tooling contracts, and the mechanisms that keep quality from silently regressing.
>
> Load this for wrappers, scanners, CI-integrated tools, examples, and any risky change that needs proof.

---

## 🧪 Testing

- [ ] 🟢 Test names describe the scenario — `returnsEmptyWhenNoOrders` not `testOrders`
- [ ] 🟡 One assertion concept per test — testing 5 things = 5 tests
- [ ] 🔴 Test edge cases explicitly — null, empty, max, negative, unicode, timezone
- [ ] 🔴 Mock external dependencies — tests shouldn't hit real APIs/databases
- [ ] 🟡 Dependency injection — pass collaborators, don't hardcode singletons
- [ ] 🟡 Fast test suite — slow tests don't run; aim for sub-second units
- [ ] 🟡 Test behavior, not implementation — users don't care about internal methods
- [ ] 🔴 No logic in tests — no `if/for` in tests. If the test has bugs, who tests the test?
- [ ] 🔴 No flaky tests tolerated — if it flakes once, fix/skip with a ticket (don't normalize it)
- [ ] 🔴 Avoid sleeps/timeouts in tests — use fakes, clocks, signals; sleeps create slow + flaky suites
- [ ] 🔴 Each test owns its data — no shared mutable fixtures that leak state across tests

### ML / Agentic Verification Limits

- [ ] 🔴 IF behavior depends on prompts, retrieval, tools, or model policies → THEN have deterministic tests around prompt builders, policy gates, sanitizers, allowlists, redaction, and fallback logic — don't leave safety in untested glue code
- [ ] 🟡 IF the repo is ML-heavy → THEN state testability limits clearly: existing tests can verify guardrail code and contracts, but they do not prove live model behavior across all prompts or sessions
- [ ] 🟡 IF the team relies on manual prompting or ad hoc notebook checks for safety claims → THEN treat that as weak evidence unless key protections are covered by repeatable automated tests
- [ ] 🟡 IF prompt-injection, RAG leakage, or tool-misuse defenses exist → THEN verify regression tests cover known bad inputs and expected blocked/redacted outcomes

---

## 📜 Comment & Documentation Smells

- [ ] 🟢 Comments that restate the code — `i++ // increment i` wastes everyone's time
- [ ] 🔴 Outdated comments that contradict the code — worse than no comment; they actively mislead
- [ ] 🟢 Commented-out alternate implementations — "we might need this" — no you won't; delete it
- [ ] 🟢 Journal comments at top of file — changelogs belong in git, not in source files
- [ ] 🟢 Javadoc / docstrings on every trivial method — `/** Gets the name. */ getName()` is noise; document WHY, not WHAT

---

## 🔧 Build & Environment Hygiene

- [ ] 🔴 No `.editorconfig` or formatter config committed — tabs vs spaces wars solved by automation, not arguments
- [ ] 🔴 Linter warnings ignored or disabled project-wide — `// eslint-disable` at the top of every file is a surrender flag
- [ ] 🟡 No pre-commit hooks for formatting/linting — reviews shouldn't waste time on style
- [ ] 🟡 Build artifacts committed to repo — `node_modules/`, `__pycache__/`, `.class` files don't belong in git

---

## 🧪 Additional Test Smells

- [ ] 🟡 Hardcoded test fixtures — `const user = { id: 1, name: "Test" }` in 50 tests. Use a factory function
- [ ] 🟢 Assertions without messages — `assert(a === b)` fails. *Why*? `assert(a === b, "User age should match DB")`
- [ ] 🔴 Testing private methods — if it's private, it's an implementation detail. Test via public method
- [ ] 🟡 Over-mocking — mocking 5 layers deep means your code is too coupled. Refactor to test the integration

---

## 🔧 Refactoring & Simplification Safety

*Focus: How to safely simplify without breaking behavior.*

- [ ] 🔴 **Separate refactor commits from behavior changes** — If a PR both "cleans up" AND "changes logic", reviewing is guesswork. One or the other.
- [ ] 🔴 **Characterization tests before refactor** — Lock current behavior (especially legacy/buggy behavior) before cleanup. No tests = no refactor safety net. If you don't have a test, you aren't refactoring; you're just changing code and hoping.
- [ ] 🟡 **Refactor in reversible steps** — Small mechanical transformations. Keep diffs reviewable. Big-bang rewrites are risky.
- [ ] 🟡 **Don't refactor without observability** — If it runs in prod, ensure logs/metrics/traces exist to validate no regressions.
- [ ] 🔪 **Delete code aggressively (with proof)** — Prefer removing unused paths over "simplifying" them. "If I delete this, will anything break?" No = DELETE. Yes = keep but simplify.
- [ ] 🟢 **Inline needless indirection** — If a function is a 1-line pass-through with no semantic value, remove it. Call the target directly.
- [ ] 🟡 **Reduce public API surface** — Make modules/classes expose the minimum. Fewer exports/public methods = easier refactors later.
- [ ] 🟡 **One obvious way** — Within a codebase, pick ONE pattern for the same thing (errors, results, async style, DI). Consistency simplifies more than cleverness.
- [ ] 🟢 **Normalize data to kill branching** — Convert inputs to canonical shape early so downstream code is simpler. Shape divergence = branching explosion.
- [ ] 🟡 **Keep refactors tool-friendly** — Use formatter + linter + "rename symbol" refactors; avoid manual risky edits that tools can't verify.

---

## 🧪 Tooling, Contracts & Verification

*Focus: Prevent wrapper drift, false confidence, and product-surface rot.*

- [ ] 🔴 **Wrapper-to-core contract drift** — If one layer wraps another CLI/API/tool, contract-test flags, arguments, outputs, and exit codes against the source. Unsupported wrapper flags are silent breakage.
- [ ] 🔴 **Weak baseline/fingerprint deduplication** — Suppressing findings via short text prefixes or unstable fingerprints creates false negatives. Use stable hashes plus enough code context to survive line shifts without merging distinct findings.
- [ ] 🟡 **Incremental scan correctness must be proven** — Cached/incremental runs must match full scans. If an analyzer cannot do partial evaluation safely, force full-scan mode and test that behavior explicitly.
- [ ] 🔴 **Docs and examples must execute** — README, checklist, action, and plugin commands are part of the product surface. Validate them in CI or they will rot.
- [ ] 🔴 **Single source of truth for version/build metadata** — Reports, banners, plugin manifests, and package metadata must derive from one canonical source, not copied strings.
- [ ] 🟡 **High-risk glue layers need integration tests** — Webhooks, actions, extensions, report renderers, wrappers, and auth adapters are where drift and security regressions hide. Unit tests alone are not enough.

---
