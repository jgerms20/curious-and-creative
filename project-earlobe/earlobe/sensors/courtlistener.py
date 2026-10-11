"""CourtListener (Free Law Project) RECAP dockets: newly filed federal cases as tier-1 signals.

  GET https://www.courtlistener.com/api/rest/v4/search/?type=r&court=<ids>&filed_after=MM/DD/YYYY
      Authorization: Token <COURTLISTENER_TOKEN>

The token comes from the `token` argument or env COURTLISTENER_TOKEN; without one this sensor
logs a warning and returns [] (it never calls the network). Filing dates are whole days, so
`since_hours` rounds down to a calendar date. Field names follow the v4 search results
(caseName, docketNumber, dateFiled, court_id, docket_absolute_url, docket_id); this sandbox could
not reach the live docs, so confirm them against a real response on the first keyed run.
"""
from __future__ import annotations

import json
import logging
import os
import urllib.parse
from datetime import datetime, timedelta

from earlobe.schemas import Signal, make_id
from earlobe.sensors import base

log = logging.getLogger("earlobe.sensors.courtlistener")

SENSOR = "courtlistener"
API = "https://www.courtlistener.com/api/rest/v4/"
SITE = "https://www.courtlistener.com"
MAX_PAGES = 3
# config/markets.yaml uses PACER-style ids; CourtListener's differ for a few courts
COURT_ALIASES = {"dsc": "scd"}


def court_ids(courts) -> list[str]:
    """Accept 'cacd', 'cacd nysd' or ['cacd', 'nysd']; apply aliases; drop blanks and dupes."""
    if isinstance(courts, str):
        courts = courts.replace(",", " ").split()
    ids = [COURT_ALIASES.get(c.strip().lower(), c.strip().lower()) for c in courts or [] if c and c.strip()]
    return list(dict.fromkeys(ids))


def search_url(courts: list[str], filed_after: datetime) -> str:
    params = {"type": "r", "court": " ".join(courts), "filed_after": filed_after.strftime("%m/%d/%Y"),
              "order_by": "dateFiled desc"}
    return f"{API}search/?{urllib.parse.urlencode(params)}"


def _signal(r: dict, market: str, beat: str) -> Signal | None:
    path = r.get("docket_absolute_url") or ""
    if not path and r.get("docket_id"):
        path = f"/docket/{r['docket_id']}/"
    if not path:
        return None
    url = urllib.parse.urljoin(SITE, path)
    case, number = (r.get("caseName") or "Untitled case").strip(), (r.get("docketNumber") or "").strip()
    court_id = r.get("court_id") or ""
    summary = " ".join(x for x in (r.get("cause"), r.get("nature_of_suit")) if x)
    return Signal(
        id=make_id("sig", url), sensor=SENSOR, market=market,
        beat="scotus" if court_id == "scotus" else beat,
        title=f"{case} ({number})" if number else case, url=url,
        outlet=r.get("court") or court_id or "CourtListener",
        published_at=base.parse_date(r.get("dateFiled")), summary=base.strip_html(summary),
        kind="court_record", tier=1,
        raw={k: v for k, v in {"docket_id": r.get("docket_id"), "court_id": court_id,
                               "docket_number": number, "date_filed": r.get("dateFiled")}.items() if v})


def recent_dockets(courts, since_hours: float = 24, token: str | None = None, *,
                   market: str = "", beat: str = "federal_court",
                   now: datetime | None = None) -> list[Signal]:
    """Dockets filed in `courts` since `since_hours` ago. [] (with a log line) if no token or on error."""
    token = token or os.environ.get("COURTLISTENER_TOKEN")
    if not token:
        log.warning("COURTLISTENER_TOKEN not set; skipping CourtListener")
        return []
    ids = court_ids(courts)
    if not ids:
        return []
    since = (now or base.utcnow()) - timedelta(hours=since_hours)
    url, out = search_url(ids, since), []
    for _ in range(MAX_PAGES):
        try:
            data = json.loads(base.fetch(url, headers={"Authorization": f"Token {token}"}))
            if not isinstance(data, dict):
                raise ValueError("unexpected response shape")
        except Exception as e:  # noqa: BLE001
            log.warning("courtlistener request failed (%s): %s", ids, e)
            break
        out += [s for r in data.get("results") or [] if (s := _signal(r, market, beat))]
        url = data.get("next")
        if not url or not url.startswith(SITE):      # never send the token anywhere else
            break
    return base.dedupe(out)
