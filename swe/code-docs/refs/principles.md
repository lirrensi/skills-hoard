# Documentation Principles

## The Core Philosophy

**Documentation is the semantic digital twin of the codebase.** Docs define what the system is, why it exists, how it behaves, and how it's structured. Code is one rendering of that truth.

**If code and docs disagree, docs win** — or docs are updated intentionally, never silently. If you had to choose between keeping the code or the docs, keep the docs. You can rebuild code from docs. You cannot rebuild docs from code.

## The Documentation Stack

The stack refines downward — each layer adds precision while preserving the truth of the layer above:

```
overview/  →  spec/  →  architecture/  →  code
(why)        (what)     (how)             (rendering)
    ╲          ↓           ↓              ↑
             verification/ — evidence that intent and implementation agree
   ↑_______________________________________________________________↑
                  stories/ — memory of how we learned
```

- `overview/` is written first. It defines product identity, purpose, value, users, and non-goals.
- `spec/` is derived from `overview/`. It defines exact, testable behavior in BDD+RFC format.
- `architecture/` is derived from `spec/`. It defines how the current implementation realizes the behavior.
- `verification/` is a cross-cutting evidence layer. It is derived from product intent, behavioral requirements, and the current implementation. It defines how the project checks that the implementation actually matches the intended behavior.
- `stories/` is the project's empirical memory. It records how we figured things out: debug sessions, migrations, incidents, and surprises. It does not override the layers above; it explains where they came from.
- Code may be discarded and regenerated from the docs. The docs are the valuable artifact.

## Layer Ownership

| Layer | Owns | Does NOT own |
|-------|------|-------------|
| **overview/** | Product identity, purpose, user value, major flows, non-goals | Exact behavior, implementation detail |
| **spec/** | Exact behavior, contracts, edge cases, state rules, data schemas, conformance | Implementation structure, framework choices |
| **architecture/** | Implementation structure, components, dependencies, boundaries, runtime shape | Product positioning, behavioral requirements |
| **verification/** | Verification strategy, test taxonomy, toolchain, commands, environments, evidence, traceability, coverage gaps | Product requirements, implementation design, unsupported claims of coverage |

## Conflict Resolution

- If `architecture/` and `spec/` disagree on behavior → **spec/ wins**.
- If `spec/` and `overview/` disagree on identity, purpose, or non-goals → **overview/ wins**.
- If code and docs disagree → **docs win**, or docs are updated intentionally.
- Lower layers MUST preserve the truth of the layer above while adding precision.
- Verification does not override the product, spec, or architecture. A failed check is evidence of a discrepancy; resolve it by intentionally updating the correct canonical layer or the implementation, never by weakening the check silently.

## Behavior-First, Goal-Driven

Every spec must answer three questions in order:

1. **WHY** — What is the goal? What problem does this behavior solve? (Purpose, Goals)
2. **WHAT** — What must the system do? What are the requirements? (Requirements, MUST/SHOULD/MAY)
3. **HOW** — How does the behavior manifest? What are concrete scenarios? (Given/When/Then)

This ensures docs are strong enough to:
- Rebuild the system in any language from scratch
- Verify correctness independently of the implementation
- Onboard new contributors without reading code

## Each Surviving Layer Matters

- If only `overview/` survives → you can recover product intent and derive a likely spec.
- If only `spec/` survives → you can rebuild the product behaviorally in any language.
- If only `architecture/` survives → you can reconstruct the current implementation shape.

The stronger the docs, the more disposable the code becomes.

## Writing Philosophy

- **Precise over vague.** Define limits, ordering, retries, idempotency, error codes explicitly.
- **Concrete over abstract.** Use scenarios with actual values, not placeholders.
- **Testable over aspirational.** Every scenario should be verifiable — you could write a test for it.
- **Evidence over green ticks.** A passing check is useful only when it exercises the intended behavior and produces inspectable evidence. Document what was checked, how, and why it proves the claim.
- **Declarative over imperative.** Describe what happens, not how to click through a UI.
- **Behavior over implementation.** `spec/` never mentions classes, functions, frameworks, or file names.
- **Internal behavior over UI.** Document what the system *does* internally (state machines, processing pipelines, decision logic) — not what buttons a user clicks. A UI redesign should never require a spec update.
- **Protocol over presentation.** Document message formats, API contracts, wire protocols, state transitions, and data schemas. The presentation layer (colors, layout, components) is implementation detail.
- **User experience over interface.** Document what the user *experiences* and *perceives* — not the interface they use to get there. "The user is authenticated" not "The user clicks the login button and a modal appears".

## Verification as a Cross-Cutting Layer

Every project MUST maintain a `node_type: verification` document at `docs/verification/strategy.md` or an explicitly linked equivalent. The strategy is not a duplicate of the spec or a list of framework names. It answers:

1. **What is being verified?** Product goals, behavioral requirements, protocols, invariants, user journeys, and operational properties.
2. **How is it checked?** Static checks, unit/component tests, integration tests, contract tests, UI or end-to-end journeys, manual exploration, and operational/release checks as applicable.
3. **What is the actual toolchain?** Test runners, browser automation, linters, type checkers, analyzers, service doubles, environments, fixtures, and exact commands.
4. **What is the execution shape?** Fast smoke checks, standard checks, long-running suites, release gates, and their CI/local cadence.
5. **What counts as evidence?** Assertions, reports, screenshots/traces, logs, metrics, protocol captures, approvals, or other inspectable artifacts.
6. **What is missing or risky?** Explicitly document untested layers, manual-only checks, flaky checks, and behavior not covered by evidence.

Verification documents MUST map important goals and spec requirements to verification IDs or named checks. They MUST distinguish:

- **Test result:** a mechanical check passed.
- **Verification result:** the check passed and its scope/evidence supports the intended behavior.
- **Validation result:** the behavior is useful and matches the product/user intent, including where human judgment is required.

## Document Lifecycle

- **Never physically delete a file.** No text must be lost as a result of any operation. Mark deprecated docs with `status: deprecated` and add `supersedes` links. Moving to `archive/` is allowed — the file still exists, it just changes location. `git rm` followed by no trace is forbidden.
- **Never silently change.** Every meaningful update bumps `updated:` and explains what changed.
- **Archive preserves history.** Completed change proposals move to `archive/` with full context.
- **Stories preserve memory.** `docs/stories/` holds dated narratives of how the system was learned the hard way. When a story reveals canonical truth, promote it into `spec/`, `architecture/`, `guides/`, or `ops/` — but keep the story as provenance.
- **INDEX.md is always current.** After any doc change, run `python scripts/index.py` to regenerate all INDEX.md files. **Never hand-edit INDEX.md — the script wipes and overwrites them completely.** The root index also provides the generated folder hierarchy and calculated file inventory.
