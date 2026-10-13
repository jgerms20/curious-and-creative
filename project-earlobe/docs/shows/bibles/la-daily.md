# LA Daily: show bible

**A verified 6-to-8-minute morning brief for Los Angeles: city and county government, housing, transit, public safety and the business of entertainment, each claim checked before it airs.**

| | |
|---|---|
| **Config** | `la-daily` in [`config/shows.yaml`](../../../config/shows.yaml): market `los-angeles`, wave 0, enabled true |
| **Lane · format** | standard · `daily_brief` |
| **Cadence · length** | Mon-Fri 06:00 PT (cron `0 13 * * 1-5` UTC) · 6-8 min · max 7 stories |
| **Hosts · disclosure** | Lena (anchor) and Marcus (co-host) · Script A ([AI Disclosure](../../standards/ai-disclosure.md) §3), about 16 s, spoken by Ava |

## 1. Premise
The Los Angeles day in seven minutes: what City Hall and the county did, what changed on roads and rails, where housing is moving, what police and prosecutors announced, and what happened in the entertainment business, with sources named. LA County is not a news desert (F-AUD-08) and the market is crowded with public radio, TV groups and a major daily, so we compete on clarity, sourcing and a fixed time budget. **Not** a gossip or celebrity show, and not a courts show (LA Courts Roundup covers dockets).

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| Angelenos planning a commute or a day across a big region | Transit, traffic, weather and air in one pass | Podcast apps, smart speakers, car audio |
| Renters, owners and people working in or near entertainment *(inference)* | Housing votes with the count; business news from filings and two independent outlets | Apps, newsletter (`next`) |

## 3. Format and segments
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | Open | Date, "This is LA Daily, with Lena and Marcus", top line | 0:20 | Lena |
| 2 | Top story | The biggest verified story. Marcus adds the why | 1:30 | Lena, Marcus |
| 3 | Government, housing, transit | City, county, zoning, rent, LA Metro changes | 2:15 | Lena, Marcus |
| 4 | Public safety | Short, no levity. Court detail goes to LA Courts Roundup | 1:00 | Lena |
| 5 | Entertainment business | Filings, labor, production, deals. No gossip | 0:45 | Marcus |
| 6 | Weather | From the structured NWS block, plus air quality when flagged | 0:30 | Lena |
| 7 | Sports and culture | Lighter. Humor allowed here only | 0:45 | Marcus |
| 8 | One thing to remember | Repeat one idea, add no new claim | 0:15 | Lena |
| 9 | **Disclosure** | Script A, always last (DISC-1) | 0:16 | Ava |

## 4. Sources
Feeds are in `config/sources/los-angeles.yaml`; all 14 are `verified: false` (F-DATA-04). Each owner group counts once (`config/owners.yaml`). Gaps to fill: LAPD, LA County Sheriff, LA City Attorney and the Board of Supervisors have no feed yet (markets note §3.3).
| Tier | Sources | How we use them |
|---|---|---|
| 1 official | LA Metro (The Source), City of Los Angeles, LA County District Attorney, U.S. Attorney C.D. Cal., NWS alerts, council and board agendas (Public Meetings Watcher, `next`) | Facts, votes, charges with attribution |
| 2 | LA Times, LAist (Southern California Public Radio), KTLA (Nexstar), NBC Los Angeles (Comcast NBCUniversal), ABC7 (Disney), CBS Los Angeles (Paramount), LA Daily News (MediaNews Group) | Facts in our words plus a link |

## 5. Lane and trust rules
- **Standard lane:** 2 independent sources, one official record suffices, balance at least 70, 2 rewrites ([Editorial Standards §2](../../standards/editorial-standards.md)).
- **Crime items** follow the [Crime and Courts Rules](../../standards/crime-and-courts-rules.md): ladder words (CR-1), every allegation attributed (CR-5), no minors, no sexual-assault survivors, no uncharged suspects.
- **Entertainment business** runs on filings, official releases and two independent owner groups. Private people get more protection than public figures (FAIR-6).
- **Numbers** carry source, unit and period (NUM-2); "not adjusted for inflation" when true (NUM-5). Time words are true at air time, Pacific (ACC-10).
- **Never:** read an article aloud (NEVER-5), air a social post as proof (NEVER-6), claim presence such as "we heard" (NEVER-7).

## 6. Voice, disclosure and ads
Lena is crisp and civic here (not her unhurried History of Hollywood register); Marcus explains the why from sourced context only, never his own theory. Say "district attorney" in full on first mention, then "the DA's office"; letters for LAPD. The starter lexicon is in [Guide §5](../../standards/voice-and-persona-guide.md). **Ads:** ad-free days 1-30, Slot A from about week 4, Slot B at day 60 if completion holds; LA has four slots to sell with History of Hollywood (advertising plan §11). No ads next to tagged crime or tragedy stories.

## 7. Sample cold open (illustrative; braces are placeholders, not real events)
> **Lena:** Good morning, Los Angeles. It's {weekday}, {month} {day}. This is LA Daily, with Lena and Marcus.
> **Marcus:** Today: {top story, attributed}, a change on {Metro line}, and {weather line}.
> **Lena:** First, {top story}. {Who did what, said by whom, in under 20 words.}

## 8. Sample episode titles
- LA Daily, {weekday} {month} {day}: {council vote}, a {freeway} closure, morning fog
- LA Daily, {weekday}: Metro changes {line} service, and what the {housing item} means for renters
- LA Daily, {weekday}: {county board} approves {item}; {studio or union} announces {change}

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| Downloads per episode, month 6 to 12 | 40 / 120 / 400 (cons / base / opt); no higher until measured | F-AUD-03 *(inference)* |
| Cost per episode | about $2.56 to $3.16 | F-LLM-07 + F-TTS-17, as of Oct 2026 — verify before buying |
| Published by 06:00 PT; inside 6-8 min | every weekday; at least 90% *(inference)* | `shows.yaml`; Showrunner KPIs |
| Completion when Slot B opens; paid placements by day 90 | within 5 points of the ad-free baseline; 2 | Advertising plan §2, §11 |
| Material corrections | 0 per quarter *(inference)* | AUTO-6 |

## 10. Open items
Owner: Showrunner: Daily Briefs (`next`); version 1.0, October 12, 2026. All 14 feeds unverified, the CBS path least certain. The fixed-UTC cron moves to 05:00 local on Nov 1, 2026. Decide how much weight the Spanish edition (LA Diario, wave 2) takes from this show's audience.
