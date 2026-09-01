# MoviePy Templates

A collection of reusable Python scripts for the MoviePy side of the `video-creator` skill.

These templates are the **utility and assembly layer**.

- Use **Remotion** when the user needs designed motion graphics, animated text systems, title cards, lower thirds, or data-driven scenes.
- Use these **MoviePy templates** when the user needs trimming, merging, subtitles, music, resizing, packaging, or batch export work.
- In a hybrid workflow, let Remotion render the polished segments first, then use these templates as the glue work.

## Installation

```bash
pip install moviepy
```

## Available Templates

| # | Script | Description | Use Case |
|---|--------|-------------|----------|
| 01 | `01_reel_maker.py` | Vertical short video (9:16) | Instagram/TikTok/Reels |
| 02 | `02_trailer_maker.py` | Movie trailer with title cards | Promos, previews |
| 03 | `03_merge_videos.py` | Combine multiple videos | Merge clips |
| 04 | `04_add_subtitles.py` | Add SRT subtitles | Caption videos |
| 05 | `05_add_music.py` | Background music | Score/vlog |
| 06 | `06_slideshow.py` | Image slideshow with Ken Burns | Photo presentations |
| 07 | `07_change_speed.py` | Speed up/slow down | Timelapse/slow-mo |
| 08 | `08_trimmer.py` | Cut specific portions | Basic editing |
| 09 | `09_resizer.py` | Change resolution | Format conversion |
| 10 | `10_video_effects.py` | Visual effects | B&W, mirror, etc. |
| 11 | `11_gif_maker.py` | Convert to GIF | Animated GIFs |
| 12 | `12_watermark.py` | Add logo/watermark | Branding |
| 13 | `13_picture_in_picture.py` | Picture-in-picture | Tutorials, reactions |
| 14 | `14_video_collage.py` | Grid layout collage | Comparisons, compilations |

## Quick Usage

```bash
# Reel maker
python 01_reel_maker.py --clips clip1.mp4 clip2.mp4 --output reel.mp4 --title "My Reel"

# Add subtitles
python 04_add_subtitles.py --video video.mp4 --subs subtitles.txt --output with_subs.mp4

# Merge videos
python 03_merge_videos.py --videos clip1.mp4 clip2.mp4 --output merged.mp4

# Add music
python 05_add_music.py --video video.mp4 --music bgm.mp3 --output with_music.mp4
```

## Requirements

- Python 3.9+
- MoviePy v2
- FFmpeg (for video encoding)

## Notes

- All scripts use MoviePy v2 API (`.with_effects()`, `.with_*` methods)
- Font files required for text (Arial.ttf or custom path)
- Adjust parameters as needed for your specific use case
