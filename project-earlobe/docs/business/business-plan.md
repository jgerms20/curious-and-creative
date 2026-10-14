# Business plan: the Curious & Creative Network (Project Earlobe)

**Curious & Creative LLC** · Joshua German & Janel Moore · draft as of Oct 13, 2026
Numbers come from [`finance/cost-out-and-roi.md`](../../finance/cost-out-and-roi.md) and the [facts sheet](../research/facts-and-figures.md). Prices are as of Oct 2026, so verify before buying. *(inference)* marks our own estimates.

---

## 1. Executive summary

The Curious & Creative Network is an **AI-produced, fully automated audio network** that publishes verified local news, breaking news, courts and true-crime coverage, and archive history, around the clock and with no human in the publishing loop.

- **Always-on agents** watch every market's press releases, newsrooms, public meetings and court dockets.
- **Producer agents** write the episodes.
- **A Trust Stack** of independent checkers verifies every claim before anything airs:
  - a blind source verifier,
  - a fact checker,
  - a bias checker,
  - a legal screener,
  - and a deterministic publish gate.
- **Original AI voices** read each episode, and every episode ends with an honest AI disclosure.

**Why now.** Podcasting is roughly a $9B industry by Freakonomics' framing. Local news keeps shrinking, and AI production costs have collapsed. The most visible attempt at this, Inception Point AI (Quiet Please, now Liquid Studios), proved volume can be made cheaply. It also showed that volume without trust gets filtered by platforms and starves on ads alone. Our bet: **verified, few-but-good, local-first**, with sponsors and services alongside ads ([competitive landscape](competitive-landscape.md), [Jeanine Wright deep dive](../research/jeanine-wright-deep-dive.md)).

**The money in one line.**
- Start: about **$7.3k one-time** plus **$1.4k a month** for the test markets.
- Base case pays back in **month 7**, with about **$9k** of peak cash needed.
- Plan runway for the conservative case: about **$25k**.

## 2. What we sell

Four products. Detail in [products.md](products.md).

| Product | For | Model | Status |
|---|---|---|---|
| **The Network** | Listeners, local sponsors, advertisers | Sponsors + programmatic ads + premium | Engine v1 built and running in dry run |
| **Trust Stack** | Publishers, AI-audio makers, platforms | Verification as a service | Runs inside the network; product later |
| **Earlobe Engine** | Newspapers, universities, companies | White-label automated audio | Later; validate with 2–3 buyers |
| **C&C Studio Services** | Local businesses, creators, nonprofits | Podcast setup, distribution, coaching | Can start now |

## 3. The lineup

Full lineup of 40+ shows with launch waves: [network-lineup.md](../shows/network-lineup.md). Show bibles: [`docs/shows/bibles/`](../shows/bibles/).

| Layer | Launch shows | Cadence |
|---|---|---|
| Local daily briefs | Columbia Daily, LA Daily, then NYC, Chicago and more | Weekdays, 6–8 min |
| Breaking | The Breaking Desk, its own show; spin-offs later | Event-driven, only when verified |
| Courts | LA Courts Roundup, then a court roundup per city | Weekdays |
| True crime | Case Tracker (weekly + development flashes), Cold Case Files | Weekly / 2× week |
| Archives | History of Hollywood, hometown and music history | 3× week |
| Hyper-specific | City council watch, high school sports, openings, pollen and more | Always-on |

## 4. How it works

The blueprint is the core of the plan.

- [Org chart](../blueprint/org-chart.md): **122 agents across 10 desks**: Command, Sensors, Editorial, Trust, Studio, Distribution, Growth, Revenue, Business Ops and Services. [Agent files](../../agents/README.md).
- [How it works](../blueprint/how-it-works.md): the actual loops, from always-on sensing to scheduled shows, breaking flashes and business loops.
- [Trust gate](../blueprint/trust-gate.md): the publish rules, encoding the journalism-school rules (two independent sources, attribution, presumption of innocence, never naming minors or victims).
- [Standards](../standards/README.md): editorial, verification, fact-check, bias, crime and courts, corrections, AI disclosure, voices.

