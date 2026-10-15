# Network Lineup

**Every show and feed the Curious & Creative Network will run at scale, by layer, with cadence, length, lane, voice and launch wave.**

| | |
|---|---|
| **Publisher** | Curious & Creative LLC |
| **Source of truth** | Live and configured shows: [`config/shows.yaml`](../../config/shows.yaml). Everything else: the Expansion roster in [`agent-catalog.md`](../blueprint/agent-catalog.md) (sections A and B) |
| **Voices** | [`config/voices.yaml`](../../config/voices.yaml) (six personas) and the [Voice & Persona Guide](../standards/voice-and-persona-guide.md) |
| **Show bibles** | [`bibles/`](bibles/): one page for each wave-0 show, plus a [template](bibles/_TEMPLATE.md) for all the others |
| **Owner** | Programming Director (`next`) proposes the order; the founders greenlight each wave |
| **Version** | 1.0, October 12, 2026. Lengths, voices and waves for shows not in `shows.yaml` are proposals *(inference)* unless the catalog states them |

## 1. The short version

- **What it is.** 73 shows and feeds in six layers. Seven are live-ready now (wave 0). Wave 1 adds 20 more instances, which brings the network to 27, the same count the cost model uses for its Wave 1 stage (`finance/build_cost_model.py`). Later waves are mostly the same templates cloned into new cities.
- **Why this shape.** Daily briefs build the local habit. Courts and true crime are the places where the Trust Stack matters most and where routine local dockets look underserved *(inference, [competitive note](../research/notes/competitive-landscape.md))*. Archive series pile up an evergreen back catalog. Niche feeds fill the always-on long tail. The Breaking Desk is the trust brand.
- **What it costs.** One 7-minute verified brief costs about $2.00 in Claude work plus $0.56 to $1.16 of voice, against about $1.03 of ad revenue at 120 downloads (F-LLM-07, F-TTS-17, F-ADS-12). *As of Oct 2026 — verify before buying.* So the lineup grows slowly, and sponsors decide which feeds stay.

## 2. How to read the tables

| Column | Meaning |
|---|---|
| **Bold name** | The show is already in `shows.yaml` (wave 0 live, NYC and Chicago configured but off) |
| **Lane** | How much proof the gate demands ([Editorial Standards §2](../standards/editorial-standards.md)): `standard` 2 independent sources; `strict` 2, plus an official record for anything sensitive; `breaking` 3, no single-source claims; `archive` 2, with more narrative room |
| **Voice** | Personas from `voices.yaml`. **Ava also speaks the AI disclosure at the end of every episode of every show** ([AI Disclosure](../standards/ai-disclosure.md) DISC-2). "new:" voices do not exist yet and must pass Voice & Persona Guide §6 |
| **Wave** | When the first instance launches. 0 = test markets, 1 = next, 2 to 5 = later (market waves from the catalog roster). "Cadence" and "Length" for event feeds describe a trigger, not a clock |

## 3. Rules for the whole lineup

1. **Slow, human-plausible rollout.** The closest rival flooded feeds, was hidden by Castro and flagged by the Podcast Index, and its feeds averaged about 69 downloads an episode (F-IPA-10, F-HOST-18, F-IPA-07). Listen Notes removed 31.5% of its August 2026 new submissions as AI (F-HOST-18). Roughly 25% to 45% of new feeds are now AI (F-AUD-01). Every new show is a decision, not a batch job.
2. **Niche-feed rules** (from the catalog): no news, no episode, never filler; one show per idea, no title variants to game search; honest titles with the place and the subject; same Trust Stack and lanes as every other show; a feed under its audience floor for 30 days is paused or merged.
3. **Disclosure scripts by layer** ([AI Disclosure §3](../standards/ai-disclosure.md)): A for dailies and niche feeds, B for Breaking, C for courts and true crime, D for archive, E added when a sponsor is on the episode.
4. **Ads by lane** ([advertising plan](../business/advertising-plan.md) §2 and §8): dailies and archive carry ads (one slot at launch). Courts and true crime are opt-in sponsors only, not sold in the first 90 days *(inference)*. Breaking is ad-free at launch, and always for deaths and attacks.
5. **Nothing launches until its sources are verified.** All 43 market feeds in `config/sources/` are still `verified: false` (F-DATA-04), and court portals often bar bulk automation (F-DATA-10).
6. **Hosting.** Per-show billing gets expensive past about 50 shows; pick a host with pooled downloads and unlimited shows before wave 2 (F-HOST-01, recall).
7. **Clock change.** The fixed-UTC crons in `shows.yaml` run one hour early in local time when daylight saving ends on Nov 1, 2026, until the Scheduler is built (catalog note).

