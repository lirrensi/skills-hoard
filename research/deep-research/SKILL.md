---
name: deep-research
description: >
  Run file-backed, resumable research inside the current workspace. Use when a task needs
  multi-source synthesis, comparison, fact-finding, trade-off analysis, current-state checking,
  or a written brief grounded in collected evidence. Avoid for simple lookups, routine debugging,
  one-source questions, or tasks that cannot be researched with the tools actually available.
---

# Deep Research

Use this skill when the user needs serious research that should survive interruption, support parallel work, and leave behind both the collected material and the final synthesis.

The point is simple:

- clarify what the hell is actually being researched before searching
- check capabilities before pretending to research
- keep working memory in files, not only in chat context
- preserve URLs, snippets, and notes used to form the answer
- support parallel collection when the harness allows it
- stay readable and lightweight

## When To Use

Use this skill when the task needs one or more of these:

- comparison across options
- multi-source synthesis
- decision support or recommendation
- current-state or latest-information checking
- fact-finding that needs verification
- competitor, market, or technology scanning
- continuation of an unfinished research thread
- a written note or brief backed by persisted evidence

Do not use this skill for:

- a single simple lookup
- summarizing one source
- routine debugging or code fixes
- finding a definition or code location
- tasks that require web research when no search capability exists

## Core Rules

- If the prompt is vague, mixed, or underspecified, do not sprint into search.
- Start with a tiny alignment pass: restate the intended question, show the plan, and let the user correct it when needed.
- Shit in, shit out: if the user wants precision, they should give at least a paragraph of what they actually want.
- Never start research before checking capabilities.
- If no search tool exists, fail clearly and stop.
- Keep research artifacts inside the current workspace.
- Keep persistence simple: plain markdown first.
- Preserve the evidence residue: URL, title when available, snippet, and why it matters.
- Prefer saving relevant extracts over discarding them. Text is cheap; lost research context is expensive.
- Full fetched page bodies may be discarded once useful extracts are preserved, but relevant source text should usually be kept in `materials.md`.
- Do not rely on chat context as the only working memory.
- Do not smooth over contradictions. Record and resolve them, or mark them disputed.

## Stage 0 - Alignment / Mini Plan

This stage happens before the capability gate when the user's request is ambiguous enough that the wrong research direction is plausible.

Goal: make sure the research target is actually understood before spending time searching.

Do this quickly:

- restate what you think the user means
- name the main possible interpretations if there are several
- show a tiny plan of what would be researched
- ask for confirmation or correction when ambiguity would materially change the search

Good reasons to trigger Stage 0:

- vague phrasing
- overloaded request
- multiple plausible meanings
- unclear target person, country, time frame, or goal
- user asked for something broad that could mean system overview or practical pathway

Move on when:

- the research target is specific enough that searching the wrong thing is unlikely
- the user confirms the direction, or the prompt is already clear enough to proceed

Stay in Stage 0 when:

- a small clarification would materially change the research path
- the user clearly means something practical but phrased it loosely

Example alignment pattern:

```text
I think you might mean one of these:
1. general overview of the education system
2. how to move there and attend college
3. how international students apply

Mini plan:
- confirm the target scenario
- check tool capability
- research the right pathway
- save both materials and summary

If you want precision, give me at least a paragraph. Shit in, shit out.
```

## Capability Gate

This is always Stage 1 after alignment.

Before planning or searching, determine whether the current harness has:

- a **search** capability
- a **fetch/read-web** capability
- a **parallel spawn** capability
- a **file write/update** capability

### Capability rules

- **Search is mandatory.** If no search tool exists, hard fail and stop.
- **File persistence is mandatory.** If findings cannot be written to workspace files, stop.
- **Fetch is strongly preferred.** If search exists but full-page fetch does not, continue only if search results and available local material are sufficient; state the limitation.
- **Parallel spawn is optional.** If it exists, use it when the work naturally splits. If it does not, continue sequentially.

Do not move on until the capability check is complete.

## Default Files

Keep the scaffold simple.

Default folder:

```text
research/<topic-slug>/
```

Default files:

```text
research/<topic-slug>/materials.md
research/<topic-slug>/summary.md
```

Optional file when useful:

```text
research/<topic-slug>/plan.md
```

### File roles

- `materials.md` = working memory, source log, snippets, stage status, unresolved conflicts
- `summary.md` = current best synthesis for the user
- `plan.md` = optional scoped plan when the task is large enough to benefit from one

Do not introduce JSON state files by default.

## Research Modes

Choose one mode early.

- `breadth` - map the space, cover major angles, compare options, discover what matters
- `balanced` - default mode; enough coverage plus enough verification
- `depth` - settle a narrow question, verify a specific claim, resolve a disputed fact, or maximize factual precision

Default to `balanced`.

### Mode cues

Prefer `breadth` when the user asks for:

- overview
- landscape
- options
- comparison
- market scan
- what matters here

Prefer `depth` when the user asks for:

- the truth
- exact answer
- verify this
- fact-check this
- settle a dispute
- confirm a number, date, or claim

