# Stories — The Project's Stupid Memory

Not everything you learn while building a system belongs in a spec or an ADR. Some knowledge is *empirical*: the weird bug that took four hours, the migration that only worked because of one counter-intuitive step, the library that *looks* right but isn't. That knowledge is too valuable to lose and too messy for formal documentation.

**Stories are the project's memory of what it was like to figure things out.** They are dated, narrative, and honest. They live next to the canon, but they are not the canon.

---

## What a story is

A `story` is a first-person or third-person account of a significant engineering session: debugging, implementing, migrating, investigating, or recovering from something. It captures:

- What we were trying to do
- What went wrong or got weird
- What we tried
- What actually worked
- What we learned

A story is **not** a spec, a runbook, or an ADR. It may *lead* to one of those, but its job is to preserve the *context* of discovery.

---

## What a story is not

| Not a story | Instead use |
|-------------|-------------|
| A formal decision with consequences | `adr` in `docs/architecture/decisions/` |
| Exact system behavior | `spec` in `docs/spec/` |
| A polished how-to | `guide` in `docs/guides/` or `runbook` in `docs/ops/` |
| Implementation structure | `architecture` or `component` |
| A one-line bug note | A code comment or issue tracker |

---

## Where stories live

```text
docs/
└── stories/
    ├── INDEX.md
    ├── 2026-06-15_auth-token-race-condition.md
    ├── 2026-06-22_worker-migration_gotcha.md
    └── 2026-07-01_why-we-pin-node-20.md
```

Every story is a dated file in `docs/stories/`. No subfolders: the layer is intentionally flat and scannable. If you have so many stories that you need folders, the real problem is probably that findings aren't being promoted into specs, architecture, or runbooks.

---

## The story lifecycle

Stories are **source material**, not final documentation. They feed the canon:

```text
                ┌─────────────────────────────────────┐
                │ A story reveals something durable   │
                └──────────────┬──────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
  Update spec/          Update architecture/    Update ops/runbooks
  (what is true)        (how it works)          (how to operate)
        │                      │                      │
        └──────────────────────┴──────────────────────┘
                               │
                               ▼
              Link the story to the updated docs
              so the history stays discoverable
```

A story may be **superseded** by canonical docs, but it is never deleted. The narrative remains useful when someone asks, *"Why did we decide this?"* or *"Has anyone seen this before?"*

---

## When to write a story

Write one when:

- You spent real time figuring something out and don't want to relearn it.
- You found a non-obvious root cause.
- You hit a dead end that future-you could hit again.
- A migration or rollout had surprises.
- The *process* of discovery matters as much as the result.

Don't write one when:

- The answer fits in a code comment.
- It's already cleanly documented in a spec or runbook.
- It's a transient tool output or chat log.

---

## Naming convention

```text
YYYY-MM-DD_short-kebab-description.md
```

Examples:

- `2026-06-15_auth-token-race-condition.md`
- `2026-06-22_worker-migration-gotcha.md`
- `2026-07-01_why-we-pin-node-20.md`

The date is the date of the session, not the date you wrote the file.

---

## Frontmatter

```yaml
---
node_type: story
title: Auth Token Race Condition
status: active
updated: 2026-06-15
session_type: debug
tags: [auth, race-condition, token, cache, gotcha]
links:
  relates_to: [/spec/auth.md, /architecture/components/auth-service.md]
  documents: [/src/auth/token-store.ts]
---
```

### Field guidance

| Field | Required | Notes |
|-------|----------|-------|
| `node_type` | **Yes** | Must be `story`. |
| `title` | Recommended | A human name for the session. |
| `status` | Recommended | `active`, `resolved`, `superseded`, or `draft`. Use `superseded` when the findings have been fully promoted to canonical docs. |
| `updated` | Recommended | Date the story happened, or the last meaningful edit. |
| `session_type` | Recommended | `debug`, `implementation`, `migration`, `incident`, `investigation`, `spike`, `review`. |
| `tags` | Recommended | Use liberally. See tag suggestions below. |
| `links` | Optional | Link to related specs, architecture, ADRs, and code. Use `relates_to` for docs and `documents` for code. |

### Story status values

Stories use a slightly wider status vocabulary than other docs:

| Status | Meaning |
|--------|---------|
| `active` | Still relevant, still the best source for this narrative. |
| `resolved` | The underlying issue is fixed; the story is kept for context. |
| `superseded` | Findings have been promoted into canonical docs; story is now historical background. |
| `draft` | Raw notes, not yet cleaned up. |
| `mystery` | We never fully figured it out. Honest and useful. |

---

## Tag suggestions

Use tags so stories are findable later. Good story tags:

- **Session type:** `debug`, `migration`, `incident`, `spike`, `implementation`, `investigation`
- **Domain:** `auth`, `api`, `cli`, `storage`, `deploy`, `cache`, `queue`, `database`
- **Flavor:** `gotcha`, `race-condition`, `workaround`, `performance`, `dead-end`, `root-cause`, `platform`, `dependency`

Example:

```yaml
tags: [debug, auth, race-condition, cache, gotcha, root-cause]
```

---

## Voice and tone

Stories should sound like a competent engineer explaining what happened to a teammate. They can be informal. They can include dead ends. They should be honest about uncertainty.

Good:

> "We assumed the cache was the problem because the symptoms looked identical to last month's issue. It wasn't. The real cause was a missing `await` in the token refresh path."

Bad:

> "The system was misconfigured. This was fixed." (No context, no searchable detail.)

---

## Linking stories to the canon

A story without links rots. After writing or updating a story:

1. If a spec needs updating, update it and link the story in `relates_to`.
2. If code changed, link the relevant files in `documents`.
3. If a runbook or guide should exist, create or update it and link back to the story.

The story becomes a **historical footnote** to the canonical truth.

---

## Searching stories

Stories are often the fastest way to answer: *"Has anyone seen this before?"*

```bash
# Recent stories
ls docs/stories/ | sort | tail -10

# Stories about a domain
rg "tags:.*auth" docs/stories/

# Stories involving a specific component
rg "documents:.*/src/auth/" docs/stories/

# Mysteries we never solved
rg "status: mystery" docs/stories/
```

In Inquire mode, search `docs/stories/` whenever the question involves history, weird behavior, or *"why did we...?"*
