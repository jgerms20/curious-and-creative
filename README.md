# The Curious & Creative Company — website

This repository holds the website for The Curious & Creative Company, a Los Angeles creative company
founded by Joshua German and Janel Moore. The company has three parts:

- **The Network**: a media network of original shows and the social channels around them.
- **The Studio**: photography, event coverage, video, editing, podcast production, and websites for clients.
- **The Consultancy**: brand and cultural strategy, audience and content systems, podcast strategy, and AI
  workflow design, enablement, and training.

## How the site is built

The site is static HTML, CSS, and JavaScript in `site/`, with no build step for the pages themselves.

- `site/index.html` and `site/pages/*.html` are the pages. `site/js/cc.js` draws the shared header, footer,
  menu, and search on every page; `site/css/cc.css` is the shared stylesheet.
- Show and episode content is read at load time from JSON in `site/data/` (`shows.json` is the show
  registry; `content.json` is what the feeds returned).
- `scripts/refresh_content.py` pulls the latest episodes, videos, and artwork from the shows' podcast feeds
  and YouTube into `site/data/content.json`.
- `tools/build_shows.py` generates one page per show in `site/shows/`.
- `tools/build_episodes.py` generates per-episode pages in `site/episodes/` and `site/sitemap.xml`.

## Deploy

`.github/workflows/pages.yml` deploys `site/` to GitHub Pages on every push to `main` and every hour.
Each run refreshes content (`scripts/refresh_content.py`, then `tools/build_shows.py --fetch --published`),
commits any changed data back to the repo, and publishes. `.github/workflows/episodes.yml` rebuilds the
episode pages, and `.github/workflows/refresh-content.yml` refreshes content on working branches.

## Run it locally

```sh
cd site
python3 -m http.server 8765
```

Then open http://localhost:8765/. The refresh and build scripts use the Python standard library (Pillow is
optional, for cover thumbnails) and need network access to reach the feeds.

## Other folders

The repository also holds planning, production, and side-project folders outside `site/`. They are not part
of the website build.
