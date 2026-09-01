# Mode: Sync

**Trigger:** Code has changed and docs may be out of sync, or asked to reconcile docs with existing code.

You read code passively. You never edit it. You update docs to match code, or write discrepancies to a throwaway `code-flags.md` for a code agent to fix.

---

## Using INDEX.md Commit Breadcrumbs

The **root `docs/INDEX.md`** records the git commit (and branch) in a `## Git Context` body section — the exact point in time the docs were last indexed. This is your drift-detection anchor. Before diving into a full sync, check the gap.

### Step 0: Measure the drift gap

1. **Read the indexed commit** from `docs/INDEX.md` — look for the `## Git Context` section:
   ```markdown
   ## Git Context
   - **Commit:** `abc1234`
   - **Branch:** `main`
   ```

2. **Compare it to HEAD.** The gap between the indexed commit and your current HEAD tells you *how many changes landed since docs were last checked* — and therefore how likely the docs are stale.

   ```bash
   # How many commits since docs were last indexed?
   git rev-list --count abc1234..HEAD

   # What files changed? (focus sync on docs that reference these files)
   git diff --stat abc1234..HEAD

   # What were the changes? (skim for behavioral changes)
   git log --oneline abc1234..HEAD
   ```

3. **Assess the risk:**

   | Gap | Risk | Action |
   |-----|------|--------|
   | 0 commits | None | Docs are current — skip sync |
   | 1–5 commits, no code paths referenced by docs changed | Low | Spot-check only |
   | 5–20 commits touching documented code paths | Medium | Targeted sync on affected specs |
   | 20+ commits, refactors, new features | High | Full Sync — walk all docs |
   | Indexed commit doesn't exist on this branch | **Unknown** | You're on a different branch. Re-run `index.py` to anchor, then re-assess. |

### Branch Awareness

The `git_commit` in INDEX.md belongs to the branch it was generated on. This has implications:

- **Switching branches invalidates the breadcrumb.** If you check out a branch where the indexed commit doesn't exist, you have no anchor. Run `python scripts/index.py` to record a fresh commit for the current branch.

- **Finding which branch an index was built on:**
  ```bash
  git branch --contains abc1234
  ```
  This lists all branches that include the indexed commit. If your current branch isn't listed, the index is from a different context — treat it as untrusted.

- **Merging workflows:** After merging branches, re-run `index.py` to anchor to the merge commit. The indexed commit should always be an ancestor of (or equal to) HEAD on the current branch.

- **Long-lived branches:** Each branch accumulates its own drift. If `feature/auth-rewrite` changes `src/auth/` heavily, the `main` branch docs don't reflect those changes until the merge. The INDEX.md commit tells you exactly where each branch's docs stopped tracking reality.

### Using drift to prioritize

When you run Sync mode, sort docs by risk:
1. **Docs with `implements` links** to files that changed since the indexed commit → check first.
2. **Architecture docs** that reference file paths changed since the indexed commit → check second.
3. **Spec docs** in domains touched by recent commits → check third.
4. Everything else → spot-check.

---

## Workflow

### Step 1: Read docs first
Load the canonical docs in order:
1. `docs/overview/` — product identity
2. `docs/spec/` — behavioral requirements
3. `docs/architecture/` — implementation structure
4. `docs/verification/` — verification strategy and evidence map

### Step 2: Read relevant code
Read only the source files related to the docs you're checking. Don't read the entire codebase.

### Step 3: Diff — find every desynchronization
For each requirement/scenario in the spec:
- Does the code implement this behavior? **Check.**
- Does the code do something the spec doesn't mention? **Flag.**
- Does the code contradict the spec? **Flag as conflict.**
- Does the architecture doc match the actual file structure? **Check.**
- Does the verification strategy name the tools, commands, suites, environments, and evidence that actually exist? **Check.**
- Do verification IDs cover important changed requirements and user journeys? **Check.**
- Are any documented checks missing, stale, blocked, flaky, or proving a narrower claim than the docs imply? **Flag.**