If the request starts broad but contains a few critical facts, run broad collection first and add a depth pass on those facts.

## Stages

The skill has explicit stages. Do not jump stages silently.

### Stage 0 - Alignment / Mini Plan

Goal: confirm what the research should actually cover before searching.

Move on only when:

- the intended question is clear enough to search usefully
- the user has confirmed the direction when the prompt was ambiguous

Resume rule:

- if the scope already clearly reflects confirmed intent, do not redo this stage
- if the run started from a vague prompt, re-check the intended target before continuing

### Stage 1 - Capability Check

Goal: determine whether research is possible here.

Move on only when:

- search capability is confirmed
- file persistence is confirmed
- fetch and parallel availability are known

Hard fail when:

- search does not exist
- findings cannot be saved to workspace files

Resume rule:

- if capability status is already recorded and still trustworthy for the current session, reuse it
- otherwise re-check

### Stage 2 - Scope

Goal: define what is being answered and how far the run should go.

Record:

- question
- user goal
- in-scope
- out-of-scope
- mode
- likely research angles

Move on only when:

- the question is specific enough to search
- the boundary of the run is clear enough to know what belongs

Stay in scope stage when:

- the request is too broad or mixed
- several unrelated questions are bundled together
- success criteria are unclear

Resume rule:

- read the existing scope block in `materials.md`
- keep it if still valid
- revise it before searching if stale, contradictory, or newly narrowed

### Stage 3 - Scaffold

Goal: create or reuse the workspace-local file scaffold.

Move on only when:

- `materials.md` exists
- `summary.md` exists or is intentionally deferred until synthesis
- there is a clear place to append findings

Resume rule:

- reuse existing files for the same thread
- do not create fresh files unless the user asks for a reset or new branch

### Stage 4 - Search Plan

Goal: decide which search tracks to run.

For a small task, this can be very short.

Record:

- main angles or sub-questions
- which ones need search
- which ones need fetch/read in depth
- which ones can run in parallel
- what evidence would be enough to stop

Move on only when:

- the search tracks are distinct enough to avoid duplicate work
- the stop condition is roughly known

Resume rule:

- inspect what angles are already covered in `materials.md`
- plan only missing, weak, or disputed areas

### Stage 5 - Evidence Collection

Goal: search, fetch, read, and preserve useful evidence.

For each meaningful source, preserve in `materials.md`:

- URL
- title or source label when available
- date if relevant
- one or more useful snippets or short extracts
- a brief note on why the source matters
- angle or claim it supports

Prefer generous capture over skinny notes. If relevant source text helps future follow-up, save it.

`materials.md` should usually end up as a real dossier, not a tiny receipt list.

Move on when the current mode has enough evidence.

In `breadth`, move on when:

- the main angles are covered
- new searches mostly duplicate known material
- enough evidence exists to map the space honestly

In `depth`, move on when:

- the narrow claim has strong support
- contradictory evidence has been directly checked
- source quality is strong enough for the stakes

Resume rule:

- read `materials.md`
- identify covered angles, weak coverage, and missing angles
- continue collecting only where needed

### Stage 6 - Verification

Goal: test whether the collected material is good enough to support the answer.

Check for:

- major claims with weak support
- single-source dependency
- outdated information
- copied claims across low-independence sources
- contradictions
- missing primary sources where they matter

Move on only when:

- major claims are supported enough for the task
- weak points are labeled
- contradictions are resolved or explicitly preserved

Resume rule:

- verify the claims that will actually appear in `summary.md`
- do not restart the whole audit unless the topic is sensitive or stale

### Stage 7 - Synthesis

Goal: write the best current answer in `summary.md` using the persisted material.

The summary should:

- answer the original question directly
- separate fact from interpretation
- state trade-offs and uncertainty clearly
- preserve conflict when evidence is mixed
- avoid claims that cannot be traced back to `materials.md`

Move on only when:

- the summary answers the actual question
- major claims are traceable to preserved evidence
- uncertainties and caveats are visible

Resume rule:

- read both `materials.md` and `summary.md`
- continue the first incomplete or weak section
- downgrade any conclusion that outruns the evidence

### Stage 8 - Finalize

Goal: leave behind a clean, resumable handoff.

Done when:

- the current stage is recorded
- `materials.md` contains enough evidence residue to resume later
- `summary.md` reflects the current state honestly
- nothing important exists only in chat context

Resume rule:

- start from the first incomplete stage
- do not redo completed work unless stale, contradictory, or explicitly reset

## Resume Model

At the top of `materials.md`, keep a tiny status block like this:

```markdown
# Research Materials: <topic>

## Status
- current_stage: evidence_collection
- overall_state: in_progress
- mode: balanced
- question: <question>
- last_updated: <date>

## Stage Checklist
- [x] capability_check
- [x] scope
- [x] scaffold
- [ ] search_plan
- [ ] evidence_collection
- [ ] verification
- [ ] synthesis
- [ ] finalize
```

This status block is the default resume anchor.

## Search Guidance

