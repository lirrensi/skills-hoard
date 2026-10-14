# AGENTS.md Essences

`docs/` canon is the truth. `AGENTS.md` files are its **essence** — small hand-maintained signposts that autoload into agent context. Essence over exhaustiveness: say what's here, what matters, where to look next.

**The split:** `INDEX.md` is the generated map (never hand-edit). `AGENTS.md` is the hand-written essence (never auto-generate). Essences point AT the map, they are never ON it — tooling ignores them for indexing, counts, lint, and migration.

---

## Root `AGENTS.md` — the ≤10-line block

The project root `AGENTS.md` MUST carry the essence block. Format (between markers, blockquote lines):

```markdown
<!-- docs-essence:start -->
> 📚 Canonical docs live in `docs/` — start with `docs/INDEX.md` (then `docs/ROSTER.md` if present).
> - `docs/overview/` — why: product, users, non-goals · `docs/spec/` — what: behavior, contracts (`features/` per-feature)
> - `docs/architecture/` — how: structure, components, decisions · `docs/verification/` — evidence: strategy, suites, gaps
> - `docs/guides/` how-to · `docs/ops/` runbooks · `docs/reference/` glossary+conventions · `docs/resources/` catalogues
> - `docs/changes/` proposals · `docs/archive/` history · `docs/stories/` memory
<!-- docs-essence:end -->
```

1 pointer line + 4 group lines + 2 marker lines = 8 lines. Room for one project-specific line if earned — cap stays at 10.

**Tool guarantees:**
- `scripts/init.py` creates the block on scaffold; also patches/upgrades an existing `AGENTS.md` that lacks it.
- `scripts/index.py` upgrades a legacy one-line pointer to the block in place (never creates; warns visibly when `AGENTS.md` is missing).
- `scripts/status.py` reports thin/missing blocks and shows folder-essence coverage — informational only, never a health gate.

States: `fat` (block present) · `thin` (legacy one-liner) · `custom` (own words, mentions `docs/INDEX.md`) · `missing`. Custom wording is respected — tooling only appends when nothing points at the docs.

---

## Subfolder `AGENTS.md` — the folder essence

Any `docs/<folder>/AGENTS.md` SHOULD capture that folder's essence for whoever lands there. Suggested shape (free-form, few lines):

```markdown
# {Folder} — essence

- **What's here:** one line on the folder's job in the stack.
- **Start with:** the 1–2 docs to read first (link them).
- **Neighbors:** where adjacent concerns live (`../spec/`, `../architecture/`…).
- **Traps:** vocabulary quirks, layer-boundary warnings (if any).
```

**Rules:**
- Essence, not inventory — never duplicate what `INDEX.md` already lists.
- Point at `INDEX.md` for the full map; keep the essence to what the map can't say (taste, traps, reading order).
- Short relative pointers (`[strategy.md](strategy.md)`, `../spec/`) are fine here — essence files are autoload signposts, not canon graph nodes.

---

- Short relative pointers (`[strategy.md](strategy.md)`, `../spec/`) are fine here — essence files are autoload signposts, not canon graph nodes.
- Copy `templates/agents-folder.md` as the starting shape — fill the four bullets, delete Traps if none.

- **Create** one when a folder gains its own vocabulary, traps, or reading order — don't wait for a reorg.
- **Rewrite** one when the folder's purpose shifts, key docs rename, or neighbors move.
- **Touch** the root block only when top-level folders appear/disappear or the reading path changes.

**Tooling contract:** no script reads, writes, counts, lints, or migrates subfolder `AGENTS.md` files. `walk_docs`, `index.py` counts, `status.py`, `check-roster.py`, `map.py`, `check-no-relative.py`, and `migrate-links.py` all skip them. Hand-edit with confidence — nothing will wipe or flag your words.

---

## What NOT to do

- ❌ Paste full INDEX.md listings into an essence — link the map, don't clone it.
- ❌ Put load-bearing requirements only in an essence — canon lives in typed docs, essence only points.
- ❌ Hand-edit inside the root block's markers for project notes — project notes go outside the markers (tooling only matches the block itself).
