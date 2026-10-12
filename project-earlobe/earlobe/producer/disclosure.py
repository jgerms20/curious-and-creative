"""Disclosure agent: the spoken AI disclosure that closes every episode.

Plain code, no model, no network. The text covers what the editorial standards (VOICE-4)
require: the show is made with an automated newsroom and AI-generated voices, the voices are
synthetic, every claim was checked against independent sources, sources and corrections are in
the show notes, how to report an error, and who is responsible (Curious & Creative LLC).

Three variants, chosen by show format:
  daily     daily briefs and court roundups
  breaking  the Breaking Desk (adds: details may change, the next report says what changed)
  archive   true-crime and history (adds: built from records, thin spots are flagged)
Strict-lane shows also get the presumption-of-innocence line.

The lines are spoken by voices.yaml `disclosure_voice`, in segment "disclosure", with no
claim_ids. Wording is versioned here; change it in one place and every episode follows.
"""
from __future__ import annotations

import dataclasses

from earlobe.schemas import Script, ScriptLine, make_id

DEFAULT_NETWORK = "Curious & Creative Network"
PUBLISHER = "Curious and Creative LLC"

# {show} and {network} are filled in; "and" replaces "&" because the text is read aloud.
VARIANTS: dict[str, list[str]] = {
    "daily": [
        "Before you go, a quick note on how this episode was made.",
        "{show} is produced by the {network} with an automated newsroom and AI-generated voices. "
        "The voices you heard are synthetic, not real people.",
        "Software helped write this episode, and every claim in it was checked against independent "
        "sources before it aired.",
        "Sources and corrections are listed in the show notes.",
        "If you hear something wrong, please tell us. Use the report-an-error link in the show notes, "
        "and we will check it and correct it in public.",
        "{publisher} publishes this network and is responsible for everything on it. Thanks for listening.",
    ],
    "breaking": [
        "A quick note on how this report was made.",
        "{show} is produced by the {network} with an automated newsroom and AI-generated voices. "
        "The voice you are hearing is synthetic, not a person.",
        "Everything in this report was checked against independent sources before it aired. Breaking "
        "news moves fast, so details may change, and when they do, our next report will say what changed.",
        "Sources and corrections are listed in the show notes. If you see an error, use the "
        "report-an-error link there, and we will check it and correct it in public.",
        "{publisher} publishes this network and is responsible for what it airs.",
    ],
    "archive": [
        "Before you go, a quick note on how this episode was made.",
        "{show} is produced by the {network} with an automated newsroom and AI-generated voices. "
        "The voices you heard are synthetic, not real people.",
        "Software helped write this episode. It draws on records, archives and published reporting, and "
        "every claim was checked against independent sources before it aired. Where the record is thin "
        "or disputed, we have said so.",
        "Sources and corrections are listed in the show notes. If you spot a mistake, use the "
        "report-an-error link there, and we will check it and correct it in public.",
        "{publisher} publishes this network and is responsible for everything on it. Thanks for listening.",
    ],
}
PRESUMPTION = ("Anyone named in connection with a criminal case is presumed innocent unless a court "
               "has ruled otherwise.")

_FORMAT_VARIANT = {"daily_brief": "daily", "court_roundup": "daily", "breaking_flash": "breaking",
                   "case_weekly": "archive", "evergreen_story": "archive"}
_LANE_VARIANT = {"breaking": "breaking", "archive": "archive", "strict": "archive"}


def variant_for(show_cfg: dict) -> str:
    """Variant name for a show: by format, else by lane, else 'daily'."""
    fmt = show_cfg.get("format")
    if fmt in _FORMAT_VARIANT:
        return _FORMAT_VARIANT[fmt]
    return _LANE_VARIANT.get(show_cfg.get("lane"), "daily")


def _texts(show_cfg: dict) -> list[str]:
    network = (show_cfg.get("network_label") or DEFAULT_NETWORK).replace("&", "and")
    texts = list(VARIANTS[variant_for(show_cfg)])
    if show_cfg.get("lane") == "strict":
        texts.insert(-1, PRESUMPTION)              # just before the sign-off
    return [t.format(show=show_cfg.get("name") or "This show", network=network, publisher=PUBLISHER)
            for t in texts]


def disclosure_text(show_cfg: dict) -> str:
    """The full spoken disclosure as one paragraph (for Episode.disclosure_text and show notes)."""
    return " ".join(_texts(show_cfg))


def disclosure_lines(show_cfg: dict, voices: dict) -> list[ScriptLine]:
    """The disclosure as script lines, spoken by the network's disclosure voice."""
    personas = voices.get("personas") or {}
    voice = voices.get("disclosure_voice") or next(iter(personas), "")
    if not voice:
        raise ValueError("voices config has no disclosure_voice and no personas")
    show = show_cfg.get("id") or show_cfg.get("name") or "show"
    return [ScriptLine(id=make_id("ln", show, "disclosure", i), speaker=voice, text=t,
                       claim_ids=[], segment="disclosure")
            for i, t in enumerate(_texts(show_cfg))]


def ensure_disclosure(script: Script, show_cfg: dict, voices: dict) -> Script:
    """Return the script with the current disclosure as its final lines (idempotent, pure).

    Any disclosure lines already present (from an older wording, or written by mistake) are
    replaced, so the text is always the canonical one and always last. Claims that lived only
    on removed disclosure lines are dropped.
    """
    removed = {l.id for l in script.lines if l.segment == "disclosure"}
    lines = [l for l in script.lines if l.segment != "disclosure"] + disclosure_lines(show_cfg, voices)
    claims = []
    for c in script.claims:
        kept = [i for i in c.line_ids if i not in removed]
        if kept or not c.line_ids:
            claims.append(dataclasses.replace(c, line_ids=kept))
    return dataclasses.replace(script, lines=lines, claims=claims)
