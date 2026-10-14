"""Text to speech.

  ElevenLabsTTS  REST call per chunk of text, stdlib urllib, returns MP3 bytes
  DryRunTTS      silent MP3 whose length matches the estimated speaking time (words / 155 wpm)

Keys and the model come from the environment (ELEVENLABS_API_KEY and the variable
named by default_tts_model_env in config/voices.yaml). Voice IDs are per persona
and are resolved in mix.py. Nothing here is ever committed with a value.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod

from earlobe import config
from earlobe.studio import AudioError, est_seconds, ffmpeg, have_ffmpeg

log = logging.getLogger(__name__)

API_ROOT = "https://api.elevenlabs.io/v1"
OUTPUT_FORMAT = "mp3_44100_128"
MAX_CHARS = 4500                       # stay well under the per-request character limit
RETRY_STATUS = {429, 500, 502, 503, 504}

# One silent MPEG-1 Layer III frame (128 kbps, 44.1 kHz, 417 bytes). Ten of them make a
# ~0.26 s placeholder that any player accepts, for dry runs on machines without ffmpeg.
_SILENT_FRAME = b"\xff\xfb\x90\x04" + bytes(413)
PLACEHOLDER_MP3 = _SILENT_FRAME * 10


class TTSError(RuntimeError):
    """The speech service refused or failed a request."""


class TTS(ABC):
    """Interface: text and a voice id in, MP3 bytes out."""

    dry_run = False

    @abstractmethod
    def synthesize(self, text: str, voice_id: str) -> bytes: ...


# ---------------------------------------------------------------- chunking
_SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def chunk_text(text: str, limit: int = MAX_CHARS) -> list[str]:
    """Split text at sentence boundaries into pieces of at most `limit` characters.

    A single sentence longer than the limit is cut at the last space before it.
    """
    text = " ".join(text.split())
    if len(text) <= limit:
        return [text] if text else []
    chunks: list[str] = []
    cur = ""
    for sentence in _SENTENCE_END.split(text):
        while len(sentence) > limit:
            cut = sentence.rfind(" ", 0, limit)
            cut = cut if cut > 0 else limit
            if cur:
                chunks.append(cur)
                cur = ""
            chunks.append(sentence[:cut])
            sentence = sentence[cut:].lstrip()
        if not sentence:
            continue
        if cur and len(cur) + 1 + len(sentence) > limit:
            chunks.append(cur)
            cur = sentence
        else:
            cur = f"{cur} {sentence}" if cur else sentence
    if cur:
        chunks.append(cur)
    return chunks


# ---------------------------------------------------------------- ElevenLabs
def _post(url: str, headers: dict, payload: dict, timeout: int = 120) -> bytes:
    """The one network call. Tests replace this."""
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _error_text(err: urllib.error.HTTPError) -> str:
    try:
        return err.read().decode("utf-8", "replace")[:200]
    except (OSError, ValueError):
        return str(err.reason or "")


class ElevenLabsTTS(TTS):
    """POST /v1/text-to-speech/{voice_id}?output_format=mp3_44100_128 per chunk, MP3 bytes back."""

    def __init__(self, api_key: str | None = None, model_id: str | None = None, *,
                 max_chars: int = MAX_CHARS, retries: int = 3):
        model_env = config.load_voices().get("default_tts_model_env", "ELEVENLABS_TTS_MODEL")
        self.api_key = api_key or os.environ.get("ELEVENLABS_API_KEY", "")
        self.model_id = model_id or os.environ.get(model_env, "")
        self.max_chars = max_chars
        self.retries = max(1, retries)
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY is not set (dry runs use DryRunTTS and need no key)")
        if not self.model_id:
            raise ValueError(f"{model_env} is not set; put the text-to-speech model id in the environment")

    def synthesize(self, text: str, voice_id: str) -> bytes:
        if not voice_id:
            raise ValueError("voice_id is required")
        chunks = chunk_text(text, self.max_chars)
        if not chunks:
            raise ValueError("no text to synthesize")
        return b"".join(self._speak(c, voice_id) for c in chunks)

    def _speak(self, chunk: str, voice_id: str) -> bytes:
        voice = urllib.parse.quote(voice_id, safe="")
        url = f"{API_ROOT}/text-to-speech/{voice}?output_format={OUTPUT_FORMAT}"
        headers = {"xi-api-key": self.api_key, "Content-Type": "application/json",
                   "Accept": "audio/mpeg"}
        payload = {"text": chunk, "model_id": self.model_id}
        for attempt in range(self.retries):
            last = attempt == self.retries - 1
            try:
                return _post(url, headers, payload)
            except urllib.error.HTTPError as e:           # before URLError: it is a subclass
                if e.code in RETRY_STATUS and not last:
                    time.sleep(2 ** attempt)
                    continue
                raise TTSError(f"ElevenLabs HTTP {e.code}: {_error_text(e)}") from None
            except urllib.error.URLError as e:
                if not last:
                    time.sleep(2 ** attempt)
                    continue
                raise TTSError(f"ElevenLabs request failed: {e.reason}") from None
        raise TTSError("ElevenLabs request failed")        # unreachable; keeps type checkers calm


# ---------------------------------------------------------------- dry run
def silent_mp3(seconds: float) -> bytes:
    """Silent 44.1 kHz stereo 128 kbps MP3 of the given length (tiny placeholder without ffmpeg)."""
    if have_ffmpeg():
        try:
            return ffmpeg("-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{seconds:.2f}",
                          "-c:a", "libmp3lame", "-b:a", "128k", "-f", "mp3", "pipe:1").stdout
        except AudioError as e:
            log.warning("silent audio via ffmpeg failed, using placeholder: %s", e)
    return PLACEHOLDER_MP3


class DryRunTTS(TTS):
    """No keys, no network: silence as long as the text would take to say."""

    dry_run = True

    def synthesize(self, text: str, voice_id: str = "") -> bytes:
        return silent_mp3(max(0.3, round(est_seconds(text), 1)))
