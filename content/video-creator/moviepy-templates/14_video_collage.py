# pyright: reportMissingImports=false
"""
Video Collage / Grid Layout
===========================
Create video collages with multiple videos in a grid layout.
Supports 2x1, 1x2, 2x2, and custom grid layouts.

Usage:
    python collage.py --videos clip1.mp4 clip2.mp4 clip3.mp4 clip4.mp4 --layout 2x2 --output collage.mp4
"""

import argparse
from moviepy import ColorClip, VideoFileClip, clips_array


def create_collage(video_paths: list, output_path: str, layout: str = "2x2"):
    """Create video collage in grid layout."""

    # Load and normalize videos to same height
    videos = []
    target_height = 720  # Standard height

    for path in video_paths:
        clip = VideoFileClip(path)
        # Take first 10 seconds if longer
        if clip.duration > 10:
            clip = clip.subclipped(0, 10)
        # Resize to target height, maintain aspect
        clip = clip.resized(height=target_height)
        videos.append(clip)

    # Parse layout (e.g., "2x2", "2x1", "1x3")
    try:
        rows, cols = map(int, layout.lower().split("x"))
    except:
        rows, cols = 2, 2

    # Build grid
    if len(videos) == 1:
        # Single video
        final = videos[0]
    elif len(videos) == 2:
        if rows == 1 or cols == 1:
            # Side by side or stacked
            final = clips_array([videos])
        else:
            # 2x1 or 1x2
            if rows == 2:
                final = clips_array([[videos[0]], [videos[1]]])
            else:
                final = clips_array([videos])
    elif len(videos) == 3:
        if rows == 2:
            # 2 rows: 2 on top, 1 on bottom (centered)
            row1 = [videos[0]]
            if cols >= 2 and len(videos) > 1:
                row1.append(videos[1])
            row2 = [videos[2]] if len(videos) > 2 else []
            final = clips_array([row1, row2])
        else:
            final = clips_array([videos])
    elif len(videos) >= 4:
        # Build proper grid
        grid = []
        for i in range(rows):
            row = videos[i * cols : (i + 1) * cols]
            # Pad if incomplete row
            while len(row) < cols:
                # Create black filler
                filler = ColorClip(size=videos[0].size, color=(0, 0, 0)).with_duration(
                    videos[0].duration
                )
                row.append(filler)
            grid.append(row)
        final = clips_array(grid)
    else:
        print(f"Need at least 1 video, got {len(video_paths)}")
        return

    final.write_videofile(output_path, fps=24, codec="libx264")

    for clip in videos:
        clip.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create video collage")
    parser.add_argument("--videos", nargs="+", required=True, help="Input video files")
    parser.add_argument("--output", default="collage.mp4", help="Output file")
    parser.add_argument(
        "--layout", default="2x2", help="Grid layout (e.g., 2x2, 2x1, 1x3)"
    )

    args = parser.parse_args()
    create_collage(args.videos, args.output, args.layout)
