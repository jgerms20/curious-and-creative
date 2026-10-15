# {Show name}: show bible

**{One sentence: what the listener gets and why they can trust it.}**

| | |
|---|---|
| **Config** | `{show-id}` in [`config/shows.yaml`](../../../config/shows.yaml): market `{market}`, wave {n}, enabled {true/false} |
| **Lane · format** | {standard / strict / breaking / archive} · {daily_brief / breaking_flash / court_roundup / case_weekly / evergreen_story / proposed template} |
| **Cadence · length** | {cron and local time; note event triggers} · {min}-{max} min · max {n} stories |
| **Hosts** | {personas from [`config/voices.yaml`](../../../config/voices.yaml)}. Ava speaks the closing disclosure |
| **Disclosure** | Script {A-E} ([AI Disclosure](../../standards/ai-disclosure.md) §3), {about N} seconds |
| **Owner · version** | {showrunner agent} · {version}, {date} |

> **How to use this page.** The Showrunner keeps it and the Producer reads it before every script. Copy it to `<show-id>.md`, fill every section, keep it under 70 lines. Numbers cite the [facts sheet](../../research/facts-and-figures.md) by ID, our own reasoning is marked *(inference)*, prices carry "as of Oct 2026 — verify before buying", and no model version strings appear. Write plainly for Joshua and Janel.

## 1. Premise
{Two or three sentences: the promise, the audience's problem, what we do that others do not. Then one line: what this show is NOT.}

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| {group} | {need} | {apps, smart speakers, site, newsletter} |

## 3. Format and segments
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | {Open} | {date, top line} | {0:20} | {persona} |
| n | **Disclosure** | Script {A-E}, always last (DISC-1) | {seconds} | Ava |

## 4. Sources
| Tier | Sources (file in `config/sources/`) | How we use them |
|---|---|---|
| 1 official | {agency, court, data feed} | {facts, allegations with attribution} |
| 2 to 3 | {newsrooms; owner groups from `config/owners.yaml`} | {facts in our words plus a link, never read aloud} |
| Leads only | {anything tier 4} | {find the record, then cite the record} |

## 5. Lane and trust rules
{Lane numbers from Editorial Standards §2. Then the rules specific to this show, each with its rule id (for example BRK-8, CR-19, FAIR-12). Then "Never:" with the show's hard stops.}

## 6. Voice, disclosure and ads
{Persona notes and handoffs (Guide H-1 to H-5); pronunciation list location; the disclosure script; the ad stance from the [advertising plan](../../business/advertising-plan.md) §8.}

## 7. Sample cold open
> {Illustrative only. Facts in braces are placeholders, never real events. No "I was there", no "we spoke to", no opinions.}

## 8. Sample episode titles
{Five or six honest, descriptive titles with the place and subject. No clickbait, and no verdict words on crime or court shows (CR-15).}

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| {downloads per episode} | {number} | {F-ID or *(inference)*} |
| {trust: corrections, gate first-pass rate} | {number} | {rule id} |

## 10. Open items
{Unverified feeds, missing lexicon entries, founder decisions. Date each one.}
