# Backend: NeuTTS Air (Neuphonic)

Load this guide when using NeuTTS Air as the TTS engine.

**When to pick this:** User wants super-realistic on-device TTS with instant voice cloning, running on CPU, phones, or even Raspberry Pi. 0.5B params, GGUF quantized for efficiency. Privacy-first, fully local.

**Repo:** https://github.com/neuphonic/neutts | **HuggingFace:** https://huggingface.co/neuphonic/neutts-air

## Setup

```bash
# Clone the repo
git clone https://github.com/neuphonic/neutts-air.git
cd neutts-air

# Install eSpeak (required dependency)
# Linux
sudo apt install espeak

# macOS
brew install espeak

# Windows: download from https://github.com/espeak-ng/espeak-ng/releases

# Install Python dependencies
pip install -r requirements.txt
```

**Requirements:** Python 3.11+, ~2-3GB disk for model weights. Optional: CUDA GPU for faster inference (CPU works fine).

### macOS eSpeak path fix

If espeak isn't found, add at the top of your script:

```python
from phonemizer.backend.espeak.wrapper import EspeakWrapper
_ESPEAK_LIBRARY = '/opt/homebrew/Cellar/espeak/1.48.04_1/lib/libespeak.1.1.48.dylib'
EspeakWrapper.set_library(_ESPEAK_LIBRARY)
```

### Windows eSpeak path fix

```powershell
$env:PHONEMIZER_ESPEAK_LIBRARY = "c:\Program Files\eSpeak NG\libespeak-ng.dll"
$env:PHONEMIZER_ESPEAK_PATH = "c:\Program Files\eSpeak NG"
```

## Models Available

| Model | Language | Format | Size |
|-------|----------|--------|------|
| NeuTTS-Air | English | Q8 GGUF, Q4 GGUF | ~2-3GB |
| NeuTTS-Nano | English | Q8 GGUF, Q4 GGUF | Smaller |
| NeuTTS-Nano-French | French | Q8 GGUF, Q4 GGUF | Smaller |
| NeuTTS-Nano-German | German | Q8 GGUF, Q4 GGUF | Smaller |
| NeuTTS-Nano-Spanish | Spanish | Q8 GGUF, Q4 GGUF | Smaller |

Download from HuggingFace: https://huggingface.co/neuphonic

## Basic Usage

```python
# See the repo's example scripts for full usage
# Models load from local GGUF files after download
```

## Voice Cloning

Instant voice cloning with as little as 3 seconds of audio:

```python
# Provide a reference audio file
# The model clones the speaker's voice characteristics
# See repo examples for full implementation
```

### Reference clip guidelines

- **Duration**: 3–10 seconds
- **Quality**: Clean audio, no background noise
- **Format**: WAV preferred

## Strengths

- Best-in-class realism for its size
- GGUF quantized — runs on phones, laptops, Raspberry Pi
- Instant voice cloning (3 seconds of audio)
- Simple LM + codec architecture
- Privacy-first: fully local, no API keys
- 5k+ GitHub stars, active development

## Limitations

- Requires git clone + manual setup (not on PyPI)
- Needs espeak installed
- English primary (Nano variants for FR/DE/ES)
- Model download required (~2-3GB)
- No SSML support
- No subtitle output
