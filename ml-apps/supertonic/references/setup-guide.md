# Supertonic TTS — Setup Guide

## Prerequisites

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python      | 3.10    | 3.12+       |
| Disk space  | 400 MB  | 1 GB        |
| RAM         | 2 GB    | 8 GB        |
| Network     | Required (first run only — model download) | |

## Installation Methods

### Method 1: pip (simplest)
```bash
pip install supertonic
```

### Method 2: uv (fastest)
```bash
uv pip install supertonic
```

### Method 3: From source (for development)
```bash
git clone https://github.com/supertone-inc/supertonic.git
cd supertonic
uv pip install -e py/
```

## Model Download

The ONNX model (~260MB) downloads **automatically** on first `synthesize()` call
from Hugging Face. Alternatively, pre-download:

```bash
python -c "
from supertonic import TTS
tts = TTS(auto_download=True)
print('Model downloaded and cached')
"
```

Cache location:
- **Linux/macOS:** `~/.cache/supertonic/`
- **Windows:** `%USERPROFILE%\.cache\supertonic\`

## Verify

```bash
python -c "
from supertonic import TTS
from supertonic import __version__
print(f'Supertonic v{__version__} ready!')
"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: onnxruntime` | `pip install onnxruntime` |
| Model download fails | Check network, or manually download from [Hugging Face](https://huggingface.co/Supertone/supertonic-3) |
| GPU not used | Ensure CUDA-enabled onnxruntime: `pip install onnxruntime-gpu` |
| `soundfile` import error on Windows | `pip install soundfile` — may need `pip install pipwin` on some systems |
