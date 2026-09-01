# MoviePy Guide

Load this guide when the request is about clip manipulation, assembly, audio work, format conversion, or batch export automation.

This guide assumes **MoviePy v2**.

## What MoviePy Should Own

- trim and subclip work
- concatenation and compositing
- fades and utility effects
- audio replacement or mixing
- resize, crop, transcode, and packaging
- batch-processing many output files

## Install

```bash
pip install moviepy
```

## Core Imports

```python
from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoFileClip,
    afx,
    concatenate_videoclips,
    vfx,
)
```

## Minimal Workflow

```python
from moviepy import AudioFileClip, VideoFileClip, afx, vfx

video = VideoFileClip("input.mp4").subclipped(3, 18)
music = AudioFileClip("music.mp3")

final = (
    video
    .with_audio(music.subclipped(0, video.duration))
    .with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
)

final.write_videofile("output.mp4", fps=30)
```

## Common Operations

```python
# Trim
clip = clip.subclipped(10, 25)

# Resize and crop
clip = clip.resized(width=1080)
clip = clip.cropped(width=1080, height=1920)

# Position in a composite
overlay = overlay.with_position((80, 120))

# Fade audio
audio = audio.with_effects([afx.AudioFadeIn(1), afx.AudioFadeOut(1)])

# Merge clips in sequence
final = concatenate_videoclips([clip1, clip2, clip3])

# Layer clips
final = CompositeVideoClip([base_clip, overlay])
```

## Good Fits

- merge footage from multiple files
- add background music or narration
- make vertical, square, and widescreen variants
- convert exports into delivery-ready files
- process many videos from a Python job

## Templates

Use `moviepy-templates/` for common utility jobs:

- `moviepy-templates/01_reel_maker.py` - vertical short-form edit
- `moviepy-templates/02_trailer_maker.py` - trailer assembly
- `moviepy-templates/03_merge_videos.py` - sequential merge
- `moviepy-templates/04_add_subtitles.py` - subtitle overlay
- `moviepy-templates/05_add_music.py` - background music
- `moviepy-templates/06_slideshow.py` - image slideshow
- `moviepy-templates/07_change_speed.py` - speed changes
- `moviepy-templates/08_trimmer.py` - trimming
- `moviepy-templates/09_resizer.py` - resize or reformat
- `moviepy-templates/10_video_effects.py` - quick effects
- `moviepy-templates/11_gif_maker.py` - gif export
- `moviepy-templates/12_watermark.py` - logo overlay
- `moviepy-templates/13_picture_in_picture.py` - picture in picture
- `moviepy-templates/14_video_collage.py` - grid collage

## Best Practices

- Remember that v2 uses `.with_*` methods and effect classes.
- Close clips or use context managers when handling many files.
- Keep MoviePy focused on clip operations and export work, not high-complexity motion design.
- When working in a hybrid pipeline, ingest rendered Remotion clips as normal video assets.

## Common Pitfalls

- Using old v1 imports such as `moviepy.editor`.
- Forgetting that `ImageClip` and `TextClip` need a duration.
- Re-timing a carefully designed Remotion animation after render without a clear reason.
