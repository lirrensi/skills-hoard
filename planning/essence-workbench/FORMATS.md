# Experience ontology

Three downstream choices, kept separate on purpose:

`source docs -> editable essence -> delivery format -> modality`

- `essence-workbench` handles Axis 1.
- `delivery-discovery` is an optional guidance step for Axes 2 and 3.
- Implementation skills happen only after the experience has been chosen.

---

## Axis 1 - content essence

What kind of knowledge structure gets extracted from the source docs.
Each essence type has a dedicated guide inside `essence-workbench/references/`.

| # | Name | What it extracts | Editable default | Guide |
|---|------|------------------|------------------|-------|
| E01 | Summary | Key points, main findings, TLDR - the irreducible core | Markdown | [summary](essence-workbench/references/summary.md) |
| E02 | Q&A pairs | Questions the docs answer, with grounded answers | YAML | [q-and-a-pairs](essence-workbench/references/q-and-a-pairs.md) |
| E03 | Timeline | Ordered events with dates, causes, consequences | YAML | [timeline](essence-workbench/references/timeline.md) |
| E04 | Concepts & definitions | Terms, ideas, how they relate to each other | Markdown | [concepts-and-definitions](essence-workbench/references/concepts-and-definitions.md) |
| E05 | Claims & evidence | Arguments made, data supporting them, counterpoints | YAML | [claims-and-evidence](essence-workbench/references/claims-and-evidence.md) |
| E06 | Entities & relations | People, orgs, places, things - and how they connect | YAML | [entities-and-relations](essence-workbench/references/entities-and-relations.md) |
| E07 | Steps & procedures | How to do something, in order | Markdown | [steps-and-procedures](essence-workbench/references/steps-and-procedures.md) |
| E08 | Comparison | Options side by side, tradeoffs, differences, recommendations | YAML | [comparison](essence-workbench/references/comparison.md) |
| E09 | Data & metrics | Numbers, tables, trends, statistics | YAML | [data-and-metrics](essence-workbench/references/data-and-metrics.md) |
| E10 | Narrative arc | Story with setup, conflict, resolution | Markdown | [narrative-arc](essence-workbench/references/narrative-arc.md) |
| E11 | Action items | Decisions made, tasks assigned, owners, deadlines | YAML | [action-items](essence-workbench/references/action-items.md) |
| E12 | Arguments & counterarguments | Positions taken, objections, rebuttals | Markdown | [arguments-and-counterarguments](essence-workbench/references/arguments-and-counterarguments.md) |
| E13 | Patterns & themes | Recurring ideas, motifs, structural patterns across sources | Markdown | [patterns-and-themes](essence-workbench/references/patterns-and-themes.md) |
| E14 | Gaps & unknowns | What is missing, unresolved, contradicted, or uncertain | YAML | [gaps-and-unknowns](essence-workbench/references/gaps-and-unknowns.md) |
| E15 | Cause & effect chains | What caused what, domino sequences, root cause analysis | YAML | [cause-and-effect-chains](essence-workbench/references/cause-and-effect-chains.md) |
| E16 | Rules & constraints | Policies, laws, requirements, invariants | YAML | [rules-and-constraints](essence-workbench/references/rules-and-constraints.md) |
| E17 | Examples & cases | Concrete instances that illustrate abstract points | YAML | [examples-and-cases](essence-workbench/references/examples-and-cases.md) |
| E18 | Sentiment & opinion | What people think, how they feel, tone of sources | YAML | [sentiment-and-opinion](essence-workbench/references/sentiment-and-opinion.md) |
| E19 | Prerequisites & dependencies | What requires what, learning order, unlock trees | YAML | [prerequisites-and-dependencies](essence-workbench/references/prerequisites-and-dependencies.md) |
| E20 | Taxonomy | Categories, hierarchies, classification systems | YAML | [taxonomy](essence-workbench/references/taxonomy.md) |
| E21 | Document structure | Sections, nesting, chunk boundaries, and source flow | Markdown | [document-structure](essence-workbench/references/document-structure.md) |
| E22 | Decisions & rationale | Choices made, alternatives considered, tradeoffs, reasons | YAML | [decisions-and-rationale](essence-workbench/references/decisions-and-rationale.md) |
| E23 | Requirements & acceptance | Requirements, acceptance criteria, success checks, failure conditions | YAML | [requirements-and-acceptance](essence-workbench/references/requirements-and-acceptance.md) |
| E24 | Scenarios & use cases | Actors, triggers, goals, main paths, edge cases, outcomes | YAML | [scenarios-and-use-cases](essence-workbench/references/scenarios-and-use-cases.md) |
| E25 | Quotes & excerpts | Verbatim passages, attribution, context, and why wording matters | YAML | [quotes-and-excerpts](essence-workbench/references/quotes-and-excerpts.md) |
| E26 | Stakeholders & positions | Stakeholders, interests, concerns, influence, stance, leverage | YAML | [stakeholders-and-positions](essence-workbench/references/stakeholders-and-positions.md) |
| E27 | Observations & signals | Findings, symptoms, anomalies, patterns noticed, confidence | YAML | [observations-and-signals](essence-workbench/references/observations-and-signals.md) |

