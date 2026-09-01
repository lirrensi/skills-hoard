"""Smoke tests — verify the supertonic CLI is installed and responsive.

Run with:
    uv run pytest tests/ -v
"""

import subprocess
import shutil
import sys

import pytest


def test_supertonic_installed():
    """supertonic CLI should be on PATH and respond."""
    assert shutil.which("supertonic") is not None, (
        "supertonic not found on PATH. Install: pip install supertonic"
    )


def test_help():
    """--help should exit 0 and list expected commands."""
    result = subprocess.run(
        ["supertonic", "--help"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "tts" in result.stdout
    assert "say" in result.stdout
    assert "list-voices" in result.stdout


def test_version():
    """--version should show version info."""
    result = subprocess.run(
        ["supertonic", "version"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip(), "Expected version output"


def test_tts_subcommand_help():
    """supertonic tts --help should show all TTS flags."""
    result = subprocess.run(
        ["supertonic", "tts", "--help"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    for flag in ["--output", "--voice", "--lang", "--steps", "--speed"]:
        assert flag in result.stdout, f"Expected flag {flag} in tts --help"


def test_say_subcommand_help():
    """supertonic say --help should show say flags."""
    result = subprocess.run(
        ["supertonic", "say", "--help"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert "--voice" in result.stdout


@pytest.mark.skipif(
    sys.platform == "win32" and not shutil.which("powershell"),
    reason="PowerShell not available for audio playback on this system",
)
def test_list_voices():
    """list-voices should fetch and display available voices."""
    result = subprocess.run(
        ["supertonic", "list-voices"],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0
