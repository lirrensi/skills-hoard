# Backend: CosyVoice2 (FunAudioLLM)

Load this guide when using CosyVoice as the TTS engine.

**When to pick this:** User wants multilingual TTS with zero-shot cloning, ultra-low latency streaming (150ms), and instruction-based control. 0.5B params, covers 9 languages + 18 Chinese dialects. Apache 2.0 licensed.

**Repo:** https://github.com/FunAudioLLM/CosyVoice (20k+ stars) | **HuggingFace:** https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B

## Setup

```bash
# Clone the repo
git clone https://github.com/FunAudioLLM/CosyVoice.git
cd CosyVoice

# Create conda environment (recommended)
conda create -n cosyvoice python=3.10
conda activate cosyvoice

# Install dependencies
pip install -r requirements.txt

# Download models (from HuggingFace or ModelScope)
# Place in pretrained_models/CosyVoice2-0.5B/
```

**Requirements:** Python 3.10, PyTorch, significant disk space for models.

## Versions

| Version | Params | Key features |
|---------|--------|-------------|
| Fun-CosyVoice 3.0 | 0.5B | Latest, RL-optimized, best quality |
| CosyVoice 2.0 | 0.5B | Streaming, 150ms latency |
| CosyVoice 1.0 | 300M | Original release |

## Basic Usage

### Web UI

```bash
python webui.py --port 50002 --model_dir pretrained_models/CosyVoice2-0.5B
```

### Python API

```python
from cosyvoice.cli.cosyvoice import CosyVoice2

# Load model
model = CosyVoice2('pretrained_models/CosyVoice2-0.5B', load_jit=False)

# Generate speech
tts_output = model.inference_sft(
    "Hello, this is CosyVoice TTS.",
    speaker_id='en',  # or specific speaker
    stream=False
)

# Save audio
import soundfile as sf
sf.write('output.wav', tts_output['tts_speech'].numpy(), 22050)
```

## Language Support

| Language | Code | Notes |
|----------|------|-------|
| Chinese | `zh` | + 18 dialects (Cantonese, Sichuan, Shanghai, etc.) |
| English | `en` | |
| Japanese | `ja` | |
| Korean | `ko` | |
| German | `de` | |
| Spanish | `es` | |
| French | `fr` | |
| Italian | `it` | |
| Russian | `ru` | |

## Key Features

### Bi-streaming (150ms latency)

```python
# Text-in streaming and audio-out streaming
# Achieves latency as low as 150ms
# See repo docs for streaming API
```

### Instruction-based control

Control generation with natural language instructions:
- Language switching
- Dialect selection
- Emotion control
- Speed adjustment
- Volume control

### Zero-shot voice cloning

```python
# Clone from reference audio
tts_output = model.inference_zero_shot(
    "Text to speak.",
    prompt_audio_path="reference.wav",  # 3-10 seconds
    stream=False
)
```

### Pronunciation inpainting

Supports Chinese Pinyin and English CMU phoneme correction for precise pronunciation control.

## Strengths

- 9 languages + 18 Chinese dialects
- Ultra-low latency streaming (150ms)
- Zero-shot voice cloning
- Instruction-based control (language, emotion, speed)
- Pronunciation inpainting for production use
- Apache 2.0 licensed
- 20k+ GitHub stars, active development
- Text normalization (handles numbers, symbols)

## Limitations

- Complex setup (git clone, conda, model download)
- Not on PyPI — manual installation required
- Large model size
- Primarily optimized for Chinese + English
- Requires decent hardware for real-time
- No CLI — Python API or Web UI only
