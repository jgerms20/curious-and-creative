"""Studio: text to speech, mixing and mastering, plus the computer-use operator stub.

  tts.py       ElevenLabsTTS (REST, stdlib urllib) and DryRunTTS (silent audio, no keys)
  mix.py       render(): per-line speech + pauses -> one loudness-normalized MP3
  operator.py  StudioOperator interface for UI-only audio engines (stubs)

Real audio work needs ffmpeg and ffprobe on PATH. Dry runs degrade to a tiny
placeholder file when ffmpeg is missing; live runs refuse instead of shipping
audio that was never loudness-normalized.
"""
from __future__ import annotations

import shutil
import subprocess

SAMPLE_RATE = 44100
WORDS_PER_MINUTE = 155


class AudioError(RuntimeError):
    """ffmpeg / ffprobe is missing or failed."""


def have_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def have_ffprobe() -> bool:
    return shutil.which("ffprobe") is not None


def run_tool(args: list[str]) -> subprocess.CompletedProcess:
    """Run a command, capturing output. Raises AudioError (with the tail of stderr) on failure."""
    try:
        proc = subprocess.run([str(a) for a in args], capture_output=True, check=False)
    except FileNotFoundError as e:
        raise AudioError(f"{args[0]} not found on PATH") from e
    if proc.returncode != 0:
        tail = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-5:]
        raise AudioError(f"{args[0]} failed ({proc.returncode}): " + " | ".join(tail))
    return proc


def ffmpeg(*args, loglevel: str = "error") -> subprocess.CompletedProcess:
    """ffmpeg with the flags every call wants: no banner, no stdin prompts, overwrite."""
    return run_tool(["ffmpeg", "-hide_banner", "-nostdin", "-nostats", "-loglevel", loglevel, "-y", *args])


def est_seconds(text: str, wpm: int = WORDS_PER_MINUTE) -> float:
    """Speaking time for a piece of text at a words-per-minute pace."""
    return len(text.split()) / wpm * 60
