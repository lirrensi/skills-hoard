# pyright: reportMissingImports=false
"""
Video Resizer - Change Resolution
=================================
Resize video to different resolutions (4K, 1080p, 720p, etc.)
or convert between aspect ratios.

Usage:
    python resizer.py --video clip.mp4 --width 1920 --height 1080 --output resized.mp4
"""

import argparse
from typing import Optional

from moviepy import VideoFileClip


def resize_video(
    video_path: str,
    output_path: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
):
    """Resize video to specified dimensions."""

    video = VideoFileClip(video_path)

    if width and height:
        # Resize to exact dimensions
        resized = video.resized((width, height))
    elif width:
        # Resize to specific width, maintain aspect
        resized = video.resized(width=width)
    elif height:
        # Resize to specific height, maintain aspect
        resized = video.resized(height=height)
    else:
        print("Please specify --width and/or --height")
        return

    resized.write_videofile(output_path, fps=video.fps, codec="libx264")

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize video")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", default="resized.mp4", help="Output file")
    parser.add_argument(
        "--width", type=int, default=None, help="Target width in pixels"
    )
    parser.add_argument(
        "--height", type=int, default=None, help="Target height in pixels"
    )

    args = parser.parse_args()
    resize_video(args.video, args.output, args.width, args.height)
