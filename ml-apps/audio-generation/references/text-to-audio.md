# Text-to-Audio

Load this guide when the user wants to turn any text into spoken audio with a single voice.

**Backend-agnostic:** This guide covers the workflow. For engine-specific commands, read the appropriate backend file from `backends.md`.

## Step 1: Choose a Backend

Read `backends.md` if the user hasn't specified an engine. Key questions:
- Offline required? → Kokoro, Pocket TTS, MeloTTS, or Piper
- Voice cloning needed? → Pocket TTS
- Simplest setup? → edge-tts
- Lowest resource usage? → Piper

Once chosen, read the backend file for its specific API/CLI.

## Step 2: Pick a Voice

If the user doesn't specify, pick based on context:

| Context | Style needed | See |
|---------|-------------|-----|
| General / versatile | Natural, warm | `voices.md` quick picks |
| Professional / news | Clear, authoritative | `voices.md` by content type |
| Casual / friendly | Conversational, upbeat | `voices.md` by content type |
| Match content language | Correct language | `voices.md` language sections |

Each backend has its own voice naming — check the backend file for available voices.

## Step 3: Set Delivery Parameters

Adjust rate/pitch/volume based on content type:

| Content type | Rate | Why |
|-------------|------|-----|
| Narration / long reads | Slower (-10% to -15%) | Helps comprehension |
| Conversational / podcast | Normal (+0%) | Natural pace |
| Promos / ads | Faster (+10% to +20%) | Energy |
| Meditation / calm | Slow (-20%), lower pitch | Relaxation |
| Children's content | Normal, higher pitch | Brightness |

Parameter syntax varies by backend — check the backend file.

## Step 4: Generate

Each backend has its own generation command. See:
- `backends/edge-tts.md` — CLI with `--text`, `--file`, `--voice`, `--rate`
- `backends/kokoro.md` — Python API with `KPipeline`
- `backends/pocket-tts.md` — Python API with voice cloning support
- `backends/melotts.md` — Python API with multilingual support
- `backends/piper.md` — CLI pipe-based, ultra-lightweight

## Step 5: Post-Process

All backends benefit from post-processing with ffmpeg:

```bash
# Normalize loudness
ffmpeg -i output.wav -af loudnorm output_normalized.mp3

# Trim silence
ffmpeg -i output.wav -af silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB output_trimmed.wav

# Add fade in/out
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 output.wav)
FADE_OUT=$(echo "$DURATION - 2" | bc)
ffmpeg -i output.wav -af "afade=t=in:st=0:d=2,afade=t=out:st=$FADE_OUT:d=2" output_faded.mp3
```

Full ffmpeg recipes: see `ffmpeg-audio.md`.

## Handling Long Text

All backends benefit from chunking. General approach:

1. Split at paragraph boundaries (never mid-sentence)
2. Generate each chunk separately
3. Concatenate with ffmpeg (see `ffmpeg-audio.md`)

Chunk size varies by backend — check the backend file for recommended limits.

## Quality Checks

- [ ] Voice matches content tone
- [ ] No mid-sentence cuts or truncation
- [ ] Volume is consistent (normalized)
- [ ] Pace feels natural for the content type
- [ ] Output format matches requirements (MP3 vs WAV)

```bash
# Check duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output.mp3

# Check volume levels
ffmpeg -i output.mp3 -af volumedetect -f null /dev/null 2>&1 | grep max_volume
```
