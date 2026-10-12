# Podcast Hosting and Monetization Platforms for a Multi-Show Automated Network (as of Oct 11, 2026)

Research notes for Project Earlobe (Curious & Creative Network). Scope: hosts (Spreaker, Acast, Megaphone, Spotify for Creators, Libsyn, RSS.com, Captivate, Transistor, Buzzsprout, Podbean, Audioboom, Simplecast, Art19, Omny), listener-side money (Spotify Partner Program, Apple Podcasts Subscriptions, Patreon), YouTube and its July 2025 "inauthentic content" policy, and a host strategy for launch, 50+ shows and 500+ shows.

## TL;DR

**Read this first: this note is only partly verified.** The web-search budget for this run was used up before the first hosting query returned, and every direct fetch of a vendor page failed (DNS error). So no vendor pricing page, API doc or policy page was read for this topic. What follows has three evidence grades, tagged in the text: **[repo]** = sourced in earlier Earlobe research notes (links kept, not re-read now), **[task]** = stated in the task brief, **[recall]** = my background knowledge of the market, unverified, low confidence, and often out of date by Oct 2026. Every [recall] price must be re-checked before it goes into the cost workbook (fact IDs F-HOST / F-ADS).

What the evidence does support: (1) the pricing *shape* matters more than any price. Hosts that bill per show (Buzzsprout, Libsyn, Podbean, Spreaker plans) get very expensive at 50 to 500 shows, while hosts that bill by pooled monthly downloads with unlimited shows (Transistor, Captivate) stay at roughly two to three digits a month *(inference, [recall] prices)*. (2) Programmatic ad access is a separate question from hosting and it is the weak spot for synthetic shows: Spreaker's owner iHeartMedia has pledged "Guaranteed Human" **[repo]**, Spotify and Apple have disclosure and impersonation rules **[repo]**, and Inception Point (the biggest AI feed factory) stopped monetizing its shows and pivoted to B2B in 2026 **[repo]**. (3) YouTube's "inauthentic content" rule targets mass-produced, templated output, so a templated daily brief on dozens of channels is the pattern most at risk *(inference)*. **Recommendation (inference):** launch on an API-first, unlimited-show, pooled-download host (Transistor first, Captivate as the alternate), own the feed domain, monetize with local direct sponsors, and treat programmatic as a measured test. At 50+ shows, split feeds across two hosts and run an eRPM bake-off. At 500+, negotiate an enterprise pooled-download deal or run a self-hosted origin, and keep long-tail shows small and unmonetized so volume does not trip spam filters.

## Method and evidence limits

- WebSearch returned "budget used up" on all six first-wave queries. Six WebFetch attempts (Spreaker, Captivate, Transistor, Buzzsprout, Podbean, YouTube Help) all failed with ENOTFOUND. I did not try workarounds through proxies or archives.
- Sources therefore are: earlier repo notes (`inception-point-business-model.md`, `liquid-studios-pivot-and-press.md`), the cost-model assumptions in `finance/build_cost_model.py`, the task brief, and my own background knowledge (training data runs to about mid-2026).
- Per `docs/CONVENTIONS.md`: all costs and policies are **as of Oct 2026 and need verifying before buying**. Inferences are marked *(inference)*.
- Not read at all: any vendor pricing page, any API documentation, YouTube Help's policy text, Apple's subscription terms, Spotify's Partner Program page, and the Podnews Weekly Review of Aug 2026 titled "What Spotify And YouTube Changes Mean For Podcast Revenue" (link in Sources; its content is unknown to me and may change several answers below).

## 1. Evidence already in the repo (sourced earlier, not re-read now)

