"""Google News RSS search: finds outlet coverage of a topic, beat or place.

  https://news.google.com/rss/search?q=<query>+when:<hours>h&hl=en-US&gl=US&ceid=US:en

Each item's <source> element names the real outlet; the item title carries a trailing
" - Outlet" that we strip. Links are Google News redirect URLs (publisher URL resolution is not
attempted), so the verifier re-sources claims instead of trusting these links as citations.
"""
from __future__ import annotations

import logging
import urllib.parse

from earlobe.schemas import Signal
from earlobe.sensors import base

log = logging.getLogger("earlobe.sensors.gnews")

SENSOR = "gnews"
ENDPOINT = "https://news.google.com/rss/search"


def search_url(query: str, hours: int = 24) -> str:
    q = urllib.parse.quote_plus(query.strip())
    return f"{ENDPOINT}?q={q}+when:{max(1, int(hours))}h&hl=en-US&gl=US&ceid=US:en"


def _tidy(sig: Signal) -> Signal:
    """Drop the ' - Outlet' title suffix; Google's description just repeats title and outlet."""
    suffix = f" - {sig.outlet}"
    if sig.outlet and sig.title.endswith(suffix):
        sig.title = sig.title[: -len(suffix)].rstrip()
    if sig.summary.startswith(sig.title):
        sig.summary = ""
    return sig


def search(query: str, market: str, hours: int = 24, *, beat: str = "", tier: int = 3) -> list[Signal]:
    """Signals for a Google News query over the last `hours`. Returns [] (and logs) on any failure."""
    try:
        xml = base.fetch(search_url(query, hours))
    except Exception as e:  # noqa: BLE001
        log.warning("gnews search failed for %r: %s", query, e)
        return []
    sigs = base.parse_feed(xml, sensor=SENSOR, market=market, beat=beat or "general",
                           outlet="Google News", tier=tier)
    for s in sigs:
        s.raw = {**s.raw, "query": query}
    return base.dedupe(_tidy(s) for s in sigs)
