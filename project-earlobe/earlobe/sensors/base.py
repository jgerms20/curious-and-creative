"""Shared sensor plumbing: robust stdlib fetch, RSS 2.0 / Atom parsing, small helpers.

Everything here is standard library. Nothing in this module reads keys or config at import
time, so sensors import cleanly (and tests run) with no network and no environment.
"""
from __future__ import annotations

import html
import logging
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Iterable

from earlobe.schemas import Signal, make_id

log = logging.getLogger("earlobe.sensors")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
ACCEPT = ("application/rss+xml, application/atom+xml, application/xml;q=0.9, "
          "application/json;q=0.8, */*;q=0.5")
MAX_BYTES = 8_000_000          # refuse bodies bigger than this
MAX_SUMMARY = 400              # Signal.summary is a snippet, never full text
_TRACKING = re.compile(r"^(utm_.+|fbclid|gclid|mc_cid|mc_eid|igshid|ref_src)$", re.I)


# ---------------------------------------------------------------- time
def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None) -> str | None:
    """datetime -> '2026-10-11T13:00:00Z' (naive values are taken as UTC)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_date(s: str | None) -> str | None:
    """RFC 822 (RSS), ISO 8601 (Atom, date-only too) or GDELT '20261011T130000Z' -> ISO UTC."""
    s = (s or "").strip()
    if not s:
        return None
    try:
        return iso(parsedate_to_datetime(s))
    except (TypeError, ValueError, IndexError):
        pass
    try:
        return iso(datetime.fromisoformat(s.replace("Z", "+00:00")))
    except ValueError:
        pass
    try:
        return iso(datetime.strptime(s, "%Y%m%dT%H%M%SZ"))
    except ValueError:
        return None


def is_recent(published_at: str | None, cutoff: str) -> bool:
    """True when the ISO timestamp is at/after cutoff. Undated items are kept (can't tell)."""
    return published_at is None or published_at >= cutoff


def cutoff_iso(since_hours: float, now: datetime | None = None) -> str:
    ts = (now or utcnow()).timestamp() - since_hours * 3600
    return iso(datetime.fromtimestamp(ts, timezone.utc))


# ---------------------------------------------------------------- text / urls
def strip_html(s: str | None, limit: int | None = MAX_SUMMARY) -> str:
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s or "")
    s = re.sub(r"(?i)<br\s*/?>|</p>", " ", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"\s+", " ", s).strip()
    if limit and len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0] + "…"
    return s


def clean_url(url: str) -> str:
    """Drop fragments and tracking params, lowercase scheme/host. Leaves the rest alone."""
    url = (url or "").strip()
    try:
        p = urllib.parse.urlsplit(url)
    except ValueError:
        return url
    if not p.scheme or not p.netloc:
        return url
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True)
         if not _TRACKING.match(k)]
    return urllib.parse.urlunsplit(
        (p.scheme.lower(), p.netloc.lower(), p.path, urllib.parse.urlencode(q), ""))


def host_of(url: str) -> str:
    host = urllib.parse.urlsplit(url or "").netloc.lower()
    return host[4:] if host.startswith("www.") else host


def dedupe(signals: Iterable[Signal]) -> list[Signal]:
    """First occurrence of each URL wins; order is preserved."""
    seen, out = set(), []
    for s in signals:
        key = clean_url(s.url).rstrip("/")
        if key and key not in seen:
            seen.add(key)
            out.append(s)
    return out


# ---------------------------------------------------------------- network
def _read(req: urllib.request.Request, timeout: float) -> str:
    deadline = time.monotonic() + timeout * 2 + 10     # hard cap against slow-drip responses
    chunks, size = [], 0
    with urllib.request.urlopen(req, timeout=timeout) as r:
        charset = r.headers.get_content_charset() or "utf-8"
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_BYTES:
                raise ValueError(f"response larger than {MAX_BYTES} bytes")
            if time.monotonic() > deadline:
                raise TimeoutError("request exceeded hard deadline")
            chunks.append(chunk)
    body = b"".join(chunks)
    try:
        return body.decode(charset, "replace")
    except LookupError:
        return body.decode("utf-8", "replace")


def fetch(url: str, timeout: float = 20, *, headers: dict | None = None, retries: int = 3) -> str:
    """GET a URL and return the body as text.

    Browser-like UA, per-request timeout plus a hard total deadline, up to `retries` attempts
    with 1.5s/3s backoff. 4xx errors other than 408/429 are not retried. Raises the last error.
    """
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept": ACCEPT, "Accept-Language": "en-US,en;q=0.9", **(headers or {})})
    last: Exception | None = None
    for attempt in range(max(1, retries)):
        try:
            return _read(req, timeout)
        except urllib.error.HTTPError as e:
            if 400 <= e.code < 500 and e.code not in (408, 429):   # client errors won't fix themselves
                raise
            last = e
        except Exception as e:  # noqa: BLE001 - network errors come in many types
            last = e
        if attempt < retries - 1:
            time.sleep(1.5 * (attempt + 1))
    assert last is not None
    raise last


