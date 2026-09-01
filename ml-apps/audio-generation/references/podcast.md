# Podcast Creation

Load this guide when the user wants to produce a multi-voice podcast episode — dialogue, interview, debate, or conversation format.

**Prerequisite:** Read `podcast-principles.md` first for the editorial rules on turning source material into natural conversation. This file handles the technical pipeline; that file handles the scriptwriting.

## Workflow Overview

1. Understand the format (speakers, topic, tone, length)
2. Generate or accept a script with speaker labels
3. Assign distinct voices to each speaker
4. Generate per-speaker audio segments
5. Assemble the episode with pauses and transitions
6. Normalize and deliver

## Step 1: Understand the Format

Ask (or infer) these details:

| Question | Why it matters |
|----------|----------------|
| How many speakers? | Determines voice assignment |
| What's the topic / source material? | Shapes the script content |
| What tone? (casual, interview, debate, educational) | Affects language style |
| Target length? | Guides script length (~150 words/minute spoken) |
| Source material provided? | If yes, script discusses it — doesn't read it aloud |

### Rough length guide

| Target duration | Approximate word count |
|-----------------|----------------------|
| 5 minutes | ~750 words |
| 10 minutes | ~1,500 words |
| 20 minutes | ~3,000 words |
| 30 minutes | ~4,500 words |

## Step 2: Script Format

Use speaker labels. Each line is one speaker's turn.

**For the editorial principles** (manufactured friction, chunking, analogy engine, emotional pacing), see `podcast-principles.md`. Below is the structural format.

```
HOST: Welcome to the show. Today we're talking about renewable energy.
GUEST: Thanks for having me. It's a topic I'm passionate about.
HOST: So let's start with the basics — what exactly is solar energy?
GUEST: Solar energy is radiation from the sun that can produce heat. It's the most abundant energy source on Earth.
HOST: And how do we actually capture it?
GUEST: Through photovoltaic cells — the panels you see on rooftops. They convert sunlight directly into electricity.
```

### Script writing guidelines

- **Conversational language**: use contractions ("it's", "don't", "we're")
- **Short segments**: 1–4 sentences per speaker turn. Long monologues sound robotic.
- **Natural transitions**: "So...", "Right, and...", "That's interesting because...", "Speaking of which..."
- **Back-channeling**: add brief reactions — "Exactly", "Right", "Sure", "Mm-hmm"
- **Filler words sparingly**: "you know", "I mean", "sort of" — one or two per minute, not every sentence
- **Source material**: script should *discuss* it, never read it verbatim. Paraphrase, react, question.

### If the user provides source material

Don't just read the article aloud as two voices. Instead:
1. Extract key points from the source
2. Frame them as a conversation — one person explains, the other asks questions or reacts
3. Add opinions, analogies, real-world connections
4. Include moments of agreement, surprise, or mild disagreement

## Step 3: Voice Assignment

Each speaker needs a noticeably different voice. Pick from different genders or distinctly different styles.

**Backend-agnostic:** Voice names vary by engine. See `voices.md` for style guidance, then check your backend file for the matching voice codes.

### Style targets (map to your backend)

| Role | Style needed | edge-tts example | Kokoro example |
|------|-------------|-----------------|----------------|
| Host (male) | Clear, professional | `en-US-GuyNeural` | `am_adam` |
| Host (female) | Warm, natural | `en-US-AriaNeural` | `af_heart` |
| Guest (male) | Deeper, thoughtful | `en-US-ChristopherNeural` | `am_michael` |
| Guest (female) | Conversational, energetic | `en-US-JennyNeural` | `af_bella` |

**Rule of thumb**: if two voices sound similar to you, they'll sound identical to the listener. Err on the side of contrast.

For more options: see `voices.md`. For backend-specific voice lists: see `backends/<engine>.md`.

## Step 4: Generate Per-Speaker Audio

Split the script by speaker, then generate each segment with your chosen backend.

