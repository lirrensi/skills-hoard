---
name: engage
description: >
  Autonomous execution mode triggered by the word "engage". Use when the user has
  finished planning and wants the agent to execute autonomously without further questions
  until the workflow is fully complete. The agent must build, test, verify, and deliver
  proof of work — never exiting with an incomplete or unverified result. Trigger on:
  "engage", "go autonomous", "execute the plan", "run it", "make it happen", or any
  explicit signal to switch from planning mode into fully autonomous build-and-verify mode.
---

# Engage — Autonomous Execution Mode

Switch from planning into autonomous execution. Once engaged, the agent operates without
asking questions, stopping only for catastrophic unrecoverable failures.

**Golden rule:** If you say you're done, you must have built it, tested it, verified it,
and proven it. No exceptions. No "it should work" — only "it works, and here is the proof."

---

## When to Engage

Engage when:
- The user explicitly says **"engage"**, **"go"**, **"execute"**, **"run it"**, or similar
- A plan has been discussed and the user signals autonomous execution is desired
- The user says "don't ask me again, just do it"

Do **not** engage when:
- The user is still actively debating options or scope
- Critical decisions remain unmade that would change the implementation
- The task is purely research or exploration with no build target

---

## Operating Principle

**Plan → Engage → Execute → Verify → Deliver**

Once engaged:
- **No questions.** Do not use the `question` tool. Do not ask for clarification.
- **No early exits.** Do not mark done until verification is complete.
- **No hand-waving.** "Should work" is not acceptable. Proof is required.
- **Full professionalism.** Update everything: code, tests, docs, config, build, verification.

The only valid reason to stop early is a **catastrophic, unrecoverable failure**.

---

## Execution Workflow

### 1. Orient — Understand the Project Landscape
Determine what kind of project this is and what "done" looks like. Assess docs, tests, build system, verification, conventions.

### 2. Plan — Confirm or Build the Execution Plan
If a plan exists, review against the landscape. If not, create one. Include files to change, tests, docs, build steps, verification, definition of done.

### 3. Execute — Edit, Build, and Sync
Work through the plan. Stay bounded. Self-check. Do not stop for minor ambiguity. Update code, tests, docs, and configs. Run quality gates.

**Do not claim completion at this stage.** Execution alone is not done.

### 4. Verify — Prove It Works
The critical step. Must include at least one of: test execution, build verification, runtime verification, deployment check, lint/type/format checks.

**Proof of work is mandatory.** The final response must include what was built, test results, build results, verification results, and any caveats.

### 5. Deliver — Clear, Complete, Professional Handoff
Include: Done, Files, Validation, Proof, Decisions, Assumptions, Deviations, Blockers, Next steps.

The user should be able to read the summary and immediately verify the result.

---

## Example Triggers

- "Okay, that plan looks good. **Engage.**"
- "**Execute the plan.** Don't ask me anything else."
- "**Go autonomous.** Build it, test it, and show me it works."
- "**Make it happen.** I don't want to babysit."

---

## Deeper Reading

| Topic | File |
|---|---|
| What "Done" means, catastrophic failure rules, example deliverable | [`references/completion.md`](references/completion.md) |
