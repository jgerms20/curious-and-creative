#!/usr/bin/env python3
"""Generate one microsite page per show: site/shows/<slug>/index.html.

  python3 tools/build_shows.py                   # every show in the registry
  python3 tools/build_shows.py --only polymath   # just these show keys (comma-separated)
  python3 tools/build_shows.py --fetch           # read each show's full RSS feed for the archive
  python3 tools/build_shows.py --published       # refresh only the pages already published (the hourly run)

Reads   site/data/shows.json        the roster: name, slug, tagline, about, hosts, tier/category, cadence,
                                    links, optional accent; top-level "hosts" holds one-line host bios
        site/data/content.json      what the hourly refresh pulled from every feed (show art, feed
                                    description, recent episodes)
        site/data/episodes.json     Eclectic Polymath catalog (Spotify episode links by number)
        site/data/episode-pages.json  per-episode pages, linked where they exist
Writes  site/shows/<slug>/index.html  (one template, filled from the data; nothing is hand-built)
        site/assets/art/thumb/<key>.jpg  small cover thumbnails (when Pillow is available)
        site/data/show-pages.json   key -> page path; the hub links each show to its page from this

Runs in the hourly GitHub Action right after scripts/refresh_content.py, so latest episodes stay
current with no manual step. Standard library only; Pillow (optional) samples each show's accent
colour from its cover art. Output is byte-stable: re-running without data changes rewrites nothing.

Portability: every link inside a show page is relative, except SITE_BASE (canonical/Open Graph)
and HUB_URL. A show that graduates to its own domain gets SITE_BASE/HUB_URL pointed at the new
home and the same template.
"""
import argparse
import html
import json
import math
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# ------------------------------------------------------------------ config
SITE_BASE = "https://jgerms20.github.io/curious-and-creative/"  # becomes https://curiousandcreative.co/
NETWORK = "The Curious + Creative Network"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DATA = os.path.join(SITE, "data")
NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd", "content": "http://purl.org/rss/1.0/modules/content/"}
PAPER = {"light": (0xFF, 0xFC, 0xF5), "dark": (0x0F, 0x0D, 0x11)}
CAT_NAMES = {"culture": "Culture", "news": "News & reads", "industry": "Industry", "sports": "Sports"}
SOCIAL_NAMES = {"instagram": "Instagram", "tiktok": "TikTok", "youtube": "YouTube", "x": "X", "twitter": "X", "threads": "Threads",
                "facebook": "Facebook", "linkedin": "LinkedIn", "bluesky": "Bluesky", "substack": "Substack"}


def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def load(path, default):
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else default


