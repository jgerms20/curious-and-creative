# Go-to-market: from two test markets to a network that leads

**The Curious & Creative Network · as of 2026-10-12 · DRAFT for Joshua and Janel.** Built from the [facts sheet](../research/facts-and-figures.md) (IDs like `F-ADS-05`), the [market research](../research/market-research.md), the [competitive landscape](competitive-landscape.md), [legal and compliance](legal-and-compliance.md), [`shows.yaml`](../../config/shows.yaml), the [agent roster](../../agents/README.md) and the [cost model](../../finance/cost-out-and-roi.md). Companion: the [risk register](risk-register.md). Our own reasoning is marked *(inference)*. *Prices and platform rules: as of Oct 2026 — verify before buying.*

## The 30-second version

| | |
|---|---|
| **Plan** | Four stages, each opened by a gate and not by a date: **Test** (Columbia, LA, national) → **Wave 1** (NYC, Chicago, +2) → **Scale** (25 markets) → **Dominate** (100 markets). |
| **Core rule** | Earn each stage with evidence. Few feeds, honest titles, human-plausible pace. Inception Point launched 200+ shows a day and ended with about 300 unmonetized ones, after Castro hid it (F-IPA-01, -02, -10). |
| **What grows us** | Distribution and trust, not production. 25% to 45% of new feeds are already AI-made (F-AUD-01) and thin AI feeds average about 69 downloads an episode (F-IPA-07). |
| **What pays** | Not ads alone: a local brief loses about $1.5 to $2.1 an episode on ads at base case (facts sheet, "five things"). Local sponsors, Studio Services and B2B carry the early months. |
| **Biggest tension** | The cost model's calendar (Scale by month 7) is faster than the pace caps below allow. Treat the model as a cost scenario, not a schedule (section 1). |

## 1. The stage ladder

Shows, monthly cost and cost per episode come from the cost model; pace caps are our setting *(inference)*.

| Stage | Markets | Shows | Cost / month | Cost / episode | Opens when | Pace cap |
|---|---|---|---|---|---|---|
| **Test** | Columbia, LA, national | 7 | $1,432 | $11.44 | Legal P0 done: lawyer review, E&O bound | All 7 listed over about 10 weeks, never in one day |
| **Wave 1** | + NYC, Chicago, Charleston, Greenville (default pick) | 27 | $2,826 | $6.36 | Gate A | 1 new market a month; 3 new public feeds a week, network-wide |
| **Scale** | 25 markets | 157 | $8,608 | $3.78 | Gate B | 2 new markets a month; 5 new feeds a week |
| **Dominate** | 100 markets | 693 | $27,723 | $2.86 | Gate C | 4 new markets a month; 10 new feeds a week |

- **Timeline by the caps:** Test about 3 months, Wave 1 about 4 more, Scale (19 more markets) about 10 more, so 25 markets near **month 17** and 100 markets near **month 36** *(inference)*. The model's default path is Test months 1 to 3, Wave 1 months 4 to 6, Scale months 7 to 12. Faster is allowed only after two clean quarters and a founders' yes.
- **Wave 1 picks.** NYC and Chicago are configured but off (`enabled: false`). Charleston and Greenville reuse Columbia's state courts, statehouse and owner map ([markets note](../research/notes/markets-sources-and-courts.md) section 8). The order is not locked until DMA ranks and Medill county data are sourced (F-AUD-08, -09).
- **Scale list (proposal):** Charlotte, Atlanta, Houston, then DC, Philadelphia, Dallas-Fort Worth, Phoenix, Miami, Tampa, Orlando, then Detroit, Denver, Baltimore, Pittsburgh, Sacramento, Bay Area, Nashville, Raleigh-Durham. **Dominate:** markets 26 to 100 are not researched yet (gap).

### Gates between stages

Every line must hold for **8 straight weeks**. Targets are the conservative or base cases in the facts sheet unless marked *(inference)*.

| Gate | Trust and platforms | Audience | Money and readiness |
|---|---|---|---|
| **A: Test → Wave 1** | 0 uncorrected errors on a named person; 2 monthly transparency reports out; 0 hides, flags or delistings | Each daily 40+ downloads an episode and rising 4 weeks running (F-AUD-03); Breaking Desk 150+ (F-AUD-04) | 1 paid sponsor or Studio Services client; real fill and eRPM measured on 2 or 3 shows; cost per episode within 1.5x of $11.44; NY and IL legal review done |
| **B: Wave 1 → Scale** | Gate A holds in all 6 markets; 0 platform actions | Local median 80+ *(inference)*; Breaking Desk 300+ *(inference)* | Sponsors in 4+ markets, sell-through 25%+ (F-ADS-10); second host live or contracted; voice quote or hybrid test passed (F-TTS-37); Quota Sentinel, Catalog Steward and Directory Sync Checker built; bigger daily-cap envelope approved |
| **C: Scale → Dominate** | 0 platform actions for 6 months | Local median 120+ (F-AUD-03 base) | Network-only net above zero without B2B, API or services; audited measurement; enterprise ad stack or direct sales; B2B demand proven by paying pilots |