---

## Axis 2 - delivery format

How the essence is shaped into a recognizable user experience.
Formats are narrative or interaction patterns, not file types.

| # | Name | What the user experiences |
|---|------|----------------------------|
| F01 | Article / document | Linear prose with sections, argument flow, and supporting detail |
| F02 | Briefing | Condensed executive-style update with stakes, context, and decisions |
| F03 | Slide deck | One idea per slide, presenter-ready, visually paced |
| F04 | Dialogue / podcast | Two or more voices in conversation, transitions, disagreement, chemistry |
| F05 | Interview | Host-guided Q&A with a subject-matter voice and prompted explanations |
| F06 | Flashcards | Discrete recall units for spaced repetition |
| F07 | Interactive quiz | Questions, scoring, feedback, retries, progression |
| F08 | Reference sheet | Dense quick-lookup format, tables, cheat-sheet structure |
| F09 | Walkthrough | Guided sequence that moves the user through steps, scenes, or milestones |
| F10 | Visual timeline | Chronological journey with pacing, eras, and notable turns |
| F11 | Diagram explainer | Relationships and flows made legible as a visual system |
| F12 | Dashboard | Metrics, comparisons, and status surfaced for scanning |
| F13 | Narrative / story | Characters, scenes, conflict, and resolution |
| F14 | Case study | Situation, intervention, outcome, and lessons learned |
| F15 | RPG / quest | Goals, choices, consequences, progression, and role-play framing |
| F16 | Simulation / game | Interactive system the user can operate and learn from |
| F17 | Social thread | Short serial posts built for scannability and momentum |
| F18 | Audiobook narration | Single-voice script paced for listening |
| F19 | Debate script | Structured opposing arguments, rebuttals, and tension |
| F20 | Tutorial / lesson | Guided instruction with checkpoints and learning progression |
| F21 | Comic / storyboard | Panel-by-panel sequence with dialogue and scene beats |
| F22 | Email / memo | Professional communication ready to send or circulate |
| F23 | FAQ page | Question-answer browsing experience |
| F24 | Explainer video script | Narration planned around visual beats and scene timing |

---

## Axis 3 - modality

What medium carries the chosen delivery format.
Modality is about how the work lands, not what the experience pattern is.

| # | Name | What it arrives as |
|---|------|--------------------|
| M01 | Markdown / plain text | Editable text file, notes page, transcript, or lightweight doc |
| M02 | Rich document / PDF | Paginated document optimized for reading or sharing |
| M03 | HTML page | Browser-based page, mini-site, or self-contained HTML artifact |
| M04 | Chat-style UI | Conversation bubbles, messenger-like transcript, or threaded viewer |
| M05 | Slides | Presentation frames, presenter notes, or slide browser |
| M06 | Diagram / canvas | SVG, Mermaid, whiteboard-like visual, or mapped system view |
| M07 | Audio | Spoken narration, voice performance, or generated speech |
| M08 | Video | Timed visuals plus narration, captions, or motion |
| M09 | Interactive app | Stateful UI with buttons, filters, scoring, or simulation controls |
| M10 | Printable one-pager | Poster, handout, cheat sheet, or leave-behind |
| M11 | Message body | Email, chat post, social post, or other in-channel text |