def write_if_changed(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and open(path, encoding="utf-8").read() == text:
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return True


def slug_for(show):
    if show.get("slug"):
        return show["slug"]
    name = re.sub(r"^the\s+", "", show["name"].lower())
    return re.sub(r"[^a-z0-9]+", "-", name.replace("&", " and ")).strip("-")


# ------------------------------------------------------------------ colour
def lum(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgbhex(c):
    return "#%02X%02X%02X" % c


def readable(c, bg, toward, need=4.5):
    """Nudge c toward black/white until it reads on bg at WCAG AA."""
    for i in range(21):
        out = mix(c, toward, i / 20)
        if contrast(out, bg) >= need:
            return out
    return toward


def sample_accent(art_path):
    """The cover's most characterful colour: frequent, saturated, not near-black or near-white."""
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        im = Image.open(art_path).convert("RGB").resize((128, 128))
    except Exception:  # noqa: BLE001
        return None
    best, score = None, -1
    for count, (r, g, b) in im.quantize(colors=20, method=Image.Quantize.MEDIANCUT).convert("RGB").getcolors(4096) or []:
        mx, mn = max(r, g, b), min(r, g, b)
        sat = (mx - mn) / mx if mx else 0
        light = (mx + mn) / 510
        if light < 0.12 or light > 0.93:
            continue
        s = count ** 0.5 * (sat ** 1.5 + 0.05) * math.exp(-((light - 0.58) / 0.2) ** 2)  # vivid mid-tones beat merely common
        if s > score:
            best, score = (r, g, b), s
    return best


def palette(show, art_path):
    base = hexrgb(show["accent"]) if show.get("accent") else sample_accent(art_path) or (0x8A, 0x5C, 0xF6)
    on = (0x0F, 0x0D, 0x11) if contrast(base, (0x0F, 0x0D, 0x11)) >= contrast(base, (255, 255, 255)) else (255, 255, 255)
    return {
        "accent": rgbhex(base),                                                     # fills (buttons, rules)
        "on": rgbhex(on),                                                           # text on the accent
        "ink_light": rgbhex(readable(base, PAPER["light"], (0, 0, 0))),             # accent text, light theme
        "ink_dark": rgbhex(readable(base, PAPER["dark"], (255, 255, 255))),         # accent text, dark theme
    }


def thumb(key, art_rel):
    """A small copy of the cover for related-show cards and social previews of lists."""
    src = os.path.join(SITE, art_rel)
    out_rel = f"assets/art/thumb/{key}.jpg"
    out = os.path.join(SITE, out_rel)
    try:
        from PIL import Image
        if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            im = Image.open(src).convert("RGB")
            im.thumbnail((240, 240))
            im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
        return out_rel
    except Exception:  # noqa: BLE001
        return art_rel


# ------------------------------------------------------------------ episodes
def text_of(raw):
    s = re.sub(r"(?i)<br\s*/?>|</p>", "\n", raw or "")
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return re.sub(r"\s+", " ", s).strip()


def secs(v):
    v = (v or "").strip()
    if v.isdigit():
        return int(v)
    total = 0
    for part in v.split(":"):
        if not part.isdigit():
            return None
        total = total * 60 + int(part)
    return total or None


def fetch_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": "CuriousCreativeShowPages/1.0"})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=30).read())
    eps = []
    for it in root.find("channel").findall("item"):
        enc = it.find("enclosure")
        d = it.findtext("pubDate")
        try:
            iso = parsedate_to_datetime(d).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:  # noqa: BLE001
            iso = None
        eps.append({"title": (it.findtext("title") or "").strip(), "date": iso,
                    "duration": secs(it.findtext("itunes:duration", namespaces=NS)),
                    "description": text_of(it.findtext("content:encoded", namespaces=NS) or it.findtext("description")),
                    "url": (it.findtext("link") or "").strip() or None, "audio": enc.get("url") if enc is not None else None})
    return eps


def clock(s):
    if not s:
        return ""
    h, rem = divmod(int(s), 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def human_date(iso):
    try:
        d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return d.strftime("%b %-d, %Y")
    except Exception:  # noqa: BLE001
        return ""


def short(text, n=240):
    text = re.sub(r"\s+", " ", text or "").strip().rstrip("…")
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0].rstrip(",;:—-")
    return cut + "…"


# ------------------------------------------------------------------ page
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
SEARCH = """<script>
(() => {
  const q = document.getElementById("archive-q"), rows = [...document.querySelectorAll("#archive-list li")], n = document.getElementById("archive-n");
  if (!q) return;
  q.addEventListener("input", () => {
    const t = q.value.trim().toLowerCase(); let shown = 0;
    rows.forEach((r) => { const hit = !t || r.dataset.t.includes(t); r.hidden = !hit; if (hit) shown++; });
    n.textContent = t ? `${shown} of ${rows.length}` : `${rows.length} episodes`;
  });
})();
</script>"""


def show_page(show, info, eps, related, pal, links, root, hosts_info):
    url_abs = SITE_BASE + f"shows/{show['slug']}/"
    art = info.get("art")
    img_abs = SITE_BASE + art if art else SITE_BASE + "assets/brand/cc-logo.jpg"
    tagline = show.get("tagline") or ""
    lead = show.get("about") or info.get("description") or tagline
    meta_desc = short(f"{tagline} {lead}".strip(), 155)
    feed_about = info.get("description") or ""
    tier = "Flagship" if show.get("tier") != "secondary" else CAT_NAMES.get(show.get("category"), "The network")
    made = "Hybrid · host + AI" if show.get("ai") in ("hybrid", "assisted") else "AI-generated" if show.get("ai") == "full" else " & ".join(show.get("hosts") or [])
    count = info.get("count") or len(eps)
    first = min((e["date"] for e in eps if e.get("date")), default=None)

    buttons = []
    for label, href, primary in links:
        buttons.append(f'<a class="sp-btn{" sp-btn--primary" if primary else ""}" href="{esc(href)}" target="_blank" rel="noopener">{esc(label)}</a>')
    # the show's own social channels (registry field `socials`), only when real links exist
    for platform, href in (show.get("socials") or {}).items():
        if isinstance(href, str) and href.startswith(("https://", "http://")):
            buttons.append(f'<a class="sp-btn" href="{esc(href)}" target="_blank" rel="noopener">{esc(SOCIAL_NAMES.get(platform, platform))}</a>')

    def listen(e):
        return e.get("spotify_url") or e.get("url")

    latest = []
    for e in eps[:5]:
        notes = e.get("page")
        latest.append(f"""
      <article class="sp-ep">
        <p class="sp-ep__meta"><time datetime="{esc(e.get('date') or '')}">{esc(human_date(e.get('date') or ''))}</time>{f'<span>{esc(clock(e.get("duration")))}</span>' if e.get('duration') else ''}</p>
        <h3 class="sp-ep__title">{esc(e['title'])}</h3>
        <p class="sp-ep__desc">{esc(short(e.get('description'), 260))}</p>
        {f'<audio class="sp-ep__audio" controls preload="none" src="{esc(e["audio"])}" aria-label="Play {esc(e["title"])}"></audio>' if e.get('audio') else ''}
        <p class="sp-ep__links">{f'<a href="{esc(listen(e))}" target="_blank" rel="noopener">Listen on Spotify ↗</a>' if listen(e) else ''}{f'<a href="{esc(root + notes)}">Episode page {ARROW}</a>' if notes else ''}</p>
      </article>""")

    archive = "".join(
        f'<li data-t="{esc(e["title"].lower())}"><a href="{esc(listen(e) or "#")}" target="_blank" rel="noopener"><span>{esc(e["title"])}</span><time datetime="{esc(e.get("date") or "")}">{esc(human_date(e.get("date") or ""))}</time></a></li>'
        for e in eps)

    host_cards = []
    for h in show.get("hosts") or []:
        if h == "AI-generated":
            continue
        b = hosts_info.get(h, {})
        photo = f'<img src="{esc(root + b["photo"])}" alt="" loading="lazy" width="56" height="56">' if b.get("photo") else ""
        bio = f'<small>{esc(b["bio"])}</small>' if b.get("bio") else ""
        host_cards.append(f"<li>{photo}<span><b>{esc(h)}</b>{bio}</span></li>")
    if not host_cards and show.get("ai") == "full":
        host_cards.append(f"<li><span><b>AI-generated</b><small>Made with AI, directed by and accountable to {esc(show.get('principal') or 'a person')}.</small></span></li>")

    about_cards = [f'<div class="sp-card"><h3>Hosts</h3><ul class="sp-hosts">{"".join(host_cards)}</ul></div>'] if host_cards else []
    if show.get("cadence"):
        about_cards.append(f'<div class="sp-card"><h3>New episodes</h3><p class="sp-big">{esc(show["cadence"])}</p></div>')
    about_cards.append(f'<div class="sp-card"><h3>Part of</h3><p class="sp-big">{esc(tier)}</p><p>{esc(NETWORK)}</p></div>')
    about_cards.append(f'<div class="sp-card"><h3>By the numbers</h3><p class="sp-big">{count} episodes</p>{f"<p>Since {esc(human_date(first))}</p>" if first else ""}</div>')

    rel = "".join(
        f'<a class="sp-rel" href="{esc(root + r["path"])}"><img src="{esc(root + r["thumb"])}" alt="" loading="lazy" width="96" height="96"><span><b>{esc(r["name"])}</b><small>{esc(r["tagline"])}</small></span></a>'
        for r in related)

    ld = {"@context": "https://schema.org", "@type": "PodcastSeries", "name": show["name"], "description": lead,
          "url": url_abs, "image": img_abs, "webFeed": show.get("rss") or info.get("feed"),
          "author": [{"@type": "Person", "name": h} for h in show.get("hosts") or [] if h != "AI-generated"] or None,
          "isPartOf": {"@type": "CreativeWorkSeries", "name": NETWORK, "url": SITE_BASE + "pages/shows.html"}}
    ld = {k: v for k, v in ld.items() if v}

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(show['name'])} — {esc(NETWORK)}</title>
  <meta name="description" content="{esc(meta_desc)}" />
  <link rel="canonical" href="{esc(url_abs)}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{esc(NETWORK)}" />
  <meta property="og:title" content="{esc(show['name'])}" />
  <meta property="og:description" content="{esc(meta_desc)}" />
  <meta property="og:image" content="{esc(img_abs)}" />
  <meta property="og:image:alt" content="{esc(show['name'])} cover art" />
  <meta property="og:url" content="{esc(url_abs)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="theme-color" content="{pal['accent']}" />
  <link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml" />
  {f'<link rel="alternate" type="application/rss+xml" title="{esc(show["name"])}" href="{esc(show.get("rss"))}" />' if show.get('rss') else ''}
  <script>try{{var t=localStorage.getItem("cc-theme");document.documentElement.dataset.theme=t||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light")}}catch(e){{document.documentElement.dataset.theme="light"}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{root}css/cc.css" />
  <link rel="stylesheet" href="{root}css/show.css" />
  <style>:root{{--accent:{pal['accent']};--on-accent:{pal['on']};--accent-ink:{pal['ink_light']}}}:root[data-theme="dark"]{{--accent-ink:{pal['ink_dark']}}}</style>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="sp">
<a class="skip" href="#main">Skip to content</a>
<header class="sp-bar">
  <a class="sp-bar__net" href="{root}pages/shows.html"><img src="{root}assets/brand/cc-logo.jpg" alt="" width="28" height="28"><span>{esc(NETWORK)}</span></a>
  <nav class="sp-bar__nav" aria-label="Show"><a href="#latest">Latest</a><a href="#about">About</a><a href="#archive">Archive</a></nav>
</header>
<main id="main">
  <section class="sp-hero">
    <div class="sp-hero__art">{f'<img src="{esc(root + art)}" alt="{esc(show["name"])} cover art" width="900" height="900" fetchpriority="high">' if art else ''}</div>
    <div class="sp-hero__text">
      <p class="sp-kicker"><span>{esc(tier)}</span><span>{esc(made)}</span></p>
      <h1 class="sp-title">{esc(show['name'])}</h1>
      {f'<p class="sp-tagline">{esc(tagline)}</p>' if tagline else ''}
      <p class="sp-lead">{esc(lead)}</p>
      <p class="sp-actions">{''.join(buttons)}</p>
      <p class="sp-stats"><span><b>{count}</b> episodes</span>{f'<span>Latest <b>{esc(human_date(eps[0]["date"]))}</b></span>' if eps and eps[0].get('date') else ''}{f'<span><b>{esc(show["cadence"])}</b></span>' if show.get('cadence') else ''}</p>
    </div>
  </section>

  <section class="sp-section" id="latest" aria-labelledby="latest-h">
    <h2 class="sp-h2" id="latest-h">Latest episodes</h2>
    <div class="sp-eps">{''.join(latest) or '<p class="sp-empty">The first episode is on its way.</p>'}
    </div>
  </section>

  <section class="sp-section" id="about" aria-labelledby="about-h">
    <h2 class="sp-h2" id="about-h">About the show</h2>
    <div class="sp-about">
      <div class="sp-about__text">{''.join(f'<p>{esc(p)}</p>' for p in (feed_about or lead).split(chr(10)) if p.strip())}</div>
      <div class="sp-about__cards">{''.join(about_cards)}</div>
    </div>
  </section>

  <section class="sp-section" id="archive" aria-labelledby="archive-h">
    <div class="sp-archive__head">
      <h2 class="sp-h2" id="archive-h">Every episode</h2>
      <label class="sp-search"><span class="sr-only">Search episodes</span><input id="archive-q" type="search" placeholder="Search {len(eps)} episodes" autocomplete="off"></label>
    </div>
    <p class="sp-archive__n" id="archive-n" aria-live="polite">{len(eps)} episodes</p>
    <ol class="sp-archive" id="archive-list">{archive}</ol>
  </section>
</main>
<footer class="sp-foot">
  <div class="sp-foot__net">
    <p class="sp-kicker"><span>Part of {esc(NETWORK)}</span></p>
    <p class="sp-foot__line">Accurate information, reported where nobody else is reporting, and made to be enjoyed.</p>
    <p class="sp-actions"><a class="sp-btn" href="{root}pages/shows.html">Every show on the network {ARROW}</a><a class="sp-btn" href="{root}pages/manifesto.html">Our standards</a></p>
  </div>
  {f'<div class="sp-foot__rel"><h2 class="sp-h3">More like this</h2><div class="sp-rels">{rel}</div></div>' if rel else ''}
  <p class="sp-foot__copy">© {datetime.now(timezone.utc).year} The Curious &amp; Creative Company · <a href="{root}index.html">curiousandcreative.co</a></p>
</footer>
{SEARCH}
</body>
</html>
"""


# ------------------------------------------------------------------ build
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="comma-separated show keys")
    ap.add_argument("--fetch", action="store_true", help="read each show's full RSS feed for the archive")
    ap.add_argument("--published", action="store_true", help="refresh only shows already in show-pages.json")
    args = ap.parse_args()

    reg = load(os.path.join(DATA, "shows.json"), {})
    content = load(os.path.join(DATA, "content.json"), {"shows": [], "episodes": []})
    catalog = load(os.path.join(DATA, "episodes.json"), [])
    ep_pages = load(os.path.join(DATA, "episode-pages.json"), {}).get("pages", {})
    hosts_info = reg.get("hosts", {})
    fetched = {s["key"]: s for s in content.get("shows", [])}
    shows = [s for s in reg.get("shows", []) if s.get("kind") != "youtube" or s.get("page")]
    for s in shows:
        s["slug"] = slug_for(s)
    only = set(args.only.split(",")) if args.only else None
    if args.published:  # new shows are published deliberately (with --only or a full run), not by the hourly job
        only = set(load(os.path.join(DATA, "show-pages.json"), {}).get("pages", {})) & (only or {s["key"] for s in shows})

    # Eclectic Polymath extras: Spotify links and episode pages by episode number
    sp_by_num = {e["episode_number"]: e["spotify_url"] for e in catalog if e.get("show", "").startswith("The Eclectic")}
    page_by_num = {}
    for k, path in ep_pages.items():
        show_key, n, _ = k.split(":")
        page_by_num[(show_key, int(n))] = path

    manifest = load(os.path.join(DATA, "show-pages.json"), {}).get("pages", {})

    def page_of(s):  # its own page if built (or being built now), else its entry on the network page
        if s["key"] in manifest or not only or s["key"] in only:
            return f"shows/{s['slug']}/"
        return f"pages/shows.html#{s['key']}"
    written, thin = 0, []
    for show in shows:
        key = show["key"]
        if only and key not in only:
            continue
        info = fetched.get(key, {})
        eps = [e for e in content.get("episodes", []) if e.get("show") == key and e.get("kind") != "short"]
        if args.fetch and show.get("rss"):
            try:
                eps = fetch_feed(show["rss"])
            except Exception as e:  # noqa: BLE001
                print(f"  {key}: feed fetch failed ({e}); using content.json")
        eps.sort(key=lambda e: e.get("date") or "", reverse=True)
        for e in eps:
            m = re.match(r"\s*#\s*(\d+)", e.get("title") or "")
            if m:
                n = int(m.group(1))
                e["spotify_url"] = e.get("spotify_url") or (sp_by_num.get(n) if key == "polymath" else None)
                e["page"] = e.get("page") or page_by_num.get((key, n))
            if not e.get("spotify_url") and "open.spotify.com/episode/" in (e.get("url") or ""):
                e["spotify_url"] = e["url"]

        art = info.get("art")
        pal = palette(show, os.path.join(SITE, art) if art else "")
        links = []
        if info.get("spotify_url") or show.get("spotify"):
            links.append(("Listen on Spotify", info.get("spotify_url") or f"https://open.spotify.com/show/{show['spotify']}", True))
        if info.get("apple_url"):
            links.append(("Apple Podcasts", info["apple_url"], False))
        if info.get("youtube_url"):
            links.append(("YouTube", info["youtube_url"], False))
        if show.get("rss"):
            links.append(("RSS feed", show["rss"], False))

        # three related shows: same category, else the same tier
        pool = [s for s in shows if s["key"] != key and fetched.get(s["key"], {}).get("art")]
        same = [s for s in pool if show.get("category") and s.get("category") == show.get("category")] or \
               [s for s in pool if (s.get("tier") != "secondary") == (show.get("tier") != "secondary")]
        related = [{"name": s["name"], "tagline": s.get("tagline") or fetched[s["key"]].get("description", "")[:90],
                    "thumb": thumb(s["key"], fetched[s["key"]]["art"]), "path": page_of(s)} for s in same[:3]]

        root = "../../"
        page = show_page(show, info, eps, related, pal, links, root, hosts_info)
        path = f"shows/{show['slug']}/"
        written += write_if_changed(os.path.join(SITE, path, "index.html"), page)
        manifest[key] = path

        gaps = [f for f, ok in [("tagline", show.get("tagline")), ("about/description", show.get("about") or info.get("description")),
                                ("cover art", art), ("Spotify link", links), ("cadence", show.get("cadence")),
                                ("host bios", show.get("ai") == "full" or all(h in hosts_info for h in show.get("hosts") or []))] if not ok]
        if gaps:
            thin.append((show["name"], gaps))
        print(f"  {key}: {len(eps)} episodes, accent {pal['accent']} -> shows/{show['slug']}/")

    write_if_changed(os.path.join(DATA, "show-pages.json"), json.dumps(
        {"_readme": "Written by tools/build_shows.py: show key -> its page. The hub links shows here.", "pages": dict(sorted(manifest.items()))},
        indent=1) + "\n")
    print(f"pages written: {written}")
    if thin:
        print("thin data (not padded; add to site/data/shows.json):")
        for name, gaps in thin:
            print(f"  - {name}: {', '.join(gaps)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
