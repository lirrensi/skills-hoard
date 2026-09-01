---
name: thinking-graph
description: Use for hard, ambiguous problems that need deeper graph-style reasoning instead of a fast first answer. Trigger on architecture choices, deep debugging, strategy design, research synthesis, root-cause work, or any task where multiple live hypotheses, reflective pruning, and deliberate convergence will improve the result. Prefer this skill when the user asks for deeper thinking, graph thinking, notebook-style exploration, or persistent reasoning files in the workspace.
---

# Thinking Graph

This skill turns notebook-style deep reasoning into a resumable workspace workflow.

The core idea is simple:

- broaden before committing
- deepen selectively
- reflect and prune aggressively
- converge deliberately
- persist the work so interruption does not destroy the useful intermediate structure

This skill is anti-premature convergence, not anti-convergence.
Persist structure, not raw mental exhaust.

If you need the long draft or paper-derived rationale, read `UTG.md`. For most tasks, use this file directly.

## When To Use

Use this skill when:

- the first obvious answer is likely to be wrong or shallow
- several materially different explanations or designs could fit
- the user wants a careful decision, not just a quick guess
- the task benefits from explicit branch tracking
- the work may be interrupted and later resumed
- you need to preserve dead ends, partial progress, and convergence blockers

Do not use this skill for trivial edits, obvious one-step fixes, simple lookups, rote transforms, urgent live troubleshooting, or tasks where notebook overhead would slow more useful progress.

## Core Stance

- Keep 3 to 5 live branches, not 20.
- Branches must differ in mechanism, framing, or constraint-handling; avoid cosmetic variants.
- Write structured working notes, not a stream-of-consciousness dump.
- Preserve failed paths so they are not rediscovered.
- Promote validated fragments into a stable backbone.
- Treat non-convergence as a valid state that must be recorded honestly.
- If no branch meaningfully differs from the current leader, do not add a new branch.
- Distinguish observed facts, inferred claims, and open assumptions.

## Branch Differentiation Rule

Each branch must differ in at least one meaningful way:

- mechanism
- abstraction level
- constraint strategy
- system boundary

Do not create near-duplicate branches just because wording changes.

## Branch Identity Discipline

- Branch IDs stay stable once created.
- Branch labels are working handles, not sacred names.
- If a label is obviously wrong and you catch it quickly, make one short correction and record it in the next cycle entry.
- Do not keep rewriting old history just to polish branch names.
- If a branch changes materially, record the mutation in the current cycle instead of repeatedly renaming earlier entries.

## Test Discipline

- Prefer discriminating tests that can eliminate multiple branches at once.
- Avoid tests that only decorate the current leader without challenging alternatives.
- If a cheap test can collapse the graph responsibly, run it early.
- If no discriminating test exists yet, record the smallest missing observation or evidence needed.

## Capability Check

Before using the full workflow, check what is available.

- If workspace-local file writing is available, create or resume a notebook.
- If file writing is not available, keep the same structure inline in the response.
- If a same-topic notebook already exists, resume it instead of starting over.
- Never write this notebook to home directories, shared temp locations, or global config paths.

Default location:

```text
thinking/<topic-slug>/journal.md
thinking/<topic-slug>/state.json
thinking/<topic-slug>/final.md   # only if a separate polished artifact helps
```

`journal.md` is cumulative and append-oriented.
`state.json` is the compact live snapshot.

## Persistence Model

Assume hidden reasoning may be lost between turns, tool calls, or interruptions.
Persist the minimum useful reasoning structure externally.

### What to persist

Persist:

- problem framing
- constraints and unknowns
- branch list with IDs
- branch weights and why they changed
- contradictions and failed tests
- frontier items that look promising but are not stable enough for backbone promotion
- promoted backbone claims
- explicit non-convergence status
- next discriminating action

Do not try to persist every micro-thought. Persist the structure that lets a later pass resume honestly.

### Journal rules

`journal.md` should be cumulative. Append a short entry after each meaningful reasoning burst, not after every sentence.

Each entry should capture:

- cycle number and phase
- active branches touched
- important findings or contradictions
- branches killed, merged, or promoted
- branch mutations or quick relabels if any
- current convergence status
- next action

Do not silently erase earlier failed paths. Move them to a graveyard section or mark them as discarded with a reason.

### State rules

`state.json` should reflect the current graph, not the whole history.

Treat branch weights as comparative fit scores, not fake probability math. A weight is just a compact signal of how well a branch currently matches the constraints, evidence, and reflection checks.

Use only three weight states:

- `low`
- `medium`
- `high`

Do not use arbitrary decimals or fake numerical precision for fluid reasoning.

Reweight only when something changed.
Always record the reason for the reweight.

## Operating Loop

Run this loop until you either converge or can state clearly why convergence would be dishonest.

### 1. Anchor the problem

Write down:

- exact question
- why it matters
- success criteria
- known facts
- unknowns
- constraints
- likely failure modes

If the notebook already exists, first note what still looks solid, what looks stale, and what remains unresolved.

### 2. Seed the graph

Create 3 to 5 candidate branches.

For each branch, capture:

- `id`
- short label
- hypothesis or approach
- why it might work
- what would falsify it
- initial weight
- next useful test

Do not create decorative branches. Each branch must earn its place.
If the new candidate does not materially differ from an existing branch, mutate or refine the existing branch instead of adding a near-duplicate.

### 3. Explore lightly

Probe each branch just enough to reveal:

- its unique leverage
- its main dependency
- its main risk
- whether it deserves deeper work

Add new branches only if they are materially distinct from the current set.
Prefer the next test that would most sharply separate the branches.

### 4. Deepen selectively

Choose the strongest 1 or 2 branches and extend them.

Make the reasoning backbone explicit:

- dependencies
- causal links
- hidden assumptions
- edge conditions
- possible breakpoints

This is where depth happens. Do not deepen every branch equally.

### 5. Reflect and prune

After each deepening burst, stop and check:

- Which branch violates constraints?
- Which assumption is weakest?
- What contradiction appeared?
- Where did reasoning drift?
- Which branch is now redundant?
- What no longer deserves attention?

Then:

- lower or raise weights
- kill weak branches
- merge compatible branches only if the assumptions truly align
- record why each change happened

If all branches repeatedly fail reflection, perform a graph reset:

- restate the problem from first principles
- identify what framing assumption misled the graph
- seed a fresh branch set
- preserve the failed set in the graveyard instead of deleting it

### 6. Maintain a frontier

Use the frontier for partially validated structures that are promising but not yet stable enough for backbone promotion.

The frontier exists to prevent premature promotion.
Move ideas from branch to frontier when they survived some scrutiny but still need discriminating evidence or reflection.

### 7. Promote a backbone

When part of a branch survives reflection, promote that fragment into the backbone.

The backbone is the stable structure that the final answer will stand on.
It may be partial before the whole task is solved.

Mark each backbone item as one of:

- `observed`
- `inferred`
- `assumed`

### 8. Converge or lock non-convergence

Converge when all are mostly true:

- alternatives were genuinely explored
- at least one reflective pass happened
- contradictions were addressed or isolated
- surviving branches are no longer producing major new insight
- one structure fits the constraints better than the others

If those conditions are not met, do not fake closure.
Instead, create a non-convergence lock entry.

That entry must say:

- why convergence is premature
- what is still blocking decision quality
- which branch is currently strongest
- what evidence or action would unlock convergence
- what to do next

## Stall Detector

If two full cycles produce no meaningful branch change, no new discriminating test, and no backbone promotion, stop expanding.

Then do one of these:

- summarize the current best frontier
- request missing evidence
- run a graph reset if the frame itself looks broken

Do not let the notebook turn into beautifully organized stagnation.

## Skill Failure Modes

Watch for these failure modes while using this skill:

- branch proliferation
- decorative branching
- journal sprawl
- reflection theater
- convergence avoidance
- notebook tax

If any of these appear, reduce branch count, tighten the next test, and return to the strongest discriminating question.

## Notebook Template

Use this structure for `journal.md`.

```md
# Thinking Graph Notebook

## Problem Frame
- Question:
- Why it matters:
- Success criteria:
- Constraints:
- Unknowns:
- Failure modes:

## Branch Register
- B1 | <label> | weight: high | status: active
  - hypothesis:
  - why it might work:
  - falsifier:
  - next test:
- B2 | <label> | weight: medium | status: active

## Frontier
- none yet

## Backbone
- none yet

## Graveyard
- none yet

## Cycle 1 - Explore
- touched: B1, B2, B3
- findings:
- contradictions:
- weight changes:
- frontier changes:
- promotions:
- discarded:
- convergence status:
- next action:
```

Append more `## Cycle N - <phase>` sections over time.

## State Snapshot Template

Use this structure for `state.json`.

```json
{
  "question": "",
  "topic_slug": "",
  "status": "scoping",
  "cycle": 0,
  "active_branches": [
    {
      "id": "B1",
      "label": "",
      "status": "active",
      "weight": "high",
      "weight_reason": "",
      "hypothesis": "",
      "falsifier": "",
      "next_test": ""
    }
  ],
  "graveyard": [
    {
      "id": "B3",
      "reason": "",
      "discarded_in_cycle": 2
    }
  ],
  "frontier": [
    {
      "claim": "",
      "source_branches": ["B1"],
      "why_not_backbone_yet": ""
    }
  ],
  "backbone": [
    {
      "claim": "",
      "source_branches": ["B1"],
      "basis": "inferred",
      "confidence": "medium"
    }
  ],
  "non_convergence": {
    "blocked": false,
    "reason": "",
    "unlocks": []
  },
  "next_action": ""
}
```

You may add fields, but keep the snapshot compact and easy to update.

## Output Shape

When replying to the user after using the notebook, return a concise result built from the graph:

1. problem frame
2. active or leading branches
3. current frontier
4. promoted backbone
5. discarded branches and why they failed
6. final decision or current best frontier
7. remaining uncertainties
8. next action

If the graph is not ready to collapse, say so plainly and use the non-convergence lock instead of pretending to have a final answer.

## Behavioral Heuristics

- Broaden, deepen, fold back, then decide.
- Do not converge early.
- Do not refuse convergence forever.
- Stop branching when new branches are mostly decorative.
- Reflection is mandatory after meaningful branching.
- Compression happens late; pruning happens continuously.
- Balance breadth and depth instead of maximizing either one.
- Prefer the test that teaches the graph the most.

## Minimal Resume Protocol

When resuming a prior notebook:

1. read `state.json`
2. scan the last relevant cycles in `journal.md`
3. restate the current strongest branch, main blocker, and next test
4. continue from there instead of recomputing the whole graph

The notebook exists so partial discovery survives interruption.
Use it as external working memory until the graph has genuinely converged.
