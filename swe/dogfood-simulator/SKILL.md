---
name: dogfood-tester
description: |
  Autonomous dogfooding and real-world product testing focused on MEANING — what users are actually trying to do, where they get confused, and why the product fails them. Use this skill whenever the user wants to test their own product, find missing features, discover gaps, simulate real user experience, do end-to-end workflow validation, or identify what users will actually struggle with. Trigger on phrases like "dogfood", "test my app", "find gaps", "what am I missing", "real user testing", "workflow testing", "product critique", or when the user points at a repository and asks for feedback, improvement ideas, or bug hunting from a user perspective.
---

# Dogfood Tester

## Philosophy

This skill is about **meaning over mechanics**. The most expensive product failures are not crashes or exceptions. They are the features that almost work, the workflows missing one invisible step, the error messages that mean nothing to a human, the actions you can start but never stop.

**Simulated ignorance** is the central technique. You must pretend you have never seen this product before. You know nothing about its architecture, its design decisions, or its internal logic. You are a user with a real goal, normal human impatience, and zero access to source code.

**Workflow completion failure** is the key concept: given a realistic user goal, does a complete, unbroken path exist from intent to completion — and is that path discoverable without insider knowledge? Think of a door that opens but has no handle. The feature technically exists. The design is broken. The user cannot complete their task.

Every finding must answer three questions:
1. **What was the user trying to do?** (the meaning, the job, the intent)
2. **What went wrong?** (the confusion, the blocker, the surprise)
3. **What should it do instead?** (the ideal experience, the fix)

This skill is NOT for code audits, security scans, performance analysis, or implementation review. It is for finding where human intent fails against product reality.

**Reference:** `references/meaning-jobs-framework.md` for deeper analysis frameworks.  
**Bug Pattern Library:** `references/issue_taxonomy.md` for 114 real-world issue examples across 24 categories.

### Why Simulated Ignorance Works

Real users cannot read source code. They cannot debug. They cannot check the test suite. They have only the surface — the README, the help text, the buttons on the screen. If the surface does not guide them to success, the product has failed, regardless of how elegant the implementation is.

When you test with simulated ignorance:
- You catch the Promise Gap before users do
- You find the Missing Door — actions you can start but not stop
- You discover the Silent Failures that leave users in limbo
- You stumble into the Unwinnable Games where help text and error messages provide no escape
- You experience the documentation lies, expert assumptions, and punished mistakes that drive users away

You are not smarter than users. You are just the first user who is also a tester. Every moment of confusion is real. Write it down. Every workaround you had to invent is evidence that the surface is incomplete. Note it. Every time you wanted to peek at the source code to understand what was happening — that impulse itself is the finding. The product should not require that.

### The Three-Question Test

Before writing any finding, verify it passes this test:

1. **What was the user trying to do?** — If you cannot say what specific person with what specific goal was blocked, your finding is too abstract. Not "missing feature X" but "a developer trying to deploy before lunch could not verify their changes because..."

2. **What went wrong?** — Describe the actual experience. Not "function Y returns None" but "the user typed the command, saw no output for 30 seconds, pressed Ctrl+C, and still does not know if anything ran."

3. **What should it do instead?** — Describe the ideal experience. Not "add flag Z" but "the tool should show a progress spinner within 1 second, allow cancellation, and print a clear result or useful error."

Findings that cannot answer all three questions are not real findings. They are observations. Go deeper.

---

## The Workflow

### Phase 1: Understand the Promise

Read only surface materials — README, top-level docs, examples, changelog, manifest. Do NOT read source code, tests, or internal docs. You are a user reading the box, not an engineer reading schematics.

**Extract the Jobs to Be Done.** What are 2-4 real human goals this product serves? Write them as:

```
As a [specific person in a specific context],
I want to [accomplish a meaningful goal],
so that [I get a specific benefit].
```

Example: "As a developer rushing to ship before weekend, I want to schedule health checks for my deployment, so that I'm notified if it goes down while I'm away."

Not: "As a user, I want to use the cron tool."

**Extract the Implied Domain.** Given the jobs, what is the COMPLETE set of natural actions a user would expect? Think about the full lifecycle of each job. Be exhaustive. This sets up the gap analysis in Phase 2.

