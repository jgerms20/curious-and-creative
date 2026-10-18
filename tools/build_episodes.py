#!/usr/bin/env python3
"""Generate one static, indexable page per podcast episode.

  python3 tools/build_episodes.py                 # rebuild every published page
  python3 tools/build_episodes.py --batch 2       # publish batch 2 (and rebuild the rest)
  python3 tools/build_episodes.py --only 126,184  # rebuild just these episode numbers
  python3 tools/build_episodes.py --check         # run the acceptance checks, change nothing

Reads   site/data/episodes.json   the episode catalog (7 fields per entry)
        site/data/overrides.json  optional per-episode YouTube / cover / cluster / highlights
Writes  site/episodes/<show-slug>/<n>-<title-slug>.html
        site/assets/covers/<show-slug>-<n>.jpg   (fetched once via Spotify oEmbed, then cached)
        site/sitemap.xml
        site/data/episode-pages.json  (published pages; the archive links its cards here)

Which batches are live is recorded in site/data/episode-pages.json, so a plain
re-run rebuilds exactly what's published. Output is byte-stable: re-running
without data changes rewrites nothing. Standard library only.
"""
import argparse
import html
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from datetime import date

# ------------------------------------------------------------------ config
SITE_BASE = "https://jgerms20.github.io/curious-and-creative/"  # becomes https://curiousandcreative.co/ later

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
DATA = os.path.join(SITE, "data")
OUT = os.path.join(SITE, "episodes")
COVERS = os.path.join(SITE, "assets", "covers")
MANIFEST = os.path.join(DATA, "episode-pages.json")

SHOWS = {
    "The Eclectic Polymath Podcast": {
        "slug": "eclectic-polymath", "key": "polymath",
        "spotify": "https://open.spotify.com/show/3dlagzJ0jiWLTB9mF3y069",
        "apple": "https://podcasts.apple.com/us/podcast/the-eclectic-polymath-podcast/id6790238134",
        "fallback_art": "assets/art/polymath.jpg",
    },
    "God is Brazilian": {
        "slug": "god-is-brazilian", "key": "brazil",
        "spotify": "https://open.spotify.com/show/4tAY78JV37aIgmJ2d1iF3w",
        "apple": None,
        "fallback_art": "assets/art/brazil.jpg",
    },
}

PROVEN = [126, 184, 96, 34, 40]  # batch 1: the proven five (Eclectic Polymath)


def batch_members(n):
    """Episode selector for a build batch (matches the brief's build order)."""
    if n == 1:
        return lambda e: e["show"].startswith("The Eclectic") and e["episode_number"] in PROVEN
    if n == 2:
        return lambda e: e["show"].startswith("The Eclectic") and 213 <= e["episode_number"] <= 222
    if 3 <= n <= 7:  # Eclectic Polymath by 50s: 0-49, 50-99, 100-149, 150-199, 200+
        lo = (n - 3) * 50
        hi = lo + 49 if n < 7 else 10 ** 6
        return lambda e: e["show"].startswith("The Eclectic") and lo <= e["episode_number"] <= hi
    if n == 8:
        return lambda e: e["show"] == "God is Brazilian"
    raise SystemExit(f"unknown batch {n} (1-8)")


