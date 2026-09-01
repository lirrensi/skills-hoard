# Testing: System Flows

> Load when the task is about end-to-end truth, critical journeys, black-box verification, or workflows that cross module boundaries.

---

## End-to-End Definition

- [ ] CRITICAL Treat end-to-end as a real workflow through a real boundary to a real outcome; it is not limited to browser UI
- [ ] CRITICAL Browser journeys, CLI commands, API consumer flows, file-processing pipelines, and multi-service workflows all qualify when they prove the full path
- [ ] HIGH Keep these tests narrow and critical; if a path is not mission-important, it probably belongs in lower-level suites

---

## Workflow Expectations

- [ ] CRITICAL IF a user or machine can complete a business-critical journey -> THEN test the full sequence, its expected success result, and its most likely failure modes
- [ ] CRITICAL IF a flow crosses trust or persistence boundaries -> THEN verify the side effects at each meaningful checkpoint, not only the final response
- [ ] HIGH IF background jobs, queues, webhooks, or scheduled work complete the flow -> THEN assert the whole chain, not just the first trigger
- [ ] HIGH IF the interface is a CLI or machine protocol -> THEN test real invocation, input/output contract, exit status, and filesystem or network side effects

---

## Stateful and Reconciled Flows

- [ ] CRITICAL IF the product has workflows or state machines -> THEN test valid transitions, invalid transitions, terminal states, and exactly-once side effects across the full journey
- [ ] CRITICAL IF the user-visible outcome depends on async completion, indexing, exports, or derived read models -> THEN test eventual convergence and verify no loss, duplication, or silent drift appears along the chain
- [ ] HIGH IF approval, import, export, or reconciliation flows exist -> THEN test operator-visible checkpoints, row-level or item-level failure reporting, and rerun safety
- [ ] HIGH IF the same end-to-end flow can resume after retry, reconnect, or restart -> THEN prove the resumed path finishes correctly without duplicating work
- [ ] HIGH IF user trust depends on a fresh follow-up read after write -> THEN test whether the workflow guarantees immediate visibility or clearly communicates eventual consistency instead of flickering between states

---

## Reliability Rules

- [ ] CRITICAL Do not use fixed sleeps; wait on observable readiness, durable state, or explicit events
- [ ] CRITICAL Keep tests independent; one flow must not prepare the world for another flow silently
- [ ] HIGH Run against a production-like environment for the surfaces under test; a fake universe does not prove the real journey
- [ ] HIGH Capture enough evidence on failure - logs, screenshots, output, traces, persisted artifacts - to explain what died
