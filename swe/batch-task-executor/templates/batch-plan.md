# Batch Plan: <short-name>

## Batch Goal

<What this batch should accomplish.>

## Source

- Type: <prompt | markdown | csv | json | tracker | codebase | hybrid>
- Reference: <path, URL, glob, pasted list, or description>
- Read method: <file read | CLI | MCP | browser | API | prompt | other>
- Update method: <checkbox | status field | tracker transition | comment | in-session only | other>
- In-progress method: <status field | assignee | comment | none | other>

## Status / Comment Policy

- Done means: <how to mark complete>
- In progress means: <how to mark currently being worked on, if supported>
- Blocked means: <how to mark blocked>
- Failed means: <how to mark failed>
- Skipped means: <how to mark skipped>
- Pending/stale means: <how to mark incomplete but not actively retrying>
- Comment policy: <when to add comments and where>

## Items

```json
[
  {
    "item_id": "example-id",
    "task": "one-item objective",
    "context": {},
    "source_ref": "where this came from",
    "constraints": [],
    "expected_result": {}
  }
]
```

## Worker Instruction

```text
You are processing exactly one batch item.

Item id: {item_id}
Task: {task}
Context: {context}
Source: {source_ref}

Return exactly one result matching the schema below. Include concrete evidence.
```

## Result Schema

```json
{
  "item_id": "string",
  "status": "completed | skipped | blocked | failed",
  "summary": "string",
  "evidence": "string or array",
  "risk": "none | low | medium | high | unknown",
  "next_action": "string"
}
```

## Execution Controls

- Mode: <plan-only | execute | resume | reduce-only>
- Max concurrency: <number>
- Max runtime per item: <duration>
- Failure policy: <continue | stop-on-first-failure | retry-idempotent>
- Incomplete policy: <retry transient/environmental failures; mark hard blockers pending/stale/blocked>
- Write policy: <read_only | isolated_write | patch_only | side_effect_allowed>

## Coordinator Analysis

- Prerequisites: <items that must run first>
- Independent safe items: <items safe to run now/parallelize>
- Sequential/shared-state items: <items that need ordering>
- Execution groups: <which items should be delegated together and why>
- Direct coordinator work: <small tasks not worth delegating>
- Ambiguous/blocking questions: <only meaningful questions>
- Conflicts/invalidation risks: <items that may contradict or invalidate others>
- Non-interactive fallback: <what to mark blocked/skipped if clarification is unavailable>

## Delegation Plan

```json
[
  {
    "group_id": "example-group",
    "items": ["example-id"],
    "mode": "direct | worker | sequential | parallel-safe",
    "rationale": "why these items belong together or must be separate",
    "dependencies": [],
    "verification": ["relevant checks/tests/artifact inspection"]
  }
]
```

## Merge Policy

<How item results become the final report/artifact.>

## Verification Policy

<How to prove all items were covered and outputs are valid.>

Include how worker reports will be read, how claims will be independently checked, and
which tests/checks are implied by the tasks.

## Output Artifacts

- <path or none>
