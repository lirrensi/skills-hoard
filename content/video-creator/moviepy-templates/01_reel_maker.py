# pyright: reportMissingImports=false
"""
Reel Generator - Vertical Short Video (9:16)
=============================================
Creates a vertical-format reel from multiple video clips with
title cards and transitions. Perfect for Instagram/TikTok/Reels.

Usage:
    python reel_maker.py --clips clip1.mp4 clip2.mp3 --output reel.mp4
"""

import argparse
from moviepy import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    vfx,
)


def create_reel(clip_paths: list, output_path: str, title: str = "My Reel"):
    """Create a vertical reel from video clips."""

    # Load all clips
    clips = []
    for path in clip_paths:
        clip = VideoFileClip(path)
        # Resize to vertical 9:16 ratio (1080x1920)
        clip = clip.resized(height=1920)
        # Crop to center if wider
        if clip.w > 1080:
            clip = clip.cropped(x1=(clip.w - 1080) // 2, width=1080)
        clips.append(clip)

    # Add fade transitions
    processed_clips = []
    for i, clip in enumerate(clips):
        # Take first 10 seconds of each if longer
        if clip.duration > 10:
            clip = clip.subclipped(0, 10)

        # Add fade in/out
        clip = clip.with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
        processed_clips.append(clip)

    # Add title card
    title_card = (
        TextClip(
            font="Arial.ttf",
            text=title,
            font_size=120,
            color="white",
            method="caption",
            size=(1080, None),
        )
        .with_duration(2)
        .with_effects([vfx.FadeIn(0.5), vfx.FadeOut(0.5)])
    )

    # Composite final video
    final = concatenate_videoclips([title_card] + processed_clips)
    final.write_videofile(output_path, fps=30, codec="libx264")

    # Cleanup
    for clip in clips:
        clip.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create vertical reel")
    parser.add_argument("--clips", nargs="+", required=True, help="Input video files")
    parser.add_argument("--output", default="reel.mp4", help="Output file")
    parser.add_argument("--title", default="My Reel", help="Reel title")

    args = parser.parse_args()
    create_reel(args.clips, args.output, args.title)