## 4. Layer 1: daily local briefs (11)

Format `daily_brief`. The habit-builders and the main ad inventory.

| # | Show | Cadence | Length | Lane | Voice | Wave |
|---|---|---|---|---|---|---|
| D1 | **Columbia Daily**: SC capital, Richland and Lexington counties | Mon-Fri 06:00 ET | 6-8 min | standard | Mara + Theo | 0 |
| D2 | **LA Daily**: city, county, housing, transit, entertainment business | Mon-Fri 06:00 PT | 6-8 min | standard | Lena + Marcus | 0 |
| D3 | **NYC Daily** (configured, off) | Mon-Fri 06:00 ET | 6-8 min | standard | Mara + Marcus | 1 |
| D4 | **Chicago Daily** (configured, off) | Mon-Fri 06:00 CT | 6-8 min | standard | Theo + Lena | 1 |
| D5 | Columbia Weekend: Saturday look-ahead (events, openings, weather, games) | Sat 07:00 ET | 8-10 min | standard | Mara + Theo | 1 |
| D6 | LA Weekend: the same format for LA | Sat 07:00 PT | 8-10 min | standard | Lena + Marcus | 1 |
| D7 | Week in Review: Sunday recap with the week's follow-ups (Columbia and LA first) | Sun 08:00 local | 15 min | standard | city anchors (Mara / Lena) | 2 |
| D8 | State House Daily: SC first, then CA, GA, TX | Weekdays in session | 5-7 min | standard (strict for election items) | Marcus + Theo | 2 |
| D9 | LA Diario: Spanish daily (then Houston, Miami, Phoenix) | Mon-Fri 06:30 PT | 6-8 min | standard | new: Spanish pair | 2 |
| D10 | {City} Daily for the next 20 markets (Charleston, Upstate, Charlotte, Atlanta, Houston, then waves 3 to 5) | Mon-Fri 06:00 local | 6-8 min | standard | the four local voices, paired per market | 2 |
| D11 | Campus Beat: UofSC, UCLA, USC, then each market's universities | Weekly in term | 6-8 min | standard | Theo + Lena | 3 |

## 5. Layer 2: The Breaking Desk and spin-offs (8)

Format `breaking_flash`. Ava is the one calm voice for every English flash, so "Ava" means "confirmed only". Spin-offs launch only when the main feed shows enough volume to justify them *(inference)*.

| # | Show | Cadence | Length | Lane | Voice | Wave |
|---|---|---|---|---|---|---|
| B1 | **The Breaking Desk**: major national and global events | Event, 30 min gap | 2-4 min | breaking | Ava | 0 |
| B2 | Breaking Desk: Weather & Disasters (hurricanes, quakes, wildfires; official sources only) | Event | 2-3 min | breaking | Ava | 1 |
| B3 | Breaking Desk: Courts (landmark rulings, major verdicts within minutes) | Event | 2-4 min | breaking | Ava | 2 |
| B4 | Decision Day: same-day Supreme Court opinion flashes | Opinion days | 2-3 min | breaking | Ava | 3 |
| B5 | Breaking Desk: Sports (franchise sales, superstar trades, coaching firings, titles) | Event | 2-3 min | breaking | Ava | 3 |
| B6 | La Mesa de Última Hora: the Breaking Desk in Spanish | Event | 2-4 min | breaking | new: Spanish voice | 3 |
| B7 | Breaking Desk: Space (launches, landings, crewed missions) | Event | 2-3 min | breaking | Ava | 4 |
| B8 | Breaking Desk: Markets (mega-mergers, crashes, CEO exits) | Event | 2-3 min | breaking | Ava | 4 |

