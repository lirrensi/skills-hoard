# pyright: reportMissingImports=false
"""
Subtitle Adder
==============
Adds styled subtitles/overlays to video from a simple
timestamped text file.

Subtitle file format (subtitles.srt style):
    00:00:01,000 --> 00:00:04,000
    Hello, world!

    00:00:05,000 --> 00:00:08,000
    This is a subtitle

Usage:
    python add_subtitles.py --video clip.mp4 --subs subtitles.txt --output with_subs.mp4
"""

import argparse
import re
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, vfx


def parse_subtitles(subtitle_file: str) -> list:
    """Parse subtitle file into list of (start, end, text) tuples."""
    subtitles = []

    with open(subtitle_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by double newlines
    blocks = re.split(r"\n\n+", content)

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) >= 3:
            # Parse timing line
            timing = lines[1]
            match = re.match(
                r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})",
                timing,
            )
            if match:
                start = (
                    int(match.group(1)) * 3600
                    + int(match.group(2)) * 60
                    + int(match.group(3))
                    + int(match.group(4)) / 1000
                )
                end = (
                    int(match.group(5)) * 3600
                    + int(match.group(6)) * 60
                    + int(match.group(7))
                    + int(match.group(8)) / 1000
                )
                text = "\n".join(lines[2:])
                subtitles.append((start, end, text))

    return subtitles


def add_subtitles(video_path: str, subtitle_file: str, output_path: str):
    """Add subtitles to video."""

    video = VideoFileClip(video_path)
    subtitles = parse_subtitles(subtitle_file)

    text_clips = []
    for start, end, text in subtitles:
        duration = end - start

        txt = (
            TextClip(
                font="Arial.ttf",
                text=text,
                font_size=48,
                color="white",
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(video.w * 0.8, None),  # 80% of video width
            )
            .with_duration(duration)
            .with_position(("center", video.h - 150))  # Near bottom
        )

        # Add subtle fade
        txt = txt.with_effects([vfx.FadeIn(0.2), vfx.FadeOut(0.2)])

        # Set start time in composition
        txt = txt.with_start(start)
        text_clips.append(txt)

    # Composite video with subtitles
    final = CompositeVideoClip([video] + text_clips)
    final.write_videofile(output_path, fps=video.fps, codec="libx264")

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add subtitles to video")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--subs", required=True, help="Subtitle file (.srt or .txt)")
    parser.add_argument("--output", default="with_subs.mp4", help="Output file")

    args = parser.parse_args()
    add_subtitles(args.video, args.subs, args.output)
