# Market research: size, ads, audience, AI attitudes, local news gaps, and what our layers could earn

**As of 2026-10-12** · Project Earlobe (Curious & Creative Network) · every number cites [facts-and-figures.md](facts-and-figures.md) by ID · companion: [Freakonomics 690 notes](freakonomics-690-notes.md)

**Evidence status (read first).** This page rests on the facts sheet and the research notes behind it. No new searching was possible, and the earlier passes could not open IAB, Edison, Pew, Reuters Institute, Medill or Nielsen pages. Confidence: **high** = several agreeing sources; **med** = one or a secondary source; **low** = recall, a single source, or our own reasoning. Anything below high is a planning number, not a quote. Reasoning we did ourselves is marked *(inference)*. Prices and policies are as of Oct 2026 — verify before buying.

## Seven things to know

1. **The market is real but badly measured.** About $9B globally (F-ADS-01), no sourced US ad-revenue figure (F-ADS-02), and only about 1% of shows said to profit (F-AUD-10).
2. **CPMs are modest.** Typical $17 to $22 (F-ADS-04); programmatic $12 to $15 (F-ADS-05). We plan on $8 / $13 / $20 (F-ADS-07).
3. **Ads alone do not pay for a local brief.** At 120 downloads an episode earns about $1.03 in ads against $2.56 to $3.16 of cost. It takes roughly 300 to 370 downloads at our base case to break even on ads (section 2).
4. **Supply of AI audio is flooding in.** 25% to 45% of new feeds look AI-made (F-AUD-01) and indexes are filtering them (F-HOST-18). Distribution, not production, is the scarce thing.
5. **No independent survey of listener or advertiser attitudes to AI audio was found.** What we have is advocacy, company claims and platform rules (section 4).
6. **In our test markets the news gap is depth, not absence.** Neither LA County nor Richland County is a news desert (F-AUD-08).
7. **Only the Network layer can be sized from sources.** Trust Stack, Engine and Studio Services have price anchors or hypotheses at best (section 6).

## 1. Market size

| Measure | Value | ID | Conf. | Read it as |
|---|---|---|---|---|
| Global podcast "industry" | About $9B | F-ADS-01 | med | Broad; mixes ads with other money. **Not** ad revenue |
| US podcast ad revenue (IAB/PwC) | No sourced figure | F-ADS-02 | n/a | Do not cite. A mid-$2B recollection for 2024 is unverified |
| Patreon payouts to podcasters, 2025 | $629M, +33% | F-ADS-03 | low | From the brief, source not found. Rewards personality-led shows *(inference)* |
| Shows that make money | About 1% | F-AUD-10 | low-med | Widely repeated, never measured |
| New feeds that look AI-made | 25% to 45%; 39% = 4,243 of 10,871 in 9 days | F-AUD-01 | med-high | A supply glut. Listen Notes removed 31.5% of Aug 2026 submissions (F-HOST-18) |
| Biggest AI-only network | 15,000+ shows claimed; about 300 active and none monetized on 2026-09-29; 12M lifetime downloads, about 69 per episode | F-IPA-01, F-IPA-07 | high (300); med | The cautionary tale: thin feeds do not draw audiences. Bot inflation not ruled out |
| Direct listener support | Apple keeps 30% in year one, 15% after; Patreon nets about 80% to 85% | F-HOST-11, F-HOST-12 | low-med | Recall; relevant to a later premium tier |

**Read-out *(inference)*.** The pie is moderate and top-heavy. Our pitch is not a slice of $9B. It is a verified, local, court-aware niche plus three adjacent revenue lines.

## 2. Ad market and CPMs by format and genre

*Almost no ad figure here is measured. Planning cases are inference anchored on two sourced ranges. As of Oct 2026 — verify before buying.*

