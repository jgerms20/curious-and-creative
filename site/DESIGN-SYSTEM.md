# Curious & Creative — Design System (Network Edition)

The public hub for everything Joshua German and Janel Moore make. Editorial,
media-network layout (Ringer-inspired structure), C&C colors, light + dark.

## Files
- `css/cc.css` — the only stylesheet: tokens (light + `[data-theme="dark"]`), header/drawer/search chrome, every section and page component.
- `js/cc.js` — shared runtime on every page: injects header/footer/drawer/search, theme toggle (saved as `localStorage['cc-theme']`, defaults to the OS setting), loads `data/*.json`, fuzzy search (typo + sound-alike tolerant: "Erica Badu" finds "Erykah Badu").
- `js/home.js` — homepage: rotating hero (flagship first), The Latest, Videos, show stack, Shorts (auto-hidden when none), ticker, photo strip.
- `js/pages.js` — Shows, Archive (search + filters), Photography (sets + lightbox), About show tiles.
- Page shell: `<body data-page="…" data-root="./|../">` with `<div data-cc="header">` / `<div data-cc="footer">`. Subpages were generated from one template; keep their `<head>` identical.

## Content pipeline (no manual updates)
- `data/shows.json` — hand-edited registry (names, hosts, taglines, Spotify/RSS/YouTube ids, art overrides). Add a show here.
- `scripts/refresh_content.py` (GitHub Actions: every deploy, every 6 hours on main, and on branch pushes that touch it) pulls episodes from RSS feeds, Spotify, and YouTube; mirrors show art, Joshua's photography sets, and portraits from joshuamgerman.com; writes `data/content.json` and `data/photos.json` and commits them.
- Shows sort by most recent episode; the flagship (The Curious & Creative Podcast) always leads.
- Spotify-only shows record each newest episode as it appears; pin the show's RSS feed in `shows.json` to get the full back catalog.

## Tokens
Paper `#FFFCF5` / dark `#0F0D11` · Ink `#151217` / `#F7F2EA` · Green `#37B34A` · Pink `#EC3F8E` · Gold `#FFC93C` · Grape `#8E6FE0` · Sky `#46C7E8` · Orange `#FF8D27`.
Show colors: ccpod green, polymath grape, tmtt pink, abolitionist gold, approachable sky, dominate orange (`[data-show]` sets `--c`).
Type: Archivo (variable width) — headlines 850–900 weight, 78–85% width, uppercase. Radii: cards 22px, boxes 32px, pills.

## Signature pieces
Rotated pill section titles · Pulse topic rail (chips open search) · story-style hero with progress bars, blurred art bed, drifting zoom, up-next minis · hover-fade cards · black boxes with fading video list + "All videos" · shuffle card stack with audio waves · tilted auto-scrolling ticker · masonry photography with lightbox.

## Kindling (`/kindling/`)
A product microsite inside the hub chrome. It uses `css/cc.css` + `js/cc.js`, then `kindling/kindling.css` + `kindling/kindling.js`.
- Pages: `index.html` (product), `play.html` (digital game), `shop.html` (cart + checkout), `deck.html` (gallery; `?layout=letter|press` is print mode for the PDF script).
- Data: `data/kindling-cards.json` is compiled from `Production/Kindling/deck/*.json` by `scripts/build_kindling.py`. Never hand-edit it. `data/kindling-shop.json` holds products, prices, and the checkout mode (see `Strategy/Kindling/shop-setup.md`).
- Tokens: night `#170B0A`, cream `#FBF0E2`, flame `#FF6A2B`, gold `#FFC24B`, ember `#C2321F`. Deck colors come from `[data-deck]`, which sets `--d`. Card prompts use Fraunces and labels use Archivo, both self-hosted in `assets/fonts/` so the print PDFs embed them.
- Cards (`.kcard`) size from `--w` and scale their internals with container units. Never put `cqw` on `.kcard` itself, only on its children.
