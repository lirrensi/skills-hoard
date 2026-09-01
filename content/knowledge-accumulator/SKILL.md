---
name: knowledge-accumulator
description: Build or maintain a long-lived knowledge base in one folder. Use whenever the user wants to accumulate research, expert notes, codebase understanding, manuals, links, taxonomies, source maps, or gap lists over multiple sessions instead of jumping straight to a small procedural skill. Also use when the user wants a durable corpus to think from, a source-of-truth reference set, or optional later distillation into a guide, workflow, or another skill.
---

# Knowledge Accumulator

Use this skill to build a durable knowledge base first.
Do not rush to compress it into a tiny procedure unless the user explicitly wants distillation.

The center of gravity is a persistent folder, not a polished final artifact.
That folder becomes a working memory for future thinking, retrieval, and optional downstream skill creation.

## What This Skill Is For

- growing a corpus across many sessions
- building or refining a taxonomy so material stays retrievable
- collecting links, notes, excerpts, patterns, contradictions, and open questions
- preserving provenance well enough to revisit sources later
- tracking what is known, what is thin, and what still needs harvesting
- optionally distilling the corpus into a procedure, briefing, small skill, or reference pack later

## What This Skill Is Not For

- a mandatory skill-generation pipeline
- a one-shot summarizer
- a polished writing workflow by default
- a replacement for execution or implementation skills

If the user already knows they want a tiny procedural artifact right now, another skill may be a better first stop. If they need a base of understanding that can keep growing, use this one.

## Core Stance

- Corpus first, compression second.
- Retrieval matters as much as accumulation.
- Keep the folder resumable by another agent or by your future self.
- Preserve source context instead of flattening everything into paraphrase.
- Taxonomy is a living map, not a ceremonial outline.
- Distillation is optional and lossy; treat it as a downstream product.

For the deeper rationale and design choices, read `references/methodology.md` and `references/design-decisions.md`.

## Folder Contract

Prefer one stable folder per knowledge base.
If the folder already exists, resume it before creating new files.

Default working set:

```text
knowledge-base/
├── charter.md
├── search_log.md
├── source_map.md
├── taxonomy.md
├── corpus.md
├── gaps.md
├── coverage_report.md
├── session_log.md
└── distillation_brief.md   # optional, only when distilling
```

Use the templates in `templates/` when bootstrapping or normalizing the folder.

## When To Trigger

Use this skill when the user wants to:

- collect a lot of knowledge in the same place over time
- turn vague research into an organized corpus
- build a taxonomy or map of a domain before solving with it
- accumulate expert knowledge, manuals, links, codebase findings, or mixed research
- maintain a source-of-truth document that later feeds thinking or distillation
- revisit a previous corpus, find gaps, and keep extending it

Do not use this skill when:

- the task is a simple lookup or quick answer
- the user needs immediate implementation more than durable accumulation
- the user wants final presentation format decisions rather than corpus-building

## Operating Modes

Choose the dominant mode based on what the user actually needs now:

- `bootstrap` - create the folder, scope, and initial map
- `taxonomy` - determine or repair classification structure
- `harvest` - add material into the corpus and source map
- `gap-repair` - find missing, weak, or contradictory areas and target them
- `distill` - produce a smaller downstream artifact from the corpus

The same project may move between modes over many sessions.

## Default Workflow

### 1. Resume before restarting

If a knowledge folder already exists:

- read `charter.md`, `taxonomy.md`, `gaps.md`, and the latest `session_log.md` entries first
- identify current scope, live gaps, and where the corpus is thin or stale
- continue the existing structure unless it is obviously broken

Do not rebuild the map from scratch just because new material arrived.

### 2. Establish the accumulation contract

If starting fresh, create or fill:

- `source_declaration.md` - quick statement of focus, source types, and starting pointers when a lightweight kickoff helps
- `charter.md` - what this knowledge base is for, who it serves, where it starts and stops
- `source_map.md` - where material comes from and how to treat each source class
- `taxonomy.md` - the current retrieval map
- `corpus.md` - the source-of-truth knowledge body
- `gaps.md` - unanswered questions, thin spots, contradictions, next harvest targets
- `search_log.md` - optional but recommended record of meaningful search activity
- `coverage_report.md` - lightweight coverage view by taxonomy area and source type
- `session_log.md` - chronological accumulation log

Use `templates/source_declaration.md`, `templates/charter.md`, and `templates/source_map.md`.

### 3. Build the retrieval map

Use `templates/taxonomy.md` and the guidance in `references/taxonomy-guidelines.md`.

The taxonomy should help future retrieval, not just look tidy.

- start with top-level domains or facets that matter for lookup
- define boundaries and common synonyms
- track relationships when they matter: parent-child, related, prerequisite, contrast
- allow the map to deepen over time; do not freeze it too early

Use a small number of top-level domains at first, but do not force an arbitrary 3 to 5 component rule if the domain wants a different shape.

### 4. Harvest into the corpus

Use `templates/corpus.md` and `references/source-handling.md`.

For each meaningful addition:

- place it in the right taxonomy area
- keep a short statement of why it matters
- preserve provenance or a source pointer
- choose between linking and embedding deliberately
- record open uncertainty instead of hiding it

If searches or source selection involved real judgment, update `templates/search_log.md` in the working folder.

Keep the corpus useful for browsing:

- concise index at the top
- stable section headers
- short source annotations next to links
- embedded excerpts only when preservation is worth the extra weight

### 5. Update gaps and next harvests

Use `templates/gaps.md`.

After each accumulation burst, ask:

- what important questions remain unanswered
- which taxonomy areas are overloaded or empty
- what contradictions appeared
- what source types are missing
- what would most improve future thinking or retrieval

If the project is growing beyond a small corpus, maintain `coverage_report.md` from `templates/coverage_report.md`.

The gaps file is not failure bookkeeping.
It is the steering layer for the next session.

### 6. Log the session

Use `templates/session_log.md`.

Capture only what is needed to resume well:

- what changed
- what sources were added or revised
- what taxonomy decisions changed
- what gaps were opened or closed
- what the next pass should focus on

### 7. Distill only when asked

If the user wants a smaller downstream artifact, read `references/distillation.md` and create `distillation_brief.md` from `templates/distillation_brief.md`.

Good distillation targets:

- a small procedural skill
- a troubleshooting guide
- a briefing or one-pager
- a decision tree
- a curated quick-reference pack

When distilling:

- treat the corpus as source of truth
- keep links back to the larger corpus when possible
- state clearly what is being compressed away

## Link vs Embed Rule

Use this default:

- link stable, navigable, maintained sources and add a one-line note about what is there
- embed fragile, ephemeral, contradictory, or unusually valuable material that may disappear or be hard to rediscover

Do not dump naked links into the corpus.
Every link should say why future-you should care.

## Response Shape

When using this skill in conversation, usually provide:

1. current project mode
2. what you are adding or changing
3. the key taxonomy or corpus decisions
4. the updated gaps or next harvest targets
5. optional distillation path, only if relevant

## Failure Modes To Avoid

- summarizing instead of accumulating
- collecting without mapping
- rigid taxonomy theater that hurts retrieval
- giant undifferentiated dumps with no provenance
- repeatedly asking the same scoping questions instead of resuming the folder
- distilling too early and losing useful knowledge
- letting generated outputs outrun the underlying corpus quality

## Reference Map

- Method and philosophy: `references/methodology.md`
- Design decisions: `references/design-decisions.md`
- Taxonomy rules: `references/taxonomy-guidelines.md`
- Source handling and provenance: `references/source-handling.md`
- Quality gates and audit checklist: `references/quality-checks.md`
- Distillation guidance: `references/distillation.md`
- Bootstrap templates: `templates/`