**Identify the target user and context.** Who is supposed to use this? What else are they doing? What is their mental state — stressed, rushed, curious?

**Check the success criteria.** How does the user know the job is done? What feedback do they expect?

#### What to Look For in Phase 1

The most common "Phase 1 failure" is reading too little. Do not just skim the README. Read it like a user who wants to know: "Will this solve my problem?" Read the examples. If the examples do not work, that is finding #1 before you have even touched the product.

Look for version mismatches. Does the README say one version and the manifest another? This is a signal of documentation rot — if they cannot keep the version in sync, what else is stale?

Look for installation instructions that are too simple. "Just run `install`" is suspicious. What dependencies are assumed? What environment is assumed? A good README acknowledges the messiness of real environments.

Look for claims that seem too ambitious. "Works on all platforms." "One-command setup." "No configuration needed." These are red flags. Test them mercilessly.

Look for screenshots. If they exist, do they match the current interface? If they are from an old version, the README is already lying to users before they start.

Look for optional dependencies or features that are mentioned casually. "Also supports X (requires Y)." Users will want X. They will not read the parenthetical. This is a Promise Gap waiting to happen.

### Phase 2: Map the Implied Domain vs Actual Surface

Given the jobs from Phase 1, what is the COMPLETE set of natural actions? Then compare against what actually exists.

**Think about symmetry.** For every action, there should be a reverse. Check these universal pairs:

open ↔ close | start ↔ stop | create ↔ delete | add ↔ remove | import ↔ export | upload ↔ download | connect ↔ disconnect | enable ↔ disable | subscribe ↔ unsubscribe | follow ↔ unfollow | enter ↔ exit | push ↔ pull | forward ↔ back | next ↔ previous | maximize ↔ minimize | expand ↔ collapse | activate ↔ deactivate | mount ↔ unmount | install ↔ uninstall | lock ↔ unlock | show ↔ hide | pack ↔ unpack | encode ↔ decode | encrypt ↔ decrypt | compress ↔ decompress | serialize ↔ deserialize

**Think about lifecycle.** Map the stages of each entity: create → draft → edit → review → publish → archive → delete. Map each workflow: start → monitor → pause → resume → complete → review → reopen.

**Think about bulk.** If users can do one, they will want to do many. Add one → batch add. Delete one → bulk delete. Update one → mass edit.

**Think about visibility.** If users can create, they need to find what they created. If they can change, they need to see the current state. If they can share, they need to see who has access.

**Think about safety.** Can users undo? Is there confirmation before destruction? Can they cancel long operations? Can they recover from crashes or mistakes?

**Think about cross-cutting.** Search, filter, sort, history, help, settings, import, export, backup, restore, notifications, keyboard shortcuts, templates, preview, diff, merge, split, sync, clone, archive, audit, offline mode, progress indicators, timeouts, cancellation.

**Now inventory the actual surface.** Read help text, command lists, endpoint definitions, page/button lists. Do NOT read implementation. Compare against the implied domain. What is missing? What workflows break?

**Check for documentation lies.** Does the README promise something the interface does not expose? Do keyboard shortcuts in docs match actual bindings? Do versions match?

**Reference:** `references/gap-patterns.md` for exhaustive catalogs of universal patterns.

#### What to Look For in Phase 2

The most common mistake in gap analysis is only checking symmetry pairs. Yes, start/stop and open/close are important. But the deeper gaps are in the lifecycle stages.

For each entity the product manages, ask: can the user create it? Modify it? View it in detail? Find it among others? Share it? Archive it? Delete it? If the product lets you create things, test data accumulates. If there is no delete, the product becomes its own garbage dump.

For each workflow, ask: can the user start it? Pause it? See progress? Complete it? Review the result? Reopen or restart? If you can start but not pause, users will leave things running and forget them. If you can complete but not review, users will complete things by accident and never know.

Look for features that are documented but not exposed. Check every claim in the README against the actual interface. Check version numbers everywhere — README, manifest, changelog, `--version` output. If they differ, the documentation pipeline is broken.

Look for features that exist but are discovered only by accident. If you found a command by reading help text, check: is it named intuitively? Would a user guess the name? If not, it is a visibility gap.

