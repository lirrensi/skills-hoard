# pyright: reportMissingImports=false
"""
Image Slideshow with Ken Burns Effect
=====================================
Creates a dynamic slideshow from images with pan/zoom
(Ken Burns effect) and optional captions.

Usage:
    python slideshow.py --images img1.jpg img2.jpg --output slideshow.mp4
"""

import argparse
from typing import Optional

from moviepy import ImageClip, TextClip, concatenate_videoclips, vfx


def create_slideshow(
    image_paths: list,
    output_path: str,
    slide_duration: float = 5.0,
    video_fps: int = 30,
    caption: Optional[str] = None,
):
    """Create slideshow with Ken Burns effect from images."""

    clips = []

    for i, img_path in enumerate(image_paths):
        # Create base clip
        clip = ImageClip(img_path).with_duration(slide_duration)

        # Resize to fill (cover)
        clip = clip.resized(height=1080)
        if clip.w > 1920:
            clip = clip.cropped(width=1920, x1=(clip.w - 1920) // 2)

        # Ken Burns: zoom in slowly
        clip = clip.with_effects(
            [
                vfx.Resize(lambda t: 1 + 0.1 * t)  # Zoom from 100% to 150%
            ]
        )

        # Add fade transition to next slide
        if i < len(image_paths) - 1:
            clip = clip.with_effects([vfx.FadeOut(0.5)])

        clips.append(clip)

    # Add title caption if provided
    if caption:
        title = (
            TextClip(
                font="Arial.ttf",
                text=caption,
                font_size=72,
                color="white",
                stroke_color="black",
                stroke_width=2,
            )
            .with_duration(slide_duration * len(image_paths))
            .with_position("center")
        )
        clips.insert(0, title)

    # Concatenate
    final = concatenate_videoclips(clips)
    final.write_videofile(output_path, fps=video_fps, codec="libx264")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create image slideshow")
    parser.add_argument("--images", nargs="+", required=True, help="Input image files")
    parser.add_argument("--output", default="slideshow.mp4", help="Output file")
    parser.add_argument(
        "--duration", type=float, default=5.0, help="Duration per slide"
    )
    parser.add_argument("--fps", type=int, default=30, help="Output FPS")
    parser.add_argument("--caption", default=None, help="Title caption")

    args = parser.parse_args()
    create_slideshow(args.images, args.output, args.duration, args.fps, args.caption)