### Step 4: Classify each discrepancy

| Type | Example | Action |
|------|---------|--------|
| **Missing behavior** | Spec says MUST validate email, code doesn't | Write flag to code-flags.md |
| **Extra behavior** | Code implements rate limiting, spec is silent | Update spec to document the behavior |
| **Contradiction** | Spec says MUST expire in 15 min, code uses 30 min | If doc is correct → write flag to code-flags.md. If code is correct → update doc |
| **Stale architecture** | Arch doc references `src/old/`, code is in `src/new/` | Update architecture doc |
| **Undocumented feature** | Whole feature exists in code, zero spec coverage | Create spec via Curate mode |
| **Undocumented verification** | Tests, CI checks, browser journeys, or release gates exist with no strategy entry | Update verification strategy |
| **Stale verification** | Strategy command/tool/evidence no longer matches the repository | Update strategy or flag implementation/tooling discrepancy |
| **Unverified claim** | Important requirement or user journey has no credible evidence | Add a check, document a gap, or ask the user to decide |

### Step 5: Decide and act
For each discrepancy:
- **If code is correct** → Update docs to match. Add missing requirements, correct stale values.
- **If doc is correct** → Collect the discrepancy into a flag (see Step 7). Do NOT edit code.
- **If uncertain** → Ask the user. Don't guess.

### Step 6: Update docs
- Apply changes following Curate mode procedures.
- Bump `updated:` dates on modified docs.
- Never silently delete documented behavior — use MODIFIED/REMOVED deltas.

### Step 7: Write throwaway code-flags.md
For every discrepancy where **docs are correct and code is wrong**, write a flag into `code-flags.md` at the **project root** (NOT inside `docs/`). This is a temporary handoff file — never committed, never kept.

Use the format from `../../templates/code-flags.md`. Each flag MUST include:
- **Source doc** (absolute path from docs root)
- **Doc requirement** (quote or tight paraphrase with RFC 2119 keyword)
- **Code location** (file path + line number + function name — precise enough to jump to)
- **What code does** (the wrong behavior)
- **Resolution** (actionable instruction — "Change X to Y on line N")
- **Status: pending**

After writing, hand the file to a code agent: *"Fix every pending flag in code-flags.md, then delete the file."*

The code agent:
1. Reads `code-flags.md`
2. Fixes each flag in code
3. **Deletes `code-flags.md`** — the file is throwaway, never committed

### Step 8: Report to user
Summarize what was found and what was done:

```
## Sync Report — YYYY-MM-DD

### Docs checked
- overview/product.md — synced, no issues
- spec/features/auth.md — 2 discrepancies (1 doc updated, 1 flagged for code)
- architecture/components/agent.md — 1 discrepancy (doc updated)

### Doc updates applied
- spec/features/auth.md — corrected session timeout (15 min → code had 30)
- architecture/components/agent.md — corrected file paths (src/agent/ → src/agents/)

### Code flags written
Wrote code-flags.md at project root with 1 flag:
- Password validation not implemented (spec/features/auth.md → src/auth/register.ts:45)

→ Hand off code-flags.md to a code agent. File is deleted after fixes are applied.
```

---

## When to Sync vs Other Modes

| Situation | Use |
|-----------|-----|
| "Check if docs are up to date" | **Sync** |
| "Update docs to match the new API" | **Sync** (or Curate if you already know the changes) |
| "Write docs for this new feature" | **Propose** (or Curate for small additions) |
| "The architecture changed, update the docs" | **Sync** (check code, then update docs) |

---

## Reference Files

Load:
- `../principles.md` — layer ownership and conflict resolution
- `../ontology.md` — for updating frontmatter on modified docs
- `../index-spec.md` — INDEX.md format and `git_commit` breadcrumb usage
- `../../templates/code-flags.md` — throwaway flag file format

Load as needed:
- `../spec-format.md` — if writing new behavioral requirements
- `../verification.md` — if writing or reconciling verification strategy
- `../folder-structure.md` — if reorganizing docs to match code structure