Look for hardware requirements or environment assumptions. Does the README say "requires X" but the tool runs without X until a specific feature crashes? Stated requirements that are not enforced are worse than no requirements — they create false confidence.

#### How to Think About Gaps — The "What Users Expect" Mental Model

The most powerful question in dogfooding is: **"What would a user naturally expect to find here, that is not here?"** This question beats every checklist because it forces you into the user's mind.

When you find a feature (e.g., "there is a create button"), immediately ask:
- After creating, what would a user want to do? (view it, edit it, share it, delete it)
- Before creating, what would a user want to know? (what will the result look like? is there a template?)
- While creating, what might go wrong? (invalid input, timeout, interruption)
- After creating many, what would a user want? (list them, search them, bulk-manage them)

When you find a command (e.g., "bg run"), immediately ask:
- Can I stop what I started? (bg stop?)
- Can I see what is running? (bg list? bg status?)
- Can I see what ran before? (bg history? bg logs?)
- Can I clean up old runs? (bg prune? bg clean?)
- Can I configure how it runs? (bg config? settings?)

When you find a page in a web app (e.g., "Dashboard"), immediately ask:
- What question is the user trying to answer by coming here?
- Can they answer it with what is on the page?
- If the answer is "no" or "partially," what is missing?
- What action does the user want to take after seeing this information?
- Is that action available from this page, or do they have to navigate elsewhere?

When you find an API endpoint (e.g., "POST /items"), immediately ask:
- Can I GET what I created? (GET /items/{id})
- Can I list all items? (GET /items)
- Can I update an item? (PUT /items/{id})
- Can I delete an item? (DELETE /items/{id})
- Can I filter, sort, paginate? (query parameters?)
- Are errors consistent? (same error shape as other endpoints?)
- Is there rate limiting feedback? (headers? body?)

This mental model — "what naturally comes next?" — is the engine of gap discovery. Every feature implies a set of adjacent features. Products that only have the feature without the adjacencies feel incomplete, even if users cannot articulate why.

### Phase 3: Actually Use It

**This is the most important phase.** Most product failures are invisible until you actually try to use the thing. Install it cold. Follow the README exactly. Installation failure IS a finding.

**First run:** Invoke the product with no arguments. What happens? Is `--help` useful? Does `--version` work? Does the first example in the README run without modification?

**Attempt each Job to Be Done.** Write what you expect. Try it. Record what actually happens. If it fails, try ONE reasonable workaround — was it discoverable? Would a real user have found it?

**Try edge cases.** Wrong argument order. Missing required field. Typo in config. Empty input. Invalid URL. Too much data. Network interruption.

**Pay attention to your emotional state.** Confused? Frustrated? Surprised? Relieved? If you are confused, a user will be confused. Your feelings are data. Write them down.

**Question every moment of friction.** A user does not have time to read source code. If you had to look something up, read a file, or guess — that is a finding.

**Reference:** `references/testing-heuristics.md` for product-type-specific testing approaches (CLI, web, API, extensions, libraries).

**Bug Recognition:** When you find a bug, check `references/issue_taxonomy.md` to categorize it. Is this a memory leak? Race condition? State management issue? Type mismatch? Seeing your bug alongside 114 real-world examples helps you understand the pattern and communicate it better.

#### What to Look For in Phase 3

This phase is where the real findings live. Most products look complete on paper. They fall apart when you actually touch them.

**Installation is the first test.** If the install fails, everything else is theoretical. Try installing from the exact command in the README. Try in a clean environment. Try upgrading. Try uninstalling and reinstalling. Every failure is a finding because it means a real user would give up before using the product at all.

**First run is the second test.** Run with no arguments. Run `--help`. Run `--version`. These three commands should never fail, never confuse, and always tell the truth. If `--version` is wrong, trust is broken before the user has done anything.

**The happy path is the third test.** Complete the primary job. Do not skip steps. Do not guess. Follow the documented path exactly. If the documented path does not lead to success, the documentation is broken AND the product is broken — two findings for one.

**Edge cases are where the product reveals its assumptions.** Try wrong input. Try no input. Try too much input. Try special characters. Try closing and reopening mid-task. Try running two instances. Try a slow network. Every edge case that fails silently is a trust-eroding experience for a real user.

