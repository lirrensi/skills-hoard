# Backend: MeloTTS (MyShell.ai)

Load this guide when using MeloTTS as the TTS engine.

**When to pick this:** User wants fast, CPU-optimized TTS with multilingual support and accent variety. Designed for real-time on CPUs. MIT-licensed, free for commercial use.

**Repo:** https://github.com/myshell-ai/MeloTTS

## Setup

```bash
# Clone and install
git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
pip install -e .

# Download required dictionary
python -m unidic download
```

**Requirements:** Python 3.9, Ubuntu 20.04+ (tested). macOS may need Docker.

### Docker Install (Windows/macOS fallback)

```bash
git clone https://github.com/myshell-ai/MeloTTS.git
cd MeloTTS
docker build -t melotts .
docker run -it -p 8888:8888 melotts
# Open http://localhost:8888
```

## Basic Usage

### CLI

```bash
# English (default)
melo "Text to read" output.wav

# Specify language
melo "Text to read" output.wav --language EN

# Specify speaker/accent
melo "Text to read" output.wav --language EN --speaker EN-US
melo "Text to read" output.wav --language EN --speaker EN-BR
melo "Text to read" output.wav --language EN --speaker EN-AU

# Adjust speed
melo "Text to read" output.wav --speed 1.5

# Load from file
melo file.txt output.wav --file

# Other languages
melo "text-to-speech 领域近年来发展迅速" zh.wav -l ZH
```

### Web UI

```bash
melo-ui
# Or: python melo/app.py
```

### Python API

```python
from melo.api import TTS

speed = 1.0
device = 'auto'  # Will use GPU if available, else CPU

# English with multiple accents
text = "Did you ever hear a folk tale about a giant turtle?"
model = TTS(language='EN', device=device)
speaker_ids = model.hps.data.spk2id

# American accent
model.tts_to_file(text, speaker_ids['EN-US'], 'en-us.wav', speed=speed)

# British accent
model.tts_to_file(text, speaker_ids['EN-BR'], 'en-br.wav', speed=speed)

# Indian accent
model.tts_to_file(text, speaker_ids['EN_INDIA'], 'en-india.wav', speed=speed)

# Australian accent
model.tts_to_file(text, speaker_ids['EN-AU'], 'en-au.wav', speed=speed)

# Default accent
model.tts_to_file(text, speaker_ids['EN-Default'], 'en-default.wav', speed=speed)
```

## Language & Accent Support

| Language | Code | Speakers/accents |
|----------|------|------------------|
| English | `EN` | `EN-US`, `EN-BR`, `EN_INDIA`, `EN-AU`, `EN-Default` |
| Spanish | `ES` | `ES` |
| French | `FR` | `FR` |
| Chinese | `ZH` | `ZH` (supports mixed Chinese/English) |
| Japanese | `JP` | `JP` |
| Korean | `KR` | `KR` |

### Other languages (Python API)

```python
# Spanish
model = TTS(language='ES', device='cpu')
model.tts_to_file("El resplandor del sol acaricia las olas.", 'ES', 'es.wav', speed=1.0)

# French
model = TTS(language='FR', device='cpu')
model.tts_to_file("La lueur dorée du soleil caresse les vagues.", 'FR', 'fr.wav', speed=1.0)

# Chinese (mixed EN)
model = TTS(language='ZH', device='cpu')
model.tts_to_file("我最近在学习machine learning。", 'ZH', 'zh.wav', speed=1.0)

# Japanese
model = TTS(language='JP', device='cpu')
model.tts_to_file("彼は毎朝ジョギングをしています。", 'JP', 'jp.wav', speed=1.0)

# Korean
model = TTS(language='KR', device='cpu')
model.tts_to_file("안녕하세요! 오늘은 날씨가 정말 좋네요.", 'KR', 'kr.wav', speed=1.0)
```

## Parameters

| Parameter | Description | Range |
|-----------|-------------|-------|
| `language` | Language code | `EN`, `ES`, `FR`, `ZH`, `JP`, `KR` |
| `speaker_id` | Accent/voice | Varies by language (see above) |
| `speed` | Speaking rate | `0.5` to `2.0`, default `1.0` |
| `device` | Compute device | `'auto'`, `'cpu'`, `'cuda'`, `'cuda:0'`, `'mps'` |

## Strengths

- Designed for CPU real-time — fast on modest hardware
- Multilingual with accent variety (especially English accents)
- MIT-licensed — free for commercial use
- Chinese speaker supports mixed Chinese/English
- Simple API, quick setup
- 7.3k+ GitHub stars

## Limitations

- Requires git clone + manual install (not on PyPI as `pip install melotts`)
- Needs `unidic` dictionary download
- macOS may need Docker for compatibility
- No voice cloning
- No SSML support
- No subtitle output
- Fewer voices than edge-tts
