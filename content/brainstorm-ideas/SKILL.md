---
name: brainstorm-ideas
description: Use when the user needs more and better options before evaluating, deciding, or planning. Trigger on brainstorming, ideation, "give me ideas", "what are other approaches", creative block, early product or architecture exploration, research directions, naming work, or when the current option set is narrow, repetitive, or trapped by assumptions. Prefer this skill when breadth matters, but do not stop at random lists - generate range, cluster the space, and land on promising candidates or next experiments.
---

# Brainstorm Ideas

This skill is an ideation router, not a bag of random prompts.

Use it to widen the option set, choose a method that fits the problem, protect against fixation, and turn raw ideas into clusters, candidates, and next moves.

If you want the deeper scientific rationale behind these defaults, read `ideas/report.md`.

## Interaction Contract

- Start as a gentle thinking partner, not a methodology lecturer.
- Route internally before speaking externally.
- Do not announce mode names, framework labels, or technique jargon unless it helps the user.
- If you do name a method, explain in plain language how it works and why it fits this case.
- Begin from the user's current thoughts, even if they arrive as fragments, half-ideas, or stream-of-consciousness notes.
- For ordinary requests, help first: reflect the brief, generate options, and lightly organize them before introducing more structure.
- Bring in heavier structure only when the space is stuck, repetitive, political, large, or ready to narrow.

## Quick Access

| Need | Reference |
|---|---|
| Pick the right brainstorming mode fast | `references/00-mode-selection.md` |
| Frame the problem before generating ideas | `references/01-framing-and-prompting.md` |
| Run strong ideation techniques and prompt passes | `references/02-technique-cards.md` |
| Cluster, narrow, and turn ideas into action | `references/03-clustering-and-convergence.md` |
| Keep a cumulative idea log through the session | `references/04-session-ledger.md` |
| Produce a durable working artifact | `templates/brainstorm-record.md` |

## Use This Skill For

- generating options when the user has too few or none
- escaping obvious, repetitive, or locally optimal ideas
- exploring product, feature, strategy, research, process, naming, or architecture directions
- balancing practical options with unconventional ones
- turning a fuzzy brief into a usable set of candidate paths
- preparing a better input set for `decision-framework`

## Do Not Use This As The Main Tool When

- the user already has a good option set and now needs commitment more than ideation
- the real blocker is missing facts, not missing ideas
- there is only one viable path and the work is execution
- the task is an urgent live response where structured exploration would only slow action

## Operating Principles

- Frame before flood.
- Keep internal complexity and external simplicity separate.
- Default to hybrid pipelines: generate individually or in parallel first, then share, cluster, and rank.
- Seek orthogonal options, not cosmetic variants of the same idea.
- Push across mechanisms, scales, time horizons, and stakeholder lenses.
- Include the baseline, the opposite, and at least one wild option.
- Separate divergence from convergence; do not let scoring kill idea volume too early.
- Switch method or take an incubation break when output becomes repetitive.
- Treat the session as cumulative work, not disposable chat.
- Preserve discarded ideas and why they were dropped so the same dead end is not rediscovered later.
- Mark whether an idea is new, a variation, a combination, a contradiction, or a reject.
- End with candidates, tests, or a handoff, not just a pile of ideas.

## Simple Entry

For a normal user request like `help me think of ideas for X`, do not start by explaining the system.

Default opening shape:

1. restate the problem in plain language
2. generate a compact first spread of ideas
3. group them lightly into a few buckets
4. note what looks promising, unusual, or underexplored
5. only then introduce more structure if it would improve the session

If the user is already thinking out loud, treat their message as raw material to shape, not as something to replace with a fresh framework dump.

## Default Workflow

### 1. Frame the search space

Read `references/01-framing-and-prompting.md`.

If the user already gave a stream of thoughts, first convert that into a clean working frame and an initial idea log.

Before generating, name:

- the real problem or opportunity
- the output needed: raw options, clusters, shortlist, or ranked picks
- who the ideas are for
- real versus assumed constraints
- what has already been tried or ruled out
- what would make an idea good enough to pursue

