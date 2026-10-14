# Voice / TTS Engines and Costs (as of Oct 11, 2026)

Research notes for Project Earlobe (Curious & Creative Network). Scope: ElevenLabs plans and API pricing, alternative TTS engines, NotebookLM / Gemini Notebook audio, and what "Meta Muse" is, ending in a recommended engine plan by volume tier.

## TL;DR

ElevenLabs is still the quality-first choice for flagship shows, but it is not the cheapest way to produce audio. Its subscription plans work out to about $0.165 to $0.20 per finished minute on the full-quality models (1 credit per character), or about half that on Flash/Turbo (0.5 credit per character). Its separate pay-as-you-go API rate card is cheaper still: $0.08 to $0.10 per 1,000 characters on v3 and Multilingual v2, and $0.04 to $0.05 on Flash/Turbo. Sources conflict on which pair is current. The $0.08/$0.04 pair is the newest report (Oct 2, 2026) and the $0.10/$0.05 pair is the Sept 2026 consensus. A new Eleven v4 model launched around Sept 28, 2026 at $0.08 list, with a 72% launch discount that ends Oct 12, 2026, which is tomorrow. At 1,000 characters per finished minute, an 8-minute episode costs about $0.64 to $0.80 on ElevenLabs v3 via API, and about $1.32 to $1.60 via a subscription. A 20-minute episode costs about $1.60 to $2.00 via API and $3.30 to $4.00 via a subscription. Hyperscaler engines are 3 to 8 times cheaper: Google Chirp 3 HD at $0.03 per minute (1M free characters a month), Azure HD at about $0.022, Amazon Polly Generative at $0.03, Gemini TTS at roughly $0.015 to $0.04 per minute (inferred from token prices), and OpenAI at $0.015 to $0.03. NotebookLM (now also called Gemini Notebook) is a consumer tool with daily caps of 3 (free), 6 (Plus), 20 (Pro) and 100 to 200 (Ultra) Audio Overviews, with no verified commercial-use terms and a controllable API only on the Enterprise edition, so it is not a production engine. "Meta Muse" is Meta's personal AI agent (launched Sept 8, 2026) and the Muse model family from Meta Superintelligence Labs. It does not generate podcast audio. Its audio product, Muse Voice Transcribe, is speech-to-text only, and it could serve as a QA transcriber. The recommendation is to run ElevenLabs as the primary engine for flagship shows, build a Google Chirp 3 HD adapter from day one as failover and low-cost engine for commodity local briefs, and move most local-news minutes to the cheap engines once monthly volume passes about 3,000 finished minutes.

## Method and assumptions

