# pyright: reportMissingImports=false
"""
Video Trimmer - Cut and Trim Videos
===================================
Simple video cutting tool. Extract specific portions
or remove unwanted sections.

Usage:
    python trimmer.py --video clip.mp4 --start 10 --end 30 --output trimmed.mp4
"""

import argparse
from typing import Optional

from moviepy import VideoFileClip


def trim_video(
    video_path: str,
    output_path: str,
    start: Optional[float] = None,
    end: Optional[float] = None,
):
    """Trim video to specified start/end times."""

    video = VideoFileClip(video_path)

    # Default to full video if not specified
    if start is None:
        start = 0
    if end is None:
        end = video.duration

    # Extract subclip
    trimmed = video.subclipped(start, end)

    trimmed.write_videofile(output_path, fps=video.fps, codec="libx264")

    video.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trim video")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--output", default="trimmed.mp4", help="Output file")
    parser.add_argument(
        "--start", type=float, default=None, help="Start time in seconds"
    )
    parser.add_argument("--end", type=float, default=None, help="End time in seconds")

    args = parser.parse_args()
    trim_video(args.video, args.output, args.start, args.end)
