# Roster

The **roster** is the curated map of *everything the project has and uses*. It is the document you read once to understand the whole world: what the components, services, resources, and specs are, what each one does in one line, and where the detail lives.

This is the **map, not the atlas**. The roster holds one-line "what it is / why it matters" summaries and pointers. The depth lives in the docs it links to.

---

## The Core Distinction: Roster vs INDEX.md

| | INDEX.md | Roster |
|---|---|---|
| **Nature** | Auto-generated navigation map | Hand-maintained curated map |
| **Answers** | "What's in this folder?" | "What do we have, and why does it matter?" |
| **Source of truth** | `scripts/index.py` (wipes on rebuild) | You, deliberately, at every change |
| **Granularity** | Every file in every folder | The things worth knowing about the system |
| **Lifecycle** | Rebuild it, don't edit it | Edit it, that's its whole purpose |

INDEX.md is the generated **existence** layer. The roster is the curated **meaning** layer. They complement, they don't replace each other. The roster links to INDEX.md folders and to individual docs; INDEX.md will also list the roster itself (it is a normal doc).

---

## Location and Node Type

- **Default location:** `docs/ROSTER.md`
- **node_type:** `roster`
- A project with a heavy external-resource catalogue may instead keep it at `docs/resources/ROSTER.md`; pass `--roster <path>` to the checker.

```yaml
---
node_type: roster
title: Resource Roster
status: active
updated: YYYY-MM-DD
tags: [roster, resources]
---
```

---

## Entry Format

Each roster entry mirrors the INDEX.md entry shape — one line, absolute link, one-line summary, status emoji:

```markdown
- [Billing API](/architecture/components/billing-api.md) — Pricing, order creation, owns payments [🟢 active]
- [Design Handbook](/resources/design-handbook.pdf) — Vendor UI guide referenced for every screen [🟢 active]
- [Auth Spec](/spec/features/auth.md) — Login, sessions, 2FA behavior [🟢 active]
```

Rules for an entry:

1. **Absolute link convention.** Use the leading-`/` form — `.md` targets resolve against the docs root, non-`.md` targets against the project root. No `../`, no `./`, no bare filenames.
2. **One line, one thought.** The summary says what the thing IS and why it matters. 40–80 chars. If it needs more, the detail goes in the linked doc, not here.
3. **Status emoji mirrors the target.** `🟢 active`, `🟡 draft`, `🔴 deprecated`, `⚫ archived`. A deprecated thing stays listed with 🔴 — the roster records history honestly.
4. **The roster can point at anything** — components, services, resource docs, specs, external artifacts. If it's part of the system's mental model, it belongs here.

---

## The Requirement: Update on Create

**Creating a resource (or any roster-worthy thing) REQUIRES adding its roster entry in the same change.** This is a hard rule, enforced by `scripts/check-roster.py`:

- Every doc with `node_type: resource` MUST appear in the roster. A resource doc with no roster line is a lint failure.
- Every roster entry's link MUST resolve to an existing file or directory. A dead pointer is a lint failure.
- The roster file itself MUST have `node_type: roster` in frontmatter.

This is the "requirement" that keeps the map honest: you cannot create a resource and forget to announce it. The roster is not generated — it is **maintained**, deliberately, and the checker makes maintenance mandatory rather than aspirational.

## The Checker

```bash
python scripts/check-roster.py                      # validate, exit 1 on violations
python scripts/check-roster.py --no-fail            # report only, exit 0
python scripts/check-roster.py --verbose            # show every entry checked
python scripts/check-roster.py --roster docs/resources/ROSTER.md  # custom location
```

Run it after any change that touches resources, components, or the roster itself. Wire it into CI next to `check-no-relative.py` — a stale roster is a lying map, and a lying map is worse than no map.

---

## When to Update the Roster

- **Create:** add the new thing with a one-line summary (required, same change).
- **Rename/Move:** update the link and summary.
- **Deprecate:** keep the line, flip the emoji to 🔴, note the replacement if any.
- **Behavior change:** update the one-liner if the old one is now wrong. The roster should never describe something the way it *used* to work.
- **Remove:** if a thing is truly gone (not just deprecated), remove its line. Deprecation keeps history; removal cleans the map.

---

## Why Curated, Not Generated

A generated roster would list files. A curated roster lists **understanding**: the ordering, the one-line judgment calls, the "why does this matter" that no filesystem can compute. That judgment is exactly what makes the roster the best first read in the system — and exactly why it must be maintained by hand, with the checker standing guard.