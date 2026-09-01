---
name: batch-task-executor
description: >
  Experimental workflow skill for coordinating many related tasks from any source.
  Use when the user asks to mass-process, batch-execute, fan out, parallelize, audit,
  review, summarize, migrate, or solve a list of tasks from a file, issue tracker,
  pasted list, directory, table, CSV, markdown checklist, Jira export, PR list, or
  direct instructions. The skill first determines how to read tasks and update their
  status/comments, then analyzes ordering, conflicts, blockers, and safe execution mode.
---

# Batch Task Executor Skill

Coordinate many related work items from an arbitrary task source. The coordinator first
figures out how to read the tasks and how to mark each task done, blocked, skipped, or
failed in the same tracker/source. Only after intake and basic feasibility analysis does
it decide whether to execute sequentially, fan out to workers, or ask for clarification.

This skill is **experimental**. Treat it as a planning and orchestration pattern first,
not as a fixed CLI contract. Runtime-specific fan-out tools may differ across harnesses.

**Project task systems:** If the project you're working in already has a task tracker,
ticket system, TODO list, or any form of work-tracking infrastructure — use that.
Don't create a new tracking mechanism when one already exists. This skill integrates
with whatever is already in place; the convention is to work within the existing
project infrastructure rather than adding a parallel system.

## Core Idea

The input does not define the workflow. A CSV, markdown checklist, Jira board, folder of
files, pasted bullet list, test matrix, package list, or direct user prompt are all just
ways to obtain a set of work items.

The stable contract is:

1. Determine how to read the task source.
2. Determine how to update the task source with status and optional comments, including how to mark work in progress.
3. Normalize tasks into work items with stable ids and source references.
4. Scout enough context to judge scope, risk, ordering, dependencies, and conflicts.
5. Separate clear/easy work from blocked, ambiguous, dangerous, or mutually exclusive work.
6. In interactive mode, ask only for clarifications that materially affect safety or correctness.
7. In non-interactive mode, mark hard/blocked/unclear items and continue with safe items.
8. Build an execution plan that separates sequential prerequisites from safe parallel groups.
9. Execute through whatever tools/harnesses are available, bounded by safety and write policy.
10. Verify reported completion before marking tracker items done.
11. If work is incomplete, decide whether to retry, continue sequentially, mark blocked, or leave pending/stale.
12. Update the tracker/source item-by-item or group-by-group with status and useful comments.
13. Summarize final coverage, failures, blocked items, pending/stale items, and next actions.

## When To Use

Use this skill when the user wants to process many similar tasks, including:

- audit one file, component, package, service, incident, PR, ticket, migration target, or customer record per item
- apply the same review rubric across many inputs
- generate structured summaries for a backlog, checklist, or tracker
- perform many independent fixes or investigations with clear boundaries
- parallelize repetitive research, validation, or codebase exploration

Do **not** use this skill when:

- there is only one task
- the tasks are tightly coupled and require a single coherent edit plan
- running workers concurrently could corrupt shared state
- the user needs real-time interactive decisions between every item

## Operating Modes

- **Plan-only mode:** Build the batch plan, item schema, worker prompt, and result schema without executing.
- **Execute mode:** Run the batch using the best available local harness or subagent mechanism.
- **Resume mode:** Continue a partially completed batch from persisted item/result state.
- **Reduce-only mode:** Merge, validate, or summarize already completed worker outputs.

If execution harness support is missing or unsafe, fall back to plan-only mode and give
the user exact commands or next steps.

## Workflow

1. Read `references/intake.md` to normalize input sources into batch items.
2. Read `references/execution.md` to select a safe execution strategy.
3. Read `references/results.md` to define worker reporting and aggregation contracts.
4. Read `references/coordinator.md` for dependency/conflict analysis and clarification rules.
5. For non-trivial batches, create a batch plan using `templates/batch-plan.md`.
6. Execute only after the item list, tracker update method, and risk model are clear enough.

