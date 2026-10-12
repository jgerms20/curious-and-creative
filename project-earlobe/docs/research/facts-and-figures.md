# Facts and figures: the canonical numbers sheet

**As of 2026-10-12** · Project Earlobe (Curious & Creative Network) · cited by every doc and by [`finance/cost-model.xlsx`](../../finance/cost-model.xlsx) (inputs live in `finance/build_cost_model.py`). A number lives here first, with source and date, then gets cited by ID ([CONVENTIONS](../CONVENTIONS.md) rule 1). IDs are stable: never renumber, add the next free number.

**Evidence status (read first).** Every research pass behind this sheet ran with web search and page fetches blocked or used up. **No vendor page, statute, court portal or pricing page was opened.** Source tags: `web` = search-result snippet or third-party tracker; `recall` = analyst memory, unverified; `repo` = our own files; `brief` = the task brief; `inf` = our inference. Confidence: **high** = several concordant sources or settled law; **med** = plausible, one or secondary source; **low** = recall, single source or conflicting. Anything below high is a planning number, not a quote.

## Five things founders should know

1. **Ads alone do not pay for a local brief** *(inference)*. One 7-minute verified brief costs about $2.00 in Claude work (F-LLM-07) plus $0.56 to $1.16 of voice (F-TTS-17), against about $1.03 of ad revenue at the research base case of 120 downloads (F-AUD-03, F-ADS-12). Sponsors, B2B and cost discipline decide the business.
2. **The model's local-sponsor rates are not supported.** $300 / $750 / $1,500 a month implies ad CPMs of $92 to $461; the sourced ceiling is $17 to $22 (F-ADS-04, F-ADS-14).
3. **Under-budgeted:** insurance ($78 vs about $500 a month planning figure), media-lawyer setup ($1,500 vs $2,500 to $7,500), Test-stage PACER, California LLC tax (see Model assumptions).
4. **Voice has a cheaper route.** ElevenLabs API (about $0.08 per 1K chars) is roughly half the subscription rate; Google Chirp 3 HD is about $0.03 a minute. A hybrid cuts Scale and Dominate voice cost by roughly 35% to 75% (F-TTS-12, F-TTS-23, F-TTS-37).
5. **Hosting, insurance and legal prices are mostly recall.** Get written quotes (and each host's AI-content position in writing) before paying anything.

## F-TTS: voice engines (ElevenLabs, alternatives, NotebookLM, Meta Muse)

*As of Oct 2026 — verify before buying. Prices come from search snippets and trackers, not vendor pages.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-TTS-01 | ElevenLabs Free | $0; 10,000 credits; **no commercial license** | | Oct 2026 | high | web [EL pricing](https://elevenlabs.io/pricing) |
| F-TTS-02 | Starter | $6/mo; 30,000 credits; commercial license; hard stop, no overage | older posts say $5 | Oct 2026 | high | web [EL pricing](https://elevenlabs.io/pricing) |
| F-TTS-03 | Creator | $22/mo ($11 first month); 121,000 credits; 1 pro voice-clone slot | | Oct 2026 | high | web [Gradually](https://www.gradually.ai/en/elevenlabs-pricing/) |
| F-TTS-04 | Pro | $99/mo; 600,000 credits | | Oct 2026 | high | web [Gradually](https://www.gradually.ai/en/elevenlabs-pricing/), [BigVu](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) |
| F-TTS-05 | Scale | $299/mo; 1,800,000 credits; 3 seats | | Oct 2026 | high | web [Costbench](https://costbench.com/software/ai-voice-tools/elevenlabs/) |
| F-TTS-06 | Business | $990/mo; 6,000,000 credits; 10 seats | older quote $1,320 (outdated or annual) | Oct 2026 | med-high | web [Costbench](https://costbench.com/software/ai-voice-tools/elevenlabs/) |
| F-TTS-07 | Enterprise | custom; the model uses $3,000 for 30M credits *(inference, no source)* | | Oct 2026 | low | inf |
| F-TTS-08 | Annual billing | pay 10 of 12 months (Pro $990/yr); Pro/Scale/Business about $0.138 per 1K credits | monthly about $0.165 | Oct 2026 | high | web [EL pricing](https://elevenlabs.io/pricing) |
| F-TTS-09 | Credits per character | 1.0 (v3, Multilingual v2); 0.5 (Flash, Turbo) | | Sep 2026 | high | web [Oakgen](https://oakgen.ai/blog/elevenlabs-pricing-limits-cost), [Texttolab](https://texttolab.com/blog/elevenlabs-pricing) |
| F-TTS-10 | Effective $ per 1K credits, monthly billing | Starter 0.200; Creator 0.182; Pro 0.165; Scale 0.166; Business 0.165 | | Oct 2026 | high | calc from F-TTS-02 to 06 |
| F-TTS-11 | Overage per 1K credits | $0.24 Pro; $0.30 Creator *(use for planning)* | $0.12 to $0.30 | 2026 | low | web [HappyRobot](https://www.happyrobot.ai/hub/elevenlabs-pricing), [Smallest.ai](https://smallest.ai/blog/elevenlabs-pricing-explained-plans-limits-hidden-costs-calculator) |
| F-TTS-12 | API per 1K chars, v3 / Multilingual v2 | **$0.08 base; $0.10 conservative** | $0.10 (Sep 23) vs $0.08 (Oct 2) | Oct 2026 | med (conflict) | web [ModelsLab](https://modelslab.com/elevenlabs-api-pricing), [Cartesia](https://www.cartesia.ai/learn/elevenlabs-pricing) |
| F-TTS-13 | API per 1K chars, Flash / Turbo | $0.04 base; $0.05 conservative | $0.05 vs $0.04 | Oct 2026 | med (conflict) | same as F-TTS-12 |
| F-TTS-14 | Eleven v4 / v4 Turbo | list $0.08 / $0.04 per 1K; **plan on list** | launch promo 72% off to Oct 12 ($0.022 / $0.011) vs 50% off to Oct 19 | Oct 2026 | med | web [ElevenAPI](https://elevenlabs.io/pricing/api), [OpenRouter](https://openrouter.ai/elevenlabs/eleven-v4) |
| F-TTS-15 | Characters per finished minute | 1,000 | 850 to 1,000 (150 wpm x about 5.7 chars) | Oct 2026 | med | inf |
| F-TTS-16 | Billing overhead for re-renders and QA | 1.25x *(inference)* | | Oct 2026 | low | inf |
| F-TTS-17 | Cost per 8-min / 20-min episode (7-min brief = 7 x per-minute) | API base $0.64 / $1.60; API conservative $0.80 / $2.00; Pro subscription $1.32 / $3.30 | Starter sub $1.60 / $4.00; Flash sub $0.66 / $1.65 | Oct 2026 | med | calc from F-TTS-10, 12 |
| F-TTS-18 | Concurrency by plan | Free 2, Starter 3, Creator 5, Pro 10, Scale 15, Business 15 (Flash about 2x) | | 2026 | med-high | web [EL blog](https://elevenlabs.io/blog/ai-rate-limiting-for-voice) |
| F-TTS-19 | Professional voice-clone slots | Starter 0, Creator 1, Pro 1, Scale 3, Business 10 | one aggregator says Pro 10 | 2026 | med | web [EL help](https://elevenlabs.io/docs/help-center/product/voice-customization/voice-cloning/how-many-professional-voice-clones-pv-cs-can-i-have) |
| F-TTS-20 | Per-request character cap | v3 5,000; Multilingual v2 10,000; Flash v2.5 40,000 (chunk and stitch) | one guide says 40,000 for v2/v3 | 2026 | low-med | web [Aireiter](https://aireiter.com/blog/elevenlabs-eleven-v3-api-guide) |
| F-TTS-21 | Text-to-Dialogue (v3) | create/stream-dialogue endpoints; billed per character (unconfirmed) | | 2026 | low-med | web [MuAPI](https://muapi.ai/comparison/elevenlabs-text-to-dialogue-v3) |
| F-TTS-22 | Startup Grant | 12 months; 33M credits (about 2.75M/mo); under 25 staff; show grant logo; reverts to Free; excludes projects aimed at under-18s | whether plain TTS for a media company qualifies: unknown | 2026 | med-high | web [EL grants](https://elevenlabs.io/startup-grants?ref=medito) |
| F-TTS-23 | Google Chirp 3 HD | $30 per 1M chars = $0.03/min (8-min episode $0.24); first 1M chars/mo free | | Jul 2026 | high | web [Google TTS](https://cloud.google.com/text-to-speech/pricing/?authuser=8) |
| F-TTS-24 | Other Google TTS tiers | Studio $160; Neural2/Polyglot $16; WaveNet/Standard $4; Instant Custom Voice $60 per 1M chars | | Jul 2026 | med-high | web [DIYAI](https://diyai.io/ai-tools/audio-generation/google-cloud-text-to-speech-pricing/) |
| F-TTS-25 | Gemini TTS (preview) | 2.5 Flash $0.50 in / $10 audio out per 1M tokens, about $0.015 to $0.019/min; 3.1 Flash $1 / $20 (batch $10 out), about $0.030 to $0.038/min | assumes 25 to 32 audio tokens/sec (unverified) | 2026 | med | web [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing) |
| F-TTS-26 | Azure AI Speech | Neural about $15; HD about $22 per 1M chars; 0.5M free/mo | US list unconfirmed | 2026 | med-low | web [Inventive HQ](https://inventivehq.com/tools/developer/tts-stt-api-cost-calculator) |
| F-TTS-27 | Amazon Polly | Standard $4; Neural $16; Generative $30; Long-Form $100 per 1M chars | | 2026 | med | web [Costbench](https://costbench.com/software/voice-apis/amazon-polly-api/) |
| F-TTS-28 | OpenAI TTS | tts-1 $15; tts-1-hd $30 per 1M chars; gpt-4o-mini-tts about $0.015/min | | Jul 2026 | med | web [CostGoat](https://costgoat.com/pricing/openai-tts) |
| F-TTS-29 | Cartesia Sonic 3 | $39 to $49 (1.25M credits); $239 to $299 (8M); about $0.037 to $0.039/min | | May to Jul 2026 | med-low | web [CloudTalk](https://www.cloudtalk.io/blog/cartesia-pricing/) |
| F-TTS-30 | Hume Octave | Pro $70 per 1M chars; Scale $200 per 3.3M; Business $500 per 10M ($0.05 to $0.07/min) | | 2026 | med-low | web [Costbench](https://www.costbench.com/software/voice-apis/hume-ai/) |
| F-TTS-31 | Resemble; PlayHT | Resemble $0.0005/sec ($0.03/min); **avoid PlayHT/PlayAI** (Meta reportedly bought PlayAI in 2025, status unclear) | | Jun 2026 | low | web [Voiceflow](https://www.voiceflow.com/articles/resemble-ai) |
| F-TTS-32 | NotebookLM / Gemini Notebook | Audio Overviews per day: Free 3, Plus 6, Pro 20, Ultra 100 to 200; no controllable commercial API (Enterprise REST v1alpha, undocumented); commercial terms not found. **Not a production engine** | | Jul to Sep 2026 | med | web [NotebookLM Guide](https://notebooklm-guide.com/notebooklm-audio-overview-limits/) |
| F-TTS-33 | Google AI Pro / Ultra plan price | about $20 / about $250 per month (the model uses $19.99) | | 2026 | low | recall (unverified) |
| F-TTS-34 | Meta Muse | Personal AI agent, US, launched 2026-09-08: Power $20/mo, Maximum $100/mo. **Not a TTS**; Muse Voice Transcribe is speech-to-text only (possible QA transcriber, price unknown) | | Sep 2026 | med-high | web [Meta](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/), [Meta API docs](https://dev.meta.ai/docs/models) |
| F-TTS-35 | Voice spend/mo, Pilot (1,000 finished min, 1.25M chars) | hybrid not needed; all-ElevenLabs subscription $255 to $299 | EL API $100 to $125; Flash API $50 to $62; Chirp 3 HD about $8 | Oct 2026 | low-med | inf (voice note section 5) |
| F-TTS-36 | Expansion (3,000 min) | hybrid (20% EL, 80% Chirp) about $120; Business subscription $990 | EL API $300 to $375; Chirp about $82 | Oct 2026 | low-med | inf |
| F-TTS-37 | Scale (10,000 min) | hybrid about $470; all-EL subscription about $2,060 | EL API $1,000 to $1,250; Chirp about $345 | Oct 2026 | low-med | inf |
| F-TTS-38 | Mass (30,000 min) | hybrid about $1,470; all-EL subscription about $6,190 | EL API $3,000 to $3,750; Chirp about $1,095 | Oct 2026 | low-med | inf |

## F-LLM: Claude API (tiers, search, batch, cache)

*As of Oct 2026 — verify before buying. Tiers only; concrete model IDs live in environment variables (CONVENTIONS rule 4).*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-LLM-01 | Opus tier | $4.00 in / $20.00 out per 1M tokens | | Oct 2026 | high | brief; [Anthropic pricing](https://www.anthropic.com/pricing) |
| F-LLM-02 | Sonnet tier | $2.00 in / $10.00 out per 1M tokens | | Oct 2026 | high | brief |
| F-LLM-03 | Haiku tier | $0.10 in / $0.50 out per 1M tokens | | Oct 2026 | high | brief |
| F-LLM-04 | Web search tool | $10 per 1,000 searches | | Oct 2026 | high | brief |
| F-LLM-05 | Batch API | 50% off; use for evergreen and archive, never breaking | | Oct 2026 | high | brief |
| F-LLM-06 | Prompt caching | cache reads bill at 0.1x input; cache-write premium not in our sources (gap); the model's 15% blended saving is *(inference)* | | Oct 2026 | high (reads) | brief |
| F-LLM-07 | One baseline 7-min verified brief | **$2.00**: Opus tier $1.89 (verifier alone $1.04 incl. 20 searches = $0.20), Sonnet tier $0.10, Haiku tier $0.01 | local brief after caching and 30% rewrites: $2.00 | Oct 2026 | med | calc from F-LLM-01 to 04 and `repo` token budgets *(inference)* |
| F-LLM-08 | Reference: Inception Point LLM passes per episode | $0.01 to $0.05 (3-min); $0.10 to $0.40 (10-min); $0.30 to $0.80 (20-min), small and mid models | Earlobe's verification chain costs roughly 5x to 20x more, by design | 2026 | low | inf [IP teardown](notes/inception-point-business-model.md) |

## F-HOST: podcast hosts, platform money and platform AI rules

*As of Oct 2026 — verify before buying. **Host prices and terms are recall** (no host page was read); get written quotes and written AI-content positions first.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-HOST-01 | How hosts bill | Pooled downloads with unlimited shows (Transistor, Captivate) beat per-show billing (Buzzsprout, Libsyn, Podbean, Spreaker plans) at 50+ shows; enterprise hosts quote only | | 2026 | med *(inference)* | inf [hosting note](notes/hosting-and-monetization-platforms.md) |
| F-HOST-02 | Transistor | about $19 / $49 / $99 per month; unlimited shows; REST API (create, upload, publish); DAI unconfirmed | | recall (2024 to 25) | low | recall [Transistor](https://transistor.fm/pricing/) |
| F-HOST-03 | Captivate | about $19 / $49 / $99 / $249; unlimited shows; Sponsors marketplace; split unknown | | recall | low-med | recall [Captivate](https://www.captivate.fm/pricing) |
| F-HOST-04 | Buzzsprout | $12 (3h) / $18 (6h) / $24 (12h) per show per month; 500 shows = $6,000 to $12,000/mo | | recall | low-med | recall [Buzzsprout](https://www.buzzsprout.com/pricing) |
| F-HOST-05 | Libsyn; Podbean | Libsyn about $5 to $40/mo per show; Podbean about $9 to $29 plus network plan near $99 | | recall | low | recall [Podbean](https://www.podbean.com/podcast-hosting-pricing) |
| F-HOST-06 | Spreaker (iHeart) | free to about $50/mo recalled; public API; programmatic profitable at about 20 listens | | 2025 | low-med | web [Podnews](https://podnews.net/update/ai-slop) |
| F-HOST-07 | Spreaker revenue share | Spreaker keeps about 40% (publisher about 60%) | undated, older article | older | low | web [AdExchanger](https://www.adexchanger.com/audio/spreaker-wants-to-be-the-google-adsense-of-podcasts) |
| F-HOST-08 | RSS.com | "Podcast Networks plan"; programmatic "from 10 downloads" (brief claim, unverified) | | 2026 | low | brief |
| F-HOST-09 | Megaphone, Art19, Omny, Acast network, Audioboom | quote only, curated; assume they decline an unproven AI-only catalog until audited audience data exists *(inference)* | | 2026 | low | inf |
| F-HOST-10 | Hosting budget by stage *(inference)* | launch $49 to $99/mo, 1 host; 50+ shows $99 to $250/mo per host x 2 hosts; 500+ placeholder $500 to $1,500/mo | | Oct 2026 | low | inf |
| F-HOST-11 | Apple Podcasts Subscriptions | Apple keeps 30% year one, 15% after; Podcasters Program $19.99/yr | | recall | low-med | recall [Apple](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) |
| F-HOST-12 | Patreon | 10% platform fee (new creators, Aug 2025) plus processing about 2.9% + $0.30; net about 80% to 85% on web | iOS billing changes possibly Nov 2026 | recall | low-med | recall |
| F-HOST-13 | YouTube Partner Program | 1,000 subs + 4,000 public watch hours (12 mo) for ads; 55% long-form share; July 2025 "inauthentic content" rule hits mass-produced, repetitive channels | | recall | med | recall [YouTube Help](https://support.google.com/youtube/answer/1311392) |
| F-HOST-14 | Spotify Partner Program | video podcasts, pays from Premium consumption; early-2025 thresholds about 2,000 hours, 10,000 streams, 1,000 listeners (since changed) | | recall | low | recall |
| F-HOST-15 | Apple AI rule | prominent AI disclosure in content and in show/episode metadata; enforcement not evident | older "material portion" wording | 2026 | med-high | web [Apple guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) |
| F-HOST-16 | Spotify AI rule | "Verified by Spotify" badges and removal of impersonating shows (2026-05-19); no blanket AI ban; no podcast AI-label rule reported | | May 2026 | high (badges) | web [Variety](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/) |
| F-HOST-17 | iHeartMedia "Guaranteed Human" | no AI on-air voices on iHeart radio or podcasts it publishes; applies to third-party shows on Spreaker: unknown | | Nov 2025 | high | web [Radio Ink](https://radioink.com/?p=97798) |
| F-HOST-18 | Discovery gating | Castro hides Inception Point shows; Podcast Index `/recent/problematic` flags "low-effort AI"; Listen Notes removed 31.5% of Aug 2026 new submissions as AI | | 2025 to 2026 | med | web [Castro](https://castro.fm/blog/hiding-inception-point-ai) |

## F-ADS: ad market, CPMs, fill, revenue share

*As of Oct 2026 — verify before buying. Almost no ad figure here is measured; planning cases are inference anchored on two sourced ranges.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-ADS-01 | Global podcast "industry" size | about $9B (broad; **not** ad revenue) | | 2026-10-09 | med | web [Freakonomics 690](https://freakonomics.com/podcast/its-show-business-baby/) |
| F-ADS-02 | US podcast ad revenue (IAB/PwC) | **no sourced figure; do not cite** | recollection only: mid-$2B for 2024 | | n/a | recall |
| F-ADS-03 | Patreon payouts to podcasters, 2025 | $629M, +33% | | 2025 | low | brief (attributed to Variety, URL not found) |
| F-ADS-04 | Typical podcast CPM | $17 to $22 | $100+ for scarce niches | 2026-10-09 | med | web [Freakonomics 690](https://freakonomics.com/podcast/its-show-business-baby/) |
| F-ADS-05 | Programmatic / DAI CPM | $12 to $15 / $18 to $22 gross | | 2026 | med | web [Podder](https://www.podderapp.com/post/podcast-cpm-rates-2026) |
| F-ADS-06 | "About $50 CPM" claim | **do not plan on it** | | 2025 | low | web (one secondary source) |
| F-ADS-07 | Planning CPM, cons / base / opt | **$8 / $13 / $20** gross, programmatic | | Oct 2026 | low | inf |
| F-ADS-08 | Planning fill, cons / base / opt | **30% / 55% / 75%** | prior range 30% to 80%; no AI network has published fill | Oct 2026 | low | inf |
| F-ADS-09 | Our share after host/marketplace | 50% / 60% / 70% | Spreaker keeps about 40% (F-HOST-07); other splits unknown | Oct 2026 | low | inf |
| F-ADS-10 | Local direct sponsor, effective CPM per slot | $20 / $35 / $60 per 1,000 downloads; slots sold 25% / 50% / 75% | flat community package $50 to $150/mo | Oct 2026 | low | inf |
| F-ADS-11 | Ad slots per 7-min brief | 1 / 2 / 2 | | Oct 2026 | low | inf |
| F-ADS-12 | Net programmatic revenue per download at 2 slots | $0.0024 / **$0.0086** / $0.021 (per 1,000: $2.40 / $8.60 / $21) | | Oct 2026 | low | inf, calc from F-ADS-07 to 11 |
| F-ADS-13 | Break-even downloads per episode, ads only (IP-note scenarios) | episode cost $0.50: about 347 / 69 / 23; $1.00: about 694 / 139 / 46 (low / mid / high) | | Oct 2026 | low | inf [IP teardown](notes/inception-point-business-model.md) |
| F-ADS-14 | Cross-check on the model's sponsor rates | $300 / $750 / $1,500 at 3,255 downloads/mo (150 x 21.7) = effective CPM $92 / $230 / $461; a $750 sponsor at $35 CPM needs about 21,400 downloads/mo (about 990 per daily episode) | | Oct 2026 | high (arithmetic) | calc [ad-market note](notes/ad-market-and-audience.md) |
| F-ADS-15 | Market direction | programmatic shifting to curation, identity, video and episode-level brand-fit scoring; no industry-wide exclusion of synthetic shows | | Dec 2025 | med | web [Triton](https://tritondigital.com/news-item/December-07-2025/programmatic-audio-shifts-to-curation-identity-and-video-in-2026) |

## F-AUD: audience and listener data

*As of Oct 2026 — verify before buying. No independent 2026 listener-attitude survey (Edison, Pew, Reuters Institute) was retrieved.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-AUD-01 | AI share of new podcast feeds | plan on 25% to 45%; 39% = 4,243 of 10,871 new feeds in 9 days | 45.7% vs 44.6% legit (Podnews, 24h); Listen Notes 31.5% (Aug 2026); Forbes about 25% | Apr to May 2026 | med-high | web [TechRadar](https://www.techradar.com/audio/podslop-is-a-real-and-growing-problem-data-shows-39-percent-of-new-podcasts-are-now-likely-generated-by-ai-heres-why-i-wont-be-listening), [Podnews](https://podnews.net/update/ai-slop-overtakes-humans) |
| F-AUD-02 | Downloads per episode, thin AI feeds (benchmark) | about 69 (12M / 175K); see F-IPA-07 | | Nov 2025 | med (derived) | web [Implicator](https://www.implicator.ai/the-dollar-episode-how-inception-point-ai-turned-podcasting-into-arbitrage/) |
| F-AUD-03 | Local daily brief, downloads per episode, steady state (month 6 to 12) | cons / base / opt **40 / 120 / 400** | | Oct 2026 | low | inf |
| F-AUD-04 | Breaking Desk; cold-case evergreen, downloads per episode | 150 / 500 / 2,000; 100 / 400 / 1,500 | | Oct 2026 | low | inf |
| F-AUD-05 | Effect of AI disclosure on listening | "very little drop-off" (company claim, unaudited) | | 2025 | low-med | web [AFP](https://www.france24.com/en/live-news/20251013-mass-produced-ai-podcasts-disrupt-a-fragile-industry) |
| F-AUD-06 | Consumer attitudes | 70% use AI tools, 90% prefer human-made media (iHeart memo; advocacy, not independent) | | Nov 2025 | med | web [Radio Ink](https://radioink.com/?p=97798) |
| F-AUD-07 | AI and news trust | about 7% weekly AI-chatbot news use (Reuters Institute 2025); about 45% of AI-assistant news answers had a significant issue (EBU/BBC, Oct 2025) | | 2025 | low-med | recall [Reuters Institute](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025) |
| F-AUD-08 | Local news gap (Medill) | zero-source counties about 204 / 206 / 213 (2023 / 24 / 25); one-source about 1,560 / 1,560 / 1,520; about 55% to 56% of counties have 0 or 1 source *(derived)*; about 3,500 papers lost since 2005. Richland County and LA County are **not** news deserts | | 2023 to 2025 | low | recall [Medill](https://localnewsinitiative.northwestern.edu/projects/state-of-local-news/) |
| F-AUD-09 | DMA ranks | New York #1, Los Angeles #2, Chicago #3; Columbia SC about 71 to 80 | | recall | med-high / low | recall [Nielsen](https://www.nielsen.com/) |
| F-AUD-10 | Share of shows that are profitable | about 1% (widely repeated) | | 2026-10-09 | low-med | web [Freakonomics 690](https://freakonomics.com/podcast/its-show-business-baby/) |

## F-IPA: Inception Point / Quiet Please / Liquid Studios

*As of Oct 2026 — verify before buying. Company figures are unaudited. Section marked inference is our reasoning, not a fact about the company.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-IPA-01 | Shows | 5,000+ (Sep 2025); 10,000+ (spring 2026); "15,000+" peak (CEO, Sep 2026); **about 300 active, none monetized** (2026-09-29), plus about 6 YouTube channels | 11,000+ (conference page); Spreaker-listed 4,749 (Indicator) | 2025 to 2026 | high (300) | web [Podnews](https://podnews.net/update/inception-point-pr-stunt), [THR](https://www.hollywoodreporter.com/business/digital/ai-podcast-start-up-plan-shows-1236361367/) |
| F-IPA-02 | Output | 3,000+ episodes/week (Sep to Dec 2025); 200+ new podcasts/day before a halt; 325 new shows in one day (about 1 in 5 of all new shows, about Apr 2026) | 10,000/wk (company, May 2026, low) | 2025 to 2026 | med | web [Podnews](https://podnews.net/update/ai-slop-overtakes-humans) |
| F-IPA-03 | Total episodes | 160K+ (Sep 2025); 175K+ (Nov); 200K+ (Dec, about 1% of all episodes some weeks); 300K+ claimed (2026) | | 2025 to 2026 | med | web [LA Times via The Star](https://www.thestar.com.my/tech/tech-news/2025/12/24/podcast-industry-under-siege-as-ai-bots-flood-airways) |
| F-IPA-04 | Cost per episode; break-even | about $1 or less; about 1 hour idea to publish; about 20 listens to profit, excluding overhead (company claims) | holds only if episode cost under about $0.45 and the high ad case (F-ADS-13) | Sep 2025 | high (as claim) | web [THR](https://www.hollywoodreporter.com/business/digital/ai-podcast-start-up-plan-shows-1236361367/), [AFP](https://www.france24.com/en/live-news/20251013-mass-produced-ai-podcasts-disrupt-a-fragile-industry) |
| F-IPA-05 | Reverse-engineered cost per episode at list *(inference)* | 3-min $0.17 to $0.38; 10-min $0.58 to $1.37; 20-min $1.27 to $2.73; with -40% TTS discount $0.11 to $0.26 / $0.40 to $1.00 / $0.90 to $2.00 | | 2026 | low | inf [IP teardown](notes/inception-point-business-model.md) |
| F-IPA-06 | Team and stack | 8 staff (4 on content); 184 agents (2025) vs 160+ (site, 2026); LLMs OpenAI, Perplexity, Claude, Gemini; voice Hume EVI (vendor case study; no ElevenLabs link found); 50+ then 120+ AI personas | | 2025 to 2026 | med | web [Hume](https://www.hume.ai/blog/case-study-hume-inception-point), [TheWrap](https://www.thewrap.com/ai-podcasts-hosts-inception-point-ai/) |
| F-IPA-07 | Audience | 10M downloads (Sep 2025); 12M lifetime and 400K subscribers (Nov 2025); **about 69 per episode**, about 2,000 per show (derived); bot inflation not ruled out | | Nov 2025 | med | web [TheWrap](https://www.thewrap.com/ai-podcasts-hosts-inception-point-ai/) |
| F-IPA-08 | Revenue | Spreaker programmatic ads; revenue never disclosed (Latka "$770K" unreliable); 2026-09-29: fully synthetic content "no longer a revenue source" | | 2026-09-29 | med-high | web [Lead Balloon 73](https://www.podcampmedia.com/post/lead-balloon-ep-73-ai-podcast-hosts-scrapped-inception-point-ceo-jeanine-wright-explains-pivot) |
| F-IPA-09 | Liquid Studios offer and price | list **$10 per finished video minute** (about $600 per 60-min episode); audio-only about **$1 per episode**; claims 15,000+ podcasts, 300K+ episodes, about 40 languages; **no named customers** | live page not read | Oct 2026 | med | web [Liquid Studios](https://liquidstudios.ai/) |
| F-IPA-10 | Platform actions | Castro hid shows (late 2025); Podcast Index removals; publishing freeze 2026-05-07 (single source) | | 2025 to 2026 | med / low (freeze) | web [PodcastVideos](https://www.podcastvideos.com/articles/inception-point-ai-freeze-synthetic-podcast-networks/) |
| F-IPA-11 | Funding; founding | about $5.05M (Reg D $5,052,490); seed 2026-01-29 (PitchBook) vs Series A 2026-01-20 (Tracxn); founded 2023 (AFP) vs 2024 (PitchBook) | investors unconfirmed | 2026 | med | web [intelligence360](https://www.intelligence360.news/inception-point-ai-has-filed-a-notice-of-an-exempt-offering-of-securities-to-raise-5052490-00-in-new-funding/) |
| F-IPA-12 | Network-level sanity check *(inference)* | 175K episodes x $0.50 to $1.00 = $88K to $175K variable cost vs 12M downloads x $0.0072 to $0.0216 = $86K to $259K lifetime ad revenue: about break-even before 8 salaries | | 2025 | low | inf |
| F-IPA-13 | Other competitors (tier B recall; do not cite outward) | Patch about 30,000 AI-newsletter communities planned; Axios Local about 30+ metros; Nexstar-Tegna $6.2B (Aug 2025, status unverified); CPB about $1.1B rescinded July 2025 | | 2025 | low | recall [competitive note](notes/competitive-landscape.md) |

## F-LEGAL: insurance, trademark, DBA, lawyer, rules with numbers

*As of Oct 2026 — verify before buying. **Not legal advice**; nothing here was checked live. Items needing a media lawyer or CPA are in the legal note.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-LEGAL-01 | Media liability (E&O) insurance | **$6,000/yr ($500/mo)** placeholder, $1M limit, $10,000 retention *(inference)* | small podcast $500 to $2,500/yr; small news publisher $2,500 to $10,000+/yr, retention $2,500 to $25,000; automated court/crime may be priced up or declined | 2026 | low | recall broker quotes needed; the model's "$78/mo (Insureon)" is **not in the research notes** |
| F-LEGAL-02 | Media-lawyer setup review (P0) | $2,500 to $7,500 flat fee *(inference)*; clearance plus filing $500 to $2,000 per mark | | Oct 2026 | low | inf [legal note](notes/legal-compliance-business-setup.md) |
| F-LEGAL-03 | USPTO trademark | **$350 per class** (from 2025-01-18); file Class 41 (intent-to-use) then 9; skip 38; 35 later | surcharges $100 / $200 / $200 per extra 1,000 chars; Statement of Use $150, extension $250, renewals $325 per class | 2025 | med | recall [USPTO fees](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) |
| F-LEGAL-04 | DBA "Curious & Creative Network" | CA fictitious name: LA County about $26 (+$5 per extra name/owner) plus 4-week newspaper publication about $30 to $150; file within 40 days; valid 5 years | SC: no statewide DBA (local license may apply); NY about $25 + county; IL up to about $150 | recall | low | recall [LA County RR/CC](https://www.lavote.gov/home/county-clerk/fictitious-business-names) |
| F-LEGAL-05 | California LLC tax | $800/yr minimum franchise tax if the LLC does business in CA (+ fee above $250,000 gross receipts; foreign registration if formed elsewhere); formation state unknown | | recall | med | recall [FTB](https://www.ftb.ca.gov/file/business/types/limited-liability-company/index.html) |
| F-LEGAL-06 | Music beds | business-tier library license $15 to $50/mo; commissioned theme and stems $500 to $5,000 one-time *(inference)*; no commercial songs | networks need enterprise quote | recall | low | recall [Epidemic Sound](https://www.epidemicsound.com/pricing/) |
| F-LEGAL-07 | Small fees | DMCA agent $6 per 3 years; domains $10 to $25/yr each; Apple Podcasters Program $19.99/yr (only if selling subscriptions) | | recall | low-med | recall [USCO](https://www.copyright.gov/dmca-directory/) |
| F-LEGAL-08 | Defamation clock and records | limitation CA 1 yr, NY 1 yr, IL 1 yr, SC 2 yrs; keep scripts, source packs, trust logs at least 3 years; re-releasing an archive episode can restart the clock | | recall | med | recall [SC Code 15-3](https://www.scstatehouse.gov/code/t15c003.php) |
| F-LEGAL-09 | Private-figure fault, public-concern speech | CA negligence; NY "gross irresponsibility" plus actual malice in public-interest suits (2020); IL negligence; SC fault required, level unconfirmed. Public figures: actual malice | | recall | med | recall [Gertz](https://supreme.justia.com/cases/federal/us/418/323/) |
| F-LEGAL-10 | Fair-report privilege | CA Civ. Code 47(d) (absolute); NY Civil Rights Law 74; IL common law (*Solaia* 2006); SC common law (confirm) | | recall | med | recall [Cal. Civ. 47](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=47) |
| F-LEGAL-11 | AI defamation and 230 | no Section 230 shield for our own scripts; *Walters v. OpenAI* summary judgment for OpenAI 2025-05-19 (one reader, public figure): **not protective** for broadcast news; *Starbuck v. Meta* settled Aug 2025 | CA retraction 48a (20-day demand, 3-week correction) may not cover podcasts | 2025 | med | recall [CourtListener](https://www.courtlistener.com/?q=%22Walters%22+%22OpenAI%22+defamation) |
| F-LEGAL-12 | Copyright | facts free (*Feist* 1991); AI-only output not protectable (*Thaler*, 2025-03-18); *Dow Jones v. Perplexity* dismissal denied (Aug 2025); *Bartz v. Anthropic* about $1.5B settlement (piracy, Sep 2025) | | 2025 | med | recall [USCO AI](https://www.copyright.gov/ai/) |
| F-LEGAL-13 | AI-disclosure laws | EU AI Act Art. 50 applies from 2026-08-02 (fines up to EUR 15M or 3% of turnover); CA SB 942 delayed to 2026-08-02 by AB 853 ($5,000 per violation per day; binds vendors with 1M+ monthly users, not us); YouTube synthetic label since 2024-03-18 | | 2026 | med | recall [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) |
| F-LEGAL-14 | FTC | Endorsement Guides rev. 2023-06-29 (AI hosts cannot claim personal experience); fake-review rule eff. 2024-10-21; impersonation rule eff. 2024-04-01; about $53,088 per violation; CAN-SPAM opt-out within 10 business days | | recall | med | recall [16 CFR 255](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-255) |
| F-LEGAL-15 | Privacy thresholds | CCPA at $26,625,000 revenue or 100,000+ CA consumers/households (the realistic trigger); CalOPPA policy from day one; BIPA $1,000 / $5,000 per violation (no voiceprints) | | 2025 | med | recall [CPPA](https://cppa.ca.gov/regulations/) |
| F-LEGAL-16 | Voice and likeness | TN ELVIS Act eff. 2024-07-01; CA AB 1836 / AB 2602 eff. 2025-01-01; CA post-mortem right 70 years; never clone real people | | 2024 to 2025 | med | recall [TN HB 2091](https://wapp.capitol.tn.gov/apps/BillInfo/Default.aspx?BillNumber=HB2091&GA=113) |
| F-LEGAL-17 | Public-domain line; BOI | published works up to 1930 now, 1931 on 2027-01-01; unpublished life + 70 years. US-formed LLCs exempt from BOI reporting (Mar 2025) | | 2026 | med | recall [Cornell](https://copyright.cornell.edu/publicdomain), [FinCEN](https://www.fincen.gov/boi) |

## F-DATA: news, court and government data

*As of Oct 2026 — verify before buying. Terms of use (bulk access, automation) were not checked for any source.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-DATA-01 | CourtListener / RECAP | free API token; REST v4 `search/?type=r`; **coverage partial**; court ids `scd` (config says `dsc`), `cacd`, `nysd`, `nyed`, `ilnd`, `scotus` | rate limit about 5,000 calls/hr (recall) | 2026 | med | repo `earlobe/sensors/courtlistener.py`; [CourtListener](https://www.courtlistener.com/help/api/rest/) |
| F-DATA-02 | PACER | $0.10/page; $3.00 cap per document; no charge at $30 or less per quarter; opinions free. Court Watch cap proposal $150 to $300/mo *(inference)* | worst case $450 to $1,800/mo at 10 to 20 documents a day | recall | med / low (waiver) | recall [PACER](https://pacer.uscourts.gov/pacer-pricing-how-fees-work) |
| F-DATA-03 | GDELT DOC 2.0 | $0, no key; 1 request per 5 sec; 75 records (250 for velocity); can answer 200 with plain text; terms unverified | | 2026 | high (behavior) / low (terms) | repo `earlobe/sensors/gdelt.py`; [GDELT](https://api.gdeltproject.org/api/v2/doc/doc) |
| F-DATA-04 | RSS market feeds | $0; **43 market feeds, all `verified: false`**; likely good: WordPress `/feed/`, NYT NYRegion, NWS; guessed: The State, Post and Courier, CivicPlus sites, `justice.gov/usao-*` RSS, LAist, WBEZ, Tribune. Fix with feed autodiscovery | | 2026-10-11 | high (repo fact) | repo `config/sources/*.yaml` |
| F-DATA-05 | Paid news and search APIs beyond RSS | **not researched**; the model uses $0 / $100 / $500 / $2,000 a month *(inference)* | | | gap | inf |
| F-DATA-06 | Free government feeds | NWS API: free, no key, descriptive User-Agent required; city open-data portals (NYC, Chicago, Cook County, LA) free; Legistar Web API `webapi.legistar.com/v1/<client>` (some token-gated) | | recall | med | recall [NWS](https://www.weather.gov/documentation/services-web-api) |
| F-DATA-07 | DOJ, FBI | DOJ press-release JSON (page size up to about 50); FBI Wanted `api.fbi.gov/wanted/v1/list`; FBI Crime Data Explorer free key via api.data.gov. All unverified | | recall | low | recall [DOJ developer](https://www.justice.gov/developer) |
| F-DATA-08 | Library of Congress (Chronicling America) | free; endpoints moving to loc.gov (`?fo=json`); poll at most 1 request/sec with backoff; newspapers over 95 years old are public domain | | recall | low-med | recall [LoC APIs](https://www.loc.gov/apis/) |
| F-DATA-09 | Cold-case sources | NamUs: no documented public API (manual only); Doe Network and Charley Project: copyrighted, **leads only, no scraping**; Murder Accountability Project: free aggregate CSV, no names | | recall | low | recall [NamUs](https://namus.nij.ojp.gov/) |
| F-DATA-10 | State and local court portals | SC Public Index free (no family/juvenile); NYSCEF free to view; WebCrims status only (records can be sealed); LA Superior Court summaries free, **document-image fee unknown**; Cook County civil free, copies per page, criminal unclear | terms often bar bulk automation | recall | low | recall [NY Courts](https://www.nycourts.gov/) |
| F-DATA-11 | Reuse licences | States Newsroom (SC Daily Gazette) CC BY-NC-ND (recall): facts in our words plus link only; Wikipedia CC BY-SA 4.0: leads only; licensed archives (Newspapers.com): never scrape or quote | | recall | med / low | recall [SC Daily Gazette](https://scdailygazette.com/) |

## F-INFRA: build and run infrastructure

*As of Oct 2026 — verify before buying. **No research pass covered these vendors**; rows come from the cost model's own notes and recall.*

| ID | Item | Value used | Range seen | As-of | Conf. | Source |
|---|---|---|---|---|---|---|
| F-INFRA-01 | GitHub Actions | public repo: free; private repo on Free plan about 2,000 min/mo; Team $4 per user per month (about 3,000 min); Linux overage about $0.008/min | GitHub re-priced runners for 2026 (recall); verify | recall | low | repo `finance/build_cost_model.py`; recall [GitHub pricing](https://github.com/pricing) |
| F-INFRA-02 | Actions minutes needed *(inference)* | at an assumed 10 min of runner per episode: about 1,250 / 4,400 / 22,800 / 96,900 min a month for Test / Wave 1 / Scale / Dominate (episodes 125 / 444 / 2,278 / 9,689 from the model) | job length unmeasured | Oct 2026 | low | inf |
| F-INFRA-03 | Supabase | Free $0 (projects pause after about a week idle; risky for always-on); Pro $25/mo per project | | recall | low-med | repo `finance/build_cost_model.py`; recall [Supabase pricing](https://supabase.com/pricing) |
| F-INFRA-04 | Admin tools | domain + mailbox $8/mo; bookkeeping $30/mo (QuickBooks Online, Xero or Wave, Wave is free); Canva-class design $15/mo | all *(inference)* | Oct 2026 | low | inf |

## Model assumptions: cost model vs research

Checked against `finance/build_cost_model.py` (read 2026-10-12). **OK** = matches research. **FLAG** = research disagrees (corrected value given). **UNSUPPORTED** = no research either way (an *(inference)* input; tune from analytics). **ADD** = a real cost the model lacks.

| Model input | Model value | Research says | Verdict | Corrected value or action |
|---|---|---|---|---|
| `chars_per_min` | 1,000 | 850 to 1,000 (F-TTS-15) | OK | none |
| `credits_per_char` | 1.0 | 1.0 full quality, 0.5 Flash/Turbo (F-TTS-09); 1.25x re-render overhead (F-TTS-16) | FLAG | use 1.25 effective, or add an overhead input; Flash for daily briefs halves it |
| `weekdays`, `days` | 21.7, 30.4 | arithmetic | OK | none |
| `cache_savings`, `rewrite_rate`, `rewrite_share` | 15%, 30%, 60% | only mechanics (reads 0.1x, F-LLM-06) | UNSUPPORTED | tune from gate logs after launch |
| `batch_discount` | 50% | F-LLM-05 | OK | the formula also discounts the $0.20 search fee; unverified, small |
| Claude tiers and search | 4/20, 2/10, 0.10/0.50; $10 per 1K | F-LLM-01 to 04 | OK | none |
| `STEPS` token budgets | $2.00 baseline | no research (F-LLM-07); IP ran 5x to 20x cheaper (F-LLM-08) | UNSUPPORTED | keep; measure real tokens per gate |
| Ad slots per episode | local 2 | base 2, conservative 1 (F-ADS-11) | OK | none |
| Downloads/ep, Test stage | local 150; breaking 600; courts 120; tracker 400; cold case 700; archive 500; niche 60 | local 40 / **120** / 400; breaking 150 / **500** / 2,000; cold case 100 / **400** / 1,500 (F-AUD-03, 04); IP actual 69 (F-IPA-07) | FLAG | local 120, breaking 500, cold case 400; courts, tracker, archive, niche are unresearched |
| `DOWNLOAD_MULT` | 1.0 / 1.5 / 2.5 / 3.5 | local at Dominate = 525 vs research optimistic 400 | FLAG | cap local at 400 per episode |
| `SHOW_COUNTS` | 7 / 27 / 157 / 693 shows | IP lesson: flooding feeds drew Castro, Podcast Index and AI-spam filters (F-IPA-10, F-AUD-01) | FLAG (risk) | 100 niche feeds at Scale and 500 at Dominate need slow, human-plausible rollout |
| ElevenLabs Creator, Pro, Scale, Business | 22/121K, 99/600K, 299/1.8M, 990/6M | F-TTS-03 to 06 | OK | none |
| Enterprise | $3,000 for 30M credits ($0.10/1K) | no source (F-TTS-07); Business is $0.165/1K | UNSUPPORTED | get a quote before trusting Scale and Dominate voice cost |
| Plan by scenario | Pro / Business / Enterprise / Enterprise | Test needs 1.2M credits (1.5M with overhead): Pro plus overage $244 to $316, so Scale $299 (F-TTS-35). Wave 1 needs 3.6M, Business $990 matches F-TTS-36 | FLAG (Test) | Test = Scale ($299); model now shows $189 |
| Engine mix | all ElevenLabs | hybrid from about 3,000 min/mo: Scale needs 16,462 min, model $3,000 vs hybrid about $775; Dominate 65,280 min, model $5,117 vs about $3,200 (pro rata from F-TTS-37, 38) | FLAG (conservative) | add an engine-mix input; model overstates Scale and Dominate voice by about 37% to 74% if adopted |
| `OVERAGE_PER_1K` | 0.15 / 0.12 / 0.08 / 0.06 | $0.12 to $0.30; Pro about $0.24 (F-TTS-11) | FLAG (Test) | Test 0.24; later stages are negotiated (unknown) |
| Programmatic CPM | $8 / $15 / $22 | $8 / **13** / 20; sourced programmatic $12 to $15 (F-ADS-05, 07) | FLAG | base 13, optimistic 20 |
| Fill | 40% / 60% / 80% | 30% / 55% / 75%; never measured (F-ADS-08) | FLAG | 30 / 55 / 75 |
| Our share | 50% / 60% / 70% | same (F-ADS-09) | OK | none |
| Revenue per download at 2 slots | cons $0.0032, base $0.0108, opt $0.0246 | $0.0024, $0.0086, $0.021 (F-ADS-12) | FLAG | model base ad revenue is about 26% high; fixed by the CPM and fill rows |
| `sponsor_rate` | $300 / $750 / $1,500 per show a month | implied CPM $92 to $461 (F-ADS-14); sourced $17 to $22 | **FLAG (wrong)** | model downloads x slots x effective CPM: per show-month at 150 downloads $16 / $57 / $146 (F-ADS-10); keep flat community packages at $50 to $150 |
| `b2b_rate` | $1,000 / $2,000 / $3,500 per client a month | only anchors: $10 per video minute (about $1,520/mo for a daily 7-min show) and about $1 per audio episode (about $22/mo); no Liquid Studios customers named (F-IPA-09) | UNSUPPORTED | sits at the video anchor, 46x to 161x the audio anchor; validate with 2 or 3 buyers before it enters any base case |
| `api_rate`, `services_rate`, volumes | $500 to $3,000; $1,500 to $5,000 | none | UNSUPPORTED | treat as hypotheses; keep out of network-only net |
| `premium_price`, `PREMIUM_NET` | $3 / $5 / $7; 70% | Apple 70% then 85%; Patreon about 80% to 85% (F-HOST-11, 12); Patreon rewards personality-led shows (F-ADS-03) | OK (net) | subscriber counts (0 / 50 / 500 / 3,000) unsupported |
| Hosting | $49 x 1 / 2 / 4 / 10 | launch $49 to $99; 50+ shows $99 to $250 x 2 hosts; 500+ $500 to $1,500 (F-HOST-10) | FLAG (Dominate) | Dominate $490 vs $500 to $1,500; all recall |
| Insurance | $78 x 1 / 1 / 2 / 3 | $500/mo planning; $208 to $833/mo for small news publishers (F-LEGAL-01); the $78 source is not in the notes | **FLAG (low)** | $500/mo from Test; may be declined for automated court and crime |
| GitHub, Compute | $0; $0 / 20 / 150 / 800 | no research (F-INFRA-01, 02); plausible *(inference)* | UNSUPPORTED | check minutes after the first month |
| Supabase | $0 all stages | free tier pauses when idle (F-INFRA-03) | FLAG (Wave 1+) | $25/mo from Wave 1 |
| News/court data | $0 / 100 / 500 / 2,000 | PACER proposal $150 to $300/mo (F-DATA-02); paid news APIs unresearched | FLAG (Test) | Test $150 for PACER, CourtListener first |
| Google AI Pro | $19.99 x 1 / 1 / 0 / 0 | NotebookLM is not a production engine (F-TTS-32) | FLAG | drop, or leave as optional prototyping |
| Domain+email, bookkeeping, design, contract help | $8; $30; $15; $0 to $8,000 | F-INFRA-04 | UNSUPPORTED | keep |
| Not in the model | none | CA LLC tax $800/yr (F-LEGAL-05); music license $15 to $50/mo (F-LEGAL-06); ongoing lawyer retainer | **ADD** | add $67/mo and $30/mo lines |
| ElevenLabs Startup Grant | not modeled | 33M credits over 12 months (F-TTS-22): Pilot (about 15M credits a year) fits; Expansion (about 45M) does not | ADD (upside) | add a grant-credits toggle |
| One-time: media lawyer | $1,500 | $2,500 to $7,500 (F-LEGAL-02) | FLAG | $2,500 low, $5,000 mid |
| One-time: trademark | $700 (2 classes) | USPTO $350/class OK (F-LEGAL-03); attorney clearance $500 to $2,000 per mark; "Curious" is crowded | FLAG (add) | add $500 to $2,000 clearance |
| One-time: DBA, art/sonic logo, domain, voice design | $50; $500; $20; $0 | CA DBA about $56 to $176 (F-LEGAL-04); theme $500 to $5,000 (F-LEGAL-06); domain $10 to $25 | OK (DBA slightly low) | DBA $60 to $180 |
| Per-episode result *(derived)* | | local brief: LLM $2.00 + voice $0.56 to $1.16 vs ads $1.03 at research base (F-LLM-07, F-TTS-17, F-ADS-12) | FLAG | ads lose about $1.5 to $2.1 per episode; sponsors or cheaper voice must close it |

## Conflicts and unknowns

| # | Conflict | What each side says | Use until resolved | IDs |
|---|---|---|---|---|
| C1 | ElevenLabs API rate | $0.10 / $0.05 per 1K (Sep 23, majority) vs $0.08 / $0.04 (Oct 2, newest) | base $0.08, conservative $0.10; ask sales if the API carries the same commercial, concurrency and voice rights as a subscription (about 2x price gap) | F-TTS-12, 13 |
| C2 | v4 launch promo | 72% off to Oct 12 (EL page) vs 50% off to Oct 19 (OpenRouter); launch Sep 28 vs Oct 7 | list prices; the 72% promo ends today | F-TTS-14 |
| C3 | Overage, PVC slots, request caps | $0.12 to $0.30; Pro 1 vs 10 clone slots; v3 cap 5,000 vs 40,000 | $0.24; 1 slot; chunk at 5,000 | F-TTS-11, 19, 20 |
| C4 | Startup Grant fit | voice note says Pilot and Expansion fit; arithmetic says Expansion (about 45M credits a year) exceeds 33M; plain-TTS eligibility unknown | apply; plan on Pilot only | F-TTS-22 |
| C5 | CPM floor | typical $17 to $22 vs programmatic $12 to $15 vs model base $15 vs "about $50" outlier | base $13 | F-ADS-04 to 07 |
| C6 | Insurance | model $78/mo vs $500 to $2,500/yr (podcast) vs $2,500 to $10,000+/yr (news publisher) | $6,000/yr | F-LEGAL-01 |
| C7 | Inception Point history | founded 2023 vs 2024; seed vs Series A; peak 10,000+ / 11,000+ / 15,000+ shows; 184 vs 160+ agents; entity "Liquify AI" vs "name unchanged"; Hume confirmed, ElevenLabs no evidence | quote ranges, label company-reported | F-IPA-01 to 11 |
| C8 | AI share of new feeds | 25% (Forbes) to 46% (Podnews) | plan 25% to 45% | F-AUD-01 |
| C9 | Platform AI rules | Apple "prominent disclosure" vs older "material portion"; Spotify podcast AI-label rule unverified | disclose in audio and metadata everywhere | F-HOST-15, 16 |
| C10 | Host facts | all recall; Transistor DAI unconfirmed; RSS.com "10 downloads" unverified; Spreaker 40% share old | written quotes; base share 60% | F-HOST-02 to 08 |
| C11 | CourtListener SC id | `scd` vs config `dsc` (sensor aliases) | `scd`; fix `config/markets.yaml` | F-DATA-01 |

**Unknowns (not in this sheet because no source exists yet):**

- **Market data:** IAB/PwC US podcast ad revenue; CPM by genre (news, true crime); real fill and sell-through; local podcast ad market; advertiser surveys on AI audio; Edison, Pew and Reuters Institute 2026 attitudes; news-podcast reach; daily-brief rankings.
- **Costs:** paid news-API prices; current GitHub Actions and Supabase plans; Anthropic cache-write premium; insurer quotes and GenAI exclusions; LA Superior Court fees; ElevenLabs Voice Design limits, GenFM price and prohibited-use rules for news and political content; Gemini audio tokens per second; Meta Model API price; LLC formation state.
- **Competitors and legal:** Liquid Studios customers; whether Inception Point's SC and LA feeds are still live; Medill 2025 and 2026 counts; SC fair-report and anti-SLAPP law; 2026 AI-defamation rulings against publishers; New York synthetic-performer ad-law date.
- **Resolve by:** a follow-up research pass with search enabled, then write the verified value into the row and bump its As-of; keep the old value in Range seen.
