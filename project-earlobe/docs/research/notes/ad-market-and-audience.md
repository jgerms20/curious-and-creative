# Podcast ad market and audience data (2025-2026): research notes

*Prepared 2026-10-11 for Project Earlobe. **Status: PARTIAL.** Read the "Research status" box first.*

## TL;DR

This pass could not collect new web evidence. The web-search budget for the turn was already spent when this task started, and every direct fetch of a primary source (IAB, Reuters Institute, Edison, Pew, Triton, Podder) failed at the network level. So this file holds only four kinds of material, each labeled: (1) figures carried over from the earlier Earlobe notes, which had real sources; (2) two figures supplied in the research brief itself (Patreon $629M, "$9B" industry); (3) clearly marked *(inference)* planning assumptions; and (4) a short list of unverified recollections that must **not** be cited until checked. The sourced evidence we do have points one way: typical podcast CPMs are in the high teens to low twenties, programmatic is lower ($12-15), and nobody, including the best-known AI podcast network, has published fill rates or revenue. The recommended planning numbers below (programmatic CPM $8 / $13 / $20, fill 30% / 55% / 75%, local daily-brief downloads per episode 40 / 120 / 400) are *(inference)* anchored on those sourced ranges. The most useful finding is a model cross-check: the cost model's local-sponsor rates imply effective CPMs of $90-$460 at Test-stage audiences, which no evidence supports. The sponsor rate should be tied to downloads.

## Research status (read first)

| Item | What happened |
|---|---|
| Web search | 0 of 6 planned first-wave searches ran. The tool returned "budget used up" (200-call per-turn limit shared by all agents). I did not work around it. |
| Direct fetches | Tried once each, all failed with a DNS error (ENOTFOUND): podderapp.com, tritondigital.com, reutersinstitute.politics.ox.ac.uk, iab.com, edisonresearch.com, pewresearch.org. Not retried. |
| What this file therefore contains | Carry-over from `inception-point-business-model.md` and `liquid-studios-pivot-and-press.md` (those had live sources), brief-supplied figures, inference, and an unverified-recall list. |
| What is NOT here | New 2026 data for: IAB/PwC US podcast ad revenue and forecast; ad-format shares; genre CPMs for news and true crime; local podcast advertising; fill/sell-through; network rev-share norms; advertiser brand-safety surveys; Edison/Pew/Reuters Institute listener attitudes to AI; news-podcast listening; daily-brief rankings; the Patreon figure's source. |
| To finish | A follow-up message after this one can re-run the search list in "Open questions / gaps". The searches are written out there, ready to send. |

Convention check: numbers here are meant to feed `docs/research/facts-and-figures.md` (which does not exist yet). Only rows marked **sourced** below should be copied there. Rows marked *(inference)* are assumptions. Rows marked **unverified** need a source first.

---

## 1. Market size

### 1.1 Global industry, "about $9 billion"

- Freakonomics Radio Ep. 690 ("It's Show Business, Baby!", 2026-10-09) frames podcasting as roughly a **$9B global industry** and asks whether that is a lot. The earlier Earlobe note summarized the episode from page and transcript fragments, not a full read. *(sourced via prior note; medium)*
- **Context (inference):** $9B is a broad, loosely defined "industry" figure. The episode's economist guest says the industry lacks shared tracking, so firm numbers are scarce. The figure probably blends advertising with other revenue (subscriptions, licensing, deals) and is not comparable to the narrower IAB "advertising revenue" series. Do not use it as an ad-revenue number.
- The same episode repeats a claim that only about 1% of shows are profitable. It is secondhand and unquantified. *(reported; low)*

### 1.2 US podcast advertising (IAB/PwC)

- **Not verified this session.** No IAB or PwC number for 2025 actuals or the 2026 forecast was retrieved.
- Unverified recollection only (see section 9): the IAB study published in 2025 put 2024 US podcast ad revenue around the mid-$2 billions, with a forecast of continued high-single-digit to low-double-digit growth. This is from memory, not a source.

### 1.3 Creator-side money: Patreon

