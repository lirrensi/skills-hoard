# Apply Mode

Use this mode when the user wants a documented customization to keep working on a newer
or fresh upstream codebase.

## Goal

Preserve the feature, not the original diff. The feature succeeds only if it exists and
works correctly on the current upstream according to the Definition of Done.

## Workflow

### 0. Scout and assess feasibility

Before editing, scout the patch and the target upstream to assess how hard this apply is.

Classify the apply as one of:

- straightforward
- substantial adaptation
- breaking or design-heavy

Call out likely break points early when you see them: moved subsystems, replaced
frameworks, changed schemas, security-sensitive rewrites, or missing extension points.
If the path is still feasible, continue right away. If not, escalate with a concrete
blocker.

### 1. Read before editing

Read `micropatch.md` fully. If `hints.diff` exists, read it as a secondary aid.
Understand the feature's intent, expected behavior, scope, and assumptions before making
changes.

### 2. Check for upstream overlap

Before re-applying anything, inspect the current upstream.

Look for cases where upstream now provides all or part of the feature already.

- If upstream has none of the feature, apply the full customization semantically.
- If upstream partially covers it, implement only the missing behavior.
- If upstream implements the same outcome differently, compare that behavior against the
  MicroPatch and Definition of Done before deciding whether anything still needs to be applied.
- If upstream fully covers the feature, do not re-add redundant code. Offer to migrate
  toward the native upstream behavior and update the patch accordingly.
- If upstream now provides a stronger or better-integrated version of the feature, ask
  which guarantees still matter most and patch only those missing guarantees instead of
  restoring the older implementation wholesale.
- Record the overlap and any adaptation in the updated patch.

### 3. Locate the modern integration points

Use `Anchors` and `hints.diff` as search directions, not strict destinations.
Paths, modules, or frameworks may have changed. Find where the behavior belongs now.

### 4. Implement semantically

Do not replay a diff mechanically. Recreate the feature in the current upstream structure
using `Intent`, `What It Does`, `Dependencies and Assumptions`, `Implementation Reference`,
`Anchors`, and `Definition of Done` as the source of truth.

This is where you may re-implement by vibe: adapt the implementation freely if needed,
but preserve the intended behavior and prove it still works. Favor modifying the current
upstream code where the feature belongs now over pasting old code back in unchanged.

When overlap makes the path ambiguous, ask what behavior guarantee actually matters:

- what must still happen
- what may change safely
- what old implementation details are no longer important

Use those answers to preserve the feature contract with the smallest necessary change.

### 5. Verify against Definition of Done

Run the listed checks whenever possible:

- tests
- commands
- API checks
- behavior checks
- manual validation when automation is not available

Reasonable fixes discovered during verification are still in scope.

### 6. Update the patch

After successful application, update `micropatch.md` so it reflects the new upstream
reality:

- updated implementation reference if it materially changed
- revised anchors
- overlap with upstream
- new caveats or migration concerns
- incremented version when the patch was materially refined or adapted

## Apply Output

When apply mode is complete, provide:

- what was implemented
- files changed
- notable adaptations made for the current upstream
- assessed feasibility and likely break points, if any
- overlap detected with upstream, if any
- verification performed
- updated `micropatch.md`
- unresolved risks or follow-up decisions