# Topic clusters, matched as whole words against titles (accents ignored).
CLUSTERS = {
    "power-money": ["Kushner", "Ellison", "Larry Jackson", "Iger", "Altman", "Hobson", "Rothschild", "Rothschilds", "Medici",
                    "Dangote", "Emanuel", "Grede", "Avant", "Pichai", "Nadella", "Dorsey", "NVIDIA", "Thrive Capital",
                    "Trusts", "Estate Planning", "Billion", "Crypto", "Bankman-Fried", "Theranos", "Ten Percent", "CAA",
                    "Clearing Houses", "GameStop", "Ownership", "Wealth"],
    "brazil": ["Brazil", "Brazils", "Brazilian", "Amazon", "Brasil", "Sao Paulo", "Rio", "Pix", "Salvador", "Quilombos", "Santa Teresa",
               "Car Wash", "Gonzaguinha", "Pericles", "Pagode", "Oscar Freire"],
    "music": ["Music", "Motown", "Hitsville", "Jazz", "Coltrane", "Kamasi", "Funk", "George Clinton", "Badu", "Nipsey",
              "Spotify", "The Smiths", "Indie Band", "Rap", "Hip-Hop", "Kendrick", "Record Label", "Masters",
              "Local Natives", "Five Percent"],
    "la-hollywood": ["Hollywood", "Los Angeles", "Inglewood", "Santa Monica", "The Grove", "Americana", "Karen Bass",
                     "Nithya Raman", "Mayor", "Mayoral", "Disney", "Spider-Man", "Marvel", "DC", "Nolan", "Seinfeld",
                     "Charlie Sheen", "Sitcom", "Nathan Fielder", "Reality TV", "Kardashians", "South Central",
                     "South LA", "CAA", "WME", "Agent"],
    "history-ideas": ["Mbiti", "African Time", "Five Percent", "Religious Studies", "Orwell", "Emerson", "Rome", "Egypt",
                      "Socialism", "Talmud", "Buddha", "Buddhist", "Confucius", "Islam", "Church", "Harlem", "Pompeii",
                      "Bolshevik", "Apartheid", "Systems Thinking", "Black Feminism", "Genres", "New Deal", "Medici",
                      "British India", "East India Company", "Arabization", "Cultural Revolution", "Humiliation",
                      "Dinosaurs", "Homestead", "Big Ben", "Clock", "Polygraph", "Migration", "Empire", "Revolution", "Philosophy", "Theory"],
    "body-health": ["GLP", "Peptides", "Body Hacking", "Eczema", "CRISPR", "Yoga", "Fitness", "Medical Tourism", "Chakras",
                    "Cannabis"],
    "politics-world": ["Putin", "Xi Jinping", "Khamenei", "Kim Jong Un", "bin Salman", "Castro", "Cuba", "Cuban", "Iran",
                       "Taiwan", "Mussolini", "Oslo", "Yom Kippur", "Mongolia", "Philippines", "Obama", "Iran-Contra",
                       "PATRIOT Act", "Assange", "Khashoggi", "Clyburn", "Wes Moore", "Huey Long", "Fidel", "China",
                       "Chinese", "El Mencho", "Narco", "Cartel", "Fred Hampton", "Occupy", "Geopolitics", "Holy Wars"],
    "sports-games": ["FIFA", "NBA", "NFL", "World Cup", "Football", "Soccer", "Lockout", "Sports", "League", "Bill Simmons",
                     "Poker", "Chess", "Bowling", "Billiard", "Pool Halls", "Olympics", "Broncos", "Lakers", "Athlete"],
    "media-culture": ["Oprah", "Vogue", "Wintour", "Degrassi", "New York Times", "Media", "Television", "TV", "Fashion",
                      "Bourdain", "Celebrity", "Kevin Hart", "Taste", "Diana", "Princess", "Yoko Ono", "Plath", "Memes",
                      "Humor", "Breakup", "Me Too", "Hoaxes", "Influencer", "Creator", "Comedy", "Netflix", "Barbecue",
                      "Food", "Spirits", "Scholastic", "39 Clues", "A Different World", "Watches", "Anime", "Japan",
                      "Hello Kitty", "Cuteness", "Bruce Lee", "Film", "Journalism", "Dieter Rams", "Design", "Genre"],
    "faith-cosmos": ["Faith", "Tithing", "Holy", "Prophecy", "Sacred", "Aquarius", "Saturn", "Astrology", "Heaven", "Islam",
                     "Islamization", "Church", "Christianity", "Religion", "Religious", "Spiritual", "Ghosts", "Buddha"],
    "love-relationships": ["Love", "Gottman", "Marriage", "Breakup", "Relationships", "Intimacy", "Dating", "Twins", "Family"],
    "places-leisure": ["Theme Parks", "Travel", "Queen Mary", "SeaWorld", "Megaregion", "Earthquake", "Roller Rinks",
                       "Bowling", "Pool Halls", "Destinations", "Dollywood", "Pop-Up", "Halloween", "Community", "Cities", "City", "Malls"],
    "tech-ai": ["AI", "NVIDIA", "DeepMind", "Hassabis", "OpenAI", "Google", "Microsoft", "Twitter", "Bitcoin", "Xbox",
                "Nanotechnology", "Wii", "Gaming", "Unabomber", "Theranos", "Gen Alpha", "Internet"],
}

