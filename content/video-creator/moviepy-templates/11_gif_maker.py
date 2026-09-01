# pyright: reportMissingImports=false
"""
Gif Maker - Convert Video to Animated GIF
==========================================
Convert video clips to animated GIFs with optional
size and duration controls.

Usage:
    python gif_maker.py --video clip.mp4 --output animation.gif
"""

import argparse
from typing import Optional

from moviepy import VideoFileClip


def create_gif(
    video_path: str,
    output_path: str,
    duration: Optional[float] = None,
    width: Optional[int] = None,
    fps: int = 15,
):
    """Convert video to GIF."""

    video = VideoFileClip(video_path)

    # Optional duration limit
    if duration:
        video = video.subclipped(0, duration)

    # Optional resize
    if width:
        video = video.resized(width=width)

    video.write_gif(output_path, fps=fps)

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create GIF from video")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", default="animation.gif", help="Output GIF file")
    parser.add_argument(
        "--duration", type=float, default=None, help="Max duration in seconds"
    )
    parser.add_argument("--width", type=int, default=None, help="GIF width in pixels")
    parser.add_argument("--fps", type=int, default=15, help="GIF frame rate")

    args = parser.parse_args()
    create_gif(args.video, args.output, args.duration, args.width, args.fps)
