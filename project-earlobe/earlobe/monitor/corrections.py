"""Corrections: fix a published episode in the open.

  open_correction(store, episode_id, description, ...) -> Correction   record that something is wrong
  apply_correction(store, correction)                  -> Episode      make the fix public
  apply_open(store, show_id=None)                      -> [Episode]    apply every open correction

apply_correction does four things, each safe to repeat, so a half-finished run just converges
when it is run again:

  1. episode status: "corrected", or "retracted" for action "retract" (a retracted episode is
     never downgraded, and an episode that was not live is never promoted)
  2. show notes: one dated bullet under "## Corrections", the same line publish.notes.show_notes
     writes, so regenerating the notes later gives the same text
  3. the show's RSS feed is rebuilt (publish.feed.write_feed); a retracted episode drops out
  4. one "correction" line is appended to the public trust log

Actions: "note" and "reissue" both mark the episode corrected and fix the notes and feed. Neither
re-renders audio; that is a production step. "retract" removes the episode from the feed.
Nothing here applies a correction on its own: recheck() only opens them.
"""
from __future__ import annotations

from datetime import datetime, timezone

from earlobe import config
from earlobe.monitor import CORRECTION, EPISODE
from earlobe.publish import coerce, trustlog
from earlobe.publish.feed import write_feed
from earlobe.schemas import Correction, Episode, make_id

HEADING = "## Corrections"
LIVE = {"published", "corrected"}


def iso(now: datetime | None = None) -> str:
    return (now or datetime.now(timezone.utc)).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def correction_id(episode_id: str, claim_id: str, description: str, reported_by: str) -> str:
    """Stable id: one correction per (episode, claim, reporter), or per description when no claim."""
    return make_id("cor", episode_id, claim_id or " ".join(description.split()), reported_by)


def open_correction(store, episode_id: str, description: str, *, claim_id: str = "",
                    reported_by: str = "listener", action: str = "note",
                    now: datetime | None = None) -> Correction:
    """Record a correction as open. Asking again for the same one returns the stored record.

    Raises LookupError if the episode is not in the store (a mistyped id should fail loudly).
    """
    description = " ".join(description.split())
    cid = correction_id(episode_id, claim_id, description, reported_by)
    existing = store.get(CORRECTION, cid)
    if existing:
        return Correction.from_dict(existing)
    ep = store.get(EPISODE, episode_id)
    if ep is None:
        raise LookupError(f"no episode {episode_id!r} in the store")
    cor = Correction(id=cid, episode_id=episode_id, description=description, claim_id=claim_id,
                     reported_by=reported_by, created_at=iso(now), status="open", action=action)
    store.put(CORRECTION, cid, cor, ep.get("show_id", ""), created_at=cor.created_at)
    return cor


# ---------------------------------------------------------------- show notes
def note_line(cor: Correction) -> str:
    """The bullet for one correction, identical to the ones publish.notes.show_notes writes."""
    date = (cor.created_at or "")[:10] or "undated"
    text = " ".join(cor.description.split()).replace("[", "(").replace("]", ")")
    return f"- {date} ({cor.action}): {text}"


def append_note(notes_md: str, cor: Correction) -> str:
    """Add the correction's bullet to the "## Corrections" section (created if missing).

    The section sits before the closing AI-disclosure rule, so the disclosure stays last.
    Adding a line that is already there changes nothing.
    """
    line = note_line(cor)
    lines = (notes_md or "").rstrip("\n").split("\n") if (notes_md or "").strip() else []
    if line in lines:
        return notes_md
    if HEADING not in lines:
        rules = [i for i, l in enumerate(lines) if l.strip() == "---"]
        at = rules[-1] if rules else len(lines)
        block = [HEADING, "", line] + ([""] if at < len(lines) else [])
        new = lines[:at] + ([""] if at and lines[at - 1].strip() else []) + block + lines[at:]
        return "\n".join(new).rstrip("\n") + "\n"
    start = lines.index(HEADING)
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("#") or lines[i].strip() == "---"), len(lines))
    while end > start + 1 and not lines[end - 1].strip():      # insert after the last real line
        end -= 1
    after_bullet = lines[end - 1].startswith("- ")
    new = lines[:end] + ([] if after_bullet else [""]) + [line] + lines[end:]
    return "\n".join(new).rstrip("\n") + "\n"


# ---------------------------------------------------------------- apply
def apply_correction(store, correction, *, base_url: str | None = None) -> Episode:
    """Make a correction public (status, notes, feed, trust log) and return the updated Episode.

    Raises LookupError if the episode is not in the store and ValueError for a rejected correction.
    """
    cor = coerce(Correction, correction)
    if cor.status == "rejected":
        raise ValueError(f"correction {cor.id} was rejected; open a new one to change that")
    raw = store.get(EPISODE, cor.episode_id)
    if raw is None:
        raise LookupError(f"no episode {cor.episode_id!r} in the store")
    ep = Episode.from_dict(raw)
    cor.created_at = cor.created_at or iso()

    if cor.action == "retract":
        ep.status = "retracted"
    elif ep.status in LIVE:
        ep.status = "corrected"
    ep.show_notes_md = append_note(ep.show_notes_md, cor)
    cor.status = "applied"
    store.put(EPISODE, ep.id, ep, ep.show_id)
    store.put(CORRECTION, cor.id, cor, ep.show_id, created_at=cor.created_at)

    show_cfg = config.load_shows().get(ep.show_id, {})
    write_feed(ep.show_id, show_cfg, store.list(EPISODE, show_id=ep.show_id), base_url)
    trustlog.append(ep.show_id, ep, ep.gate or {"script_id": ep.script_id},
                    corrections=[cor], event="correction")
    return ep


def apply_open(store, show_id: str | None = None) -> list[Episode]:
    """Apply every open correction (optionally for one show). Returns the episodes it changed."""
    return [apply_correction(store, c) for c in store.list(CORRECTION, show_id=show_id)
            if c.get("status") == "open"]