**Moat.** Verification with a public trust log and a corrections record. Platforms and listeners are actively filtering out "AI slop", and being checkable is what keeps us out of that bucket.

## 5. Market

Detail in [market-research.md](../research/market-research.md) and [Freakonomics ep. 690 notes](../research/freakonomics-690-notes.md).

- Podcast ad market growing; programmatic CPMs about $8–$20 (F-ADS-07).
- Local news deserts keep spreading. The local brief has little automated, verified competition.
- 25–45% of new feeds are already AI-made (F-AUD-01). Discovery and trust, not production, are the scarce things.

## 6. Revenue model

Base case, monthly. Full tables and all three cases are in the [ROI report](../../finance/cost-out-and-roi.md).

| | Test | Wave 1 | Scale |
|---|---|---|---|
| Shows / episodes per month | 7 / 125 | 27 / 444 | 157 / 2,278 |
| Total cost | $1,432 | $2,826 | $8,608 |
| Programmatic ads | $275 | $1,058 | $5,493 |
| Local sponsors + community packages | $573 | $3,030 | $17,677 |
| B2B + Trust Stack API | $0 | $2,000 | $14,500 |
| Studio Services | $3,000 | $6,000 | $9,000 |
| **Net per month** | **$2,417** | **$9,437** | **$39,812** |
| Network-only net (no B2B, API, services) | −$583 | $1,437 | $16,312 |

**The honest part.**
- At about 120 downloads an episode, ads alone don't cover a verified local brief. It costs about $3.91 in AI and voice and breaks even near 455 downloads.
- Sponsors and services carry the early months.
- Advertising plan: [advertising-plan.md](advertising-plan.md), covering programmatic, local packages, rate card and brand safety.

## 7. Go-to-market

Detail in [go-to-market.md](go-to-market.md).

- **Stages open by evidence gates, not dates:** Test (Columbia, LA, national) → Wave 1 (+NYC, Chicago, +2) → Scale (25 markets) → Dominate (100).
- **Pace caps keep us out of AI-spam filters.** We never flood feeds, which is the trap that sank Quiet Please's standing.
- **Growth comes from distribution:** Apple, Spotify, YouTube, the website, newsletter, short clips, local partners and cross-promotion between shows.

## 8. Operations and team

- **Founders:** Joshua German (journalism school, strategy, product) and Janel Moore. They own standards, sales relationships, legal decisions and the kill switch.
- **Workforce:** the agents. 23 are built now, 82 are in the next wave, 17 are future.
- **Model tiers:**
  - Haiku tier for triage.
  - Sonnet tier for writing, marketing and operations.
  - Opus tier for scripts and the Trust Stack.
- **First hires come from revenue** *(inference)*: a part-time local sales lead, then a media lawyer on retainer.

## 9. Milestones

The timeline is in [timeline.md](timeline.md).

1. Founder setup: legal review, insurance, accounts and keys.
2. A 2–3 week **dark run**: everything renders privately through the gate.
3. Columbia Daily and LA Daily go public, then Breaking, Courts and the archives over about 10 weeks.
4. Gate A, then Wave 1.
5. First sponsor and first Studio Services client.
6. Meeting with Jeanine Wright: [meeting prep](meeting-jeanine-wright.md).

## 10. Risks

Full list in [risk-register.md](risk-register.md).

| Risk | Mitigation |
|---|---|
| Defamation | Strict lane, official records only, lawyer review, E&O insurance |
| Hallucination | Blind verifier, deterministic gate, 7-day re-check |
| Platform delisting as AI spam | Pace caps, disclosure, quality bar |
| Ads don't fill | Sponsors, services, B2B |
| Voice-vendor dependence | Hybrid engine option |
| Data access to courts | CourtListener/PACER first; ask the court information office |
| Brand risk to the human flagship shows | Separate network label and feeds |

## 11. The ask and next steps

- Commit about **$7.3k** of startup cash, plus **$25k of runway** for the conservative case.
- Complete the [founder to-do](founder-todo.md) "Now" list.
- Run the dark run.
- Go public in the test markets.
- Reach out to Jeanine Wright.
