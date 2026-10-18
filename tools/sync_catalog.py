#!/usr/bin/env python3
"""Extend site/data/episodes.json from the shows' public feeds.

episodes.json is the episode catalog (a flat list, exactly seven fields per
entry). The real source of truth is the Eclectic Polymath workspace's
episode-catalog.json; copying it over this file always wins. This script
only ADDS episodes the catalog doesn't have yet, from public data:

  The Eclectic Polymath Podcast  RSS feed (title, full description, date,
                                 duration) + the Spotify episode URL the RSS
                                 item's Spotify for Creators link resolves to
  God is Brazilian               episodes the site pipeline already tracked
                                 (site/data/content.json, with Spotify URLs)
                                 + the description from the episode's page

An entry is written only when all seven fields are filled; anything that
can't be completed is reported, never guessed. Needs network access
(run it in GitHub Actions or locally). Standard library only.
"""
import html
import json
import os
import re
import sys
import urllib.request
import base64
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "site", "data")
CATALOG = os.path.join(DATA, "episodes.json")
CACHE = os.path.join(DATA, "_spotify_resolve.json")
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd", "content": "http://purl.org/rss/1.0/modules/content/"}
FIELDS = ["episode_number", "title", "description", "duration_ms", "publish_date", "spotify_url", "show"]
SPOTIFY_EP = re.compile(r"(?:open\.spotify\.com/episode/|spotify:episode:)([A-Za-z0-9]{22})")
DEBUG = {"resolve": []}

POLYMATH = {"show": "The Eclectic Polymath Podcast", "key": "polymath"}
BRAZIL = {"show": "God is Brazilian", "key": "brazil"}


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.geturl(), r.read().decode("utf-8", "replace")


