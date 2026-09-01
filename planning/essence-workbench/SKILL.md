---
name: essence-workbench
description: Create editable source-of-truth essence documents from raw material. Use when turning notes, transcripts, research, specs, reports, or mixed source data into structured Markdown or YAML that stays easy to revise. This skill is only for data preparation and essence extraction, not for rendering the final presentation or form.
---

# Essence Workbench

Use this skill only for essence creation. The job here is to turn raw material into a durable structured essence that can later feed other workflows, but this skill does not handle presentation shaping or rendering.

The broader pipeline is:

`raw material -> structured essence -> presentation shape -> rendered delivery`

This skill owns only the `raw material -> structured essence` step.

## Core rules

- Essence is presentation-agnostic. It captures structure, meaning, evidence, and uncertainty without deciding how the material will later be delivered.
- Essence is destination-aware, not destination-driven. If the user already knows the likely final use, use that only to decide what must not be lost.
- Essence is a purposeful compression. Every essence keeps some structure sharp and lets other structure recede, so choose intentionally.
- One source can support more than one valid essence. If one essence would flatten important structure, create a small essence set instead of forcing a bad fit.
- The saved file is the editable source of truth, not a presentation artifact.

## Workflow

1. Run an optional downstream intent check.
2. Determine which essence type best preserves what matters in the source.
3. If the choice is not obvious, suggest the top 3 candidate essences based on the user's initial want plus the structure already present in the source.
4. Open the matching guide and any needed selection reference.
5. Draft and save the essence document as the source of truth.

The essence document is the editable source of truth. Keep it clean, explicit, and easy to patch.

## Step 0 - optional downstream intent check

Before selecting an essence, check whether the user already knows the likely final use.

Useful prompts:

- `Do you already know what this will probably become later?`
- `What would be most painful to lose while structuring this?`
- `Will this later need to support a visual, a talk, a reference doc, or something else?`

Use the answer only as a preservation hint.

- If the later goal is visual, preserve labels, groupings, entities, metrics, and comparison dimensions.
- If the later goal is conversational or audio, preserve tension, voice, questions, chronology, and transitions in meaning.
- If the later goal is instructional, preserve sequence, prerequisites, checks, and failure points.

Do not let downstream intent decide pacing, screen layout, narration style, slide beats, or file type here.

## Step 1 - choose the essence

Pick the shape that best matches what the user wants to preserve from the source material.

If the choice is fuzzy, read `references/selection-questions.md` first. If the user already knows the likely later use, read `references/downstream-intent.md` only to sharpen preservation priorities.

Start from two signals together:

- what structure already exists in the source
- what the user most wants to keep useful

If several essences seem plausible, do not dump the whole catalog. Recommend the top 3 candidates only.

For each candidate, give:

- the essence name
- one short reason it fits the source
- one short watchout about what it would flatten

Then recommend one default path.

Good shape:

```text
Top picks:
1. `claims-and-evidence` - best if the real job is checking what is supported.
   Watchout: weaker for chronology.
2. `summary` - best if you mainly want fast orientation.
   Watchout: flattens the evidence ledger.
3. `gaps-and-unknowns` - best if the unresolved parts are the real story.
   Watchout: weak as a general overview.

Recommended default: `claims-and-evidence`
```

This keeps choice manageable while still letting the user steer when the source could validly go more than one way.

## Step 2 - quick essence map

Use this table to choose quickly, then read the linked guide.