SIGNOFF = re.compile(r"(Follow along for the next deep dive|Stay curious\b|Follow the show|Subscribe (?:to|for|and)|"
                     r"Like,? (?:and )?subscribe|Leave a (?:rating|review)|Rate and review|Thanks for listening|"
                     r"Support the show|Connect with|Follow (?:me|us) on|https?://|www\.)", re.I)

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


# ------------------------------------------------------------------ helpers
def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def fold(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'")  # keep apostrophes: "Brazil’s" must still match Brazil
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def title_slug(title):
    t = re.sub(r"^\s*#\s*\d+\s*:?\s*", "", title)
    t = re.sub(r"[^a-z0-9\s-]", "", fold(t).lower().replace("&", " and "))
    words, out = t.split(), []
    for w in words:
        if len("-".join(out + [w])) > 60:
            break
        out.append(w)
    return "-".join(out) or "episode"


def spotify_id(url):
    m = re.search(r"/episode/([A-Za-z0-9]{22})", url or "")
    return m.group(1) if m else None


def human_date(iso):
    y, m, d = (int(x) for x in iso[:10].split("-"))
    return f"{MONTHS[m - 1]} {d}, {y}"


def clock(ms):
    s = round(ms / 1000)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"


def iso_duration(ms):
    s = round(ms / 1000)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "") + (f"{sec}S" if sec or not (h or m) else "")


def paragraphs(desc):
    """Catalog descriptions arrive with paragraphs run together ("...end.Next para").
    Split on explicit breaks when present, else on a sentence end glued to a capital."""
    if "\n" in desc:
        parts = re.split(r"\n\s*\n|\n", desc)
    else:
        parts = re.split(r"(?<=[.!?…\"”’)])(?=[A-Z“\"‘(])", desc)
    return [" ".join(p.split()) for p in parts if p.strip()]


def strip_signoff(paras):
    out = []
    for p in paras:
        m = SIGNOFF.search(p)
        if m:
            head = p[:m.start()].strip()
            if head:
                out.append(head)
            break
        out.append(p)
    return out


def sentences(p):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z“\"])", p) if s.strip()]


def trimmed(desc):
    """The hook and the recognition points: the first 2-3 short paragraphs, sign-off cut."""
    paras = strip_signoff(paragraphs(desc))
    keep, size = [], 0
    for p in paras:
        if keep and (len(keep) >= 3 or size + len(p) > 900):
            break
        keep.append(p)
        size += len(p)
    if keep and len(keep[0]) > 900:  # one long block: keep whole sentences up to ~700 chars
        out, n = [], 0
        for s in sentences(keep[0]):
            if out and n + len(s) > 700:
                break
            out.append(s)
            n += len(s) + 1
        keep = [" ".join(out)]
    return keep


def key_points(desc, shown):
    """3-5 sentences lifted verbatim from the description: the names, numbers and turns
    a searcher would recognise. Never rewritten; a long sentence may be cut at a colon,
    semicolon or dash into its verbatim clauses."""
    body = strip_signoff(paragraphs(desc))
    seen = " ".join(shown)
    cands = []
    for i, p in enumerate(body):
        for j, s in enumerate(sentences(p)):
            parts = [s] if len(s) <= 240 else [c.strip(" ,") for c in re.split(r":\s|;\s|\s?—\s?|\s–\s", s)]
            if len(parts) == 1 and len(s) > 240:
                parts = [s]  # nowhere to cut it: keep the whole sentence if it isn't huge
            for k, c in enumerate(parts):
                if not 40 <= len(c) <= 320 or c.endswith(("?", "…", "...")):
                    continue
                words = c.split()
                names = sum(1 for w in words[1:] if w[:1].isupper())
                nums = len(re.findall(r"\$?\d[\d,.]*", c))
                cands.append((c not in seen, names + 2 * nums, i, j, k, c))
    named = [c for c in cands if c[1] >= 1]
    best = sorted(named, key=lambda c: (-c[0], -c[1]))[:5]  # not already in "About" first, then most specific
    for c in cands:  # too few names/numbers: top up with the description's own next sentences
        if len(best) >= 3:
            break
        if c not in best:
            best.append(c)
    if len(best) < 3:
        return []
    return [c[5] for c in sorted(best, key=lambda c: c[2:5])]