| Topic | What the earlier notes say | As-of | Confidence |
|---|---|---|---|
| Spreaker programmatic | Spreaker's programmatic ads reportedly make a show profitable at about 20 listens (Podnews, via repo). Inception Point ran its network on Spreaker via API, feeding Apple, Spotify, Amazon/Audible, iHeartRadio and others | 2025 | medium |
| Spreaker revenue share | AdExchanger reported Spreaker keeps 40% (article undated or older) | older | low |
| iHeartMedia stance | "Guaranteed Human": no AI-generated on-air voices on iHeart radio or on podcasts it publishes; AI allowed in back-office work. Spreaker is iHeart-owned | 2025-11, still in effect 2026 | high (pledge); unknown whether it governs third-party shows hosted on Spreaker *(inference)* |
| Programmatic CPMs | Libsyn Ads 2026 rate table via Podder: programmatic about $12 to $15 gross CPM; dynamic ad insertion (DAI) about $18 to $22 | 2026 | medium |
| Spotify | "Verified by Spotify" badges for podcasts (authentic listenership is one factor); removes shows that impersonate a creator, including AI voice clones; no blanket AI ban | 2026-05-19 | high (badges, impersonation); medium (no-disclosure claim) |
| Apple Podcasts | Content guidelines require prominent disclosure of AI-generated audio/video, synthetic voices and AI hosts, in the content and in show/episode metadata; bar deceptive portrayals of real events | 2026 live guidelines | medium to high |
| Discovery gating | Castro hides Inception Point shows; Podcast Index flags "low-effort AI" feeds through a `/recent/problematic` API; Listen Notes removes AI "fake" podcasts (31.5% of new submissions removed as AI in Aug 2026, secondary source) | 2025 to 2026 | medium |
| Ad market | No industry-wide exclusion of synthetic shows; trend is disclosure, verification, curated marketplaces and episode-level brand-fit scoring (Triton 2026 outlook) | 2025-12 (2026 outlook) | medium |
| Inception Point outcome | Peak 15,000+ active shows; by Sep 2026 about 300 active, **none monetized**, plus a few YouTube channels; company pivoted to Liquid Studios, a B2B per-minute service; a publishing freeze was reported in May 2026 (single source) | 2026-09-29 | medium to high |
| Current cost model | Hosting $49/mo times 1, 2, 4, 10 across Test/Wave 1/Scale/Dominate; CPM 8/15/22; fill 40/60/80%; our share 50/60/70%; premium net 70% | repo, Oct 2026 | inference (planning numbers) |

## 2. How hosts charge: the structural point (inference)

| Billing model | Examples | What happens at 10 / 50 / 500 shows |
|---|---|---|
| Per show (plan per podcast, or storage hours per show) | Buzzsprout, Libsyn, Podbean standard plans, Spreaker standard plans | Cost scales linearly with show count. At Buzzsprout's recalled $12 to $24 per show per month, 500 shows is roughly $6,000 to $12,000 a month before any ad income. Not viable for a long tail |
| Pooled monthly downloads, unlimited shows | Transistor, Captivate | Cost tracks total network downloads, not show count. Small audiences per show means a low-tier plan can carry many shows *(check the download allowance, overage rules and any show cap)* |
| Enterprise / quote only | Megaphone, Art19, Omny, Acast network deals, Audioboom, Simplecast enterprise | Price set by negotiation, usually tied to audience size and ad revenue share; vetting of content is likely |
| Free hosting funded by ad share | Spotify for Creators, Acast starter *(recall)*, Spreaker free tier *(recall)* | No fee, but you give up ad revenue share and some control. Policy risk sits with the platform |

Downloads, not show count, are what drive both revenue and cost for a network of small shows, so "unlimited shows with pooled downloads" is the fit for Earlobe's shape (many shows, few downloads each) *(inference)*.

## 3. Host-by-host comparison

**Grade key:** [repo] sourced earlier; [task] from the brief; [recall] unverified background knowledge, low confidence; "unknown" means I have no reliable recollection. Prices are recalled list prices from 2024 to 2025 and may have moved.

