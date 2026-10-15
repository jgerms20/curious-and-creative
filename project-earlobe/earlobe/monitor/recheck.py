"""Re-check: verify recent episodes again, because stories change after we publish.

recheck(store, llm, days=7) walks the live episodes (published or corrected) published in the
last `days`, re-runs the blind Source Verifier (trust.verifier.verify) on each one's script, and
opens a Correction for every claim whose status has become "contradicted".

  * It only OPENS corrections (action "note", reported_by "monitor:recheck"). A person, or an
    explicit corrections.apply_open(), decides what goes public; a retraction is never automatic.
  * One correction per (episode, claim): re-running does not duplicate, and a correction that was
    rejected stays rejected. The return value lists only the new ones.
  * Cost is logged against the show (store.log_run), and an episode whose show is over its daily
    budget is skipped until the next UTC day. The kill switch is NOT consulted: a halted show must
    still be able to correct itself.
  * Dry-run: pass LLM(dry_run=True). The verifier then uses fixtures.fake and nothing leaves the machine.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from earlobe import config
from earlobe.monitor import CORRECTION, EPISODE, RECHECK_REPORT, SCRIPT, budget, corrections
from earlobe.schemas import Correction, Episode, Script, make_id
from earlobe.trust.verifier import verify

log = logging.getLogger(__name__)

REPORTER = "monitor:recheck"
NOTE_LIMIT = 240


def _parse(value: str | None) -> datetime | None:
    try:
        when = datetime.fromisoformat((value or "").replace("Z", "+00:00"))
    except ValueError:
        return None
    return when if when.tzinfo else when.replace(tzinfo=timezone.utc)


def _clip(text: str, n: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def _describe(claim, finding) -> str:
    """Listener-facing sentence for the show notes: the claim, then what the evidence says."""
    base = f"On re-check, independent sources contradict this claim from the episode: \"{claim.text}\""
    note = _clip(finding.note, NOTE_LIMIT)
    return f"{base}. {note}" if note else f"{base}."


def _recent(store, cutoff: datetime) -> list[Episode]:
    """Live episodes published at or after the cutoff (an unparseable or missing date is skipped)."""
    eps = [Episode.from_dict(raw) for raw in store.list(EPISODE)]
    return [e for e in eps if e.status in corrections.LIVE
            and (_parse(e.published_at) or datetime.min.replace(tzinfo=timezone.utc)) >= cutoff]


def recheck(store, llm, days: int = 7, *, now: datetime | None = None, owners: dict | None = None,
            max_searches: int = 10, respect_budget: bool = True) -> list[Correction]:
    """Re-verify episodes published in the last `days`; return the corrections newly opened."""
    now = now or datetime.now(timezone.utc)
    owners = config.load_owners() if owners is None else owners
    opened: list[Correction] = []
    for ep in _recent(store, now - timedelta(days=days)):
        raw = store.get(SCRIPT, ep.script_id)
        if raw is None:
            log.warning("recheck: no script %s for episode %s; skipped", ep.script_id, ep.id)
            continue
        if respect_budget and not budget.within_budget(store, ep.show_id, now):
            log.warning("recheck: %s is over budget today; episode %s skipped", ep.show_id, ep.id)
            continue
        script = Script.from_dict(raw)
        start = len(llm.runs)
        report = verify(script, llm, owners, max_searches=max_searches)
        for run in llm.runs[start:]:
            store.log_run(run, ep.show_id)
        store.put(RECHECK_REPORT, make_id("rck", ep.id, corrections.iso(now)[:10]),
                  {**report.to_dict(), "episode_id": ep.id, "checked_at": corrections.iso(now)},
                  ep.show_id)

        claims = {c.id: c for c in script.claims}
        for finding in report.findings:
            claim = claims.get(finding.claim_id)
            if finding.status != "contradicted" or claim is None:
                continue
            text = _describe(claim, finding)
            cid = corrections.correction_id(ep.id, claim.id, text, REPORTER)
            if store.get(CORRECTION, cid) is None:
                opened.append(corrections.open_correction(
                    store, ep.id, text, claim_id=claim.id, reported_by=REPORTER, action="note",
                    now=now))
    return opened