def clusters_for(title, override=None):
    if override:
        return list(override) if isinstance(override, list) else [override]
    t = fold(title)
    return [k for k, words in CLUSTERS.items()
            if any(re.search(r"(?<![A-Za-z])" + re.escape(fold(w)) + r"(?![A-Za-z])", t) for w in words)]


def load_json(path, default):
    return json.load(open(path)) if os.path.exists(path) else default


def write_if_changed(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path) and open(path, encoding="utf-8").read() == text:
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return True


# ------------------------------------------------------------------ cover art
def cover_for(ep, overrides, fetch=True):
    """Local file > Spotify oEmbed art (downloaded once, committed) > None."""
    show = SHOWS[ep["show"]]
    name = f"{show['slug']}-{ep['episode_number']}"
    if (ep.get("_dup") or 0) > 0:
        name += f"-{ep['_dup']}"
    o = overrides.get(f"{show['slug']}:{ep['episode_number']}", {})
    if o.get("cover"):
        return o["cover"]
    for ext in ("jpg", "jpeg", "webp", "png"):
        if os.path.exists(os.path.join(COVERS, f"{name}.{ext}")):
            return f"assets/covers/{name}.{ext}"
    if not fetch:
        return None
    try:
        q = urllib.parse.quote(ep["spotify_url"], safe="")
        req = urllib.request.Request(f"https://open.spotify.com/oembed?url={q}", headers={"User-Agent": "Mozilla/5.0"})
        thumb = json.loads(urllib.request.urlopen(req, timeout=20).read()).get("thumbnail_url")
        if not thumb:
            return None
        img = None
        big = re.sub(r"(/image/ab676563[0-9a-f]{4})5f1f", r"\1ba8a", thumb)  # oEmbed gives 300px; same art at 640px
        for u in dict.fromkeys([big, thumb]):
            try:
                img = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=20).read()
                break
            except Exception:  # noqa: BLE001
                continue
        if not img:
            return None
        os.makedirs(COVERS, exist_ok=True)
        path = os.path.join(COVERS, f"{name}.jpg")
        try:  # keep it at most 800x800 when Pillow is around; Spotify art is already 640px
            from io import BytesIO
            from PIL import Image
            im = Image.open(BytesIO(img)).convert("RGB")
            im.thumbnail((800, 800))
            im.save(path, "JPEG", quality=84, optimize=True, progressive=True)
        except ImportError:
            open(path, "wb").write(img)
        return f"assets/covers/{name}.jpg"
    except Exception as e:  # noqa: BLE001
        print(f"  cover fetch failed for {ep['title']}: {e}")
        return None


# ------------------------------------------------------------------ page
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'


