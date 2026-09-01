# pyright: reportMissingImports=false
"""
Video Merger - Combine Multiple Videos
======================================
Merges multiple video files into one continuous video.
Supports different resolutions - will auto-scale to match.

Usage:
    python merge_videos.py --videos clip1.mp4 clip2.mp4 --output merged.mp4
"""

import argparse
from moviepy import VideoFileClip, concatenate_videoclips, vfx


def merge_videos(video_paths: list, output_path: str, transition_duration: float = 0.5):
    """Merge multiple videos with optional fade transitions."""

    clips = []
    for path in video_paths:
        clip = VideoFileClip(path)

        # Add crossfade between clips
        if transition_duration > 0 and len(clips) > 0:
            # Fade out previous clip
            clips[-1] = clips[-1].with_effects([vfx.FadeOut(transition_duration)])
            # Fade in new clip
            clip = clip.with_effects([vfx.FadeIn(transition_duration)])

        clips.append(clip)

    # Concatenate all clips
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, fps=24, codec="libx264")

    # Cleanup
    for clip in clips:
        clip.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge multiple videos")
    parser.add_argument("--videos", nargs="+", required=True, help="Input video files")
    parser.add_argument("--output", default="merged.mp4", help="Output file")
    parser.add_argument(
        "--transition", type=float, default=0.5, help="Fade transition duration"
    )

    args = parser.parse_args()
    merge_videos(args.videos, args.output, args.transition)
