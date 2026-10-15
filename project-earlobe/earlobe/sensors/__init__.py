"""Sensors: raw items from the outside world, as Signals.

  rss            a market's configured news feeds (config/sources/<market>.yaml)
  press          its official feeds: press releases, agency data, court-record feeds
  gnews          Google News RSS search, one query per beat
  gdelt          GDELT DOC 2.0 article discovery and velocity (national market only here)
  courtlistener  newly filed federal dockets (needs COURTLISTENER_TOKEN)

run_sensors() is the one entry point the pipeline uses. It never raises: each sensor runs in
its own guard, failures are logged and the others carry on. `beats` steers the search sensors
(gnews, gdelt) and whether dockets are pulled; configured feeds are always polled whole.
Signals with beat 'general' came from a multi-beat feed with no keyword match.
"""
from __future__ import annotations

import logging
from typing import Callable

from earlobe.schemas import Signal
from earlobe.sensors import base, courtlistener, gdelt, gnews, press, rss

log = logging.getLogger("earlobe.sensors")

GDELT_MARKETS = {"national"}            # GDELT is a national net; local markets use feeds + gnews
COURT_BEATS = {"federal_court", "civil_court", "criminal_court", "da_press", "tracked_cases", "scotus"}

__all__ = ["run_sensors", "base", "rss", "press", "gnews", "gdelt", "courtlistener"]


def _market_cfg(market: str) -> dict:
    try:
        from earlobe import config
        return config.load_markets().get(market) or {}
    except Exception as e:  # noqa: BLE001
        log.warning("no market config for %s: %s", market, e)
        return {}


def _place(market: str, cfg: dict) -> str:
    """Geo term for local searches ('Columbia, SC'); empty for the national market."""
    return "" if market == "national" else (cfg.get("name") or "")


def _news_query(beat: str, place: str) -> str:
    terms = base.beat_query(beat)
    return f'"{place}" ({terms})' if place else f"({terms})"


def _guard(name: str, fn: Callable[[], list]) -> list[Signal]:
    """Run one sensor; log and return [] on any failure."""
    try:
        got = fn()
        log.info("sensor %s: %d signals", name, len(got))
        return list(got)
    except Exception as e:  # noqa: BLE001 - the contract is that run_sensors never raises
        log.warning("sensor %s failed: %s: %s", name, type(e).__name__, e)
        return []


def _dry_run(market: str) -> list[Signal]:
    from earlobe import fixtures
    return list(fixtures.sample_signals(market))


def _live(market: str, beats: list[str], since_hours: float) -> list[Signal]:
    cfg = _market_cfg(market)
    place, hours = _place(market, cfg), max(1, round(since_hours))
    found: list[Signal] = []
    found += _guard("rss", lambda: rss.poll_market(market, since_hours, kinds=("article",)))
    found += _guard("press", lambda: press.poll_press(market, since_hours))

    courts = (cfg.get("courts") or {}).get("federal")
    if courts and (not beats or COURT_BEATS & set(beats)):
        found += _guard("courtlistener", lambda: courtlistener.recent_dockets(
            courts, since_hours, market=market))

    def one_query(beat: str) -> list[Signal]:
        return _guard(f"gnews:{beat}", lambda: gnews.search(
            _news_query(beat, place), market, hours, beat=beat))

    for got in base.pmap(one_query, list(dict.fromkeys(beats)), workers=4):
        found += got

    if market in GDELT_MARKETS:                  # sequential: GDELT rate-limits to ~1 request / 5 s
        for beat in dict.fromkeys(beats):
            found += _guard(f"gdelt:{beat}", lambda b=beat: gdelt.articles(
                base.beat_query(b), f"{hours}h", market=market, beat=b))

    found = base.dedupe(found)
    found.sort(key=lambda s: s.published_at or "", reverse=True)
    return found


def run_sensors(market: str, beats: list[str], since_hours: float = 24,
                dry_run: bool = False) -> list[Signal]:
    """All sensors for a market, deduped by URL, newest first. Never raises.

    dry_run returns fixtures.sample_signals(market): no keys, no network, no config reads.
    """
    try:
        if dry_run:
            return _dry_run(market)
        return _live(market, list(beats or []), since_hours)
    except Exception as e:  # noqa: BLE001
        log.warning("run_sensors(%s) failed: %s: %s", market, type(e).__name__, e)
        return []
