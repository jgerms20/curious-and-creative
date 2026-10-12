"""RSS 2.0 feeds with iTunes and podcast-namespace tags.

build_feed(show_id, show_cfg, episodes, base_url) -> str   the XML
write_feed(show_id, show_cfg, episodes, base_url)  -> path  data/public/feeds/<show>.xml

  * channel: title, link, description (with the AI disclosure), language, itunes:author,
    itunes:explicit false, itunes:category, podcast:locked no, podcast:guid (UUIDv5 of the feed URL,
    per the podcast namespace), atom:link self
  * item: title, description (with the AI disclosure), content:encoded (show notes as HTML),
    enclosure with url, length and type, guid, pubDate, itunes:duration, itunes:explicit false,
    podcast:transcript when the episode has one
  * episodes that are drafts, gated, retracted, killed or without audio are left out, so a
    retraction removes the item on the next rebuild

Rebuild on every publish, correction and retraction; the file is replaced atomically.
"""
from __future__ import annotations

import os
import re
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

from earlobe.publish import coerce, disclosure_text, public_base_url, public_dir
from earlobe.publish.notes import notes_html
from earlobe.schemas import Episode

NS = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "podcast": "https://podcastindex.org/namespace/1.0",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "atom": "http://www.w3.org/2005/Atom",
}
for _prefix, _uri in NS.items():
    ET.register_namespace(_prefix, _uri)

PODCAST_GUID_NAMESPACE = uuid.UUID("ead4c236-bf58-58c6-a2d6-a6b28d128cb6")   # fixed by the podcast namespace spec
EXCLUDED_STATUS = {"draft", "gated", "retracted", "killed"}
BYTES_PER_SECOND = 16000          # 128 kbps; used for enclosure length when the file is not on disk
AUDIO_TYPES = {".mp3": "audio/mpeg", ".m4a": "audio/x-m4a", ".wav": "audio/wav"}
TRANSCRIPT_TYPES = {".vtt": "text/vtt", ".srt": "application/x-subrip", ".json": "application/json",
                    ".html": "text/html", ".htm": "text/html"}

_BAD_XML = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f￾￿]")


def _q(prefix: str, name: str) -> str:
    return f"{{{NS[prefix]}}}{name}"


def _sub(parent: ET.Element, tag: str, body=None, **attrs) -> ET.Element:
    """Child element with optional text `body` and attributes (kept apart so an attribute can be called "text")."""
    el = ET.SubElement(parent, tag, {k: _BAD_XML.sub("", str(v)) for k, v in attrs.items()})
    if body is not None:
        el.text = _BAD_XML.sub("", str(body))
    return el


def _parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _rfc2822(dt: datetime) -> str:
    return format_datetime(dt.astimezone(timezone.utc), usegmt=True)