- Conversion: about 1,000 characters per finished audio minute (the task's assumption). A news-read pace of about 150 words per minute, at roughly 5.7 characters per word including spaces, gives about 850 to 1,000 characters per minute, so 1,000 is slightly conservative (inference).
- Episode sizes: 8-minute episode = 8,000 characters; 20-minute episode = 20,000 characters.
- Billed volume includes a 1.25x overhead for re-renders, QA retakes and fixes after the Trust Stack (inference, a planning number, not sourced).
- Two ElevenLabs price regimes are modelled: the subscription (credits) and the API rate card (per 1,000 characters). They differ by roughly 2x.
- Tools note: the environment blocked direct page fetches for almost every domain (DNS failures), and the search budget ran out before the last few planned checks. Official vendor pages were seen only through search-result snippets, which is flagged in the confidence column. Nothing here was read directly from a vendor page.

## 1. ElevenLabs

### 1.1 Plans (subscription)

| Plan | Price/mo | Credits/mo | Finished min at 1 cr/char (v3, Multilingual v2) | Finished min at 0.5 cr/char (Flash/Turbo) | Notes |
|---|---|---|---|---|---|
| Free | $0 | 10,000 | about 10 | about 20 | No commercial license (reported) |
| Starter | $6 | 30,000 | about 30 | about 60 | Commercial license, instant voice cloning; hard stop at the limit (no overage) |
| Creator | $22 ($11 first month) | 121,000 | about 121 | about 242 | Professional voice cloning (1 slot); overage allowed |
| Pro | $99 | 600,000 | about 600 | about 1,200 | 44.1 kHz PCM via API, lower overage rate |
| Scale | $299 | 1,800,000 | about 1,800 | about 3,600 | 3 workspace seats |
| Business | $990 | 6,000,000 | about 6,000 | about 12,000 | 10 workspace seats |
| Enterprise | custom | custom | custom | custom | Elevated limits negotiated |

- Annual billing gives two months free (pay for 10 months). That works out to $60/yr Starter, $220 Creator, $990 Pro, $2,990 Scale, $9,900 Business (inference from the official "2 months free" statement). Older articles quoting Starter at $5 and a Business price of $1,320 are outdated or reflect annual pricing.
- Effective subscription price per 1,000 credits (monthly billing): Starter $0.200, Creator $0.182, Pro $0.165, Scale $0.166, Business $0.165. On annual billing, Pro, Scale and Business drop to about $0.138. Scale and Business give almost no volume discount per credit over Pro; the upgrade buys credits, seats, concurrency and voice slots, not a better rate (inference from the arithmetic).
- Credits are shared across all ElevenLabs products (Studio, dubbing, agents, etc.) per the official French pricing page snippet.
- Overage: Starter cannot go over. Creator reportedly pays about $0.30 per 1,000 credits and Pro about $0.24 (single-source, low confidence). Another aggregator quotes a range of $0.30 down to $0.12 per 1,000 for Multilingual v2 by tier, and a third quotes about $0.18/min on Creator and $0.17/min on Pro. These do not agree, so treat overage as roughly $0.12 to $0.30 per 1,000 credits and get it confirmed.
- Rollover: one source says unused credits carry for up to two months, capped at twice the monthly quota (low confidence).

### 1.2 Credits per character and API rate card

- Credits per character: 1 credit per character on Multilingual v2 and Eleven v3; 0.5 credit per character on Flash and Turbo models (several concurring sources; high-medium confidence).
- API (ElevenAPI) per 1,000 characters, conflicting:
  - $0.10 for v3 and Multilingual v2, $0.05 for Flash/Turbo and v3 Conversational. This is the majority view, with a ModelsLab check dated Sept 23, 2026 and other guides from Sept 2026.
  - $0.08 for v3 and Multilingual v2, $0.04 for Flash/Turbo and v3 Conversational. Cartesia reports that the API page showed these on Oct 2, 2026. This is the newest report and is consistent with a price cut around the v4 launch (inference).
  - Planning rule: use $0.08/$0.04 as the base case and $0.10/$0.05 as the conservative case.
- Eleven v4 and v4 Turbo: launched around Sept 28, 2026 (OpenRouter shows Oct 7, so the date is not certain). List price $0.08 per 1,000 characters for v4 and $0.04 for v4 Turbo. The official API page shows a 72% launch discount (v4 at $0.022, Turbo at $0.011) until Oct 12, 2026. OpenRouter instead reports 50% off all ElevenLabs models through Oct 19. Plan on list prices, since the discount ends tomorrow. Secondary write-ups call v4 the top-ranked model on the TTS Arena leaderboard (medium-low confidence).
- Per-request character caps (one guide, medium-low confidence): Eleven v3 5,000; Multilingual v2 10,000; Flash v2.5 40,000. Another guide groups v2/v3 under 40,000, so verify. If v3 is capped at 5,000, an 8-minute episode (8,000 characters) needs at least 2 requests and a 20-minute episode at least 4, so the pipeline must chunk and stitch (inference).

### 1.3 Cost per finished minute and per episode (1,000 characters per minute)

| Route | $/1K chars (effective) | $/min | 8-min episode | 20-min episode |
|---|---|---|---|---|
| API, v3 / Multilingual v2 (conservative $0.10) | 0.100 | 0.100 | $0.80 | $2.00 |
| API, v3 / Multilingual v2 (base $0.08) | 0.080 | 0.080 | $0.64 | $1.60 |
| API, Flash/Turbo (conservative $0.05) | 0.050 | 0.050 | $0.40 | $1.00 |
| API, Flash/Turbo (base $0.04) | 0.040 | 0.040 | $0.32 | $0.80 |
| API, v4 launch promo (ends Oct 12) | 0.022 | 0.022 | $0.18 | $0.44 |
| Subscription Starter, 1 cr/char | 0.200 | 0.200 | $1.60 | $4.00 |
| Subscription Creator, 1 cr/char | 0.182 | 0.182 | $1.45 | $3.64 |
| Subscription Pro/Business, 1 cr/char | 0.165 | 0.165 | $1.32 | $3.30 |
| Subscription Scale, 1 cr/char | 0.166 | 0.166 | $1.33 | $3.32 |
| Subscription Pro/Scale/Business, Flash (0.5 cr/char) | 0.083 | 0.083 | $0.66 | $1.65 |
| Subscription Creator, Flash (0.5 cr/char) | 0.091 | 0.091 | $0.73 | $1.82 |
| Subscription, annual billing, Pro/Scale/Business, 1 cr/char | 0.138 | 0.138 | $1.10 | $2.75 |

Open point: it is not confirmed whether the API rate card is a separate pay-as-you-go product that carries the same commercial license, concurrency and voice-slot rights as a subscription. If it is, it is roughly half the price of the subscription for the same model (inference; verify with ElevenLabs sales).

### 1.4 Rights, seats, concurrency, voices

- Commercial use: Free has no commercial license; Starter and above include one (several sources agree; the official terms were not read). A free-plan attribution requirement was not verified here.
- Seats: Scale 3 and Business 10 (reported). Plans below Scale are single-seat (inference; sources list seats only from Scale up).
- Concurrency (official help-center figures, reported via search, for standard TTS such as Multilingual v2): Free 2, Starter 3, Creator 5, Pro 10, Scale 15, Business 15; Enterprise elevated. Flash is about double: Starter 6, Creator 10, Pro 20, Scale 30, Business 30. A batch pipeline is unlikely to be limited by these (inference): even 10 concurrent requests at about 10 seconds per 1,000-character chunk is about 60 finished minutes of audio per minute of wall clock.
- Professional Voice Clone (PVC) slots per official help page: Starter none (instant cloning only), Creator 1, Pro 1, Scale 3, Business 10, Enterprise by contract. One aggregator disagrees on Pro (says 10), so confirm. Extra slots are not sold as add-ons, per one guide.
- Voice Design limits and custom-voice slot counts per plan were not found (gap).

### 1.5 Text-to-Dialogue, Studio, GenFM

- Text-to-Dialogue: the Eleven v3 API has dialogue endpoints (create-dialogue and stream-dialogue) for multi-speaker audio from a script. A reseller says billing is per character consumed, so a dialogue script is charged like normal v3 text (not confirmed for the dialogue endpoint specifically). Audio tags are supported in v3. Useful for cold-case and true-crime roundtable formats.
- Studio is the long-form project editor, available from Starter upward per one source; it draws from the same credit pool.
- GenFM (auto-generated podcasts from documents): no pricing or limits found. Treat as unverified. For an API-driven, Trust-Stack-gated network, a controllable script-to-audio path (Text-to-Dialogue or plain TTS) is better than a black-box generator anyway (inference).

### 1.6 Startup grants

- The official ElevenLabs Startup Grants blog says the program is now 12 months (up from 3) with 33 million credits per recipient, described as over 680 hours of Conversational AI audio. 33M credits is about 2.75M per month. At 1 credit per character that is 33,000 finished minutes (550 hours), or 1,100 hours at Flash rates (inference). Pilot volume (about 1.25M characters per month) and the Expansion tier fit inside it.
- Terms reported: rolling review with a decision in about a week; companies with fewer than 25 employees, a real product and a monetization plan; display the "ElevenLabs Grants" logo and link for 12 months; existing enterprise customers are not eligible; projects aimed at children 18 and under are excluded (third-party listings); the plan reverts to Free at the end of the grant or when 10,000 credits remain.
- Open: whether grant credits can be spent on plain TTS for a media company (the program was marketed around Conversational AI). Apply anyway; it is cheap to try.

## 2. Alternatives

All figures at 1,000 characters per minute. "Effective $/min" for token- or second-priced engines is derived (inference).

| Engine | List price | $/1K chars | $/min | 8-min | 20-min | Free tier / notes |
|---|---|---|---|---|---|---|
| Google Cloud TTS, Chirp 3 HD | $30 per 1M chars | 0.030 | 0.030 | $0.24 | $0.60 | 1M chars/mo free |
| Google Cloud TTS, Studio | $160 per 1M | 0.160 | 0.160 | $1.28 | $3.20 | 1M free (reported) |
| Google Cloud TTS, Neural2 / Polyglot | $16 per 1M | 0.016 | 0.016 | $0.13 | $0.32 | |
| Google Cloud TTS, WaveNet / Standard | $4 per 1M | 0.004 | 0.004 | $0.03 | $0.08 | |
| Google Cloud TTS, Instant Custom Voice | $60 per 1M | 0.060 | 0.060 | $0.48 | $1.20 | |
| Gemini TTS 2.5 Flash (preview) | $0.50/1M text in, $10/1M audio out tokens | n/a | about 0.015 to 0.019 | $0.12 to $0.15 | $0.30 to $0.38 | Widely reported, unverified on Google's page |
| Gemini TTS 3.1 Flash (preview) | $1.00/1M text in, $20/1M audio out tokens; batch $10 out | n/a | about 0.030 to 0.038 | $0.24 to $0.31 | $0.60 to $0.77 | From a snippet of Google's page |
| Azure AI Speech, Neural | about $15 per 1M | 0.015 | 0.015 | $0.12 | $0.30 | 0.5M chars/mo free (F0) |
| Azure AI Speech, HD | about $22 per 1M | 0.022 | 0.022 | $0.18 | $0.44 | |
| Amazon Polly, Generative | $30 per 1M | 0.030 | 0.030 | $0.24 | $0.60 | |
| Amazon Polly, Long-Form | $100 per 1M | 0.100 | 0.100 | $0.80 | $2.00 | |
| Amazon Polly, Neural / Standard | $16 / $4 per 1M | 0.016 / 0.004 | 0.016 / 0.004 | $0.13 / $0.03 | $0.32 / $0.08 | |
| OpenAI tts-1 | $15 per 1M chars | 0.015 | 0.015 | $0.12 | $0.30 | |
| OpenAI tts-1-hd | $30 per 1M chars | 0.030 | 0.030 | $0.24 | $0.60 | |
| OpenAI gpt-4o-mini-tts | $0.60/1M text in, $12/1M audio out tokens | n/a | about 0.015 | $0.12 | $0.30 | |
| Cartesia Sonic 3 | Startup $39 to $49 for 1.25M credits; Scale $239 to $299 for 8M credits; about 1 credit per character | about 0.037 to 0.039 | about 0.037 to 0.039 | $0.30 to $0.31 | $0.75 to $0.78 | Free tier 20K to 120K credits (sources differ) |
| Hume Octave | Pro $70 for 1M chars; Scale $200 for 3.3M; Business $500 for 10M | 0.05 to 0.07 | 0.05 to 0.07 | $0.40 to $0.56 | $1.00 to $1.40 | Octave 2 reportedly about half the overage price |
| Resemble AI | Flex pay-as-you-go $0.0005 per second of audio | n/a | 0.030 | $0.24 | $0.60 | Pre-2025 list was $0.006/s ($0.36/min) |
| PlayHT / PlayAI | n/a | n/a | n/a | n/a | n/a | Meta reportedly acquired PlayAI (July 2025); service status unclear, avoid |

Vendor notes:

- Google Chirp 3 HD: best price-to-quality for commodity narration among the major clouds, with a free allowance that alone covers about 1,000 finished minutes a month. The pricing page confirms $30 per 1M characters (via snippet; July 2026 trackers agree).
- Gemini TTS: priced on tokens, not characters. Assuming 25 to 32 audio tokens per second of speech (an assumption to verify), a minute of audio is about 1,500 to 1,920 tokens. Text input adds under $0.0003 per minute. One listing gives a per-request cap of 8,000 input and 16,000 output tokens, which is about 8 to 11 minutes of audio, a natural fit for 8-minute episodes (inference). The model supports single- and multi-speaker output; the commonly cited two-speaker limit was not verified here. The 3.1 preview costs double the 2.5 preview.
- Azure: HD voices (about $22 per 1M) and standard neural (about $15 to $16) come from third-party trackers; Microsoft's own China-region page is in CNY, so US list prices need confirming.
- Polly: figures come from an auto-generated price tracker; the Long-Form tier (positioned for audiobooks and podcasts) costs over 3x the Generative tier.
- OpenAI: tts-1 and tts-1-hd are charged per character; gpt-4o-mini-tts per token (about $0.015 per minute). OpenAI's docs were inconsistent about the unit in late 2025. No newer OpenAI TTS model was found.
- Cartesia: built for low-latency voice agents; long-form podcast expressiveness is unverified. Cartesia also publishes ElevenLabs comparisons that serve its own marketing, so its ElevenLabs figures should be cross-checked.
- Hume: expressive and emotion-steerable, but priced above the hyperscalers; low fit for bulk news briefs.
- PlayHT: Meta's acquisition of PlayAI was reported in mid-2025 (Bloomberg-based coverage); one weak source claims a shutdown on Dec 31, 2025 with a contradictory timeline. Do not depend on it.
- Resemble: the latest review (June 30, 2026) shows pay-as-you-go TTS at $0.0005 per second plus a $2 per month rapid-clone add-on, but another tracker says those add-ons were removed. Low confidence on the details.

## 3. NotebookLM / Gemini Notebook

- Naming: Google's help center is reported to use "Gemini Notebook" for what was NotebookLM; both names appear.
- Audio Overview daily caps by plan (consistent across several third-party guides citing Google's upgrade page, checked July to Sept 2026): Standard (free) 3, Plus 6, Pro 20, Ultra with 20 TB 100, Ultra with 30 TB 200. Workspace "Expanded" reportedly allows 40 per day. Caps are subject to change and reset on a rolling 24 hours, not at midnight. Two sources that show 200 per day for the free tier are wrong.
- Plan prices were not verified in this pass. From memory, Google AI Pro is about $20 a month and AI Ultra about $250 a month; treat those as unverified.
- Enterprise API: NotebookLM Enterprise is a Google Cloud product (standalone, and included in some Gemini Enterprise subscriptions). A REST API (reported as v1alpha, under the Discovery Engine surface) reportedly covers notebooks, sources and audio, with a podcast endpoint; community clients (the nblm Python package and a CLI) exist. No official Google reference, quota or price was found (low confidence).
- Commercial-use terms for generated audio were not found. They must be read in Google's NotebookLM additional terms and, for paid and Enterprise use, the Cloud or Workspace terms before any use.
- Fit for Project Earlobe: poor as an automated engine. The consumer product has no controllable API, a fixed two-host format, no pronunciation or voice control, and daily caps far below network volume (a single market's daily brief would use most of a free day). Use at most as a human-in-the-loop experiment or an Enterprise-API pilot (inference).

## 4. "Meta Muse"

What it is (high confidence from multiple reports, including Meta's own announcement):

- Muse is Meta's personal AI agent, announced Sept 8, 2026 and released in the US on iOS, Android and the web. It runs long tasks for the user (email, bookings, shopping, forms) rather than only answering questions, and it expanded to small businesses on Sept 29, 2026 with Shopify, Dropbox and Slack integrations.
- It runs on the Muse model family from Meta Superintelligence Labs: Muse Spark (first model, April 2026; versions 1.2 and 1.3 later), Muse Image, Muse Video, Muse Glimmer (listed on Meta's research page, details not found) and Muse Voice Transcribe (a real-time speech-to-text model, about Sept 1, 2026, with diarization for 20+ speakers).
- Pricing for the agent: a free tier plus Power at $20 a month and Maximum at $100 a month, US only, card required. Token allowances differ by source (100M tokens a week free per a CNET quote of Zuckerberg; 500M and 3B per week for Power and Maximum per one tracker), so treat the caps as approximate.

Can it make podcast audio? No evidence that it can. Per the Meta Model API docs (via search), Muse Spark models accept audio input but produce text; Muse Voice Transcribe is speech recognition only. The consumer "voice conversations" feature is conversational speech with the assistant, not a TTS or podcast tool. No Meta text-to-speech API was found. Meta's acquisition of PlayAI (2025) suggests a future voice-generation capability, but nothing has shipped that I could find (inference).

Use for Earlobe: not a TTS engine. A possible side use is Muse Voice Transcribe in the Trust Stack as an independent transcript of finished audio, to check the audio against the script (inference); Meta Model API pricing was not found.

## 5. Cost model by volume tier

Finished minutes per month, with 1.25x billing overhead. Dollar amounts are monthly voice-generation cost only.

| Tier | Scope (assumption) | Finished min/mo | Billed chars | All-ElevenLabs subscription (full quality) | All-ElevenLabs API (v3, $0.08 to $0.10) | ElevenLabs Flash API ($0.04 to $0.05) | Google Chirp 3 HD | Gemini TTS 2.5 / 3.1 | Hybrid (20% flagship on EL API, 80% on Chirp 3 HD) |
|---|---|---|---|---|---|---|---|---|---|
| A. Pilot | 2 local markets + Breaking Desk + 1 to 2 trackers + archive | 1,000 | 1.25M | about $255 to $299 (Pro + overage or Scale) | $100 to $125 | $50 to $62 | about $8 | $19 to $24 / $38 to $48 | not worth the complexity |
| B. Expansion | 6 to 8 markets | 3,000 | 3.75M | about $990 (Business) | $300 to $375 | $150 to $188 | about $82 | $56 to $72 / $112 to $144 | about $120 |
| C. Scale | about 20 markets | 10,000 | 12.5M | about $2,060 at Business effective rate | $1,000 to $1,250 | $500 to $625 | about $345 | $188 to $240 / $375 to $480 | about $470 |
| D. Mass | 50+ markets, multi-language | 30,000 | 37.5M | about $6,190 at Business effective rate, then Enterprise discounts | $3,000 to $3,750 | $1,500 to $1,875 | about $1,095 | $562 to $720 / $1,125 to $1,440 | about $1,470 |

Flash on a subscription (0.5 credit per character) is about half the full-quality subscription cost: roughly $105 to $130 at A, $300 to $320 at B, $1,030 to $1,050 at C, $3,090 at D. Overage rates are uncertain, so those are approximate.

## 6. Recommended engine plan by volume tier

Principles: (1) Pick one engine and one voice per show and route by show, not by episode, so each show keeps a consistent sound. (2) Keep the TTS layer behind a vendor-neutral adapter with at least two live engines from day one. (3) At pilot scale, voice spend is a few hundred dollars a month at most, so choose for quality, not price. Price starts to matter above about 3,000 finished minutes a month.

- **Tier A, Pilot (about 1,000 min/mo).** Primary: ElevenLabs. Use v3 or v4 for the evergreen and narrative shows (cold case, History of Hollywood, true crime) and Flash/Turbo or v4 Turbo for the daily briefs. Prefer the API rate card if it carries commercial rights, otherwise Scale ($299) for the credits and Pro ($99) only if the briefs run on Flash. Budget about $50 to $300 a month. Apply for the Startup Grant now. Build a Google Chirp 3 HD adapter as failover and for A/B listening tests (near zero cost under the 1M free characters). Test Gemini TTS multi-speaker against ElevenLabs Text-to-Dialogue for roundtable formats. Skip NotebookLM, Muse and PlayHT for production.
- **Tier B, Expansion (about 3,000 min/mo).** Keep ElevenLabs for the 2 to 3 flagship shows (national Breaking Desk, trackers, archive). Move local daily briefs to Chirp 3 HD or Gemini 2.5 Flash TTS if blind listening tests pass. Expected spend about $120 to $400 a month hybrid, versus about $300 to $990 all-ElevenLabs. If the grant is awarded, ElevenLabs credits for this tier are effectively free for 12 months.
- **Tier C, Scale (about 10,000 min/mo).** Open an ElevenLabs Enterprise or committed-use negotiation for the flagship slice (about 20% of minutes). Run the roughly 80% commodity local minutes on Google Chirp 3 HD, Gemini TTS (use batch pricing where it exists), Azure HD or Polly Generative at $0.015 to $0.03 per minute. Expected spend about $470 to $650 a month, versus $1,000 to $2,060 all-ElevenLabs. Add a third engine as a hot spare.
- **Tier D, Mass (30,000+ min/mo).** Use a per-show router with quality tiers, committed-use discounts from Google and Azure, an ElevenLabs Enterprise contract for flagship and custom voices, and consider evaluating self-hosted open-weight TTS for the lowest tier (not researched). Expected spend about $1,500 to $3,000 a month, versus $3,000 to $6,200 all-ElevenLabs.

Content and policy notes (inference): use stock or designed voices rather than cloning real journalists; disclose AI voices in show notes; read ElevenLabs' prohibited-use policy for news and political content before launch, since it was not reviewed here.

## 7. Findings table

| Fact | Value | As-of | Source | Confidence |
|---|---|---|---|---|
| ElevenLabs Starter price and credits | $6/mo, 30,000 credits | Oct 2026 | [ElevenLabs pricing](https://elevenlabs.io/pricing), [Gradually](https://www.gradually.ai/en/elevenlabs-pricing/) | high |
| ElevenLabs Creator price and credits | $22/mo ($11 first month), 121,000 credits | Oct 2026 | [ElevenLabs pricing (fr)](https://elevenlabs.io/fr/pricing), [Gradually](https://www.gradually.ai/en/elevenlabs-pricing/) | high |
| ElevenLabs Pro price and credits | $99/mo, 600,000 credits | Oct 2026 | [Gradually](https://www.gradually.ai/en/elevenlabs-pricing/), [BigVu](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) | high |
| ElevenLabs Scale price and credits | $299/mo, 1,800,000 credits, 3 seats | Oct 2026 | [Gradually](https://www.gradually.ai/en/elevenlabs-pricing/), [Costbench](https://costbench.com/software/ai-voice-tools/elevenlabs/) | high |
| ElevenLabs Business price and credits | $990/mo, 6,000,000 credits, 10 seats | Oct 2026 | [Gradually](https://www.gradually.ai/en/elevenlabs-pricing/), [Costbench](https://costbench.com/software/ai-voice-tools/elevenlabs/) | medium-high |
| ElevenLabs Free plan | $0, 10,000 credits, no commercial license | Oct 2026 | [ElevenLabs pricing](https://elevenlabs.io/pricing) | high |
| Annual billing discount | 2 months free | Oct 2026 | [ElevenLabs pricing](https://elevenlabs.io/pricing) | high |
| Credits per character | 1 (v3, Multilingual v2); 0.5 (Flash/Turbo) | Sept 2026 | [Oakgen](https://oakgen.ai/blog/elevenlabs-pricing-limits-cost), [Texttolab](https://texttolab.com/blog/elevenlabs-pricing) | high |
| API price, v3 / Multilingual v2 | $0.10 per 1K chars (Sept 23) vs $0.08 (Oct 2) | Sept 23 to Oct 2, 2026 | [ModelsLab](https://modelslab.com/elevenlabs-api-pricing), [Cartesia](https://www.cartesia.ai/learn/elevenlabs-pricing) | medium (conflict) |
| API price, Flash/Turbo | $0.05 per 1K (Sept 23) vs $0.04 (Oct 2) | Sept 23 to Oct 2, 2026 | [ModelsLab](https://modelslab.com/elevenlabs-api-pricing), [Cartesia](https://www.cartesia.ai/learn/elevenlabs-pricing) | medium (conflict) |
| Eleven v4 price | $0.08 per 1K list; Turbo $0.04; 72% off until Oct 12, 2026 | Oct 2026 | [ElevenAPI pricing](https://elevenlabs.io/pricing/api), [OpenRouter](https://openrouter.ai/elevenlabs/eleven-v4) | medium (promo dates conflict) |
| Overage rate | about $0.30 per 1K credits Creator, $0.24 Pro (range $0.12 to $0.30) | 2026 | [HappyRobot](https://www.happyrobot.ai/hub/elevenlabs-pricing), [Smallest.ai](https://smallest.ai/blog/elevenlabs-pricing-explained-plans-limits-hidden-costs-calculator) | low |
| Concurrency by plan | Free 2, Starter 3, Creator 5, Pro 10, Scale 15, Business 15; Flash about 2x | 2026 | [ElevenLabs blog](https://elevenlabs.io/blog/ai-rate-limiting-for-voice), [help center](https://help.elevenlabs.io/hc/en-us/articles/19571824571921) | medium-high |
| PVC slots | Starter 0, Creator 1, Pro 1, Scale 3, Business 10 | 2026 | [ElevenLabs help](https://elevenlabs.io/docs/help-center/product/voice-customization/voice-cloning/how-many-professional-voice-clones-pv-cs-can-i-have) | medium |
| Per-request character caps | v3 5,000; Multilingual v2 10,000; Flash v2.5 40,000 | 2026 | [Aireiter](https://aireiter.com/blog/elevenlabs-eleven-v3-api-guide) | low-medium |
| Text-to-Dialogue | v3 dialogue endpoints; billed per character | 2026 | [Aireiter](https://aireiter.com/blog/elevenlabs-eleven-v3-api-guide), [MuAPI](https://muapi.ai/comparison/elevenlabs-text-to-dialogue-v3) | low-medium |
| Startup grant | 12 months, 33M credits, fewer than 25 employees, logo required | 2026 | [ElevenLabs blog](https://elevenlabs.io/blog/elevenlabs-startup-grants-just-got-bigger-now-12-months-and-over-680-hours-of-conversational-ai-audio), [grant page](https://elevenlabs.io/startup-grants?ref=medito) | medium-high |
| Google Chirp 3 HD | $30 per 1M chars, 1M free per month | Jul 2026 | [Google pricing](https://cloud.google.com/text-to-speech/pricing/?authuser=8), [DIYAI](https://diyai.io/ai-tools/audio-generation/google-cloud-text-to-speech-pricing/) | high |
| Google Studio / Neural2 / WaveNet-Standard / Instant Custom Voice | $160 / $16 / $4 / $60 per 1M chars | Jul 2026 | [DIYAI](https://diyai.io/ai-tools/audio-generation/google-cloud-text-to-speech-pricing/), [Costbench](https://costbench.com/software/ai-voice-tools/google-cloud-text-to-speech/) | medium-high |
| Gemini 2.5 Flash TTS preview | $0.50/1M in, $10/1M audio out | 2026 | [Maxim](https://www.getmaxim.ai/bifrost/llm-cost-calculator/provider/gemini/model/gemini-2.5-flash-preview-tts) | medium |
| Gemini 3.1 Flash TTS preview | $1.00/1M text in, $20/1M audio out; batch $10 | 2026 | [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing) | medium |
| Azure Neural / HD | about $15 / about $22 per 1M chars | 2026 | [Inventive HQ](https://inventivehq.com/tools/developer/tts-stt-api-cost-calculator), [Gradium](https://gradium.ai/content/how-to-compare-tts-pricing-across-providers-2026) | medium-low |
| Amazon Polly | $4 / $16 / $30 / $100 per 1M (Standard / Neural / Generative / Long-Form) | 2026 | [Costbench](https://costbench.com/software/voice-apis/amazon-polly-api/) | medium |
| OpenAI TTS | tts-1 $15/1M chars; tts-1-hd $30/1M chars; gpt-4o-mini-tts $0.60 in + $12 out per 1M tokens (about $0.015/min) | Jul 2026 | [CostGoat](https://costgoat.com/pricing/openai-tts), [s-anand](https://www.s-anand.net/blog/openai-tts-cost/) | medium |
| Cartesia | Startup $39 to $49 (1.25M credits), Scale $239 to $299 (8M); about 1 credit per character | May to Jul 2026 | [CloudTalk](https://www.cloudtalk.io/blog/cartesia-pricing/), [Soniox](https://soniox.com/pricing/tts/soniox-vs-cartesia) | medium-low |
| Hume Octave | Pro $70 / 1M chars, Scale $200 / 3.3M, Business $500 / 10M; Octave 2 about half overage | 2026 | [Costbench](https://www.costbench.com/software/voice-apis/hume-ai/), [UsagePricing](https://usagepricing.com/blueprint/hume-ai) | medium-low |
| Resemble | $0.0005 per second ($0.03/min) pay-as-you-go | Jun 30, 2026 | [Voiceflow](https://www.voiceflow.com/articles/resemble-ai) | low-medium |
| PlayHT / PlayAI | Meta reportedly acquired PlayAI in 2025; service status unclear | 2025 to 2026 | [Nasdaq/Bloomberg report](https://www.nasdaq.com/articles/meta-platforms-reportedly-advanced-talks-acquire-playai), [Infrabase](https://infrabase.ai/audio/playht) | low |
| NotebookLM Audio Overview caps | Free 3, Plus 6, Pro 20, Ultra 100 / 200 per day | Jul to Sept 2026 | [NotebookLM Guide](https://notebooklm-guide.com/notebooklm-audio-overview-limits/), [Superlore](https://superlore.ai/blog/notebooklm-audio-overview-daily-limit-2026) | medium |
| NotebookLM Enterprise API | REST (v1alpha) with audio and podcast endpoint; no official doc seen | 2026 | [innFactory](https://innfactory.de/en/cloud/gcp/products/notebooklm-enterprise/), [nblm](https://pypi.org/project/nblm/) | low |
| Meta Muse (agent) | Personal AI agent, launched Sept 8, 2026, US only; Power $20, Maximum $100 | Sept 2026 | [Meta](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/), [TechCrunch](https://techcrunch.com/2026/09/29/meta-is-expanding-its-ai-agent-muse-to-small-businesses/), [Layer3](https://www.layer3labs.io/guides/meta-muse-pricing) | high (tiers); medium (token caps) |
| Muse model audio | Muse Spark outputs text only; Muse Voice Transcribe is speech-to-text | Sept 2026 | [Meta Model API docs](https://dev.meta.ai/docs/models), [MarkTechPost](https://www.marktechpost.com/2026/09/01/meta-superintelligence-labs-releases-muse-voice-transcribe-one-real-time-model-for-streaming-asr-diarization-and-endpointing/) | medium-high |

## 8. Open questions / gaps

- Which ElevenLabs API rate is current ($0.08/$0.04 or $0.10/$0.05), and whether the pay-as-you-go ElevenAPI carries the same commercial license, concurrency and voice rights as a subscription. The official page could not be opened directly.
- Whether the subscription API draws credits at the same rates as the rate card (a 2x price difference otherwise).
- Overage rates per plan (sources range from $0.12 to $0.30 per 1,000 credits) and the exact rollover rule.
- ElevenLabs Voice Design limits, custom voice slots per plan, GenFM pricing, Studio per-project limits, and the Enterprise feature set.
- ElevenLabs' prohibited-use and attribution policies for news and political content, and the free-plan attribution rule.
- Whether the Startup Grant credits can be spent on TTS for a media company, and whether Project Earlobe is eligible.
- Gemini TTS: audio tokens per second (assumed 25 to 32), multi-speaker limits, and the 2.5 versus 3.1 preview status; the official 2.5 price row was not seen.
- Azure and Polly prices were taken from third-party trackers; the official US pages were not reachable.
- NotebookLM / Gemini Notebook: plan prices, commercial-use terms for generated audio, and the Enterprise podcast API's official docs, quotas and price.
- Meta: Meta Model API pricing, whether any Muse model will output speech, what "Muse Glimmer" is, and the outcome of the PlayAI acquisition.
- Search budget ran out before checking OpenAI's newest TTS models, open-weight self-hosted TTS options, and independent blind-test quality rankings across engines.

## 9. Sources

ElevenLabs
- [ElevenLabs pricing](https://elevenlabs.io/pricing)
- [ElevenLabs pricing (French page)](https://elevenlabs.io/fr/pricing)
- [ElevenAPI pricing](https://elevenlabs.io/pricing/api)
- [ElevenLabs blog: rate limiting for voice](https://elevenlabs.io/blog/ai-rate-limiting-for-voice)
- [ElevenLabs help: API error 429](https://help.elevenlabs.io/hc/en-us/articles/19571824571921)
- [ElevenLabs help: how many Professional Voice Clones](https://elevenlabs.io/docs/help-center/product/voice-customization/voice-cloning/how-many-professional-voice-clones-pv-cs-can-i-have)
- [ElevenLabs Startup Grants blog](https://elevenlabs.io/blog/elevenlabs-startup-grants-just-got-bigger-now-12-months-and-over-680-hours-of-conversational-ai-audio)
- [ElevenLabs startup grants page](https://elevenlabs.io/startup-grants?ref=medito)
- [Cartesia: ElevenLabs pricing explainer](https://www.cartesia.ai/learn/elevenlabs-pricing)
- [Gradually: ElevenLabs pricing](https://www.gradually.ai/en/elevenlabs-pricing/)
- [BigVu: ElevenLabs pricing 2026](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/)
- [Costbench: ElevenLabs](https://costbench.com/software/ai-voice-tools/elevenlabs/)
- [Texttolab: ElevenLabs pricing](https://texttolab.com/blog/elevenlabs-pricing)
- [ModelsLab: ElevenLabs API pricing](https://modelslab.com/elevenlabs-api-pricing)
- [Oakgen: ElevenLabs cost](https://oakgen.ai/blog/elevenlabs-pricing-limits-cost)
- [HappyRobot: ElevenLabs pricing](https://www.happyrobot.ai/hub/elevenlabs-pricing)
- [Smallest.ai: ElevenLabs pricing explained](https://smallest.ai/blog/elevenlabs-pricing-explained-plans-limits-hidden-costs-calculator)
- [Aireiter: Eleven v3 API guide](https://aireiter.com/blog/elevenlabs-eleven-v3-api-guide)
- [MuAPI: Text to Dialogue v3](https://muapi.ai/comparison/elevenlabs-text-to-dialogue-v3)
- [OpenRouter: Eleven v4](https://openrouter.ai/elevenlabs/eleven-v4)
- [Eesel: Eleven v4 explained](https://www.eesel.ai/blog/eleven-v4)
- [Progressive Robot: Eleven v4 tops TTS Arena](https://www.progressiverobot.com/2026/09/28/eleven-v4-turbo-elevenlabs-tops-tts-arena/)

Alternatives
- [Google Cloud Text-to-Speech pricing](https://cloud.google.com/text-to-speech/pricing/?authuser=8)
- [DIYAI: Google Cloud TTS pricing 2026](https://diyai.io/ai-tools/audio-generation/google-cloud-text-to-speech-pricing/)
- [Costbench: Google Cloud TTS](https://costbench.com/software/ai-voice-tools/google-cloud-text-to-speech/)
- [Gemini Developer API pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Maxim: Gemini 2.5 Flash preview TTS](https://www.getmaxim.ai/bifrost/llm-cost-calculator/provider/gemini/model/gemini-2.5-flash-preview-tts)
- [Inventive HQ: TTS/STT cost calculator](https://inventivehq.com/tools/developer/tts-stt-api-cost-calculator)
- [Gradium: comparing TTS pricing 2026](https://gradium.ai/content/how-to-compare-tts-pricing-across-providers-2026)
- [Azure pricing (China region)](https://www.azure.cn/en-us/pricing/details/cognitive-services/)
- [Costbench: Amazon Polly](https://costbench.com/software/voice-apis/amazon-polly-api/)
- [CostGoat: OpenAI TTS](https://costgoat.com/pricing/openai-tts)
- [s-anand: OpenAI TTS cost](https://www.s-anand.net/blog/openai-tts-cost/)
- [CloudTalk: Cartesia pricing](https://www.cloudtalk.io/blog/cartesia-pricing/)
- [Soniox: Soniox vs Cartesia](https://soniox.com/pricing/tts/soniox-vs-cartesia)
- [Costbench: Hume AI](https://www.costbench.com/software/voice-apis/hume-ai/)
- [UsagePricing: Hume AI](https://usagepricing.com/blueprint/hume-ai)
- [Nasdaq: Meta and PlayAI](https://www.nasdaq.com/articles/meta-platforms-reportedly-advanced-talks-acquire-playai)
- [Infrabase: PlayHT](https://infrabase.ai/audio/playht)
- [Voiceflow: Resemble AI](https://www.voiceflow.com/articles/resemble-ai)

NotebookLM / Gemini Notebook
- [NotebookLM Guide: Audio Overview limits](https://notebooklm-guide.com/notebooklm-audio-overview-limits/)
- [Superlore: Audio Overview daily limit](https://superlore.ai/blog/notebooklm-audio-overview-daily-limit-2026)
- [Gemini Omni Prompts: NotebookLM limits](https://geminiomniprompts.org/blog/notebooklm-limits/)
- [innFactory: NotebookLM Enterprise](https://innfactory.de/en/cloud/gcp/products/notebooklm-enterprise/)
- [nblm Python client](https://pypi.org/project/nblm/)

Meta Muse
- [Meta: Introducing Muse](https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/)
- [TechCrunch: Muse for small businesses](https://techcrunch.com/2026/09/29/meta-is-expanding-its-ai-agent-muse-to-small-businesses/)
- [CNBC: Muse for Small Business](https://www.cnbc.com/2026/09/29/meta-launches-muse-for-small-business-zuckerberg-pushes-enterprise-ai.html)
- [Meta AI research page](https://ai.meta.com/research/)
- [Meta Model API docs](https://dev.meta.ai/docs/models)
- [Layer3 Labs: Muse pricing](https://www.layer3labs.io/guides/meta-muse-pricing)
- [MarkTechPost: Muse Voice Transcribe](https://www.marktechpost.com/2026/09/01/meta-superintelligence-labs-releases-muse-voice-transcribe-one-real-time-model-for-streaming-asr-diarization-and-endpointing/)
- [The New Stack: Muse Voice Transcribe](https://thenewstack.io/meta-muse-voice-transcribe/)
