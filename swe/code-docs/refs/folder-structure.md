# Folder Structure

The canonical documentation layout. Every folder has an `INDEX.md`. Documents are placed by their `node_type` — never arbitrarily.

---

## Full Layout

```
docs/
├── INDEX.md                    # Master map of everything (node_type: index)
├── ontology.md                 # This documentation system's ontology (node_type: reference)
├── ROSTER.md                   # Curated map of everything the project has (node_type: roster)
│
├── overview/                   # "Why" layer — identity, purpose, goals
│   ├── INDEX.md
│   ├── product.md              # Elevator pitch, core value, major flows (node_type: overview)
│   └── personas.md             # User roles, journeys, needs (node_type: overview)
│
├── spec/                       # "What" layer — behavioral specification
│   ├── INDEX.md
│   ├── system-model.md         # Actors, states, core concepts (node_type: spec)
│   ├── data-model.md           # Entities, schemas, transitions (node_type: spec)
│   ├── error-handling.md       # Failure modes, edge cases, limits (node_type: spec)
│   └── features/               # Per-feature behavioral specs
│       ├── INDEX.md
│       ├── auth.md             # (node_type: spec)
│       ├── api.md              # (node_type: spec)
│       └── ...                 # One file per feature
│
├── architecture/               # "How" layer — implementation structure
│   ├── INDEX.md
│   ├── core.md                 # Shared foundation, boundaries (node_type: architecture)
│   ├── components/             # Per-component architecture detail
│   │   ├── INDEX.md
│   │   ├── agent.md            # (node_type: component)
│   │   ├── cli.md              # (node_type: component)
│   │   └── ...                 # One file per independently-understandable component
│   └── decisions/              # Architecture Decision Records
│       ├── INDEX.md
│       └── 0001-short-name.md  # (node_type: adr)
│
├── verification/               # Evidence layer — how we know the system works
│   ├── INDEX.md
│   ├── strategy.md             # Project-wide verification strategy (node_type: verification)
│   └── ...                     # Feature/component verification maps when justified
│
├── changes/                    # Active change proposals
│   ├── INDEX.md
│   └── <change-name>/          # One folder per change
│       ├── proposal.md         # Why + scope (node_type: change-proposal)
│       ├── behavior.md         # Delta spec: ADDED/MODIFIED/REMOVED (node_type: change-behavior)
│       ├── design.md           # Technical approach (node_type: change-design)
│       └── tasks.md            # Implementation checklist (node_type: change-tasks)
│
├── archive/                    # Completed changes (preserved for history)
│   ├── INDEX.md
│   └── <YYYY-MM-DD>-<change-name>/  # Date-prefixed for chronological order
│       └── ...                 # Full change context preserved
│
├── stories/                    # Dated engineering narratives — the project's memory
│   ├── INDEX.md
│   └── YYYY-MM-DD-short-name.md  # (node_type: story)
│
├── guides/                     # How-to documents
│   ├── INDEX.md
│   └── ...                     # (node_type: guide)
│
├── reference/                  # Cross-cutting reference material
│   ├── INDEX.md
│   ├── glossary.md             # Shared terminology (node_type: reference)
│   └── conventions.md          # Coding conventions (node_type: reference)
│
├── resources/                  # External resource catalogues
│   ├── INDEX.md
│   └── ...                     # (node_type: resource)
│
└── ops/                        # Operational documentation
    ├── INDEX.md
    └── ...                     # (node_type: runbook)
```

---

## Placement Rules

