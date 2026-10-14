"""Mixing and mastering: a Script and a TTS engine in, one broadcast-ready MP3 out.

  1. Each script line is spoken with its persona's voice (voice id from the env var named
     by voice_id_env in config/voices.yaml) and decoded to 44.1 kHz stereo PCM.
  2. Short pauses go between lines: longer when the speaker or segment changes.
  3. ffmpeg joins everything (concat), optionally lays a music bed under the intro and
     outro (ducked by the voice), then masters to -16 LUFS integrated, -1.5 dBTP,
     LRA 11, 44.1 kHz stereo, MP3 128 kbps. Loudness is measured first and applied
     in a second pass (linear), with a one-pass fallback for audio it cannot measure.

With DryRunTTS this runs end to end with no keys and no network. Without ffmpeg a
dry run falls back to a tiny placeholder file; a live run raises AudioError.
"""
from __future__ import annotations

import json
import logging
import math
import os
import re
import tempfile
import wave
from pathlib import Path

from earlobe import config
from earlobe.schemas import Script
from earlobe.studio import (
    SAMPLE_RATE,
    AudioError,
    ffmpeg,
    have_ffmpeg,
    have_ffprobe,
    run_tool,
)
from earlobe.studio.tts import TTS

log = logging.getLogger(__name__)

# pauses, in seconds
PAUSE_SAME_SPEAKER = 0.25
PAUSE_SPEAKER_CHANGE = 0.40
PAUSE_SEGMENT_CHANGE = 0.80

# loudness targets (EBU R128 style, podcast friendly)
TARGET_I, TARGET_TP, TARGET_LRA = -16, -1.5, 11

# music bed: played only under the intro and outro, ducked whenever someone talks
INTRO_SEGMENTS = {"cold_open", "intro"}
OUTRO_SEGMENTS = {"disclosure", "outro"}
MUSIC_LEAD = 2.0        # seconds of music before the first word
MUSIC_TAIL = 3.0        # seconds of music after the last word
MUSIC_GAIN = 0.35       # bed level before ducking (linear)
MUSIC_FADE = 1.5        # fade in / out at the edge of each music window
MIN_WINDOW = 0.5

AI_TAG = "AI-generated audio. Voices are synthetic."


# ---------------------------------------------------------------- voices
def voice_id_for(voices: dict, speaker: str, segment: str = "", *, strict: bool = True) -> str:
    """ElevenLabs voice id for a persona, read from the env var named in voices.yaml.

    An unknown persona is always an error. A missing env var is an error unless strict=False
    (dry runs, where the voice id is never used).
    """
    personas = voices.get("personas", {})
    if speaker not in personas and segment == "disclosure":
        speaker = voices.get("disclosure_voice", speaker)
    if speaker not in personas:
        raise ValueError(f"speaker {speaker!r} is not a persona in config/voices.yaml")
    env = personas[speaker].get("voice_id_env", "")
    voice = os.environ.get(env, "") if env else ""
    if not voice and strict:
        raise ValueError(f"set {env or 'voice_id_env'} to the voice id for persona {speaker!r}")
    return voice


# ---------------------------------------------------------------- small audio helpers
def _wav_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as w:
        return w.getnframes() / w.getframerate()


def _write_silence(path: Path, seconds: float) -> None:
    """A stereo 16-bit PCM WAV of silence, matching the decoded speech format."""
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(bytes(4 * round(seconds * SAMPLE_RATE)))


def probe_duration(path: str | Path) -> float | None:
    """Duration in seconds via ffprobe; None if ffprobe is missing or cannot read the file."""
    if not have_ffprobe():
        return None
    try:
        out = run_tool(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path]).stdout.decode().strip()
        return float(out)
    except (AudioError, ValueError):
        return None


def _pause_after(prev, nxt) -> float:
    if prev.segment != nxt.segment:
        return PAUSE_SEGMENT_CHANGE
    return PAUSE_SAME_SPEAKER if prev.speaker == nxt.speaker else PAUSE_SPEAKER_CHANGE


