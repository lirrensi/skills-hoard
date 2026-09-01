# TTS Backends

Load this guide when choosing or setting up a TTS engine. This is the routing layer — pick a backend based on the user's environment and needs, then read the specific backend file for setup and usage.

## Available Backends

### Cloud

| Backend | Best for | Quality | Voices | Read next |
|---------|----------|---------|--------|-----------|
| **edge-tts** | Quick start, no install, 400+ voices | High | 400+ | `backends/edge-tts.md` |

### Local — CPU-friendly, quick start

| Backend | Best for | Params | Quality | Speed (CPU) | Cloning | Read next |
|---------|----------|--------|---------|-------------|---------|-----------|
| **Kokoro** | Reliable daily driver, natural quality | 82M | Very high | Near real-time | No | `backends/kokoro.md` |
| **Pocket TTS** | Voice cloning on CPU, newest (Jan 2026) | 100M | High | ~6x real-time | Yes | `backends/pocket-tts.md` |
| **MeloTTS** | Multilingual accents, CPU-optimized | ~100M | High | Real-time | No | `backends/melotts.md` |
| **Piper** | Lightest, runs on Raspberry Pi | ~30-100M | Good | Very fast | No | `backends/piper.md` |
| **NeuTTS Air** | Super-realistic on-device, GGUF quantized | 500M | Very high | Real-time | Instant (3s) | `backends/neutts-air.md` |

### Local — advanced, GPU recommended

| Backend | Best for | Params | Quality | Speed | Cloning | Read next |
|---------|----------|--------|---------|-------|---------|-----------|
| **Chatterbox-Turbo** | ElevenLabs killer, paralinguistic tags | 350M | Very high | Good (CPU viable) | Zero-shot | `backends/chatterbox.md` |
| **CosyVoice2** | Multilingual streaming, 150ms latency | 500M | Very high | Ultra-low latency | Zero-shot | `backends/cosyvoice.md` |
| **Fish Speech** | 80+ languages, fine-grained emotion | Large | Top | <100ms first packet | Zero-shot | `backends/fish-speech.md` |
| **IndexTTS2** | Duration control, emotion disentanglement | Large | Top | GPU-optimized | Zero-shot | `backends/indextts2.md` |

## How to Choose

### Quick decision flowchart

```
User wants TTS
├── Internet OK, zero setup? → edge-tts
├── Needs voice cloning?
│   ├── CPU only?
│   │   ├── Quick start? → Pocket TTS
│   │   └── Best realism? → NeuTTS Air
│   ├── GPU available?
│   │   ├── Emotional expression? → Chatterbox-Turbo
│   │   ├── Multilingual? → CosyVoice2 or Fish Speech
│   │   └── Duration control? → IndexTTS2
│   └── Don't know? → Pocket TTS (safest)
├── No cloning needed?
│   ├── CPU only?
│   │   ├── Best quality? → Kokoro
│   │   ├── Multilingual accents? → MeloTTS
│   │   ├── Lowest resources? → Piper
│   │   └── Don't know? → Kokoro
│   └── GPU available? → Chatterbox-Turbo or CosyVoice2
└── Don't know hardware? → edge-tts (cloud) or Kokoro (local)
```

### By use case

| Use case | Recommended | Why |
|----------|-------------|-----|
| Quick test / prototype | edge-tts | Zero setup, instant |
| Daily podcast production | Kokoro | Reliable, fast, natural |
| Podcast with voice cloning | Pocket TTS | CPU-friendly cloning |
| Audiobook narration | NeuTTS Air | Super-realistic, long-form |
| Emotional storytelling | Chatterbox-Turbo | Paralinguistic tags |
| Multilingual podcast | Fish Speech or CosyVoice2 | 80+ languages |
| Video dubbing (synced) | IndexTTS2 | Precise duration control |
| Raspberry Pi / embedded | Piper | Lightest possible |
| Batch overnight rendering | Piper or Kokoro | Reliable, fast |

### Default choice

When the user has no preference:
- **edge-tts** if internet is available (simplest)
- **Kokoro** if they want local (safest CPU bet)

## Setup Complexity

| Backend | Install method | Time | Notes |
|---------|---------------|------|-------|
| edge-tts | `pip install edge-tts` | Seconds | Needs internet |
| Kokoro | `pip install kokoro soundfile` | Minutes | + espeak-ng |
| Pocket TTS | `pip install pocket-tts` | Minutes | Model download |
| MeloTTS | git clone + `pip install -e .` | Minutes | + unidic download |
| Piper | `pip install piper-tts` | Seconds | Model auto-download |
| NeuTTS Air | git clone + `pip install -r requirements.txt` | Minutes | + espeak, model download |
| Chatterbox-Turbo | `pip install chatterbox-tts` | Minutes | Model download |
| CosyVoice2 | git clone + conda | Longer | Complex setup |
| Fish Speech | git clone + pip | Longer | Complex setup |
| IndexTTS2 | git clone + pip | Longer | Model download |

## Feature Matrix

| Feature | edge-tts | Kokoro | Pocket | MeloTTS | Piper | NeuTTS | Chatterbox | CosyVoice2 | Fish | IndexTTS2 |
|---------|----------|--------|--------|---------|-------|--------|------------|------------|------|-----------|
| Offline | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Voice cloning | ✗ | ✗ | ✓ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Multilingual | ✓ | Limited | ✗ | ✓ | ✓ | Limited | ✗ | ✓ | ✓ | Limited |
| Emotion control | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Streaming | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✗ |
| Duration control | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Subtitle output | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| On PyPI | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| License | N/A | Apache | MIT | MIT | GPL-3.0 | Custom | MIT | Apache | Custom | Custom |