## 2. Test markets: the order we go public

Config says `enabled: true` for seven shows. **Enabled is not listed.** Directory submission is the launch, and it is staged. The 10-episode dry run and the weeks below are our setting *(inference)*.

| When | What goes public | Why then |
|---|---|---|
| **Dark run, 2 to 3 weeks** | Nothing. All 7 shows render privately through the full gate | Calibrate cost, hold and kill rates; fix pronunciation; test the kill switch |
| **T+0** | Columbia Daily, History of Hollywood | Lowest legal risk (standard and archive lanes); Columbia is where the depth gap is clearest (F-AUD-08) |
| **T+3 weeks** | LA Daily | Crowded market: differentiate on format and verification, never lead with LA as proof |
| **T+5 weeks** | The Breaking Desk | Needs 30 days of clean trust-log data because it names people (legal P0, item 3) |
| **T+8 weeks** | LA Courts Roundup, Case Tracker (weekly only) | Strict lanes; flashes wait for the Case Development Watcher (`next`) |
| **T+10 weeks** | Cold Case Files | Name clearance and a fresh legal pass; victims' families (section 3) |

## 3. Launch checklist

Most launch helpers are `next` (Show Launcher, Catalog Steward, Market Launch Marketer, Directory Sync Checker, Clip Maker, Website Publisher). Until they ship, Joshua, Janel or a build task does each step by hand.

**Gates for every show (all must be done before the feed is submitted):**

| # | Gate | Detail |
|---|---|---|
| G1 | Legal P0 | Media-lawyer review ($2,500 to $7,500, F-LEGAL-02); E&O bound with no AI exclusion (about $6,000 a year, F-LEGAL-01) |
| G2 | Names cleared | Show, persona and network names searched (USPTO, app stores, directories); file Class 41 at $350 (F-LEGAL-03) |
| G3 | Day-one pages | Terms, Privacy, Corrections and Ethics, "How this show is made", legal contact |
| G4 | Disclosure | Spoken AI outro at the end of every episode, and the same words in show and episode metadata (F-HOST-15) |
| G5 | Host and feed | Written AI-content position from the host before paying; feed URL on a domain we own; one feed per show |
| G6 | Sources | Market source file loaded; guessed feeds fixed by autodiscovery (all 43 are `verified: false`, F-DATA-04); court ids correct (`scd`, not `dsc`) |
| G7 | Dry run | 10 episodes through the gate with PUBLISH, QA Listener pass, local-name pronunciation list, trust log written |
| G8 | Safety wiring | Kill switch tested ([`killswitch.yaml`](../../config/killswitch.yaml)); daily cap set ([`budgets.yaml`](../../config/budgets.yaml)); Quota check |
| G9 | Brand | Cover art, sonic logo, licensed music with a log (F-LEGAL-06), original personas registered |
| G10 | Measurement | IAB-certified measurement on from day one so early counts are not bots; baseline dashboard |
| G11 | Launch kit | Trailer, 30-day launch plan, partner list, newsletter signup, first 5 clips |

**Extra gates by show:**

| Show (lane) | Extra before listing |
|---|---|
| Columbia Daily (standard) | Check whether an old Inception Point SC feed is still listed; SC Daily Gazette is CC BY-NC-ND, so facts in our words plus a link (F-DATA-11); clear the name echo |
| LA Daily (standard) | Sources for transit, housing, entertainment business; name clearance against existing papers |
| The Breaking Desk (breaking) | Replay 20 past events through the Breaking Detector *(inference)*; 3 independent sources; no names or deaths before an official release; ad-free by default on deaths and attacks |
| LA Courts Roundup (strict) | Fair-report drafting rules on; sealed and juvenile items dropped; identity matching; LA court terms and fees checked; CourtListener first, PACER capped (F-DATA-02) |
| Case Tracker (strict) | Start with high-profile public cases only *(inference)*; presumption-of-innocence wording; weekly only until flashes ship |
| Cold Case Files (strict) | Rename or clear (A&E title); no uncharged suspects; Doe Network and Charley Project are leads only (F-DATA-09); a re-run restarts the defamation clock (F-LEGAL-08) |
| History of Hollywood (archive) | Public-domain line (works through 1930, F-LEGAL-17); no invented dialogue; no replica of a dead star's voice |

## 4. Distribution

