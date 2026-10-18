#!/usr/bin/env python3
"""Pull real show content into site/data/content.json.

Runs in GitHub Actions (which has open internet) on every deploy and on a
schedule. Standard library only. Never exits non-zero: if a source fails,
the previously committed data for that show is kept and the failure is
recorded in content.json["report"].

Sources
  podcasts : Apple Podcasts directory -> RSS feed (full history, descriptions)
             + Spotify embed page (episode links) keyed by the known show id
  youtube  : channel page -> channel id -> YouTube RSS (latest 15, merged
             into history so older videos are kept), shorts detected
  probe    : snapshot of listed personal sites (text + images) for curation
"""
import html
import signal
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DATA = os.path.join(SITE, "data")
ART = os.path.join(SITE, "assets", "art")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

NS = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "atom": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

report = {}


def log(*a):
    print(*a, flush=True)


class Deadline(Exception):
    pass


def _alarm(signum, frame):
    raise Deadline("request exceeded hard deadline")


signal.signal(signal.SIGALRM, _alarm)


def fetch(url, binary=False, timeout=25, method="GET", follow=True):
    signal.alarm(timeout + 10)
    try:
        return _fetch(url, binary, timeout, method, follow)
    finally:
        signal.alarm(0)


def _fetch(url, binary=False, timeout=25, method="GET", follow=True):
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA,
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "CONSENT=YES+cb; SOCS=CAI",
    })
    if not follow:
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kw):
                return None
        opener = urllib.request.build_opener(NoRedirect)
        try:
            with opener.open(req, timeout=timeout) as r:
                return r.status, b""
        except urllib.error.HTTPError as e:
            return e.code, b""
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
                return body if binary else body.decode("utf-8", "replace")
        except Deadline:
            raise
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 410):
                raise
            last = e
            time.sleep(1.5 * (attempt + 1))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise last


def fetch_as(url, ua, timeout=25):
    signal.alarm(timeout + 10)
    try:
        return _fetch_as(url, ua, timeout)
    finally:
        signal.alarm(0)