| Essence | What it contains | Vibe | Default shape | Guide |
|---|---|---|---|---|
| `summary` | Main point, key support, practical takeaway | Shortest faithful compression | Markdown | `references/summary.md` |
| `q-and-a-pairs` | Real questions and grounded answers | Browseable, searchable, teachable | YAML | `references/q-and-a-pairs.md` |
| `timeline` | Ordered events, causes, consequences | Chronological, investigative | YAML | `references/timeline.md` |
| `concepts-and-definitions` | Terms, meanings, relationships | Explanatory, domain-mapping | Markdown | `references/concepts-and-definitions.md` |
| `claims-and-evidence` | Assertions, support, counterpoints | Analytical, evidence-first | YAML | `references/claims-and-evidence.md` |
| `entities-and-relations` | Actors, objects, links between them | System map, graph-like | YAML | `references/entities-and-relations.md` |
| `steps-and-procedures` | Ordered instructions and checks | Operational, executable | Markdown | `references/steps-and-procedures.md` |
| `comparison` | Options, criteria, tradeoffs | Decision-support, side-by-side | YAML | `references/comparison.md` |
| `data-and-metrics` | Numbers, trends, units, periods | Quantitative, report-like | YAML | `references/data-and-metrics.md` |
| `narrative-arc` | Setup, tension, turning point, outcome | Story-shaped, meaning-first | Markdown | `references/narrative-arc.md` |
| `action-items` | Tasks, owners, dates, blockers | Operational follow-through | YAML | `references/action-items.md` |
| `arguments-and-counterarguments` | Positions, objections, rebuttals | Debate-ready, adversarial | Markdown | `references/arguments-and-counterarguments.md` |
| `patterns-and-themes` | Repeated ideas across examples | Synthetic, cross-source | Markdown | `references/patterns-and-themes.md` |
| `gaps-and-unknowns` | Missing info, contradictions, uncertainty | Honest, decision-risk aware | YAML | `references/gaps-and-unknowns.md` |
| `cause-and-effect-chains` | Mechanisms and domino sequences | Root-cause, causal | YAML | `references/cause-and-effect-chains.md` |
| `rules-and-constraints` | Requirements, prohibitions, invariants | Guardrail-focused, exacting | YAML | `references/rules-and-constraints.md` |
| `examples-and-cases` | Concrete instances and lessons | Illustrative, grounded | YAML | `references/examples-and-cases.md` |
| `sentiment-and-opinion` | Stances, tone, strength of feeling | Attitudinal, voice-aware | YAML | `references/sentiment-and-opinion.md` |
| `prerequisites-and-dependencies` | What must exist first, what unlocks what | Readiness and sequencing | YAML | `references/prerequisites-and-dependencies.md` |
| `taxonomy` | Categories and hierarchy | Classification, library-like | YAML | `references/taxonomy.md` |
| `document-structure` | Sections, nesting, chunk boundaries, source flow | Skeleton-first, document-shaped | Markdown | `references/document-structure.md` |
| `decisions-and-rationale` | Choices made, alternatives, tradeoffs, reasons | ADR-like, decision-tracing | YAML | `references/decisions-and-rationale.md` |
| `requirements-and-acceptance` | Requirements, success checks, failure conditions | Spec-like, testable | YAML | `references/requirements-and-acceptance.md` |
| `scenarios-and-use-cases` | Actors, triggers, goals, paths, edge cases | Situational, user-journey aware | YAML | `references/scenarios-and-use-cases.md` |
| `quotes-and-excerpts` | Verbatim passages, who said them, why they matter | Source-faithful, wording-sensitive | YAML | `references/quotes-and-excerpts.md` |
| `stakeholders-and-positions` | Who cares, what they want, tensions, leverage | Political, incentive-aware | YAML | `references/stakeholders-and-positions.md` |
| `observations-and-signals` | Findings, anomalies, symptoms, weak signals | Field-note, evidence-gathering | YAML | `references/observations-and-signals.md` |

Read only the guide you need.

## Step 3 - draft and save the essence

- Always separate `extraction` from `presentation`.
- Preserve source structure before optimizing for anyone's favorite output format.
- Prefer Markdown or YAML for the essence doc.
- Prefer YAML when the content is mostly records, entities, fields, timelines, or lists.
- Prefer Markdown when the content is mostly narrative, explanation, argument, or synthesis.
- If both help, use Markdown with short YAML frontmatter.
- Produce the smallest faithful editable document that preserves meaning, evidence, and uncertainty.
- If downstream intent is known, preserve the details that later work will need, but keep the file presentation-neutral.
- Include provenance, confidence, and open questions somewhere in the essence doc.
- Do not invent facts, smooth over contradictions, or silently fill missing fields.
- If the source is unclear, mark uncertainty explicitly instead of guessing.
- If a claim matters and the support is weak, reflect that weakness in the file.
- Save the essence as the durable source document, not as a presentation artifact.

## When to split into multiple essences

Do not force one essence to carry everything if the source clearly contains more than one important structure.

- A research report may need `summary`, `claims-and-evidence`, and `data-and-metrics`.
- A meeting may need `action-items` plus `gaps-and-unknowns`.
- A complex domain primer may need `concepts-and-definitions` plus `taxonomy`.
- A product discovery set may need `scenarios-and-use-cases`, `requirements-and-acceptance`, and `stakeholders-and-positions`.
- Interview material may need `quotes-and-excerpts`, `sentiment-and-opinion`, and `patterns-and-themes`.

If you split, keep each essence small and clean instead of making one giant mixed file.

## Default essence shape

Use this default unless the selected essence guide gives a better structure:

```markdown
---
essence: <type>
source_scope: <what was analyzed>
confidence: high|medium|low
---

# <working title>

## Core content
<structured content>

## Evidence or provenance
- <where it came from>

## Open questions
- <what is still missing or uncertain>
```

## Non-goals

- Do not decide presentation shape here.
- Do not choose file type, modality, or renderer here.
- Do not optimize for slides, dashboards, podcasts, infographics, or forms while extracting.
- Do not add layout notes, scene directions, animation cues, or presenter instructions.
- Do not collapse uncertainty just to make the document look neat.

## References

- Selection help: `references/selection-questions.md`
- Downstream preservation hints: `references/downstream-intent.md`
