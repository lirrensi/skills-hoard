---
summary: "What this workflow or behavioral guidance covers and when to apply it"
created: YYYY-MM-DD
updated: YYYY-MM-DD
memory_type: procedural
tags: [domain, topic, workflow]
status: active
confidence: certain
version: 1
reuse: once
skill_ref: ""
related: []
aliases: []
source: ""
---

# Title

## Purpose
What this procedure or guidance achieves and when to use it.

> **Note:** This template works for both task workflows *and* behavioral guidance. If you are documenting how to approach a situation or how to behave, use the **Approach / Behavior** section below instead of the checklist.

## Prerequisites (optional)
What must be true or available before starting.

## Procedure / Checklist
Use for concrete, step-by-step workflows.

1. Step one
2. Step two
3. Step three

## Approach / Behavior
Use for behavioral guidance — how to act, respond, or handle a situation.

- **When this applies:** describe the trigger context
- **Core principle:** the guiding rule or mindset
- **What to do:** specific actions or posture
- **What to avoid:** common missteps in this situation
- **Why this works:** the reasoning behind the approach

## Verification (optional)
How to confirm the procedure completed successfully, or how to recognize the approach is working.

## Troubleshooting / Edge Cases (optional)
Common failures, exceptions, or nuanced situations and how to handle them.

## Related Workflows / Patterns
Links to other procedures or behavioral guides that connect to this one.

## Reuse & Promotion
- **Frequency:** `once` = cold one-off, `often` = hot workflow you run every damn time (e.g. deploy). Default `once` if unsure.
- **Should this become a skill?** Only if stable + validated 2–3x + cross-project + tool-heavy. Behavioral guidance never promotes. See `SKILL.md` → Procedural vs Skill.
- **Skill link:** `skill_ref` frontmatter path when promoted (local-first: `.agents/skills/<name>/SKILL.md`, never global unless asked), else empty.
- **Parallelizable? (optional, env-agnostic):** note which steps are independent and could run in parallel *when workload is heavy and your environment supports delegation* (subagents, background runners, etc.). Never mandatory — some envs have no delegation. Example: `Steps 2+3 are independent file scans — parallelize if slow, else sequential is fine`.