def _fetch_as(url, ua, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
    s = s.lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def strip_html(s, limit=None):
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", s or "")
    s = re.sub(r"(?i)<br\s*/?>|</p>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t\r\f\v]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s).strip()
    if limit and len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0] + "…"
    return s


def iso(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        return iso(parsedate_to_datetime(s))
    except Exception:  # noqa: BLE001
        pass
    try:
        return iso(datetime.fromisoformat(s.replace("Z", "+00:00")))
    except Exception:  # noqa: BLE001
        return None


def duration_seconds(v):
    if not v:
        return None
    v = v.strip()
    if v.isdigit():
        return int(v)
    parts = [p for p in v.split(":") if p.strip().isdigit()]
    if not parts:
        return None
    secs = 0
    for p in parts:
        secs = secs * 60 + int(p)
    return secs


def write_image(data, path, max_side):
    """Save as web-sized JPEG when Pillow is available, raw bytes otherwise."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        from io import BytesIO
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(BytesIO(data)))
        if im.mode not in ("RGB", "L"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im.convert("RGBA"), mask=im.convert("RGBA").split()[-1])
            im = bg
        im.thumbnail((max_side, max_side))
        im.convert("RGB").save(path, "JPEG", quality=84, optimize=True, progressive=True)
        return im.size
    except ImportError:
        with open(path, "wb") as f:
            f.write(data)
        return None


def save_art(key, url):
    if not url:
        return None
    try:
        data = fetch(url, binary=True)
        if len(data) < 2000:
            return None
        write_image(data, os.path.join(ART, f"{key}.jpg"), 900)
        return f"assets/art/{key}.jpg"
    except Exception as e:  # noqa: BLE001
        log(f"  art download failed for {key}: {e}")
        return None


def sync_photos(reg, probes):
    """Mirror the curated photography sets (web-sized) into assets/photos."""
    cfg = reg.get("photos") or {}
    sets = cfg.get("sets", {})
    page = None
    for p in probes:
        for pg in p.get("pages", []):
            if pg.get("url", "").rstrip("/") == cfg.get("page", "").rstrip("/"):
                page = pg
    if not page:
        log("  photography page not in probe; keeping existing photos")
        return None
    photos, seen = [], set()
    for img in page.get("images", []):
        m = re.search(r"/_sized/([a-z]+)-(.+)-480\.webp$", img["src"])
        if not m or m.group(1) not in sets:
            continue
        cat, name = m.group(1), m.group(2)
        if (cat, name) in seen:
            continue
        seen.add((cat, name))
        base = img["src"].rsplit("/", 1)[0]
        slug = f"{cat}-{name}".lower()
        out = {"id": slug, "set": sets[cat], "alt": img.get("alt", ""),
               "src": f"assets/photos/{slug}.jpg", "thumb": f"assets/photos/{slug}-sm.jpg"}
        try:
            big = os.path.join(SITE, out["src"])
            small = os.path.join(SITE, out["thumb"])
            if not os.path.exists(big):
                for size in ("1280", "960", "480"):
                    try:
                        write_image(fetch(f"{base}/{cat}-{name}-{size}.webp", binary=True), big, 1400)
                        break
                    except Exception:  # noqa: BLE001
                        continue
            if not os.path.exists(small):
                write_image(fetch(img["src"], binary=True), small, 640)
            photos.append(out)
        except Exception as e:  # noqa: BLE001
            log(f"  photo failed {slug}: {e}")
    feat = cfg.get("featured") or []
    for ph in photos:
        ph["featured"] = ph["id"] in feat
    photos.sort(key=lambda ph: feat.index(ph["id"]) if ph["id"] in feat else len(feat))
    log(f"  photos synced: {len(photos)} ({sum(ph['featured'] for ph in photos)} featured)")
    return photos


def sync_people(reg):
    people = {}
    for who, urls in (reg.get("people") or {}).items():
        dest = os.path.join(SITE, "assets", "people", f"{who}.jpg")
        for u in urls:
            try:
                write_image(fetch(u, binary=True), dest, 1000)
                people[who] = f"assets/people/{who}.jpg"
                break
            except Exception as e:  # noqa: BLE001
                log(f"  person photo {who} failed from {u}: {e}")
        if who not in people and os.path.exists(dest):
            people[who] = f"assets/people/{who}.jpg"
    return people


def scan_ids(text):
    return {
        "spotify": sorted(set(re.findall(r"open\.spotify\.com/(?:embed/)?((?:show|episode)/[A-Za-z0-9]{22})", text))),
        "anchor": sorted(set(re.findall(r"anchor\.fm/s/[0-9a-f]+/podcast/rss", text))),
        "youtube": sorted(set(re.findall(r"(?:youtube(?:-nocookie)?\.com/(?:embed/|watch\?v=|shorts/)|youtu\.be/)([\w-]{11})", text))),
    }


# ---------------------------------------------------------------- Spotify
DEBUG = {}


def spotify_oembed(show_id):
    try:
        d = json.loads(fetch("https://open.spotify.com/oembed?url=" + urllib.parse.quote(
            f"https://open.spotify.com/show/{show_id}", safe="")))
        return {"name": d.get("title"), "cover": d.get("thumbnail_url")}
    except Exception as e:  # noqa: BLE001
        log(f"  spotify oembed failed: {e}")
        return None


def spotify_embed(show_id):
    """Episode list (title -> episode url) + show name from the embed page."""
    page = fetch(f"https://open.spotify.com/embed/show/{show_id}")
    dbg = DEBUG.setdefault("spotify", {}).setdefault(show_id, {})
    try:
        legacy = fetch(f"https://open.spotify.com/embed-podcast/show/{show_id}", timeout=15)
        dbg["legacy_len"] = len(legacy)
        dbg["legacy_episode_ids"] = len(set(re.findall(r"spotify:episode:([A-Za-z0-9]{22})", legacy)))
        if dbg["legacy_episode_ids"] > 1:
            page = legacy
    except Exception as e:  # noqa: BLE001
        dbg["legacy_error"] = str(e)
    dbg["len"] = len(page)
    dbg["script_ids"] = re.findall(r'<script[^>]*id="([^"]+)"', page)[:20]
    dbg["head"] = page[:1200]
    dbg["episode_ids"] = sorted(set(re.findall(r"spotify:episode:([A-Za-z0-9]{22})", page)))[:60]
    dbg["anchor_ids"] = sorted(set(re.findall(r"anchor\.fm/s/([0-9a-f]+)", page)))
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    if not m:
        return None
    data = json.loads(m.group(1))

    found = {}

    def walk(o):
        if isinstance(o, dict):
            if "trackList" in o and not found:
                found.update(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(data)
    ent = (((data.get("props") or {}).get("pageProps") or {}).get("state") or {}).get("data", {}).get("entity") or {}
    if not found and ent.get("type") == "episode" and ent.get("id"):
        covers = ent.get("relatedEntityCoverArt") or []
        cover = max(covers, key=lambda c: c.get("maxWidth") or 0)["url"] if covers else None
        rd = (ent.get("releaseDate") or {}).get("isoString")
        return {"name": ent.get("subtitle"), "cover": cover, "episodes": [{
            "title": ent.get("title") or ent.get("name") or "",
            "spotify_url": f"https://open.spotify.com/episode/{ent['id']}",
            "duration": round((ent.get("duration") or 0) / 1000) or None,
            "date": parse_date(rd) if rd else None,
            "description": "",
            "video": bool(ent.get("hasVideo")),
        }]}
    if not found:
        def keys(o, depth=0, path=""):
            if depth > 6 or not isinstance(o, dict):
                return []
            out = [path]
            for k, v in o.items():
                out += keys(v, depth + 1, f"{path}.{k}")
            return out
        dbg["paths"] = keys(data)[:200]
        return None
    eps = []
    for t in found.get("trackList") or []:
        uri = t.get("uri") or ""
        eid = uri.split(":")[-1] if uri.startswith("spotify:episode:") else None
        if not eid:
            continue
        rd = t.get("releaseDate")
        if isinstance(rd, dict):
            rd = rd.get("isoString")
        eps.append({
            "title": t.get("title") or "",
            "spotify_url": f"https://open.spotify.com/episode/{eid}",
            "duration": round((t.get("duration") or 0) / 1000) or None,
            "date": parse_date(rd) if isinstance(rd, str) else None,
            "description": t.get("subtitle") or "",
        })
    cover = None
    try:
        srcs = (found.get("coverArt") or {}).get("sources") or []
        if srcs:
            cover = max(srcs, key=lambda s: s.get("width") or 0).get("url")
    except Exception:  # noqa: BLE001
        pass
    if found.get("trackList"):
        dbg["track_sample"] = found["trackList"][0]
        log(f"  spotify embed sample keys: {sorted(found['trackList'][0].keys())}")
    return {"name": found.get("name") or found.get("title"), "episodes": eps, "cover": cover}



# ---------------------------------------------------------------- Spotify Web API
_SP_TOKEN = {}


def spotify_token():
    cid, sec = os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not cid or not sec:
        return None
    if _SP_TOKEN.get("exp", 0) > time.time() + 60:
        return _SP_TOKEN["tok"]
    import base64
    req = urllib.request.Request("https://accounts.spotify.com/api/token", data=b"grant_type=client_credentials",
                                 headers={"Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode(),
                                          "Content-Type": "application/x-www-form-urlencoded"})
    signal.alarm(40)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            d = json.loads(r.read())
    finally:
        signal.alarm(0)
    _SP_TOKEN.update(tok=d["access_token"], exp=time.time() + d.get("expires_in", 3600))
    return _SP_TOKEN["tok"]


def spotify_api(path):
    tok = spotify_token()
    req = urllib.request.Request("https://api.spotify.com/v1/" + path, headers={"Authorization": f"Bearer {tok}"})
    signal.alarm(40)
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read())
    finally:
        signal.alarm(0)


def spotify_full(show_id):
    """Every episode of a Spotify show via the official Web API (needs repo secrets)."""
    if not spotify_token():
        return None
    show = spotify_api(f"shows/{show_id}?market=US")
    eps, offset = [], 0
    while True:
        page = spotify_api(f"shows/{show_id}/episodes?market=US&limit=50&offset={offset}")
        for e in page.get("items") or []:
            if not e:
                continue
            imgs = e.get("images") or []
            eps.append({
                "title": e.get("name") or "",
                "spotify_url": (e.get("external_urls") or {}).get("spotify") or f"https://open.spotify.com/episode/{e['id']}",
                "duration": round((e.get("duration_ms") or 0) / 1000) or None,
                "date": parse_date(e.get("release_date")) if e.get("release_date") else None,
                "description": strip_html(e.get("html_description") or e.get("description") or "", 700),
                "image": imgs[0]["url"] if imgs else None,
            })
        if not page.get("next"):
            break
        offset += 50
    imgs = show.get("images") or []
    return {"name": show.get("name"), "cover": imgs[0]["url"] if imgs else None,
            "description": strip_html(show.get("html_description") or show.get("description") or "", 600),
            "episodes": eps, "full": True}


def spotify_episode(eid):
    """One episode's details from its public embed page."""
    page = fetch(f"https://open.spotify.com/embed/episode/{eid}")
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    if not m:
        return None
    ent = (((json.loads(m.group(1)).get("props") or {}).get("pageProps") or {}).get("state") or {}).get("data", {}).get("entity") or {}
    if not ent.get("id"):
        return None
    covers = ent.get("coverArt", {}).get("sources") if isinstance(ent.get("coverArt"), dict) else None
    covers = covers or ent.get("relatedEntityCoverArt") or []
    cover = max(covers, key=lambda c: c.get("maxWidth") or c.get("width") or 0)["url"] if covers else None
    rd = (ent.get("releaseDate") or {}).get("isoString")
    return {"title": ent.get("title") or ent.get("name") or "", "spotify_url": f"https://open.spotify.com/episode/{ent['id']}",
            "duration": round((ent.get("duration") or 0) / 1000) or None, "date": parse_date(rd) if rd else None,
            "description": "", "image": cover, "video": bool(ent.get("hasVideo")), "show_uri": ent.get("relatedEntityUri")}


def big_art(url):
    """Spotify image URLs carry a size code; ask for the 640px version."""
    return re.sub(r"(/image/ab676563[0-9a-f]{4})5f1f", r"\1ba8a", url) if url else url


def episode_art(spotify_url):
    """The episode's current artwork, straight from Spotify (so new art shows up on the next run)."""
    try:
        d = json.loads(fetch("https://open.spotify.com/oembed?url=" + urllib.parse.quote(spotify_url, safe=""), timeout=15))
        return big_art(d.get("thumbnail_url"))
    except Exception:  # noqa: BLE001
        return None


CRAWLERS = ["Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
            "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "Twitterbot/1.0",
            "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)"]


def spotify_episode_ids(show_id):
    """Every episode id of a Spotify show we can see without API keys: the anonymous
    web-player token, then the show page as search crawlers get it."""
    dbg = DEBUG.setdefault("catalog", {}).setdefault(show_id, {})
    ids = []
    try:
        tok = json.loads(fetch("https://open.spotify.com/get_access_token?reason=transport&productType=web_player", timeout=15)).get("accessToken")
        dbg["anon_token"] = bool(tok)
        nxt = f"https://api.spotify.com/v1/shows/{show_id}/episodes?market=US&limit=50" if tok else None
        while nxt:
            req = urllib.request.Request(nxt, headers={"Authorization": f"Bearer {tok}", "User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as r:
                page = json.loads(r.read())
            ids += [e["id"] for e in page.get("items") or [] if e]
            nxt = page.get("next")
        dbg["anon_api"] = len(ids)
    except Exception as e:  # noqa: BLE001
        dbg["anon_error"] = str(e)[:200]
    for ua in CRAWLERS:
        try:
            page = fetch_as(f"https://open.spotify.com/show/{show_id}", ua, timeout=15)
            found = re.findall(r"(?:/episode/|spotify:episode:)([A-Za-z0-9]{22})", page)
            dbg[f"crawler:{ua.split('/')[0].split('(')[-1][:20]}"] = len(set(found))
            ids += found
        except Exception as e:  # noqa: BLE001
            dbg[f"crawler_error:{ua[:20]}"] = str(e)[:120]
    out = list(dict.fromkeys(ids))
    dbg["total"] = len(out)
    return out


def discover_feed(show, spotify_name):
    """Find a Spotify-hosted show's public RSS feed without API keys."""
    names = [n for n in dict.fromkeys([spotify_name, show["name"], show.get("short")]) if n]
    want = [norm(n) for n in names]
    # 1) Podcast Index (open directory) via its public web search
    for n in names:
        try:
            res = json.loads(fetch("https://podcastindex.org/api/search/byterm?q=" + urllib.parse.quote(n)))
            for f in (res.get("feeds") or [])[:15]:
                title, author, url = norm(f.get("title")), norm(f.get("author")), f.get("url") or f.get("originalUrl")
                hosts = [norm(h).split()[-1] for h in show.get("hosts", [])]
                if url and title in want and (not hosts or any(h in author for h in hosts)):
                    log(f"  podcastindex feed: {f.get('title')} | {f.get('author')} -> {url}")
                    return url
        except Exception as e:  # noqa: BLE001
            log(f"  podcastindex search failed ({n}): {e}")
    # 2) Spotify for Creators public show page, which links the RSS feed
    slugs = show.get("creator_slugs") or []
    for n in names:
        base = re.sub(r"[^a-z0-9]+", "", (n or "").lower())
        slugs += [base, base.replace("the", "", 1)]
    for n in names:
        words = re.findall(r"[a-z0-9]+", (n or "").lower().replace("&", " and ").replace("+", " and "))
        slugs += ["-".join(words), "".join(words), "-".join(w for w in words if w not in ("the", "podcast")),
                  "".join(w for w in words if w not in ("the", "podcast", "and"))]
    tried = DEBUG.setdefault("creators", {}).setdefault(show["key"], {})
    for slug in dict.fromkeys(x for x in slugs if x):
        for host in ("creators.spotify.com/pod/profile", "creators.spotify.com/pod/show", "anchor.fm"):
            try:
                page = fetch(f"https://{host}/{slug}", timeout=12).replace("\\u002F", "/")
            except Exception as e:  # noqa: BLE001
                tried[f"{host}/{slug}"] = str(e)[:60]
                continue
            m = re.search(r"https://anchor\.fm/s/[0-9a-f]+/podcast/rss", page)
            st = re.search(r'"stationId":"([0-9a-f]+)"', page)
            title = re.search(r"<title>(.*?)</title>", page, re.S)
            tried[f"{host}/{slug}"] = f"{len(page)} {title and title.group(1)[:60]} rss={bool(m)} station={st and st.group(1)}"
            url = m.group(0) if m else (st and f"https://anchor.fm/s/{st.group(1)}/podcast/rss")
            if url and any(w and w in norm(page[:200000]) for w in want):
                try:  # the feed has to be this show's, not a namesake's
                    ch, _ = parse_rss(fetch(url))
                    if norm(ch["title"]) in want or any(w and w in norm(ch["title"]) for w in want):
                        log(f"  creators page {host}/{slug} -> {url}")
                        return url
                    tried[f"{host}/{slug}"] += f" feed title {ch['title']!r} not ours"
                except Exception as e:  # noqa: BLE001
                    tried[f"{host}/{slug}"] += f" feed failed {e}"
    return None


def spotify_has_video(episode_url):
    try:
        eid = episode_url.rstrip("/").rsplit("/", 1)[-1].split("?")[0]
        page = fetch(f"https://open.spotify.com/embed/episode/{eid}")
        return '"hasVideo":true' in page.replace(" ", "")
    except Exception:  # noqa: BLE001
        return False

# ---------------------------------------------------------------- Apple
def itunes_search(term):
    q = urllib.parse.urlencode({"term": term, "media": "podcast", "entity": "podcast", "limit": 15})
    res = json.loads(fetch(f"https://itunes.apple.com/search?{q}"))
    return res.get("results", [])


def pick_feed(show, spotify_name):
    want = norm(spotify_name or show["name"])
    artists = [norm(a) for a in show.get("match_artist", [])]
    best, best_score = None, 0
    seen = []
    for term in show.get("itunes_search", []):
        try:
            results = itunes_search(term)
        except Exception as e:  # noqa: BLE001
            log(f"  itunes search failed '{term}': {e}")
            continue
        for r in results:
            name = norm(r.get("collectionName"))
            artist = norm(r.get("artistName"))
            seen.append(f"{r.get('collectionName')} | {r.get('artistName')} | {r.get('feedUrl')}")
            score = 0
            if name == want:
                score = 100
            elif want and (want in name or name in want):
                score = 60
            if artists:
                if any(a in artist for a in artists):
                    score += 30
                else:
                    score = 0
            if not r.get("feedUrl"):
                score = 0
            if score > best_score:
                best, best_score = r, score
    log("  itunes candidates:")
    for s in dict.fromkeys(seen):
        log("    -", s)
    if best and best_score >= 60:
        return best
    return None


def parse_rss(xml_text):
    root = ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text)
    ch = root.find("channel")
    img = ch.find("itunes:image", NS)
    channel = {
        "title": (ch.findtext("title") or "").strip(),
        "description": strip_html(ch.findtext("description") or ch.findtext("itunes:summary", namespaces=NS), 600),
        "image": img.get("href") if img is not None else (ch.findtext("image/url") or None),
        "link": ch.findtext("link"),
    }
    items = []
    for it in ch.findall("item"):
        title = (it.findtext("title") or "").strip()
        desc_raw = it.findtext("content:encoded", namespaces=NS) or it.findtext("description") or ""
        iimg = it.find("itunes:image", NS)
        enc = it.find("enclosure")
        items.append({
            "guid": (it.findtext("guid") or title).strip(),
            "title": title,
            "date": parse_date(it.findtext("pubDate")),
            "link": (it.findtext("link") or "").strip() or None,
            "audio": enc.get("url") if enc is not None else None,
            "duration": duration_seconds(it.findtext("itunes:duration", namespaces=NS)),
            "description": strip_html(desc_raw, 700),
            "image": iimg.get("href") if iimg is not None else None,
            "season": it.findtext("itunes:season", namespaces=NS),
            "episode": it.findtext("itunes:episode", namespaces=NS),
        })
    return channel, items


def match_spotify(title, sp_eps):
    t = norm(title)
    for e in sp_eps:
        s = norm(e["title"])
        if s == t or (len(s) > 12 and (s in t or t in s)):
            return e
    return None


def do_podcast(show, prev_eps):
    key = show["key"]
    out = {"show": {}, "episodes": []}
    sp = None
    if show.get("spotify"):
        try:
            sp = spotify_full(show["spotify"])
            if sp:
                log(f"  spotify api: {sp['name']} — {len(sp['episodes'])} episodes")
        except Exception as e:  # noqa: BLE001
            log(f"  spotify api failed: {e}")
            sp = None
    if show.get("spotify") and not sp:
        try:
            sp = spotify_embed(show["spotify"])
            log(f"  spotify: {sp and sp['name']} — {len(sp['episodes']) if sp else 0} episodes")
        except Exception as e:  # noqa: BLE001
            log(f"  spotify embed failed: {e}")
        if not sp or not sp.get("name"):
            oe = spotify_oembed(show["spotify"])
            if oe:
                sp = {**(sp or {"episodes": []}), **{k: v for k, v in oe.items() if v}}
                log(f"  spotify oembed: {oe.get('name')}")
    feed_url = show.get("rss")
    apple = None
    if not feed_url and show.get("itunes_search"):
        apple = pick_feed(show, sp and sp.get("name"))
        if apple:
            feed_url = apple.get("feedUrl")
            log(f"  chose feed: {apple.get('collectionName')} -> {feed_url}")
    if not feed_url and show.get("spotify") and not (sp and sp.get("full")):
        feed_url = discover_feed(show, sp and sp.get("name"))
    channel, items = None, []
    if feed_url:
        try:
            channel, items = parse_rss(fetch(feed_url))
            log(f"  rss: {channel['title']} — {len(items)} items")
        except Exception as e:  # noqa: BLE001
            log(f"  rss failed: {e}")

    sp_eps = sp["episodes"] if sp else []
    eps = []
    if items:
        for it in items:
            m = match_spotify(it["title"], sp_eps)
            eps.append({
                "id": f"{key}:{norm(it['guid'])[:80]}",
                "show": key,
                "kind": "episode",
                "title": it["title"],
                "date": it["date"] or (m and m["date"]),
                "duration": it["duration"] or (m and m["duration"]),
                "description": it["description"],
                "image": it["image"],
                "url": (m and m["spotify_url"]) or it["link"] or feed_url,
                "spotify_url": m and m["spotify_url"],
                "audio": it["audio"],
                "number": it["episode"],
            })
    elif sp_eps:
        for e in sp_eps:
            eps.append({
                "id": f"{key}:{e['spotify_url'].rsplit('/', 1)[-1]}",
                "show": key, "kind": "episode", "title": e["title"], "date": e["date"],
                "duration": e["duration"], "description": e["description"], "image": e.get("image"),
                "url": e["spotify_url"], "spotify_url": e["spotify_url"],
                "spotify_video": bool(e.get("video")),
            })

    for link in show.get("episode_links") or []:
        eid = link.rstrip("/").split("/episode/")[-1].split("?")[0]
        if any(e.get("spotify_url", "").endswith(eid) for e in eps):
            continue
        try:
            got = spotify_episode(eid)
        except Exception as e:  # noqa: BLE001
            log(f"  episode link failed {link}: {e}")
            got = None
        if got:
            eps.append({"id": f"{key}:{eid}", "show": key, "kind": "episode", "title": got["title"], "date": got["date"],
                        "duration": got["duration"], "description": got["description"], "image": got["image"],
                        "url": got["spotify_url"], "spotify_url": got["spotify_url"], "spotify_video": got["video"]})
            log(f"  pinned episode: {got['title']}")

    if not items and eps:
        have = {e["id"] for e in eps}
        eps += [e for e in prev_eps if e.get("show") == key and e["id"] not in have]

    if show.get("spotify") and not items and not (sp and sp.get("full")):
        # Spotify-only show: find every episode, not just the latest one the embed shows
        have = {e.get("spotify_url", "").rsplit("/", 1)[-1] for e in eps}
        for eid in spotify_episode_ids(show["spotify"]):
            if eid in have:
                continue
            try:
                got = spotify_episode(eid)
            except Exception as e:  # noqa: BLE001
                log(f"  episode {eid} failed: {e}")
                got = None
            if got and got.get("show_uri") and got["show_uri"] != f"spotify:show:{show['spotify']}":
                continue  # a recommendation from another show, not ours
            if got and got.get("title"):
                have.add(eid)
                eps.append({"id": f"{key}:{eid}", "show": key, "kind": "episode", "title": got["title"], "date": got["date"],
                            "duration": got["duration"], "description": got["description"], "image": got["image"],
                            "url": got["spotify_url"], "spotify_url": got["spotify_url"], "spotify_video": got["video"]})
                log(f"  found episode: {got['title']}")
        # artwork changes on Spotify reach the site on the next run
        for e in eps[:80]:
            if e.get("spotify_url") and not items:
                art = episode_art(e["spotify_url"])
                if art:
                    e["image"] = art
        eps.sort(key=lambda e: e.get("date") or "", reverse=True)

    if show.get("video_check"):
        known = {e["id"]: e.get("spotify_video") for e in prev_eps if e.get("show") == key}
        for e in eps[:25]:
            if e.get("spotify_url") and not e.get("spotify_video"):
                e["spotify_video"] = known.get(e["id"]) or spotify_has_video(e["spotify_url"])
        log(f"  video episodes: {sum(1 for e in eps if e.get('spotify_video'))}")

    hide = [w.lower() for w in show.get("hide_matching", [])]
    if hide:
        eps = [e for e in eps if not any(re.search(rf"\b{re.escape(w)}\b", e["title"].lower()) for w in hide)]

    only = [w.lower() for w in show.get("only_matching", [])]
    if only:
        eps = [e for e in eps if any(w in (e["title"] + " " + e["description"]).lower() for w in only)]

    live = (channel and channel.get("image")) or big_art(sp and sp.get("cover"))
    if not live and show.get("spotify"):
        live = big_art((spotify_oembed(show["spotify"]) or {}).get("cover"))
    cover = live or show.get("art_url") or (apple and apple.get("artworkUrl600"))  # current art from the feed/Spotify first
    art = save_art(key, cover)
    out["show"] = {
        "feed": feed_url,
        "apple_url": show.get("apple") or (apple and apple.get("collectionViewUrl")),
        "spotify_url": show.get("spotify") and f"https://open.spotify.com/show/{show['spotify']}",
        "feed_title": (channel and channel["title"]) or (sp and sp.get("name")),
        "description": (channel and channel["description"]) or (sp and sp.get("description")),
        "complete": bool(items) or bool(sp and sp.get("full")),
        "art": art or cover,
        "art_remote": cover,
    }
    out["episodes"] = eps if eps else [e for e in prev_eps if e.get("show") == key
                                       and not any(re.search(rf"\b{re.escape(w)}\b", e["title"].lower()) for w in hide)]
    report[key] = {"ok": bool(eps), "feed": feed_url, "spotify_name": sp and sp.get("name"),
                   "full_catalog": out["show"]["complete"], "episodes": len(out["episodes"]),
                   "spotify_matches": sum(1 for e in eps if e.get("spotify_url"))}
    return out


# ---------------------------------------------------------------- YouTube
def do_youtube(show, prev_eps):
    key = show["key"]
    cid = show.get("youtube_channel_id")
    avatar = None
    handle = show.get("youtube_handle")
    if handle:
        try:
            page = fetch(f"https://www.youtube.com/{handle}")
            if not cid:
                for pat in (r'"externalId":"(UC[\w-]{22})"', r'"channelId":"(UC[\w-]{22})"',
                            r'channel/(UC[\w-]{22})'):
                    m = re.search(pat, page)
                    if m:
                        cid = m.group(1)
                        break
            m = re.search(r'<meta property="og:image" content="([^"]+)"', page)
            avatar = m and html.unescape(m.group(1))
            m = re.search(r'<meta property="og:description" content="([^"]*)"', page)
            desc = m and html.unescape(m.group(1))
        except Exception as e:  # noqa: BLE001
            log(f"  channel page failed: {e}")
            desc = None
    log(f"  channel id: {cid}")
    eps = []
    if cid:
        try:
            root = ET.fromstring(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}").encode())
            A = "{http://www.w3.org/2005/Atom}"
            for en in root.findall(f"{A}entry"):
                vid = en.findtext("yt:videoId", namespaces=NS)
                grp = en.find("media:group", NS)
                d = grp.findtext("media:description", namespaces=NS) if grp is not None else ""
                link = en.find(f"{A}link")
                href = link.get("href") if link is not None else ""
                is_short = "/shorts/" in href
                if not is_short:
                    try:
                        status, _ = fetch(f"https://www.youtube.com/shorts/{vid}", follow=False, timeout=12)
                        is_short = status == 200
                    except Exception:  # noqa: BLE001
                        pass
                eps.append({
                    "id": f"{key}:{vid}", "show": key,
                    "kind": "short" if is_short else "video",
                    "title": (en.findtext(f"{A}title") or "").strip(),
                    "date": parse_date(en.findtext(f"{A}published")),
                    "duration": None,
                    "description": strip_html(d, 700),
                    "image": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                    "url": f"https://www.youtube.com/{'shorts/' if is_short else 'watch?v='}{vid}",
                    "youtube_id": vid,
                })
            log(f"  youtube rss: {len(eps)} entries ({sum(e['kind']=='short' for e in eps)} shorts)")
        except Exception as e:  # noqa: BLE001
            log(f"  youtube rss failed: {e}")
    # keep history: RSS only carries the latest 15
    have = {e["id"] for e in eps}
    eps += [e for e in prev_eps if e.get("show") == key and e["id"] not in have]
    art = save_art(key, show.get("art_url") or avatar)
    report[key] = {"ok": bool(cid), "channel_id": cid, "episodes": len(eps)}
    return {"show": {"youtube_url": f"https://www.youtube.com/{handle}" if handle else None,
                     "channel_id": cid, "art": art or avatar, "art_remote": avatar,
                     "description": desc if handle else None},
            "episodes": eps}


# ---------------------------------------------------------------- probe
class Grab(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs, self.links, self.text, self.meta, self._skip = [], [], [], {}, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript"):
            self._skip += 1
        if tag == "img":
            src = a.get("src") or a.get("data-src") or ""
            srcset = a.get("srcset") or a.get("data-srcset") or ""
            if srcset:
                cands = [c.strip().split(" ")[0] for c in srcset.split(",") if c.strip()]
                src = cands[-1] if cands else src
            if src:
                self.imgs.append({"src": src, "alt": a.get("alt", "")})
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "meta" and a.get("content") and (a.get("property") or a.get("name")):
            self.meta[a.get("property") or a.get("name")] = a["content"]

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self._skip:
            self._skip -= 1

    def handle_data(self, d):
        if not self._skip and d.strip():
            self.text.append(d.strip())


def probe_site(base):
    out = {"base": base, "pages": []}
    host = urllib.parse.urlparse(base).netloc
    queue, seen = [base], set()
    while queue and len(seen) < 25:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        try:
            page = fetch(url)
        except Exception as e:  # noqa: BLE001
            out["pages"].append({"url": url, "error": str(e)})
            continue
        g = Grab()
        g.feed(page)
        bg = re.findall(r'url\((["\']?)(https?://[^)"\']+\.(?:jpe?g|png|webp))\1\)', page)
        imgs = [{"src": urllib.parse.urljoin(url, i["src"]), "alt": i["alt"]} for i in g.imgs]
        imgs += [{"src": u, "alt": "(css background)"} for _, u in bg]
        ids = scan_ids(page)
        for src in re.findall(r'<script[^>]+src="([^"]+)"', page):
            su = urllib.parse.urljoin(url, src)
            if urllib.parse.urlparse(su).netloc == host and su not in seen:
                seen.add(su)
                try:
                    more = scan_ids(fetch(su))
                    for k in ids:
                        ids[k] = sorted(set(ids[k]) | set(more[k]))
                except Exception:  # noqa: BLE001
                    pass
        out["pages"].append({
            "url": url,
            "ids": ids,
            "title": g.meta.get("og:title") or (re.search(r"<title>(.*?)</title>", page, re.S) or [None, ""])[1],
            "meta": g.meta,
            "text": " ".join(g.text)[:80000],
            "images": imgs,
            "links": sorted(set(urllib.parse.urljoin(url, h) for h in g.links)),
            "links_ordered": list(dict.fromkeys(urllib.parse.urljoin(url, h) for h in g.links)),
        })
        for h in g.links:
            u = urllib.parse.urljoin(url, h).split("#")[0]
            if urllib.parse.urlparse(u).netloc == host and u not in seen and not re.search(r"\.(jpe?g|png|pdf|webp|gif|zip)$", u, re.I):
                queue.append(u)
    return out


# ---------------------------------------------------------------- projects + writing
PROJECT_HOSTS = ("jgerms20.github.io", "vercel.app", "ai.studio", "github.com/jgerms20/")


def probe_projects(probes):
    """Title, description and preview image for each project Joshua links."""
    links = set()
    for p in probes:
        for pg in p.get("pages", []):
            links |= {l for l in pg.get("links", []) if any(h in l for h in PROJECT_HOSTS)}
    out = []
    for link in sorted(links):
        if "curious-and-creative" in link:
            continue
        rec = {"url": link}
        try:
            page = fetch(link, timeout=15)
            g = Grab()
            g.feed(page)
            m = re.search(r"<title>(.*?)</title>", page, re.S)
            rec.update({"title": html.unescape((g.meta.get("og:title") or (m.group(1) if m else "")).strip()),
                        "description": html.unescape(g.meta.get("og:description") or g.meta.get("description") or ""),
                        "image": urllib.parse.urljoin(link, g.meta.get("og:image") or "") if g.meta.get("og:image") else None,
                        "text": " ".join(g.text)[:1500]})
        except Exception as e:  # noqa: BLE001
            rec["error"] = str(e)
        out.append(rec)
        log(f"  project {link}: {rec.get('title') or rec.get('error')}")
    return out


def parse_feed_posts(xml_text, author, limit=30):
    root = ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text)
    ch = root.find("channel")
    posts = []
    for it in ch.findall("item")[:limit]:
        enc = it.find("enclosure")
        posts.append({
            "title": (it.findtext("title") or "").strip(),
            "url": (it.findtext("link") or "").strip(),
            "date": parse_date(it.findtext("pubDate")),
            "excerpt": strip_html(it.findtext("description") or it.findtext("content:encoded", namespaces=NS) or "", 280),
            "image": enc.get("url") if enc is not None and "image" in (enc.get("type") or "") else None,
            "author": author,
        })
    return {"title": (ch.findtext("title") or "").strip(), "url": (ch.findtext("link") or "").strip(), "posts": posts}


LB_NS = "https://letterboxd.com"


def letterboxd_feed(user):
    """Diary + reviews from a Letterboxd profile's public RSS."""
    url = f"https://letterboxd.com/{user}/rss/"
    try:
        root = ET.fromstring(fetch(url).encode())
        items = []
        for it in root.find("channel").findall("item"):
            d = it.findtext("description") or ""
            img = re.search(r'<img src="([^"]+)"', d)
            text = strip_html(re.sub(r"<p><img[^>]*/?></p>", "", d), 600)
            items.append({
                "film": it.findtext(f"{{{LB_NS}}}filmTitle") or (it.findtext("title") or "").split(",")[0],
                "year": it.findtext(f"{{{LB_NS}}}filmYear"),
                "rating": it.findtext(f"{{{LB_NS}}}memberRating"),
                "watched": it.findtext(f"{{{LB_NS}}}watchedDate"),
                "title": (it.findtext("title") or "").strip(),
                "url": (it.findtext("link") or "").strip(),
                "poster": img.group(1) if img else None,
                "review": "" if re.match(r"^Watched on ", text) else text,
                "date": parse_date(it.findtext("pubDate")),
            })
        return items
    except Exception as e:  # noqa: BLE001
        log(f"  letterboxd rss blocked for {user} ({e}); trying rss2json")
        j = json.loads(fetch("https://api.rss2json.com/v1/api.json?rss_url=" + urllib.parse.quote(url, safe="")))
        if j.get("status") != "ok":
            raise RuntimeError(j.get("message") or "rss2json failed")
        out = []
        for it in j.get("items", []):
            d = it.get("description") or ""
            img = re.search(r'<img src="([^"]+)"', d)
            text = strip_html(re.sub(r"<p><img[^>]*/?></p>", "", d), 600)
            t = it.get("title", "")
            m = re.match(r"^(.*?), (\d{4})(?: - (.*))?$", t)
            out.append({"film": m.group(1) if m else t, "year": m.group(2) if m else None, "rating": None, "stars": (m.group(3) if m else None),
                        "title": t, "url": it.get("link"), "poster": img.group(1) if img else it.get("thumbnail"),
                        "review": "" if re.match(r"^Watched on ", text) else text,
                        "date": parse_date(it.get("pubDate", "").replace(" ", "T") + "Z") if it.get("pubDate") else None})
        return out


def find_letterboxd(seed, match):
    """Look for a member (e.g. Janel) among the people a known profile follows."""
    found = []
    for page in ("following", "followers"):
        try:
            h = fetch(f"https://letterboxd.com/{seed}/{page}/", timeout=15)
            for user, name in re.findall(r'<a[^>]+href="/([A-Za-z0-9_]+)/"[^>]*>\s*([^<]{2,60})</a>', h):
                if match.lower() in name.lower() and user not in found:
                    found.append(user)
            DEBUG.setdefault("letterboxd_search", {})[page] = found[:]
        except Exception as e:  # noqa: BLE001
            DEBUG.setdefault("letterboxd_search", {})[page] = str(e)
    return found


def do_writing(reg):
    """Substack feeds for each writer in shows.json["writing"]."""
    out = {"sources": [], "posts": []}
    for w in reg.get("writing", []):
        src = dict(w)
        feed = w.get("feed")
        if not feed and w.get("search"):
            for q in w["search"]:
                for api in (f"https://substack.com/api/v1/publication/search?query={urllib.parse.quote(q)}&page=0&limit=10",
                            f"https://substack.com/api/v1/profile/search?query={urllib.parse.quote(q)}&page=0"):
                    try:
                        res = json.loads(fetch(api, timeout=15))
                        DEBUG.setdefault("substack_search", {})[f"{q} | {api.split('/v1/')[1].split('?')[0]}"] = res if len(json.dumps(res)) < 20000 else json.dumps(res)[:20000]
                    except Exception as e:  # noqa: BLE001
                        DEBUG.setdefault("substack_search", {})[q] = str(e)
        if feed:
            try:
                try:
                    f = parse_feed_posts(fetch(feed), w.get("author"))
                except Exception as e:  # noqa: BLE001
                    # Substack blocks datacenter IPs; read the same feed through rss2json instead
                    log(f"  writing feed blocked ({e}); trying rss2json")
                    j = json.loads(fetch("https://api.rss2json.com/v1/api.json?rss_url=" + urllib.parse.quote(feed, safe="")))
                    if j.get("status") != "ok":
                        raise RuntimeError(j.get("message") or "rss2json failed")
                    f = {"title": (j.get("feed") or {}).get("title"), "url": (j.get("feed") or {}).get("link"),
                         "posts": [{"title": it.get("title", "").strip(), "url": it.get("link"), "date": parse_date(it.get("pubDate", "").replace(" ", "T") + "Z") if it.get("pubDate") else None,
                                    "excerpt": strip_html(it.get("description") or it.get("content") or "", 280),
                                    "image": it.get("thumbnail") or ((it.get("enclosure") or {}).get("link") if "image" in ((it.get("enclosure") or {}).get("type") or "") else None),
                                    "author": w.get("author")} for it in j.get("items", [])]}
                src.update(title=f["title"] or w.get("title"), url=f["url"] or w.get("url"), count=len(f["posts"]))
                out["posts"] += f["posts"]
                log(f"  writing {w.get('author')}: {len(f['posts'])} posts")
            except Exception as e:  # noqa: BLE001
                log(f"  writing feed failed {feed}: {e}")
        out["sources"].append(src)
    out["posts"].sort(key=lambda x: x.get("date") or "", reverse=True)
    out["letterboxd"] = []
    for lb in reg.get("letterboxd", []):
        rec = dict(lb)
        user = lb.get("user")
        if not user and lb.get("find_via"):
            cands = find_letterboxd(lb["find_via"], lb.get("match", ""))
            rec["candidates"] = cands
            user = cands[0] if len(cands) == 1 else None
        if user:
            rec["user"], rec["url"] = user, f"https://letterboxd.com/{user}/"
            try:
                rec["entries"] = letterboxd_feed(user)
                log(f"  letterboxd {user}: {len(rec['entries'])} entries, {sum(1 for x in rec['entries'] if x.get('review'))} reviews")
            except Exception as e:  # noqa: BLE001
                log(f"  letterboxd failed {user}: {e}")
        out["letterboxd"].append(rec)
    return out


# ---------------------------------------------------------------- main
def main():
    with open(os.path.join(DATA, "shows.json")) as f:
        reg = json.load(f)
    prev_path = os.path.join(DATA, "content.json")
    prev = {}
    if os.path.exists(prev_path):
        try:
            with open(prev_path) as f:
                prev = json.load(f)
        except Exception:  # noqa: BLE001
            prev = {}
    prev_eps = prev.get("episodes", [])
    prev_shows = {s["key"]: s for s in prev.get("shows", [])}

    shows, episodes = [], []
    for show in reg["shows"]:
        log(f"\n=== {show['key']} ({show['name']})")
        try:
            res = do_youtube(show, prev_eps) if show["kind"] == "youtube" else do_podcast(show, prev_eps)
        except Exception as e:  # noqa: BLE001
            log(f"  FAILED: {e}")
            report[show["key"]] = {"ok": False, "error": str(e)}
            res = {"show": {k: v for k, v in prev_shows.get(show["key"], {}).items()},
                   "episodes": [e for e in prev_eps if e.get("show") == show["key"]]}
        eps = sorted(res["episodes"], key=lambda e: e.get("date") or "", reverse=True)
        meta = {k: v for k, v in show.items() if k not in ("itunes_search", "match_artist", "only_matching", "hide_matching", "video_check", "episode_links", "creator_slugs")}
        meta.update({k: v for k, v in res["show"].items() if v})
        if not res["show"].get("art") and prev_shows.get(show["key"], {}).get("art"):
            meta["art"] = prev_shows[show["key"]]["art"]
        meta["latest"] = eps[0]["date"] if eps else None
        meta["count"] = len(eps)
        shows.append(meta)
        episodes += eps
        for e in eps[:3]:
            log(f"    {e.get('date')}  {e['title'][:90]}")

    episodes.sort(key=lambda e: e.get("date") or "", reverse=True)
    content = {
        "generated_at": iso(datetime.now(timezone.utc)),
        "shows": shows,
        "episodes": episodes,
        "report": report,
    }
    os.makedirs(DATA, exist_ok=True)
    with open(prev_path, "w") as f:
        json.dump(content, f, indent=1, ensure_ascii=False)
    log(f"\nwrote {prev_path}: {len(shows)} shows, {len(episodes)} episodes")

    if os.environ.get("PROBE_SITES", "1") == "1":
        probes = []
        for base in reg.get("probe_sites", []):
            log(f"\n=== probe {base}")
            try:
                p = probe_site(base)
                probes.append(p)
                for pg in p["pages"]:
                    log(f"  {pg.get('url')}  imgs={len(pg.get('images', []))}  {pg.get('error', '')}")
            except Exception as e:  # noqa: BLE001
                log(f"  probe failed: {e}")
        with open(os.path.join(DATA, "_probe.json"), "w") as f:
            json.dump(probes, f, indent=1, ensure_ascii=False)
        log("\n=== photos")
        photos = sync_photos(reg, probes)
        if photos is not None:
            with open(os.path.join(DATA, "photos.json"), "w") as f:
                json.dump({"source": reg["photos"]["page"], "photos": photos}, f, indent=1, ensure_ascii=False)
        log("\n=== projects")
        projects = probe_projects(probes)
        with open(os.path.join(DATA, "_projects.json"), "w") as f:
            json.dump(projects, f, indent=1, ensure_ascii=False)
        people = sync_people(reg)
        log(f"  people: {people}")
        content["people"] = people
        with open(prev_path, "w") as f:
            json.dump(content, f, indent=1, ensure_ascii=False)
    log("\n=== writing")
    try:
        writing = do_writing(reg)
        prev_w = json.load(open(os.path.join(DATA, "writing.json"))) if os.path.exists(os.path.join(DATA, "writing.json")) else {}
        if not writing["posts"]:
            writing["posts"] = prev_w.get("posts", [])
        prev_lb = {x.get("key"): x for x in prev_w.get("letterboxd", [])}
        for x in writing.get("letterboxd", []):
            if not x.get("entries") and prev_lb.get(x.get("key"), {}).get("entries"):
                x.update({k: v for k, v in prev_lb[x["key"]].items() if k in ("entries", "user", "url")})
        if True:
            with open(os.path.join(DATA, "writing.json"), "w") as f:
                json.dump(writing, f, indent=1, ensure_ascii=False)
    except Exception as e:  # noqa: BLE001
        log(f"  writing failed: {e}")
    with open(os.path.join(DATA, "_debug.json"), "w") as f:
        json.dump(DEBUG, f, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        log(f"refresh_content crashed: {e}")
        sys.exit(0)
