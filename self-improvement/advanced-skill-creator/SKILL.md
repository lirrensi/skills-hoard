---
name: advanced-skill-creator
description: >
  Create, distill, improve, and evaluate agent skills from source material and large corpora.
  Use this skill when the user wants to turn a repo, manual, idea dump, or source corpus into
  a field-manual-style skill, revise an existing skill folder, sharpen triggering, reduce bloat,
  or audit a skill using local references and comparison skills instead of inventing guidance.
---

# Advanced Skill Creator

Create and revise skills from source material with progressive disclosure.

This skill works inside the current skill folder. Treat the target skill as a source-backed
artifact, not a blank page.

## Core Rule

- Start from source material, not vibes.
- If the source is a large corpus, distill the transferable core into a field-manual skill.
- Prefer local files, neighboring skills, user notes, and evals before synthesizing new guidance.
- Keep edits inside this folder unless the user explicitly asks for something else.

## Modes

- `distill` - compress a large corpus, repo, manual, or idea dump into a skill-shaped manual.
- `create` - build a new skill from a scoped source packet.
- `improve` - revise an existing skill using evidence and local comparison.
- `evaluate` - test a skill revision against a compact prompt set.

## Routing

1. Identify the mode.
2. Read the matching reference:
   - `references/field-manual-principles.md`
   - `references/distill.md`
   - `references/create.md`
   - `references/improve.md`
   - `references/evaluation.md`
3. Pull only the source material needed for that mode.
4. Make the smallest change that improves triggering, routing, coverage, or reliability.

## Source Packet

A good source packet contains:

- the target skill or domain
- the source corpus, repo, manual, or idea dump when available
- raw ideas, notes, examples, or constraints
- nearby local skills for comparison
- failures, evals, or complaints
- output or tool constraints that matter

If the source is thin, gather more material before polishing the skill.

## Field-Manual Principles

- Progressive disclosure: keep `SKILL.md` lean and push detail into references.
- Corpus first, compression second: the source corpus stays canonical, the skill is downstream.
- Source-led writing: important instructions should come from a file, example, eval, or user requirement.
- One action per step: prefer short ordered procedures over dense prose.
- Rule, example, checklist: those are the default building blocks of the manual.
- Recovery paths: add if/then handling for common errors and near-miss cases.
- Retrieval first: use stable headings, small sections, and clear file names.
- Provenance: keep claims tied to the source packet when possible.

For the full doctrine and structure rules, see `references/field-manual-principles.md`.

## Comparison Set

Use nearby local skills as comparison material when improving or creating.

- Start with the target skill, if it exists.
- Inspect a few strong neighboring skills to borrow structure, not voice.
- Extract principles, not cargo-cult formatting.

Useful patterns to borrow:

- crisp descriptions that trigger at the right times
- clear routing or mode-selection steps
- lean instructions with little repetition
- good examples that clarify behavior without overconstraining it
- bundled scripts or references when repeated work should be standardized

## Improvement Rules

- Fix the root cause, not just the wording.
- Preserve the skill's identity unless the user asks to rename or repurpose it.
- Remove bloat before adding new text.
- Add references when a repeated pattern needs a stable home.
- Use scripts only when a repeated step benefits from deterministic execution.

## What To Avoid

- writing from thin air when source material exists
- duplicating long reference content in `SKILL.md`
- overfitting to one prompt or one complaint
- changing scope or name casually
- editing outside this folder unless requested

## Evaluation

Load `references/evaluation.md` when comparing versions, checking regression risk, or validating a meaningful revision.

This skill should usually produce:

- diagnosis
- mode
- edits
- rationale
- remaining risks
- suggested evals