def page_html(ep, path, cover, related, overrides, cover_ok):
    show = SHOWS[ep["show"]]
    root = "../../"
    o = overrides.get(f"{show['slug']}:{ep['episode_number']}", {})
    paras = trimmed(ep["description"])
    plain = " ".join(paras)
    meta_desc = plain if len(plain) <= 155 else plain[:154].rsplit(" ", 1)[0] + "…"
    points = o.get("highlights") or key_points(ep["description"], paras)
    sid = spotify_id(ep["spotify_url"])
    url_abs = SITE_BASE + path
    img_abs = SITE_BASE + cover
    ld = {
        "@context": "https://schema.org",
        "@type": "PodcastEpisode",
        "name": ep["title"],
        "episodeNumber": ep["episode_number"],
        "datePublished": ep["publish_date"],
        "duration": iso_duration(ep["duration_ms"]),
        "description": plain,
        "image": img_abs,
        "url": url_abs,
        "associatedMedia": {"@type": "MediaObject", "contentUrl": ep["spotify_url"]},
        "partOfSeries": {"@type": "PodcastSeries", "name": ep["show"], "url": show["spotify"]},
    }
    listen = [f'<a class="btn btn--sm" href="{esc(ep["spotify_url"])}" target="_blank" rel="noopener">Listen on Spotify</a>']
    apple = ep.get("apple_url") or show["apple"]
    if apple:
        listen.append(f'<a class="btn btn--ghost btn--sm" href="{esc(apple)}" target="_blank" rel="noopener">Apple Podcasts</a>')
    if o.get("youtube"):
        listen.append(f'<a class="btn btn--ghost btn--sm" href="{esc(o["youtube"])}" target="_blank" rel="noopener">Watch on YouTube</a>')
    pts = ""
    if isinstance(points, list) and points:
        items = []
        for p in points:
            if isinstance(p, dict) and p.get("t"):
                items.append(f'<li><span class="epi__ts">{esc(p["t"])}</span> {esc(p.get("text", ""))}</li>')
            else:
                items.append(f"<li>{esc(p if isinstance(p, str) else p.get('text', ''))}</li>")
        pts = f'<section class="epi__section" aria-labelledby="kp"><h2 id="kp">Key points</h2><ul class="epi__points">{"".join(items)}</ul></section>'
    rel = ""
    if related:
        cards = "".join(
            f'<a class="ep" href="{esc(root + r["path"])}" data-show="{show["key"]}"><img src="{esc(root + r["cover"])}" alt="" loading="lazy" width="72" height="72">'
            f'<span><b>{esc(r["title"])}</b><small>{esc(human_date(r["publish_date"]))}</small></span>'
            f'<span class="ep__when">{esc(clock(r["duration_ms"]))}</span></a>'
            for r in related)
        rel = f'<section class="epi__section" aria-labelledby="rel"><h2 id="rel">More like this</h2><div class="eps">{cards}</div></section>'
    desc_html = "".join(f"<p>{esc(p)}</p>" for p in paras)
    head_title = f"{ep['title']} — {ep['show']}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(head_title)}</title>
  <meta name="description" content="{esc(meta_desc)}" />
  <link rel="canonical" href="{esc(url_abs)}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{esc(ep['title'])}" />
  <meta property="og:description" content="{esc(meta_desc)}" />
  <meta property="og:image" content="{esc(img_abs)}" />
  <meta property="og:url" content="{esc(url_abs)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml" />
  <script>try{{var t=localStorage.getItem("cc-theme");document.documentElement.dataset.theme=t||(matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light")}}catch(e){{document.documentElement.dataset.theme="light"}}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{root}css/cc.css" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body data-page="episode" data-root="{root}">
<div data-cc="header"></div>
<main id="main" class="wrap">
<article class="epi" data-show="{show['key']}">
  <p class="epi__crumbs"><a href="{root}pages/shows.html#{show['key']}">{esc(ep['show'])}</a> · <a href="{root}pages/archive.html">Archive</a></p>
  <h1 class="epi__title">{esc(ep['title'])}</h1>
  <p class="epi__meta"><span>Episode {ep['episode_number']}</span><span><time datetime="{esc(ep['publish_date'])}">{esc(human_date(ep['publish_date']))}</time></span><span>{esc(clock(ep['duration_ms']))}</span></p>
  <img class="epi__cover{'' if cover_ok else ' epi__cover--show'}" src="{esc(root + cover)}" alt="{esc(ep['title'])}" loading="lazy" width="640" height="640" />
  <section class="epi__listen" aria-label="Listen">
    <iframe class="epi__player" src="https://open.spotify.com/embed/episode/{esc(sid)}?utm_source=generator" title="Play {esc(ep['title'])} on Spotify" loading="lazy" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"></iframe>
    <p class="showblock__links">{''.join(listen)}</p>
  </section>
  <section class="epi__section prose" aria-labelledby="about">
    <h2 id="about">About this episode</h2>
    {desc_html}
  </section>
  {pts}
  {rel}
  <nav class="epi__foot" aria-label="More from the show">
    <a class="pill-more" href="{root}pages/archive.html">Back to the archive {ARROW}</a>
    <a class="pill-more" href="{esc(show['spotify'])}" target="_blank" rel="noopener">{esc(ep['show'])} on Spotify {ARROW}</a>
  </nav>
</article>
</main>
<div data-cc="footer"></div>
<script src="{root}js/cc.js"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ build
def prepare(catalog):
    """Attach path, clusters and a duplicate index (God is Brazilian has #14 twice)."""
    seen = {}
    for ep in catalog:
        show = SHOWS[ep["show"]]
        k = (ep["show"], ep["episode_number"])
        ep["_dup"] = seen.get(k, 0)
        seen[k] = ep["_dup"] + 1
        ep["path"] = f"episodes/{show['slug']}/{ep['episode_number']}-{title_slug(ep['title'])}.html"
    return catalog


def related_for(ep, live, overrides):
    show = SHOWS[ep["show"]]
    o = overrides.get(f"{show['slug']}:{ep['episode_number']}", {})
    mine = set(clusters_for(ep["title"], o.get("cluster")))
    pool = [x for x in live if x is not ep and x["path"] != ep["path"]]
    scored = []
    for x in pool:
        ox = overrides.get(f"{SHOWS[x['show']]['slug']}:{x['episode_number']}", {})
        shared = len(mine & set(clusters_for(x["title"], ox.get("cluster"))))
        if shared:
            scored.append((shared, x["publish_date"], x))
    picks = [x for _, _, x in sorted(scored, key=lambda t: (t[0], t[1]), reverse=True)][:4]
    if len(picks) < 3:  # no cluster match: neighbours, then the proven five
        same = [x for x in pool if x["show"] == ep["show"]]
        near = sorted(same, key=lambda x: abs(x["episode_number"] - ep["episode_number"]))
        proven = [x for x in same if x["episode_number"] in PROVEN and x["show"].startswith("The Eclectic")]
        for x in near[:2] + proven + near[2:]:
            if x not in picks:
                picks.append(x)
            if len(picks) >= 4:
                break
    return picks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", type=int, action="append", help="publish this batch (1-8); repeatable")
    ap.add_argument("--only", help="comma-separated episode numbers to rebuild")
    ap.add_argument("--no-fetch", action="store_true", help="never download cover art")
    ap.add_argument("--check", action="store_true", help="run acceptance checks only")
    args = ap.parse_args()

    catalog = prepare([e for e in load_json(os.path.join(DATA, "episodes.json"), []) if e.get("show") in SHOWS])
    overrides = load_json(os.path.join(DATA, "overrides.json"), {})
    overrides = {k: v for k, v in overrides.items() if not k.startswith("_")}
    manifest = load_json(MANIFEST, {"batches": [], "pages": {}})

    if args.check:
        return check(catalog, manifest)

    batches = sorted(set(manifest.get("batches", [])) | set(args.batch or []))
    sel = [batch_members(b) for b in batches]
    live = [e for e in catalog if any(f(e) for f in sel)]
    only = {int(x) for x in args.only.split(",")} if args.only else None
    build = [e for e in live if not only or e["episode_number"] in only]
    print(f"batches {batches}: {len(live)} pages live, building {len(build)}")

    covers, missing_art = {}, []
    for e in live:
        c = cover_for(e, overrides, fetch=not args.no_fetch)
        if not c:
            missing_art.append(e["title"])
        covers[e["path"]] = c
        e["cover"] = c or SHOWS[e["show"]]["fallback_art"]

    written = 0
    for e in build:
        rel = related_for(e, live, overrides)
        written += write_if_changed(os.path.join(SITE, e["path"]), page_html(e, e["path"], e["cover"], rel, overrides, bool(covers[e["path"]])))
    print(f"pages written: {written} (unchanged: {len(build) - written})")

    pages = {f"{SHOWS[e['show']]['key']}:{e['episode_number']}:{spotify_id(e['spotify_url'])}": e["path"] for e in live}
    write_if_changed(MANIFEST, json.dumps({"_readme": "Written by tools/build_episodes.py. 'batches' = published build batches; 'pages' maps show:number:spotifyId -> page.", "batches": batches, "pages": dict(sorted(pages.items()))}, indent=1) + "\n")

    urls = [("", None), ("pages/archive.html", None)] + [(e["path"], e["publish_date"]) for e in sorted(live, key=lambda x: x["path"])]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, d in urls:
        sm.append(f"  <url><loc>{esc(SITE_BASE + p)}</loc>{f'<lastmod>{d}</lastmod>' if d else ''}</url>")
    sm.append("</urlset>")
    write_if_changed(os.path.join(SITE, "sitemap.xml"), "\n".join(sm) + "\n")

    if missing_art:
        print(f"WARNING: {len(missing_art)} pages use the show's art because the episode art isn't cached yet:")
        for t in missing_art:
            print("  -", t)
    return check(catalog, load_json(MANIFEST, {}))


# ------------------------------------------------------------------ acceptance checks
def check(catalog, manifest):
    pages = manifest.get("pages", {})
    by_path = {e["path"]: e for e in catalog}
    fails = []
    srcre = re.compile(r'(?:src|href)="([^"#?]+)')
    for key, path in pages.items():
        full = os.path.join(SITE, path)
        ep = by_path.get(path)
        if not os.path.exists(full) or not ep:
            fails.append(f"missing page or catalog entry: {path}")
            continue
        h = open(full, encoding="utf-8").read()
        base = os.path.dirname(full)
        for ref in srcre.findall(h):
            if ref.startswith(("http:", "https:", "mailto:", "data:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, ref))):
                fails.append(f"{path}: broken link {ref}")
        sid = spotify_id(ep["spotify_url"])
        if f"embed/episode/{sid}?" not in h or f'href="{esc(ep["spotify_url"])}"' not in h:
            fails.append(f"{path}: Spotify embed/link mismatch")
        m = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
        try:
            ld = json.loads(m.group(1))
            for k in ("name", "datePublished", "duration", "partOfSeries"):
                if not ld.get(k):
                    fails.append(f"{path}: JSON-LD missing {k}")
            if not (ld.get("associatedMedia") or {}).get("contentUrl"):
                fails.append(f"{path}: JSON-LD missing associatedMedia.contentUrl")
            if ld.get("name") != ep["title"] or ld.get("datePublished") != ep["publish_date"]:
                fails.append(f"{path}: JSON-LD name/date differ from catalog")
        except Exception as e:  # noqa: BLE001
            fails.append(f"{path}: JSON-LD invalid ({e})")
        h1 = re.search(r'<h1 class="epi__title">(.*?)</h1>', h)
        if not h1 or html.unescape(h1.group(1)) != ep["title"]:
            fails.append(f"{path}: <h1> differs from catalog title")
        if f">Episode {ep['episode_number']}<" not in h or human_date(ep["publish_date"]) not in h:
            fails.append(f"{path}: number/date differ from catalog")
        if "epi__cover--show" in h:
            fails.append(f"{path}: episode art not cached (show art shown)")
        if len(h.encode()) > 100_000:
            fails.append(f"{path}: {len(h.encode())} bytes (> 100 KB)")
    sm = open(os.path.join(SITE, "sitemap.xml")).read() if os.path.exists(os.path.join(SITE, "sitemap.xml")) else ""
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    if len(locs) != len(set(locs)):
        fails.append("sitemap has duplicate URLs")
    for loc in locs:
        rel = html.unescape(loc)[len(SITE_BASE):]
        if rel and not os.path.exists(os.path.join(SITE, rel)):
            fails.append(f"sitemap dead URL: {loc}")
    missing = [p for p in pages.values() if SITE_BASE + p not in [html.unescape(x) for x in locs]]
    fails += [f"sitemap missing {p}" for p in missing]
    print(f"\nchecks: {len(pages)} pages, {len(locs)} sitemap URLs, {len(fails)} failures")
    for f in fails:
        print("  FAIL", f)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