# ---------------------------------------------------------------- music windows and filters
def _merge(windows: list[tuple[float, float]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for a, b in sorted(windows):
        if out and a <= out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], b))
        else:
            out.append((a, b))
    return [w for w in out if w[1] - w[0] >= MIN_WINDOW]


def music_windows(spans: list[tuple[str, float, float]], total: float,
                  lead: float = MUSIC_LEAD, tail: float = MUSIC_TAIL) -> list[tuple[float, float]]:
    """Where the bed plays. spans = [(segment, start, end)] for each spoken line (times in the final timeline).

    Intro window: from 0 to the end of the leading cold_open/intro lines (or just the lead-in).
    Outro window: from the start of the trailing disclosure/outro lines (or just the tail) to the end.
    """
    head = 0
    while head < len(spans) and spans[head][0] in INTRO_SEGMENTS:
        head += 1
    foot = len(spans)
    while foot > head and spans[foot - 1][0] in OUTRO_SEGMENTS:
        foot -= 1
    intro_end = spans[head - 1][2] if head else lead
    outro_start = spans[foot][1] if foot < len(spans) else total - tail
    return _merge([(0.0, intro_end), (max(outro_start - 0.5, 0.0), total)])


def _gain_expr(windows: list[tuple[float, float]]) -> str:
    """ffmpeg volume expression: a smooth 0..MUSIC_GAIN envelope that is non-zero only inside the windows."""
    f = MUSIC_FADE
    terms = "+".join(f"max(0,min(1,min((t-{a:.3f})/{f},({b:.3f}-t)/{f})))" for a, b in windows)
    return f"{MUSIC_GAIN}*({terms})"


def _graph(windows: list[tuple[float, float]] | None) -> str:
    """Filter graph from the voice (input 0) and optional music (input 1) to the label [pre]."""
    if not windows:
        return "[0:a]anull[pre]"
    return (f"[1:a]aformat=sample_rates={SAMPLE_RATE}:channel_layouts=stereo,"
            f"volume='{_gain_expr(windows)}':eval=frame[mus];"
            "[0:a]asplit=2[vo][key];"
            "[mus][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=400:makeup=1[duck];"
            "[vo][duck]amix=inputs=2:duration=first:normalize=0[pre]")


