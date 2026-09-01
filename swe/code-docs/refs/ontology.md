# Documentation Ontology

Every document in `docs/` is a typed **object** in the ontology — inspired by Palantir Foundry's ontology model and GitMark's code-ontology. Each document has a `node_type` (what kind of thing it is), frontmatter **properties** (metadata), and typed **links** (relationships to other docs and code).

---

## Node Types

Each document has exactly one `node_type`. Choose based on what the document IS, not what it contains.

| `node_type` | What it is | Lives in |
|-------------|-----------|----------|
| `overview` | Product identity, purpose, users, non-goals | `docs/overview/` |
| `spec` | Behavioral specification — cross-cutting system behavior and user-perceivable features (requirements + scenarios) | `docs/spec/` |
| `architecture` | Implementation structure description | `docs/architecture/` |
| `component` | Per-component architecture detail | `docs/architecture/components/` |
| `verification` | Verification strategy and evidence map — how project claims are checked against implementation and intent | `docs/verification/` |
| `adr` | Architectural decision record | `docs/architecture/decisions/` |
| `guide` | How-to / tutorial | `docs/guides/` |
| `runbook` | Operational procedure | `docs/ops/` |
| `reference` | Cross-cutting reference (glossary, conventions) | `docs/reference/` |
| `resource` | External resource catalogue — describes artifacts adjacent to the project (downloaded docs, design handbooks, business process PDFs, static assets) that are not part of the codebase but are useful references | `docs/resources/` |
| `roster` | Curated map of everything the project has and uses — hand-maintained one-line entries pointing at the things that matter. The "read this first" document. NOT auto-generated; creating a resource REQUIRES updating it | `docs/ROSTER.md` (or `docs/resources/ROSTER.md`) |
| `change-proposal` | Proposal for a change (why + scope) | `docs/changes/<name>/proposal.md` |
| `change-behavior` | Delta behavior spec (ADDED/MODIFIED/REMOVED) | `docs/changes/<name>/behavior.md` |
| `change-design` | Technical approach for a change | `docs/changes/<name>/design.md` |
| `change-tasks` | Implementation checklist | `docs/changes/<name>/tasks.md` |
| `index` | Folder table of contents | Any `INDEX.md` |
| `story` | Dated narrative of an engineering session — debug, migration, implementation, incident | `docs/stories/` |

