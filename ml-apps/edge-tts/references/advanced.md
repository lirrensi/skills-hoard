# Advanced Usage & Gotchas

## Common Gotchas

- **`--play` doesn't exist on Windows** — always use `edge-playback` executable instead
- **Rate/Volume/Pitch need `+X%` / `+XHz` format** — not plain numbers
- **Requires internet** — edge-tts calls Microsoft's servers for synthesis
- **Output is MP3** not WAV — use ffmpeg if WAV needed: `ffmpeg -i out.mp3 out.wav`
- **Voice names are case-sensitive** — `en-US-AriaNeural` not `en-us-arianeural`
- **`uv tool install`** puts executables in uv's tool bin — make sure it's on PATH
