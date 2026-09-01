# pyright: reportMissingImports=false
"""
Video with Background Music
============================
Adds background music to a video, with options for volume
control and fade in/out.

Usage:
    python add_music.py --video clip.mp4 --music background.mp3 --output with_music.mp4
"""

import argparse
from moviepy import VideoFileClip, AudioFileClip, afx


def add_background_music(
    video_path: str,
    music_path: str,
    output_path: str,
    music_volume: float = 0.3,
    fade_duration: float = 2.0,
):
    """Add background music to video."""

    video = VideoFileClip(video_path)
    music = AudioFileClip(music_path)

    # Loop music if shorter than video
    if music.duration < video.duration:
        loops_needed = int(video.duration / music.duration) + 1
        music = music.with_effects([afx.AudioLoop(loops_needed)])

    # Trim music to video length
    music = music.subclipped(0, video.duration)

    # Lower the volume
    music = music.with_effects([afx.MultiplyVolume(music_volume)])

    # Add fade in/out
    music = music.with_effects(
        [afx.AudioFadeIn(fade_duration), afx.AudioFadeOut(fade_duration)]
    )

    # Set audio on video
    final = video.with_audio(music)
    final.write_videofile(output_path, fps=video.fps, codec="libx264")

    video.close()
    music.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add background music to video")
    parser.add_argument("--video", required=True, help="Input video file")
    parser.add_argument("--music", required=True, help="Background music file")
    parser.add_argument("--output", default="with_music.mp4", help="Output file")
    parser.add_argument(
        "--volume", type=float, default=0.3, help="Music volume (0.0-1.0)"
    )
    parser.add_argument(
        "--fade", type=float, default=2.0, help="Fade duration in seconds"
    )

    args = parser.parse_args()
    add_background_music(args.video, args.music, args.output, args.volume, args.fade)
