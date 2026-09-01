# pyright: reportMissingImports=false
"""
Watermark Adder
===============
Add a logo/watermark overlay to video. Supports positioning
and opacity control.

Usage:
    python watermark.py --video clip.mp4 --logo logo.png --output watermarked.mp4
"""

import argparse
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip


def add_watermark(
    video_path: str,
    logo_path: str,
    output_path: str,
    position: str = "bottom-right",
    opacity: float = 0.8,
    scale: float = 0.15,
):
    """Add watermark/logo to video."""

    video = VideoFileClip(video_path)

    # Create watermark from logo
    watermark = ImageClip(logo_path)

    # Scale watermark relative to video size
    target_width = int(video.w * scale)
    watermark = watermark.resized(width=target_width)

    # Set opacity
    watermark = watermark.with_opacity(opacity)

    # Position: top-left, top-right, bottom-left, bottom-right, center
    position_map = {
        "top-left": ("left", "top"),
        "top-right": ("right", "top"),
        "bottom-left": ("left", "bottom"),
        "bottom-right": ("right", "bottom"),
        "center": ("center", "center"),
    }

    pos = position_map.get(position, ("right", "bottom"))
    watermark = watermark.with_position(pos)

    # Make watermark duration match video
    watermark = watermark.with_duration(video.duration)

    # Composite
    final = CompositeVideoClip([video, watermark])
    final.write_videofile(output_path, fps=video.fps, codec="libx264")

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add watermark to video")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--logo", required=True, help="Logo/watermark image")
    parser.add_argument("--output", default="watermarked.mp4", help="Output file")
    parser.add_argument(
        "--position",
        default="bottom-right",
        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
        help="Watermark position",
    )
    parser.add_argument(
        "--opacity", type=float, default=0.8, help="Watermark opacity (0-1)"
    )
    parser.add_argument(
        "--scale", type=float, default=0.15, help="Scale relative to video width"
    )

    args = parser.parse_args()
    add_watermark(
        args.video, args.logo, args.output, args.position, args.opacity, args.scale
    )