| Format or genre | Gross CPM | ID | Conf. | Note |
|---|---|---|---|---|
| Typical podcast | $17 to $22 | F-ADS-04 | med | Market-average price per 1,000 ad plays |
| Scarce, hard-to-reach niche | $100+ | F-ADS-04 | med | Needs a rare audience we do not have yet |
| Programmatic (marketplace) | $12 to $15 | F-ADS-05 | med | Rate-table figure, gross |
| Dynamic ad insertion (DAI) | $18 to $22 | F-ADS-05 | med | Gross |
| Host-read vs announcer-read | No sourced figure | n/a | gap | Host-read usually earns a premium *(inference)*. Our voices are synthetic and disclosed, closer to announcer-read, so do not assume it |
| News genre | No sourced CPM | n/a | gap | Mainstream and brand-safety-sensitive *(inference)* |
| True crime | No sourced CPM | n/a | gap | Big audiences, but a common advertiser exclusion *(inference)*. Our Ad Ops tags crime, death, disaster, politics; Breaking Desk coverage of deaths and attacks runs ad-free by default ([how it works](../blueprint/how-it-works.md)) |
| "About $50" claim | Do not plan on it | F-ADS-06 | low | One secondary source |

**How we turn CPM into money.** Net per download = CPM x fill x our share x slots. Slots per brief are 1 / 2 / 2 (F-ADS-11), but F-ADS-12 uses 2 for every case.

| | Conservative | Base | Optimistic | ID |
|---|---|---|---|---|
| Programmatic CPM | $8 | $13 | $20 | F-ADS-07 |
| Fill (share of slots sold) | 30% | 55% | 75% | F-ADS-08 |
| Our share after host/marketplace | 50% | 60% | 70% | F-ADS-09 |
| Net per download, 2 slots | $0.0024 | $0.0086 | $0.021 | F-ADS-12 |
| Downloads per episode, local brief | 40 | 120 | 400 | F-AUD-03 |
| Ads per episode | $0.10 | $1.03 | $8.40 | calc *(inference)* |

**Break-even on ads alone** *(inference; cost = $2.00 of Claude work, F-LLM-07, plus $0.56 to $1.16 of voice, F-TTS-17)*:

| Case | Downloads per episode to cover $2.56 / $3.16 | Our planning audience | Verdict |
|---|---|---|---|
| Conservative | about 1,070 / 1,320 | 40 | Far short |
| Base | about 300 / 370 | 120 | Short by 2.5x to 3x |
| Optimistic | about 120 / 150 | 400 | Covered |

A cheaper voice route (Google Chirp 3 HD, about $0.21 for 7 minutes, F-TTS-23) cuts base break-even to about 260. Cost discipline helps, but audience is the lever.

**Local direct sponsors.** Effective CPM per slot $20 / $35 / $60, with 25% / 50% / 75% of slots sold (F-ADS-10). At 150 downloads that is $16 / $57 / $146 per show-month. A flat community package runs $50 to $150 a month (F-ADS-10). The cost model's $300 / $750 / $1,500 sponsor rates imply CPMs of $92 to $461, which no source supports (F-ADS-14). A $750 sponsor at a $35 CPM needs about 21,400 downloads a month, roughly 990 per daily episode (F-ADS-14).

**Where the market is heading.** Programmatic audio is moving toward curation, identity, video and episode-level brand-fit scoring, with no industry-wide exclusion of synthetic shows (F-ADS-15, med). Spreaker keeps about 40% of programmatic revenue (F-HOST-07, low, older). iHeart owns Spreaker and runs "Guaranteed Human" (F-HOST-17); whether it governs third-party shows is unknown. The old AI-network claim of profit at about 20 listens needs an episode cost under about $0.45 plus the high ad case (F-IPA-04, F-ADS-13).

## 3. Audience and listening data

*As of Oct 2026 — verify before buying. No Edison, Pew or Infinite Dial 2026 listening data was retrieved.*

