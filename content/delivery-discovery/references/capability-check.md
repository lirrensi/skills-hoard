# Capability check

This skill is capability-aware, but capability checking should stay lightweight.

The goal is not to plan production in detail. The goal is to keep recommendations honest.

## Recommendation buckets

- `Recommended now`: the idea fits the essence and the workspace already looks able to produce it.
- `Good with setup`: the idea fits well, but a key capability is missing.
- `Possible but awkward`: the idea is technically possible, but the fit or feasibility is poor.

## How to check quietly

1. Look for obvious workspace signals first.
2. Check only the capabilities that matter for the likely modalities.
3. Ask the user only if the capability picture is still ambiguous.
4. Report capability gaps in plain language, without turning discovery into a setup lecture.

## Common modality checks

| Modality | What to look for |
|---|---|
| `markdown / plain text` | almost always available |
| `rich document / PDF` | Pandoc, document templates, PDF export path, or an established doc workflow |
| `HTML page` | Node, Python, static site tooling, or an existing web app structure |
| `chat-style UI` | HTML capability plus a lightweight viewer or web stack |
| `slides` | Marp, Reveal, PowerPoint generation path, or a slide-friendly markdown workflow |
| `diagram / canvas` | Mermaid, SVG workflow, diagram libraries, or existing visual tooling |
| `audio` | TTS tool or voice workflow, plus audio assembly support such as `ffmpeg` |
| `video` | `ffmpeg`, image or HTML capture path, and usually an audio path too |
| `interactive app` | browser app stack, JS runtime, or an obvious interactive frontend path |
| `printable one-pager` | print CSS, PDF export, or a document layout path |
| `message body` | always available |

## Useful example checks

- Runtime checks: `python --version`, `node --version`
- Audio checks: `edge-tts --version`, `ffmpeg -version`
- Slide checks: `marp --version`
- Workspace checks: look for an existing web app, document pipeline, or media-generation scripts

Treat any check result as a local snapshot, not as a permanent truth.

## How to talk about gaps

- If the format is strong but the modality is blocked, say that clearly.
- Offer the nearest available alternative first.
- Mention missing capability only at the level needed to decide.

Example:

- `audio podcast` is a good experiential fit, but this workspace does not currently show a TTS path.
- `podcast transcript` or `chat-style podcast viewer` are available lower-friction alternatives.
- If the user still wants audio, the next step is enabling a TTS or recorded-voice workflow.

## Ask only when needed

If the environment is unclear, ask one narrow question such as:

`Do we already have a way in this workspace to generate audio or video, or should I treat those as setup-required options?`
