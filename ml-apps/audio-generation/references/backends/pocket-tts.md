# Backend: Pocket TTS (Kyutai)

Load this guide when using Pocket TTS as the TTS engine.

**When to pick this:** User wants voice cloning from short audio clips, running locally on CPU. 100M params, ~6x real-time on MacBook Air M4, English only (more languages planned).

**Repo:** https://github.com/kyutai-labs/pocket-tts | **Demo:** https://kyutai.org/pocket-tts

## Setup

```bash
pip install pocket-tts

# Or with uv (recommended — handles deps on the fly):
uvx pocket-tts generate
```

**Requirements:** Python 3.10–3.14, PyTorch 2.5+ (CPU version is fine, GPU not needed).

## Basic Usage

### CLI

```bash
# Generate with default voice
pocket-tts generate

# Specify voice and text
pocket-tts generate --voice alba --text "Hello world, this is a test."

# Run a local web server (keeps model in memory, faster for multiple requests)
pocket-tts serve
# Then open http://localhost:8000

# Export a voice for fast loading later
pocket-tts export-voice --audio-input ./my_voice.wav --output ./my_voice.safetensors
```

### Python API

```python
from pocket_tts import TTSModel
import scipy.io.wavfile

# Load model (downloads on first run)
tts_model = TTSModel.load_model()

# Generate with a pre-made voice
voice_state = tts_model.get_state_for_audio_prompt("alba")
audio = tts_model.generate_audio(voice_state, "Hello world, this is a test.")

# Audio is a 1D torch tensor containing PCM data
scipy.io.wavfile.write("output.wav", tts_model.sample_rate, audio.numpy())
```

## Pre-made Voices

| Voice | Description |
|-------|-------------|
| `alba` | Casual, natural female |
| `marius` | Male voice |
| `javert` | Male voice |
| `jean` | Male voice |
| `fantine` | Female voice |
| `cosette` | Female voice (confused style) |
| `eponine` | Female voice |
| `azelma` | Female voice |

Voice samples and licenses: https://huggingface.co/kyutai/tts-voices

## Voice Cloning

Pocket TTS's standout feature. Provide a reference audio file and it mimics the voice.

### From a local audio file

```python
from pocket_tts import TTSModel
import scipy.io.wavfile

tts_model = TTSModel.load_model()

# Clone from a local WAV file (3-10 seconds of clean speech)
voice_state = tts_model.get_state_for_audio_prompt("./my_voice_sample.wav")
audio = tts_model.generate_audio(voice_state, "This will sound like the reference voice.")
scipy.io.wavfile.write("cloned.wav", tts_model.sample_rate, audio.numpy())
```

### From Hugging Face

```python
# Use a voice from the HF voice repository
voice_state = tts_model.get_state_for_audio_prompt(
    "hf://kyutai/tts-voices/expresso/ex01-ex02_default_001_channel2_198s.wav"
)
```

### CLI voice cloning

```bash
pocket-tts generate --voice ./my_voice_sample.wav --text "Cloned voice speaking."
```

### Reference clip guidelines

- **Duration**: 3–10 seconds is ideal
- **Quality**: Clean audio, no background noise, no music
- **Content**: Natural speech, not whispering or shouting
- **Tip**: Clean the sample first (e.g., Adobe Podcast Enhance)

## Export/Import Voice States

Processing audio for cloning is slow, but loading a safetensors file is fast:

```python
from pocket_tts import TTSModel, export_model_state, import_model_state

model = TTSModel.load_model()

# Export a voice state for fast loading later
voice_state = model.get_state_for_audio_prompt("some_voice.wav")
export_model_state(voice_state, "some_voice.safetensors")

# Later, load it quickly (just reads kvcache from disk)
voice_state = import_model_state("some_voice.safetensors")
audio = model.generate_audio(voice_state, "Fast voice loading!")
```

## Performance

- ~6x real-time on MacBook Air M4 CPU
- ~200ms latency for first audio chunk
- Uses only 2 CPU cores
- Audio streaming supported
- Handles infinitely long text inputs

## Strengths

- Voice cloning from short clips (3-10 seconds)
- Runs on CPU at ~6x real-time
- Low latency (~200ms first chunk)
- Audio streaming
- No internet required after model download
- Can run in-browser (WASM implementations available)
- Active development (3.6k+ GitHub stars)

## Limitations

- English only (more languages planned)
- No SSML support
- No subtitle output
- Model download required (~400MB)
- Processing reference audio for cloning is relatively slow (export to safetensors for reuse)
- GPU doesn't provide speedup (model is small, CPU-bound)