### Parse script into per-speaker files

```python
import re

lines = open('script.txt').readlines()
current_speaker = None
current_text = []
seg_num = 0

for line in lines:
    match = re.match(r'^(\w+):\s*(.*)', line)
    if match:
        if current_speaker and current_text:
            seg_num += 1
            open(f'seg_{seg_num:03d}_{current_speaker}.txt', 'w').write(' '.join(current_text))
        current_speaker = match.group(1).lower()
        current_text = [match.group(2)]
    elif current_speaker:
        current_text.append(line.strip())

if current_speaker and current_text:
    seg_num += 1
    open(f'seg_{seg_num:03d}_{current_speaker}.txt', 'w').write(' '.join(current_text))
```

### Generate with your backend

Each backend has its own command. See the backend file for specifics:

- **edge-tts**: `edge-tts --file seg_001_host.txt --voice en-US-GuyNeural --write-media seg_001_host.mp3`
- **Kokoro**: Python API — see `backends/kokoro.md`
- **Pocket TTS**: Python API with optional voice cloning — see `backends/pocket-tts.md`
- **MeloTTS**: Python API — see `backends/melotts.md`
- **Piper**: `cat seg_001_host.txt | piper --model en_US-lessac-medium --output_file seg_001_host.wav`

The assembly steps below are the same regardless of backend.

## Step 5: Assemble the Episode

### Generate silence files

```bash
# Short pause between speakers (0.4s)
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 0.4 -q:a 9 pause_short.mp3

# Longer pause for topic transitions (1.0s)
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 1.0 -q:a 9 pause_long.mp3
```

### Build the file list

```bash
# Concatenate segments with pauses between speakers
python3 -c "
import glob, re

segments = sorted(glob.glob('seg_*.mp3'))
with open('filelist.txt', 'w') as f:
    for i, seg in enumerate(segments):
        f.write(f\"file '{seg}'\n\")
        if i < len(segments) - 1:
            # Check if next segment is a different speaker
            curr_speaker = re.search(r'_(\w+)\.mp3$', seg).group(1)
            next_speaker = re.search(r'_(\w+)\.mp3$', segments[i+1]).group(1)
            if curr_speaker != next_speaker:
                f.write(\"file 'pause_short.mp3'\n\")
            else:
                f.write(\"file 'pause_short.mp3'\n\")
"
```

### Concatenate and normalize

```bash
# Concatenate
ffmpeg -f concat -safe 0 -i filelist.txt -c copy episode_raw.mp3

# Normalize loudness
ffmpeg -i episode_raw.mp3 -af loudnorm episode_final.mp3
```

### Optional: add intro/outro music

```bash
# Mix intro music with voice (music fades under voice)
ffmpeg -i intro_music.mp3 -i first_segment.mp3 \
  -filter_complex "[0]afade=t=out:st=3:d=2[bg];[bg][1]amix=inputs=2:duration=first:dropout_transition=2" \
  intro_mixed.mp3
```

## Step 6: Quality Checks

Before delivering, verify:

- [ ] Each speaker sounds distinct
- [ ] Pauses feel natural (not too short, not too long)
- [ ] No mid-sentence cuts
- [ ] Volume is consistent throughout
- [ ] Total duration matches target (±10%)

```bash
# Check duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 episode_final.mp3

# Check for clipping or volume issues
ffmpeg -i episode_final.mp3 -af volumedetect -f null /dev/null 2>&1 | grep -E "max_volume|mean_volume"
```

## Common Patterns

### Interview style (host asks, guest answers)
Keep host segments short (questions), guest segments can be longer (answers). Host reacts between answers.

### Debate style (two opposing views)
Give each speaker a clear stance. Use phrases like "But here's the thing...", "I disagree because...", "That's fair, however..."

### Educational / explainer
One voice explains, the other asks clarifying questions. The "student" voice keeps the pace grounded.