def text_paragraphs(raw):
    """HTML description -> plain text, one blank line between paragraphs."""
    s = re.sub(r"(?i)<br\s*/?>", "\n", raw or "")
    s = re.sub(r"(?i)</(p|div|li|h\d)>", "\n\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    s = re.sub(r"[ \t ]+", " ", s)
    paras = [p.strip() for p in re.split(r"\n\s*\n", s) if p.strip()]
    return "\n\n".join(" ".join(p.split()) for p in paras)


def seconds(v):
    v = (v or "").strip()
    if v.isdigit():
        return int(v)
    total = 0
    for part in v.split(":"):
        if not part.strip().isdigit():
            return None
        total = total * 60 + int(part)
    return total or None


def iso_date(s):
    try:
        return parsedate_to_datetime(s).astimezone(timezone.utc).strftime("%Y-%m-%d")
    except Exception:  # noqa: BLE001
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except Exception:  # noqa: BLE001
            return None


def number(title):
    m = re.match(r"\s*#\s*(\d+)", title or "")
    return int(m.group(1)) if m else None


def resolve_spotify(link, cache):
    """Spotify for Creators episode link -> open.spotify.com episode URL."""
    if link in cache:
        return cache[link]
    found = None
    try:
        final, body = get(link)
        ids = list(dict.fromkeys(SPOTIFY_EP.findall(final) + SPOTIFY_EP.findall(body)))
        if len(DEBUG["resolve"]) < 3:  # what the page looked like, so a failed resolve can be diagnosed
            i = body.find("open.spotify.com")
            DEBUG["resolve"].append({"link": link, "final": final, "len": len(body), "ids": ids[:5],
                                     "near": body[max(0, i - 200):i + 200] if i >= 0 else body[:400]})
        if len(ids) == 1:  # one unambiguous episode id on the page
            found = f"https://open.spotify.com/episode/{ids[0]}"
    except Exception as e:  # noqa: BLE001
        print(f"  resolve failed {link}: {e}")
        if len(DEBUG["resolve"]) < 3:
            DEBUG["resolve"].append({"link": link, "error": str(e)})
        return None  # not cached: try again next run
    cache[link] = found
    return found


def norm(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def spotify_api_titles(show_id):
    """title -> open.spotify.com URL for every episode, via the Spotify Web API when the
    repo has SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET. Empty dict otherwise."""
    cid, sec = os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not cid or not sec:
        return {}
    try:
        req = urllib.request.Request("https://accounts.spotify.com/api/token", data=b"grant_type=client_credentials",
                                     headers={"Authorization": "Basic " + base64.b64encode(f"{cid}:{sec}".encode()).decode(),
                                              "Content-Type": "application/x-www-form-urlencoded"})
        tok = json.loads(urllib.request.urlopen(req, timeout=25).read())["access_token"]
        out, nxt = {}, f"https://api.spotify.com/v1/shows/{show_id}/episodes?market=US&limit=50"
        while nxt:
            r = urllib.request.Request(nxt, headers={"Authorization": f"Bearer {tok}"})
            page = json.loads(urllib.request.urlopen(r, timeout=25).read())
            for e in page.get("items") or []:
                if e:
                    out[norm(e["name"])] = f"https://open.spotify.com/episode/{e['id']}"
            nxt = page.get("next")
        print(f"spotify api: {len(out)} episodes")
        return out
    except Exception as e:  # noqa: BLE001
        print(f"spotify api failed: {e}")
        return {}


def polymath_entries(rss_url, cache, api):
    _, xml_text = get(rss_url)
    ch = ET.fromstring(xml_text.encode("utf-8")).find("channel")
    items = ch.findall("item")
    links = [(it.findtext("link") or "").strip() for it in items]
    todo = [l for l in links if l and l not in cache and norm(next((it.findtext("title") for it in items if (it.findtext("link") or "").strip() == l), "")) not in api]
    with ThreadPoolExecutor(8) as pool:  # resolve the uncached links in parallel
        list(pool.map(lambda l: resolve_spotify(l, cache), todo))
    out = []
    for it in items:
        title = (it.findtext("title") or "").strip()
        n = number(title)
        link = (it.findtext("link") or "").strip()
        rec = {
            "episode_number": n,
            "title": title,
            "description": text_paragraphs(it.findtext("content:encoded", namespaces=NS) or it.findtext("description")),
            "duration_ms": (seconds(it.findtext("itunes:duration", namespaces=NS)) or 0) * 1000 or None,
            "publish_date": iso_date(it.findtext("pubDate")),
            "spotify_url": api.get(norm(title)) or (cache.get(link) if link else None),
            "show": POLYMATH["show"],
        }
        out.append(rec)
    return out


def brazil_entries(cache):
    content = json.load(open(os.path.join(DATA, "content.json")))
    out = []
    for e in content.get("episodes", []):
        if e.get("show") != BRAZIL["key"] or not e.get("spotify_url"):
            continue
        url = e["spotify_url"]
        desc = cache.get("desc:" + url)
        if desc is None:
            try:
                _, page = get(url)
                m = re.search(r'<meta (?:property|name)="(?:og:)?description" content="([^"]*)"', page)
                desc = html.unescape(m.group(1)).strip() if m else ""
            except Exception as ex:  # noqa: BLE001
                print(f"  description fetch failed {url}: {ex}")
                desc = ""
            cache["desc:" + url] = desc
        out.append({
            "episode_number": number(e.get("title")),
            "title": e.get("title", "").strip(),
            "description": desc,
            "duration_ms": (e.get("duration") or 0) * 1000 or None,
            "publish_date": (e.get("date") or "")[:10] or None,
            "spotify_url": url,
            "show": BRAZIL["show"],
        })
    return out


def main():
    catalog = json.load(open(CATALOG)) if os.path.exists(CATALOG) else []
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    shows = json.load(open(os.path.join(DATA, "shows.json")))["shows"]
    rss = next((s.get("rss") for s in shows if s["key"] == POLYMATH["key"]), None)

    candidates = []
    if rss:
        print(f"polymath feed: {rss}")
        candidates += polymath_entries(rss, cache, spotify_api_titles("3dlagzJ0jiWLTB9mF3y069"))
    candidates += brazil_entries(cache)

    have = {e["spotify_url"] for e in catalog}
    have_num = {(e["show"], e["episode_number"], e["title"]) for e in catalog}
    added, skipped = [], []
    for rec in candidates:
        missing = [f for f in FIELDS if rec.get(f) in (None, "")]
        if missing:
            skipped.append((rec.get("title"), missing))
            continue
        if rec["spotify_url"] in have or (rec["show"], rec["episode_number"], rec["title"]) in have_num:
            continue
        catalog.append({f: rec[f] for f in FIELDS})
        have.add(rec["spotify_url"])
        added.append(rec["title"])

    catalog.sort(key=lambda e: (e["show"] != POLYMATH["show"], e["episode_number"], e["title"]))
    with open(CATALOG, "w") as f:
        json.dump(catalog, f, indent=1, ensure_ascii=False)
        f.write("\n")
    with open(CACHE, "w") as f:
        json.dump(cache, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    DEBUG["skipped"] = len(skipped)
    with open(os.path.join(DATA, "_sync_debug.json"), "w") as f:
        json.dump(DEBUG, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"catalog: {len(catalog)} entries, {len(added)} added")
    for t in added[:20]:
        print("  +", t)
    for t, miss in skipped:
        print(f"  skipped (missing {', '.join(miss)}): {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