Host: Transistor first, Captivate as the alternate (hosting note; prices are recall) *(inference)*. Add a second host at 50+ shows and keep any one host under 60% to 70% of feeds. Get each platform's AI position in writing.

| Channel | How | Rule or catch | When |
|---|---|---|---|
| **Apple Podcasts** | RSS via Apple Podcasts Connect (account exists under the LLC) | Prominent AI disclosure in content and metadata (F-HOST-15); Podcasters Program $19.99 a year only if we sell subscriptions (F-LEGAL-07) | Launch day |
| **Spotify** | Spotify for Creators (exists) | No blanket AI ban; impersonators removed, verified badges (F-HOST-16); Partner Program is video-only, so Breaking Desk upside at most (F-HOST-14) | Launch day |
| **YouTube** | A few consolidated channels with playlists; Breaking Desk as a human-reviewed video show | July 2025 "inauthentic content" rule hits templated channels (F-HOST-13); synthetic label on (F-LEGAL-13); ads need 1,000 subs and 4,000 watch hours | After week 4 |
| **Amazon Music / Audible** | Host's directory submission or RSS | Not researched: get Amazon's AI-content rules in writing (gap); Art19 is quote-only and curated (F-HOST-09) | After Apple and Spotify are stable |
| **iHeartRadio / Spreaker** | Hold | "Guaranteed Human" (F-HOST-17); whether it covers third-party feeds is unknown. Ask before listing or hosting | Only after a written answer |
| **Index apps** (Castro, Podcast Index, Listen Notes) | Pick up the RSS | Castro hid Inception Point; Listen Notes removed 31.5% of Aug 2026 submissions as AI (F-HOST-18). Catalog Steward checks the flag lists weekly | Automatic |
| **Website + RSS** | A page per show and episode: sources, transcript, chapters, corrections, trust report (Website Publisher) | Owning the feed URL lets us change hosts without losing subscribers | Before launch |
| **Newsletter** | Daily local email paired with each brief; weekly network digest | CAN-SPAM opt-out within 10 business days (F-LEGAL-14); consent via Privacy Steward | Launch week |
| **Social clips** | 30 to 60 second audiograms and vertical video (Clip Maker, Social Media Manager) | Label AI where platforms ask; promote gated content only; no fake or bought reviews (F-LEGAL-14) | Week 1 |
| **Radio, smart speakers** | Syndication Packager (`future`) | After Scale | Later |

## 5. Growth loops

| Loop | How it turns | Metric | Guard |
|---|---|---|---|
| **Trust** | Public scorecard, corrections and the monthly transparency report → press, partners, sponsors → listeners | Press mentions, partner inquiries | Publish bad months too |
| **Search** | Transcripts and source pages → search traffic → subscribers | Search-to-follow rate | No keyword stuffing; Castro punished it |
| **Clips** | Clip → social → episode | Clip-to-follow conversion | Label AI; never exaggerate the episode |
| **Newsletter** | Daily email → habit → episode listens and sponsor inventory | Newsletter-to-podcast follows | Unsubscribe in one click |
| **House promo** | Trailers and "if you liked this" pointers on our own feeds (Cross-Promo Planner) | Follows attributed to promo | Match by audience overlap; cap frequency |
| **Breaking → local** | A Breaking Desk flash points to the local daily when there is a real local angle (Localizer) | Cross-feed follows | Only real local angles |
| **Partner** | Partner shares us, we credit and link them | Listeners attributed to partners | No endorsement claims |
| **Sponsor** | Campaign report → renewal → referral to the next local business | Renewal rate | Sponsors never see scripts |
| **Return** | Follow-Up Editor brings a story back when its date arrives; Case Tracker flashes | Repeat listeners | Only when something changed |
| **Tips** | Listener tips and corrections → better coverage → trust | Tips accepted | A tip is a lead, never proof |

## 6. Partnerships

Anything that commits money or signs a contract goes to Joshua or Janel (Partnerships Scout rule). Targets are found per market by the Partnerships Scout; we name no organization here.

| Partner type | We offer | We ask | Watch out |
|---|---|---|---|
| **Public libraries** | Local-history and hometown archive stories; a listening-station item | Newsletter and branch promotion | No implied endorsement |
| **Colleges** (journalism and communications programs, student media) | A live verification case study; talks on "how this show is made" | Student-media cross-promo; outside review of our corrections log | Some will object to AI: say it plainly, never claim "first" |
| **Public and community radio** | A 2 to 3 minute flash briefing cut with on-air credit | Airtime or a credit line | iHeart's "Guaranteed Human" (F-HOST-17); some stations will refuse AI voices |
| **Local newsrooms** | Audio versions of their stories with credit and link | Link-backs; text licenses (P2 legal item) | Never summarize without credit; check licenses (F-DATA-11) |
| **Chambers, civic groups** | Community sponsor packages at $50 to $150 a month (F-ADS-10); event listings | Introductions to member businesses | Ads are marked and never buy coverage (promise 9) |
| **Platforms and hosts** | A transparency report | Written AI-content position; Spotify Verified path | Keep every answer on file |

