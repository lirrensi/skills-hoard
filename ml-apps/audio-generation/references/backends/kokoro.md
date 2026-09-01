# Backend: Kokoro (Kokoro-82M)

Load this guide when using Kokoro as the TTS engine.

**When to pick this:** User wants local/offline generation on CPU with high quality. 82M params, Apache-licensed, delivers comparable quality to larger models while being significantly faster. The go-to local TTS.

**Repo:** https://github.com/hexgrad/kokoro | **Model:** https://huggingface.co/hexgrad/Kokoro-82M

## Setup

```bash
pip install kokoro>=0.9.4 soundfile
```

**espeak-ng** is required for English OOD fallback and some non-English languages:

```bash
# Linux
sudo apt-get install espeak-ng

# macOS
brew install espeak-ng

# Windows: download MSI from https://github.com/espeak-ng/espeak-ng/releases
# Download the *.msi from Latest release, run the installer
```

**Requirements:** Python 3.9–3.12 (3.13+ not currently supported for some packages).

## Basic Usage

```python
from kokoro import KPipeline
import soundfile as sf

# Initialize pipeline
# 🇺🇸 'a' => American English, 🇬🇧 'b' => British English
# 🇪🇸 'e' => Spanish, 🇫🇷 'f' => French, 🇮🇳 'h' => Hindi
# 🇮🇹 'i' => Italian, 🇯🇵 'j' => Japanese (pip install misaki[ja])
# 🇧🇷 'p' => Brazilian Portuguese, 🇨🇳 'z' => Mandarin Chinese (pip install misaki[zh])
pipeline = KPipeline(lang_code='a')

# Generate
text = "Hello world, this is Kokoro TTS."
generator = pipeline(text, voice='af_heart')

for i, (gs, ps, audio) in enumerate(generator):
    sf.write(f'{i}.wav', audio, 24000)  # 24kHz output
```

## Voice Selection

Kokoro uses named voice tensors. Common English voices:

| Voice | Style | Best for |
|-------|-------|----------|
| `af_heart` | Warm female | General, narration |
| `af_bella` | Clear female | Professional |
| `af_sarah` | Soft female | Calm, gentle |
| `af_nicole` | Expressive female | Podcasts |
| `am_adam` | Natural male | Conversational |
| `am_michael` | Deeper male | Authoritative |
| `bf_emma` | British female | Elegant narration |
| `bm_lewis` | British male | Documentary |
| `bm_george` | British male | Warm, measured |

Full list: check the [Hugging Face model page](https://huggingface.co/hexgrad/Kokoro-82M) or load voices from the pipeline.

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `lang_code` | Language code | Required |
| `voice` | Voice name or tensor | Required |
| `speed` | Playback speed | `1.0` |
| `split_pattern` | Regex for splitting text | `r'\n+'` |

```python
# Slower narration
generator = pipeline(text, voice='af_heart', speed=0.85)

# Faster delivery
generator = pipeline(text, voice='am_adam', speed=1.2)
```

## Advanced Usage

```python
from kokoro import KPipeline
import soundfile as sf
import torch

pipeline = KPipeline(lang_code='a')

# Long text with automatic splitting
text = """
First paragraph of content here.

Second paragraph continues the story.

Third paragraph wraps things up.
"""

generator = pipeline(
    text,
    voice='af_heart',
    speed=1,
    split_pattern=r'\n+'
)

for i, (gs, ps, audio) in enumerate(generator):
    print(f"Segment {i}: {gs[:50]}...")
    sf.write(f'segment_{i:03d}.wav', audio, 24000)
```

### Load custom voice tensor

```python
voice_tensor = torch.load('path/to/voice.pt', weights_only=True)
generator = pipeline(text, voice=voice_tensor, speed=1)
```

## macOS Apple Silicon GPU Acceleration

On M1/M2/M3/M4 devices, enable GPU acceleration:

```bash
PYTORCH_ENABLE_MPS_FALLBACK=1 python your_script.py
```

## Conda Environment (if dependency issues)

```yaml
name: kokoro
channels:
  - defaults
dependencies:
  - python==3.9
  - libstdcxx~=12.4.0  # Needed for espeak loading
  - pip:
      - kokoro>=0.3.1
      - soundfile
      - misaki[en]
```

## Strengths

- Runs well on CPU — near real-time on modern machines
- High natural quality for its size (82M params)
- No internet required after initial model download
- Apache-licensed weights — deploy anywhere
- 8+ language support
- Simple Python API
- Active community (6k+ GitHub stars)

## Limitations

- Needs espeak-ng installed for full functionality
- No voice cloning (use Pocket TTS for that)
- No SSML support (rate/pitch via parameters only)
- No subtitle (SRT) output
- Python 3.13+ has some compatibility issues
- Model download on first use (~200MB)
