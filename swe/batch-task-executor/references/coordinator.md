# Coordinator Reference

The coordinator is not just a dispatcher. It is the part of the workflow that prevents
the batch from becoming a beautiful parallelized disaster.

## Step 1: Locate and Understand the Task Source

Before solving anything, determine how tasks are read and how status is written back.

Common sources:

- markdown checklists or task files
- CSV, JSON, YAML, TSV, or other structured exports
- Jira, GitHub issues, Linear, or other trackers through CLI, MCP, browser, or API
- pasted tasks in the chat
- repo docs that define a team task workflow

If the user did not specify the tracker, do a quick local/context sweep first. Look for
obvious project files such as README, CONTRIBUTING, docs, task files, issue templates,
project notes, or user-provided context. Do not perform broad global searches unless the
user asks.

## Step 2: Determine Status and Comment Mechanics

Every item needs a way to record outcome. Prefer the user's existing tracker/source.

Minimum status model:

- `done` - completed successfully
- `in_progress` - currently being worked on, if the tracker/source supports it
- `not_done` - not completed yet
- `blocked` - cannot proceed without information, access, or prerequisite work
- `failed` - attempted but did not succeed
- `skipped` - intentionally not attempted, usually due to conflict, invalidation, or scope
- `pending` / `stale` - incomplete and not actively retrying, often because it needs a later pass or external change

Tracker-specific examples:

- Markdown checklist: change `- [ ]` to `- [x]`; append an indented note if needed.
- Task table: update status column; optionally fill comment/notes column.
- Jira/GitHub/Linear: transition status if appropriate; add a short comment for problems or caveats.
- Pasted list with no writable source: maintain an in-session status table and ask where to persist if needed.

Comments are encouraged when they add value:

- why an item is blocked or failed
- what prerequisite is missing
- what risk or caveat was discovered
- what was completed if the item is non-obvious

For straightforward successful items, a status change alone is often enough.

Only the coordinator should write tracker-facing comments. Workers and tools report raw
results to the coordinator; the coordinator summarizes them into concise, accurate,
non-dramatic tracker text.

## Step 3: Scout Context Before Execution

For each item or group of similar items, gather enough context to classify:

- scope: small, medium, large, unknown
- difficulty: easy, moderate, hard, unknown
- breakage risk: low, medium, high
- dependencies: what must happen before this item
- conflicts: what other items it may invalidate or contradict
- ownership: files, services, tickets, or external objects touched
- execution mode: safe for parallelism, sequential only, or blocked
- delegation unit: one item, small coherent group, sequential chain, or direct coordinator work

Do not over-research every item before doing anything. Scout enough to detect the obvious
landmines and ordering constraints, then proceed with clear work.

## Step 4: Build the Execution Order

Sort items into buckets:

1. **Prerequisites:** items that unblock other work.
2. **Clear independent work:** safe to execute now, possibly in parallel.
3. **Sequential work:** safe, but must be ordered because of shared files/state.
4. **Small coherent groups:** related items best handled together by one worker or by the coordinator.
5. **Ambiguous work:** needs clarification in interactive mode; mark blocked in non-interactive mode.
6. **Conflicting or invalidating work:** requires coordinator decision; do not blindly execute both.
7. **Too risky / insufficient context:** mark blocked or skipped with explanation if non-interactive.

This is the basic bullshit detector: find impossible, contradictory, underspecified,
dangerous, duplicate, or mutually exclusive items before workers waste time.

## Step 5: Build Delegation Groups

After ordering, decide how work should be delegated:

- Use one worker for a coherent cluster of small related changes in the same area.
- Use separate workers for independent areas that do not share files, state, or prerequisites.
- Use sequential execution when one task creates the contract or foundation another task needs.
- Keep risky architectural or logic changes isolated so they can be verified independently.
- Let the coordinator do trivial tracker/file updates directly if spawning a worker would be silly.

Examples:

- Three small frontend styling fixes in one component can be one execution group.
- Backend API contract changes should usually precede frontend integration work.
- Frontend logic depending on backend behavior should not run first unless using an explicit stub/mock plan.
- Tests that rely on implementation should run after the relevant implementation group, not before.
- Two workers should not edit the same component, migration, or config file at the same time.

If dependencies are likely to shift while work is being done, run the affected items
sequentially. If dependencies are stable and ownership is separate, parallel execution is
usually acceptable.

## Step 6: Clarification Policy

Interactive mode:

- Present only meaningful blockers, conflicts, or serious ambiguity.
- Do not ask about clear, low-risk tasks; just do them.
- Keep questions compact and tied to decisions the user can actually make.
- Offer a recommended path when possible.

Non-interactive mode:

- Do not stall the whole batch on unclear hard items.
- Mark ambiguous/risky/impossible items as `blocked`, `failed`, or `skipped` with a concise comment.
- Continue executing clear safe items.
- Final summary must list unresolved items and what information/action would unblock them.

## Step 7: Incomplete Work Policy

When a worker or execution unit ends incomplete, classify the failure before deciding
what to do next:

- **Transient/environment/tool failure:** retry when safe. Examples: flaky install, network hiccup, test runner crash unrelated to code, temporary service outage, interrupted process.
- **Task blocker:** do not blindly retry. Mark blocked or pending/stale with a concise comment. Examples: missing credentials, missing product decision, dependency not implemented, unclear requirement.
- **Breaking-scope discovery:** stop that item and mark it blocked/skipped/pending according to tracker convention. Example: a small UI button actually requires redesigning a core flow or replacing a subsystem.
- **Partial progress:** update remaining plan. Continue dependent work only if the incomplete part is not required.

Use retries sparingly. Restarting the same impossible task three times is not resilience;
it is a tiny haunted treadmill.

## Step 8: Tracker as Interaction Surface

When the user wants to interact through the task tracker, use it as the shared state:

- read new or updated tasks from the tracker/source
- mark items in-progress when useful and supported
- write status changes back as work progresses
- add comments for blockers, caveats, and failed attempts
- avoid inventing a separate status system unless the source is not writable

The final response should summarize, but the tracker/source should remain the durable
record of item-level progress whenever possible.

## Step 9: Verification Before Tracker Completion

For each completed execution unit:

- read the worker's report or command output
- inspect relevant artifacts or diffs when available
- run relevant tests/checks when feasible
- decide whether the result actually satisfies the task
- update each associated task item only after verification

If verification is impossible or inconclusive, do not pretend. Mark the item blocked or
completed-with-caveat according to the tracker convention, and add a concise comment.
