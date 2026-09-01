# pyright: reportMissingImports=false
"""
Video Speed Changer - Speed Up or Slow Down
==========================================
Changes video speed (slow motion or timelapse).

Usage:
    python change_speed.py --video clip.mp4 --factor 2.0 --output fast_clip.mp4
    # factor > 1 = faster, factor < 1 = slower
"""

import argparse
from moviepy import VideoFileClip, vfx


def change_speed(video_path: str, output_path: str, factor: float = 1.0):
    """Change video speed. factor > 1 = faster, factor < 1 = slower."""

    video = VideoFileClip(video_path)

    # Speed change using with_speed_scaled
    # factor of 2 = 2x speed (half duration)
    # factor of 0.5 = 0.5x speed (double duration)
    modified = video.with_speed_scaled(factor)

    modified.write_videofile(output_path, fps=video.fps, codec="libx264")

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Change video speed")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", default="speed_changed.mp4", help="Output file")
    parser.add_argument(
        "--factor",
        type=float,
        default=1.0,
        help="Speed factor (2.0 = 2x faster, 0.5 = 2x slower)",
    )

    args = parser.parse_args()
    change_speed(args.video, args.output, args.factor)
