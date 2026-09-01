---
name: micropatch
description: >
  Use this skill when the user wants to capture, document, re-apply, or maintain
  customizations made to a forked upstream project as semantic MicroPatches.
  Trigger when the user wants to extract intentional fork changes, carry a feature
  forward onto a newer upstream release, sync a long-lived fork without relying on
  brittle merges, or document how a fork-specific feature should survive upstream
  updates.
---

# MicroPatch Skill

A MicroPatch is a versioned, semantic specification of a fork-specific customization.
It exists to ensure that a feature from a fork can still exist and work correctly on
newer upstream versions, even when raw diffs, rebases, or merge-based workflows stop
being reliable.

A MicroPatch is not a raw patch file and is not meant to be applied mechanically. It
captures the feature's intent, expected behavior, implementation reference, and
verification criteria so an agent can adapt the implementation to the current upstream
while preserving what the feature is supposed to do. It is also not guaranteed to
auto-apply cleanly: substantial upstream changes may require modifying existing code
where the feature belongs now rather than stuffing old code back into the tree.

In practice: implement semantically. Re-implement by vibe if needed, but prove the
result with the Definition of Done.

## Core Principles

- **Semantic over textual:** Preserve the feature's behavior and intent, not exact line edits.
- **One coherent customization per patch:** Split unrelated fork changes into separate MicroPatches.
- **Definition of Done decides success:** The feature is only preserved if it still works as specified.
- **Adapt to upstream reality:** If upstream changed shape, place the feature where it belongs now.
- **Upstream overlap matters:** If upstream now implements part of the feature, do not duplicate it.
- **Specification over history:** A good MicroPatch stands on its own without requiring commit history.

## Folder Structure

Each MicroPatch lives in its own folder:

```text
micropatch-your-feature-name/
├── micropatch.md
├── hints.diff          # optional, advisory only
└── files/              # optional, for large new files or implementation artifacts
```

Repositories with multiple customizations should have multiple MicroPatch folders.
Archive or remove a folder when the customization is no longer needed.

The skill may also include `examples/` for reference material that demonstrates good
MicroPatch structure and application patterns.

## MicroPatch Format

Each `micropatch.md` should include at least these sections:

```markdown
# MicroPatch: [Feature Name]
version: 1

# Optional metadata
last_applied_upstream: <tag-or-commit>
risk: low | medium | high
context: short note if useful

## What It Is
One sentence describing the customization.

## Intent
Why this exists, what problem it solves, why it remains outside upstream, and what
tradeoffs or invariants matter when re-applying it.

## Scope and Non-Goals
What this patch covers, and what it intentionally does not change.

## What It Does
Behavioral description from the outside: API behavior, UI behavior, CLI behavior,
pseudocode, examples, or request/response flows.

## Dependencies and Assumptions
Required packages, env vars, configuration, schema expectations, middleware order,
feature flags, upstream APIs, or build assumptions.

## Implementation Reference
Include the full contents of newly added files and the full final form of any
modified functions, classes, routes, config blocks, templates, or other units
needed to reproduce the customization. Large artifacts may live in `files/`.

## Anchors
Anchors are approximate integration guides, not brittle coordinates. Describe the file
or subsystem, what that file does, and where the change likely belongs within it.
Prefer searchable landmarks and architectural context over line references.

## Definition of Done
How to verify the feature now exists and works correctly on the current upstream.
Prefer checks the agent can run directly when possible.

## Notes for Future Re-application
Likely overlap with future upstream changes, fragile areas, migration concerns, or
known caveats.
```

Optional metadata is for extra context only. It can help future application, but the
semantic spec remains the important part.

If `hints.diff` exists, it is optional and advisory only. Never apply it mechanically.
If `hints.diff` and `micropatch.md` disagree, follow `micropatch.md`.

## Operating Modes

This skill has two modes:

- **Create mode:** Distill fork-specific changes into one or more MicroPatches.
- **Apply mode:** Re-apply a MicroPatch onto a newer or fresh upstream codebase.

Read the relevant workflow reference before doing mode-specific work:

- `references/create.md` for creating MicroPatches from an existing fork
- `references/apply.md` for applying a MicroPatch to a newer upstream
- `references/rules.md` for shared rules, escalation boundaries, and output contracts
- `examples/` for concrete examples and reference material

## Mode Selection

Use **create mode** when the user has an existing fork and wants to capture, document,
or cleanly separate its customizations for future reuse.

Use **apply mode** when the user wants a previously documented customization to keep
working on a new upstream version.

If the user asks for both, create or refine the MicroPatch first, then apply it.

## How to Think About Apply

When applying a MicroPatch, think like a maintainer preserving a feature contract, not
like a tool replaying an old change.

- preserve the behavior the user cared about, even if the implementation shape changes
- prefer integrating with the current upstream design over restoring obsolete structure
- modify existing code where the feature belongs now instead of stuffing old code back in
- if upstream already moved toward the feature, preserve only the missing guarantees
- let `Definition of Done` resolve ambiguity: if the behavior matches the spec, the patch succeeded

## Quality Bar

A good MicroPatch makes future application easier, not harder. It should be clear what
feature is being preserved, what counts as success, what assumptions it relies on, and
how to tell when upstream already covers some or all of it.
