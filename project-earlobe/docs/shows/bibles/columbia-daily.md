# Columbia Daily: show bible

**A verified 6-to-8-minute morning brief for the Columbia area, with every claim checked against independent sources before it airs.**

| | |
|---|---|
| **Config** | `columbia-daily` in [`config/shows.yaml`](../../../config/shows.yaml): market `columbia-sc`, wave 0, enabled true |
| **Lane · format** | standard · `daily_brief` |
| **Cadence · length** | Mon-Fri 06:00 ET (cron `0 10 * * 1-5` UTC) · 6-8 min · max 6 stories |
| **Hosts · disclosure** | Mara (anchor) and Theo (co-host) · Script A ([AI Disclosure](../../standards/ai-disclosure.md) §3), about 16 s, spoken by Ava |

## 1. Premise
The day in Columbia in seven minutes: what city and county government did, what police and the courts announced, schools, business and development, the weather, then one sports and one culture item. Richland County is not a news desert (F-AUD-08), so we win on speed, clarity and sourcing, not on filling a void. It is **not** a national show: national events appear only with a real Columbia angle (Localizer).

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| Midlands residents getting ready for the day | The few things that change their day, in order | Podcast apps, smart speakers |
| Government, school and university workers (Columbia is the state capital) *(inference)* | Council, county and campus news with the vote counts | Apps, daily newsletter (`next`) |

## 3. Format and segments
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | Open | Date, "This is Columbia Daily, with Mara and Theo", top line | 0:20 | Mara |
| 2 | Top story | The biggest verified story. At most one Theo question | 1:45 | Mara, Theo |
| 3 | Government, schools, business, development | Council, county, planning, with who voted how | 2:30 | Mara, Theo |
| 4 | Public safety | Short, no levity, legal-word ladder | 1:00 | Mara |
| 5 | Weather | From the structured NWS block. Hosts never improvise a forecast | 0:30 | Mara |
| 6 | Sports and culture | Lighter. Humor allowed here only | 0:45 | Theo |
| 7 | One thing to remember | Repeat one idea, add no new claim (Guide §4) | 0:15 | Mara |
| 8 | **Disclosure** | Script A, always last (DISC-1) | 0:16 | Ava |

## 4. Sources
Feeds are in `config/sources/columbia-sc.yaml`; all 8 are still `verified: false` (F-DATA-04). One owner group counts as one source and wire copy counts as the wire (`config/owners.yaml`).
| Tier | Sources | How we use them |
|---|---|---|
| 1 official | City of Columbia and Richland County releases, NWS alerts for SC, meeting agendas and minutes (Public Meetings Watcher, `next`), SC Judicial Branch Public Index (manual, low rate, F-DATA-10) | Facts, votes, allegations with attribution |
| 2 | The State (McClatchy), The Post and Courier (Evening Post Industries), WIS (Gray Media), WLTX (TEGNA) | Facts in our words plus a link |
| 3 | SC Daily Gazette (States Newsroom, CC BY-NC-ND, recall) | Facts in our words plus a link, never its text (F-DATA-11) |

## 5. Lane and trust rules
- **Standard lane:** 2 independent sources, one official record is enough, balance at least 70, 2 rewrites, then KILL ([Editorial Standards §2](../../standards/editorial-standards.md)).
- **Crime and court items** get the full [Crime and Courts Rules](../../standards/crime-and-courts-rules.md): ladder words (CR-1), every allegation attributed (CR-5), no minors, no uncharged suspects.
- **Time words are true at air time**, Eastern (ACC-10). Numbers carry source, unit and period (NUM-2).
- **Never:** read an article aloud (NEVER-5), air a social post as proof (NEVER-6), say "I was there" or "we spoke to" (NEVER-7), joke near a death, crime or court story.

## 6. Voice, disclosure and ads
Mara opens and closes; Theo asks the listener's question, at most one per story; handoff lines carry no new fact (H-1). In South Carolina the prosecutor is the **solicitor**, never "DA". Starter pronunciations are in [Guide §5](../../standards/voice-and-persona-guide.md); entries marked **?** are unconfirmed. **Ads:** ad-free days 1-30 to set a completion baseline, Slot A from about week 4, Slot B at day 60 if completion holds within 5 points (advertising plan §2, §11). Breaks never sit inside a story (COI-2); a story about a sponsor says so (COI-4).

## 7. Sample cold open (illustrative; braces are placeholders, not real events)
> **Mara:** Good morning, Columbia. It's {weekday}, {month} {day}. This is Columbia Daily, with Mara and Theo.
> **Theo:** Three things before you leave: {top story, attributed}, {second item}, and {weather line}.
> **Mara:** We start with {top story}. {Who did what, said by whom, in under 20 words.}

## 8. Sample episode titles
- Columbia Daily, {weekday} {month} {day}: {council vote}, a {road} closure, rain by afternoon
- Columbia Daily, {weekday}: {school board item} and what the {county} budget changes
- Columbia Daily, {weekday}: {development project} gets a hearing date

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| Downloads per episode, month 6 to 12 | 40 / 120 / 400 (cons / base / opt) | F-AUD-03 *(inference)* |
| Cost per episode | about $2.56 to $3.16 | F-LLM-07 + F-TTS-17, as of Oct 2026 — verify before buying |
| Published by 06:00 ET; inside 6-8 min | every weekday; at least 90% *(inference)* | `shows.yaml`; Showrunner KPIs |
| Completion when Slot B opens; paid placements by day 90 | within 5 points of the ad-free baseline; 2 | Advertising plan §2, §11 |
| Material corrections | 0 per quarter *(inference)* | AUTO-6 |

## 10. Open items
Owner: Showrunner: Daily Briefs (`next`); version 1.0, October 12, 2026. All 8 feeds unverified. Add Columbia Police, Richland County Sheriff, the Fifth Circuit Solicitor and SLED pages once confirmed (markets note §2.3). Confirm the starred pronunciations by listening. The fixed-UTC cron moves to 05:00 local on Nov 1, 2026 until the Scheduler lands.