## 6. Layer 3: courts, per city and federal (10)

Format `court_roundup`. Every courts show says the presumption of innocence out loud ([Crime and Courts Rules](../standards/crime-and-courts-rules.md)).

| # | Show | Cadence | Length | Lane | Voice | Wave |
|---|---|---|---|---|---|---|
| C1 | **LA Courts Roundup**: filings, rulings, pleas, sentencings, DA and US Attorney releases | Mon-Fri 17:00 PT | 8-12 min | strict | June | 0 |
| C2 | NYC Courts Roundup (state courts, S.D.N.Y., E.D.N.Y.) | Weekdays | 8-12 min | strict | June | 1 |
| C3 | Cook County Courts (with N.D. Ill.) | Weekdays | 8-12 min | strict | June | 1 |
| C4 | Columbia Courts (Richland, Lexington, D.S.C.) | Weekly | 10-15 min | strict | June | 2 |
| C5 | Courts roundups for new markets: Charlotte and Atlanta (w2), Philadelphia (w3), "Vegas in Court" (w5) | Weekly, weekdays when volume allows | 8-12 min | strict | June, then courts-2 | 2 |
| C6 | Federal Docket Weekly: notable new federal suits and rulings nationwide | Weekly | 10-15 min | strict | June | 3 |
| C7 | Supreme Court Week: arguments, orders and opinions, in term | Weekly in term | 10-15 min | strict | June | 3 |
| C8 | Hollywood in Court: entertainment litigation in LA Superior and C.D. Cal. | Weekly | 8-12 min | strict | new: courts-2 | 3 |
| C9 | Bankruptcy Watch: major business bankruptcies | Weekly | 8-10 min | strict | courts-2 | 4 |
| C10 | Appeals Watch: Fourth and Ninth Circuits | Weekly | 8-12 min | strict | courts-2 | 4 |

## 7. Layer 4: true crime (9)

Formats `case_weekly`, `evergreen_story`, `niche_minute`. All strict. The presumption of innocence is said in every episode. No mugshots. Minors and sexual-assault survivors are never named.

| # | Show | Cadence | Length | Lane | Voice | Wave |
|---|---|---|---|---|---|---|
| T1 | **Case Tracker**: weekly best of the last 7 days plus development flashes | Fri 10:00 ET + event | 15-25 min (flashes 2-4) | strict | June + Theo | 0 |
| T2 | **Cold Case Files**: unsolved adult cases where an agency is asking for tips | Tue/Thu 05:00 ET | 18-25 min | strict | June | 0 |
| T3 | Cold Case Files: Carolinas | Weekly | 18-25 min | strict | June | 2 |
| T4 | Missing: {Region}: official missing-adult appeals with the tip line, short and respectful (minors excluded, CR-21) | Weekly + event | 2-4 min | strict | June | 2 |
| T5 | Cold Case Files: Southern California | Weekly | 18-25 min | strict | new: courts-2 | 3 |
| T6 | Trial Day: a temporary daily feed for one major trial, ending at the verdict | Trial days | 5-8 min | strict | courts-2 + Theo | 3 |
| T7 | The Verdict: weekly verdicts and sentencings across our markets | Weekly | 8-12 min | strict | courts-2 | 3 |
| T8 | Solved: cold cases closed by new evidence, from official announcements | Biweekly | 15-20 min | strict | courts-2 | 4 |
| T9 | Exonerated: wrongful convictions overturned, from court records (counsel review first) | Biweekly | 15-20 min | strict | courts-2 | 4 |

## 8. Layer 5: archive series (15)

Format `evergreen_story`. Told from records, never from the legend. No third-party audio without a license (COPY-6); History of Hollywood describes films and never plays them (COPY-7), and the music series follow the same practice unless a license is in hand. Back-catalog episodes are Batch API candidates at 50% off (F-LLM-05).

