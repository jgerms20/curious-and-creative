# Case Tracker: show bible

**A weekly status report on the major criminal cases we follow, from charge to outcome, plus short flashes when a case moves.**

| | |
|---|---|
| **Config** | `case-tracker` in [`config/shows.yaml`](../../../config/shows.yaml): market `national`, wave 0, enabled true |
| **Lane · format** | strict · `case_weekly` |
| **Cadence · length** | Fri 10:00 ET (cron `0 14 * * 5` UTC) plus a flash on `case.development` · 15-25 min weekly; flashes 2-4 min *(inference)* |
| **Hosts · disclosure** | June (status) and Theo (the listener's question) · Script C ([AI Disclosure](../../standards/ai-disclosure.md) §3), about 22 s, spoken by Ava |

## 1. Premise
Cases take months. Most coverage shows up at the arrest and the verdict and misses the middle. Case Tracker keeps one sourced file per case and tells you, each Friday, where it stands as of a date, what happened this week, what is on the docket next and what nobody knows yet. It follows cases to the end, and a dismissal or an acquittal gets the same prominence the arrest did (FAIR-11). It is **not** a theory show, a "who did it" show or a commentary show.

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| People following a national case; LA Courts Roundup listeners when a local case goes national | Status, not speculation | Podcast apps, smart speakers |
| Families, advocates, press *(inference)* | A record exact about the legal word and the date | Show notes with dated docket links |

## 3. Format and segments
Weekly: 3 to 5 cases at about 3 to 4 minutes each *(inference)*. Every case segment restates its current legal status.
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | Open | Date, the cases in this episode, "charges are accusations" | 0:30 | June |
| 2 | Case segment (repeat) | Status as of {date}, this week, what is next on the docket, what is not known | 3:30 each | June; Theo asks "what happens next", June answers only from the docket |
| 3 | Closed this week | Outcomes, with the same weight as the original charge | 2:00 | June |
| 4 | Dates to watch and close | Scheduled hearings and trials, never outcomes; one sentence to remember | 1:50 | June |
| 5 | **Disclosure** | Script C, always last (DISC-1) | 0:22 | Ava |
**Flash:** status now, what changed, the docket entry and its date, what is next. It works from the same case file as the weekly, so the two never disagree.

## 4. Sources
Case Development Watcher (Haiku tier, `next`) polls every 30 minutes; the Case File Keeper (Opus tier, `next`) holds one file per case. *As of Oct 2026 — verify before buying.*
| Tier | Sources | How we use them |
|---|---|---|
| 1 official | CourtListener RECAP (partial, F-DATA-01), PACER ($0.10 a page, $3 cap, F-DATA-02), DOJ and U.S. Attorney releases, state AG and DA or solicitor releases, state court portals (manual, low rate, F-DATA-10) | Charges, orders, dates. Every status line names its record and date. RECAP gaps are not proof, so pair with PACER |
| 2 | Established newsrooms | Corroboration, facts in our words plus a link |
| Never | Social posts, mugshot and people-search sites, forums, "justice for" pages, crowdfunding pages | Not sources (NEVER-6) |

## 5. Lane and trust rules
- **Strict lane:** 2 independent sources, an official record for every sensitive claim, no single-source claims, balance at least 75, medium-severity legal issues block ([Editorial Standards §2](../../standards/editorial-standards.md)).
- **A person enters a tracked case only after an official charging record**, or an agency naming them on the record (FAIR-5). Match defendants on case number, court and a second identifier, never a name alone *(inference; research note §2.3)*.
- **Ladder words, status as of air time, exact counts and courts** (CR-1 to CR-3). Allegations name the accuser (CR-5); the defendant's side is included when on the record (CR-7).
- **Victims are people** (FAIR-10, CR-11 to CR-14): no graphic detail beyond need, no invented family words, no cliffhangers over a death; named only after an official release and next-of-kin notice (CR-12).
- **Never:** name minors (NEVER-2) or sexual-assault survivors (NEVER-3), show a mugshot, use verdict words in a title (CR-15).
- A weekly docket sweep covers every named person; a credible takedown request suppresses the content within 24 hours (Crime and Courts Rules §5, §7).

## 6. Voice, disclosure and ads
June about 140 words a minute, no dramatic pauses on accusations. Theo asks at most one question per case, never states a fact inside it and never wonders aloud (NEVER-1, Guide H-2). Quiet bed or none. **Ads:** opt-in advertisers only, nothing sold in the first 90 days, memberships later *(inference)* (advertising plan §8, [products](../../business/products.md)); flashes ad-free *(inference)*.

## 7. Sample cold open (illustrative; braces are placeholders, not real events)
> **June:** This is Case Tracker for the week of {date}. We cover {n} cases. Charges are accusations; anyone named is presumed innocent unless a court has ruled otherwise.
> **Theo:** First up?
> **June:** {Case short name}. As of {date}, {defendant} is charged with {charge, exact}, according to {court record}. This week, {docket event}.

## 8. Sample episode titles
- Case Tracker, week of {date}: a trial date is set, a plea hearing moves, one case ends
- Case Tracker, week of {date}: charges dismissed in {case}; where the other {n} stand
- Case Tracker flash: {court} schedules sentencing in {case}; docket as of {date}

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| Weekly completion rate; harm and legal gate issues | tracked; trending to 0 | Showrunner KPIs |
| Minutes from development to published flash | set after the first 20 flashes; no sourced number | Showrunner KPI *(inference)* |
| Follow-through within 72 hours of an outcome | 100% | Crime and Courts Rules §5 |
| Downloads per episode | 300 at the cost model's input, unresearched | `finance/build_cost_model.py` |
| Cost per 20-minute weekly | about $5.20 to $6.90 *(inference)* | 1.8x F-LLM-07 + F-TTS-17 |

## 10. Open items
Owner: Showrunner: Case Tracker (`next`); version 1.0, October 12, 2026. Founders approve the case-selection rule and the first tracked list. Counsel reviews before go-live (Crime and Courts Rules §2). The outcome follow-through monitor is not built (NE-14). Insurance may exclude automated crime coverage (F-LEGAL-01).
