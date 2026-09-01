# code-flags.md — Throwaway Handoff Format

**This is NOT a persistent document. It is a temporary working file.** Sync mode generates it at the project root. A code agent reads it, fixes the flagged code, and **deletes the file immediately**. Never commit it. Never keep it. It does not live in `docs/`.

Each flag is a self-contained fix instruction.

---

## Format

```markdown
# Code Discrepancy Flags — {YYYY-MM-DD} Sync Run

## Flag: {Short description}

- **Source doc:** `/spec/features/auth.md`
- **Doc requirement:** {Exact quote or paraphrase — what the doc says MUST/SHOULD happen}
- **Code location:** `src/auth/session.ts:142` — {function/block name}
- **What code does:** {Actual wrong behavior — be specific}
- **Resolution:** {Clear instruction — code must change to match the doc}
- **Status:** pending
```

### Field rules
- **Source doc:** Absolute path from docs root, e.g. `/spec/features/auth.md`
- **Doc requirement:** Quote or tightly paraphrase the doc. Include RFC 2119 keyword (MUST, SHOULD, MAY).
- **Code location:** File path from project root + line number + function/block name. Precise enough that a code agent can jump directly to it.
- **What code does:** Describe the actual behavior — the wrong thing. Contrast with doc requirement.
- **Resolution:** Actionable instruction. "Change X to Y." or "Add validation function before line N."
- **Status:** `pending` (code agent picks up) → `in-progress` (working) → deleted when fixed.

## Lifecycle

1. Sync mode generates `code-flags.md` at **project root** (NOT in `docs/`).
2. File is handed to a code agent: "Fix every flag in this file, then delete it."
3. Code agent works through flags, fixes code, **deletes `code-flags.md`**.
4. File is never committed, never tracked, never persisted.