---

## HTML artifacts — a note

M03 (HTML page) covers a wide range. At its simplest, it's a styled page. At its most
powerful, it's a **self-contained HTML artifact** — a single file with embedded CSS and
JavaScript that can contain:

- Styled text, tables, and layouts
- Diagrams (Mermaid, Graphviz, SVG)
- Charts (Chart.js, D3, Plotly)
- Interactive state (filters, tabs, scoring, simulations)
- Reveal.js slide decks
- Mixed media (text + charts + diagrams + interactivity in one file)

An HTML artifact works offline, requires no build step, and opens in any browser.
It fills the gap between "static document" and "full app" — powerful enough to be
interactive, simple enough to be a single file.

**When to suggest HTML artifacts:**
- The content benefits from interactivity (filtering, exploring, clicking through)
- Multiple visual elements need to live together (text + charts + diagrams)
- The user wants something they can open, tweak, and re-open
- A static document would flatten the material, but a full app is overkill
- The format is a dashboard, quiz, simulation, interactive explainer, or visual guide

**When to suggest something simpler:**
- Content is purely text → Markdown or PDF
- Content is a single diagram → Mermaid/SVG directly
- Content is a single chart → Chart.js template
- User needs to edit in Word/Google Docs → PPTX/docx via document-generator

The HTML artifact is the most flexible output in the library. Use it when nothing
else is flexible enough.

---

## Example combinations

These are examples, not hard pairings:

| Essence | Format | Modality | Result |
|---------|--------|----------|--------|
| E03 timeline | F09 walkthrough | M05 slides | A paced project-history walkthrough |
| E03 timeline | F18 audiobook narration | M07 audio | History as a narrated listening experience |
| E04 concepts | F20 tutorial / lesson | M03 HTML page | Concepts taught as a guided lesson |
| E02 Q&A pairs | F04 dialogue / podcast | M04 chat-style UI | Two hosts work through grounded questions |
| E11 action items | F15 RPG / quest | M03 HTML page | Meeting follow-up as a quest log |
| E09 data | F12 dashboard | M09 interactive app | Metrics explored through cards and filters |
| E10 narrative arc | F17 social thread | M11 message body | Research retold as a serial thread |
| E05 claims & evidence | F19 debate script | M07 audio | Two voices argue both sides of a position |
| E07 steps & procedures | F20 tutorial / lesson | M03 HTML page | SOP transformed into an interactive lesson |
| E01 summary | F02 briefing | M02 rich document / PDF | Concise leadership-ready briefing |
| E14 gaps & unknowns | F22 email / memo | M11 message body | "Here is what we still do not know" update |
| E08 comparison | F08 reference sheet | M03 HTML page | Self-contained filterable comparison artifact |
| E02 Q&A pairs | F07 interactive quiz | M03 HTML page | Stateful quiz with scoring and feedback |
| E09 data | F12 dashboard | M03 HTML page | Interactive dashboard artifact with filters and charts |
| E07 steps & procedures | F16 simulation / game | M03 HTML page | Step-through simulation with state tracking |
| E27 observations & signals | F11 diagram explainer | M03 HTML page | Interactive explainer with clickable nodes and detail panels |

---

## How to use this file

- Use Axis 1 to decide what the source materially contains.
- Use Axis 2 to decide the experience pattern.
- Use Axis 3 to decide how it lands.
- Use `delivery-discovery` when the user is unsure about Axes 2 and 3.
- Let implementation skills worry about tools only after the experience choice is clear.

## Capability-aware discovery

When suggesting formats and modalities, keep three buckets in mind:

- `Recommended now`: strong fit for the essence and plausible with the current workspace.
- `Good with setup`: a strong experiential fit, but the environment is missing key capabilities.
- `Possible but awkward`: technically possible, but a weak match for either the essence or the current stack.