**Creating new types:** You MAY create new `node_type` values if none of the existing types fit your document. However, every new type MUST be:
1. Documented in `docs/ontology.md` (the project's ontology registry) with a clear explanation of what it is, where it lives, and why it exists.
2. Added to the table above so the vocabulary stays current.

**Guidance:** Only create a new type when it captures a genuinely distinct kind of document that will be used repeatedly. If it only fits one or two documents, use the closest existing type instead.

**The ontology registry (`docs/ontology.md`) is the single source of truth for what document types exist and what they mean.** If a type isn't in the registry, it doesn't exist. If a new type is created, the registry must be updated.

**Fallback rule:** If unsure and you don't want to create a new type, a behavioral spec is `spec`, a how-to is `guide`.

**Stories:** `story` documents live in `docs/stories/` and capture dated engineering narratives. They are *not* canonical specs or runbooks — they are source material that may feed those layers. See `refs/stories.md` for full conventions, templates, and the story lifecycle.

---

## Frontmatter Specification

Every document MUST have YAML frontmatter. Minimal for index/non-load-bearing docs, full for all others.

> **Hard rule:** all link paths in user-authored docs MUST start with `/`. No `../`, no `./`, no bare `foo.md`, no folder-prefix forms. See [Link Path Convention](#link-path-convention--always-absolute) for the full story and [Enforcement](#enforcement-the-no-relative-crap-rule) for how it's linted.

### Minimal (for `index` and lightweight docs)

```yaml
---
node_type: index
updated: 2026-06-09
---
```

### Full (for all load-bearing docs)

```yaml
---
node_type: spec
title: Authentication Behavior
status: active
updated: 2026-06-09
tags: [auth, security, sessions]
confidence: certain
links:
  depends_on: [/overview/product.md]
  documents: [/src/auth/]
  supersedes: [/archive/old-auth-spec.md]
---
```

Verification documents use the verification relationship to make evidence discoverable:

```yaml
---
node_type: verification
title: Project Verification Strategy
status: active
updated: 2026-06-09
tags: [verification, testing]
links:
  depends_on: [/overview/product.md, /spec/INDEX.md, /architecture/INDEX.md]
  verifies: [/spec/INDEX.md]
---
```

### Field Reference

| Field | Required | Values | Notes |
|-------|----------|--------|-------|
| `node_type` | **Yes** | See table above | Determines where the doc lives and how it's treated |
| `title` | Recommended | Free text | Human-readable name; used in INDEX.md |
| `status` | Recommended | `active`, `draft`, `deprecated`, `archived` | Defaults to `active` if absent |
| `updated` | Recommended | `YYYY-MM-DD` | Last meaningful content edit |
| `tags` | Optional | `[lowercase, hyphenated]` | Free-form for search and grouping |
| `confidence` | Optional | `decided`, `tentative`, `exploratory` | Whether a decision has been made, or it's open to change |
| `links` | Optional | See below | Typed links to other docs and code |
| `resource` | Optional | URI or path string | Canonical pointer to the *underlying asset* the doc describes (dashboard URL, service endpoint, table, repo path, file location, etc.). Distinct from `links.*`: it answers "where is the real thing this doc talks about?", not "how does it relate to other docs?". |
| `sync_status` | Optional | `verified`, `unchecked`, `drifted` | Whether Sync mode has confirmed docs match code. `unchecked` = never synced, `verified` = confirmed match, `drifted` = discrepancy found |
| `last_synced` | Optional | `YYYY-MM-DD` | When Sync mode last ran against this doc's linked code |

### Confidence Field

Describes whether a decision has been finalized, not how sure you are:

| Value | Meaning | When to use |
|-------|---------|------------|
| `decided` | Decision is made and settled | Architecture choices, spec requirements, accepted ADRs |
| `tentative` | Decision is made but may change | New features, experimental components, early-stage specs |
| `exploratory` | No decision yet — exploring options | Research spikes, prototype docs, pre-ADR analysis |

Do NOT use `confidence` to express how sure you are about facts. Use it to signal whether a decision is locked or still in play. A spec with `confidence: tentative` says "this is the current plan but expect changes."

---

## Resource Field

`resource:` is a **single, canonical pointer to the real-world asset a doc is about** — a live URL, a service endpoint, a dashboard, a database table, a repo path, a file on disk. It is *not* a relationship to other docs; that is what `links:` is for. It answers a different question:

- `links.*` → *"how does this doc relate to other docs and code?"*
- `resource:` → *"where is the actual thing this doc describes?"*

**Use `resource:` when the doc describes a tangible asset** (a service, a table, a dashboard, an API, a runbook target). **Omit it when the doc is purely abstract** (a philosophy, a concept, a definition, a process).

`resource:` is a single string. Prefer absolute URIs when one exists. If a relative path is the only option, resolve it the same way `links.*` paths are resolved (relative to the doc's own directory).

### Examples

```yaml
# A spec for a BigQuery table — pointer is the BigQuery console URL
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders

# An architecture doc for a service — pointer is the service entry in code
resource: /services/billing/src/index.ts

# A runbook for a dashboard — pointer is the dashboard URL
resource: https://grafana.example.internal/d/billing-funnel

# An ops runbook for an alert — pointer is the alert config
resource: /infra/alerts/billing-freshness.yaml

# A spec describing a concept (e.g. "metric definition") — no resource
# (omit the field; the doc is abstract)
```

### Why it's a separate field, not a `links.*` type

- It is **singular** by design — every doc has at most one canonical asset, which keeps "jump to the real thing" a one-key lookup.
- It is **renderable** — `INDEX.md` and `status.py` can show a "↗ live" affordance next to docs that have a `resource:`.
- It is **stable under rename** — moving the doc across folders does not break the link, because the resource is usually absolute or repo-rooted.

### In `status.py` reports

`resource:` is treated as a *soft signal*, not an invariant. A doc without one is **not** a finding — many abstract docs legitimately have no asset. A doc *with* a `resource:` is **not** verified; we do not check that the URL still resolves (that would be HTTP probing on every run, which is rude and slow). It is purely a navigational affordance.

### The double meaning: `resource` field vs `resource` node_type

The word "resource" serves two distinct roles in the ontology. They share a name because they answer complementary questions about the same concept — but they operate at different levels:

| Concept | Scope | Question it answers |
|---------|-------|---------------------|
| **`resource:` field** (frontmatter) | Any doc | *"Where is the real-world asset this doc describes?"* |
| **`resource` node_type** (document type) | A standalone doc | *"What is this external artifact, and why is it useful to this project?"* |

**How they relate:** A `resource` node_type doc typically has a `resource:` field pointing to the actual artifact it catalogues (the file path, URL, or location). The field says "it's over there," the doc body explains what it is, why it matters, and how to use it.

**How to tell them apart in conversation:** If someone says "check the resource," they mean the document. If someone says "what's the resource field say," they mean the frontmatter pointer. Context disambiguates — same word, different jobs, no conflict.

**On a spec doc:** the `resource:` field might point to a dashboard URL. **On a resource doc:** the `resource:` field points to the downloaded PDF or ZIP, and the body catalogues it. Same field, same syntax, different purpose depending on the doc it lives in.

---

## Link Types

Links are markdown links `[text](path.md)` declared under `links:` in frontmatter. Inline links in body text default to `relates_to`.

| Link type | Meaning | Direction |
|-----------|---------|-----------|
| `depends_on` | Read that first to understand this | doc → doc |
| `documents` | This doc describes that code/service | doc → code |
| `implemented_by` | Where this behavior lives in code | spec → source |
| `supersedes` | Replaces a stale document | new → old |
| `relates_to` | Adjacent topic (default for inline links) | doc ↔ doc |
| `part_of` | Belongs to a larger index | doc → index |
| `implements` | This code satisfies that requirement | code → spec |
| `verifies` | This verification document/check provides evidence for that behavior | verification → spec/overview/architecture |
| `verified_by` | This behavior or design is covered by that verification strategy/check | spec/overview/architecture → verification |

### Link Examples

```yaml
links:
  depends_on: [/overview/product.md]
  documents: [/src/auth/, /src/sessions/]
  supersedes: [/archive/old-auth-flow.md]
  implemented_by: [/src/auth/login.ts]
```

---

## Link Path Convention — Always Absolute

**All link paths in `links:` frontmatter and in inline body prose MUST be absolute, scoped to the docs root or the project root.** No `../` anywhere. No `./sibling.md`. No `../overview/foo.md`. The reason is simple: relative links are a slow-motion bug factory. They break the moment you move a file, and you only find out when somebody clicks the link and 404s — or an agent walks the graph and gets lost.

### The rule

A leading `/` means **absolute**. The scope is inferred from the file extension:

| Link looks like… | Resolves against… | Example |
|---|---|---|
| `/overview/product.md` (any `.md` / `.markdown`) | the **docs root** | `docs/overview/product.md` |
| `/src/auth/index.ts` (anything else) | the **project root** | `src/auth/index.ts` |

So `docs/spec/features/auth.md` writing `depends_on: [/overview/product.md]` and `docs/architecture/core.md` writing `depends_on: [/overview/product.md]` produce **the same target**. Move either referrer anywhere inside `docs/` — the link still works. Move the *target* — only the target's own location matters, and the link will report as broken (which is what you want).

### Why this and not `../`?

- **No math.** You never count `..`s. You just write the path the way you'd say it out loud: "the auth spec is at `/spec/features/auth.md`."
- **Stable on referrer move.** If `docs/spec/auth.md` becomes `docs/spec/features/auth.md`, no link in any other doc needs updating.
- **Stable on docs-folder rename.** The convention's contract is "leading `/` means docs root for `.md`" — `docs/` can be renamed in the resolver config without touching the docs themselves.
- **One syntax for docs and code.** `[text](/src/auth/)` works identically to `[text](/overview/product.md)`. No fallback rules, no special cases.
- **OKF-compatible shape.** The Open Knowledge Format uses the same leading-`/` convention for bundle-relative paths. If Pharaoh ever publishes an OKF bundle, no rewriting needed.

### What about code targets?

Code targets (`/src/...`, `/services/...`, `/infra/...`) resolve to the project root, not the docs root. So a spec at `docs/spec/auth.md` can say `documents: [/src/auth/]` and it will find `src/auth/` in the project root, no matter where the spec lives.

### Legacy relative form (still accepted, not recommended)

For backward compatibility, the resolver also accepts:

- A path starting with a known top-level folder (e.g. `overview/product.md`, `src/auth/`) — treated as relative to docs root or project root respectively based on the folder convention.
- A plain relative path (e.g. `sibling.md`, `./foo.md`, `../bar.md`) — relative to the doc's own directory.

These forms work but break on move. They are supported only to make migration painless. The canonical, recommended form is the leading-`/` absolute form.

### In `status.py` reports

When a link is broken, the report shows the **raw href the author wrote** (e.g. `/overview/ghost.md`), not a re-serialised path. So you can see exactly what the doc says and fix it in one place.

### Migration

Run `python scripts/migrate-links.py docs/` to auto-rewrite existing relative links in frontmatter and body prose into the absolute form. The script is idempotent — running it twice is a no-op.

### Enforcement (the "no relative crap" rule)

**All link paths in user-authored docs MUST start with `/`.** No exceptions, no `../`, no `./`, no bare `foo.md`, no folder-prefix `overview/foo.md`. Just the leading slash.

Run `python scripts/check-no-relative.py docs/` to lint the doc tree. It exits **1** when it finds any relative path in any user-authored doc, and prints the exact location and offending href so you can fix it in one place. The check is **CI-friendly** — wire it into your pre-commit hook or your CI pipeline and a relative path can never sneak in.

The check is intentionally **strict but smart**:

| Path / file pattern | Linted? | Why |
|---|---|---|
| `docs/overview/foo.md`, `docs/spec/bar.md`, etc. | ✅ yes | normal user-authored docs |
| `docs/INDEX.md`, `docs/overview/INDEX.md`, etc. | ❌ skipped | auto-generated by `index.py` |
| `docs/changes/<name>/{proposal,behavior,design,tasks}.md` | ❌ skipped | change-artifact templates use bare siblings; resolver handles correctly |
| `docs/changes/<name>/stray.md` (any other name) | ✅ yes | if you put a non-canonical file in a change folder, it gets linted |
| `docs/changes/<name>/{*.md}` with `--include-changes` flag | ✅ yes | opt-in strict mode for projects that want *no* exceptions |
| `skills/code-docs/refs/*.md`, `skills/code-docs/templates/*.md` | n/a | skill internals, not user docs |
| External URLs (`http://...`, `mailto:...`, `tel:...`) | ✅ allowed | navigation off-repo |
| Pure anchors (`#section`) | ✅ allowed | in-page navigation |

Use `--no-fail` to make the check informational (exit 0 even on violations) — useful for surfacing a backlog of legacy paths during migration without breaking CI. Use `--verbose` to see every file inspected. Use `--include-changes` to enable the strictest mode that also lints the change-artifact siblings.

---

## Status Values

| Status | Meaning | When to use |
|--------|---------|------------|
| `active` | Current, authoritative | Default for all live docs |
| `draft` | Work in progress, not yet authoritative | New docs still being shaped |
| `deprecated` | No longer current, kept for history | Old behavior replaced by newer doc; set `supersedes` on replacement |
| `archived` | Historical record only | Moved to `docs/archive/` after a change is completed |

### Story status values

Stories may use a slightly wider vocabulary. See `refs/stories.md` for the full list. The additional values are:

| Status | Meaning |
|--------|---------|
| `resolved` | The underlying issue is fixed; the story is kept for context. |
| `mystery` | We never fully figured it out. Honest and useful. |

---

## Tags

Tags enable cross-cutting search and grouping. Use lowercase, hyphenated, stable tags.

Good tag categories:
- **domain:** `auth`, `api`, `cli`, `ui`, `storage`
- **type:** `spec`, `decision`, `incident`, `workflow`
- **quality:** `security`, `performance`, `reliability`

```yaml
tags: [auth, security, api, spec]
```

---

## Invariants (enforced by Audit mode)

These must hold for a healthy documentation ontology:

- **I1:** Every folder in `docs/` has an `INDEX.md` with `node_type: index`.
- **I2:** Every doc (except `index`) has frontmatter with a valid `node_type`.
- **I3:** No broken cross-references (markdown links to missing files).
- **I4:** No orphans — every load-bearing doc is linked from at least one `INDEX.md`.
- **I5:** A `supersedes` target has `status: deprecated` or `status: archived`.
- **I6:** Layer coherence — `spec/` doesn't contradict `overview/`, `architecture/` doesn't contradict `spec/`.
