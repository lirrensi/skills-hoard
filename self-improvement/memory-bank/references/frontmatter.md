# Tags, Naming & Frontmatter (full)

> Companion to `SKILL.md` → Core Philosophy. Load this when writing a new memory file and you want the tag vocabulary, filename shape, and every frontmatter field.

## Tags

Use tags generously but intentionally. Tags make cross-cutting retrieval easy without overcomplicating the folder structure.

Good tag categories:
- domain: `code`, `business`, `personal`, `research`, `creative`
- topic: `auth`, `deploy`, `health`, `finance`, `planning`
- entity: `client-acme`, `project-helios`, `user`, `team`
- type hints: `decision`, `preference`, `incident`, `checklist`, `workflow`, `failed-approach`, `gotcha`, `convention`
- scope (project-based default): `scope-project` (default, omit if obvious), `scope-global` (durable across projects — only when user says to share), `proj-<name>` (e.g. `proj-auth`, `proj-billing` for microservices)

Prefer short, stable, lowercase tags with hyphens when needed. Tags are enough for scope — no `scope:` frontmatter field needed. This bank is root-agnostic: `MEMORY_DIR` is wherever you put it (`./memory/` by default, scripts accept an explicit path), you set it, the skill never hardcodes your layout.

Examples:
- `tags: [code, auth, incident, project-helios]`
- `tags: [business, client-acme, preference, communication]`
- `tags: [personal, travel, checklist]`

## File Naming

```
episodic:   YYYY_MM_DD_meaningful_name.md
semantic:   stable_subject_name.md
procedural: how_to_meaningful_name.md
```

Examples — notice these span many domains:
- *Code:* `2025_03_09_auth_bug_root_cause.md`
- *Business:* `2025_03_10_q1_marketing_decisions.md`
- *Personal:* `user_preferences.md`, `health_tracking_setup.md`
- *Business:* `client_acme_profile.md`, `project_helios_status.md`
- *Code:* `how_to_rotate_api_keys.md`, `incident_response_playbook.md`
- *Behavioral:* `how_to_approach_stressed_user.md`, `tone_guidance_for_sensitive_topics.md`
- *Creative:* `character_ariel_backstory.md`, `songwriting_process.md`
- *Business:* `weekly_client_reporting_workflow.md`

Multiple episodic files per day are normal and encouraged. Semantic and procedural files should usually keep stable names so they can be updated over time.

Rule of thumb:
- `episodic/` = many dated files over time
- `semantic/` = one evolving file per topic
- `procedural/` = one evolving file per workflow or behavior pattern

## Optional YAML Fields (Obsidian-Compatible)

The shared frontmatter supports extra fields. Use any, all, or none — they are optional.

```yaml
---
summary: "One line — specific enough to know if you need to read this"
created: YYYY-MM-DD
updated: YYYY-MM-DD
memory_type: episodic | semantic | procedural | decision | person | project | failed_approach | gotcha | convention | external_ref
tags: [optional, tags]
status: active | superseded | draft | archived
confidence: certain | likely | tentative | deprecated
version: 1
reuse: once | often
skill_ref: ""
related: [other_file.md, another.md]
aliases: [alt-name]
source: "where this came from"
---
```

- `status`: mark outdated ones with `superseded` instead of deleting them
- `confidence`: signal how solid this knowledge is (`certain` ≈ high reliability, `tentative` ≈ low — gate promotion on this)
- `version` (living pages only — semantic/procedural/decision/person/project/convention; never episodic/failed_approach history): integer, starts at 1, bump on every canonical update + one line in body saying *why* it changed (`v3: deploy order flipped, evidence 2026-09-03 session`). Git holds the diff, version holds the reason. Rollback = git revert + note.
- `reuse` (procedural mainly): `once` = cold one-off note, `often` = hot workflow you run every damn time (e.g. deploy). Default `once` if unsure.
- `skill_ref` (procedural mainly): project-local path to the promoted skill when `reuse: often` hardens, e.g. `.agents/skills/deploy/SKILL.md`. Empty until promoted. Local-only — never `~/.agents/` unless user explicitly says promote to global. When set, consider `status: superseded` with a pointer body — never delete.
- `related`: backlinks to other memory files for graph traversal. Use relative paths from `./memory/` root; filenames are unique across the whole memory space, so a simple filename is enough: `related: [semantic/auth_constraints.md, episodic/2026_05_14_auth_bug.md]`
- `aliases`: alternate names to search by
- `source`: whatever you have, never a blocker — `2026-09-03 live session`, `backfill-2024-11 old chat`, a URL, a filename, a person. Inside chat you often have no IDs at all, and that's fine: date + `live-session` beats empty. Used to weigh contradictions (live + recent beats old + backfill unless evidence says otherwise).

These fields make the memory graph richer without adding complexity for simple notes. Only `procedural` needs `reuse`/`skill_ref` — skip them elsewhere.