| # | Show | Cadence | Length | Lane | Voice | Wave |
|---|---|---|---|---|---|---|
| A1 | **History of Hollywood**: film-industry and LA history from primary records | Mon/Wed/Fri 02:00 PT | 15-20 min | archive | Lena | 0 |
| A2 | Hometown History: Columbia (the Congaree to the 1865 burning to the modern capital) | Weekly | 15-20 min | archive | Marcus | 1 |
| A3 | Lost Los Angeles: vanished landmarks, neighborhoods and streetcar lines | Weekly | 12-18 min | archive | Lena | 1 |
| A4 | Front Page, 100 Years Ago: public-domain newspaper stories retold for today (1926 now; F-LEGAL-17, F-DATA-08) | Daily | 3 min | archive | Theo | 1 |
| A5 | Central Avenue: LA's jazz history (a season of 10) | Weekly | 15-20 min | archive | Lena | 2 |
| A6 | Hometown History: Charleston | Weekly | 15-20 min | archive | Mara | 2 |
| A7 | Hometown History: Philadelphia (w3), Boston (w4) | Weekly | 15-20 min | archive | Marcus | 3 |
| A8 | On This Day in {City} | Daily | 2 min | archive | Mara | 3 |
| A9 | Landmark Cases: Supreme Court decisions that changed daily life | Weekly | 15-20 min | archive (strict for crime facts) | Marcus | 3 |
| A10 | Neighborhood Notes: one neighborhood a week, from records, meetings and history | Weekly | 8-10 min | standard | Mara | 3 |
| A11 | Austin music history (title to be set) | Weekly | 15-20 min | archive | Lena | 4 |
| A12 | Sports History: This Week | Weekly | 10-15 min | archive | Theo | 4 |
| A13 | Motor City Sound (Detroit) | Weekly | 15-20 min | archive | Marcus | 5 |
| A14 | Birth of Jazz (New Orleans) | Weekly | 15-20 min | archive | Lena | 5 |
| A15 | Music City Stories (Nashville) | Weekly | 15-20 min | archive | Theo | 5 |

## 9. Layer 6: hyper-specific always-on feeds (20)

Formats `meeting_watch`, `niche_minute`, `data_minute`, `scoreboard`, `breaking_flash` (local), all *(proposed)* templates run by the Niche Showrunner. Most start in Columbia and LA, then clone into each market that has the data.

