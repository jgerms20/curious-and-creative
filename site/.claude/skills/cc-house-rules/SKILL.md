---
name: cc-house-rules
description: The Curious & Creative Company's standing brand, copy, roster, and workflow rules for curiousandcreative.co. Load before writing or editing ANY copy, page, show entry, or design on this site, and before opening a PR. Triggers on copy edits, new sections, show list changes, About/Studio/Consultancy/Network pages, brand colors or type, "house rules", "brand guidelines".
---

# Curious & Creative house rules

Joshua shouldn't have to re-explain these. If a request conflicts with a rule, ask before you build.

## Who's who
- **Joshua German** and **Janel Moore** are the co-founders.
  - Joshua: creative strategy, production, editorial.
  - Janel: technology, finance, campaigns, and host of Too Much to Tweet.
- **Joshua is a strategist first.** "AI Strategy and Systems Lead" was a real title he held at TBWA and works as a proof point. Never lead with "AI strategist".
- **His TBWA role ended Nov 15, 2026.** Never present agency jobs as current, and never use "Senior Connections Strategist" on this site.
- **joshuamgerman.com is Joshua's own site.** This site is the company. Keep the two from sounding identical.

## Facts that must stay exact
- **Never invent** clients, results, numbers, quotes, testimonials, prices, capabilities or processes.
- **Not an LLC** (the filing happens January 2027). Never write LLC.
- **Founder-experience line**, word for word, in its own section: "Our founders bring experience from work on Levi's, Gatorade, DoorDash, DIRECTV, Sephora, MLB, and BMW." That experience is agency work, never C&C client work.
- **SCAiL** appears only in the site footer and once on About.
- **Contact** is admin@curiousandcreative.co through the Supabase inquiry form (`CC.mountInquiry`). No personal Gmail anywhere.
- **Exactly one @viewsbygerm link**, at the end of Studio > Photography.
- **Gen Alpha Intelligence Lab** sits behind a password gate (`CC.labGate`). Never print the password on a page.
- **Kindling and Inventions** live on joshuamgerman.com, not here.

## Structure (CONFIRMED)
- Three legs: **The Network**, **The Studio**, **The Consultancy**.
- The homepage and leg pages use identical leg names and leg lines.
- Event coverage is a named Studio service.
- Anything else drafted Nov 8–9 is PROPOSED until Joshua rules on it. Don't lock it in.

## Voice
- Plain, confident, conversational. Show, don't tell: lead with an image, then at most one short line per section.
- **No em dashes in new copy.**
- Don't overuse curiosity, intentional, meaningful, thoughtful or perspective.
- **Positioning to avoid:**
  - AI is not the company headline.
  - The company is not anti-advertising or anti-corporate.
  - Not every piece of media has to be educational.
- **Approved lines:**
  - "Curious first. Then creative."
  - "Media for people who want to leave more curious than they arrived."
- "What remains after the attention is spent?" is internal only.

## Show roster (`site/data/shows.json`)
- Umar's latest handoff is the source of truth.
- **Never rename a show** unless Joshua orders that specific rename.
- **Never delete a show.** To take one off the network, set `"active": false`; its old pages keep working.
- **New shows:**
  - pin `spotify` and `rss` when they're known;
  - otherwise add `match_owner`, so discovery only accepts feeds the fleet owns (namesake shows have burned us before).
- **Never hard-code show or episode counts** in copy. Use `[data-show-count]`.

## Brand system (`site/css/cc.css`)
- **Type:** Archivo, bold condensed display, pill headings (`.pill-title`, plus `--green`, `--pink`).
- **Colors:**
  - Paper `#FFFCF5`, ink `#151217`.
  - Accents: green `#37B34A`, pink `#EC3F8E`, gold `#FFC93C`, grape `#8E6FE0`, sky `#46C7E8`, orange `#FF8D27`.
  - Wordmark green `#1E8A33`, wordmark pink `#D11F77`.
- **Images and themes:**
  - Use only real assets (`data/photos.json`, show art, `assets/people/*`). No stock or generated photos of people.
  - Light and dark must both work.
  - No horizontal overflow at 375px.
  - Lazy-load below the fold, with real alt text.

## Done means
1. Run the `run-site` smoke test on every page you touched.
2. `node .claude/skills/run-site/crawl.mjs` reports `bad 0`.
3. Grep new copy for "—".
4. **Git:**
   - Work on the session branch. Never force-push.
   - If the last PR merged, reset to `origin/main` and open a NEW PR.
   - Merge main into the branch rather than rebasing.