- The research brief says Patreon paid podcasters **$629M in 2025, up 33%**, per Variety. **Not independently confirmed this session**; no URL was available. Treat as brief-supplied, confidence low until the Variety article is found.
- **Why it matters (inference):** if accurate, direct listener support is a large and fast-growing slice compared with the ~$2-3B US ad market. It supports the cost model's "premium/ad-free subscription" line, but Patreon mostly rewards personality-led shows with a human fan relationship, which a synthetic news brief does not have.

---

## 2. CPM levels

### 2.1 What the sources say

| Format or context | CPM (gross, per 1,000 ad impressions) | As of | Source | Confidence |
|---|---|---|---|---|
| "Typical" podcast CPM | about $17-22; $100+ for valuable niches or hard-to-reach audiences | 2026-10-09 | Freakonomics Ep. 690 (via prior note) | medium |
| Programmatic | about $12-15 | 2026 | Podder, citing the Libsyn Ads 2026 rate table (via prior note) | medium |
| Dynamic ad insertion (DAI) | about $18-22 | 2026 | Same | medium |
| Model's own gross programmatic range | $8 / $15 / $22 (cons/base/opt) | Oct 2026 | `finance/build_cost_model.py` | inference |
| High-CPM claim in the AI-podcast press | about $50 | 2025 | One secondary source, quoted in the Jeanine Wright note | low |

- Earlier notes already flagged the $50 figure as unrealistic for synthetic inventory. Do not plan on it.
- **Conflict to keep in view:** "typical $17-22" (Freakonomics) and "programmatic $12-15, DAI $18-22" (Podder/Libsyn) agree on the low-twenties ceiling for mainstream inventory but differ on the floor. The likely reason (inference) is that the first is a market-average for sold, mostly host-read/DAI inventory, while the second is a rate table for a mid-size programmatic marketplace.

### 2.2 By format and genre (host-read, announcer-read, news, true crime)

- **No sourced figure obtained.** The brief asked for CPMs by host-read, announcer-read, programmatic and dynamic formats, and by genre with focus on news and true crime. Only the programmatic and DAI figures above are sourced.
- **Directional inference:** host-read typically sells at a premium over announcer-read and programmatic because the host endorses the product. For Earlobe, a synthetic voice is closer to announcer-read, so the host-read premium should not be assumed. News is usually priced as a mainstream, brand-safety-sensitive genre. True crime has large audiences but is a common brand-safety exclusion category. Neither claim is sourced here.

---

## 3. Format mix: programmatic vs host-read vs baked-in

- **Not verified this session.** No current IAB format split was retrieved.
- Directional facts that are sourced in prior notes: Triton's 2026 outlook describes programmatic audio moving toward **curation, identity and video**, and episode-level "brand fit" scoring, with the Media Rating Council reportedly working on AI-measurement standards (medium; partly vendor sources).
- **Implication (inference):** the programmatic share of podcast spend is rising, and curated marketplaces will decide who gets brand-safe demand. A new, AI-labeled show begins at the bottom of that curation ladder.

---

## 4. Fill rates, sell-through and revenue share

| Item | Value | As of | Source | Confidence |
|---|---|---|---|---|
| Spreaker's cut of programmatic revenue | Spreaker keeps about 40%, publisher about 60% | undated or older | AdExchanger, "Spreaker wants to be the Google AdSense of podcasts" (via prior note) | low |
| Fill rate for AI-made, unvetted, low-audience inventory | assumed 30-80% | 2025-2026 | Earlobe prior note (assumption, not measured) | inference |
| Actual fill rates / revenue of any AI podcast network | never published | 2026-09 | Prior notes (Quiet Please/Inception Point) | n/a |
| Model's share after host/marketplace | 50% / 60% / 70% | Oct 2026 | `build_cost_model.py` | inference |

- **Sell-through** for direct-sold inventory (how much of the available ad time actually sells) has no sourced figure. See section 8 for the planning assumption.
- **Network rev-share norms** (ad-sales rep commission, network splits) were not retrieved. The only sourced anchor is the Spreaker 40% cut, and that is old.

---

## 5. Local podcast advertising

