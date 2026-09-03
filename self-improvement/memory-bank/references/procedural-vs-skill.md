# Procedural vs Skill (full)

> Companion to `SKILL.md` → Learn Pass step 4. Load this when a procedural feels hot and you're deciding whether it earns a full skill. Core equation: `runbook == skill`, no extra entity. Procedural stays cheap cold storage inside `memory/procedural/`; skill is the hot, testable artifact outside `memory/` in project-local skills.

Ask one question when writing procedural:

> **Is this for once or for every damn time?**

- **`reuse: once`** (default) — cold note. One-off fix, single-project checklist, evolving steps, behavioral guidance. Stays procedural forever. Example: `how_to_fix_that_weird_2am_bug.md`.
- **`reuse: often`** — hot workflow. You run it every damn time, steps stopped changing, validated 2–3x. Candidate for promotion. Example: deploy procedure.
- **Never promotes**: behavioral / adaptive guidance (`how_to_approach_stressed_user.md`), personal routines, tone rules, single-use context. If it's *how to behave*, not *how to execute*, it stays.

**Promotion checklist** (all should be true before proposing a skill):
- [ ] stable — steps haven't changed in last 2–3 runs
- [ ] cross-project or high-value repeat — not just one repo
- [ ] tool-heavy or painful to reconstruct — scripts, MCP wiring, multi-step commands worth a `SKILL.md` + `scripts/`
- [ ] validated — `confidence: certain|likely`, not `tentative`. A wrong lesson is worse than none.
- [ ] smallest component — would a checklist suffice? Only skill-ify if checklist keeps failing.

**How promotion works:**
1. Always create `procedural` first — never jump straight to skill from `episodic`. This kills skill-spam.
2. When hot, propose skill (via `learn` pass or dream mode). On approval, author the skill **project-local** at `./.agents/skills/<skill-name>/SKILL.md` via your normal skill flow. Never global (`~/.agents/`, `~/.config/opencode/`) unless the user explicitly says `promote to global / share it`.
3. Follow classic skill protocol — light + progressive everywhere, in memory notes and in skills alike: lean `SKILL.md` (~100–200 lines, capability not implementation, exact commands verbatim from source, never invent flags/APIs), bulk goes in `references/` loaded on demand, scripts in `scripts/`, one verification command that proves it worked. A promoted skill that crams everything into one file will rot like a bloated memory file.
4. Link back: set `skill_ref: ".agents/skills/<skill-name>/SKILL.md"` in the procedural frontmatter, flip body to a pointer (`Superseded by [my-skill](...) — see skill for canonical steps`), set `status: superseded` only if the skill is now canonical. Never delete.
5. Rebuild index — the procedural shows up under `Skill Candidates` → `Promoted` automatically.

Delegation note (never required): when a workflow was heavy and steps were independent, add one line `Parallelizable: steps X+Y could run in parallel where delegation exists`. Some envs have subagents, some don't; the note helps future-you decide, nothing auto-delegates.