| Host | Price for many shows | Publishing API | Dynamic ad insertion (DAI) | Programmatic marketplace and minimums | Creator revenue share | AI-content policy | YouTube distribution |
|---|---|---|---|---|---|---|---|
| **Spreaker** (iHeart) | Plan tiers from free up to a recalled top tier near $50/mo [recall]; publisher/network deals by sales. Per-show limits unknown | Yes, public API, used by Inception Point [repo, medium] | Yes, programmatic DAI [repo] | Programmatic ads "profitable at about 20 listens" [repo]; low minimums | Spreaker keeps about 40% [repo, low, older] | iHeart "Guaranteed Human" pledge [repo]; applicability to hosted third-party shows unclear | Not confirmed; unknown |
| **Acast** | Free and paid tiers for creators [recall]; network deals negotiated | Partner/open API exists [recall, low] | Yes (core product) | Acast Marketplace (programmatic plus sponsor deals); terms and minimums unknown | Revenue split, figure unknown; Acast+ is its paid-subscription product, take unknown | Unknown | Unknown |
| **Megaphone** (Spotify) | Quote only, built for publishers | Yes, documented publisher API [recall, medium] | Yes, native | Access to Spotify's ad network; aimed at established audiences *(inference)* | Negotiated | Unknown; Spotify's public rules in section 4 apply | Unknown |
| **Spotify for Creators** | Free | No public publishing API *(recall, medium)*; RSS ingest only | Spotify-run ads for eligible shows [recall, low] | Spotify ad network; Partner Program (video) in section 4 | Program-specific, see section 4 | Spotify rules [repo] | Not applicable |
| **Libsyn** | Storage-tiered plans per show, roughly $5 to $40/mo [recall]; unlimited downloads on plans [recall, medium]; network/enterprise by sales | Yes, an API exists [recall, low] | Yes, via Libsyn Ads | Libsyn Ads (AdvertiseCast merged in) [recall]; CPMs $12 to $15 programmatic, $18 to $22 DAI [repo] | Unknown | Unknown | Unknown |
| **RSS.com** | "Podcast Networks plan" [task]; prices unknown | API exists [recall, low] | Reportedly yes | Programmatic "from 10 downloads" [task, unverified] | Unknown | Unknown | Unknown |
| **Captivate** | Unlimited shows on every plan, pooled downloads; recalled tiers about $19, $49, $99, $249 per month [recall, low to medium] | Public API [recall, low] | Dynamic content (intros/outros); sponsor insertion via Captivate Sponsors | Captivate Sponsors marketplace; minimums and split unknown | Unknown | Unknown | Unknown |
| **Transistor** | Unlimited shows on every plan, pooled downloads; recalled tiers about $19, $49, $99, higher enterprise [recall, medium] | Yes, documented REST API with episode create, audio upload and publish [recall, medium-high]; scaffolded in repo (`TRANSISTOR_API_KEY`) | Native DAI unconfirmed; [task] lists it as something to check | No ad marketplace that I recall | n/a | Unknown | Unknown |
| **Buzzsprout** | Per show: recalled $12 (3h), $18 (6h), $24 (12h) per month [recall, medium] | Yes, documented API [recall, medium] | "Dynamic content" insertion [recall] | Buzzsprout Ads; minimums unknown | Unknown | Unknown | Unknown |
| **Podbean** | Tiered; recalled about $9 to $29 unlimited-audio plans plus a network plan near $99 [recall, low] | Yes, OAuth API [recall, low] | Yes | Podbean Ads marketplace; minimums unknown | Unknown | Unknown | Unknown |
| **Audioboom** | Network/publisher model, quote based | Publisher API [recall, low] | Yes | Showcase marketplace; curated | Negotiated | Unknown; curated model suggests vetting *(inference)* | Unknown |
| **Simplecast** (SiriusXM) | Tiered plans, roughly $15 and up [recall, low]; enterprise by sales | Yes, public REST API [recall, medium] | Yes via SiriusXM ad stack *(recall, low)* | Via SiriusXM Podcast Network; unknown | Negotiated | Unknown | Unknown |
| **Art19** (Amazon) | Quote only, enterprise | Partner API [recall, low] | Yes, native | Amazon ad stack; curated | Negotiated | Unknown. Amazon reorganized its audio unit in 2025 [repo link: Variety] | Unknown |
| **Omny** (Triton) | Quote only, radio and publisher focus | Yes [recall, low] | Yes, native | Triton marketplace; curated | Negotiated | Unknown | Unknown |

