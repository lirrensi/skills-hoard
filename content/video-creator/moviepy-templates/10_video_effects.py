# pyright: reportMissingImports=false
"""
Video Effects - Apply Visual Effects
===================================
Apply various visual effects to video: B&W, sepia, blur,
color correction, and more.

Usage:
    python video_effects.py --video clip.mp4 --effect grayscale --output bw.mp4
"""

import argparse
from moviepy import VideoFileClip, vfx


def apply_effect(video_path: str, output_path: str, effect: str):
    """Apply visual effect to video."""

    video = VideoFileClip(video_path)

    effect_map = {
        "grayscale": vfx.BlackAndWhite,
        "mirrorx": vfx.MirrorX,
        "mirrory": vfx.MirrorY,
        "invert": vfx.InvertColors,
        "blur": lambda: vfx.Blur(lambda t: min(t * 2, 3)),  # Progressive blur
        "painting": vfx.Painting,
    }

    if effect not in effect_map:
        print(f"Available effects: {', '.join(effect_map.keys())}")
        return

    effect_func = effect_map[effect]
    modified = video.with_effects([effect_func()])

    modified.write_videofile(output_path, fps=video.fps, codec="libx264")

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply effect to video")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", default="with_effect.mp4", help="Output file")
    parser.add_argument(
        "--effect",
        required=True,
        choices=["grayscale", "mirrorx", "mirrory", "invert", "blur", "painting"],
        help="Effect to apply",
    )

    args = parser.parse_args()
    apply_effect(args.video, args.output, args.effect)