def pmap(fn: Callable[[Any], Any], items: list, workers: int = 8) -> list:
    """Ordered parallel map for I/O-bound calls. `fn` must handle its own errors."""
    if len(items) <= 1:
        return [fn(i) for i in items]
    with ThreadPoolExecutor(max_workers=min(workers, len(items))) as ex:
        return list(ex.map(fn, items))


# ---------------------------------------------------------------- beats
# Search terms per beat. They build Google News / GDELT queries and tag items from multi-beat feeds.
BEAT_KEYWORDS: dict[str, list[str]] = {
    "government": ["city council", "county council", "mayor", "commissioner", "ordinance", "budget"],
    "public_safety": ["police", "sheriff", "fire department", "arrest", "shooting", "crash", "deputies"],
    "education": ["school board", "school district", "university", "college", "students", "teachers"],
    "business": ["business", "jobs", "economy", "company", "layoffs", "hiring"],
    "development": ["development", "zoning", "rezoning", "construction", "developer", "permit"],
    "housing": ["housing", "rent", "eviction", "homeless", "tenants", "affordable housing"],
    "transit": ["transit", "traffic", "bus", "rail", "highway", "metro", "airport"],
    "weather": ["weather", "storm", "flood", "heat", "forecast", "tornado", "hurricane"],
    "sports": ["game", "coach", "championship", "playoff", "season", "team"],
    "culture": ["festival", "museum", "music", "arts", "theater", "concert", "restaurant"],
    "entertainment_business": ["studio", "streaming", "box office", "film production", "Hollywood"],
    "hollywood_history": ["Hollywood history", "classic Hollywood", "silent film", "golden age"],
    "major_death": ["dies", "dead at", "obituary", "death of", "passed away"],
    "attack_or_attempt": ["attack", "shooting", "assassination", "bombing", "gunman", "explosion"],
    "disaster": ["earthquake", "wildfire", "hurricane", "tornado", "flood", "tsunami", "evacuation"],
    "scotus": ["Supreme Court", "justices", "SCOTUS"],
    "federal_government": ["White House", "Congress", "Senate", "federal agency", "president", "Pentagon"],
    "space": ["NASA", "spacecraft", "astronaut", "rocket", "SpaceX", "satellite"],
    "sports_mega": ["Super Bowl", "World Series", "NBA Finals", "Stanley Cup", "Olympics", "World Cup"],
    "business_mega": ["merger", "acquisition", "earnings", "IPO", "bankruptcy", "antitrust"],
    "world": ["international", "foreign minister", "summit", "ceasefire", "prime minister", "sanctions"],
    "criminal_court": ["indicted", "sentenced", "convicted", "arraigned", "trial", "verdict", "plea"],
    "civil_court": ["lawsuit", "sued", "judge ruled", "settlement", "injunction", "class action"],
    "federal_court": ["federal court", "federal judge", "U.S. District Court", "indictment", "docket"],
    "da_press": ["district attorney", "prosecutors", "charged", "charges filed"],
    "tracked_cases": ["trial", "verdict", "sentencing", "indictment", "hearing"],
    "cold_case": ["cold case", "unsolved", "decades-old", "DNA match", "remains identified"],
}
_BEAT_RX: dict[str, re.Pattern] = {}


def _beat_rx(beat: str) -> re.Pattern | None:
    if beat not in _BEAT_RX and BEAT_KEYWORDS.get(beat):
        terms = "|".join(re.escape(k) for k in BEAT_KEYWORDS[beat])
        _BEAT_RX[beat] = re.compile(rf"\b(?:{terms})(?:s|es|ed|ing)?\b", re.I)
    return _BEAT_RX.get(beat)


def beat_query(beat: str) -> str:
    """Google News / GDELT boolean for a beat: '"city council" OR mayor OR ...'. Unknown beats
    fall back to the beat name as words."""
    terms = BEAT_KEYWORDS.get(beat) or [beat.replace("_", " ")]
    return " OR ".join(f'"{t}"' if " " in t else t for t in terms)


