# Backend: Fish Speech (fishaudio)

Load this guide when using Fish Speech as the TTS engine.

**When to pick this:** User wants the most advanced multilingual TTS with fine-grained emotional control, trained on 10M+ hours across 80+ languages. S2 is the latest (March 2026). Best for multilingual podcast episodes.

**Repo:** https://github.com/fishaudio/fish-speech (28k+ stars) | **Docs:** https://speech.fish.audio

## Setup

```bash
# Follow official installation docs:
# https://speech.fish.audio/install/

# Clone the repo
git clone https://github.com/fishaudio/fish-speech.git
cd fish-speech

# Install dependencies (see docs for full instructions)
pip install -e .
```

**Requirements:** Python 3.10+, PyTorch. See docs for detailed setup.

### Docker setup

```bash
# Docker option available
# See: https://speech.fish.audio/install/
```

## Versions

| Version | Status | Key features |
|---------|--------|-------------|
| **S2** (latest) | Current | Fine-grained control, streaming, 80+ languages |
| V1.5 | Stable | 1M+ hours, 13 languages |
| V1.4 | Previous | Earlier multilingual release |

## Language Support

### S2 (latest)
Trained on 10M+ hours across 80+ languages. Major languages with extensive training data.

### V1.5
| Language | Training hours |
|----------|---------------|
| English | >300k hours |
| Chinese | >300k hours |
| Japanese | >100k hours |
| German | ~20k hours |
| French | ~20k hours |
| Spanish | ~20k hours |
| Korean | ~20k hours |
| Arabic | ~20k hours |
| Russian | ~20k hours |
| Portuguese | <10k hours |
| Polish | <10k hours |
| Italian | <10k hours |
| Dutch | <10k hours |

## Key Features (S2)

### Fine-grained control via tags

Insert emotion/style tags directly in text:

```python
# Emotional expressions
"[laugh] That's hilarious!"
"[whispers] Can you keep a secret?"
"[super happy] We did it!"
```

### Multi-speaker conversations

Supports generating multi-speaker dialogues natively.

### Production streaming

- RTF (Real-Time Factor): 0.195
- First-packet latency: <100ms
- Production-ready streaming

### Zero-shot voice cloning

Clone voices from reference audio samples.

## Basic Usage

### CLI

```bash
# See docs: https://speech.fish.audio/install/
fish-speech --help
```

### Web UI

```bash
# Launch the web interface
# See docs for commands
```

### Server mode

```bash
# Run as an API server
# SGLang server for production deployment
# See: https://speech.fish.audio/install/
```

## Strengths

- Most advanced multilingual TTS available (80+ languages in S2)
- Fine-grained emotional control via text tags
- Ultra-low latency streaming (<100ms first packet)
- Multi-speaker conversation support
- Zero-shot voice cloning
- 28k+ GitHub stars — massive community
- Production-ready with SGLang server
- Trained on 10M+ hours of data

## Limitations

- Complex setup — not a simple pip install
- Large model size
- Requires decent hardware
- License: Fish Audio Research License (check terms)
- Primarily optimized for GPU inference
- CPU performance may be limited
- Documentation primarily in English + Chinese