| If the doc is about... | Place it in... | `node_type` |
|------------------------|---------------|-------------|
| Product identity, purpose, users | `docs/overview/` | `overview` |
| Exact system behavior, contracts | `docs/spec/` | `spec` |
| One specific feature's behavior | `docs/spec/features/` | `spec` |
| Implementation structure | `docs/architecture/` | `architecture` |
| One specific component | `docs/architecture/components/` | `component` |
| An architectural decision | `docs/architecture/decisions/` | `adr` |
| How project behavior is verified, including tools, suites, evidence, and gaps | `docs/verification/` | `verification` |
| How to do something | `docs/guides/` | `guide` |
| Operational procedure | `docs/ops/` | `runbook` |
| Shared definition or convention | `docs/reference/` | `reference` |
| An external artifact to catalogue — downloaded docs, design handbook, business process PDF, static reference material | `docs/resources/` | `resource` |
| The curated map of everything the project has and uses — hand-maintained, one line per thing | `docs/ROSTER.md` (or `docs/resources/ROSTER.md`) | `roster` |
| A proposed change | `docs/changes/<name>/` | `change-*` |
| Completed change | `docs/archive/<date>-<name>/` | `change-*` (preserved) |
| An engineering narrative: debug session, migration, incident, investigation | `docs/stories/` | `story` |

---

## Split Rules

### When to split `spec/features/`

A feature gets its own spec file (still `node_type: spec`) if:
1. **Independence test:** the feature could be understood, specified, and tested independently.
2. **Size threshold:** the parent spec exceeds 300 lines — extract features.
3. **Different actors:** the feature involves different user roles or subsystems.

### When to split `architecture/components/`

A component gets its own `component` file if:
1. **Replaceability test:** it could be rewritten independently without forcing changes to other components.
2. **Size threshold:** the architecture doc exceeds 500 lines — split it.

### When to split `verification/`

Keep the project-wide strategy in `strategy.md`. Add a separate verification document only when a feature, subsystem, or release surface has a distinct toolchain, environment, evidence lifecycle, or execution cadence that would make the strategy harder to navigate. Each split document MUST link back to `strategy.md` and to the specs it verifies.

### When to create a new top-level folder

Add a new folder under `docs/` only when:
- You have ≥3 documents that share a distinct `node_type` not covered above.
- Those documents would clutter an existing folder.

**Exception:** `docs/verification/` is mandatory for maintained projects even when it contains only the canonical `strategy.md`. Verification is a cross-cutting concern and must be discoverable rather than hidden inside architecture or contributor docs.

### Naming rules

- Architecture component files: `arch_{name}.md` → just `{name}.md` inside `components/`.
- ADRs: `NNNN-short-description.md` (4-digit sequential number).
- Change folders: kebab-case, descriptive (`add-dark-mode`, `fix-auth-timeout`).
- Archive folders: `YYYY-MM-DD-<change-name>` (date of archive).
- Story files: `YYYY-MM-DD-short-description.md` (date the session happened).
- Never freeform names like `final-version.md` or `notes-about-stuff.md`.

---

## INDEX.md Rules

- Every folder in `docs/` MUST have an `INDEX.md`.
- `INDEX.md` is a map, not a content document. It lists what's in the folder with one-line summaries.
- `INDEX.md` is also the generated folder inventory. It records the exact indexed-folder hierarchy and calculated direct and recursive file totals; do not maintain those values manually.
- The format is specified in `./index-spec.md`.
- After creating, moving, or deleting any doc, rebuild the affected INDEX.md files.

---

## Glossary Guidance

Create `docs/reference/glossary.md` when:
- The project has ≥2 architecture documents and terms may be interpreted differently
- The spec uses specialized domain terms that need precise definitions
- Multiple agents or contributors could interpret important terms differently
- A term is used inconsistently across the docs

### Glossary format
```markdown
---
node_type: reference
title: Glossary
status: active
updated: YYYY-MM-DD
tags: [reference]
---

# Glossary

## {Term}
{Definition — 1-3 sentences. Precise, unambiguous.}

## {Term}
{Definition}
```

### Glossary rules
- **The glossary wins.** If a term is used inconsistently, the glossary definition is authoritative.
- **The inconsistency is a discrepancy.** Fix the docs, not the glossary.
- **Never silently rewrite the glossary** to match misuse. If the meaning truly changed, update the glossary intentionally and note the change.
- **Only add terms that are ambiguous.** Don't glossary every word — only terms where misunderstanding would cause implementation errors.
