"""The public trust log: one JSON line per gate decision, appended to data/public/trustlog/<show>.jsonl.

A line records the episode id, date, decision, lane, rewrite count, the gate's scores, how many
sources the episode used and any corrections. It is how a listener (or a journalist) checks that
we ran our own rules. It records every decision, not just PUBLISH (episode may be None for a
script that never became an episode; the script id is logged instead).

Appending the same record twice is a no-op, so re-running a pipeline does not duplicate lines.
Corrections are appended as their own lines (event "correction") by passing `corrections`.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from earlobe.publish import coerce, public_dir
from earlobe.schemas import Correction, Episode


def _g(obj, key, default=None):
    value = obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)
    return default if value is None else value


def path_for(show_id: str, out_dir: str | Path | None = None) -> Path:
    folder = Path(out_dir) if out_dir else public_dir("trustlog")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / f"{show_id}.jsonl"


def read(show_id: str, out_dir: str | Path | None = None) -> list[dict]:
    """All lines of a show's trust log ([] if none yet)."""
    path = path_for(show_id, out_dir)
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _record(show_id: str, episode: Episode | None, decision, corrections: list, event: str,
            history: list | None) -> dict:
    scores = dict(_g(decision, "scores", {}) or {})
    when = (episode.published_at if episode else None) or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec = {
        "show_id": show_id,
        "event": event,
        "episode_id": episode.id if episode else "",
        "script_id": _g(decision, "script_id", episode.script_id if episode else ""),
        "date": when[:10],
        "decision": _g(decision, "decision", ""),
        "lane": _g(decision, "lane_policy", ""),
        "revision": _g(decision, "revision", 0),
        "rules": [_g(r, "rule_id", "") for r in _g(decision, "reasons", [])],
        "scores": scores,
        "source_count": episode.source_count if episode else 0,
        "corrections": [{"id": c.id, "action": c.action, "claim_id": c.claim_id,
                         "reported_by": c.reported_by, "status": c.status, "summary": c.description}
                        for c in corrections],
    }
    if history:
        rec["history"] = history
    return rec


def append(show_id: str, episode, decision, *, corrections: list | None = None, event: str = "gate",
           history: list | None = None, out_dir: str | Path | None = None) -> str:
    """Append one line to the show's trust log and return the file path.

    episode:     Episode (or dict), or None when no episode exists.
    decision:    GateDecision (or dict).
    corrections: Correction records to log with this line; use event="correction" for a correction line.
    history:     optional per-revision decisions from the rewrite loop.
    """
    episode = coerce(Episode, episode) if episode is not None else None
    fixes = [coerce(Correction, c) for c in (corrections or [])]
    record = _record(show_id, episode, decision, fixes, event, history)
    path = path_for(show_id, out_dir)
    if any({k: v for k, v in line.items() if k != "logged_at"} == record for line in read(show_id, out_dir)):
        return str(path)
    record["logged_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return str(path)