def _measure(stderr: str) -> dict | None:
    """Parse loudnorm's JSON report; None if any value is not finite (silence, too short, ...)."""
    for block in reversed(re.findall(r"\{[^{}]*\}", stderr, re.DOTALL)):
        try:
            data = json.loads(block)
            vals = {k: float(data[k]) for k in
                    ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")}
        except (ValueError, KeyError):
            continue
        return vals if all(math.isfinite(v) for v in vals.values()) else None
    return None


def _loudnorm(measured: dict | None = None, *, report: bool = False) -> str:
    """The loudnorm filter: pass 1 (report=True) prints measurements, pass 2 applies them."""
    base = f"loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}"
    if report:
        return base + ":print_format=json"
    if measured:
        base += (f":measured_I={measured['input_i']}:measured_TP={measured['input_tp']}"
                 f":measured_LRA={measured['input_lra']}:measured_thresh={measured['input_thresh']}"
                 f":offset={measured['target_offset']}:linear=true")
    return f"{base},aresample={SAMPLE_RATE}"


# ---------------------------------------------------------------- render
def _speak_lines(script: Script, voices: dict, tts: TTS, tmp: Path) -> list[tuple[object, Path, float]]:
    """Synthesize every non-empty line to a decoded WAV: [(line, wav_path, seconds)]."""
    out = []
    for i, line in enumerate(script.lines):
        text = (line.text or "").strip()
        if not text:
            continue
        voice = voice_id_for(voices, line.speaker, line.segment, strict=not tts.dry_run)
        mp3, wav = tmp / f"line_{i:04d}.mp3", tmp / f"line_{i:04d}.wav"
        mp3.write_bytes(tts.synthesize(text, voice))
        ffmpeg("-i", mp3, "-ar", SAMPLE_RATE, "-ac", 2, "-c:a", "pcm_s16le", wav)
        out.append((line, wav, _wav_seconds(wav)))
    return out


def _render_placeholder(script: Script, voices: dict, tts: TTS, out: Path) -> tuple[str, int]:
    """Dry run on a machine without ffmpeg: raw MP3 frames joined, duration estimated from the words."""
    if not tts.dry_run:
        raise AudioError("ffmpeg is required to mix and normalize audio; install it, or use --dry-run")
    log.warning("ffmpeg not found: writing a placeholder file instead of a mixed episode")
    data = b"".join(tts.synthesize(l.text, "") for l in script.lines if (l.text or "").strip())
    out.write_bytes(data)
    return str(out), script.est_duration_sec()


def render(script: Script, voices: dict | None, tts: TTS, out_path: str | Path,
           music_bed: str | Path | None = None) -> tuple[str, int]:
    """Speak, join, master. Returns (path to the MP3, duration in whole seconds)."""
    if isinstance(script, dict):
        script = Script.from_dict(script)
    voices = voices or config.load_voices()
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not any((l.text or "").strip() for l in script.lines):
        raise ValueError("script has no speakable lines")
    if music_bed is not None and not Path(music_bed).is_file():
        raise FileNotFoundError(f"music bed not found: {music_bed}")
    if not have_ffmpeg():
        return _render_placeholder(script, voices, tts, out)

    with tempfile.TemporaryDirectory(prefix="earlobe-mix-") as td:
        tmp = Path(td)
        spoken = _speak_lines(script, voices, tts, tmp)

        # timeline: [lead] line (pause line)* [tail], remembering where each line sits
        files: list[Path] = []
        spans: list[tuple[str, float, float]] = []
        clock = 0.0

        def add_silence(seconds: float) -> None:
            nonlocal clock
            path = tmp / f"gap_{len(files):04d}.wav"
            _write_silence(path, seconds)
            files.append(path)
            clock += seconds

        if music_bed:
            add_silence(MUSIC_LEAD)
        for n, (line, wav, seconds) in enumerate(spoken):
            if n:
                add_silence(_pause_after(spoken[n - 1][0], line))
            files.append(wav)
            spans.append((line.segment, clock, clock + seconds))
            clock += seconds
        if music_bed:
            add_silence(MUSIC_TAIL)
        total = clock

        listing = tmp / "list.txt"
        listing.write_text("".join("file '{}'\n".format(str(p).replace("'", "'\\''")) for p in files),
                           encoding="utf-8")
        inputs = ["-f", "concat", "-safe", 0, "-i", listing]
        graph = _graph(music_windows(spans, total) if music_bed else None)
        if music_bed:
            inputs += ["-stream_loop", -1, "-i", music_bed]

        # pass 1: measure loudness of the final mix; pass 2: apply it and encode
        probe = ffmpeg(*inputs, "-filter_complex", f"{graph};[pre]{_loudnorm(report=True)}[out]",
                       "-map", "[out]", "-t", f"{total:.3f}", "-f", "null", "-", loglevel="info")
        measured = _measure(probe.stderr.decode("utf-8", "replace"))
        part = out.with_name(out.name + ".part")
        ffmpeg(*inputs, "-filter_complex", f"{graph};[pre]{_loudnorm(measured)}[out]", "-map", "[out]",
               "-t", f"{total:.3f}", "-ar", SAMPLE_RATE, "-ac", 2, "-c:a", "libmp3lame", "-b:a", "128k",
               "-metadata", f"title={script.title}", "-metadata", f"comment={AI_TAG}", "-f", "mp3", part)
        os.replace(part, out)

    measured_len = probe_duration(out)
    return str(out), round(measured_len if measured_len is not None else total)
