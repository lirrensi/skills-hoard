# Batch Results Reference

Results are the product of the batch. They should be structured enough to merge and
human-readable enough to trust.

## Default Result Schema

```json
{
  "item_id": "string",
  "status": "completed | skipped | blocked | failed | pending | stale",
  "summary": "string",
  "evidence": "string or array",
  "risk": "none | low | medium | high | unknown",
  "next_action": "string"
}
```

Customize the schema for the task. For example, code reviews may need `file`, `severity`,
and `recommendation`; ticket audits may need `owner`, `priority`, and `blocked_by`.

## Aggregation Rules

1. Keep original item fields in the combined output when practical.
2. Add metadata: status, worker id/job id if available, errors, runtime, and result JSON.
3. Preserve raw worker output for debugging long or risky batches.
4. Produce a final human summary grouped by status, risk, owner, area, or next action.
5. Clearly list incomplete items and whether they are retryable.

## Quality Checks

- Count source items and result rows; they must match unless explicitly filtered.
- Validate every result against the declared schema.
- Ensure no item has multiple conflicting final results.
- Check that evidence is specific enough to support the summary.
- Confirm that failures are represented as data, not silently omitted.
- Confirm tracker/source status was updated for every completed, blocked, skipped, or failed item when writable.
- Confirm tracker/source status was updated for every completed, blocked, skipped, failed, pending, or stale item when writable.
- Confirm unresolved items include comments explaining what blocked them.
- Confirm completed items were accepted only after coordinator verification, not just worker self-report.
- Confirm grouped execution results map cleanly back to individual tracker items.
- Confirm tracker-facing comments were written or cleaned up by the coordinator, not copied raw from worker noise.

## Artifact Naming

Prefer explicit paths from the user. Otherwise use a local, descriptive artifact name:

```text
batch-results/<batch-slug>/items.jsonl
batch-results/<batch-slug>/results.jsonl
batch-results/<batch-slug>/summary.md
batch-results/<batch-slug>/results.csv
```
