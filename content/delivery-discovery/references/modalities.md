# Modalities

Modality is the medium that carries a chosen delivery format.
It is separate from the format itself.

Example:

- `dialogue / podcast` is a format.
- `audio` and `chat-style UI` are modalities.

## Modality guide

| Modality | What it feels like | Good for | Common penalties | Typical capability signals |
|---|---|---|---|---|
| `markdown / plain text` | Direct, editable, low-friction | transcripts, briefings, FAQs, lessons | can feel plain or underdesigned | almost always available |
| `rich document / PDF` | finished, shareable, paginated | briefings, case studies, formal docs | harder to iterate if it becomes the source of truth | doc or PDF generation path |
| `HTML page` | browseable, styled, flexible | lessons, dashboards, timelines, FAQ pages | easy to overbuild | static web or app path |
| `chat-style UI` | conversational, turn-based, social | podcasts as transcripts, interviews, Q&A | can trivialize serious material if used carelessly | HTML or web UI path |
| `slides` | paced, presentational, one beat at a time | walkthroughs, briefings, timelines | weak for dense nuance unless carefully staged | slide generator or presentation path |
| `diagram / canvas` | spatial, relational, map-like | systems, dependencies, entities, taxonomies | labels can replace explanation if overused | Mermaid, SVG, or drawing path |
| `audio` | human-paced, ambient, listenable | podcasts, narration, guided explainers | hard to scan; source grounding must be handled carefully | TTS, voice recording, or audio editing path |
| `video` | timed, multimodal, cinematic | explainers, storyboards, narrated walkthroughs | expensive to produce well; easy to oversell | video assembly plus visual asset path |
| `interactive app` | exploratory, participatory, stateful | dashboards, quizzes, simulations, games | more engineering overhead than static outputs | app stack or browser runtime |
| `printable one-pager` | concise, durable, handout-like | reference sheets, taxonomies, rules | very limited space for nuance | print-friendly layout path |
| `message body` | in-channel, lightweight, immediate | email updates, memos, threads, stakeholder notes | constrained by channel conventions and length | almost always available |

## Selection hints

- Choose `markdown / plain text` when editability or speed matters most.
- Choose `HTML page` when browsing, layering, or interaction matters.
- Choose `slides` when the material benefits from pacing and presentation rhythm.
- Choose `audio` when listening is part of the value, not just novelty.
- Choose `video` only when visuals genuinely add meaning.
- Choose `interactive app` when the user should explore, manipulate, or answer.

## Pairing reminders

- A strong format can survive across modalities.
- Some pairings are better as transcripts or scripts before they become media.
- If the workspace cannot support the most obvious modality, offer the nearest lower-friction version instead.
