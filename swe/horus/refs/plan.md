# Plan Writing

A plan is the handoff from Horus to the worker. It says *what* must change, what behavior should result, and how completion will be proved. It carries enough responsibility for the worker to finish the bounded task without a second planning or verification loop, while staying proportional to the task.

The orchestrator writes the behavior and success contract. The worker decides ordinary implementation details, executes the change, tests it, verifies it, and reports evidence.

---

## Plan vs Direct vs Brief

| Situation | Produce |
|---|---|
| Micro change — rename, fix one line, obvious scope | **Direct** — no document. State the behavior result and focused verification in the assignment. |
| Standard feature, bug fix, concrete work | **Plan** — one proportional document. Include behavior, steps, tests, verification, and success criteria. |
| Investigation, review, exploration | **Brief** — compass, not recipe. See `./brief.md`. |

---

## Plan Format

```markdown
# Plan: [Title]
_[One sentence. What does done look like?]_

## Behavior Change
_What is different for users, operators, or other code after this work? Describe the intended end state and important boundaries._
- [behavior before → behavior after]
- [important non-goal or preserved behavior]

## Success
_What the worker must make true and prove before returning._
- [ ] [criterion]
- [ ] [criterion]

## Testing & Verification
_Use the smallest strategy that gives credible evidence for this task. Do not pad a small change with an elaborate test campaign._
- **Tests:** [tests to add or update, if needed]
- **Checks:** [commands, flows, fixtures, or manual checks to run]
- **Evidence:** [outputs or concrete observations that establish completion]

## Execution
- **Documentation:** [update mature canon as the final step / skip because docs are absent, immature, or already correct]
- **Initiative:** [commit/deploy permissions or "no commit/deploy"]

## Prerequisites
_What must exist or be true before Step 1._
- [pre-req]

## Scope *(if needed)*
_What explicitly NOT to touch. Only include when there is a real boundary to respect._
- `path/to/module` — deliberately left alone

---

## Steps

_Steps are in execution order. Horus already knows which depend on which — Ptah follows the order given._

### Step 1: [Title]

_What to achieve._
- **Expected:** [what should be true after this step]
- **Verify:** [focused check or evidence for this step]
- [ ] Complete

### Step 2: [Title]

_What to achieve._
- **Expected:** [what should be true after this step]
- **Verify:** [focused check or evidence for this step]
- [ ] Complete
```

---

## Multi-Plan: Chaining for Large Tasks

When the work is too large for one plan, break it into a chain of meaningful plans rather than bloating one document or slicing the work into arbitrary crumbs.

**Sequential chain** — each plan depends on the previous:
```
Plan A → Plan B → Plan C
```
Run one after another. Each plan should leave a usable, verifiable result before the next begins.

**Parallel plans** — independent sub-tasks can run at the same time:
```
          → Plan B
Plan A ──┤
          → Plan C
```
Only when the sub-tasks do not depend on one another and do not touch conflicting files or state.

Horus decides the structure. Ptah executes one plan at a time. Horus hands off the next when ready.

---

## Rules

| Rule | Meaning |
|---|---|
| **Behavior before code** | Say what changes for users, operators, or dependent code. Don't write half the implementation. |
| **Real paths** | Name files and modules explicitly. No placeholders. |
| **Per-step expected** | Every step says what's true when it's done. |
| **Per-step verification** | Every step names the smallest credible check or evidence. |
| **Overall success** | Top-level criteria. What "done" means end-to-end. |
| **Testing in the plan** | State what to test and how to prove the behavior; scale it to the task. |
| **Docs last, conditionally** | Update mature, affected canon only after the behavior is implemented and verified; otherwise say why it is skipped. |
| **Initiative explicit** | State whether commit/deploy actions are included and let the worker follow that boundary. |
| **Scope only when needed** | Don't add an empty Scope section. Include it when there's something Ptah must not touch. |
| **Checkboxes track progress** | Ptah ticks them off. On re-run, scan for first `[ ]` and continue. |

Keep plans proportional. A micro change does not need a ceremonial document. If a standard plan becomes too extensive, split it into meaningful dependent plans instead of forcing one oversized handoff.

---

## Example: Small Plan

```markdown
# Plan: Add user avatar to profile
_Users can upload and see their avatar on the profile page._

## Behavior Change
- **Before:** Profile has no avatar.
- **After:** Users see their uploaded avatar, or a stable default when none exists.

## Success
- [ ] Avatar upload endpoint accepts images under 5 MB
- [ ] Profile page displays the uploaded avatar or a default
- [ ] Existing profile data is unchanged

## Testing & Verification
- **Tests:** Add endpoint and display-path tests for upload, display, and default behavior.
- **Checks:** Run the focused profile test suite and exercise the upload/display flow.
- **Evidence:** Record the commands and results in the worker report.

## Execution
- **Documentation:** Update mature profile behavior docs after verification if they exist and are affected.
- **Initiative:** No deploy; commit only if Horus authorizes it.

## Prerequisites
- `POST /profile` endpoint exists (see `src/routes/profile.ts`)
- Image storage configured (`src/storage/images.ts`)

## Scope
- `src/routes/avatar.ts` — do not touch, handled in a separate plan

## Steps

### Step 1: Add upload endpoint
- **Expected:** `POST /profile/avatar` accepts multipart image, saves to storage, returns URL.
- **Verify:** Focused endpoint tests pass, including the size boundary.
- [ ] Complete

### Step 2: Display avatar on profile
- **Expected:** Profile page shows saved avatar. Falls back to default silhouette if none set.
- **Verify:** Display tests and the focused profile flow pass for both saved and missing avatars.
- [ ] Complete
```

Save to `.agents/reports/plan_{short-name}_{yyyy-mm-dd}.md`.
