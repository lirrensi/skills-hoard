# Batch Execution Reference

Execution is harness-agnostic. After intake, analysis, and any required confirmation,
use whatever safe tools are available in the current runtime. Do not hard-code the skill
to one implementation such as CSV fan-out or a specific subagent API.

## Execution Strategy Order

1. **Native batch/subagent API:** Use when the harness exposes a formal fan-out tool and the tasks are suitable for it.
2. **Task/subagent tool loop:** Spawn bounded workers manually if supported.
3. **CLI-backed worker runner:** Use scripts, local commands, test runners, or project tools when appropriate.
4. **Direct coordinator execution:** The coordinator may do clear small tasks itself when delegation adds overhead.
5. **Sequential fallback:** Process items one by one when concurrency is unsafe or unavailable.
6. **Plan-only fallback:** Produce a ready-to-run plan if execution cannot be done safely.

The selected strategy is an implementation detail. The important contract is that each
task or execution group gets clear instructions, finishes or reports a blocker, is
verified, and is reflected back into the tracker/source.

## Delegation Unit Selection

Do not assume one task equals one worker. Choose delegation units deliberately:

- **Single-item worker:** best for independent audits, isolated fixes, one ticket per worker, or high-risk changes.
- **Small coherent group:** best for several related tasks in the same subsystem, such as multiple UI polish fixes in one component.
- **Sequential chain:** best when one item creates prerequisites for another, such as backend API change before frontend integration.
- **Coordinator-owned direct work:** best for trivial updates, tracker cleanup, or changes cheaper to do than delegate.

Avoid grouping when tasks touch unrelated subsystems, require different expertise, have
different risk profiles, or may conflict over the same files/state.

## Concurrency Guidance

- Default to low concurrency for code edits or external side effects.
- Higher concurrency is acceptable for read-only audits, summarization, or independent research.
- Avoid workers writing to shared files. Have workers write item-specific outputs, then merge.
- If using external services, respect rate limits and authentication boundaries.
- Parallelize only after identifying shared files, shared state, ordering dependencies, and test dependencies.
- Prefer separate workers for independent frontend/backend/docs/research streams, but sequence them when one depends on another.
- Do not launch frontend changes that rely on backend behavior before the backend/API contract exists or is stubbed intentionally.
- If multiple tasks may edit the same file or component, group them into one worker or execute sequentially.

## Execution Ordering

Common ordering rules:

1. Define or update shared contracts first: schemas, APIs, types, interfaces, migrations.
2. Implement backend/service foundations before UI or integration tasks that rely on them.
3. Apply dependent frontend/client changes after the underlying contract is stable.
4. Run or update tests after the relevant implementation layer exists.
5. Run final cross-cutting verification after all dependent groups complete.

Tests are usually implied. If a task will obviously require tests or existing tests will
fail until a prerequisite task is done, order the work so tests become meaningful rather
than noisy.

## Worker Prompt Template

Each worker prompt should include:

- exact item id(s), item context, and execution group id when grouped
- clear boundary: one item only, or one explicitly listed coherent group only
- allowed tools and write permissions
- result schema
- requirement to report exactly once
- evidence requirements
- timeout or stop condition

## Write Policies

- `read_only`: Workers may inspect and report only.
- `isolated_write`: Workers may edit files uniquely owned by their item.
- `patch_only`: Workers produce proposed patches, but the coordinator applies them.
- `side_effect_allowed`: Workers may touch external systems only with explicit user approval.

## Coordinator Duties

- Ensure every item is assigned once.
- Analyze item scope, ordering, dependencies, conflicts, and invalidation risks before dispatch.
- Execute prerequisite or shared-state tasks before dependent parallel work.
- Decide the correct delegation unit: single item, grouped items, sequential chain, or direct coordinator work.
- Track pending, running, completed, failed, skipped, and blocked items.
- Update the task tracker/source after each item or safe batch checkpoint.
- Collect results without losing failed-worker diagnostics.
- Read each worker report and perform quick verification before accepting completion.
- Retry only idempotent work unless the user approves otherwise.
- Verify that the final aggregation covers all source items.

## Delegation-to-Completion Loop

For each execution unit:

1. Prepare a prompt or command with scope, allowed changes, relevant context, expected result schema, and verification expectations.
2. Mark the covered tracker item(s) in-progress when useful and supported.
3. Run it using the best available harness/tool.
4. Wait for completion or timeout according to the plan.
5. Read the reported result, artifacts, diffs, logs, or test output.
6. Perform a quick independent verification appropriate to the task.
7. If incomplete, classify it as transient/environmental, hard-blocked, breaking-scope, or partial progress.
8. Retry only transient/environmental failures when safe; otherwise mark blocked, pending/stale, failed, or skipped.
9. Mark each covered tracker item done only after verification.
10. Add a concise coordinator-written comment when the result is blocked, failed, risky, caveated, pending/stale, or otherwise non-obvious.
11. Feed discovered blockers/dependencies into the remaining execution plan.

Verification can be lightweight but must be real: inspect changed files, run relevant
tests/checks when feasible, verify generated artifacts exist, or confirm tracker/API
state. Do not mark `done` solely because a worker said it was done.

Workers report to the coordinator only. The coordinator is responsible for translating
messy worker output into clear tracker status and concise comments.