### 2. Choose the mode

Read `references/00-mode-selection.md`.

Default to `hybrid-default` unless a more specific mode clearly fits better.

Choose internally. In most cases, do not expose the mode name unless the user asked for the process or the method choice materially affects the collaboration.

Common modes:

- `quick-spread`
- `hybrid-default`
- `brainwriting`
- `ngt`
- `delphi-lite`
- `morphology`
- `triz-light`
- `ai-co-ideation`
- `incubation-reset`

### 3. Diverge in passes

Read `references/02-technique-cards.md`.

Start from the user's own material when available:

- extract seed ideas already present
- add adjacent variants
- add orthogonal alternatives
- add one or two genuinely different or wild moves
- mark weak or wrong ideas without deleting them from the record

Good default sequence:

1. practical and obvious ideas
2. alternative mechanisms or business models
3. inversions, opposites, and extreme constraints
4. analogies, imports, and cross-domain transfers
5. combinations, mutations, and sharper variants

Aim for roughly:

- 15-25 ideas for small or low-stakes topics
- 25-40 ideas for most meaningful explorations
- 40-60 ideas for high-stakes or complex spaces

### 4. Cluster the field

Read `references/03-clustering-and-convergence.md`.

If the session is more conversational than formal, cluster softly using plain labels like:

- similar to current direction
- sharper variant
- materially different path
- wildcard worth keeping
- probably wrong or currently weak

Group ideas into 4-8 themes. Name the mechanism, not the vibe.

Note:

- which clusters look strongest
- which parts of the space are underexplored
- whether the set is too incremental, too wild, or too redundant

### 5. Converge to candidates

If the user wants range only, stop after clustering and highlight the best directions.

If the user needs candidates, apply a light ranking or structured scoring pass.

If the user needs commitment under uncertainty, hand off to `decision-framework` once the option set is strong enough.

### 6. Land the work

Unless the user asks for another format, return:

1. the frame and, only if useful, the chosen mode
2. the major idea clusters
3. the strongest candidates or directions
4. the main trade-offs or unknowns
5. the next experiment, research step, or decision move

## Session Ledger

Read `references/04-session-ledger.md`.

For anything beyond a very short one-off brainstorm, maintain a running idea ledger.

The ledger should preserve:

- stable idea IDs
- the raw thought in plain language
- whether it is a seed, variant, combination, orthogonal move, wildcard, or reject
- which cluster it belongs to
- whether it is active, parked, selected, or discarded
- why discarded ideas were dropped

Use this ledger to periodically tell the user:

- what has already been explored
- what keeps recurring
- what is genuinely new
- what was discarded and should stay discarded unless new evidence appears

## Routing Rules

- If the user has zero traction, start with `quick-spread` plus reframing prompts.
- If the user is thinking out loud, first mirror and structure their raw material before adding new ideas.
- If ideas feel repetitive, switch to analogy, inversion, morphology, or contradiction prompts.
- If hierarchy, politics, or anxiety may suppress ideas, use nominal, parallel, or anonymous methods.
- If a ranked short list is needed quickly, use `ngt`-style convergence.
- If expert judgment must converge across time or geography, use `delphi-lite`.
- If the problem is a technical contradiction, use `triz-light` instead of generic creativity prompts.
- If AI is helping, use it to diversify, cluster, critique, and reframe - not as an unchallenged source of final answers.
- If naming any method in the user-facing response, explain it briefly and tie it to the current blockage or need.

## Guardrails

- Do not confuse energy with coverage.
- Do not dump technique names when a plain-language response would do.
- Do not stop at the first clever idea.
- Do not over-index on novelty when the user needs feasibility.
- Do not stay so practical that you never escape the local optimum.
- Do not let evaluation leak into early divergence.
- Do not lose the thread of the session; accumulate and revisit.
- Do not stop at list-making; cluster and land.

## Companion Skills

- `thinking-partner` for clarifying the brief before ideation
- `thinking-graph` for deep branch exploration after promising directions appear
- `thinking-opponent` for pre-mortems and assumption attacks
- `decision-framework` when it is time to choose and commit
