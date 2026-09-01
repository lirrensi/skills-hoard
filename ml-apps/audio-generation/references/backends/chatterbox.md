# Backend: Chatterbox-Turbo (Resemble AI)

Load this guide when using Chatterbox as the TTS engine.

**When to pick this:** User wants production-grade TTS with zero-shot voice cloning, paralinguistic expression tags, and MIT licensing. Wins blind tests against ElevenLabs. 350M params, CPU viable.

**Repo:** https://github.com/resemble-ai/chatterbox | **PyPI:** https://pypi.org/project/chatterbox-tts/

## Setup

```bash
pip install chatterbox-tts
```

**Requirements:** Python 3.10+, ffmpeg (for audio I/O).

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows: download from https://ffmpeg.org/download.html
```

## Basic Usage

### Python API

```python
from chatterbox_tts import ChatterboxTTS

# Load model (downloads on first run)
model = ChatterboxTTS.from_pretrained()

# Generate with default voice (American English female)
audio = model.generate("Hello world, this is Chatterbox TTS.")
model.save(audio, "output.wav")

# Generate with voice cloning
audio = model.generate(
    "This will sound like the reference voice.",
    ref_audio_path="reference_clip.wav"
)
model.save(audio, "cloned.wav")
```

### Gradio demo

```python
import gradio as gr
from chatterbox_tts import ChatterboxTTS

model = ChatterboxTTS.from_pretrained()

def generate(text, ref_audio):
    audio = model.generate(text, ref_audio_path=ref_audio)
    return (model.sample_rate, audio)

demo = gr.Interface(fn=generate, inputs=["text", "audio"], outputs="audio")
demo.launch()
```

## Paralinguistic Tags

Chatterbox-Turbo's standout feature — insert emotion tags directly in text:

```python
# Emotional expressions
audio = model.generate("I can't believe it! [laugh] That's amazing!")
audio = model.generate("[sigh] I'm so tired of waiting.")
audio = model.generate("[chuckle] You won't believe what happened.")
audio = model.generate("[cough] Excuse me, where was I?")
```

Supported tags: `[laugh]`, `[sigh]`, `[chuckle]`, `[cough]`, and more.

## Voice Cloning

Zero-shot cloning — no fine-tuning needed:

```python
# Clone from a reference audio file (5+ seconds recommended)
audio = model.generate(
    "Welcome to the podcast. Today we discuss AI.",
    ref_audio_path="host_sample.wav"
)
```

### Without cloning

```python
# Default voice (no reference needed)
audio = model.generate("Hello world.")
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ref_audio_path` | Path to voice clone sample | None (default voice) |
| `exaggeration` | Emotion intensity | 0.5 |
| `cfg_weight` | Classifier-free guidance | 0.5 |

## Strengths

- MIT-licensed — fully open, commercial-friendly
- Zero-shot voice cloning
- Paralinguistic tags for emotional expression
- Wins blind tests against ElevenLabs
- On PyPI — simple `pip install`
- 96k+ monthly downloads
- Built-in audio watermarking
- CPU viable (faster with GPU)

## Limitations

- 350M params — heavier than Kokoro/Piper
- English only (multilingual version exists but separate)
- CPU inference is slower than GPU
- No SSML support
- No subtitle output
- Model download on first use
