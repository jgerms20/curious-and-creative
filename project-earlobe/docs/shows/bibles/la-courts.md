# LA Courts Roundup: show bible

**What was filed, ruled and scheduled in Los Angeles courts, in careful language, with every legal word matching the record.**

| | |
|---|---|
| **Config** | `la-courts` in [`config/shows.yaml`](../../../config/shows.yaml): market `los-angeles`, wave 0, enabled true |
| **Lane · format** | strict · `court_roundup` |
| **Cadence · length** | Cron `0 1 * * 2-6` UTC, local 17:00 PT, so Mon-Fri evenings · 8-12 min |
| **Hosts · disclosure** | June (solo) · Script C, crime and courts ([AI Disclosure](../../standards/ai-disclosure.md) §3), about 22 s, spoken by Ava |

## 1. Premise
Most court news is not a celebrity trial. It is a housing suit, a ruling on a city policy, a federal filing, a plea. This show reads the public record each day and reports it plainly: new filings, rulings, pleas and sentencings, then the hearings ahead. It balances the famous case with the civil, housing and government cases that touch more listeners. It is **not** a verdict predictor, a gossip show or a courtroom-audio show.

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| Angelenos affected by civil, housing and government cases | What was filed and decided, and what comes next | Podcast apps, smart speakers |
| People following a notable case; local professionals and press *(inference)* | Status as of today in the right legal words; a sourced read of the day's dockets | Apps, show notes with links |

## 3. Format and segments
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | Open | Date, what is in today's roundup, "charges are accusations" | 0:20 | June |
| 2 | New filings | Civil suits, criminal complaints, DA and U.S. Attorney releases | 2:30 | June |
| 3 | Rulings | Decisions in Superior Court and C.D. Cal. | 2:30 | June |
| 4 | Pleas, verdicts, sentencings | Ladder words, each with an "as of" date | 2:00 | June |
| 5 | The week ahead | Hearings and trial dates from calendars. A calendar is never an outcome | 1:30 | June |
| 6 | Follow-through and close | How earlier cases ended, with the same prominence (FAIR-11); one line to remember | 1:00 | June |
| 7 | **Disclosure** | Script C, always last (DISC-1) | 0:22 | Ava |

## 4. Sources
Court Watch (Haiku tier, built) polls every 30 minutes on court days. Terms often bar bulk automation (F-DATA-10), so Compliance clears each portal first. A missing RECAP entry is not evidence that nothing happened. PACER gets a cap of $150 to $300 a month *(inference)*, RECAP first; *as of Oct 2026 — verify before buying.*
| Tier | Sources | How we use them |
|---|---|---|
| 1 official | LA Superior Court case lookup (summaries free; document-image fee unknown); CourtListener RECAP `cacd` (partial, F-DATA-01); PACER ($0.10 a page, $3 cap, F-DATA-02); LA County District Attorney and U.S. Attorney C.D. Cal. releases | Filings, orders, charges, with attribution |
| 2 | LA Times, LAist, TV outlets (see [LA Daily](la-daily.md)) | Context and corroboration, in our words |
| Never | Mugshot and people-search sites, forums, crowdfunding pages, courtroom audio (COPY-6) | Not sources (NEVER-6) |

## 5. Lane and trust rules
- **Strict lane:** 2 independent sources, an official record for every sensitive claim, no single-source claims, balance at least 75, medium-severity legal issues block ([Editorial Standards §2](../../standards/editorial-standards.md)).
- **Ladder words only** (CR-1); **status as of air time**, with an "as of" date when the record is over 7 days old (CR-2); charges, counts and courts exact (CR-3).
- **Every allegation names who alleges it** (CR-5). Give the defendant's side when on the record; otherwise "We did not find a public response from...", never "we reached out" (CR-7).
- **Never name** minors (NEVER-2), people who say they were sexually assaulted (NEVER-3) or uncharged suspects (FAIR-5). Stop naming anyone whose case is sealed, expunged or diverted, the same day.
- **Follow-through:** dismissals and acquittals get a follow-up within 72 hours; a weekly docket sweep covers everyone named (Crime and Courts Rules §5).
- Fair-report protection in California rests on Civil Code 47(d) (F-LEGAL-10, recall); the defamation clock is one year and records are kept 3 years (F-LEGAL-08). Counsel reviews before launch.

## 6. Voice, disclosure and ads
June is measured, about 140 words a minute, with a pause before a name or legal term; no adjectives about a defendant, no "alleged killer" (FAIR-10). Quiet bed or none; no sting on an accusation or a victim's name. Lexicon includes Foltz and Roybal ([Guide §5](../../standards/voice-and-persona-guide.md)). **Ads:** programmatic off, nothing sold in the first 90 days *(inference)*, then opt-in advertisers only, calm categories, no law firms or bail bonds (advertising plan §8).

## 7. Sample cold open (illustrative; braces are placeholders, not real events)
> **June:** This is LA Courts Roundup for {weekday}, {month} {day}. Today: {n} new filings, {n} rulings, and the week ahead.
> **June:** A reminder: charges are accusations. We begin with a civil suit. {Plaintiff} filed it in {court} on {date}. According to the complaint, {claim, one sentence}. We did not find a public response from {defendant} in the record as of {date}.

## 8. Sample episode titles
- LA Courts Roundup, {weekday} {month} {day}: a new suit over {issue}, a federal ruling, Thursday's hearings
- LA Courts Roundup, {weekday}: prosecutors file charges in {matter}; a judge sets a hearing date
- LA Courts Roundup, {weekday}: {case} sentencing is set for {date}

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| Legal-screen issues per episode; corrections | trending to 0; 0 | Showrunner KPIs; AUTO-6 |
| Civic (non-celebrity) cases in each episode | most of the episode *(inference)* | Showrunner KPI |
| Follow-through within 72 hours; stale-status lines | 100%; 0 | Crime and Courts Rules §5, CR-2 |
| Downloads per episode | 120 at the cost model's test input, unresearched | Facts sheet, Model assumptions |
| Cost per 10-minute episode | about $3.40 to $4.25 *(inference)* | 1.3x F-LLM-07 + F-TTS-17, as of Oct 2026 — verify before buying |

## 10. Open items
Owner: Showrunner: Courts Roundups (`next`); version 1.0, October 12, 2026. Confirm the Superior Court document-image fee and whether media get fee-free access. Add LA City Attorney as a source (it prosecutes misdemeanors *(inference)*). Media-lawyer review before launch (F-LEGAL-02). An insurer may price up or decline automated court coverage (F-LEGAL-01).
