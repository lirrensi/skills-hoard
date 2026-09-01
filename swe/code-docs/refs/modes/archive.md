# Mode: Archive

**Trigger:** A change proposal has been implemented and reviewed. It's time to merge its behavior deltas into the main specs and preserve the change for history.

---

## Preconditions

Before archiving, verify:
1. All tasks in `tasks.md` are checked off (completed).
2. The implementation matches the behavior deltas (Sync mode was run or verified).
3. Stakeholders have approved the change.
4. The verification strategy and traceability matrix reflect the changed behavior, or explicitly record the remaining verification gap and risk.

If any of these aren't true, **do not archive.** Flag what's missing.

---

## Workflow

### Step 1: Read the change
Load all artifacts from the change folder:
- `docs/changes/<name>/proposal.md`
- `docs/changes/<name>/behavior.md`
- `docs/changes/<name>/design.md`
- `docs/changes/<name>/tasks.md`

### Step 2: Apply ADDED requirements
For each requirement in the `## ADDED Requirements` section of `behavior.md`:
1. Find the target spec document (from `links: documents` in frontmatter or the section heading).
2. Append the requirement and its scenarios to the target spec.
3. Bump `updated:` on the target spec.
4. If the requirement references a new feature file, create it.

### Step 3: Apply MODIFIED requirements
For each requirement in the `## MODIFIED Requirements` section:
1. Find the existing requirement in the target spec.
2. **Replace** the old requirement text and scenarios with the new version.
3. Keep the "(Previously: ...)" note in the archived behavior.md for historical context — don't carry it into the main spec.
4. Bump `updated:` on the target spec.

### Step 4: Apply REMOVED requirements
For each requirement in the `## REMOVED Requirements` section:
1. Find the requirement in the target spec.
2. **Remove** it from the target spec.
3. If the spec document would be empty after removal, mark it `status: deprecated` instead of deleting it.
4. Bump `updated:` on the target spec.

### Step 5: Move to archive
1. Rename the change folder: `docs/changes/<name>/` → `docs/archive/<YYYY-MM-DD>-<name>/`
2. Use today's date as the prefix.
3. Do NOT modify the archived files — preserve them exactly as they were.

### Step 6: Regenerate INDEX.md files
Run `python scripts/index.py` — the script will:
1. Remove the archived change from `docs/changes/INDEX.md`.
2. Add the archived change to `docs/archive/INDEX.md`.
3. Refresh any affected spec INDEX.md files (if requirements were merged into them).

### Step 7: Report
```
## Archive Complete

### Change archived
`docs/archive/2026-06-09-add-dark-mode/`

### Specs updated
| Spec | Change | Requirements |
|------|--------|-------------|
| spec/features/ui.md | ADDED | Theme Persistence, System Preference Detection |
| spec/features/ui.md | MODIFIED | Theme Toggle (now in header) |
| spec/features/ui.md | REMOVED | Per-Page Theme Override |

### INDEX.md regenerated
- docs/changes/INDEX.md
- docs/archive/INDEX.md
- docs/spec/features/INDEX.md

### Next steps
- Commit the archived change and updated specs
- Notify team of behavior changes
```

---

## What NOT to do during Archive

- ❌ Modify the archived change artifacts (proposal, behavior, design, tasks) — preserve exact history
- ❌ Skip running `python scripts/index.py` after archive
- ❌ Archive without verifying implementation matches specs
- ❌ Delete changed files instead of archiving them
- ❌ Archive if any tasks are incomplete

---

## Reference Files

Load:
- `../spec-format.md` — for correct spec formatting when merging
- `../verification.md` — for updating verification evidence and traceability
- `../ontology.md` — for updating frontmatter on merged specs
- `../folder-structure.md` — for archive folder naming and layout
