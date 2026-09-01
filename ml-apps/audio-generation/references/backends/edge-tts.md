# Backend: edge-tts

Load this guide when using edge-tts as the TTS engine.

**When to pick this:** User has internet, wants zero setup, needs 400+ voices across many languages, or wants subtitle (SRT) output. Cloud-based — no local compute needed.

## Setup

```bash
pip install edge-tts

# Or for CLI-only (isolated install):
pipx install edge-tts
```

**Requirements:** Python 3.7+, internet connection.

## Basic Usage

### CLI

```bash
# Generate audio + subtitles
edge-tts --text "Hello, world!" --write-media hello.mp3 --write-subtitles hello.srt

# From a file
edge-tts --file script.txt --write-media output.mp3

# Play back immediately (requires mpv, except on Windows)
edge-playback --text "Hello, world!"
```

### Python API

```python
import edge_tts
import asyncio

async def generate():
    communicate = edge_tts.Communicate("Hello, world!", "en-US-AriaNeural")
    await communicate.save("output.mp3")

asyncio.run(generate())
```

## Voice Selection

```bash
# List all voices with gender and personality
edge-tts --list-voices
```

Output format:
```
Name                          Gender  ContentCategories  VoicePersonalities
---------------------------------  --------  ---------------------  --------------------------------------
af-ZA-AdriNeural                 Female    General                Friendly, Positive
en-US-AriaNeural                 Female    General                Friendly, Positive
en-US-GuyNeural                  Male      General                Friendly, Positive
```

```bash
# Filter by language
edge-tts --list-voices | grep "en-"
edge-tts --list-voices | grep "es-"
```

See `voices.md` for the full catalog and selection guidelines.

## Delivery Parameters

| Parameter | Flag | Range | Default |
|-----------|------|-------|---------|
| Speed | `--rate` | `-100%` to `+200%` | `+0%` |
| Pitch | `--pitch` | `-50Hz` to `+50Hz` | `+0Hz` |
| Volume | `--volume` | `-100%` to `+100%` | `+0%` |

```bash
# Calm narration
edge-tts --text "Relax and breathe." --voice en-US-AriaNeural \
  --rate="-20%" --write-media calm.mp3

# Energetic
edge-tts --text "Let's go!" --voice en-US-TonyNeural \
  --rate="+20%" --write-media energetic.mp3
```

## Chunking for Long Text

edge-tts handles chunks well but keep under ~5,000 characters per call:

```bash
# Split and generate (Python helper)
python3 -c "
text = open('long_text.txt').read()
paragraphs = text.split('\n\n')
chunk = ''
chunk_num = 1
for p in paragraphs:
    if len(chunk) + len(p) > 4500:
        open(f'chunk_{chunk_num:03d}.txt', 'w').write(chunk.strip())
        chunk_num += 1
        chunk = p + '\n\n'
    else:
        chunk += p + '\n\n'
if chunk.strip():
    open(f'chunk_{chunk_num:03d}.txt', 'w').write(chunk.strip())
"

for f in chunk_*.txt; do
  edge-tts --file "$f" --voice en-US-AriaNeural --write-media "${f%.txt}.mp3"
done
```

## Strengths

- Zero local compute — runs on anything with internet
- 400+ voices across 70+ languages
- Subtitle (SRT) output for syncing
- SSML-style rate/pitch/volume control
- Consistent quality (Microsoft Azure neural voices)
- 1M+ monthly downloads on PyPI — battle-tested

## Limitations

- Requires internet connection
- No voice cloning
- No offline use
- Subject to rate limits (rarely hit in practice)
- Latency depends on network speed
