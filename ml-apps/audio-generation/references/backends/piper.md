# Backend: Piper TTS

Load this guide when using Piper as the TTS engine.

**When to pick this:** User needs the lightest, fastest, most reliable local TTS. Runs on anything — including Raspberry Pi. Perfect for batch rendering, overnight jobs, or low-resource environments. The "it just works" option.

**Repo (active):** https://github.com/OHF-Voice/piper1-gpl (Open Home Foundation)
**Old repo (archived):** https://github.com/rhasspy/piper — development has moved to `piper1-gpl`

## Setup

```bash
pip install piper-tts
```

**Requirements:** Python 3.x, espeak-ng (bundled in the pip package for most platforms).

## Basic Usage

### CLI

```bash
# Pipe text to piper
echo "Hello world" | piper --model en_US-lessac-medium --output_file output.wav

# From a file
cat script.txt | piper --model en_US-lessac-medium --output_file output.wav
```

### Python API

```python
from piper import PiperVoice
import wave

# Load model (downloads on first use)
voice = PiperVoice.load("en_US-lessac-medium")

# Generate
with wave.open("output.wav", "wb") as wav_file:
    voice.synthesize("Hello world, this is Piper TTS.", wav_file)
```

## Voice Models

Piper uses pre-trained ONNX voice models. Browse available voices:
- Voice list: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/VOICES.md
- Samples: https://rhasspy.github.io/piper-samples

Common models:

| Model | Quality | Size | Style |
|-------|---------|------|-------|
| `en_US-lessac-medium` | Good | ~60MB | Clear, professional female |
| `en_US-libritts_r-medium` | Higher | ~100MB | Natural, expressive |
| `en_US-ryan-medium` | Good | ~60MB | Male, conversational |
| `en_GB-alan-medium` | Good | ~60MB | British male |
| `de_DE-thorsten-medium` | Good | ~60MB | German male |
| `es_ES-davefx-medium` | Good | ~60MB | Spanish male |

Models are downloaded automatically on first use, or manually from Hugging Face.

## Parameters

| Parameter | Flag | Description | Range |
|-----------|------|-------------|-------|
| `--model` | Required | Voice model name | See voice list |
| `--output_file` | Optional | Output path | Any path |
| `--length_scale` | Optional | Speaking rate | `0.5` (fast) to `2.0` (slow) |
| `--noise_scale` | Optional | Voice variation | `0.0` (stable) to `1.0` (expressive) |
| `--sentence_silence` | Optional | Pause between sentences | Seconds, default `0.5` |

```bash
# Slower narration
echo "Hello world" | piper --model en_US-lessac-medium \
  --length_scale 1.3 --output_file calm.wav

# More expressive
echo "Hello world" | piper --model en_US-lessac-medium \
  --noise_scale 0.8 --output_file expressive.wav
```

## Web Server

Piper includes an HTTP server for serving TTS over the network:

```bash
# See docs: https://github.com/OHF-Voice/piper1-gpl/blob/main/docs/API_HTTP.md
```

## Batch Rendering

Piper excels at batch jobs:

```bash
# Render each line as a separate file
num=0
while IFS= read -r line; do
  echo "$line" | piper --model en_US-lessac-medium --output_file "seg_$(printf '%03d' $num).wav"
  ((num++))
done < script.txt
```

## Projects Using Piper

- Home Assistant (voice assistant TTS)
- NVDA (screen reader for visually impaired)
- LocalAI
- Open Voice Operating System
- Many Raspberry Pi projects

## Strengths

- Extremely lightweight — runs on Raspberry Pi
- Fastest generation speed of all local backends
- Rock solid, zero drama, "just works"
- Great for batch/overnight rendering
- Small model sizes (~60MB per voice)
- Wide language support via community models
- No GPU needed at all
- Active development under Open Home Foundation (GPL-3.0)

## Limitations

- Lower expressiveness than Kokoro or Pocket TTS
- No voice cloning
- No SSML support
- Quality noticeably below neural cloud voices
- Voice selection limited to available pre-trained models
- Can sound slightly robotic on longer content
- Original repo archived — use `OHF-Voice/piper1-gpl`