## Required Batch Plan Fields

Every batch should have:

- `batch_goal` - what the whole batch is trying to accomplish
- `source` - where items came from, such as file path, tracker, pasted list, glob, or direct prompt
- `read_method` - how the coordinator obtains the task list
- `update_method` - how the coordinator marks status and adds comments back to the source
- `in_progress_method` - how the coordinator marks a task currently being worked on, if supported
- `items` - normalized records, each with a stable `item_id`
- `dependency_map` - required ordering, mutually exclusive items, conflicts, and invalidation risks
- `execution_groups` - logical groups of one or more items that can be delegated together
- `worker_instruction` - task template for one item
- `result_schema` - expected fields in each worker result
- `max_concurrency` - bounded parallelism, chosen conservatively
- `write_policy` - whether workers may edit files or only report findings
- `merge_policy` - how results become the final answer or artifact
- `verification_policy` - how to confirm coverage, quality, and failures

## Worker Contract

Each worker gets exactly one item unless the selected harness requires chunking. Workers
must return exactly one structured result for their assigned item.

Workers may also receive a small coherent group of items when that is safer or more
efficient than one-worker-per-item, such as three related UI polish fixes in the same
component. Do not group unrelated items just to reduce job count, and do not split tightly
coupled changes into parallel workers that will fight over the same code.

Minimum result fields:

- `item_id`
- `status`: `completed`, `skipped`, `blocked`, `failed`, `pending`, or `stale`
- `summary`
- `evidence`
- `next_action`

When a harness provides a formal result-reporting tool, the worker must use that tool
exactly once. When no such tool exists, require the worker's final message to contain a
single JSON object matching the result schema.

## Safety Rules

- Prefer read-only workers unless the user explicitly asks for changes.
- Never let multiple workers edit the same file, database row, ticket, or external object.
- Use stable item ids; do not rely on row numbers unless no better id exists.
- Before execution, determine how each item should be marked done, blocked, failed, or skipped.
- Mark items or groups as in-progress when the tracker/source supports it and doing so will not create noise.
- Do not blindly spawn every task in parallel. Decide sequential vs parallel vs grouped execution first.
- Group tasks by logical ownership, files touched, subsystem, dependency chain, and verification needs.
- Execute prerequisites before dependent tasks, especially when tests or UI changes rely on backend/API changes.
- Assume relevant tests/checks are implied unless the user explicitly says not to verify.
- Verify worker claims before marking tracker items done.
- Only the coordinator/orchestrator writes final tracker comments. Workers report to the coordinator; the coordinator turns that into concise, clear, bullshit-free tracker updates.
- Retry incomplete work only when the failure appears unrelated to the task itself, such as transient environment/tool/network problems.
- When incomplete work hits a hard task blocker, mark it blocked or pending/stale with a concise explanation instead of retrying blindly.
- Prefer updating the user's existing task tracker over creating a separate status system.
- Add concise comments when an item is blocked, failed, risky, or completed with notable caveats.
- Leave comments empty or minimal for boring successful items unless the tracker/team convention says otherwise.
- Keep concurrency modest by default. Increase only when the task is read-only or the user requests speed.
- Persist the item list and partial results for long batches when possible.
- If any worker fails to report, mark that item as `failed` with the last observed error.
- Summaries must distinguish completed work from skipped, blocked, and failed items.

## Example Requests

- "Use batch-task-executor to review every component listed in `components.md`."
- "Mass-audit these Jira tickets and return risk, owner, and next action."
- "Here are 40 migration targets; fan them out and tell me which are risky."
- "Check every package in this monorepo for deprecated APIs."
- "Process this CSV, but don't make the workflow depend on CSV specifically."

## Output Expectations

Final response should include:

- total item count
- completed / skipped / blocked / failed counts
- output artifact path if one was produced
- top findings or grouped results
- unresolved items with reasons
- recommended next batch or follow-up action