| Item | Value | ID | Conf. |
|---|---|---|---|
| Downloads per episode, thin AI feeds (benchmark) | About 69 (12M / 175K) | F-AUD-02, F-IPA-07 | med (derived) |
| Local daily brief, steady state (month 6 to 12) | 40 / 120 / 400 | F-AUD-03 | low |
| The Breaking Desk | 150 / 500 / 2,000 | F-AUD-04 | low |
| Cold-case evergreen | 100 / 400 / 1,500 | F-AUD-04 | low |
| Courts, Case Tracker, archive, niche feeds | Not researched | Model assumptions | gap |
| Discovery gating | Castro hides Inception Point shows; Podcast Index flags "low-effort AI"; Listen Notes removed 31.5% of Aug 2026 new submissions | F-HOST-18 | med |
| Spotify "Verified" badges (authentic listenership is a factor) | Live since 2026-05-19 | F-HOST-16 | high |
| Market ranks (Nielsen DMA) | New York #1, Los Angeles #2, Chicago #3; Columbia SC about 71 to 80 | F-AUD-09 | med-high / low |
| Daily-brief leaders (national and local) | No ranking or download count retrieved | n/a | gap |

**Read-out *(inference)*.**
- With a quarter to nearly half of new feeds AI-made and indexes gating them, audience comes from distribution. Launch few feeds, at a human-plausible pace, with honest titles.
- Line up partner distribution early: local outlets, public radio, local radio and smart-speaker flash briefings. Turn on IAB-certified measurement so early counts are not bots.
- Our wave-0 slate is seven live shows (Columbia Daily, LA Daily, The Breaking Desk, LA Courts Roundup, Case Tracker, Cold Case Files, History of Hollywood). NYC and Chicago are configured but off ([shows.yaml](../../config/shows.yaml)).

## 4. Attitudes to AI audio and disclosure

*As of Oct 2026 — verify before buying. Platform rules change; re-check each quarter.*

| Signal | Value | ID | Conf. |
|---|---|---|---|
| Consumer stance | 70% use AI tools, 90% prefer human-made media (iHeart memo: advocacy, not independent) | F-AUD-06 | med |
| Effect of disclosure on listening | Reported as little to no drop-off (company claim, unaudited) | F-AUD-05 | low-med |
| Trust in AI news | About 7% weekly AI-chatbot news use (Reuters Institute 2025); about 45% of AI-assistant news answers had a significant issue (EBU/BBC, Oct 2025) | F-AUD-07 | low-med |
| Apple Podcasts | Prominent AI disclosure in the content and in show/episode metadata; enforcement not evident | F-HOST-15 | med-high |
| Spotify | Verified badges and removal of impersonators; no blanket AI ban; no podcast AI-label rule reported | F-HOST-16 | high (badges) |
| iHeartMedia | "Guaranteed Human": no AI on-air voices on its radio or podcasts | F-HOST-17 | high |
| YouTube and law | YouTube synthetic label since 2024-03-18 and a July 2025 "inauthentic content" rule against mass-produced channels; EU AI Act Art. 50 from 2026-08-02; California SB 942 binds big vendors, not us | F-HOST-13, F-LEGAL-13 | med |
| Advertisers | No direct survey found; Triton sees disclosure, verification and curation, not exclusion | F-ADS-15 | med |

**Read-out *(inference)*.**
- The evidence leans one way: the biggest audio seller markets "human" as premium, trust incidents are common, and platforms are wary of AI feeds. Nothing shows disclosure itself hurts listening, but the only evidence is a company claim.
- We have no clean data on whether a listener or sponsor will choose a disclosed, verified synthetic local brief. That is a test to run, not a fact to assume: two or three real sponsor conversations, and an A/B on disclosure wording once there is traffic.
- Our stance is already set: spoken disclosure at the end of every episode and in metadata ([AI disclosure standard](../standards/ai-disclosure.md), DISC-1 and DISC-4), original personas, no fake humans, public corrections. For a news network these are the product, not a cost.
- Trust failures by others (recalled, low, not for outward use): AI-written false local stories at NewsBreak, fake bylines at Hoodline, accuracy complaints about a major paper's AI podcast, Apple pausing AI news summaries in early 2025 ([competitive note](notes/competitive-landscape.md)).

