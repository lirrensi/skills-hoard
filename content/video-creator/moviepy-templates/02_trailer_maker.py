# pyright: reportMissingImports=false
"""
Movie Trailer Generator
=======================
Creates an exciting movie trailer from a longer video with
opening title, action scenes, and closing credits.

Usage:
    python trailer_maker.py --video movie.mp4 --output trailer.mp4
"""

import argparse
from moviepy import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    vfx,
)


def create_trailer(video_path: str, output_path: str, title: str):
    """Create a movie trailer."""

    video = VideoFileClip(video_path)

    # Define trailer scenes (start, end times in seconds)
    scenes = [
        (0, 15),  # Opening
        (30, 45),  # First action
        (120, 140),  # Second action
        (200, 220),  # Climax
    ]

    # Extract and process scenes
    subclips = []
    for start, end in scenes:
        if end <= video.duration:
            sub = video.subclipped(start, end)
            # Add dramatic fade
            sub = sub.with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])
            subclips.append(sub)

    # Create title card
    title_clip = (
        TextClip(
            font="Arial.ttf",
            text=title,
            font_size=150,
            color="white",
            stroke_color="black",
            stroke_width=5,
        )
        .with_duration(4)
        .with_position("center")
    )

    # Create "Coming Soon" closing
    closing = (
        TextClip(font="Arial.ttf", text="COMING SOON", font_size=80, color="white")
        .with_duration(3)
        .with_effects([vfx.FadeIn(1), vfx.FadeOut(1)])
    )

    # Composite
    final = concatenate_videoclips([title_clip] + subclips + [closing])
    final.write_videofile(output_path, fps=24, codec="libx264")

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create movie trailer")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", default="trailer.mp4", help="Output file")
    parser.add_argument("--title", default="THE STORY", help="Movie title")

    args = parser.parse_args()
    create_trailer(args.video, args.output, args.title)
