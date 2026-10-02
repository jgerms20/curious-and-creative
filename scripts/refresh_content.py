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


def fetch(url, binary=False, timeout=25, method="GET", follow=True):
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
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise last


def fetch_as(url, ua, timeout=25):
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
    log(f"  photos synced: {len(photos)}")
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
    dbg["len"] = len(page)
    dbg["script_ids"] = re.findall(r'<script[^>]*id="([^"]+)"', page)[:20]
    dbg["head"] = page[:1200]
    dbg["episode_ids"] = sorted(set(re.findall(r"spotify:episode:([A-Za-z0-9]{22})", page)))[:60]
    dbg["anchor_ids"] = sorted(set(re.findall(r"anchor\.fm/s/([0-9a-f]+)", page)))
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    if not m:
        return None
    data = json.loads(m.group(1))
    try:
        dbg["entity"] = json.dumps(data["props"]["pageProps"]["state"]["data"])[:6000]
    except Exception:  # noqa: BLE001
        pass
    try:
        bot = fetch_as(f"https://open.spotify.com/show/{show_id}",
                       "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")
        dbg["bot_len"] = len(bot)
        dbg["bot_episode_links"] = len(set(re.findall(r"/episode/([A-Za-z0-9]{22})", bot)))
        dbg["bot_anchor"] = sorted(set(re.findall(r"anchor\.fm/s/([0-9a-f]+)", bot)))
        i = bot.find("/episode/")
        dbg["bot_sample"] = bot[max(0, i - 1500):i + 2500] if i >= 0 else bot[:3000]
        dbg["bot_script_ids"] = re.findall(r'<script[^>]*id="([^"]+)"', bot)[:20]
    except Exception as e:  # noqa: BLE001
        dbg["bot_error"] = str(e)

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
                "duration": e["duration"], "description": e["description"], "image": None,
                "url": e["spotify_url"], "spotify_url": e["spotify_url"],
            })

    only = [w.lower() for w in show.get("only_matching", [])]
    if only:
        eps = [e for e in eps if any(w in (e["title"] + " " + e["description"]).lower() for w in only)]

    cover = show.get("art_url") or (channel and channel.get("image")) or (sp and sp.get("cover")) or (apple and apple.get("artworkUrl600"))
    art = save_art(key, cover)
    out["show"] = {
        "feed": feed_url,
        "apple_url": show.get("apple") or (apple and apple.get("collectionViewUrl")),
        "spotify_url": show.get("spotify") and f"https://open.spotify.com/show/{show['spotify']}",
        "feed_title": (channel and channel["title"]) or (sp and sp.get("name")),
        "description": channel and channel["description"],
        "art": art or cover,
        "art_remote": cover,
    }
    out["episodes"] = eps if eps else [e for e in prev_eps if e.get("show") == key]
    report[key] = {"ok": bool(eps), "feed": feed_url, "episodes": len(out["episodes"]),
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
            "text": " ".join(g.text)[:6000],
            "images": imgs,
            "links": sorted(set(urllib.parse.urljoin(url, h) for h in g.links)),
        })
        for h in g.links:
            u = urllib.parse.urljoin(url, h).split("#")[0]
            if urllib.parse.urlparse(u).netloc == host and u not in seen and not re.search(r"\.(jpe?g|png|pdf|webp|gif|zip)$", u, re.I):
                queue.append(u)
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
        meta = {k: v for k, v in show.items() if k not in ("itunes_search", "match_artist", "only_matching")}
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
        people = sync_people(reg)
        log(f"  people: {people}")
        content["people"] = people
        with open(prev_path, "w") as f:
            json.dump(content, f, indent=1, ensure_ascii=False)
    with open(os.path.join(DATA, "_debug.json"), "w") as f:
        json.dump(DEBUG, f, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # noqa: BLE001
        log(f"refresh_content crashed: {e}")
        sys.exit(0)
