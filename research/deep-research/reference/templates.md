# Deep Research Templates

Use these as copy-start points. Keep them simple, but do not under-save. Fill them in as the research progresses.

The default workflow needs only two files:

- `materials.md`
- `summary.md`

Add `plan.md` only when the task is large enough to benefit from explicit search tracks.

## 1. `materials.md` Template

```markdown
# Research Materials: <topic>

## Status
- current_stage: alignment
- overall_state: in_progress
- mode: balanced
- question: <main question>
- last_updated: <YYYY-MM-DD>

## Stage Checklist
- [ ] alignment
- [ ] capability_check
- [ ] scope
- [ ] scaffold
- [ ] search_plan
- [ ] evidence_collection
- [ ] verification
- [ ] synthesis
- [ ] finalize

## Capabilities
- search: yes / no / unknown
- fetch: yes / no / limited / unknown
- parallel: yes / no / unknown
- file_write: yes / no / unknown
- notes: <important limits>

## Alignment
- Raw user request:
- Interpreted request:
- Other plausible meanings:
- Confirmed intent:
- Mini plan:
  1.
  2.
  3.
- Clarification needed?: yes / no

## Scope
- Goal:
- In scope:
- Out of scope:
- Success looks like:

## Search Plan
- Angle 1:
  - purpose:
  - query ideas:
  - can run in parallel: yes / no
- Angle 2:
  - purpose:
  - query ideas:
  - can run in parallel: yes / no

## Collected Evidence

### Source 1
- URL:
- Title:
- Date:
- Angle:
- Why it matters:
- Snippet 1:
- Snippet 2:
- Notes:

### Source 2
- URL:
- Title:
- Date:
- Angle:
- Why it matters:
- Snippet 1:
- Snippet 2:
- Notes:

## Findings By Angle

### Angle 1
- Finding:
- Supporting source(s):
- Supporting text:
- Notes:

### Angle 2
- Finding:
- Supporting source(s):
- Supporting text:
- Notes:

## Follow-Up Hooks
- Likely next question:
- Current best answer:
- Evidence pointers:

- Likely next question:
- Current best answer:
- Evidence pointers:

## Contradictions
- Claim A:
- Claim B:
- Source A:
- Source B:
- Likely cause: time drift / scope mismatch / definition mismatch / source-quality mismatch / unresolved dispute
- Status: unresolved / resolved / disputed
- Notes:

## Open Questions
- ...
```

Rule of thumb: if the source is relevant, save it. Text is cheap; losing useful context is dumb.

## 2. `summary.md` Template

```markdown
# Research Summary: <topic>

## Executive Summary

## Best Current Answer

## Key Findings
- ...

## Trade-Offs / Risks
- ...

## Contradictions / Uncertainties
- ...

## Recommendation / Next Step
- ...
```

## 3. `plan.md` Template

Use this only when the task has enough moving parts to justify a dedicated plan file.

```markdown
# Research Plan: <topic>

## Intent
<What the user wants and why>

## Mode
- breadth / balanced / depth

## Search Tracks
1. <track>
2. <track>
3. <track>

## Parallel Split
- worker 1:
- worker 2:
- critic:
- fact-checker:

## Stop Conditions
- We can stop when...

## Known Risks
- ...
```

## 4. Parallel Worker Drop-In Template

Use this when the harness supports parallel work and the task splits cleanly.

```markdown
### Worker Brief
- Role: researcher / critic / fact-checker
- Assigned angle:
- Questions to answer:
- What to collect:
  - URL
  - title
  - date
  - snippet
  - why it matters
- Output target:
  - append mergeable notes for `materials.md`
```

## 5. Query Scratchpad Template

Use this to quickly test phrasing before the full run.

```markdown
## Query Scratchpad

### Orientation
- <broad query>

### Angle-specific
- <query 1>
- <query 2>

### Verification
- <query to verify a claim>

### Adversarial
- <query that might disprove the obvious answer>
```

## 6. Quick Fact-Check Block

Use this inside `materials.md` when the task is narrow and precision-heavy.

```markdown
## Fact Check
- Claim:
- Source A:
- Source B:
- Agreement / conflict:
- Best current reading:
- Confidence: low / medium / high
```

## 7. Optional Academic Reading Block

Keep this only when the research is paper-heavy.

```markdown
### Paper Note
- Citation:
- Venue / year:
- Problem:
- Contribution:
- Method:
- Main result:
- Limitation:
- Why it matters here:
```

Templates are here to reduce friction, not create bureaucracy. Copy the smallest thing that works.