Reading across the table (inference): the *only* hosts I can place with moderate confidence on "unlimited shows plus API plus low fixed cost" are Transistor and Captivate. The enterprise names (Megaphone, Art19, Omny, Acast network, Audioboom) offer the best ad stacks but are quote-based and curated, so assume they say no to an unproven AI-only catalog until a track record exists.

## 4. Listener-side and platform money

**Spotify Partner Program (SPP).** Launched Jan 2025 for video podcasts; pays from Premium-subscriber consumption rather than a CPM split *(recall, medium)*. Recalled early-2025 eligibility: around 12 or more episodes, roughly 2,000 consumption hours and 10,000 streams in 30 days, about 1,000 unique listeners *(recall, low; thresholds and markets have since changed and the Aug 2026 Podnews review likely covers it)*. Needs video episodes, original content and no impersonation. Spotify has made no blanket AI ban but removes AI impersonation and added verified badges in May 2026 **[repo]**. Treat SPP as an upside for the Breaking Desk video show only.

**Apple Podcasts Subscriptions.** Apple Podcasters Program fee recalled at $19.99 per year; Apple's cut recalled at 30% in a subscriber's first year and 15% afterward *(recall, medium)*. Subscription terms and AI-disclosure rules live on Apple's creator guidelines page **[repo link]**. Not read now. The repo's 70% premium net assumption fits year-one Apple economics *(inference)*.

**Patreon.** Recalled: 10% platform fee for new creators since Aug 2025, plus payment processing near 2.9% + $0.30 (higher percentage on small pledges), private podcast feeds per tier *(recall, medium-low)*. Recalled that iOS in-app billing rules were due to tighten in Nov 2026, which would add Apple's cut on iOS signups *(recall, low; check, it is next month)*. Net to creator then sits around 80 to 85% on web, lower via iOS *(inference)*.

**Direct sponsorship (off-host).** The repo model assumes $300 / $750 / $1,500 per show per month in local sponsors. Hosts matter here only for DAI markers, accurate stats and clean exports for sponsor reports *(inference)*.

## 5. YouTube

