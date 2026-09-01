---
name: edge-tts
description: >
  Generate complete, production-ready TTS (Text-to-Speech) scripts and CLI tools using
  edge-tts — Microsoft's neural voice engine with 400+ natural-sounding voices.
  Use this skill whenever the user wants to speak text aloud from the terminal/PowerShell,
  list or search voices, select voices by name/language/gender, control rate/volume/pitch,
  save speech to MP3/audio files, or pipe text into a speak command.
  Trigger for ANY request involving TTS, speech synthesis, say command, speak function,
  voice output, edge-tts, or audio from scripts — even small snippets. Always check
  installation first and prefer uv tool install for setup.
---

# PowerShell / Terminal TTS Skill (edge-tts)

Use **edge-tts** — free, neural-quality voices (400+), works from any terminal.
No Windows API nonsense. Sounds like a real human.

---

## Step 1 — Check & Install

**Always check if installed first:**
```powershell
Get-Command edge-tts -ErrorAction SilentlyContinue
```

**Install with uv (preferred):**
```powershell
uv tool install edge-tts
```

**Fallback with pip:**
```powershell
pip install edge-tts
```

This installs two executables: `edge-tts` (generate audio) and `edge-playback` (speak aloud).

---

## Step 2 — Basic Usage

**Speak aloud (use `edge-playback`, NOT `edge-tts --play`):**
```powershell
edge-playback --text "Hello world"
```

**Save to MP3:**
```powershell
edge-tts --text "Hello world" --write-media output.mp3
```

> ⚠️ `--play` flag does NOT exist on Windows. Always use `edge-playback` to speak aloud.

---

## Step 3 — Voices

**List ALL voices (400+):**
```powershell
edge-tts --list-voices
```

**Filter by language:**
```powershell
edge-tts --list-voices | Select-String "en-US"
edge-tts --list-voices | Select-String "Female"
```

**Recommended English neural voices:**
| Voice | Gender | Style |
|---|---|---|
| `en-US-AriaNeural` | Female | Natural, warm |
| `en-US-JennyNeural` | Female | Friendly |
| `en-US-GuyNeural` | Male | Natural |
| `en-GB-SoniaNeural` | Female | British |
| `en-GB-RyanNeural` | Male | British |

**Use a specific voice:**
```powershell
edge-playback --voice "en-US-AriaNeural" --text "Hi, I'm Aria!"
edge-tts --voice "en-US-AriaNeural" --text "Hi" --write-media aria.mp3
```

---

## Step 4 — Rate, Volume, Pitch

All adjustments use `+X%` or `-X%` string format:

```powershell
# Rate: default +0%, range roughly -50% to +100%
edge-playback --voice "en-US-AriaNeural" --rate "+20%" --text "Faster speech"
edge-playback --voice "en-US-AriaNeural" --rate "-30%" --text "Slower speech"

# Volume: default +0%
edge-playback --voice "en-US-AriaNeural" --volume "+50%" --text "Louder"

# Pitch: default +0Hz
edge-playback --voice "en-US-AriaNeural" --pitch "+10Hz" --text "Higher pitch"
```

---

## Deeper Reading

| Topic | File |
|---|---|
| Full Say.ps1 wrapper script with pipeline support | [`references/say-script.md`](references/say-script.md) |
| Gotchas (platform quirks, case sensitivity, etc.) | [`references/advanced.md`](references/advanced.md) |
