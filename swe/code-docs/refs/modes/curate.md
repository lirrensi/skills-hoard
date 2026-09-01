# Mode: Curate

**Trigger:** Asked to create, update, move, or deprecate individual documents. Handles single-doc changes. For multi-doc feature changes, use Propose mode instead.

---

## Before Any Write — Search First

1. Read the folder's `INDEX.md` to see what already exists.
2. If the topic already has a document → **edit the existing one**, don't create a second.
3. If a similar topic exists → check whether this belongs as a new section in an existing doc.

---

## CREATE — New Document

### 1. Classify
Determine the `node_type` and folder from `../ontology.md` and `../folder-structure.md`.

### 2. Place
Put it in the correct folder. If unsure:
- Behavioral spec → `docs/spec/` or `docs/spec/features/`
- How-to → `docs/guides/`
- Architecture → `docs/architecture/` or `docs/architecture/components/`

### 3. Frontmatter
Add full frontmatter per `../ontology.md`:
```yaml
---
node_type: <type>
title: <Human Name>
status: active
updated: YYYY-MM-DD
tags: [domain, topic]
links:
  depends_on: [/path/to/parent.md]
---
```

### 4. Content
Write content following the format for the `node_type`:
- `spec` → use `../spec-format.md`. Focus on behavior, protocol contracts, internal processing — NOT UI details.
- `verification` → use `../verification.md` and `../../templates/verification.md`. Focus on actual checks, tools, commands, environments, evidence, traceability, suite tiers, and honest gaps.
- `overview` → free-form but concise, warm tone. Focus on user experience, not interface.
- `architecture` / `component` → structural, factual. Focus on internal behavior, processing pipelines, and communication protocols.
- `guide` → step-by-step, task-oriented
- `adr` → Status, Context, Decision, Consequences

### 5. Link
Add at least one incoming link in frontmatter:
- Add `links: depends_on` in frontmatter to parent/related docs.
- INDEX.md entries and folder inventory metadata are auto-generated from the filesystem and frontmatter — you do NOT manually add entries, summaries, counts, or hierarchy lines.

### 6. Rebuild INDEX.md
Run `python scripts/index.py` to regenerate all INDEX.md files from frontmatter.
**Never hand-edit an INDEX.md — the script wipes and overwrites every INDEX.md.** Any manual change you make will be lost.

Do not create or update those counts; rerun `scripts/index.py` instead.

### 7. Roster — required when creating a resource
If the new doc is `node_type: resource` (or anything roster-worthy — a service, component, or artifact that belongs in the project's mental model), **MUST update the roster in the same change** (`docs/ROSTER.md` by default, see `../roster.md`):

- Add one line: `- [Name](/abs/path.md) — one-line what/why [🟢 status emoji]`
- If the roster does not exist yet, create it from `templates/roster.md`.
- Validate: `python scripts/check-roster.py`. It fails if a resource doc has no roster entry, or a roster entry points nowhere.

Creating a resource and *not* rostering it is a lint failure — treat it like forgetting to link the doc.

---

## CAPTURE — Write a Story

Use this for engineering narratives: debug sessions, migrations, incidents, implementation slogs, or any session where the *process of figuring it out* is worth preserving.

### 1. Decide if it belongs in `docs/stories/`

A story is right when:
- You spent meaningful time figuring something out.
- The dead ends and hypotheses matter.
- The context of discovery is useful to future readers.

A story is wrong when:
- The answer fits in a code comment.
- It's already cleanly covered by a spec, runbook, or guide.

### 2. Name it

```text
docs/stories/YYYY-MM-DD_short-description.md
```

Use the date the session happened, not the date you write the file.

### 3. Use the story template

Copy `templates/story.md` and fill it in. Key fields:

```yaml
---
node_type: story
title: {Short, specific title}
status: active
updated: YYYY-MM-DD
session_type: debug | implementation | migration | incident | investigation | spike | review
tags: [debug, auth, race-condition, gotcha]
links:
  relates_to: [/spec/auth.md]
  documents: [/src/auth/token-store.ts]
---
```

### 4. Promote findings to canonical docs

After writing the story, ask:
- Does a `spec/` doc need updating? Update it and link back to the story.
- Does an `architecture/` doc need updating? Update it and link back.
- Does an `ops/` runbook or `guides/` doc need creating? Create it and link back.

The story becomes provenance. The canonical docs become truth.

### 5. Rebuild INDEX.md

Run `python scripts/index.py` so `docs/stories/INDEX.md` lists the new story.

---

## UPDATE — Edit Existing Document

1. **Read first.** Load the current doc and any `depends_on` links.
2. **Check layer.** Don't put implementation detail in spec, don't put behavioral requirements in architecture.
3. **Bump updated.** Change `updated: YYYY-MM-DD` in frontmatter.
4. **Report.** After editing, say what changed, which doc was touched, and any conflicts.

### When to update vs deprecate + replace
- **Update** if the change is small (adding a scenario, fixing a description).
- **Deprecate + create new** if the change is fundamental (new approach, different architecture).

**If the doc is rostered**, update the roster line in the same change: fix the link on move, flip the emoji on deprecate, refresh the summary when the behavior description changes. The roster must never describe something the way it used to work.

---

## MOVE — Relocate a Document

1. **Use git mv** to preserve history: `git mv docs/old/path.md docs/new/path.md`
2. **Rewrite every link** pointing to the old path — check all frontmatter `links:` and body markdown links.
3. **Run `python scripts/index.py`** to regenerate all INDEX.md files — the script will pick up the new location from frontmatter and the old folder's INDEX.md will drop the entry automatically.

---

## DEPRECATE — Mark as Outdated

1. Set `status: deprecated` in frontmatter.
2. Add `supersedes: [old-file.md]` in the replacement doc's frontmatter (if applicable).
3. Run `python scripts/index.py` — the script reads `status: deprecated` from frontmatter and adds the 🔴 emoji automatically.
4. **Never physically delete a file.** No text must be lost as a result of any operation. Git preserves history; the doc stays for reference. Moving to `archive/` is allowed (the file still exists).

---

## Reference Files

Always load for Curate mode:
- `../ontology.md` — node_type vocabulary, frontmatter spec, link types, status values
- `../index-spec.md` — INDEX.md format and script usage (`python scripts/index.py`)

Load as needed:
- `../folder-structure.md` — if placing a new doc or reorganizing
- `../spec-format.md` — if writing a behavioral spec
- `../verification.md` — if writing or editing a verification strategy
- `../principles.md` — if unsure about layer boundaries
- `../stories.md` — if capturing or editing a `story`
- `../roster.md` — if creating, moving, or deprecating anything roster-worthy (resources, services, components)
