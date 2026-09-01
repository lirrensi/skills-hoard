# pyright: reportMissingImports=false
"""
Picture-in-Picture (PiP)
========================
Create picture-in-picture effect with a smaller video
overlay on top of a main video.

Usage:
    python pip.py --main main.mp4 --pip overlay.mp4 --output pip_video.mp4
"""

import argparse
from typing import Optional

from moviepy import VideoFileClip, CompositeVideoClip, vfx


def create_pip(
    main_path: str,
    pip_path: str,
    output_path: str,
    pip_position: str = "bottom-right",
    pip_scale: float = 0.25,
    pip_start: float = 0,
    pip_duration: Optional[float] = None,
):
    """Create picture-in-picture effect."""

    main_video = VideoFileClip(main_path)
    pip_video = VideoFileClip(pip_path)

    # Scale PiP video
    target_width = int(main_video.w * pip_scale)
    pip_video = pip_video.resized(width=target_width)

    # Position PiP
    margin = 20  # Margin from edges
    position_map = {
        "top-left": (margin, margin),
        "top-right": (main_video.w - pip_video.w - margin, margin),
        "bottom-left": (margin, main_video.h - pip_video.h - margin),
        "bottom-right": (
            main_video.w - pip_video.w - margin,
            main_video.h - pip_video.h - margin,
        ),
        "center": (
            (main_video.w - pip_video.w) // 2,
            (main_video.h - pip_video.h) // 2,
        ),
    }

    pos = position_map.get(
        pip_position,
        (main_video.w - pip_video.w - margin, main_video.h - pip_video.h - margin),
    )
    pip_video = pip_video.with_position(pos)

    # Set timing
    if pip_duration is None:
        pip_duration = min(pip_video.duration, main_video.duration - pip_start)

    pip_video = pip_video.with_duration(pip_duration).with_start(pip_start)

    # Add border/frame to PiP
    pip_video = pip_video.with_effects(
        [vfx.Margin(left=5, right=5, top=5, bottom=5, color=(255, 255, 255))]
    )

    # Composite
    final = CompositeVideoClip([main_video, pip_video])
    final.write_videofile(output_path, fps=main_video.fps, codec="libx264")

    main_video.close()
    pip_video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create picture-in-picture video")
    parser.add_argument("--main", required=True, help="Main video file")
    parser.add_argument("--pip", required=True, help="PiP overlay video file")
    parser.add_argument("--output", default="pip_video.mp4", help="Output file")
    parser.add_argument(
        "--position",
        default="bottom-right",
        choices=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
        help="PiP position",
    )
    parser.add_argument(
        "--scale", type=float, default=0.25, help="PiP scale relative to main video"
    )
    parser.add_argument(
        "--start", type=float, default=0, help="PiP start time in seconds"
    )
    parser.add_argument(
        "--duration", type=float, default=None, help="PiP duration in seconds"
    )

    args = parser.parse_args()
    create_pip(
        args.main,
        args.pip,
        args.output,
        args.position,
        args.scale,
        args.start,
        args.duration,
    )
