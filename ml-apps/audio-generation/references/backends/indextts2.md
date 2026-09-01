# Backend: IndexTTS2 (Bilibili)

Load this guide when using IndexTTS2 as the TTS engine.

**When to pick this:** User wants zero-shot voice cloning with precise duration control and emotional expression. Ideal for video dubbing, audiobook production, and synced narration. Developed by Bilibili.

**Repo:** https://github.com/index-tts/index-tts (19k+ stars) | **Paper:** arXiv

## Setup

```bash
# Clone the repo
git clone https://github.com/index-tts/index-tts.git
cd index-tts

# Install dependencies
pip install -r requirements.txt

# Download model weights
# See repo README for download links
```

**Requirements:** Python 3.x, PyTorch, CUDA recommended (CPU possible but slower). Model weights required.

## Key Features

### 1. Zero-shot voice cloning

Clone any voice with just a few seconds of reference audio. Supports Chinese, English, and Japanese output from any input language.

```python
# Clone from reference audio
# See repo examples for full API
```

### 2. Precise duration control

Two generation modes:
- **Explicit token count**: Specify number of tokens to control exact duration
- **Free autoregressive**: Model generates freely while reproducing input prosody

This is critical for video dubbing where audio must sync to visual timing.

### 3. Emotion-timbre disentanglement

Independent control over:
- **Timbre** (speaker identity) — from reference audio
- **Emotion** — from separate emotion prompt or vector

Emotion control methods:
| Method | Description |
|--------|-------------|
| Audio reference | Use emotional speech sample |
| 8D emotion vector | Precise numerical control |
| Natural language | User-friendly text descriptions |

### 4. Multilingual

- **Output**: Chinese, English, Japanese
- **Input**: Any language for voice cloning

## Training Data

- 55,000 hours of multilingual corpus
- Chinese, English, and Japanese
- Based on XTTS and Tortoise architecture improvements

## Performance

- Outperforms XTTS, CosyVoice2, Fish-Speech, and F5-TTS in benchmarks
- BigVGAN2 audio quality optimization
- Character-pinyin hybrid modeling for Chinese pronunciation
- Punctuation-based pause control

## Community Integrations

- **ComfyUI nodes**: https://github.com/kana112233/ComfyUI-kaola-IndexTTS2
- **Windows build**: https://github.com/wwzhifeng/index-tts-windows
- **HuggingFace Demo**: Available
- **ModelScope Demo**: Available

## Strengths

- Best-in-class emotion control (3 methods)
- Precise duration control for video dubbing
- Zero-shot voice cloning
- Speaker-emotion disentanglement
- Outperforms major competitors in benchmarks
- 19k+ GitHub stars
- Active development (Bilibili-backed)

## Limitations

- Complex setup (git clone, model download)
- Not on PyPI
- Primarily GPU-optimized (CPU slow)
- Output limited to Chinese, English, Japanese
- Large model size
- No CLI — Python API only
- License: check repo (NOASSERTION)