## 5. Local news gaps and news deserts

*Medill counts are recall; the pages were not opened, and the 2026 report is probably due this fall (inference). As of Oct 2026 — verify before any outward claim. Direction of travel is more reliable than any single count.*

| Measure (Medill State of Local News) | 2023 | 2024 | 2025 | ID | Conf. |
|---|---|---|---|---|---|
| Counties with no local news source | about 204 | about 206 | about 213 | F-AUD-08 | low |
| Counties with one source | about 1,560 | about 1,560 | about 1,520 | F-AUD-08 | low |
| Share of ~3,143 counties with zero or one source | about 56% | about 56% | about 55% | derived from F-AUD-08 | low |
| Newspapers lost since 2005 | n/a | n/a | about 3,500 | F-AUD-08 | low-med |

**What it means for our markets** *(inference unless noted)*.
- Real news deserts are mostly rural counties. **Richland County and LA County are not news deserts** (F-AUD-08). In big metros the opening is a hollowed legacy daily, a thin county layer, and almost no daily local audio.
- **Columbia (Richland County):** mid-size, concentrated ownership, nearest desert counties are rural SC. The gap shows up most clearly here. **Los Angeles:** abundance, so we differentiate on format (6 to 8 minute verified audio), city documents, courts and Hollywood history. Do not lead with LA as proof.
- Pick next markets as large DMAs with weak county coverage, not small towns ([markets note](notes/markets-sources-and-courts.md), section 8). DMA ranks (F-AUD-09) and Medill county data must be checked before the order is locked.

**Who already serves the gap** (recalled, low; do not cite outward):

| Player type | Examples | What they leave open |
|---|---|---|
| Local text and newsletters | Patch (about 30,000 AI-newsletter communities planned, F-IPA-13), Axios Local (30+ metros), Good Daily, 6AM City | They are text, not audio |
| AI local aggregators | NewsBreak, Hoodline | Documented fabrication and fake bylines |
| Local TV groups | Nexstar-Tegna ($6.2B, Aug 2025, status unverified, F-IPA-13) | Video-first; no verified audio brief |
| Public radio | CPB funding of about $1.1B rescinded July 2025 (F-IPA-13) | Shrinking capacity; few daily municipal briefs; possible partners |
| Big-tech AI audio | Google Daily Listen, NotebookLM (not a production engine, F-TTS-32), ElevenLabs GenFM | National, unsourced, no local data or courts |
| Court and true crime | Law&Crime, Court TV, Courthouse News; no AI-native player found | Routine local dockets are thinly covered |

**Whitespace *(inference, low-med)*:** audio-first, city-level, document-grounded news with visible per-episode sourcing, a public corrections log, honest AI labels and courts as a beat. We found no one combining these, but we could not search, so say "built to be checked", never "first" or "only".

## 6. Opportunity sizing for our four layers

*As of Oct 2026 — verify before buying. Only layer 1 has sourced ingredients; layers 2 to 4 are price anchors and hypotheses.*

**Layer 1, The Network (owned shows, ads and sponsors).** One weekday daily brief, 21.7 episodes a month:

| Per show-month *(inference)* | Conservative | Base | Optimistic |
|---|---|---|---|
| Downloads (40 / 120 / 400 per episode) | 868 | 2,604 | 8,680 |
| Programmatic ads (F-ADS-12) | $2 | $22 | $182 |
| One local sponsor, scaled from F-ADS-10 | $4 | $46 | $389 |
| Cost to make 21.7 briefs ($2.56 to $3.16 each) | $56 to $69 | $56 to $69 | $56 to $69 |

