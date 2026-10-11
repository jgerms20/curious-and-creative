"""GDELT DOC 2.0: wide-net article discovery and story velocity.

  https://api.gdeltproject.org/api/v2/doc/doc?query=...&mode=ArtList&format=json&timespan=1h&maxrecords=75

GDELT lists articles with their domain only, so outlet = domain and tier 4 (a lead, never
corroboration on its own). velocity() counts DISTINCT domains per hour, a cheap proxy for how
many independent newsrooms are on a story right now. GDELT asks for one request per ~5 seconds;
calls here are throttled to that. Bad or empty replies (GDELT sometimes answers 200 with plain
text) give [] / 0.0.
"""
from __future__ import annotations

import json
import logging
import re
import time
import urllib.parse

from earlobe.schemas import Signal, make_id
from earlobe.sensors import base

log = logging.getLogger("earlobe.sensors.gdelt")

SENSOR = "gdelt"
ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"
MAX_RECORDS = 75            # articles(); velocity() asks for the API maximum so it saturates later
MAX_RECORDS_VELOCITY = 250
MIN_INTERVAL = 5.0          # seconds between requests
_last_call = [0.0]
_UNITS = {"min": 1 / 60, "h": 1, "hour": 1, "hours": 1, "d": 24, "day": 24, "days": 24,
          "w": 168, "week": 168, "weeks": 168}


def timespan_hours(timespan: str) -> float:
    """'30min' -> 0.5, '1h' -> 1, '2d' -> 48. Raises ValueError on anything else."""
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([a-z]+)\s*", timespan or "", re.I)
    if not m or m.group(2).lower() not in _UNITS:
        raise ValueError(f"bad GDELT timespan {timespan!r}")
    return float(m.group(1)) * _UNITS[m.group(2).lower()]


def _prep(query: str, lang: str | None = None) -> str:
    """GDELT wants OR'd terms in parentheses; optionally restrict the source language."""
    q = query.strip()
    if " OR " in q and not q.startswith("("):
        q = f"({q})"
    return f"{q} sourcelang:{lang}" if lang and "sourcelang:" not in q else q


def doc_url(query: str, timespan: str, maxrecords: int) -> str:
    params = {"query": query, "mode": "ArtList", "format": "json",
              "timespan": timespan, "maxrecords": maxrecords}
    return f"{ENDPOINT}?{urllib.parse.urlencode(params)}"


def _articles(query: str, timespan: str, maxrecords: int) -> list[dict]:
    wait = MIN_INTERVAL - (time.monotonic() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    _last_call[0] = time.monotonic()
    try:
        body = base.fetch(doc_url(query, timespan, maxrecords))
        data = json.loads(body) if body.strip() else {}
    except Exception as e:  # noqa: BLE001 - network error or non-JSON reply
        log.warning("gdelt query failed for %r: %s", query, e)
        return []
    arts = data.get("articles") if isinstance(data, dict) else None
    return [a for a in arts or [] if isinstance(a, dict) and a.get("url")]


def articles(query: str, timespan: str = "1h", *, market: str = "", beat: str = "",
             lang: str | None = "english") -> list[Signal]:
    """Articles matching a GDELT query. `lang` adds sourcelang:<lang> (None = any language)."""
    out = []
    for a in _articles(_prep(query, lang), timespan, MAX_RECORDS):
        url = base.clean_url(a["url"])
        domain = (a.get("domain") or base.host_of(url)).lower().removeprefix("www.")
        out.append(Signal(
            id=make_id("sig", url), sensor=SENSOR, market=market, beat=beat or "general",
            title=base.strip_html(a.get("title") or "", None) or domain, url=url, outlet=domain,
            published_at=base.parse_date(a.get("seendate")), kind="article", tier=4,
            raw={k: a[k] for k in ("domain", "language", "sourcecountry", "seendate") if a.get(k)}))
    return base.dedupe(out)


def velocity(query: str, timespan: str = "1h") -> float:
    """Distinct domains publishing on `query` per hour over `timespan` (0.0 on any failure)."""
    try:
        hours = timespan_hours(timespan)
    except ValueError as e:
        log.warning("%s", e)
        return 0.0
    arts = _articles(_prep(query), timespan, MAX_RECORDS_VELOCITY)
    domains = {(a.get("domain") or base.host_of(a["url"])).lower().removeprefix("www.") for a in arts}
    return round(len(domains) / hours, 2)