def _hms(seconds: int) -> str:
    h, rem = divmod(max(int(seconds), 0), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def feed_url(show_id: str, show_cfg: dict | None = None, base_url: str | None = None) -> str:
    return (show_cfg or {}).get("feed_url") or f"{public_base_url(base_url)}/feeds/{show_id}.xml"


def podcast_guid(url: str) -> str:
    """UUIDv5 of the feed URL without scheme or trailing slash (podcast namespace rule)."""
    return str(uuid.uuid5(PODCAST_GUID_NAMESPACE, re.sub(r"^[a-z][a-z0-9+.-]*://", "", url).rstrip("/")))


def transcript_url(path: str, base_url: str | None = None) -> str:
    """Public URL of a transcript: an http(s) URL is used as is, a local file is served from /transcripts/."""
    if re.match(r"^https?://", path):
        return path
    return f"{public_base_url(base_url)}/transcripts/{Path(path).name}"


def _enclosure_length(ep: Episode) -> int:
    try:
        return os.path.getsize(ep.audio_path)
    except (OSError, TypeError):
        return int(ep.duration_sec * BYTES_PER_SECOND)


def _channel_description(show_cfg: dict, show_id: str) -> str:
    name = show_cfg.get("name") or show_id
    label = show_cfg.get("network_label") or "Curious & Creative Network"
    base = show_cfg.get("description") or (
        f"{name}, from the {label}. Episodes are published only after automated checks against "
        "independent sources, and each episode's sources are linked in its show notes.")
    return f"{base} {disclosure_text(show_cfg)}"


def _add_item(channel: ET.Element, ep: Episode, show_cfg: dict, base_url: str | None) -> None:
    disclosure = ep.disclosure_text or disclosure_text(show_cfg)
    description = ep.description or ep.title
    if disclosure not in description:
        description = f"{description}\n\n{disclosure}"
    item = _sub(channel, "item")
    _sub(item, "title", ep.title)
    _sub(item, "description", description)
    if ep.show_notes_md:
        _sub(item, _q("content", "encoded"), notes_html(ep.show_notes_md))
    ext = Path(ep.audio_url.split("?")[0]).suffix.lower()
    _sub(item, "enclosure", url=ep.audio_url, length=_enclosure_length(ep),
         type=AUDIO_TYPES.get(ext, "audio/mpeg"))
    _sub(item, "guid", ep.guid or ep.id, isPermaLink="false")
    when = _parse_time(ep.published_at)
    if when:
        _sub(item, "pubDate", _rfc2822(when))
    if ep.duration_sec:
        _sub(item, _q("itunes", "duration"), _hms(ep.duration_sec))
    _sub(item, _q("itunes", "explicit"), "false")
    _sub(item, _q("itunes", "episodeType"), "full")
    if ep.transcript_path:
        suffix = Path(ep.transcript_path).suffix.lower()
        _sub(item, _q("podcast", "transcript"), url=transcript_url(ep.transcript_path, base_url),
             type=TRANSCRIPT_TYPES.get(suffix, "text/plain"),
             language=(show_cfg.get("language") or "en-us").split("-")[0])


def _publishable(episodes) -> list[Episode]:
    eps = [coerce(Episode, e) for e in episodes]
    eps = [e for e in eps if e.status not in EXCLUDED_STATUS and e.audio_url]
    eps.sort(key=lambda e: (e.published_at or "", e.id), reverse=True)
    return eps


def build_feed(show_id: str, show_cfg: dict, episodes, base_url: str | None = None) -> str:
    """The RSS 2.0 XML for one show."""
    show_cfg = show_cfg or {}
    base = public_base_url(base_url)
    url = feed_url(show_id, show_cfg, base)
    name = show_cfg.get("name") or show_id
    label = show_cfg.get("network_label") or "Curious & Creative Network"
    email = show_cfg.get("owner_email") or ""
    eps = _publishable(episodes)
    description = _channel_description(show_cfg, show_id)

    rss = ET.Element("rss", version="2.0")
    ch = _sub(rss, "channel")
    _sub(ch, "title", name)
    _sub(ch, "link", show_cfg.get("link") or base)
    _sub(ch, "description", description)
    _sub(ch, "language", show_cfg.get("language") or "en-us")
    newest = max((t for t in (_parse_time(e.published_at) for e in eps) if t), default=None)
    _sub(ch, "lastBuildDate", _rfc2822(newest or datetime.now(timezone.utc)))
    _sub(ch, "generator", "Earlobe")
    _sub(ch, _q("atom", "link"), href=url, rel="self", type="application/rss+xml")
    _sub(ch, _q("itunes", "author"), show_cfg.get("author") or label)
    _sub(ch, _q("itunes", "summary"), description)
    _sub(ch, _q("itunes", "explicit"), "false")
    _sub(ch, _q("itunes", "type"), "episodic")
    _sub(ch, _q("itunes", "category"), text=show_cfg.get("itunes_category") or "News")
    if show_cfg.get("image_url"):
        _sub(ch, _q("itunes", "image"), href=show_cfg["image_url"])
    if email:
        owner = _sub(ch, _q("itunes", "owner"))
        _sub(owner, _q("itunes", "name"), show_cfg.get("owner_name") or label)
        _sub(owner, _q("itunes", "email"), email)
    _sub(ch, _q("podcast", "locked"), "no", **({"owner": email} if email else {}))
    _sub(ch, _q("podcast", "guid"), podcast_guid(url))
    for ep in eps:
        _add_item(ch, ep, show_cfg, base)

    ET.indent(rss)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(rss, encoding="unicode") + "\n"


def write_feed(show_id: str, show_cfg: dict, episodes, base_url: str | None = None,
               out_dir: str | Path | None = None) -> str:
    """Build the feed and write data/public/feeds/<show>.xml (atomically). Returns the path."""
    xml = build_feed(show_id, show_cfg, episodes, base_url)
    folder = Path(out_dir) if out_dir else public_dir("feeds")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{show_id}.xml"
    part = path.with_name(path.name + ".part")
    part.write_text(xml, encoding="utf-8")
    os.replace(part, path)
    return str(path)
