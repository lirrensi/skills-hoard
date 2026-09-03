# File Organization (full)

> Companion to `SKILL.md` → Default structure. Load this when the flat layout starts bursting — microservices, sagas, sub-teams. Default stays flat by type; structure only when files drown each other. Index finds any depth automatically.

You may encounter or be instructed to use a more structured layout such as `./memory/semantic/clients/` or `./memory/procedural/operations/`. Follow whatever structure exists; if none exists, use the default type-based layout.

**Microservices / multi-project (3 simple related projects):** tags are enough — `proj-auth`, `proj-billing`, `proj-gateway` + `scope-project`. Only add folders when one project's files start drowning the others, e.g. `./memory/semantic/projects/auth/`, `./memory/semantic/projects/billing/`. Index finds any depth automatically. Cross-project lesson the user wants in two places? Don't duplicate — keep canonical in one bank, tag `scope-global`, link via `related:` from the other. Duplication rots; links don't.

**New types:** Decision, person, and project memories may live in their respective type folders or in a flat structure — consistency matters more than depth. If you create `./memory/decision/`, `./memory/person/`, or `./memory/project/`, the index script will find and catalog them automatically. Same for new kinds (`failed_approach/`, `gotcha/`, `convention/`, `external_ref/`) — folders optional, index auto-catalogs any `memory_type`.

**Threads are just semantic:** no `threads/` folder required. A long-lived pattern that accumulates + references periodically = one semantic file with dated `## Log` entries at the bottom + `related:` links to its episodic moments. Example: `semantic/auth_migration_saga.md` with `## 2026-08-10`, `## 2026-08-18` sections. If a saga outgrows one file, split by phase — still semantic, still canonical-per-topic. Only create `memory/threads/<topic>/` when a single file truly can't hold the working scratch anymore; index finds it either way.
