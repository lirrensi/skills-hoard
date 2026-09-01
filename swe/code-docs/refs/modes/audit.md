# Mode: Audit

**Trigger:** Asked to check documentation health, verify invariants, or find quality issues. Runs passive checks — never edits docs unless explicitly asked.

---

## Workflow

### Step 1: Load ontology
Read `../ontology.md` for the invariant definitions and vocabulary.

### Step 2: Run each invariant check

#### I1: Every folder has INDEX.md
Scan `docs/` recursively. Every directory must contain an `INDEX.md` file.

**Check:**
- List all directories under `docs/`
- Check for `INDEX.md` in each
- Skip `docs/changes/<name>/` folders (they don't need INDEX.md; only `docs/changes/INDEX.md` matters)

**Report:**
```
Missing INDEX.md:
- docs/guides/ — no INDEX.md found
- docs/spec/features/ — no INDEX.md found
```

#### I2: Every doc has valid frontmatter
Scan all `.md` files in `docs/`. Each must have:
- YAML frontmatter (between `---` delimiters)
- A valid `node_type` field (must be in the vocabulary)

**Check:**
- Files with no frontmatter → flag
- Files with missing `node_type` → flag
- Files with `node_type` outside vocabulary → flag (suggest closest match)

**Report:**
```
Frontmatter issues:
- spec/features/auth.md — missing node_type
- architecture/old-stuff.md — invalid node_type "legacy" (did you mean "architecture"?)
- guides/setup.md — no frontmatter at all
```

#### I3: No broken cross-references
Check every markdown link `[text](path.md)` in both body text and frontmatter `links:`.

**Check:**
- For each link, verify the target file exists
- For `links:` frontmatter arrays, verify each path resolves
- Skip external URLs (http/https)

**Report:**
```
Broken links:
- spec/features/auth.md → /overview/product.md (broken: product.md not found at that path)
- spec/features/api.md: links.documents → /src/api/ (directory exists, but no .md files there)
```

#### I4: No orphans
Every load-bearing doc (not `node_type: index` or `node_type: change-*`) must have at least one incoming link.

**Check:**
- For each doc, search all other docs' `links:` frontmatter and INDEX.md entries for a link to it
- A doc is orphaned if NOTHING links to it (not from any INDEX.md, not from any `links: depends_on`, not from any body link)

**Report:**
```
Orphaned documents (no incoming links):
- spec/features/old-feature.md — exists but nothing references it
- architecture/components/unused.md — not linked from any INDEX.md or doc
```

#### I5: Superseded docs are marked
Check frontmatter `links: supersedes` targets. The target doc must have `status: deprecated` or `status: archived`.

**Check:**
- Find all docs with `links: supersedes`
- Read the target's frontmatter
- If target `status` is `active` → flag

**Report:**
```
Supersede issues:
- spec/features/auth-v2.md supersedes auth-v1.md — but auth-v1.md is still status: active
```

#### I6: Layer coherence
Check that lower layers don't contradict higher layers.

**Check (heuristic — not exhaustive):**
- `architecture/` docs should not define behavioral requirements (that belongs in `spec/`)
- `spec/` docs should not reference implementation details (classes, files, frameworks)
- `overview/` docs should not contain detailed behavioral specs

#### I7: Verification strategy exists and is discoverable

Every maintained project MUST have a `node_type: verification` strategy at `docs/verification/strategy.md` or an explicitly linked equivalent. Confirm that it names actual tools/commands, test layers, suite tiers, environments, evidence, and known gaps. A missing strategy is a documentation-quality finding even when tests exist.

#### I8: Verification traceability is honest

Important goals, requirements, protocols, and user journeys MUST map to a verification check/evidence entry or an explicit gap. Check that the strategy does not claim more than a check can prove (for example, a unit test presented as end-to-end UI coverage).

**Report:**
```
Layer coherence issues:
- architecture/components/agent.md — contains behavioral requirements (should be in spec/)
- spec/features/api.md — references "Express middleware" (implementation detail, should be in architecture/)
```

#### I9: Roster is present and honest

If the project has any `node_type: resource` docs (or otherwise roster-worthy components/services), a roster must exist (`docs/ROSTER.md` by default) and every resource doc must appear in it.

**Check:** run `python scripts/check-roster.py`. It validates:
- R1 — every roster entry's link resolves to an existing file/directory
- R2 — every doc with `node_type: resource` appears in the roster
- R3 — the roster file itself has `node_type: roster`

**Report:**
```
Roster issues:
- resources/handbook.pdf.md — resource exists but is not in ROSTER.md (creating it REQUIRES a roster entry)
- ROSTER.md line 12: 'Old Service' → /services/old-svc.md (broken: target not found)
```

### Step 3: Generate summary

```markdown
## Audit Report — YYYY-MM-DD

### Summary
| Invariant | Status | Issues |
|-----------|--------|--------|
| I1: INDEX.md coverage | ❌ 2 missing | guides/, spec/features/ |
| I2: Valid frontmatter | ❌ 3 issues | See below |
| I3: No broken links | ✅ Clean | — |
| I4: No orphans | ❌ 2 orphans | See below |
| I5: Supersede marking | ✅ Clean | — |
| I6: Layer coherence | ⚠️ 2 warnings | See below |
| I7: Verification strategy | ❌ missing/incomplete | See below |
| I8: Verification traceability | ⚠️ gaps/overclaims | See below |
| I9: Roster present + honest | ❌ 2 issues | See below |

### Files checked
{N} documents across {N} folders

### Recommendations
1. Run `python scripts/index.py` to generate INDEX.md for all folders
2. Add frontmatter to: guides/setup.md, architecture/old-stuff.md
3. Link or deprecate orphaned docs: old-feature.md, unused.md
4. Move behavioral requirements from architecture/components/agent.md to spec/
5. Run `python scripts/check-roster.py` and fix roster gaps
```

---

## Audit Severity

| Symbol | Meaning |
|--------|---------|
| ❌ | Must fix — breaks ontology guarantees |
| ⚠️ | Should fix — degrades doc quality |
| ✅ | Clean |

---

## What NOT to do during Audit

- ❌ Edit any docs (unless explicitly asked to fix issues found)
- ❌ Run `python scripts/index.py` automatically (report the gap, don't fill it)
- ❌ Delete orphaned docs (report them, let the user decide)
- ❌ Guess at correct frontmatter values

---

## Reference Files

Load:
- `../ontology.md` — invariant definitions, node_type vocabulary, link types, status values
- `../folder-structure.md` — expected folder layout
- `../index-spec.md` — INDEX.md format expectations
- `../verification.md` — verification content and evidence standards
- `../roster.md` — roster format and the create-⇒-roster requirement