- **No market-size or rate data retrieved** for local-business podcast advertising or the local radio/TV migration to podcasts.
- One usable anecdote (sourced, medium): the former Inception Point CEO told AFP in 2025 that a hyper-niche one-city pollen show heard by only a few dozen people could still attract **antihistamine advertisers**. This is a claim about contextual relevance. It was never matched by disclosed revenue, and the company later said its remaining shows were no longer monetized.
- **Inference:** local money is real in radio and TV, but it is sold on relationships, category exclusivity and flat monthly packages, not on CPM auctions. A brand-new daily brief with a few hundred downloads does not give a local advertiser a measurable audience. The first local revenue is therefore more likely small community-sponsor packages than meaningful income. See the cross-check in section 8.2.

---

## 6. Brand safety and advertiser attitudes to AI podcasts

All rows are carried over from earlier Earlobe notes, with their original sources.

| Signal | Detail | As of | Source | Confidence |
|---|---|---|---|---|
| iHeartMedia "Guaranteed Human" | No AI-generated on-air voices on its radio or on podcasts it publishes. It cites 70% of consumers using AI tools but 90% preferring human-made media. Still in effect in 2026. | 2025-11 | [Radio Ink](https://radioink.com/?p=97798); [AOL](https://www.aol.com/articles/guaranteed-human-audio-giant-iheartmedia-213100883.html) | high |
| Apple Podcasts | Guidelines require prominent disclosure of AI-generated audio, synthetic voices and AI hosts. Podnews found no evidence of enforcement. | 2026 | [Apple guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) | medium-high |
| Spotify | "Verified by Spotify" badges; removes shows that impersonate a creator's likeness. No blanket AI ban. | 2026-05-19 | [Variety](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/) | high (badges), medium (no disclosure rule) |
| Ad market | No industry-wide exclusion of synthetic shows. Trend is disclosure, verification, curated marketplaces and episode-level brand-fit scoring. | 2026 | [Triton Digital outlook](https://tritondigital.com/news-item/December-07-2025/programmatic-audio-shifts-to-curation-identity-and-video-in-2026) | medium |
| AI share of new feeds | 39% of 10,871 new feeds in nine days showed AI signs. Other trackers range from about 25% to about 46%. | 2026-04/05 | [TechRadar](https://www.techradar.com/audio/podslop-is-a-real-and-growing-problem-data-shows-39-percent-of-new-podcasts-are-now-likely-generated-by-ai-heres-why-i-wont-be-listening); [Podnews](https://podnews.net/update/ai-slop-overtakes-humans) | medium-high |
| Discovery suppression | Castro hides Inception Point feeds; Spotify, Podcast Index and Listen Notes apply spam and AI flags. | 2025-2026 | [Castro](https://castro.fm/blog/hiding-inception-point-ai) | medium |

- **What is missing:** a direct advertiser or agency survey on AI-generated podcasts or news adjacency (for example from IAB, Edison, Magellan AI or a brand-safety vendor). None was retrieved.
- **Inference:** the market is not closed to AI shows, but the largest audio seller has marked human-made as the premium, and the flood of low-quality feeds has made platforms suspicious. For a news network the Trust Stack, visible corrections and clear disclosure are the commercial differentiator, not a cost.

---

## 7. Listener attitudes, disclosure and news-podcast listening

- **Reuters Institute Digital News Report 2026, Edison Research, and Pew: not retrieved.** No 2026 number on AI-news comfort, AI-podcast attitudes or news-podcast reach was obtained.
- Only sourced datapoint on disclosure effect: the former Inception Point CEO told AFP in 2025 that disclosure produced "very little drop-off." This is a company claim, unaudited. *(reported; low-medium)*
- iHeart's cited consumer split (70% use AI tools, 90% prefer human-made media) is the only attitude statistic in hand. It comes from iHeart's own memo, so it is advocacy, not independent research. *(reported; medium)*
- **Daily news brief format (The Daily, Up First, NPR local):** no current ranking or download figure retrieved. Qualitative inference only: the short daily brief is an established, high-habit format, but the leaders are strongly human-branded and backed by large newsrooms.

---

## 8. Planning assumptions for a new automated local/news network

All figures here are *(inference)* anchored on the sourced ranges in sections 2 and 4. They replace nothing until real analytics exist. As of Oct 2026, verify before relying on them.

### 8.1 Recommended cases

| Assumption | Conservative | Base | Optimistic | Basis |
|---|---|---|---|---|
| Programmatic gross CPM (per 1,000 impressions) | $8 | $13 | $20 | Libsyn/Podder programmatic $12-15 and DAI $18-22; conservative applies a discount for AI-labeled, uncurated news inventory |
| Programmatic fill rate | 30% | 55% | 75% | Prior-note assumption range of 30-80%; no measured data exists |
| Our share after marketplace/host | 50% | 60% | 70% | Spreaker 40% cut (old) |
| Local direct sponsor effective CPM (per slot, per 1,000 downloads) | $20 | $35 | $60 | Announcer-read premium over programmatic; $17-22 typical, $100+ only for scarce niches |
| Share of local sponsor slots sold | 25% | 50% | 75% | No source; typical sell-through for a new show is far below 100% |
| Downloads per episode, local daily brief (steady state, month 6-12) | 40 | 120 | 400 | Inception Point averaged about 69 per episode across thin feeds (12M / 175K, unaudited); local relevance and distribution partnerships could lift this |
| Downloads per episode, Breaking Desk / national news | 150 | 500 | 2,000 | Inference only; breaking news feeds can spike but compete with large brands |
| Downloads per episode, cold-case / true-crime evergreen | 100 | 400 | 1,500 | Inference only; evergreen archives compound slowly |
| Ad slots per 7-minute brief | 1 | 2 | 2 | Model uses 2 |

**Programmatic revenue per download at 2 slots (inference):** conservative about $0.0024, base about $0.0086, optimistic about $0.021. Per 1,000 downloads that is about $2.40, $8.60 and $21. At 150 downloads, the base case is about $1.29 per episode, which is thin once the Trust Stack's per-episode cost is counted. The model's existing 8/15/22 CPM, 40/60/80 fill and 50/60/70 share give $0.48, $1.62 and $3.70 per episode at 150 downloads. They are close to the recommended set; the main difference is a lower fill and base CPM.

### 8.2 Cross-check: the local sponsor rate in the cost model

`finance/build_cost_model.py` assumes a local sponsor pays **$300 / $750 / $1,500 per show per month**, with a local daily brief at **150 downloads per episode** and **21.7 episodes a month** (stage multipliers 1.0 / 1.5 / 2.5 / 3.5). Treating each sponsor as one slot per episode, the implied effective CPM is:

| Stage | Monthly downloads | Implied CPM at $300 | at $750 | at $1,500 |
|---|---|---|---|---|
| Test | 3,255 | $92 | $230 | $461 |
| Wave 1 | 4,882 | $61 | $154 | $307 |
| Scale | 8,138 | $37 | $92 | $184 |
| Dominate | 11,392 | $26 | $66 | $132 |

- Sourced CPMs top out around $17-22 typical, with $100+ only for scarce niches. Most of this grid sits far above anything the evidence supports, especially the Test and Wave 1 rows.
- At a $35 effective CPM, a $750 monthly sponsor needs about 21,400 monthly downloads, or roughly **990 downloads per episode** on a daily show. At $20 it needs about 1,730 per episode; at $60, about 580.
- At the model's 150 downloads per episode, one sponsor slot is worth only about $65 / $114 / $195 per month at $20 / $35 / $60 CPM.
- **Recommendation (inference):** model sponsor revenue as downloads x slots sold x effective CPM, not as a flat fee. Keep a flat "community sponsor" package only as a labeled low-confidence line, priced at what a small local business pays for goodwill ($50-$150 a month) rather than for audience.

---

## Findings table

| Fact | Value | As of | Source | Confidence |
|---|---|---|---|---|
| Global podcast "industry" size | about $9B | 2026-10-09 | [Freakonomics Ep. 690](https://freakonomics.com/podcast/its-show-business-baby/) (via prior note) | medium |
| Typical podcast CPM | about $17-22; $100+ for valuable niches | 2026-10-09 | Freakonomics Ep. 690 | medium |
| Programmatic podcast CPM | about $12-15 | 2026 | [Podder](https://www.podderapp.com/post/podcast-cpm-rates-2026), citing Libsyn Ads (not re-read this session) | medium |
| DAI podcast CPM | about $18-22 | 2026 | Same | medium |
| Spreaker keeps about 40% of programmatic revenue | 40% | undated/older | [AdExchanger](https://www.adexchanger.com/audio/spreaker-wants-to-be-the-google-adsense-of-podcasts) | low |
| Patreon payouts to podcasters, 2025 | $629M, +33% (brief-supplied) | 2025 | Variety (URL not found; not verified) | low |
| iHeart "Guaranteed Human" policy | no AI on-air voices; 70% use AI tools, 90% prefer human-made | 2025-11 | [Radio Ink](https://radioink.com/?p=97798) | high |
| AI share of new podcast feeds | about 39% (range 25-46%) | 2026-04/05 | [TechRadar](https://www.techradar.com/audio/podslop-is-a-real-and-growing-problem-data-shows-39-percent-of-new-podcasts-are-now-likely-generated-by-ai-heres-why-i-wont-be-listening) | medium-high |
| Inception Point average downloads per episode | about 69 (12M / 175K) | 2025-11 | [Implicator](https://www.implicator.ai/the-dollar-episode-how-inception-point-ai-turned-podcasting-into-arbitrage/) | medium (derived) |
| Apple requires prominent AI disclosure | yes | 2026 | [Apple guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) | medium-high |
| Fill rate for AI-made, low-audience inventory | 30-80% assumed; never measured | 2025-2026 | Prior note | inference |
| Recommended programmatic CPM (cons/base/opt) | $8 / $13 / $20 | Oct 2026 | Analyst inference | inference |
| Recommended fill (cons/base/opt) | 30% / 55% / 75% | Oct 2026 | Analyst inference | inference |
| Recommended local daily-brief downloads per episode | 40 / 120 / 400 | Oct 2026 | Analyst inference | inference |
| Model's local-sponsor rate implies CPM of $92-$461 at Test stage | $92 / $230 / $461 | Oct 2026 | Arithmetic on `build_cost_model.py` inputs | inference (calculation is exact; its significance is judgment) |

---

## 9. Unverified recollections (do NOT cite until sourced)

These came from memory, not from a source seen this session. They are listed only so the follow-up search knows what to confirm or refute. Each is **unverified**, confidence **low**.

| Recollection | Why it is not usable yet |
|---|---|
| IAB's 2025 study put 2024 US podcast ad revenue in the mid-$2B range, with a forecast for 2025 slightly higher | No URL, no figure checked; the 2025 actual and 2026 forecast are the numbers actually wanted |
| Common ad-network rate cards list roughly high-teens CPMs for 30-second spots and mid-$20s for 60-second spots, with finance/business higher and true crime near average | Vendor rate cards change yearly; no 2026 card was seen |
| Weekly use of AI chatbots for news was in the single digits in the 2025 Reuters Institute report, higher among under-25s | Wrong year; the 2026 edition is what matters |
| Edison's Infinite Dial reported monthly podcast listening by a majority of Americans 12+ in 2025 | The 2026 edition and the AI-specific questions were not seen |
| Small-show download benchmarks (median episode in the tens of downloads in the first week) | Host-vendor statistics; edition and definition unknown |

---

## Open questions / gaps

Searches to send in a follow-up (each phrased for the search tool):

1. `IAB US podcast advertising revenue study 2025 results 2026 forecast` (get total, growth, format split, news and true crime share).
2. `IAB PwC podcast ad revenue 2025 host-read programmatic share` (if the format split is in a separate release).
3. `podcast CPM rates 2026 true crime news genre average host-read announcer-read` (AdvertiseCast, Podcorn, Acast, Libsyn).
4. `Variety Patreon podcasters $629 million 2025 33%` (confirm the number and the URL).
5. `Reuters Institute Digital News Report 2026 AI-generated news comfort chatbot weekly use podcasts` and `Digital News Report 2026 United States podcasts news`.
6. `Edison Research 2026 AI-generated podcasts listeners survey disclosure` and `Infinite Dial 2026 podcast listening`.
7. `Pew Research 2026 podcasts news Americans AI` (news-podcast reach and AI attitudes).
8. `advertisers AI-generated podcasts brand safety survey 2026` (IAB, Magellan AI, Podscribe, DoubleVerify, Integral Ad Science).
9. `local podcast advertising local businesses radio groups podcasts 2026` (Audacy, iHeart local, Cumulus, local TV groups moving to podcasts).
10. `podcast ad sell-through fill rate programmatic average` and `Acast Megaphone Libsyn Ads publisher revenue share`.
11. `The Daily Up First downloads 2026 Edison top podcasts news` and `NPR local daily news podcast results`.
12. Direct read of the Freakonomics Ep. 690 transcript for the CPM and $9B context.

Questions that data alone will not answer:

- Does a brand-safe advertiser buy a synthetic-voice news brief at all, or only through remnant programmatic? Test with two or three real local sponsor conversations.
- Do the platforms' AI disclosure rules shift again in the next two quarters? (Apple enforcement, Spotify podcast policy.)
- How much of any early download count is bots or auto-download? Use IAB-certified measurement.

---

## Sources

Carried over from earlier Earlobe notes (not re-read this session unless stated):

- [Freakonomics Radio Ep. 690, "It's Show Business, Baby!" (2026-10-09)](https://freakonomics.com/podcast/its-show-business-baby/)
- [Podder: Podcast CPM rates 2026](https://www.podderapp.com/post/podcast-cpm-rates-2026)
- [Triton Digital: Programmatic audio shifts to curation, identity and video in 2026](https://tritondigital.com/news-item/December-07-2025/programmatic-audio-shifts-to-curation-identity-and-video-in-2026)
- [AdExchanger: Spreaker wants to be the Google AdSense of podcasts (older)](https://www.adexchanger.com/audio/spreaker-wants-to-be-the-google-adsense-of-podcasts)
- [Radio Ink: iHeartMedia draws line against AI voices](https://radioink.com/?p=97798)
- [AOL: "Guaranteed Human", iHeartMedia](https://www.aol.com/articles/guaranteed-human-audio-giant-iheartmedia-213100883.html)
- [Apple Podcasts for Creators: Content guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines)
- [Variety: Spotify bans AI impersonation podcasts, adds verified badges (2026)](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/)
- [TechRadar: 39% of new podcasts likely AI (2026-05-10)](https://www.techradar.com/audio/podslop-is-a-real-and-growing-problem-data-shows-39-percent-of-new-podcasts-are-now-likely-generated-by-ai-heres-why-i-wont-be-listening)
- [Podnews: More new AI-generated podcasts than human ones](https://podnews.net/update/ai-slop-overtakes-humans)
- [Castro: Hiding Inception Point AI Spam](https://castro.fm/blog/hiding-inception-point-ai)
- [Implicator: The Dollar Episode (Nov 2025)](https://www.implicator.ai/the-dollar-episode-how-inception-point-ai-turned-podcasting-into-arbitrage/)
- [TheWrap: An AI Podcasting Machine Is Churning Out 3,000 Episodes a Week (2025-11-17)](https://www.thewrap.com/ai-podcasts-hosts-inception-point-ai/)
- [AFP via France24: Mass-produced AI podcasts disrupt a fragile industry (2025-10-13)](https://www.france24.com/en/live-news/20251013-mass-produced-ai-podcasts-disrupt-a-fragile-industry)

Internal files used:

- `/home/user/curious-and-creative/project-earlobe/docs/research/notes/inception-point-business-model.md`
- `/home/user/curious-and-creative/project-earlobe/docs/research/notes/liquid-studios-pivot-and-press.md`
- `/home/user/curious-and-creative/project-earlobe/docs/research/notes/jeanine-wright-career.md`
- `/home/user/curious-and-creative/project-earlobe/finance/build_cost_model.py`

Not sourced (brief-supplied only): Patreon $629M / +33% attributed to Variety.