## 7. Avoiding the AI-spam trap

Inception Point went from 15,000+ claimed shows to about 300 unmonetized (F-IPA-01, -08). Castro hid it, the Podcast Index flagged it (F-IPA-10), and the average episode drew about 69 downloads (F-IPA-07). We copy none of that.

| Guardrail | Rule | Enforced by |
|---|---|---|
| **One feed per market** | A new market launches with its daily only. A courts or hometown-history feed follows after day 60, if the daily is above its floor | Show Launcher, Catalog Steward |
| **Pace caps** | Section 1. Any platform flag freezes all new launches until cleared | Programming Director |
| **Honest titles** | Titles describe the show. No near-duplicate shows, no title variants, no search-term stuffing | Catalog Steward |
| **News or nothing** | Skip the day rather than pad (promise 7); `max_stories` is 6 for Columbia, 7 for LA | Assignment Editor, gate |
| **Audience floor** | A feed under its floor for 30 days is paused or merged. Starting floor is the conservative case: local 40, Breaking Desk 150, cold case 100 *(inference)* | Catalog Steward, Programming Director |
| **Quality bars** | G7 dry run; gate PUBLISH; QA Listener pass; unique art; disclosure in audio and metadata | Standards Editor, Disclosure Agent |
| **No tragedy chasing** | Breaking: 3 sources, no names or deaths before an official release | Breaking Detector, gate |
| **Original personas** | No invented backstories or expert titles | Brand Guardian, Voice Director |
| **Lead with proof** | Scorecard, not scale; never say "first" or "only" | Press & PR Agent |

## 8. KPIs by stage

Cost and net rows are cost-model outputs, not promises *(inference)*. Targets without an ID are our setting.

| KPI | Test | Wave 1 | Scale | Dominate |
|---|---|---|---|---|
| Markets / shows | 2 + national / 7 | 6 / 27 | 25 / 157 | 100 / 693 |
| Feeds hidden, flagged or delisted | 0 | 0 | 0 | 0 |
| Episodes with spoken and metadata AI disclosure | 100% | 100% | 100% | 100% |
| Named-person errors reaching air | 0 | 0 | 0 | 0 |
| Local daily downloads per episode (median) | 40+ (F-AUD-03) | 80+ | 120+ | 120+, capped at 400 |
| Breaking Desk downloads per episode | 150+ (F-AUD-04) | 300+ | 500+ | 500+ |
| Local partners signed per new market | 1+ | 1+ | 1+ | 1+ |
| Sponsor sell-through | first paid sponsor | 25%+ in 4 markets | 50% (F-ADS-10 base) | 50% to 75% |
| Programmatic fill, measured | measure on 2 or 3 shows | 30%+ (F-ADS-08) | 55% base | not load-bearing |
| Cost per episode (all-in) | $11.44 | $6.36 | $3.78 | $2.86 |
| Network-only monthly net, base | -$583 | +$1,437 | +$16,312 | +$95,594 |
| Days over the daily cap | 0 | 0 | 0 | 0 |
| Revenue lines proven | 1 Studio Services client | 1 B2B pilot priced | 5 B2B, 3 API (model volumes) | 20 B2B, 15 API (model volumes) |

## 9. Decisions for the founders, and gaps

| Decision | Suggested default |
|---|---|
| Accept the slower pace caps over the model's calendar | Yes; revisit after two clean quarters |
| Wave 1 market pick | NYC, Chicago, Charleston, Greenville, after DMA and Medill data are sourced |
| Human sign-off on court, crime and Breaking Desk naming until 30 clean days | Yes (legal P0, item 3); it is an extra input, never a gate override |
| Name an accountable editor of record | Yes, before T+0 |
| Bigger daily-cap envelope at Scale (Wave 1 caps already sum to $59 of $60) | Decide at Gate B |

**Gaps to research:** Amazon's and Apple's current AI enforcement; markets 26 to 100; DMA ranks and household counts; real fill and eRPM; sponsor demand for disclosed AI audio; local radio and college interest; a newsletter benchmark; an IAB-certified measurement vendor.

*Sources: the facts sheet and its notes; [`shows.yaml`](../../config/shows.yaml); [`markets.yaml`](../../config/markets.yaml); [`budgets.yaml`](../../config/budgets.yaml); [agent roster](../../agents/README.md); [org chart](../blueprint/org-chart.md); [standards](../standards/README.md).*
