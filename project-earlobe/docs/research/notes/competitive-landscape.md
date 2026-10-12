# Competitive landscape: AI-generated audio news and automated podcast networks (2025-2026)

*Research notes for Project Earlobe (Curious & Creative Network). Compiled 2026-10-11. **Status: PARTIAL.** Read the "Research status" box before relying on any number.*

---

## TL;DR

The one competitor with hard, sourced evidence is the one Earlobe most resembles: Inception Point AI (Quiet Please), now Liquid Studios. It ran 5,000 to 15,000 shows at about $1 per episode, reached only about 69 downloads per episode, was hidden by Castro and filtered by the Podcast Index, and by 2026-09-29 was down to about 300 unmonetized shows while it pivoted to B2B. Its failure was about distribution, revenue per download and trust, not production cost. Around it sit four groups, and my picture of them rests on recall, not fresh evidence. (1) Big-tech generic AI audio: Google (Daily Listen, NotebookLM Audio Overviews), ElevenLabs (Reader, GenFM), Spotify, Audible/Amazon, and the news-reader apps Particle and Yahoo. They make audio from any text, but they are national, un-reported and unaccountable. (2) Local text and newsletter players: Patch, NewsBreak, Axios Local, Good Daily, 6AM City, Hoodline/Impress3, and local TV groups. They have local reach, but they are text-first, and the AI-heavy ones (NewsBreak, Hoodline) have documented fabrication or fake-byline scandals. (3) Public radio: the most trusted audio brand, but it is financially weakened by the 2025 federal funding rescission. (4) AI-slop feeds on Spotify, Apple and YouTube, which platforms are now filtering at roughly 25% to 46% of new podcast feeds. The Medill "State of Local News" series shows about 55% of US counties with zero or one local news source and about 3,500 newspapers lost since 2005 (recalled figures, to be verified). Neither Richland County SC nor Los Angeles County is a news desert, so Earlobe's gap is depth inside metros (municipal government, courts, neighborhoods), not absence. **Whitespace (inference): audio-first, city-level, document-grounded news with visible per-episode sourcing, a public corrections log, honest AI labeling, and court dockets as a beat.** Nobody I can identify combines those. The archive shows (Cold Case Files, History of Hollywood) face crowded human competition, so their edge is verification, not novelty. Three risks matter most: platform and vendor absorption (Google or ElevenLabs shipping "good enough" local audio), a "verified" brand that fails publicly on one wrong crime story, and name collisions (A&E's *Cold Case Files*).

---

## Research status (read first)

