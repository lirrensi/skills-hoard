# Shared Rules

These rules apply in both create mode and apply mode.

## Authority

- `micropatch.md` is authoritative.
- `hints.diff` is optional, advisory, and may be stale.
- Never treat `hints.diff` as a patch to apply mechanically.

## Anchors

Anchors describe where a change belongs without relying on brittle file offsets.

Good anchors usually include:

- the file or subsystem
- what that file or subsystem does
- the likely integration point inside it

Example anchor:

- `src/server/auth.ts` handles request authentication; add token extraction after header parsing and before permission checks.

Bad anchor:

- `somewhere near the auth code around line 80`

Good anchor:

- `src/server/auth.ts` validates inbound auth headers; add token normalization after header parsing and before permission checks.`

## What Good Looks Like

- one coherent customization per patch
- clear intent and scope
- enough implementation detail to reproduce the feature
- explicit dependencies and assumptions
- a Definition of Done that can actually be checked
- a patch that is safe to re-apply semantically, even if it cannot auto-apply mechanically
- idempotent application whenever reasonably possible; applying twice should not create duplicate behavior

## Patch Quality Checklist

Before treating a MicroPatch as complete, check that it has:

- a clear statement of what feature is being preserved
- intent that explains why the feature exists
- scope boundaries and non-goals
- dependencies and assumptions called out explicitly
- anchors that point to the right subsystem and integration point
- a Definition of Done that reads like a behavior spec, not a vague wish
- notes about likely upstream overlap or fragile areas

## Definition of Done

Definition of Done is the behavioral contract for the feature. It should describe what
must be true after application, what should be true when relevant, and what must not
happen.

Prefer RFC-style language when it helps remove ambiguity:

- **must** for required behavior or invariants
- **should** for expected behavior with some implementation flexibility
- **must not** for forbidden outcomes or regressions

Good DoD usually focuses on externally visible guarantees:

- request and response behavior
- command behavior and output
- data shape or schema guarantees
- access-control boundaries
- compatibility expectations

Weak DoD:

- `auth works`
- `the command is fine`

Stronger DoD:

- `Requests to protected /api routes without a bearer token must return 401.`
- `Requests with a valid token must reach the handler and must expose req.user.id.`
- `The /health endpoint must remain publicly accessible without authentication.`
- `The command should preserve the existing JSON schema even if the internal implementation changes.`

## Escalate to the user when

- intent is unclear and multiple valid implementations exist
- preserving behavior now requires product or architecture decisions
- schema, migration, or destructive state changes are involved
- auth, permissions, billing, encryption, deletion, or other security-sensitive behavior is ambiguous
- the feature has no plausible home in the new upstream
- the patch appears to target the wrong repository

When escalating, explain:

- what you believe the feature is trying to preserve
- what blocker prevents safe completion
- what specific decision or information you need

## Output Expectations

Always be explicit about:

- what feature the patch represents
- what changed
- what assumptions were relied on
- how the result was verified
- what remains uncertain, if anything

## Versioning

Use a consistent `version: N` format.

Increment the version when the MicroPatch is materially updated to reflect a new upstream
integration or a refined understanding of the customization.