| # | Show | Cadence | Length | Lane | Voice | Wave |
|---|---|---|---|---|---|---|
| N1 | City Council Watch: one feed per governing body, out within hours of each meeting, plus a Friday preview | Per meeting | 3-6 min | standard | Marcus | 1 |
| N2 | School Board Watch: Richland One and Two, LAUSD and so on | Per meeting | 3-6 min | standard (minors rule) | Theo | 2 |
| N3 | Election Night {City}: official tallies only, no projections (only if eval-tested) | Election nights | 1-3 min | strict | Ava | 3 |
| N4 | Open & Shut: restaurant and shop openings and closings | Mon/Wed/Fri | 3-4 min | standard | city anchors (Mara / Lena) | 1 |
| N5 | Permit Pulse: notable building permits and development | Weekly | 4-5 min | standard | Marcus | 1 |
| N6 | Main Street Ledger: new business filings, layoffs (WARN), big hires | Weekly | 4-5 min | standard | Theo | 2 |
| N7 | Pollen & Air: pollen and air quality (Columbia's pollen season, LA smog) | Daily in season | 90 sec | standard | city anchors (Mara / Lena) | 1 |
| N8 | Weather Ready: speaks only when an official warning fires | Event | 1-2 min | standard | city anchors (Mara / Lena) | 1 |
| N9 | Recall Roundup: FDA, USDA, CPSC and NHTSA recalls, official data only | Daily when recalls qualify | 2-3 min | standard | Theo | 1 |
| N10 | Wildfire Watch LA (seasonal) | Event + daily in season | 1-3 min | standard | Lena | 2 |
| N11 | Hurricane Desk: Carolinas, Gulf and Florida, June to November | Event + daily in season | 2-3 min | standard | Mara | 2 |
| N12 | Transit Minute: LA Metro, CTA and MTA service changes | Weekday mornings | 2 min | standard | Marcus | 3 |
| N13 | Cost of Living Watch: gas, rent, utilities and prices from official data | Weekly | 4-5 min | standard | Theo | 3 |
| N14 | Friday Night Scoreboard: high school football, SC first (results only, see decisions) | Fri night / Sat morning in season | 4-6 min | standard (minors rule) | Theo | 3 |
| N15 | Real Estate Pulse: big sales, development and market data | Weekly | 4-6 min | standard | Marcus | 3 |
| N16 | Liquor License Watch: which bars and restaurants are coming | Weekly | 3-4 min | standard | city anchors (Mara / Lena) | 3 |
| N17 | Jobs Day: BLS release days, national plus each market's numbers | Release days | 3-4 min | standard | Marcus | 3 |
| N18 | Community Calendar: free and cheap things to do this week | Weekly | 4-6 min | standard | city anchors (Mara / Lena) | 3 |
| N19 | Film Permits LA: what is shooting where (terms to be cleared) | Weekly | 3-4 min | standard | Lena | 4 |
| N20 | Health Inspection Report: official inspection results only | Weekly | 3-5 min | strict (named businesses) | courts-2 | 4 |

## 10. Rollout by wave

Instances counted the way the cost model counts them: Columbia and LA copies of one template are two shows. Waves 2 to 5 follow the market order in the catalog (24 markets in all).

| Wave | New concept rows | Live shows after the wave | What has to exist first |
|---|---|---|---|
| 0 | 7 | 7 | Engine v1 (built), Apple Podcasts Connect and Spotify for Creators accounts (done by Joshua), the seven bibles, verified feeds, a media-lawyer review of the strict-lane shows |
| 1 | 16 | 27 (+20: 4 dailies, 1 breaking, 2 courts, 3 archive, 10 niche) | Beat agents for NYC and Chicago, Public Meetings, Records & Filings, Weather & Hazard and Press-Release watchers (all `next`), the Niche Showrunner pulled forward from `future`, a licensed pollen source (vendor TBD) |
| 2 | 15 | not itemized | Southeast cluster plus Houston (below), Legislature Watcher, Spanish Editions Editor, an unlimited-shows host (F-HOST-01) |
| 3 | 22 | not itemized | Civic Data Watcher and Sports Watcher (both `future`), Federal and Supreme Court coverage, second strict-lane voice |
| 4 | 10 | not itemized | Bay Area, Seattle, Denver, Austin, Boston; counsel review for Solved and Exonerated |
| 5 | 3 | not itemized | Music licensing method settled; culture cities |

**Wave-1 niche instances (10).** City Council Watch, Open & Shut, Pollen & Air and Weather Ready in both Columbia and LA (8), Permit Pulse in LA (1) and Recall Roundup (1). The cost model's stages are Test 7, Wave 1 27, Scale 157 and Dominate 693 shows; the last two are not tied to a wave number here.

**Reality check on the top end** *(inference)*. The cost model assumes 100 niche feeds at Scale and 500 at Dominate (`SHOW_COUNTS`). Our 20 niche templates in 24 markets give 480 only if each ran once everywhere. Wildfire, hurricane and film-permit feeds do not fit every city, so the rest would have to come from meeting feeds (one per governing body) and new templates. The facts sheet already flags that count as a platform-standing risk (F-IPA-10, F-AUD-01).

## 11. Markets by wave

| Wave | Markets | Signature shows at launch |
|---|---|---|
| 0 | Columbia SC, Los Angeles, national desk | Seven wave-0 shows |
| 1 | New York City, Chicago | Dailies and courts roundups; the other shows clone later |
| 2 | Charleston SC, Greenville-Spartanburg SC, Charlotte, Atlanta, Houston | Daily in each; Hometown History: Charleston; Hurricane Desk; Charlotte and Atlanta Courts; State House Daily: Georgia; Houston Diario |
| 3 | Washington DC, Philadelphia, Phoenix, Dallas-Fort Worth, Miami | DC adds Supreme Court Week and Federal Docket Weekly; Breaking Desk: Sports (DFW); Diarios in Phoenix and Miami; Real Estate Pulse: Miami |
| 4 | Bay Area, Seattle, Denver, Austin, Boston | Transit Minute: Bay Area and Seattle; State House Daily: Colorado; Austin music history; Hometown History: Boston |
| 5 | Detroit, New Orleans, Nashville, Las Vegas, Twin Cities | Motor City Sound; Birth of Jazz; Music City Stories; Vegas in Court; Weather Ready: Twin Cities |

## 12. Voice load

Each persona is a voice, not a life. Six personas, plus the proposed new voices, carry 73 rows, so each is heard on many feeds. The Voice Director keeps a cap on overexposure ([voice-director](../../agents/studio/voice-director.md)). Counts are rows in this lineup that name the persona.

| Persona | Rows | Where | Watch-out |
|---|---|---|---|
| Lena | 17 | LA dailies, History of Hollywood, Lost LA, jazz and music series | The most heard voice; keep archive Lena (unhurried) distinct from anchor Lena (crisp) |
| Theo | 15 | Co-host on Columbia and Chicago, Case Tracker, short daily feeds | Asks, never opines (Guide H-2) |
| Mara | 13 | Columbia, NYC, city-anchor niche feeds | Morning-anchor register; no jokes near crime or tragedy |
| Marcus | 13 | LA, NYC, meeting and data feeds, hometown history | Explains the why from sources, never his own theory |
| June | 11 | LA, NYC and Cook courts, Case Tracker, Cold Case Files | One slow strict-lane voice; wave-3 shows move to courts-2 |
| courts-2 (new) | 10 | Strict-lane shows from wave 3 | Needs Voice Design and a name check; without it June would carry 21 rows |
| Ava | 8, plus every closing | Every English breaking flash, Election Night, all 73 disclosures | Keep her to breaking and the disclosure, never a local daily |
| Spanish pair (new) | 2 | LA Diario, La Mesa de Última Hora | The Spanish Editions Editor adapts, it does not translate |

## 13. Decisions for Joshua and Janel

1. **Courts order.** Wave 1 puts NYC and Cook County courts ahead of Columbia Courts to match the cost model's three courts shows. If Columbia's home-market value matters more, swap Columbia Courts (C4) in for Cook County Courts (C3).
2. **A second strict-lane voice.** Without it June would carry 21 of the 73 rows. A new "courts-2" voice and a Spanish pair need Voice Design on a paid plan; plan limits are unconfirmed (facts sheet, unknowns).
3. **Short feeds and the disclosure.** The shortest script is 11 seconds and the daily script is about 16 (AI Disclosure §3). On a 90-second feed that is about 18% of the runtime. Options: fold micro-feeds into a longer digest, or accept it. The five required items cannot shrink without a policy change.
4. **High school names.** NEVER-2 allows naming a young athlete only in a story about their public work, using the name the school or league publishes. Until counsel confirms, Friday Night Scoreboard (N14) names schools and teams only *(inference)*.
5. **Missing and Exonerated.** Missing excludes minors by default (CR-21). Exonerated and Solved name living people who were once charged or convicted, so they wait for a media-lawyer review (F-LEGAL-02).
6. **Niche economics.** At the cost model's niche inputs (5 minutes, 0.6x the baseline Claude work, one ad slot, 60 downloads; F-LLM-07, F-TTS-17, F-ADS-12) a niche episode costs roughly $1.60 to $2.00 and earns about $0.26, so about $1.30 to $1.80 lost per episode *(inference)*. Niche feeds need a sponsor or services lead, a cheaper voice route (Chirp 3 HD is about $0.03 a minute, F-TTS-23), or they stay small. *As of Oct 2026 — verify before buying.*

## 14. Sources for this page

[`config/shows.yaml`](../../config/shows.yaml), [`config/voices.yaml`](../../config/voices.yaml), [`config/markets.yaml`](../../config/markets.yaml), the Expansion roster in [`agent-catalog.md`](../blueprint/agent-catalog.md), the [facts sheet](../research/facts-and-figures.md), [AI Disclosure](../standards/ai-disclosure.md), [Crime and Courts Rules](../standards/crime-and-courts-rules.md), [Voice & Persona Guide](../standards/voice-and-persona-guide.md), the [advertising plan](../business/advertising-plan.md) and [`finance/build_cost_model.py`](../../finance/build_cost_model.py). No web research.