def classify_beat(text: str, beats: list[str]) -> str:
    """Pick the declared beat whose keywords hit `text` most. One beat -> that beat; no hit among
    several -> 'general' (the Story Desk triage assigns the final beat)."""
    beats = [b for b in beats or [] if b]
    if len(beats) <= 1:
        return beats[0] if beats else "general"
    scores = {b: len(_beat_rx(b).findall(text)) if _beat_rx(b) else 0 for b in beats}
    best = max(beats, key=lambda b: scores[b])          # ties: first declared beat
    return best if scores[best] else "general"


# ---------------------------------------------------------------- config access (lazy)
def market_feeds(market: str) -> list[dict]:
    """config/sources/<market>.yaml feeds, normalised to {url, outlet, kind, tier, beats}.

    config.load_sources(market) yields [{outlet, url, kind, tier, beats, verified}, ...]. Never
    raises: a missing or unreadable file logs a warning and gives []. Config is imported lazily
    so dry runs and parsing tests need neither PyYAML nor the file.
    """
    try:
        from earlobe import config
        data = config.load_sources(market)
    except Exception as e:  # noqa: BLE001
        log.warning("no source config for %s: %s", market, e)
        return []
    if isinstance(data, dict):
        data = data.get("feeds") or []
    out = []
    for e in data or []:
        e = {"url": e} if isinstance(e, str) else dict(e or {})
        if not e.get("url"):
            continue
        beats = e.get("beats") if e.get("beats") is not None else e.get("beat")
        e["beats"] = [beats] if isinstance(beats, str) else list(beats or [])
        e["outlet"] = e.get("outlet") or e.get("name") or ""
        e["kind"] = e.get("kind") or "article"
        e["tier"] = int(e.get("tier") or 3)
        out.append(e)
    return out


# ---------------------------------------------------------------- feed parsing
def _local(tag: Any) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _kids(el: ET.Element, name: str) -> list[ET.Element]:
    return [c for c in el if _local(c.tag) == name]


def _text(el: ET.Element, *names: str) -> str:
    """Text of the first direct child (by local name, in `names` order) that has any."""
    for name in names:
        for c in _kids(el, name):
            t = "".join(c.itertext()).strip()
            if t:
                return t
    return ""


def _link(item: ET.Element) -> str:
    """Article URL: feedburner origLink, else RSS <link> text, else Atom <link href> (alternate)."""
    orig = _text(item, "origLink")
    if orig:
        return orig
    for c in _kids(item, "link"):
        href = c.get("href")
        if href:
            if c.get("rel") in (None, "", "alternate"):   # skip self / enclosure / related
                return href.strip()
        elif (c.text or "").strip():
            return c.text.strip()
    return ""


def parse_feed(xml: str | bytes, *, sensor: str, market: str, beat: str, outlet: str, tier: int,
               kind: str = "article") -> list[Signal]:
    """RSS 2.0 or Atom -> Signals, newest-first order of the feed preserved.

    `outlet` is the default; an item's own <source> element (Google News) overrides it, and if
    both are empty the feed title, then the link's host, is used. Items without a URL are
    skipped. Malformed XML logs a warning and returns [].
    """
    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        log.warning("%s: feed is not valid XML (%s)", sensor, e)
        return []
    feed_title = ""
    if _local(root.tag) == "feed":                                  # Atom
        feed_title = _text(root, "title")
        items = _kids(root, "entry")
    else:                                                           # RSS 2.0 (and RSS 1.0 items)
        channels = _kids(root, "channel")
        feed_title = _text(channels[0], "title") if channels else ""
        items = [e for e in root.iter() if _local(e.tag) == "item"]

    out: list[Signal] = []
    for it in items:
        url = clean_url(_link(it))
        if not url:
            guid = _text(it, "guid", "id")
            url = clean_url(guid) if guid.lower().startswith("http") else ""
        title = strip_html(_text(it, "title"), None)
        if not url or not title:
            continue
        src = (_kids(it, "source") or [None])[0]       # RSS: <source url=..>Outlet</source>
        src_name = ""                                  # Atom: <source><title>Outlet</title>..
        if src is not None:
            src_name = _text(src, "title") if len(src) else (src.text or "").strip()
        raw = {"guid": _text(it, "guid", "id"), "author": _text(it, "author", "creator"),
               "source_url": (src.get("url") or "") if src is not None else ""}
        out.append(Signal(
            id=make_id("sig", url), sensor=sensor, market=market, beat=beat, title=title, url=url,
            outlet=src_name or outlet or feed_title or host_of(url),
            published_at=parse_date(_text(it, "pubDate", "published", "updated", "date")),
            summary=strip_html(_text(it, "description", "summary", "content")),
            kind=kind, tier=tier, raw={k: v for k, v in raw.items() if v}))
    return out
