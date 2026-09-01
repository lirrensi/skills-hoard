# Design Decisions

This file explains the main choices behind `knowledge-accumulator`.

## Corpus over compressed output

The central artifact is the knowledge folder, especially `corpus.md`.
Smaller outputs such as guides, procedures, or skills are useful, but they are downstream products rather than the source of truth.

## Folder support around the corpus

The corpus stays central, but it is supported by:

- `source_declaration.md` for quick kickoff context
- `charter.md` for scope and purpose
- `source_map.md` for provenance and source handling
- `taxonomy.md` for retrieval structure
- `gaps.md` for steering future harvesting
- `session_log.md` for resumability

This keeps the project usable across many sessions.

## Resumable modes over rigid phases

Knowledge work rarely stays linear.
This skill uses modes that can repeat or alternate:

- bootstrap
- taxonomy
- harvest
- gap-repair
- distill

That makes it easier to continue an existing knowledge base without pretending every session starts from zero.

## Living taxonomy over fixed component counts

The taxonomy should fit the domain and the retrieval needs.
Start small, but let the map branch, split, or merge when the material demands it.
Avoid arbitrary component-count rules.

## Distillation is optional

Some knowledge bases should later produce a smaller artifact.
Others should remain a research base, thinking substrate, or source library.
This skill supports both paths.

## Retrieval and provenance from day one

Accumulation without retrieval becomes clutter.
Retrieval without provenance becomes brittle.
That is why this skill always pairs corpus growth with taxonomy, source mapping, and explicit gap tracking.