- **Policy.** In July 2025 YouTube renamed its "repetitious content" rule to **"inauthentic content"** under the Partner Program: mass-produced or repetitive content is not monetizable. YouTube framed this as a clarification of existing policy *(recall, medium; policy text not read now; the date and name are also in the task brief)*. The prior rule on labeling realistic altered or synthetic content still applies *(recall, medium)*.
- **What it means for AI shows (inference).** Automation is not itself banned. The risk is a channel (or channel farm) of near-identical episodes with synthetic voice over static art. A daily brief template across dozens of local markets looks exactly like that to a reviewer. Mitigations: unique reporting per episode (already the Trust Stack's job), meaningful visuals or on-screen sources, human editorial sign-off recorded in the trust log, honest AI disclosure, and few consolidated channels with playlists instead of one channel per show.
- **Partner Program thresholds (recall, medium):** 1,000 subscribers plus 4,000 public watch hours in 12 months for ad revenue; 500 subscribers, 3 public uploads in 90 days and 3,000 watch hours for the earlier fan-funding tier; long-form ad revenue share 55% to creators *(recall, medium-high)*.
- **RSS-ingested podcasts on YouTube.** YouTube can ingest a podcast RSS feed; whether ingested audio earns ad revenue under the same YPP rules is unknown to me (gap).

## 6. AI-content policy landscape by platform

| Platform | Stance | Grade |
|---|---|---|
| iHeart / Spreaker | "Guaranteed Human" pledge for iHeart-published content; hosting-side rules for third parties unknown | high (pledge) / unknown (hosting) |
| Spotify | No blanket ban; impersonation removed; verified badges | high |
| Apple | Prominent AI disclosure in content and metadata | medium to high |
| YouTube | "Inauthentic content" (mass-produced/repetitive) monetization rule; synthetic-media disclosure | medium *(recall)* |
| Podcast Index / Listen Notes / Castro | Flag or remove low-effort AI feeds | medium |
| Other hosts | No reliable information; ask in writing | unknown |

Practical rule (inference): get each host's AI-content position in writing (support ticket or sales email) *before* paying for an annual plan, and keep the disclosure outro plus RSS-level disclosure already required by `docs/CONVENTIONS.md`.

## 7. Recommended host strategy (all inference, built on sections 1 to 6)

**Principles.**
1. Never let one host hold the whole catalog. A single policy decision froze or could freeze every feed (compare the Inception Point freeze reported May 2026).
2. Own the feed URL (a domain you control that points or redirects to the host feed). RSS has a standard move tag (`itunes:new-feed-url`) so migrations keep subscribers *(recall, high)*.
3. Keep the `HostAdapter` abstraction in `earlobe/publish/hosts.py` (the Transistor adapter is marked "verify vs docs"). Adding a second adapter is the main engineering task for multi-host.
4. Do not make programmatic revenue the load-bearing assumption. Sell local sponsors; use programmatic as a measured extra.

**(a) Launch (about 2 test markets, Breaking Desk, a few trackers, up to roughly 10 shows).**
- Host: **Transistor** (API-first, unlimited shows, pooled downloads, adapter already scaffolded). Alternate: **Captivate** (unlimited shows, sponsor marketplace) if Transistor lacks DAI or the AI terms are unclear.
- Budget: use $49 to $99 per month, consistent with the cost model's $49 line.
- Money: direct local sponsors first. Run a small programmatic test (2 or 3 shows) on whichever host-integrated marketplace accepts the shows (RSS.com, Captivate Sponsors, Libsyn Ads or Spreaker) to get a *real* eRPM.
- Platforms: submit RSS to Apple (with AI disclosure metadata) and Spotify; use Spotify for Creators for stats, not hosting. Put Breaking Desk on YouTube as a human-reviewed video show; do not auto-upload every local brief as a template video.
- Before paying: written AI-content confirmation from the host.

**(b) 50+ shows.**
- Keep a pooled-download unlimited-show host as primary; move up a tier if download caps bind (recalled $99 to $250 per month bracket). Avoid per-show-priced hosts: 50 shows at $12 to $24 is $600 to $1,200 per month against roughly $100 to $250 pooled.
- Add a **second host** and cap any one host at roughly 60 to 70% of feeds (inference). Use the split as an experiment: put different markets or verticals on different programmatic marketplaces for 8 to 12 weeks and compare net eRPM, fill and payout reliability.
- Require: DAI with pre/mid/post markers, downloads stats suitable for sponsor reporting, an API rate limit that tolerates daily batch publishing, and webhooks or polling for status.
- Ask the primary host for an enterprise quote; ask the second host about network-plan terms (RSS.com Podcast Networks plan **[task]**, Podbean network plan).

**(c) 500+ shows.**
- Per-show pricing is out (about $6,000 to $12,000 per month at Buzzsprout-style rates). Two workable shapes:
  1. **Enterprise pooled-download deal** with negotiated API limits, an account manager and a written AI policy, spread across two hosts.
  2. **Self-hosted origin** (object storage plus CDN plus the repo's own feed builder) behind a DAI/ad partner. Gains independence and switching power; costs engineering and certified-measurement effort that ad buyers expect.
- Enterprise ad stacks (Megaphone, Art19, Omny, Acast network, Audioboom) are curated. Expect to earn them with audited audience data, not buy in on day one.
- Tier the catalog: monetized flagship shows (local briefs with sponsors, Breaking Desk) on the premium path; evergreen/tracker long tail cheap and mostly unmonetized. The Inception Point record (15,000 shows down to about 300 unmonetized, platform suppression) is the warning that volume without audience compounds nothing **[repo]**.

## 8. Numbers to use in the cost workbook (F-HOST / F-ADS), all provisional

| Key | Value | Rationale |
|---|---|---|
| Hosting, launch | $49 to $99 per month, 1 host | Transistor/Captivate recalled tiers; matches current $49 line |
| Hosting, 50+ shows | $99 to $250 per month per host, 2 hosts | Pooled tier bracket, two hosts for resilience |
| Hosting, 500+ shows | Enterprise quote; placeholder $500 to $1,500 per month | No data; negotiate; revisit after quotes |
| Programmatic CPM | $12 to $15 gross; DAI $18 to $22 | Libsyn Ads table via Podder **[repo]**; existing model range 8/15/22 stays |
| Our share of ad revenue | 50% base, 60% to 70% upside | Spreaker keeps about 40% **[repo, low]**; other splits unknown, so stay conservative |
| Apple year-one net | 70% (85% after year one) | Recalled 30%/15% Apple cut |
| Patreon net | about 80 to 85% on web | Recalled fees; lower on iOS |
| YouTube long-form share | 55% | Recalled YPP split |

## 9. Findings table

| Fact | Value | As-of | Source | Confidence |
|---|---|---|---|---|
| Spreaker programmatic profitability | About 20 listens | 2025 | Podnews via repo notes | medium |
| Spreaker revenue share | Spreaker keeps 40% | older | AdExchanger | low |
| iHeartMedia "Guaranteed Human" | No AI on-air voices on iHeart-published content | 2025-11 | Radio Ink; AOL | high |
| Programmatic podcast CPM | $12 to $15 gross; DAI $18 to $22 | 2026 | Podder (Libsyn Ads table) | medium |
| Spotify verified badges, impersonation removal | Announced | 2026-05-19 | Variety; MBW; TheWrap | high |
| Apple AI disclosure guideline | Required in content and metadata | 2026 | Apple creator guidelines | medium to high |
| Inception Point status | About 300 active shows, none monetized; pivot to B2B | 2026-09-29 | Podnews | medium to high |
| AI share of new feeds | About 25% to 45% | 2026 | Multiple trackers via repo | medium |
| Transistor / Captivate billing | Unlimited shows, pooled downloads | recall (2024 to 2025) | Vendor pages, not read | low |
| Transistor and Captivate recalled tiers | About $19 / $49 / $99 (Captivate also about $249) | recall | Vendor pages, not read | low |
| Buzzsprout pricing | About $12 / $18 / $24 per show per month | recall | Vendor page, not read | low to medium |
| Apple Subscriptions cut | 30% year one, 15% after | recall | Apple, not read | low to medium |
| Apple Podcasters Program fee | $19.99 per year | recall | Apple, not read | low to medium |
| Patreon fee | 10% for new creators plus processing | recall (Aug 2025) | Patreon, not read | low to medium |
| YouTube "inauthentic content" rename | July 2025, replaces "repetitious content" | recall; also in task brief | YouTube Help, not read | medium |
| YPP ad thresholds and share | 1,000 subs plus 4,000 hours; 55% long-form share | recall | YouTube Help, not read | medium |
| Spotify Partner Program | Pays from Premium video consumption; early-2025 thresholds recalled | recall | Spotify, not read | low |
| RSS.com programmatic minimum | "From 10 downloads" | stated in task brief | Task brief, unverified | low |

## 10. Open questions / gaps (in priority order)

1. **Re-run this research with search enabled.** Ask for a follow-up turn or raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`. Priority checks, in order: Transistor and Captivate current plans, download caps, overage rules, API write access, DAI; RSS.com Podcast Networks plan and the "10 downloads" programmatic claim; Spreaker publisher plan and whether iHeart's "Guaranteed Human" applies to hosted third-party shows; each host's written AI-content policy.
2. Read the Podnews Weekly Review (Aug 2026) on Spotify and YouTube revenue changes. It may supersede the Spotify Partner Program and YouTube details above.
3. YouTube Help text for "inauthentic content" and any podcast-specific guidance; whether RSS-ingested podcasts are monetizable.
4. Spotify Partner Program: current eligibility thresholds, markets and whether non-video shows can join.
5. Acast Marketplace, Megaphone, Art19, Omny, Audioboom: minimum audience, revenue share and willingness to onboard AI-produced shows. All unknown here.
6. Apple Subscriptions terms and any 2026 changes; Patreon fee and iOS billing change timing (possibly Nov 2026).
7. Revenue-share figures for every host other than Spreaker's old 40% report.
8. Whether certified download measurement is required by local sponsors and by enterprise ad stacks, and who provides it for a self-hosted origin.
9. How much ad revenue a synthetic, disclosed local-news show actually earns; no real analytics until launch.

## 11. Sources

Earlier repo research (links carried over, not re-read in this run):
- [AdExchanger: Spreaker wants to be the Google AdSense of podcasts](https://www.adexchanger.com/audio/spreaker-wants-to-be-the-google-adsense-of-podcasts)
- [Podder: Podcast CPM rates 2026](https://www.podderapp.com/post/podcast-cpm-rates-2026)
- [Podnews: The podcast factory making 3,000 episodes a week](https://podnews.net/update/ai-slop)
- [Podnews: Was Inception Point AI just a PR stunt? (2026-09-29)](https://podnews.net/update/inception-point-pr-stunt)
- [Podnews Weekly Review: What Spotify And YouTube Changes Mean For Podcast Revenue (Aug 2026), unread](https://weekly.podnews.net/1538779/episodes/19679394-what-spotify-and-youtube-changes-mean-for-podcast-revenue)
- [Radio Ink: iHeartMedia draws line against AI voices](https://radioink.com/?p=97798)
- [AOL: "Guaranteed Human", iHeartMedia](https://www.aol.com/articles/guaranteed-human-audio-giant-iheartmedia-213100883.html)
- [Variety: Spotify bans AI impersonation, adds verified badges (2026)](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/)
- [Music Business Worldwide: Verified badges extended to podcasts](https://www.musicbusinessworldwide.com/spotify-extends-verified-by-spotify-badges-to-podcasts-further-cracking-down-on-ai-impersonators/)
- [TheWrap: Spotify adds verified badges to podcasts](https://www.thewrap.com/industry-news/tech/spotify-adds-verified-badges-podcasts-against-ai/)
- [Apple Podcasts for Creators: Content and subscription guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines)
- [Triton Digital: Programmatic audio shifts in 2026](https://tritondigital.com/news-item/December-07-2025/programmatic-audio-shifts-to-curation-identity-and-video-in-2026)
- [Castro: Hiding Inception Point AI Spam](https://castro.fm/blog/hiding-inception-point-ai)
- [PodcastVideos: Inception Point AI Silent Freeze (about 2026-06-01)](https://www.podcastvideos.com/articles/inception-point-ai-freeze-synthetic-podcast-networks/)
- [Variety: Amazon reorganizes audio (2025)](https://au.variety.com/2025/biz/news/amazon-reorganizes-audio-wondery-audible-jen-sargent-exit-26111)

Vendor pages to verify against (NOT read in this run; listed as where to check, not as evidence):
- [Spreaker pricing](https://www.spreaker.com/pricing)
- [Captivate pricing](https://www.captivate.fm/pricing)
- [Transistor pricing](https://transistor.fm/pricing/)
- [Buzzsprout pricing](https://www.buzzsprout.com/pricing)
- [Podbean pricing](https://www.podbean.com/podcast-hosting-pricing)
- [YouTube Help: Partner Program policies](https://support.google.com/youtube/answer/1311392)