Research should start broad enough to orient, then narrow enough to answer.

Before search, if the prompt is vague, run Stage 0 and align first.

### Good query habits

- include the actual topic, not vague shorthand
- include the current year when recency matters
- include the exact entity, product, date, claim, or metric when known
- search from multiple angles, not one phrasing repeated forever
- prefer terms that surface primary sources, official docs, research, filings, reports, standards, or direct evidence

### Bad query habits

- one vague query and then immediate synthesis
- only searching confirmatory phrasing
- using broad hype words without the actual subject
- never varying wording when results are weak
- treating search snippets as if they were evidence

### Typical progression

1. orientation query
2. angle-specific queries
3. verification queries
4. contradiction or adversarial queries when needed

## Breadth vs Depth Rules

### Breadth

Use when the question is wide and the main job is coverage.

Bias toward:

- more distinct search angles
- more source diversity
- thinner reading per source
- parallel collection when available

Stop when:

- you can map the major terrain without obvious blind spots
- new material is mostly repetitive

### Depth

Use when the question is narrow and the main job is truth-finding.

Bias toward:

- fewer but better sources
- fuller reading
- stronger verification
- more direct conflict checking

Stop when:

- the key claim is supported strongly enough
- contradictions have been investigated directly
- remaining uncertainty is clearly bounded

## Contradictions And Opposing Data

Never average contradictions away.

When sources disagree, classify the conflict.

Common causes:

- **time drift** - one source is older than another
- **scope mismatch** - they measure different things
- **definition mismatch** - same term, different meaning
- **source-quality mismatch** - stronger source versus weaker source
- **genuine unresolved dispute** - the evidence really conflicts

For each important contradiction, record:

- claim A
- claim B
- source and date for each
- likely cause of disagreement
- current resolution status

### Resolution order

Prefer, in general:

1. primary or official source
2. more recent source
3. more specific methodology or scope match
4. broader agreement across independent sources

If nothing clearly wins, mark the point as **disputed** and make the final answer conditional where necessary.

## Parallel Mode

Parallel work is optional, not mandatory.

Use it when:

- the question splits into distinct sub-questions
- comparison candidates can be researched separately
- one worker can gather while another checks recency or contradictions
- the merge path is clear

Do not use parallelism when:

- the problem is tiny
- workers would duplicate each other
- the question is so narrow that splitting hurts quality

### Recommended roles when parallel is available

- **researcher** - gathers evidence for one sub-question or angle
- **critic** - tries to disprove the obvious answer or surface contradictions
- **fact-checker** - verifies key numbers, dates, names, and exact claims

Use the critic and fact-checker especially when the topic is current, contested, comparative, or precision-sensitive.

### Parallel writing rule

Sub-workers should contribute to the same research thread by appending source residue to the shared `materials.md` structure, or by writing clearly mergeable subsections that the lead consolidates into `materials.md`.

The final summary should still be synthesized centrally.

## Quality Controls

Before considering the research good enough, check:

- Did Stage 0 confirm the actual target, or was the request already clear enough?
- Does the summary answer the actual question?
- Are major claims backed by preserved evidence?
- Are current or time-sensitive claims dated?
- Are weak points labeled?
- Were contradictory sources investigated instead of ignored?
- Does the stopping point match the mode: breadth or depth?
- Could another agent resume from the files without guessing?
- Is `materials.md` rich enough to support follow-up conversation, not just one summary?

## Writing Rules

- Write clearly and densely.
- Prefer exact language over inflated language.
- Separate sourced fact from interpretation.
- Use bullets for source logs and lists, not for all analysis.
- Keep the final answer useful for decisions.
- Match the user's language.

## Delivery Contract

When finished or paused, provide:

1. a short executive brief in chat
2. the path to `materials.md`
3. the path to `summary.md`
4. whether the thread is complete, in progress, or blocked
5. the biggest gaps, assumptions, or unresolved contradictions

## Minimal Materials Shape

Use plain markdown. Keep it simple.

```markdown
# Research Materials: <topic>

## Status
- current_stage: <stage>
- overall_state: <in_progress|complete|blocked>
- mode: <breadth|balanced|depth>
- question: <question>
- last_updated: <date>

## Scope
- Interpreted request:
- Confirmed intent:
- Goal:
- In scope:
- Out of scope:

## Search Plan
- Angle 1:
- Angle 2:

## Findings By Angle
### Angle 1
- finding:
- supporting text:
- source:

## Collected Evidence
### Source
- URL:
- Title:
- Date:
- Why it matters:
- Snippet:

## Follow-Up Hooks
- likely user question:
- current best answer:
- source pointers:

## Contradictions
- Claim A:
- Claim B:
- Notes:
- Status: resolved / disputed / needs more checking

## Open Questions
- ...
```

## Minimal Summary Shape

```markdown
# Research Summary: <topic>

## Executive Summary

## Key Findings

## Trade-offs / Risks

## Contradictions or Uncertainties

## Recommendation / Best Current Answer
```

Keep the system strong. Keep the files simple. Keep the truth trace.
