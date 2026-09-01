# FFmpeg Audio Recipes

Load this guide whenever audio assembly, post-processing, format conversion, or manipulation is needed. This is the audio workbench — all non-TTS operations live here.

## Concatenation

### Simple concat (same format, same codec)

```bash
# Create file list
echo "file 'part1.mp3'" > filelist.txt
echo "file 'part2.mp3'" >> filelist.txt
echo "file 'part3.mp3'" >> filelist.txt

# Concatenate
ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp3
```

### Concat with silence between segments

```bash
# Generate silence file (once, reuse everywhere)
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 0.5 -q:a 9 silence_0.5s.mp3
ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t 1.0 -q:a 9 silence_1.0s.mp3

# Build file list with pauses
echo "file 'part1.mp3'" > filelist.txt
echo "file 'silence_0.5s.mp3'" >> filelist.txt
echo "file 'part2.mp3'" >> filelist.txt
echo "file 'silence_0.5s.mp3'" >> filelist.txt
echo "file 'part3.mp3'" >> filelist.txt

ffmpeg -f concat -safe 0 -i filelist.txt -c copy output.mp3
```

### Concat with different formats

When source files have different sample rates, channels, or codecs, re-encode instead of stream copy:

```bash
ffmpeg -i part1.wav -i part2.mp3 -i part3.ogg \
  -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[outa]" \
  -map "[outa]" output.mp3
```

## Volume & Loudness

### Normalize loudness (EBU R128 — the standard)

```bash
# Single pass (good for most cases)
ffmpeg -i input.mp3 -af loudnorm output.mp3

# Two pass (more accurate, for production quality)
ffmpeg -i input.mp3 -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null /dev/null 2>&1 | tail -12
# Use the measured values from the output:
ffmpeg -i input.mp3 -af loudnorm=I=-16:TP=-1.5:LRA=11:measured_I=-20:measured_TP=-3:measured_LRA=8:measured_thresh=-30:offset=0.5:linear=true output.mp3
```

### Adjust volume

```bash
# Increase by 50%
ffmpeg -i input.mp3 -af "volume=1.5" output.mp3

# Decrease by 50%
ffmpeg -i input.mp3 -af "volume=0.5" output.mp3

# Set to specific dB
ffmpeg -i input.mp3 -af "volume=3dB" output.mp3
```

### Detect volume levels

```bash
ffmpeg -i input.mp3 -af volumedetect -f null /dev/null 2>&1 | grep -E "max_volume|mean_volume"
```

## Fades

### Fade in

```bash
# 2 second fade in from silence
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=2" output.mp3
```

### Fade out

```bash
# 2 second fade out to silence (at end of file)
ffmpeg -i input.mp3 -af "afade=t=out:st=58:d=2" output.mp3
# st=start time, d=duration
```

### Both fades

```bash
# Get duration first
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp3)
FADE_OUT=$(echo "$DURATION - 2" | bc)

ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=2,afade=t=out:st=$FADE_OUT:d=2" output.mp3
```

## Trimming & Silence Removal

### Trim start/end

```bash
# Skip first 5 seconds
ffmpeg -ss 5 -i input.mp3 output.mp3

# Take only seconds 10-30
ffmpeg -ss 10 -t 20 -i input.mp3 output.mp3

# Trim to specific duration
ffmpeg -t 60 -i input.mp3 output.mp3  # first 60 seconds
```

### Remove silence

```bash
# Remove leading/trailing silence
ffmpeg -i input.mp3 -af silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB output.mp3

# Remove silence between segments (more aggressive)
ffmpeg -i input.mp3 -af silenceremove=stop_periods=-1:stop_silence=0.5:stop_threshold=-50dB output.mp3
```

## Format Conversion

