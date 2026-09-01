---
name: audio-generation
description: >
  Use this skill whenever the user wants to generate audio from text, create podcast
  episodes, convert articles or long-form content into narrated audio, or produce any
  kind of spoken-word audio track. Triggers on phrases like "text to speech", "make
  this into audio", "create a podcast", "read this article aloud", "narrate this",
  "audiobook", "voice over", "TTS", "generate speech", "audio from text", or any
  request where text needs to become spoken audio. Covers three domains: general
  text-to-audio generation, multi-voice podcast production, and long-read narration.
---

# Audio Generation

## Route First

| User need | Read next |
|-----------|-----------|
| Choose a TTS engine — compare backends, pick based on hardware/needs | `references/backends.md` |
| Turn any text into spoken audio — single voice, short or long | `references/text-to-audio.md` |
| Produce a multi-voice podcast episode from a script or source material | `references/podcast.md` (technical) + `references/podcast-principles.md` (editorial) |
| Convert an article, document, or long-form text into narrated audio | `references/long-reads.md` (technical) + `references/long-read-principles.md` (editorial) |
| Audio assembly, concatenation, normalization, fades, format conversion | `references/ffmpeg-audio.md` |
| Choose a voice — catalog, language coverage, style matching | `references/voices.md` |

If the request is ambiguous, ask: *"Is this a single voice reading, a multi-person conversation, or a narration of existing content?"*

## Mental Model

- **TTS backends** are pluggable. Pick the right one for the user's environment — see `references/backends.md` for the decision flowchart. Options range from cloud (edge-tts) to local CPU (Kokoro, Piper, MeloTTS, Pocket TTS).
- **ffmpeg** is the audio workbench. Concatenation, trimming, format conversion, fades, mixing, normalization — all post-production lives here.
- **pydub** (optional) is for Python-level audio control when ffmpeg CLI isn't enough.

## Core Rules

1. **Pick the right backend.** Don't default blindly — check the user's hardware, offline needs, and voice cloning requirements. See `references/backends.md`.
2. **Normalize loudness** on every final deliverable (`ffmpeg -af loudnorm`).
3. **Default output: MP3** at 24kHz mono. Use WAV only if the user needs lossless or the backend outputs WAV natively.
4. **Chunk long text** at paragraph boundaries, never mid-sentence. Chunk size depends on backend (see backend-specific docs).
5. **Name files descriptively:** `podcast-episode-1.mp3`, `article-narration.mp3`, `intro-audio.mp3`.

## Dependencies

- **Required**: one TTS backend (see `references/backends.md`), `ffmpeg` (system install)
- **Optional**: `pydub` (`pip install pydub`), `markitdown` (`pip install markitdown`)
