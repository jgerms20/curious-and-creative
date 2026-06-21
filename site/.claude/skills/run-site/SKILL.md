---
name: run-site
description: Serve, smoke-test, and screenshot the Curious & Creative hub site (static HTML/CSS/JS in /site/). Use when an agent needs to run the site, take a screenshot, verify a visual change, check a page renders, or smoke every page after an edit. Triggers on "run site", "screenshot site", "preview the hub site", "check the site renders".
---

# run-site

The Curious & Creative hub site is static HTML/CSS/JS — no build, no framework. Drive it by serving with `python3 -m http.server` and screenshotting via a small Playwright driver: `.claude/skills/run-site/driver.mjs`.

All paths in this doc are relative to **`site/`** (this skill's host unit).

## Prerequisites

Already installed in this container:
- `python3` (built-in)
- Playwright + Chromium at `/opt/node22/lib/node_modules/playwright` and `/opt/pw-browsers/chromium-1194/`

Nothing to `apt-get`.

## Run (agent path — primary)

Boot the static server, then run the driver:

```bash
cd <site>
python3 -m http.server 8765 >/tmp/site-server.log 2>&1 &
echo $! > /tmp/site-server.pid
timeout 10 bash -c 'until curl -sf http://localhost:8765/ >/dev/null; do sleep 0.2; done'

# Smoke all 7 pages (exit 0 if no real errors)
node .claude/skills/run-site/driver.mjs

# Single page only
node .claude/skills/run-site/driver.mjs about
# Valid names: home about studio shows inventions art contact

# Dark mode — seeds localStorage + emulates prefers-color-scheme: dark.
# Writes <page>.dark.png alongside the light <page>.png.
THEME=dark node .claude/skills/run-site/driver.mjs

# Show "noise" (expected cert errors, expected 404s)
VERBOSE=1 node .claude/skills/run-site/driver.mjs home

# Custom port / host
BASE=http://localhost:9999 node .claude/skills/run-site/driver.mjs

# Stop the server when done
kill $(cat /tmp/site-server.pid) 2>/dev/null
```

Screenshots land at `.claude/skills/run-site/screenshots/<page>.png` (full-page, 1280px wide). Dark-mode runs write `<page>.dark.png` in the same dir. Read the PNG with the Read tool to actually see it.

Exit code: `0` = all good, `1` = a real JS error or a broken local asset was reported on at least one page. Cross-origin cert errors and the documented founder-photo 404s never fail the run.

## Run (human path)

```bash
cd <site>
python3 -m http.server 8765
# open http://localhost:8765 in a browser
```

Useless inside this container — there's no browser to render it. Use the driver.

## Tests

There is no test suite. The driver IS the smoke test.

## Gotchas

- **Reveal-on-scroll suppresses full-page screenshots.** Sections use `.reveal { opacity: 0 }` with an `IntersectionObserver` that adds `.is-visible` on scroll. A `fullPage` screenshot renders the whole canvas without scrolling, so without intervention most sections show as blank cream/blush bands. The driver works around this by emulating `prefers-reduced-motion: reduce` (`reducedMotion: 'reduce'` on the browser context) — see `css/base.css` and `js/main.js`, both honor reduced-motion by adding `.is-visible` immediately. If you ever change the reveal logic, keep the reduced-motion bypass intact or the driver's screenshots break silently.

- **About page emits two expected 404s.** `/assets/joshua.jpg` and `/assets/janel.jpg` are intentional drop-in slots. The `<img onerror="this.remove()">` handler hides them so the JG/JM initials fallback shows instead. The driver filters them via `EXPECTED_404S` — keep that list in sync if you ever rename the slots. If the founders ever drop their photos in, those filenames are what's expected.

- **Cross-origin cert errors are sandbox noise.** Google Fonts (Fredoka + Nunito) and the Spotify embed iframes both fetch over HTTPS and the container's TLS interception triggers `ERR_CERT_AUTHORITY_INVALID`. The site still renders — fonts fall back to system serif/sans, embeds show a "couldn't load" inline. Not a real bug. The driver classifies these as noise and reports `✓ (noise)` rather than failing.

- **Spotify embeds don't render content in this sandbox.** The cert error blocks the iframe from loading the show. The page layout still renders correctly (iframe placeholder is sized), but no cover art appears in the screenshot. Live on GitHub Pages, they show real cover art + a play button. If you need to validate the embed iframes themselves, do it on the live deployed URL, not locally.

- **EADDRINUSE if you re-run without killing the server.** `python3 -m http.server` doesn't `SO_REUSEADDR`. Always `kill $(cat /tmp/site-server.pid)` (or `pkill -f 'http.server 8765'`) before relaunching.

- **Deployment is via GitHub Actions, not this driver.** `.github/workflows/pages.yml` deploys `./site` to GitHub Pages on push to `main` and `claude/design-curious-creative-hub-sJkxe`. Repo setting required (one-time): Pages → Source → "GitHub Actions". The live URL ends up at `https://jgerms20.github.io/curious-and-creative/`.

- **Repo moved.** Git remote points at `jgerms20/curious-and-creative-agency` but pushes redirect to `jgerms20/curious-and-creative` — both work, but PRs against the new repo.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `EADDRINUSE` on port 8765 | `kill $(cat /tmp/site-server.pid)` or `pkill -f 'http.server 8765'`, then relaunch. |
| Driver fails with `Named export 'chromium' not found` | Playwright is CommonJS — use the `import pw from ...; const { chromium } = pw;` shape that's already in the driver. |
| All pages show blank middle sections in screenshots | The `reducedMotion: 'reduce'` context option got removed. Restore it on `browser.newContext()`. |
| `requestfailed: ... ERR_CONNECTION_REFUSED` on localhost | Server isn't running. Start it first; the poll loop above waits for it. |
| `console.error: Failed to load resource: net::ERR_CERT_AUTHORITY_INVALID` | Expected sandbox noise from Google Fonts / Spotify HTTPS. Ignore. |
| Driver exits `1` but only shows noise lines | A real error is being misclassified. Run with `VERBOSE=1` to see all classified messages; tighten the `noise` regexes in `driver.mjs` if needed. |

## Files

- `SKILL.md` — this file
- `driver.mjs` — Playwright smoke driver
- `screenshots/` — output from each run (gitignored-equivalent: small + regenerable, no need to commit)
