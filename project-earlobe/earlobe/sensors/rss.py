"""Poll a market's configured feeds (RSS 2.0 / Atom) into Signals.

Feeds come from config/sources/<market>.yaml via config.load_sources(market):
  {outlet, url, kind, tier, beats, verified}
`kind` is article | press_release | official_data | court_record. A feed that declares several
beats tags each item with the best-matching one (base.classify_beat), or 'general' when nothing
matches; the Story Desk triage assigns the final beat. One dead feed never stops the others.
"""
from __future__ import annotations

import logging

from earlobe.schemas import Signal
from earlobe.sensors import base

log = logging.getLogger("earlobe.sensors.rss")

OFFICIAL_KINDS = ("press_release", "official_data", "court_record")


def sensor_id(market: str) -> str:
    return f"beat-{market}"


def _poll_one(job: tuple) -> tuple[dict, list[Signal], str]:
    """Fetch and parse one feed. Returns (feed, signals, error); never raises."""
    feed, market, sensor = job
    try:
        xml = base.fetch(feed["url"])
        sigs = base.parse_feed(xml, sensor=sensor, market=market, beat="general",
                               outlet=feed["outlet"], tier=feed["tier"], kind=feed["kind"])
    except Exception as e:  # noqa: BLE001 - one bad feed must not stop the rest
        return feed, [], f"{type(e).__name__}: {e}"
    for s in sigs:
        s.beat = base.classify_beat(f"{s.title} {s.summary}", feed["beats"])
        s.raw = {**s.raw, "feed_url": feed["url"]}
    return feed, sigs, ""


def poll_feeds(market: str, feeds: list[dict], since_hours: float, sensor: str) -> list[Signal]:
    """Fetch `feeds` in parallel; keep items from the last `since_hours` (undated items are kept)."""
    cutoff = base.cutoff_iso(since_hours)
    out: list[Signal] = []
    for feed, sigs, err in base.pmap(_poll_one, [(f, market, sensor) for f in feeds]):
        if err:
            log.warning("%s: feed failed %s (%s)", market, feed["url"], err)
            continue
        fresh = [s for s in sigs if base.is_recent(s.published_at, cutoff)]
        log.info("%s: %s -> %d items, %d fresh", market, feed["outlet"] or feed["url"], len(sigs), len(fresh))
        out.extend(fresh)
    return base.dedupe(out)


def poll_market(market: str, since_hours: float = 24, dry_run: bool = False, *,
                kinds: tuple[str, ...] | None = None) -> list[Signal]:
    """All configured feeds for a market (or only those whose kind is in `kinds`).

    dry_run returns fixtures.sample_signals(market): no config read, no network.
    """
    if dry_run:
        from earlobe import fixtures
        return list(fixtures.sample_signals(market))
    feeds = [f for f in base.market_feeds(market) if kinds is None or f["kind"] in kinds]
    return poll_feeds(market, feeds, since_hours, sensor_id(market))


def check_feeds(market: str) -> list[dict]:
    """Health report for the Beat agent's first-run check: one row per configured feed with
    ok, item count, newest item timestamp and error. Never raises."""
    rows = []
    feeds = base.market_feeds(market)
    for feed, sigs, err in base.pmap(_poll_one, [(f, market, sensor_id(market)) for f in feeds]):
        dates = [s.published_at for s in sigs if s.published_at]
        rows.append({"outlet": feed["outlet"], "url": feed["url"], "ok": not err and bool(sigs),
                     "items": len(sigs), "newest": max(dates) if dates else None, "error": err})
    return rows
