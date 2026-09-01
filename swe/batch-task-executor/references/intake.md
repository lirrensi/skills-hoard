# Batch Intake Reference

Batch intake converts messy task sources into normalized work items. The skill should
care about item shape, not the original source format. Intake also includes determining
how the task source can be updated with status and comments.

## Supported Source Patterns

- **Direct prompt:** The user lists tasks directly in chat.
- **Markdown:** Checklists, tables, TODO docs, specs, migration plans, incident lists.
- **CSV / TSV / JSON / YAML:** Structured exports from tools or hand-authored tables.
- **Issue trackers:** Jira, GitHub issues, Linear, or similar systems when accessible.
- **Codebase discovery:** Globs, package manifests, service directories, ownership files.
- **Hybrid:** A file provides item ids while the prompt provides the rubric.

## Normalized Item Shape

Use this conceptual shape regardless of source:

```json
{
  "item_id": "stable-human-readable-id",
  "task": "single item objective",
  "context": {},
  "source_ref": "file path, URL, ticket id, row id, or prompt section",
  "constraints": [],
  "expected_result": {}
}
```

## Intake Rules

1. Preserve provenance. Every item should point back to where it came from.
2. Prefer stable ids from paths, ticket keys, package names, or explicit user labels.
3. Split compound rows only when they clearly contain multiple independent tasks.
4. Merge duplicates only when they are semantically the same task and share an id.
5. Determine the write-back/update mechanism before execution when possible.
6. Ask for clarification only when ambiguity creates meaningful risk.

## Quick Tracker Discovery

If the source/tracker is not explicit, inspect only local/project context first:

- README or project overview files
- CONTRIBUTING or development docs
- docs folders
- issue or PR templates
- obvious task files such as TODO, TASKS, ROADMAP, backlog, planning docs, or markdown checklists
- user-provided context from the conversation

Use discovered conventions directly when they are clear. If multiple trackers appear or
the update mechanism is risky, ask in interactive mode or mark blocked in non-interactive
mode.

## Intake Questions When Needed

- Should workers be allowed to modify files or only report findings?
- What task source should be treated as canonical if several exist?
- How should status be updated if the source has no obvious status field?
- What result fields should every item produce?
- What is the maximum acceptable concurrency?
- Should failed items stop the batch or be collected for later retry?
- Where should the combined output be written?
