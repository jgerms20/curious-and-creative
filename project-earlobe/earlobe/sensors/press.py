"""Official-source sensor: press releases, agency data feeds and court-record feeds.

These are the feeds in config/sources/<market>.yaml whose kind is press_release, official_data
or court_record (city and county newsrooms, police, the National Weather Service, the Supreme
Court). They are the tier-1 primary sources the trust stack prefers, so they get their own
sensor id and are polled separately from news outlets (sensors/rss.py).
"""
from __future__ import annotations

from earlobe.schemas import Signal
from earlobe.sensors import base, rss


def sensor_id(market: str) -> str:
    return f"press-{market}"


def poll_press(market: str, since_hours: float = 24, dry_run: bool = False) -> list[Signal]:
    """Official feeds for a market. dry_run returns the sample set's official items (no network)."""
    if dry_run:
        from earlobe import fixtures
        return [s for s in fixtures.sample_signals(market) if s.kind in rss.OFFICIAL_KINDS]
    feeds = [f for f in base.market_feeds(market) if f["kind"] in rss.OFFICIAL_KINDS]
    return rss.poll_feeds(market, feeds, since_hours, sensor_id(market))
