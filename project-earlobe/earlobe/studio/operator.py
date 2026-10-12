"""Studio Operator: interface for audio engines that only have a web UI.

Some engines (Google's NotebookLM audio overviews, Meta's Muse) have no API we can
call. The plan is to drive them with a computer-use agent (agents/studio/studio-operator.md,
status `future`). This module only fixes the shape so the rest of the engine can be
written against it today.

Two rules that make these engines different from our own studio:

  1. They write their own words. The script's claim map does not exist for that audio,
     so the output is transcribed (STT), turned back into a Script, and sent through the
     FULL trust stack (claims -> verifier -> fact check -> bias -> legal -> gate) like any
     other draft. Nothing from an operator publishes on its own authority.
  2. Their terms decide whether we may use them at all. See the ToS check on each class.

Best fit when built: evergreen deep dives and bonus episodes. Not news.
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from pathlib import Path

from earlobe import config
from earlobe.studio.tts import DryRunTTS


class StudioOperator(ABC):
    """Interface for a computer-use audio engine.

    produce() takes either a Script (spoken text) or a research pack / list of sources
    (the engine writes its own) and returns the path of the audio file it produced.
    Implementations must:
      * check the kill switch and the budget before starting, and stop cleanly if told to;
      * read credentials from the environment only, never from files in the repo;
      * leave the raw audio on disk and return its path; the caller transcribes it and
        runs the trust loop before anything publishes;
      * add our own AI disclosure segment (our TTS, a persona voice) before release.
    """

    engine = ""                 # short id, e.g. "notebooklm"
    tos_cleared = False         # flip to True only after Compliance & Platform Policy Watch signs off

    @abstractmethod
    def produce(self, script_or_sources) -> str:
        """Return the path of the generated audio file."""


class NotebookLMOperator(StudioOperator):
    """NotebookLM audio overview, driven through its web UI.

    Computer-use plan (not built):
      1. Preflight: kill switch, budget, and a recorded ToS clearance (below).
      2. Open a fresh notebook in a sandboxed browser session signed in with credentials
         from the environment.
      3. Add sources: URLs from the gated research pack, plus our own plain-language
         summaries. Never paste full article text.
      4. Start the audio overview, wait for it to finish, download the file.
      5. Return the path. The caller transcribes it, rebuilds a Script and runs the
         trust loop; REWRITE is not possible here (we cannot edit their words), so a
         failed gate means the audio is discarded, not patched.

    ToS check (do this before writing any code; terms change, verify as of the build date):
      * Does Google allow automated or agent-driven use of the web app?
      * May generated audio be distributed commercially, and is attribution required?
      * Are there limits on who may use the product, or on volume?
    Until a human records "yes" to all three, `tos_cleared` stays False.
    """

    engine = "notebooklm"

    def produce(self, script_or_sources) -> str:
        raise NotImplementedError(
            "NotebookLMOperator is a documented stub: see the class docstring for the computer-use "
            "plan and the terms-of-service check that must pass first.")


class MetaMuseOperator(StudioOperator):
    """Meta's Muse audio engine, driven through its web UI.

    Same plan as NotebookLMOperator (preflight, upload gated sources, generate, download,
    return the path, then transcribe and run the full trust loop).

    ToS check, and one extra step: confirm the product and its current terms exist in the
    form we assume. The name comes from the project brief, not from a terms page we have read.
    Also check whether the terms allow automated access and commercial redistribution of the
    output, and how the engine's voices must be disclosed. Keep `tos_cleared` False until a
    human has recorded the answers.
    """

    engine = "meta-muse"

    def produce(self, script_or_sources) -> str:
        raise NotImplementedError(
            "MetaMuseOperator is a documented stub: see the class docstring for the computer-use "
            "plan and the terms-of-service check that must pass first.")


class DryRunOperator(StudioOperator):
    """No-network stand-in so the interface can be exercised: silent audio sized from the text."""

    engine = "dry-run"
    tos_cleared = True

    def produce(self, script_or_sources) -> str:
        lines = getattr(script_or_sources, "lines", None)
        text = " ".join(l.text for l in lines) if lines else str(script_or_sources)
        out = config.data_dir("audio", "operator") / f"{self.engine}-{int(time.time() * 1000)}.mp3"
        Path(out).write_bytes(DryRunTTS().synthesize(text))
        return str(out)