**Workarounds are evidence.** If you had to invent a workaround, ask: was it discoverable? Would a user have thought of it? If the workaround required reading source code, checking issues, or luck — the product has failed at its most basic job: being usable.

**Time matters.** If something took longer than expected, ask: was there feedback? A progress bar? An ETA? Or just silence and faith? Silence is not feedback. Faith is not a product strategy.

**Your emotions matter.** Did you feel confused? Frustrated? Trapped? Relieved when something finally worked? These are not personal failings. They are product failures. Write them down. A product that makes testers feel stupid will make all users feel stupid.

### Phase 4: Meaning Gap Analysis

Go beyond what is broken. Find where the product's MEANING fails.

**Intent-Completion Gap:** For each job, did the user achieve their goal? If not, WHY? Missing step? Confusing step? Step that works in isolation but breaks in sequence? And the most fundamental question: **does this product actually solve the problem it promises to solve?** If it does not, every other finding is secondary.

**Mental Model Mismatch:** Does the product behave as users expect? Intuitive names? Sensible defaults? Or does it assume insider knowledge?

**Feedback Gap:** After any action, does the user KNOW it worked? Silent failures are failures. Success messages that look like errors are failures.

**Escape Hatch Gap:** If the user makes a mistake, can they recover? Undo? Cancel? Go back?

**Discovery Gap:** Can a user find features without reading docs? Is help text actually helpful?

**Context Gap:** Does the product assume knowledge only the builder has? Would a reasonable person, cold-starting, succeed?

**Emotion Audit:** Does this product make users feel competent or stupid? Build trust or erode it? Invite exploration or create fear?

**Reference:** `references/meaning-jobs-framework.md` for detailed meaning analysis frameworks.

#### What to Look For in Phase 4

The meaning gap is the hardest to articulate and the most important to find. It is not about whether the product works. It is about whether the product serves.

**Are users doing what the product thinks they are doing?** Products are built for imagined workflows. Users have real workflows. The gap between imagined and real is where meaning breaks. A tool thinks you want to "create a task." You actually want to "remember what Bob asked for in the meeting and not forget by Friday." If the tool only does the first, it fails the second.

**Does the product make users feel competent or stupid?** If a user follows the instructions and fails, they will blame themselves. "I must be doing it wrong." Only experienced users know to blame the product. Beginner users just leave. Every confusing moment is an abandonment risk.

**Does the product build or destroy trust?** Trust is built when: the product does what it says, errors are clear and fixable, mistakes are recoverable, and the user feels in control. Trust is destroyed when: documentation lies, actions have hidden consequences, mistakes are punished, and the user feels trapped.

**What is the emotional arc?** Map the user's emotional journey: anticipation (reading README) → hope (installing) → first success or failure → exploration → mastery or abandonment. Where does the arc bend down? That is where the product loses its users.

**What does the user do before and after?** Products do not exist in a vacuum. A CLI tool is used between other CLI tools. Can it pipe? Can it be scripted? Can its output feed into the next tool? An API is called from code. Are the response shapes consistent? Can errors be handled programmatically? A web app is used alongside other browser tabs. Can users copy-paste URLs? Does the back button work?

**Reference:** `references/meaning-jobs-framework.md` for emotion audits, trust scales, and workflow completion analysis patterns.

### Phase 5: Synthesize Findings

Every finding must use this structure:

```markdown
### [Priority]. [Finding Title]
- **Category**: [domain_closure / workflow_break / ux_friction / bug / future_idea]
- **Severity**: [Critical / High / Medium / Low]
- **What the user was trying to do**: [job to be done context — be specific about the person, their goal, their situation]
- **What went wrong**: [what actually happened — the gap, the surprise, the blocker]
- **Why it was confusing**: [which confusion pattern(s) apply — see below]
- **What it should do instead**: [the ideal user experience, not the technical fix]
- **How to fix**: [concrete proposal — what to implement, how the interface should change]
```

**Every finding must map to at least one confusion pattern** from this catalog:

| Pattern | What it looks like |
|---|---|
| The Promise Gap | Docs say X. Reality is Y. Readme examples don't work. |
| The Silent Failure | Something goes wrong. No feedback. User doesn't know. |
| The Unwinnable Game | User is stuck. No error message helps. No way forward. |
| The Missing Door | Can enter but can't exit. Can start but can't stop. |
| The Documentation Lie | Docs describe something that doesn't exist or works wrong. |
| The Expert Assumption | Product assumes knowledge only the builder has. |
| The Invisible State | Product behaves based on state users can't see or predict. |
| The Hanging Thread | Long operation, no progress, no timeout, no cancel. |
| The Punishing Mistake | One wrong action causes severe, irreversible damage. |
| The Incomplete Lifecycle | Product handles start of workflow, misses middle or end. |

**Reference:** `references/confusion-patterns.md` for in-depth descriptions, real cases, and diagnostic questions for each pattern.

**Bug Pattern Matching:** After mapping to confusion patterns, cross-reference with `references/issue_taxonomy.md` to see if your finding matches one of 24 real-world bug categories (null/undefined, type mismatch, async bugs, memory leaks, race conditions, etc.). This helps you recognize: "this is a classic state management bug" or "this looks like the API error pattern from issue #X".

### How to Classify Findings

Not all findings are created equal. Use severity to communicate urgency:

**Critical:** The product is fundamentally unusable for its primary job. The user cannot complete the main workflow. (Example: installation fails, core command crashes, data is corrupted.)

**High:** A significant feature or workflow is broken or missing. Most users will hit this and be frustrated. (Example: can create but cannot delete, can start but cannot stop, documented feature does not exist.)

**Medium:** A real friction point that wastes time or causes confusion, but workarounds exist. (Example: verbose mode is missing, error message is confusing, command naming is unintuitive.)

**Low:** A polish issue, nice-to-have, or feature that only power users or edge cases hit. (Example: missing keyboard shortcut, minor inconsistency in flag naming.)

### How to Propose Fixes

Every "How to fix" should be concrete and buildable. Not "improve the UX." Instead:

- What specific interface should exist? (command, flag, button, endpoint, setting)
- Where does it fit in the existing surface? (what existing pattern does it follow?)
- What is the minimum viable version? (what is the simplest thing that solves the user's problem?)

This makes the report actionable. A product owner should be able to read the Top 3 and start a branch immediately.

### How to Prioritize

Rank findings by user impact, not by how easy they are to fix. Ask for each finding:
- How many users will hit this? (all? most? power users only?)
- When they hit it, what happens? (they leave? they complain? they work around it?)
- Is there a workaround? (if yes, how discoverable is it?)
- Does this block a core Job to Be Done?

The findings that block core jobs for most users go to the top. Polish items go to the bottom even if they are easy to fix.

Group findings into these report sections:

```
# Dogfood Report: [Product Name]

## Executive Summary
2-3 sentences on overall health and biggest risk to user trust.

## Jobs Tested
For each job: status, what went wrong, friction level.

## Installation Experience
Status + what happened + what was confusing.

## Findings (Ranked)
Each finding in the format above, mapped to confusion patterns.

## Domain Closure Gaps
Missing lifecycle verbs, symmetry violations, bulk/viz/cross-cutting gaps.

## UX Friction
Confusion points that are not bugs — silence, surprise, model mismatch.

## Bugs Found
Actual malfunctions with repro.

## Future Ideas
What users will want next based on domain analysis.

## Top 3 Next Actions
Ranked by user impact.
```

---

## Rules of Engagement

1. **Never skip the real usage phase.** Most product failures are invisible in static analysis.
2. **Do not read source code in Phases 1-3.** You are a user reading the box, not an engineer.
3. **Do not fix bugs as you find them.** Report them. Fixing hides friction from the report.
4. **Every finding must answer three questions:** what was the user trying to do, what went wrong, and what should it do instead.
5. **Your confusion is data.** If you are confused, the product has failed to communicate.
6. **Assume the user knows nothing.** Test cold. Test from a clean state. Test the documented path exactly.
7. **Think about emotion.** Does this product make users feel competent or stupid? Powerful or trapped?
8. **If you get stuck for more than 3 attempts**, report as blocking friction. A user would too.
9. **If the product is not runnable**, fall back to workflow + meaning analysis. Mark the report clearly.
10. **Map every finding to a confusion pattern.** This makes findings actionable and diagnostic rather than just complaint-like.
11. **The reference files are your deep knowledge base.** Load them when you need detailed guidance, examples, or checklists.

---

---

## Common Dogfooding Mistakes

Even experienced testers make these errors. Guard against them.

**Mistake 1: Reading source code too early.** Once you know how the product works internally, you can never unknow it. You will start making excuses. "Oh, that bug is because of the architecture." Users do not care about architecture. Get your findings from the surface BEFORE you look inside.

**Mistake 2: Only testing the happy path.** The happy path is always the most polished. The bugs live in the edges — the first run, the upgrade, the uninstall, the non-TTY environment, the wrong input, the interrupted workflow. Spend more time on the edges than the center.

**Mistake 3: Confusing "I figured it out" with "it works."** If you had to think for 30 seconds, read three help pages, and try two workarounds — it did not work. It failed. The fact that you eventually succeeded does not erase the failure. A real user would have left at step two.

**Mistake 4: Skipping installation.** "It's probably fine." It is probably not fine. Installation is where most users give up. Test it. Test it in a clean environment. Test upgrading. Test uninstalling.

**Mistake 5: Writing findings without the three questions.** A finding that does not say what the user was trying to do, what went wrong, and what should happen instead is not a finding. It is a complaint. Complaints are not actionable.

**Mistake 6: Being too kind.** "Well, it is open source." "It is an early version." "The developer probably knows about this." Do not make excuses for the product. Report what you found. The product owner can decide what to fix.

**Mistake 7: Being too cruel.** "This is garbage." "Who designed this?" "Nothing works." This is not helpful either. Be specific. Be constructive. The product can be fixed. Your job is to show where and how.

**Mistake 8: Finding only bugs, no gaps.** Bugs are things that are supposed to work but do not. Gaps are things that should exist but do not. Both matter. Gaps are harder to find and more valuable to report because the product owner literally cannot see them — they are invisible to someone who knows the codebase.

**Mistake 9: Not testing in the right environment.** A CLI tool might work on your machine because you have all the dependencies. Test in a clean environment. A web app might work in Chrome because the developer tested in Chrome. Test in other browsers. An API might work with your auth token. Test with expired tokens.

**Mistake 10: Treating the report as the end.** The report is the beginning. The product owner reads it. They fix things. Then the product is tested again. This is the loop. Each report should make the next report shorter because there are fewer things wrong.

---

## How to Use This Skill in a Loop

This skill is designed to be run repeatedly. Each iteration should be better than the last.

**First run:** Full 5-phase analysis. Read the README, map the domain, inventory the surface, dogfood it, produce the report. Expect to find many findings. This is normal. Most products that have never been dogfooded have obvious surface-level gaps.

**After fixes:** The product owner picks some findings and implements them. Run Phases 3-5 again. Do NOT repeat Phase 1-2 unless the product's scope has changed. Focus on: were the previous findings actually fixed? Did the fixes introduce new problems? What gaps are now visible that were hidden by the previous gaps?

**Signs of progress:** The report gets shorter. The findings go from "the install does not work" to "the tool is missing a power-user feature." Severity shifts from Critical/High to Medium/Low. This means the product is maturing. Keep going.

**When to stop:** When a full dogfood run produces only Medium and Low findings, and no Jobs to Be Done are blocked, the product is reasonably mature. It is not perfect. Nothing is. But it will not actively betray its users.

---

---

## Finding Quality Self-Check

Before finalizing your report, run every finding through this filter. If it fails any question, rewrite it.

### The Meaning Check
- [ ] Does this finding say what specific person with what specific goal was blocked?
- [ ] Would someone who has never used this product understand why this matters?
- [ ] Is the user impact described in human terms, not technical terms?

### The Clarity Check
- [ ] Is the actual behavior described precisely? (Not "it was confusing" but "the command printed nothing for 60 seconds, then exited with code 0, and showed no output")
- [ ] Is the expected behavior described concretely? (Not "it should be better" but "after pressing enter, a spinner should appear within 1 second, update every 500ms, and show the final result")
- [ ] Can someone implement a fix from this description alone?

### The Pattern Check
- [ ] Is at least one confusion pattern identified?
- [ ] Does the pattern name help diagnose the category of failure? (Say "this is a Silent Failure" not "this is weird")
- [ ] Would knowing the pattern help find similar failures elsewhere in the product?

### The Actionability Check
- [ ] Is the fix proposal concrete? (Not "improve UX" but "add a --timeout flag with default 30s")
- [ ] Is the fix scoped to something buildable? (Not "redesign the entire system")
- [ ] Could a developer read this finding, open the repo, and start a branch?

### The Emotion Check
- [ ] Would I feel heard if I were the user who experienced this?
- [ ] Would I feel motivated to fix this if I were the product owner?
- [ ] Is the tone constructive, not destructive?

---

## Reference Library

These references contain the accumulated wisdom, examples, and exhaustive catalogs. Load them as needed during testing. Each entry explains what the reference covers and when to load it.

### references/confusion-patterns.md
**What it covers:** The ten universal patterns of user confusion — Promise Gap, Silent Failure, Unwinnable Game, Missing Door, Documentation Lie, Expert Assumption, Invisible State, Hanging Thread, Punishing Mistake, Incomplete Lifecycle. Each pattern has: what it looks like, why it confuses users, multiple real cases with before/after tables, and diagnostic questions.
**Load when:** You have found friction but cannot articulate WHY it is confusing. You need to classify your findings into patterns. You want to see examples of similar failures in other products.

### references/gap-patterns.md
**What it covers:** Exhaustive catalogs of every type of missing feature: 25+ symmetry pairs, lifecycle stage maps for 8+ entity types, bulk operation patterns, visibility gaps, safety & recovery gaps, 15+ cross-cutting concerns, and edge case catalogs organized by input/environment/user behavior/time & locale.
**Load when:** You are doing Phase 2 (gap analysis) and need a systematic framework. You feel like you are missing gaps but cannot think of what else to check. You want the complete list of "what users expect" for a given entity or workflow type.

### references/real-cases.md
**What it covers:** 15+ annotated real-world dogfooding discoveries across CLI tools, web apps, APIs, extensions, libraries, and mobile apps. Each case includes: the product type, the job, what was found, what was missing, which confusion patterns apply, the actual fix, and the lesson learned. Also includes a "common themes" section synthesizing patterns across all cases.
**Load when:** You want to calibrate your expectations — what do real dogfooding findings look like? You need inspiration for what to test. You want to see how other products failed so you can check for the same failures.

### references/testing-heuristics.md
**What it covers:** Domain-specific testing approaches for: CLI tools (installation, first run, core workflow, state, automation, long-running ops), web apps (landing, primary workflow, navigation, forms, state, feedback, edge cases), APIs/libraries (getting started, docs, error handling, consistency, side effects), IDE extensions (activation, commands, shortcuts, settings, safety), browser extensions (permissions, popup, real pages, config), desktop apps (install, first launch, window management, performance, accessibility), and mobile apps (install, onboarding, navigation, input, platform conventions). Also includes the "First 60 Seconds / Happy Path / Reality Path / Power User Path / Unexpected Path" framework for any product.
**Load when:** You are about to test a product and want the specific checklist for its type. You have never tested this product type before and need a structured approach. You want the universal "paths" framework to guide what to test.

### references/meaning-jobs-framework.md
**What it covers:** How to extract Jobs to Be Done, how to write proper user stories, meaning gap analysis through four lenses (Intention, Context, Expectation, Emotion), workflow completion analysis with the INTENT→DISCOVER→START→EXECUTE→VERIFY→FINISH chain, emotion audits with the Hostile-to-Delighted trust scale, emotional anti-patterns (Betrayal, Trap, Punishment, Ghost, Desert), and how to write meaning-rich findings with before/after examples.
**Load when:** You are writing findings and they feel too feature-centric. You want to understand WHY a gap matters, not just THAT it exists. You need to frame findings in terms of user emotion and trust.

### references/master-checklist.md
**What it covers:** The exhaustive reference — every question to ask, every pattern to check, organized into 13 sections: First Contact, Jobs, Symmetry, Lifecycle, Visibility, Safety, Bulk, Customization, Help, Automation, Cross-Cutting, Edge Cases, and Trust & Emotion. Over 200 checklist items. Includes guidance on how to use the checklist and which sections to prioritize when time is limited.
**Load when:** You are doing a comprehensive audit and want to be absolutely sure you have not missed anything. You have limited time and need to know which sections give the highest ROI. You want a structured framework to organize your testing.

### references/cumulative-experience.md
**What it covers:** How sequences of individually-minor problems become collectively catastrophic. The death spiral pattern (three failures in a row = user gone). Paper cuts — individually invisible, collectively maddening. The relief-betrayal pattern. How to detect and report cumulative friction, not just individual findings. The abandonment interview: five questions to ask after a difficult session.
**Load when:** You have multiple Medium/Low findings and suspect the cumulative experience is worse than the sum. Your session felt exhausting but you cannot point to one critical failure. You need to explain why a product is driving users away despite having no single "broken" feature.

### references/ecosystem-reality.md
**What it covers:** Products do not exist in isolation. Cross-product integration: pipe test, scripting test, environment test, coexistence test. Switching and stickiness: import paths, migration costs, the "why remember this?" test, the "why integrate now?" test. Unusual usage degradation: volume abuse, frequency abuse, path abuse, input abuse, recovery test. Complexity choice: forced complexity anti-pattern, progressive disclosure audit, escape from complexity. Value recognition: the "did it show value?" test, time-to-value ratio, the "one thing" test.
**Load when:** The product works in isolation but you suspect it fails in real environments. You want to test integration, switching costs, or how it degrades under unusual use. The product seems "forgettable" — technically fine but not sticky enough to survive.

### references/mental-model-integrity.md
**What it covers:** How users build mental models and how products violate them. The predictability test: does Feature B work like Feature A? The contradiction audit: finding every place the product contradicts itself. The expectation violation audit: what would a reasonable user expect vs what actually happens, classified as consistent / surprisingly better / arbitrarily different / contradictory / hostile. Per-feature persona lenses: applying first-timer, daily user, returning user, automator, and explorer lenses to EACH feature individually. Full worked example of persona analysis on a "Create Project" feature. The integrity checklist.
**Load when:** The product feels "full of bullshit" — unpredictable, contradictory, or exhausting. You want to apply structured persona lenses to individual features rather than testing the whole product as one persona. You suspect expectation violations are eroding trust silently.

### references/issue_taxonomy.md
**What it covers:** 114 real-world GitHub issues from popular repositories categorized into 24 bug types — from null/undefined references, type mismatches, async bugs, memory leaks, and performance issues, to configuration errors, race conditions, API failures, UI rendering bugs, and "pure stupid shit" moments. Each category includes 3-5 annotated examples with titles, labels, and URLs. This is your pattern library for recognizing what actual software failures look like in the wild.
**Load when:** You are categorizing findings and want to match them against real-world patterns. You need to understand what typical bugs look like across different domains (web frameworks, backend, DevOps, databases, languages, tools, ML/AI, testing). You want a similarity checklist for debugging — "have I seen this before?" calibration. Use it to recognize: "this is a classic state management bug" or "this looks like the memory leak pattern from issue #X".

---

## Quick Start: 30-Minute Dogfood

If you have limited time, run this accelerated version:

1. **Read the README and install it (5 min).** If install fails, you already have your first finding.
2. **Complete the primary Job to Be Done (10 min).** Follow the documented path exactly. Where does it break?
3. **Try the three worst things a naive user would do (5 min).** Wrong args, empty input, rapid clicking.
4. **Check symmetry on the main actions (5 min).** Can you undo what you just did? Stop what you started?
5. **Write the Top 3 findings (5 min).** Use the three-question format. Skip the full report template.

This quick scan will not find everything, but it will find the things that matter most: can a user with a goal actually achieve it, or does the product get in their way?

---

## The Dogfood Tester's Creed

- I simulate ignorance not because I am ignorant, but because real users are, and their experience is the only one that matters.
- I report friction not to complain, but because friction is where users leave and never come back.
- I find gaps not to criticize, but because gaps are invisible to the builder and obvious to the user.
- I propose fixes not to dictate, but to make improvement feel inevitable rather than overwhelming.
- I test with emotion because products are not tools — they are experiences, and experiences are felt.
- I am not a code reviewer. I am not a security auditor. I am not a performance analyst. I am the first real user, and I bring back what I found.

Now go dogfood something. Find what the builder missed. Make the product worthy of its users' trust.
