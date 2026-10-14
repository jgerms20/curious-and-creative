"""Publishing: show notes, RSS feeds, host adapters and the public trust log.

  notes.py     show_notes(): markdown with sources, chapters and a verification summary
  feed.py      build_feed() / write_feed(): RSS 2.0 with iTunes and podcast-namespace tags
  hosts.py     HostAdapter, LocalHost, TransistorHost
  trustlog.py  append(): one public JSONL line per gate decision

Everything public lands under data/public/ (gitignored), laid out so that the folder can be
served as the site root:

  data/public/audio/<episode id>.mp3        https://<base>/audio/...
  data/public/transcripts/<name>            https://<base>/transcripts/...
  data/public/feeds/<show id>.xml           https://<base>/feeds/<show id>.xml
  data/public/trustlog/<show id>.jsonl      https://<base>/trustlog/<show id>.jsonl

<base> is env EARLOBE_PUBLIC_BASE_URL. When it is unset (dry runs) URLs point at
earlobe.invalid, which can never resolve.
"""
from __future__ import annotations

import os
from pathlib import Path

from earlobe import config

DEFAULT_BASE_URL = "https://earlobe.invalid"
PUBLISHER = "Curious & Creative LLC"


def public_base_url(base_url: str | None = None) -> str:
    """Where data/public/ is served from, no trailing slash."""
    return (base_url or os.environ.get("EARLOBE_PUBLIC_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def public_dir(*parts: str) -> Path:
    """data/public/<parts>, created on demand."""
    return config.data_dir("public", *parts)


def coerce(cls, obj):
    """A contract dataclass from either the dataclass itself or its dict form (the store returns dicts)."""
    return cls.from_dict(obj) if isinstance(obj, dict) else obj


def disclosure_text(show_cfg: dict | None = None) -> str:
    """The AI disclosure carried in metadata (editorial standards VOICE-4 / VOICE-5).

    A show can override it with `disclosure_text` in its config; the wording must keep the
    five points: AI-written and voiced, synthetic voices, automated fact checks against
    independent sources, sources and corrections in the notes, and who publishes.
    """
    show_cfg = show_cfg or {}
    if show_cfg.get("disclosure_text"):
        return str(show_cfg["disclosure_text"])
    name = show_cfg.get("name") or "This show"
    return ("This episode was written and voiced using AI. The voices you hear are synthetic, "
            "not real people. Facts were checked by automated systems against independent sources. "
            f"Sources and corrections are in the show notes. {name} is published by {PUBLISHER}.")


def corrections_url(show_id: str, base_url: str | None = None) -> str:
    """Public page where corrections for a show are posted."""
    return f"{public_base_url(base_url)}/corrections/{show_id}"
