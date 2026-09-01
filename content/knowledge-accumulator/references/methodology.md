# Knowledge Accumulator Methodology

## Purpose

Knowledge Accumulator is for building a durable corpus that can support future reasoning, retrieval, execution, and optional distillation.

The main output is not a polished final skill.
The main output is a folder that keeps getting more useful.

## Core ideas

### 1. The corpus is the source of truth

Keep one main body of accumulated knowledge in `corpus.md`.
Do not treat downstream outputs as canonical.
If a later guide, skill, or reference sheet needs to change, update the corpus first.

### 2. Iteration beats one-shot authoring

Good knowledge bases are built over many sessions:

- initial scope and rough map
- first-pass harvesting
- use in real thinking or tasks
- discover gaps and contradictions
- refine taxonomy and add more material
- optionally distill when enough value exists

### 3. Retrieval matters from day one

Accumulation without retrieval becomes landfill.
Use taxonomy, source mapping, and gap tracking so future work can find the right material quickly.

### 4. Distillation is valuable but lossy

Procedures and small skills are compressed outputs.
They are useful precisely because they omit detail.
That makes them downstream products, not the source of truth.

## Recommended artifact roles

- `source_declaration.md` - lightweight kickoff note for focus, source types, and starting pointers
- `charter.md` - mission, scope, source types, success criteria, exclusions
- `source_map.md` - source inventory, handling rules, provenance notes
- `taxonomy.md` - retrieval map, synonyms, relationships, boundaries
- `corpus.md` - accumulated knowledge body
- `gaps.md` - missing areas, contradictions, next harvest targets
- `search_log.md` - reproducible record of meaningful searches and selection choices
- `coverage_report.md` - quick view of strong, thin, and overloaded areas
- `session_log.md` - resumable history of what changed and why
- `distillation_brief.md` - optional compression plan for a downstream artifact

## Working rhythm

### Bootstrap

Start with enough clarity to avoid chaotic accumulation:

- what domain or problem this corpus serves
- where sources will come from
- what retrieval questions the future corpus should answer
- what is in scope and out of scope

### Taxonomy pass

Build the first retrieval map before heavy harvesting.
Keep it thin at first.
It only needs to be good enough to keep later additions organized.

### Harvest pass

Add useful material into `corpus.md` while updating `source_map.md` and `gaps.md`.
Do not wait for perfect structure before collecting.
Do not collect so fast that structure collapses.

### Gap pass

Use the corpus, source map, and real usage to identify:

- thin or overloaded taxonomy areas
- open questions
- unresolved contradictions
- missing source classes
- missing examples, procedures, or edge cases

### Distillation pass

Only when requested, compress part of the corpus into a smaller artifact.
The corpus remains canonical.

## Quality bar

A knowledge base is in decent shape when:

- another agent can understand the purpose quickly
- major sections are discoverable from the taxonomy
- links and embedded notes have clear why-this-matters context
- important claims can be traced back to sources or provenance notes
- gaps are explicit instead of hidden
- resuming after a break is easy

## Non-goals

- forced final packaging
- perfect formal ontology from the start
- replacing all external sources with copied content
- endless summarization of already-known material