```bash
# MP3 to WAV (lossless)
ffmpeg -i input.mp3 output.wav

# WAV to MP3 (with bitrate)
ffmpeg -i input.wav -b:a 192k output.mp3

# Any format to MP3
ffmpeg -i input.ogg output.mp3
ffmpeg -i input.flac output.mp3
ffmpeg -i input.m4a output.mp3

# MP3 to M4A/AAC
ffmpeg -i input.mp3 -c:a aac output.m4a

# Change sample rate
ffmpeg -i input.mp3 -ar 44100 output.mp3

# Change channels (mono to stereo, or vice versa)
ffmpeg -i input.mp3 -ac 1 output_mono.mp3
ffmpeg -i input.mp3 -ac 2 output_stereo.mp3
```

## Mixing & Overlay

### Mix voice with background music

```bash
# Music plays under voice, auto-fades when voice starts
ffmpeg -i voice.mp3 -i music.mp3 \
  -filter_complex "[1]volume=0.1[bg];[0][bg]amix=inputs=2:duration=first:dropout_transition=2" \
  output.mp3
```

### Overlay a sound effect at a specific time

```bash
# Add a ding at 30 seconds into the narration
ffmpeg -i narration.mp3 -i ding.mp3 \
  -filter_complex "[1]adelay=30000|30000[delayed];[0][delayed]amix=inputs=2:duration=first" \
  output.mp3
```

### Crossfade between two audio files

```bash
# 2 second crossfade
ffmpeg -i part1.mp3 -i part2.mp3 \
  -filter_complex "[0][1]acrossfade=d=2:c1=tri:c2=tri" \
  output.mp3
```

## Speed & Pitch

### Change speed (affects pitch)

```bash
# 2x speed
ffmpeg -i input.mp3 -af "atempo=2.0" output.mp3

# 0.5x speed
ffmpeg -i input.mp3 -af "atempo=0.5" output.mp3

# Extreme: chain atempo filters (each maxes at 2.0)
ffmpeg -i input.mp3 -af "atempo=2.0,atempo=2.0" output.mp3  # 4x
```

### Change speed without affecting pitch

```bash
# Requires rubberband
ffmpeg -i input.mp3 -af "rubberband=tempo=1.5" output.mp3
```

### Change pitch without affecting speed

```bash
ffmpeg -i input.mp3 -af "asetrate=44100*0.9,aresample=44100" output.mp3  # lower pitch
```

## Metadata

```bash
# Add metadata
ffmpeg -i input.mp3 -metadata title="My Podcast" -metadata artist="Host Name" -metadata album="Season 1" output.mp3

# Strip all metadata
ffmpeg -i input.mp3 -map_metadata -1 output.mp3

# Show metadata
ffprobe -v error -show_entries format_tags -of default=noprint_wrappers=1 input.mp3
```

## Info & Analysis

```bash
# Get duration
ffprobe -v error -show_entries format=duration -of csv=p=0 input.mp3

# Get file info (codec, bitrate, sample rate)
ffprobe -v error -show_entries stream=codec_name,sample_rate,channels,bit_rate -of default=noprint_wrappers=1 input.mp3

# Generate waveform image
ffmpeg -i input.mp3 -filter_complex "showwavespic=s=1024x256" -frames:v 1 waveform.png
```

## Common Recipes for Audio Generation

### Prepare a silence file library

Generate once, reuse everywhere:

```bash
for dur in 0.3 0.5 0.8 1.0 1.5 2.0; do
  ffmpeg -f lavfi -i anullsrc=r=24000:cl=mono -t $dur -q:a 9 "silence_${dur}s.mp3"
done
```

### Generate a section separator tone

```bash
# Short pleasant ding
ffmpeg -f lavfi -i sine=frequency=800:duration=0.3 \
  -af "afade=t=in:d=0.05,afade=t=out:d=0.2,volume=0.3" \
  separator.mp3
```

### Batch convert all files in a directory

```bash
for f in input/*.wav; do
  ffmpeg -i "$f" -b:a 192k "output/$(basename ${f%.wav}).mp3"
done
```