| Item | What happened |
|---|---|
| Web search | 0 of about 25 planned searches ran. Every call returned "budget used up" (200-call per-turn limit shared by all agents). I did not work around it with curl, wget, readers or archives. |
| Direct fetches (WebFetch) | One attempt per domain, all failed with a DNS error (ENOTFOUND): localnewsinitiative.northwestern.edu, elevenlabs.io, wondercraft.ai, en.wikipedia.org, niemanlab.org, poynter.org, techcrunch.com, axios.com, patch.com. Not retried. |
| Google Drive | One search for earlier Earlobe competitor material: no results. |
| What this file therefore contains | **Tier A**: facts carried over from sibling notes that had live search sources (Inception Point, Liquid Studios, platform rules, ad-market anchors, voice vendors). **Tier B**: analyst recall from training knowledge (cutoff mid-2026). Not verified in this session and often imprecise on numbers. **Tier C**: my inference, labeled as such. |
| How to treat Tier B | Planning context only. Do not copy a Tier B number into `docs/research/facts-and-figures.md`, a pitch, or an episode until it is checked. Source links for Tier B rows are **landing pages I did not open**, not citations of the specific claim. |
| To finish | A follow-up message can run the search list in the last section. The searches are written out and ready to send. Alternatively raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`. |

Convention: in the findings table, "(A)", "(B)" and "(C)" after the confidence word give the evidence tier.

---

## 1. Landscape map

| Segment | Players | Scale (best available) | Business model | Weakness relative to Earlobe |
|---|---|---|---|---|
| AI podcast factories | Inception Point / Quiet Please / Liquid Studios | Peak claim 10,000 to 15,000+ shows; 3,000+ episodes a week; now about 300 unmonetized shows (A) | Programmatic ads (failed); now B2B transformation fees | Delisted, unmonetized, no verification layer, fake-expert personas, glitches (A) |
| Self-serve AI audio tools | Wondercraft; also Jellypod, Podcastle, Speechify (names recalled) | Unknown (B) | SaaS subscriptions | Tools, not publishers: no sourcing, no local data, no accountability (C) |
| Voice/model vendors with consumer apps | ElevenLabs (Reader, GenFM) | Large and fast-growing vendor; valuation reportedly in the multi-billions (B) | API and subscriptions, publisher deals | Generic "turn this document into a podcast"; also Earlobe's primary voice supplier (dependency) |
| Big-tech audio news | Google Daily Listen, NotebookLM Audio Overviews; Spotify (DJ, Daily Drive, Wrapped); Amazon (Audible AI narration, Alexa+) | Platform scale (B) | Ads, subscriptions, ecosystem lock-in | National or personalized, not local; no named sources inside the audio; no courts |
| AI news-reader apps | Particle, Yahoo News (ex-Artifact) | Small to mid (B) | Ads, publisher deals | Text-first with audio add-ons; national mix |
| Publisher AI audio | Washington Post "Your Personal Podcast" (late 2025) | One publisher (B) | Subscription retention | Reported accuracy complaints; national scope |
| Local text/newsletter | Patch (AI newsletters), Axios Local, Good Daily, 6AM City | Patch: claimed expansion to tens of thousands of communities (B); Axios Local about 30+ metros (B) | Local sponsors, ads | Newsletters, not audio; AI-light versions are thin |
| Local aggregators with AI | NewsBreak; Hoodline/Impress3 | NewsBreak claimed tens of millions of monthly users (B) | Ads | Documented AI fabrication (NewsBreak) and fake AI bylines (Hoodline) (B) |
| Local TV groups | Nexstar (owns KTLA in LA), Gray, Sinclair, Tegna (WLTX Columbia, pending Nexstar deal) | Hundreds of stations combined (B) | Retrans fees, local ads | Video-first; AI used for workflow and web copy, not audio briefs (B, low) |
| Public radio / NPR | NPR member stations (SC Public Radio, LAist, KCRW) | About 1,000+ stations nationwide (B) | Donations, underwriting; federal CPB funding ended (B/A mix) | Newsroom capacity shrinking; few daily local audio briefs |
| Court / true crime | Law&Crime, Court TV, Courthouse News, local TV court reporters; no AI-native player identified | Law&Crime large on YouTube (B) | Ads, subscriptions | Focus on high-profile cases; routine local dockets underserved (C) |
| AI-slop feeds | Mass AI shows on Spotify/Apple; AI "true crime" channels on YouTube | 25% to 46% of new podcast feeds in 2026 snapshots (A) | Programmatic ads, YouTube AdSense | Platforms now filter or demonetize them |

---

## 2. Competitor profiles

### 2.1 Inception Point AI / Quiet Please / Liquid Studios (Tier A, see companion notes)

Full detail is in `inception-point-business-model.md` and `liquid-studios-pivot-and-press.md`. Facts that matter for positioning:

- **What they did:** built a fully automated network of 5,000+ shows (Sep 2025), peaking at a claimed 10,000 to 15,000+ shows and 300,000+ episodes by spring 2026. Roughly 3,000+ episodes a week, about 8 staff, about 184 agents (company claim), about $1 or less per episode, about 20 listens to break even (company claim, excludes overhead).
- **Directly in Earlobe's markets:** a *South Carolina News and Info Tracker* (295 episodes, active 2024 to 2025), LA weather, air quality and pollen shows, city crime logs. Whether these are still live is unknown (gap).
- **Scale reality:** about 12M lifetime downloads and 400K subscribers by Nov 2025, which works out to about 69 downloads per episode (derived).
- **Business model:** Spreaker programmatic ads. Wright said on 2026-09-29 that fully synthetic content is "no longer a revenue source."
- **Now:** about 300 unmonetized sandbox shows; B2B Liquid Studios sells "content transformation" for existing catalogs at a list price of about $10 per finished video minute and about $1 per audio episode (search summaries; verify on the live page).
- **Weaknesses Earlobe can exploit:** Castro hid the shows; the Podcast Index flagged or removed them; AI hosts posed with invented backstories; no published corrections policy; documented audio glitches; keyword-chasing on a shooting within about an hour; backlash from the "lazy luddites" remark.
- **What not to read into it (inference):** their failure does not show that automated local audio is unwanted. It shows that unverified, volume-first, ad-only audio is not viable. Their remnant city-level feeds (crime logs under a synthetic voice named "Agent Monday," single low-quality source) suggest the local-data format still works technically.

### 2.2 Wondercraft (Tier B)

- **What it is (recall):** a self-serve platform that turns text or prompts into podcast-style audio with AI voices, music and editing, aimed at marketers, educators and small publishers. It raised a modest seed round (amount not verified).
- **Business model:** subscription tiers (pricing not verified).
- **Weakness vs Earlobe (inference):** a tool, not a publisher. No source verification, no data pipeline for municipal or court records, no accountability for what customers publish. It is a possible vendor or a benchmark for pricing, not a rival for the same audience.
- **Evidence gap:** funding, customers, pricing and any "news" product need searching.

### 2.3 ElevenLabs: Reader and GenFM (Tier B, plus Tier A pricing in `voice-tts-costs.md`)

- **What they do:** Reader (a mobile app, launched 2024) reads articles, PDFs and ebooks aloud, including in licensed celebrity voices (recall). GenFM (launched Nov 2024 inside Reader) turns uploaded documents or links into a two-host podcast in dozens of languages (recall). ElevenLabs also sells an API, Studio, dubbing and music tools.
- **Scale:** reported valuation moved from about $3.3B (Jan 2025) to several billions more by 2026, with a large new round reported in early 2026 (recall, low confidence on the exact numbers).
- **Business model:** usage-based API and subscriptions plus enterprise and publisher deals.
- **Dual role for Earlobe (inference):** ElevenLabs is the primary voice supplier. It is also a potential competitor in "document to podcast." GenFM is a black-box generator: no sourcing control, no pronunciation control, no disclosure standard of its own. The conflict is mild now, but it strengthens the case for a tested fallback voice vendor.
- **Pricing and rights:** see `voice-tts-costs.md` (API about $0.05 to $0.10 per 1K characters; Startup Grants program, 12 months, 33M credits; GenFM pricing not found).

### 2.4 Google: Daily Listen, NotebookLM, Audio Overviews (Tier B; Tier A for caps)

- **Daily Listen (recall):** a Search Labs / Google app experiment in the US (announced mid-2025). It produces a short personalized AI audio news briefing based on the user's interests, with links to sources. Expansion status in 2026 unknown.
- **NotebookLM Audio Overviews:** launched Sept 2024; two AI hosts discuss uploaded sources; later added more formats, many languages and video overviews (recall). Daily caps in 2026: Free 3, Plus 6, Pro 20, Ultra 100 to 200 (Tier A, `voice-tts-costs.md`, third-party guides citing Google). Spotify used NotebookLM for a Wrapped podcast in Dec 2024 (recall).
- **Business model:** ecosystem and engagement; paid tiers for higher caps. No direct news revenue from these audio features.
- **Weakness vs Earlobe (inference):** national or personalized, not a local-first show; no court dockets; no published corrections or verification process; fixed host format; NotebookLM has no controllable commercial API (Tier A). A 6-to-8-minute local brief grounded in municipal documents is not what Daily Listen is built for.
- **Threat to monitor:** Google expands local signals into Daily Listen, or licenses local publisher content. That would shrink the "generic AI briefing" space fast.

### 2.5 Particle (Tier B)

- **What it is (recall):** an AI-native news-reader app founded by former Twitter engineers (Sara Beykpour, Marcel Molina), launched 2024 and venture-backed (reported low-eleven-million-dollar Series A; verify). Features include AI story summaries, multi-perspective views, and publisher revenue arrangements. Whether it has an audio mode in 2026 needs checking.
- **Naming trap (recall, medium):** NewsBreak's parent company is "Particle Media Inc.," which is unrelated to the Particle app. Check names before citing either.
- **Weakness vs Earlobe (inference):** national aggregation, text-first, no hyperlocal depth.

### 2.6 Yahoo News AI audio (Tier B, thin)

- **What I recall:** Yahoo bought the Artifact news app (Apr 2024) and folded its AI summarization into the Yahoo News app; Yahoo has added AI "key takeaways." I could not recall specifics on AI audio or a podcast product.
- **Weakness vs Earlobe (inference):** broad national feed. Yahoo's local coverage depends on syndication.
- **Evidence gap:** audio product details, scale and monetization are all unverified.

### 2.7 Spotify (Tier B and A)

- **AI features (recall):** AI DJ (2023), voice-translation pilot for podcasts (2023), Daily Drive (news and music mix), accepts ElevenLabs-narrated audiobooks (2025), AI disclosure and spam rules for music (Sept 2025).
- **Policy that matters (Tier A):** "Verified by Spotify" badges for podcasts and removal of shows that impersonate a creator (2026-05-19). No blanket AI ban, and reportedly no mandatory podcast AI disclosure rule.
- **Role:** gatekeeper and distributor more than competitor. The threat is a personalized AI news mix inside the app, which I could not confirm.
- **Weakness vs Earlobe (inference):** generates no original local reporting.

### 2.8 Audible / Amazon (Tier B and A)

- **AI narration (recall):** Audible announced AI narration and translation tools for publishers in 2025. Audible also carried Inception Point shows as "Audible Books & Originals" (Tier A).
- **Corporate context (Tier A):** Amazon reorganized Wondery in Aug 2025 (about 110 jobs cut), moved narrative shows to Audible, and Wright had already left.
- **Alexa+ (recall, low):** includes news summaries from publishers.
- **Weakness vs Earlobe (inference):** book-centric; no local news products identified.

### 2.9 Publisher AI audio: Washington Post "Your Personal Podcast" (Tier B, low)

- **What I recall:** the Post launched AI-generated personalized podcasts in its app in late 2025, and trade press reported accuracy complaints from inside the building, including misattributed or invented details.
- **Why it matters (inference):** even a top newsroom with a verification culture shipped an AI audio product that drew accuracy criticism. A verified-audio claim needs published proof, not just a pipeline.

### 2.10 Local news players

| Player | What they do (Tier B unless stated) | Scale | Model | Weakness vs Earlobe (inference) |
|---|---|---|---|---|
| **Patch** | Hyperlocal news sites; in 2025 announced AI-generated newsletters to cover a very large number of US communities (about 30,000 reported) with human oversight | Claimed expansion from about 1,000+ communities to tens of thousands | Local ads and sponsors | Text newsletters, no audio; quality of AI-generated local copy unproven |
| **NewsBreak** | Largest local-news aggregator app (tens of millions of monthly users claimed); a Reuters investigation (Dec 2024) reported AI-generated erroneous local stories | Very large reach | Ads | Documented fabrication; trust damage; Chinese-origin ownership scrutiny |
| **Axios Local** | Human-reported newsletters in about 30+ metros; owned by Cox Enterprises (Axios bought for about $525M in 2022) | About 30+ cities | Local sponsors, ads | Text; limited metros; whether it covers Columbia or LA needs checking |
| **Good Daily** | Local newsletter network (details not reliably recalled) | Unknown | Ads | **Evidence gap** |
| **6AM City** | Local newsletter network in mid-size US cities | Unknown | Ads, sponsors | **Evidence gap.** Check whether it covers Columbia SC |
| **Hoodline / Impress3** | Local news sites that published stories under AI-generated "journalist" personas with fake bylines (reported 2023 to 2024); labels were added after criticism | Dozens of metros claimed | Ads | Fake bylines are the template for what Earlobe must not do |
| **Local TV groups** | Nexstar (KTLA, LA; announced $6.2B Tegna purchase in Aug 2025, which would add WLTX Columbia, status to verify), Gray (likely WIS Columbia), Sinclair. AI used for workflow, web copy, clips | Hundreds of stations | Retrans, ads | Video-first; no verified-audio brief; but own the local-news habit |
| **Futuri RadioGPT-style local radio AI** | AI-voiced local radio segments (2023 launch, recall) | Pilot-level | Radio ads | Unclear current traction |

### 2.11 Public radio / NPR local (Tier B, one Tier A hook)

- **Strength:** the most trusted audio brand; flagship daily brief *Up First*; local stations such as SC Public Radio (Columbia), LAist and KCRW (LA).
- **Funding shock (recall, medium-high):** Congress rescinded about $1.1B in Corporation for Public Broadcasting funding in July 2025; CPB announced a wind-down, and stations have announced cuts. Effect on specific Columbia and LA stations needs checking.
- **Weakness vs Earlobe (inference):** shrinking local capacity and few daily municipal-level audio briefs. Opportunity for partnership or syndication, but expect public-media staff to be cautious about AI.
- **Ad-market note (Tier A):** no current daily-brief ranking was retrieved; see `ad-market-and-audience.md`.

### 2.12 AI court and true-crime (Tier B; absence finding)

- **AI-native court or true-crime podcast startups:** none identified with traction. Because search was unavailable, treat this as "not found," not "does not exist."
- **Human incumbents:** Law&Crime Network (large YouTube presence), Court TV (Scripps), Courthouse News Service (wire), local TV court reporters, and true-crime audio giants such as *Crime Junkie*. All are human-made.
- **AI-slop true crime (recall, low):** YouTube channels with AI-fabricated "true crime" cases were reported in 2025. That is the trust problem a verified court show can contrast with.
- **Inception Point crime logs (Tier A):** city crime reports (for example Fresno) were templated blotter readouts. They are the nearest AI-native precedent, and they carry defamation risk because blotter entries name people.
- **Name collision (recall, high confidence the TV show exists):** *Cold Case Files* is an established A&E television title. Run a trademark search before launching a podcast under that name.
- **Whitespace (inference):** routine local dockets (sentencings, civil judgments, verdicts) are covered thinly by shrinking newsrooms and are not served by national true-crime shows.

### 2.13 AI-slop networks on Spotify / Apple / YouTube (Tier A mostly)

- **Share of new feeds:** 39% (Bloomberg/Podcast Index, 9 days, 4,243 of 10,871); 45.7% possibly AI (Podnews 24-hour snapshot); Listen Notes about 31.5% of Aug 2026 submissions; Forbes about 25%. Plan on a 25% to 45% range.
- **Platform responses (Tier A):** Castro hid Inception Point; Podcast Index `/recent/problematic` flags; Spotify Verified badges and impersonation takedowns (2026-05-19); Apple requires prominent AI disclosure; iHeart's "Guaranteed Human" pledge (2025-11).
- **YouTube (Tier A via `hosting-and-monetization-platforms.md`, policy text unread):** July 2025 "inauthentic content" monetization policy targets mass-produced, repetitive content.
- **Other AI news-farm context (recall, low):** NewsGuard counted well over a thousand AI-generated "news" sites by 2025, and partisan "pink slime" sites reportedly outnumbered daily newspapers in 2024.

---

## 3. The local news gap (Medill State of Local News)

**Source:** Northwestern University Medill Local News Initiative, annual "State of Local News" report. The series is published each fall. The 2026 edition has probably not been published yet as of 2026-10-11 (inference from past cadence).

**All numbers in this table are Tier B recall and must be verified before use.** Ranges show my uncertainty.

| Metric | 2023 report | 2024 report | 2025 report | Confidence |
|---|---|---|---|---|
| Counties with no local news source ("news deserts") | about 204 | about 206 | about 213 | low |
| Counties with only one local source | about 1,560 | about 1,560 | about 1,520 | low |
| People in deserts or with limited access | about 70M (older series) | about 55M | about 50M | low |
| Newspapers lost since 2005 | about 2,900 | about 3,200 to 3,300 | about 3,500 | low-medium |
| Closures in the past year | about 130 | about 127 | about 136 | low |

**Derived (inference):** (206 + 1,561) / 3,143 US counties is about 56% of counties with zero or one local news source in 2024, and about 55% on the 2025 recall. The pace is about 2.5 newspaper closures per week. Direction of travel (more losses, slow growth in digital startups) is more reliable than any single count.

**Implications for Earlobe's two test markets (inference):**
- **Los Angeles County and Richland County SC are not news deserts.** Both have several outlets. The gap is depth: municipal meetings, school boards, courts and neighborhoods, especially in audio.
- **Columbia SC:** a mid-size market with consolidated ownership (the main daily, *The State*, is part of a large chain; TV is dominated by group-owned stations). The nearest news-desert counties are in rural SC. A Columbia brief can show the gap more clearly than LA. Verify county-level and state-level figures from the Medill state pages (gap).
- **Los Angeles:** abundance, not scarcity, so differentiation must come from format (audio), verification, and the courts and Hollywood-history angles.
- **Philanthropy (recall, low):** Press Forward and similar funds put money into human local newsrooms, which are potential partners and rival applicants for grants.

---

## 4. Trust-deficit evidence (why "verified" can be the wedge)

| Incident or study | What happened | As-of | Tier / confidence |
|---|---|---|---|
| Apple AI notification summaries | Apple paused AI summaries for news apps in early 2025 after publisher complaints (BBC) about false headlines | Jan 2025 | B, medium-high |
| EBU/BBC study of AI assistants | Found that a large share of AI assistant answers about news had at least one significant issue (about 45% reported) | Oct 2025 | B, medium |
| NewsBreak | Reuters reported AI-generated false local stories | Dec 2024 | B, medium |
| Hoodline / Impress3 | AI personas with fake bylines on local stories | 2023 to 2024 | B, medium |
| Washington Post personalized AI podcast | Accuracy complaints reported | Late 2025 | B, low |
| Inception Point | Glitches, groans, repeated words in a sample of 19 episodes; keyword-chasing on a shooting; legacy health shows with bad information | 2025 to 2026 | A, medium-high |
| Reuters Institute Digital News Report 2025 | Weekly use of AI chatbots for news was small (about 7% overall, higher among young people); audiences expected AI to make news cheaper but less trustworthy | Jun 2025 | B, low-medium |

**Inference:** consumers and publishers have seen enough failures that a visible verification layer is a differentiator. But one public failure would turn the claim into the story, so the claim must be backed by published metrics (see section 5).

---

## 5. Whitespace and positioning

### 5.1 Capability matrix (inference, coarse)

"Y" = clearly offers it, "P" = partly, "N" = not offered, "?" = unknown. Based on Tier A and Tier B evidence. Treat as a hypothesis to test.

| Player | Hyperlocal (city or municipal) | Audio-first | Visible per-episode sourcing | Courts / dockets | Evergreen archive | Clear AI disclosure | Corrections log |
|---|---|---|---|---|---|---|---|
| Inception Point (past) | P (templated data) | Y | N | P (crime logs) | P (biographies) | P (closing line) | N |
| Google Daily Listen / NotebookLM | N | Y | P (links) | N | N | P | N |
| ElevenLabs GenFM | N | Y | N | N | N | ? | N |
| Particle / Yahoo | N | P | P | N | N | P | ? |
| NewsBreak | P | N | N | N | N | ? | ? |
| Patch | Y | N | P | N | N | ? | ? |
| Axios Local | Y (30+ metros) | N | P | N | N | n/a | Y |
| Local TV groups | Y | N (video) | N | P | N | n/a | Y |
| Public radio | P | Y | P | N | N | n/a | Y |
| Law&Crime / Court TV | N | P (video) | P | P (high-profile) | N | n/a | ? |
| **Earlobe (target)** | **Y** | **Y** | **Y** | **Y** | **P** | **Y** | **Y** |

### 5.2 Positioning statement (draft, inference)

"Local audio news you can check. Every claim is matched to at least two independent sources (three for breaking news), every episode says it is AI-made, and every correction is public."

The editorial standards already promise this. The research adds three conditions:

1. **Publish proof, not just promises.** Show a public verification scorecard: claims checked, claims dropped, corrections issued, hold and kill rates. A "verified" brand with no numbers reads like marketing.
2. **Own the record.** The standards say no person reads each episode. That is defensible only with a named, accountable editor of record and a fast correction path. This is a business decision for the founder, not something this research can settle.
3. **Never use "first" or "only" in a claim.** I could not search, so I cannot prove absence. Use "built to be checked."

### 5.3 Whitespace by show (inference)

| Earlobe show | Competitive picture | Whitespace | Risk |
|---|---|---|---|
| Columbia Daily | Few audio local briefs; Inception Point's SC tracker may still be listed; TV and a daily paper dominate | Municipal-level, audio-first, sourced brief for a mid-size metro | Local officials and sources are used to human reporters; thin audience at launch |
| LA Daily | Crowded: LA Times, LAist, KCRW, TV, many neighborhood outlets | Format (6 to 8 minute verified brief) and city-agency documents | Hardest to differentiate; do not lead with LA as the proof |
| LA Courts Roundup / Case Tracker | Human high-profile court coverage; no AI-native rival found | Routine docket coverage in audio, with primary-document citations | Highest defamation and privacy exposure; strict lane is essential |
| The Breaking Desk | Giant, fast, human-branded competition | Only a slower, three-source "confirmed" flash, which is a trust niche rather than a speed play | Hold-and-kill rules cost speed; do not compete on "first" |
| Cold Case Files | Crowded true-crime market; A&E title collision | Primary-source, no-fabrication cold cases with source lists | Trademark; victims' families; fabricated-case scandals set a high bar |
| History of Hollywood | Crowded human podcast niche | Archive transformation and verified sourcing; potential B2B line | Low differentiation; treat as evergreen volume and a B2B proof of concept |

### 5.4 Strategic moves worth testing (inference)

1. **Lead with Columbia and the courts,** where the competition is weakest and the verification story is easiest to prove.
2. **Partner, don't scrape.** Credit and link local outlets, seek licenses or syndication, and consider public-radio partnerships. This answers the "free rider" critique and any copyright exposure.
3. **Launch few feeds, at a human-plausible cadence, with honest titles.** This avoids the Castro / Podcast Index treatment (Tier A).
4. **Second-source the voice vendor** and keep model-agnostic orchestration, because Inception Point's CEO called single-model reliance "extremely risky" (Tier A).
5. **Keep a B2B option.** Liquid Studios' $10 per video minute and about $1 per audio episode are price anchors. Earlobe's pipeline could serve local publishers' archives (inference).
6. **Check names first:** *Cold Case Files* (A&E), plus *Columbia Daily* and *LA Daily* (existing papers with similar names). Do a trademark and app-store search.

### 5.5 Threats to watch

- Google or Spotify adding local signals to AI audio briefings.
- ElevenLabs productizing "local news GenFM" or signing local publisher partnerships.
- Public radio or local TV groups launching their own AI-assisted audio briefs (Nexstar after the Tegna deal is the one to watch).
- A platform rule that treats all fully automated news audio as low quality regardless of verification (Spotify Verified criteria, Apple enforcement).
- A defamation or accuracy incident in the court or crime lane.

---

## Findings table

Evidence tiers: (A) carried over from sibling notes with live sources, (B) analyst recall, unverified this session, (C) inference. Rows marked (B) must not be copied into outward-facing material until checked.

| Fact | Value | As-of | Source | Confidence |
|---|---|---|---|---|
| Inception Point shows at launch | 5,000+ shows; 3,000+ episodes a week; about $1 per episode; about 8 staff | 2025-09 | [Hollywood Reporter](https://www.hollywoodreporter.com/business/digital/ai-podcast-start-up-plan-shows-1236361367/) | high (A) |
| Inception Point peak claim | 10,000 to 15,000+ shows; 300K+ episodes | 2026-04 to 2026-09 | [Podnews](https://podnews.net/update/inception-point-pr-stunt); [Freakonomics Ep. 690](https://freakonomics.com/podcast/its-show-business-baby/) | medium (A) |
| Lifetime downloads and subscribers | 12M downloads; 400K subscribers; about 69 downloads per episode (derived) | 2025-11 | [TheWrap](https://www.thewrap.com/ai-podcasts-hosts-inception-point-ai/) | medium (A) |
| Quiet Please today | About 300 active shows, not monetized; AI hosts retired | 2026-09-29 | [Podnews](https://podnews.net/update/inception-point-pr-stunt) | high (A) |
| Liquid Studios pricing | About $10 per finished video minute; about $1 per audio episode | 2026-10 | [Liquid Studios](https://liquidstudios.ai/) | medium (A, via search summaries) |
| Liquid Studios customers | None named | 2026-10-11 | n/a | gap (A) |
| Inception Point SC and LA feeds | *South Carolina News and Info Tracker* (295 eps), LA weather/AQI, Fresno crime log; current status unknown | 2025 to 2026 | [Apple Podcasts](https://podcasts.apple.com/gb/podcast/south-carolina-news-and-info-tracker/id1757689268) | medium (A) |
| Castro action | Hid Inception Point shows from search and charts | late 2025 | [Castro](https://castro.fm/blog/hiding-inception-point-ai) | medium-high (A) |
| AI share of new podcast feeds | 39% (4,243 of 10,871 in 9 days); other trackers 25% to 46% | 2026-04/05 | [TechRadar](https://www.techradar.com/audio/podslop-is-a-real-and-growing-problem-data-shows-39-percent-of-new-podcasts-are-now-likely-generated-by-ai-heres-why-i-wont-be-listening); [Podnews](https://podnews.net/update/ai-slop-overtakes-humans) | medium-high (A) |
| Spotify rule | Verified badges; removes impersonation incl. AI voice clones; no blanket AI ban | 2026-05-19 | [Variety](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/) | high (A) |
| Apple rule | Requires prominent AI disclosure in audio and metadata; enforcement not evident | 2026 | [Apple Podcasts guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines) | medium-high (A) |
| iHeartMedia "Guaranteed Human" | No AI on-air voices on its radio or the podcasts it publishes | 2025-11 | [Radio Ink](https://radioink.com/?p=97798) | high (A) |
| Typical podcast CPM | About $17 to $22; programmatic $12 to $15; DAI $18 to $22 | 2026 | [Freakonomics](https://freakonomics.com/podcast/its-show-business-baby/); [Podder](https://www.podderapp.com/post/podcast-cpm-rates-2026) | medium (A) |
| Amazon / Wondery reorganization | About 110 jobs cut; narrative shows moved to Audible | 2025-08 | [Variety](https://au.variety.com/2025/biz/news/amazon-reorganizes-audio-wondery-audible-jen-sargent-exit-26111) | medium (A) |
| NotebookLM Audio Overview daily caps | Free 3, Plus 6, Pro 20, Ultra 100 to 200 | 2026-07 to 09 | [NotebookLM Guide](https://notebooklm-guide.com/notebooklm-audio-overview-limits/) | medium (A) |
| ElevenLabs API TTS price | About $0.05 to $0.10 per 1K characters | 2026-06 to 08 | [Puter](https://developer.puter.com/tutorials/elevenlabs-api-pricing/) | medium (A) |
| ElevenLabs GenFM | Two-host podcast from documents; launched in Reader, Nov 2024; pricing not found | 2024-11 | [ElevenLabs Reader](https://elevenlabs.io/reader) (landing page, not opened) | low (B) |
| ElevenLabs valuation | About $3.3B in Jan 2025; reportedly several times higher by early 2026 | 2025 to 2026 | [ElevenLabs](https://elevenlabs.io/) (landing page, not opened) | low (B) |
| Google Daily Listen | Personalized short AI audio news briefing, US Search Labs | 2025-06 | [Google blog](https://blog.google/products/search/) (landing page, not opened) | low-medium (B) |
| NotebookLM Audio Overviews | Launched Sept 2024; two AI hosts; later formats and languages | 2024-09 | [NotebookLM](https://notebooklm.google/) (landing page, not opened) | medium (B) |
| Particle app | Founded by ex-Twitter engineers; launched 2024; unrelated to NewsBreak's parent Particle Media Inc. | 2024 to 2025 | [Particle](https://particle.news/) (landing page, not opened) | low-medium (B) |
| Yahoo News AI | Acquired Artifact Apr 2024; AI summaries; audio details unknown | 2024 to 2026 | [Yahoo News](https://news.yahoo.com/) (landing page, not opened) | low (B) |
| Spotify AI features | DJ (2023), voice translation pilot, Daily Drive; Sept 2025 AI-music disclosure and spam policy | 2023 to 2025 | [Spotify newsroom](https://newsroom.spotify.com/) (landing page, not opened) | low-medium (B) |
| Audible AI narration | Announced AI narration and translation tools for publishers | 2025 | [Audible](https://www.audible.com/) (landing page, not opened) | low-medium (B) |
| Wondercraft | Self-serve AI podcast/audio platform; funding and customers unverified | 2026 | [Wondercraft](https://www.wondercraft.ai/) (landing page, not opened) | low (B) |
| Patch AI newsletters | Plan to cover about 30,000 communities with AI newsletters | 2025 | [Patch](https://patch.com/) (landing page, not opened) | low (B) |
| NewsBreak AI errors | Reuters reported AI-generated false local stories | 2024-12 | [Reuters](https://www.reuters.com/) (landing page, not opened) | low-medium (B) |
| Axios Local | About 30+ metros; Cox bought Axios for about $525M | 2022 to 2025 | [Axios Local](https://local.axios.com/) (landing page, not opened) | low-medium (B) |
| Hoodline / Impress3 | AI personas with fake bylines on local stories | 2023 to 2024 | [Hoodline](https://hoodline.com/) (landing page, not opened) | low-medium (B) |
| Good Daily; 6AM City | Local newsletter networks; details and coverage of Columbia/LA unverified | 2026 | [6AM City](https://6amcity.com/) (landing page, not opened) | low (B) |
| Nexstar / Tegna | $6.2B Tegna purchase announced Aug 2025; Nexstar owns KTLA; status of deal unverified | 2025-08 | [Nexstar](https://www.nexstar.tv/) (landing page, not opened) | low-medium (B) |
| CPB funding | About $1.1B rescinded July 2025; CPB wind-down announced Aug 2025 | 2025 | [CPB](https://cpb.org/) (landing page, not opened) | medium (B) |
| Medill: news-desert counties | About 204 (2023), 206 (2024), 213 (2025) | 2023 to 2025 | [Medill Local News Initiative](https://localnewsinitiative.northwestern.edu/projects/state-of-local-news/) (landing page, not opened) | low (B) |
| Medill: one-source counties | About 1,560 (2023, 2024), about 1,520 (2025) | 2023 to 2025 | same | low (B) |
| Medill: people with limited or no access | About 55M (2024); about 50M (2025) | 2024 to 2025 | same | low (B) |
| Medill: newspapers lost since 2005 | About 3,200 to 3,300 (2024); about 3,500 (2025); about 2.5 closures per week | 2024 to 2025 | same | low-medium (B) |
| Counties with zero or one source (derived) | About 55% to 56% of 3,143 US counties | 2024 to 2025 | derived from rows above | low (C) |
| Medill 2026 report | Likely not yet published as of 2026-10-11; expect fall 2026 | 2026-10 | inferred from past cadence | low (C) |
| BBC/EBU AI-assistant news study | About 45% of answers had a significant issue | 2025-10 | [EBU](https://www.ebu.ch/) (landing page, not opened) | low-medium (B) |
| Reuters Institute DNR 2025 | About 7% weekly AI-chatbot use for news | 2025-06 | [Reuters Institute](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025) (landing page, not opened) | low-medium (B) |
| A&E *Cold Case Files* | Established TV title; possible naming conflict | n/a | [A&E Networks](https://www.aenetworks.com/) (landing page, not opened) | medium (B) |
| AI-native court/true-crime startups | None identified (search not run) | 2026-10-11 | n/a | gap |
| Whitespace | Audio-first, city-level, document-grounded, visibly sourced, with courts as a beat; no player found that combines these | 2026-10-11 | analyst synthesis | low-medium (C) |

---

## Open questions / gaps

**Not done because search was unavailable:**
- **Medill 2025 report:** confirm exact 2025 counts (news deserts, one-source counties, people affected, newspapers lost, closures, digital startups, pink-slime sites), plus the **South Carolina** and **California** state pages and the **Richland County SC** and **Los Angeles County** county profiles. Check whether a 2026 edition is out.
- **Wondercraft:** funding, customers, pricing, any news or publisher product.
- **ElevenLabs:** current valuation and revenue; Reader and GenFM scale, languages, publisher deals; whether GenFM has an API or pricing; any local-news initiative.
- **Google:** Daily Listen status in 2026 (expansion, local content, publisher licensing); NotebookLM commercial-use terms.
- **Particle and Yahoo:** whether either has an audio product; Yahoo News AI audio specifics.
- **Spotify and Audible/Amazon:** any 2026 AI news-audio launch; Spotify Verified criteria for AI-labeled shows; Alexa+ news.
- **Local players:** Patch AI newsletter results; NewsBreak's current state and Reuters findings; Axios Local city list (Columbia? LA?); Good Daily and 6AM City facts and coverage; Hoodline/Impress3 status; Nexstar-Tegna closing and any AI audio plans at Nexstar, Gray, Sinclair.
- **Public radio:** post-CPB status of SC Public Radio, LAist and KCRW; any AI policy or partnership appetite; local daily podcasts in both markets.
- **Court / true crime:** any AI-native entrant; Law&Crime and Court TV audience figures; AI-fabricated true-crime YouTube channels.
- **Naming:** trademark search for *Cold Case Files*, *Columbia Daily*, *LA Daily*, *Case Tracker*.
- **Inception Point's SC and LA feeds:** still live? Same directory keywords.

**Conflicts to resolve:** Medill 2025 counts (my recall differs between "about 213" and nearby values); Inception Point's entity name and founding year (from sibling notes).

### Ready-to-run search list for a follow-up (suggested modes)

1. `Medill State of Local News 2025 news deserts counties report` (extended)
2. `Medill State of Local News South Carolina Richland County` and `... Los Angeles County` (standard)
3. `Northwestern Local News Initiative 2026 report` (standard)
4. `ElevenLabs GenFM Reader app users publishers 2026` (extended)
5. `ElevenLabs valuation ARR 2026` (standard)
6. `Google Daily Listen AI audio news 2026 expansion` (extended)
7. `Wondercraft AI funding customers` (standard)
8. `Particle news app audio podcast 2026` (standard)
9. `Yahoo News AI audio podcast Artifact 2026` (standard)
10. `Spotify AI news podcast Daily Drive 2026` (standard)
11. `Audible AI narration publishers 2025 2026` (standard)
12. `Washington Post "Your Personal Podcast" AI errors` (extended)
13. `Patch AI newsletters 30,000 communities` (extended)
14. `NewsBreak AI-generated stories Reuters investigation` (standard)
15. `Axios Local cities list Columbia Los Angeles` (standard)
16. `Good Daily local newsletter` and `6AM City cities` (standard)
17. `Hoodline Impress3 AI bylines` (standard)
18. `Nexstar Tegna merger status KTLA WLTX AI` (extended)
19. `Gray Sinclair local TV AI news production 2026` (extended)
20. `CPB shutdown public radio stations South Carolina Los Angeles layoffs` (extended)
21. `AI podcast true crime court cases startup` (extended)
22. `Law&Crime Network audience 2026; Court TV podcast` (standard)
23. `AI-generated true crime YouTube fabricated cases` (standard)
24. `YouTube inauthentic content policy July 2025 AI channels` (standard)
25. `BBC EBU study AI assistants news accuracy` and `Reuters Institute Digital News Report 2026 AI` (standard)

---

## Sources

Sourcing rule for this file: links under "Opened in earlier research" were found through live searches in the sibling notes. Links under "Landing pages not opened" are canonical sites I recall; they support the existence of the entity or topic only and are **not** citations for the specific numbers in this file.

**Opened in earlier research (via sibling notes)**
- [Hollywood Reporter: 5,000 Podcasts. 3,000 Episodes a Week. $1 Cost Per Episode (Sep 2025)](https://www.hollywoodreporter.com/business/digital/ai-podcast-start-up-plan-shows-1236361367/)
- [Podnews: Was Inception Point AI just a PR stunt? (2026-09-29)](https://podnews.net/update/inception-point-pr-stunt)
- [Podnews: More new AI-generated podcasts than human ones (about Apr 2026)](https://podnews.net/update/ai-slop-overtakes-humans)
- [TheWrap: An AI Podcasting Machine Is Churning Out 3,000 Episodes a Week](https://www.thewrap.com/ai-podcasts-hosts-inception-point-ai/)
- [Lead Balloon Ep. 73: pivot and rebrand as Liquid Studios (2026-09-29)](https://www.podcampmedia.com/post/lead-balloon-ep-73-ai-podcast-hosts-scrapped-inception-point-ceo-jeanine-wright-explains-pivot)
- [Liquid Studios homepage](https://liquidstudios.ai/)
- [Freakonomics Radio Ep. 690: It's Show Business, Baby! (2026-10-09)](https://freakonomics.com/podcast/its-show-business-baby/)
- [Castro: Hiding Inception Point AI Spam](https://castro.fm/blog/hiding-inception-point-ai)
- [TechRadar: 39% of new podcasts likely AI (2026-05-10)](https://www.techradar.com/audio/podslop-is-a-real-and-growing-problem-data-shows-39-percent-of-new-podcasts-are-now-likely-generated-by-ai-heres-why-i-wont-be-listening)
- [Variety: Spotify bans AI impersonation podcasts, adds verified badges (2026)](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/)
- [Apple Podcasts for Creators: content guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines)
- [Radio Ink: iHeartMedia draws line against AI voices](https://radioink.com/?p=97798)
- [Podder: Podcast CPM rates 2026](https://www.podderapp.com/post/podcast-cpm-rates-2026)
- [Variety: Amazon reorganizes audio; Wondery moves to Audible (2025)](https://au.variety.com/2025/biz/news/amazon-reorganizes-audio-wondery-audible-jen-sargent-exit-26111)
- [NotebookLM Guide: Audio Overview limits](https://notebooklm-guide.com/notebooklm-audio-overview-limits/)
- [Puter: ElevenLabs API pricing breakdown (Jun 2026)](https://developer.puter.com/tutorials/elevenlabs-api-pricing/)
- [Apple Podcasts: South Carolina News and Info Tracker](https://podcasts.apple.com/gb/podcast/south-carolina-news-and-info-tracker/id1757689268)
- Companion notes in this folder: `inception-point-business-model.md`, `liquid-studios-pivot-and-press.md`, `voice-tts-costs.md`, `ad-market-and-audience.md`, `hosting-and-monetization-platforms.md`

**Landing pages not opened (recall, existence only)**
- [Medill Local News Initiative: State of Local News](https://localnewsinitiative.northwestern.edu/projects/state-of-local-news/)
- [ElevenLabs Reader](https://elevenlabs.io/reader)
- [ElevenLabs](https://elevenlabs.io/)
- [Wondercraft](https://www.wondercraft.ai/)
- [Google Search blog](https://blog.google/products/search/)
- [NotebookLM](https://notebooklm.google/)
- [Particle](https://particle.news/)
- [Yahoo News](https://news.yahoo.com/)
- [Spotify newsroom](https://newsroom.spotify.com/)
- [Audible](https://www.audible.com/)
- [Patch](https://patch.com/)
- [Axios Local](https://local.axios.com/)
- [6AM City](https://6amcity.com/)
- [Hoodline](https://hoodline.com/)
- [Reuters](https://www.reuters.com/)
- [Nexstar](https://www.nexstar.tv/)
- [Corporation for Public Broadcasting](https://cpb.org/)
- [EBU](https://www.ebu.ch/)
- [Reuters Institute Digital News Report 2025](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2025)
- [A&E Networks](https://www.aenetworks.com/)