- A sponsor takes a slot programmatic would have filled, so do not simply add the rows. Base case with one sponsor replacing one of two programmatic slots: about $11 + $46 = $57, roughly equal to cost.
- Seven wave-0 shows at base audiences are a learning stage, not a revenue stage. Growth must come from audience per show, more markets, sponsors and syndication, not feed count: flooding drew the filters (F-IPA-10, F-AUD-01).

**Layer 2, Trust Stack (verification as a product).** *Not sizeable from our sources.*
- Cost to serve: the verifier alone is about $1.04 of the $2.00 brief (F-LLM-07). Inception Point spent $0.01 to $0.05 on LLM passes for a 3-minute episode; ours costs 5x to 20x more by design (F-LLM-08).
- Demand signals: AI-assistant news errors near 45% (F-AUD-07), curation and brand-fit scoring (F-ADS-15), the "human premium" (F-HOST-17). Possible buyers: publishers, ad buyers, platforms, other AI-audio makers *(inference)*.
- First proof is our own published verification numbers. No price anchor exists.

**Layer 3, Earlobe Engine (our workflow as a product).**
- Only price anchors: Liquid Studios lists $10 per finished video minute (about $600 an hour) and about $1 per audio episode, with no named customers (F-IPA-09).
- The cost model's B2B rate of $1,000 to $3,500 a client a month sits at the video anchor, 46x to 161x the audio anchor (Model assumptions). Validate with 2 or 3 buyers before it enters any base case.
- NotebookLM and similar tools are not production engines (F-TTS-32), which leaves room for a managed, verified pipeline *(inference)*.

**Layer 4, C&C Studio Services (in-person podcast setup and distribution).**
- Demand data: none. Rate hypothesis $1,500 to $5,000 a project (Model assumptions, unsupported). Pass-through costs are small: hosting about $19 to $99 a month (F-HOST-02, F-HOST-03, low), Apple Podcasters Program $19.99 a year only if selling subscriptions (F-LEGAL-07).
- It is the fastest route to cash and the first cash line in the agent plan, but it is capped by founder hours on site *(inference)*. One $1,500 project covers about three months of the $500-a-month media-insurance placeholder (F-LEGAL-01).

| Layer | Sized from sources? | Best number we have | Next proof |
|---|---|---|---|
| 1 Network | Partly | $2 / $22 / $182 programmatic per daily show-month | Real downloads and fill from the first 90 days |
| 2 Trust Stack | No | $1.04 verifier cost per brief | Public scorecard; one outside buyer conversation |
| 3 Engine | No | $10 per video minute; about $1 per audio episode (competitor list) | 2 or 3 priced pilot conversations |
| 4 Studio Services | No | $1,500 to $5,000 a project (hypothesis) | First paid client |

## 7. Biggest gaps to close next

Resolve with a research pass that has search enabled, then write the verified value into the facts sheet and bump its as-of date.

1. IAB/PwC US podcast ad revenue, forecast and format split (F-ADS-02); CPM by genre and host-read vs announcer-read; real fill and sell-through (F-ADS-07, F-ADS-08).
2. Local podcast advertising: market size, rates, how radio and TV groups sell it; advertiser and agency surveys on AI audio.
3. Edison, Pew and Reuters Institute 2026 data on AI attitudes and news-podcast reach (F-AUD-06, F-AUD-07).
4. Medill 2025 and 2026 counts with Richland and LA county profiles (F-AUD-08); Nielsen DMA ranks for candidate markets (F-AUD-09).
5. Daily-brief rankings and download benchmarks for local audio.

*Sources: [facts sheet](facts-and-figures.md); notes [ad market and audience](notes/ad-market-and-audience.md), [competitive landscape](notes/competitive-landscape.md), [markets and courts](notes/markets-sources-and-courts.md), [Liquid Studios pivot](notes/liquid-studios-pivot-and-press.md), [hosting and monetization](notes/hosting-and-monetization-platforms.md); [shows.yaml](../../config/shows.yaml); [agent roster](../../agents/README.md).*
