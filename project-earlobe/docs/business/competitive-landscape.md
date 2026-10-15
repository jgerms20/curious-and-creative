# Competitive landscape: who else is doing this, and where we win

**The Curious & Creative Network · as of 2026-10-12 · DRAFT for Joshua and Janel.** Built from the [competitive research note](../research/notes/competitive-landscape.md), the [Liquid Studios pivot note](../research/notes/liquid-studios-pivot-and-press.md) and the [facts sheet](../research/facts-and-figures.md) (IDs like `F-IPA-01`). Company figures are unaudited. Our own reasoning is marked *(inference)*.

**Evidence tags.** **A** = sourced in earlier live research. **B** = analyst recall, no page was opened: planning context only, do not quote outside the company until checked. **C** = our inference. Every search and page fetch for this topic was blocked or used up, so a follow-up pass with search on should clear every B row (list in section 9).

## The 30-second version

| | |
|---|---|
| **Closest rival** | Inception Point AI (Quiet Please), now Liquid Studios. It ran a claimed 10,000 to 15,000+ AI shows, averaged about 69 downloads per episode, was hidden or flagged by Castro and the Podcast Index, and by 2026-09-29 was down to about 300 unmonetized shows (F-IPA-01, -07, -10). |
| **Why it failed** | Distribution, revenue per download and trust, not production cost *(inference)*. That does not prove automated local audio is unwanted. It shows unverified, volume-first, ad-only audio is not viable. |
| **Everyone else** | Big tech makes audio from any text but is national and unaccountable. Local news players are text or video first. Public radio is trusted but shrinking. No AI-native court or crime show with traction was found (B; "not found" is not "does not exist"). |
| **Whitespace** *(inference)* | Audio-first, city-level, document-grounded news with visible sourcing, a public corrections log, honest AI labeling and court dockets as a beat. Nobody found combines these. |
| **Honest catch** | Verification costs us roughly 5x to 20x more per episode than they spent (F-LLM-08), and ads alone lose about $1.5 to $2.1 on a local brief (facts sheet, "Model assumptions"). We win only if "verified" earns sponsors and B2B fees. |

## 1. Competitor table

*Scale and price figures are as of Oct 2026 — verify before relying.*

| Who | What they do | Scale | Model | Weakness vs us | Ev. |
|---|---|---|---|---|---|
| **Inception Point / Quiet Please / Liquid Studios** | Automated podcast network; now a managed B2B "content transformation" service | Peak claim 10,000 to 15,000+ shows, 3,000+ episodes a week; now about 300 unmonetized shows (F-IPA-01, -02); about 69 downloads per episode (F-IPA-07) | Programmatic ads (stopped working); now fees: list $10 per finished video minute, about $1 per audio episode, no named customers (F-IPA-08, -09) | Castro hid it, Podcast Index flagged it (F-IPA-10); no verification layer; invented-expert personas; audio glitches | A |
| **Mass AI feeds** (Apple, Spotify, YouTube) | Thin AI shows, AI "true crime" channels | 25% to 45% of new feeds (F-AUD-01) | Programmatic ads, AdSense | Platforms filter or demonetize them (F-HOST-13, -18). They make our category look bad | A |
| **ElevenLabs** (Reader, GenFM) | Turns documents into two-host podcasts; sells the voice API | Large vendor; valuation figures unverified | API, subscriptions, publisher deals | Generic, no sourcing or disclosure control. Also our primary voice supplier, so a dependency | B |
| **Wondercraft** and similar tools | Self-serve text-to-podcast for marketers and small publishers | Unknown | Subscriptions | Tools, not publishers: no sourcing, no local data, no accountability | B |
| **Google** (Daily Listen, NotebookLM) | Personalized short AI news brief; two-host summaries of uploads | Platform scale; NotebookLM daily caps Free 3 up to Ultra 100 to 200 (F-TTS-32) | Ecosystem, paid tiers | National or personalized, not local; no courts, no corrections log; no controllable commercial API | A/B |
| **Spotify; Audible/Amazon** | Distribution plus AI features (DJ, Daily Drive, AI narration) | Platform scale | Ads, subscriptions | Gatekeepers more than rivals; no local reporting. Spotify now badges verified shows and removes impersonators (F-HOST-16) | A/B |
| **Particle, Yahoo News, Washington Post AI podcast** | AI summaries; the Post personalized AI audio (late 2025) | Small to mid | Ads, subscriptions | National, text-first; the Post drew accuracy complaints (reported, low) | B |
| **Patch, NewsBreak, Hoodline** | AI-assisted local text. Patch planned about 30,000 community newsletters (F-IPA-13; do not cite outward) | Large claimed reach | Local ads | Text, not audio. NewsBreak ran AI-fabricated local stories; Hoodline used fake AI bylines | B |
| **Axios Local, Good Daily, 6AM City** | Human-written local newsletters | Axios about 30+ metros | Sponsors, ads | Text; limited cities; Columbia and LA coverage unchecked | B |
| **Local TV groups** (Nexstar owns KTLA; Tegna WLTX deal status unverified) | Local video news | Hundreds of stations | Retrans fees, ads | Video-first, no verified audio brief, but they own the local news habit | B |
| **Public radio** (SC Public Radio, LAist, KCRW) | Most trusted audio news brand | About 1,000+ stations | Donations; about $1.1B federal funding rescinded July 2025 (F-IPA-13) | Shrinking local capacity, few daily municipal briefs. Partner, syndication target or grant rival | B |
| **Law&Crime, Court TV, Courthouse News** | Human court and true-crime coverage | Law&Crime large on YouTube | Ads, subscriptions | High-profile cases only; routine local dockets underserved *(inference)* | B |
| **A&E *Cold Case Files*** | TV title that matches our show name | n/a | n/a | Naming collision: clear it or rename before launch (F-LEGAL-03, F-LEGAL-02) | B |

## 2. The closest rival: what happened and what we do about it

| What Inception Point did | What followed | Our rule |
|---|---|---|
| Flooded feeds: 200+ new shows a day, 325 in one day (F-IPA-02) | Castro hid the shows, Podcast Index flagged them, Listen Notes removed 31.5% of Aug 2026 new submissions as AI (F-IPA-10, F-HOST-18) | Launch few feeds, one per market and format, at a human-plausible pace. Wave 0 is seven shows (`config/shows.yaml`). Hyper-specific feeds roll out slowly |
| Chased keywords on a shooting within about an hour | The most-cited abuse in the press | The Breaking Desk needs 3 independent sources, no names or deaths before an official release |
| Gave AI hosts invented backstories and expert titles | Trust damage; Spotify now removes impersonators | Original synthetic personas with no human backstory ([voice guide](../standards/voice-and-persona-guide.md)) |
| Lived on programmatic ads at about $1 per episode | About 69 downloads per episode; the CEO said fully synthetic content is "no longer a revenue source" (Lead Balloon Ep. 73, 2026-09-29; F-IPA-08) | Plan on sponsors, B2B and direct sales. Ads alone do not pay for a local brief (facts sheet, five things) |
| Leaned on one model or a handful | The CEO later called that extremely risky (Freakonomics Ep. 690 postscript; unclear whether AI models or business models) | Orchestration layer with swappable vendors; ElevenLabs primary, Google Chirp 3 HD as tested fallback (F-TTS-23) |
| Loud PR about volume | The volume became the story | Lead with proof: a public verification scorecard, not scale |
| Left bad legacy episodes up; shipped glitchy audio | Documented errors, repeated words, bad health advice | 7-day automatic re-check, evergreen re-checks, an audio QA gate |

Liquid Studios is also a possible **vendor and partner**, not only a rival: its list prices are price anchors for our B2B line (F-IPA-09; live page not read). See the [meeting prep](meeting-jeanine-wright.md).

## 3. The local news gap

*Medill figures are recall, low confidence (F-AUD-08). Direction is more reliable than any count.*

| Fact | Detail | Ev. |
|---|---|---|
| Counties with 0 or 1 local news source | About 55% to 56% of US counties *(derived)*; about 3,500 newspapers lost since 2005 | B |
| Our test markets | Richland County SC and LA County are **not** news deserts. The gap is **depth**: municipal meetings, school boards, courts, neighborhoods, especially in audio | B/C |
| Market size | New York #1, Los Angeles #2, Chicago #3, Columbia about 71 to 80 (F-AUD-09). Columbia is small and consolidated, so the gap is easiest to prove there. LA is abundant, so we differentiate on format and verification | B/C |

## 4. Whitespace and positioning

**Capability matrix** *(inference, coarse; Y = yes, P = partly, N = no, ? = unknown)*

| Player | City-level | Audio-first | Visible sourcing | Courts | Clear AI label | Corrections log |
|---|---|---|---|---|---|---|
| Inception Point (past) | P | Y | N | P | P | N |
| Google / ElevenLabs GenFM | N | Y | P / N | N | P / ? | N |
| Particle / Yahoo | N | P | P | N | P | ? |
| NewsBreak | P | N | N | N | ? | ? |
| Patch / Axios Local | Y | N | P | N | ? / n/a | ? / Y |
| Local TV | Y | N (video) | N | P | n/a | Y |
| Public radio | P | Y | P | N | n/a | Y |
| Law&Crime / Court TV | N | P | P | P (high-profile) | n/a | ? |
| **Earlobe (target)** | **Y** | **Y** | **Y** | **Y** | **Y** | **Y** |

**Positioning statement** *(draft, inference).* "Local audio news you can check. Every claim is matched to at least two independent sources (three for breaking news), every episode says it is AI-made, and every correction is public." Three conditions: (1) **publish proof**, not promises: claims checked and dropped, corrections issued, hold and kill rates; (2) **name an accountable editor of record** (a founder decision); (3) **never say "first" or "only"**, we cannot prove absence. Say "built to be checked."

**Whitespace by show** *(inference)*

| Show | Competitive picture | Whitespace | Risk |
|---|---|---|---|
| Columbia Daily | Few audio local briefs; a daily paper and TV dominate; an old Inception Point SC tracker may still be listed | Municipal-level, sourced, audio-first brief | Local sources prefer human reporters; thin audience at launch |
| LA Daily | Crowded: LA Times, LAist, KCRW, TV | Format (6 to 8 min verified brief) plus city documents | Hardest to differentiate; do not lead with LA as proof |
| LA Courts Roundup, Case Tracker | Human high-profile coverage; no AI-native rival found | Routine dockets in audio with primary-document citations | Highest defamation and privacy exposure: strict lane ([legal](legal-and-compliance.md)) |
| The Breaking Desk | Giant, fast, human-branded | A slower three-source "confirmed" flash is a trust niche, not a speed play | Hold rules cost speed; never compete on "first" |
| Cold Case Files; History of Hollywood | Crowded human podcast niches | Primary-source, no-fabrication; archive as B2B proof | Low differentiation; name collision; victims' families |
| NYC, Chicago, more markets | Far larger and more crowded | Same method, later | Not researched (gap) |

## 5. How we win

| Advantage | Proof we must publish | Feeds product |
|---|---|---|
| **Checkable claims.** Two independent owner groups (three for breaking), fail-closed gate ([trust gate](../blueprint/trust-gate.md)) | Public scorecard and trust log | Trust Stack |
| **City depth and courts.** Municipal documents and dockets that shrinking newsrooms thin out *(inference)* | Every source linked in show notes | Network |
| **Honest AI label** spoken at the end and in metadata, as Apple asks (F-HOST-15) | "How this show is made" page ([disclosure standard](../standards/ai-disclosure.md)) | Network |
| **Public corrections** and one accountable company, not "the AI" | Monthly numbers, including bad ones | Network, Trust Stack |
| **Few feeds, plausible pace**, so discovery filters do not catch us | Listed and charting on Apple, Spotify, Castro | Network |
| **Cost discipline and swappable vendors**; voice hybrid cuts Scale-stage voice cost 35% to 75% (F-TTS-12, -23) | Cost per episode and downloads per episode, tracked from day one | Earlobe Engine |
| **Network first, tools later.** Running real shows is the demo for the other three products | Case studies with real numbers | All four |

## 6. Competition by product

| Product | Who competes | Price anchors / notes |
|---|---|---|
| **The Network** | Sections 1 and 4 | Typical CPM $17 to $22 (F-ADS-04); our planning programmatic CPM $8 / $13 / $20 (F-ADS-07); sponsors and B2B must close the gap |
| **Trust Stack** | No direct product found (B; not searched). Adjacent: platform "verified" badges, newsroom fact-check tools, Liquid Studios if it adds QA | No buyer demand validated yet *(inference)* |
| **Earlobe Engine** | Liquid Studios, Wondercraft, ElevenLabs Studio and GenFM | $10 per video minute, about $1 per audio episode (F-IPA-09). Our model's B2B guess ($1,000 to $3,500 a client a month) sits 46x to 161x above the audio anchor: validate with 2 or 3 buyers first |
| **C&C Studio Services** | Podcast production agencies, hosting companies' done-for-you services | Not researched (gap) |

## 7. Threats to watch

| Threat | Weight *(inference)* | Early signal | Our move |
|---|---|---|---|
| Google or Spotify add local signals to AI audio briefs | High | Daily Listen expansion; local publisher licenses | Go deeper than they will: courts, municipal records, visible sourcing |
| ElevenLabs ships "local news GenFM" or signs local publishers | Medium | Reader or GenFM announcements | Second-source the voice now; stay model-agnostic |
| Public radio or Nexstar launch AI-assisted audio briefs | Medium | Station announcements after the Tegna deal | Offer partnership or syndication before they build |
| A platform treats all automated news audio as low quality, verified or not | High | Spotify Verified criteria; Apple enforcement; iHeart's "Guaranteed Human" (F-HOST-17) | Disclose fully, publish proof, keep listener numbers honest |
| One public accuracy or defamation failure in the court or crime lane | High | A correction on a named person; a demand letter | Strict lane, insurance and a lawyer first ([legal](legal-and-compliance.md)) |
| Name collisions (*Cold Case Files*, *Columbia Daily*, *LA Daily*, "Curious") | Medium | Trademark search hits | Clearance before launch; rename early |
| Liquid Studios wins publisher deals and adds a verification layer | Low to medium | Named customers appear | Move first on a published scorecard and partners |
| The economics, not a rival: ad fill and CPM are unmeasured (F-ADS-08) | High | Real fill under 30% | Sell sponsors and B2B early; cap spend per show |

## 8. Naming and clearance flags

*Cold Case Files* (A&E title), *Columbia Daily* and *LA Daily* (echo existing papers), "Curious" (crowded), *Breaking Desk* and *Case Tracker* (unchecked). Search USPTO, app stores and podcast directories before launch. Filing fees are $350 per class (F-LEGAL-03).

## 9. Gaps: what to research next

1. Whether Inception Point's SC and LA feeds are still live, and Liquid Studios customers or case studies.
2. Google Daily Listen status, ElevenLabs GenFM pricing and any local news plans, Spotify Verified criteria for AI-labeled shows.
3. Medill 2025 and any 2026 report, with the SC and CA state pages and the Richland and LA county profiles.
4. Public radio and local TV AI plans in Columbia and LA; whether Axios Local or 6AM City cover either city.
5. Any AI-native court or true-crime entrant; listener surveys on AI news audio (F-AUD-06, -07 are advocacy or recall).
6. Trust Stack and Studio Services competitors (not searched).

## Sources

Opened in earlier research (via the notes): [Hollywood Reporter](https://www.hollywoodreporter.com/business/digital/ai-podcast-start-up-plan-shows-1236361367/), [Podnews on the pivot](https://podnews.net/update/inception-point-pr-stunt), [Lead Balloon Ep. 73](https://www.podcampmedia.com/post/lead-balloon-ep-73-ai-podcast-hosts-scrapped-inception-point-ceo-jeanine-wright-explains-pivot), [Castro](https://castro.fm/blog/hiding-inception-point-ai), [Variety on Spotify](https://variety.com/2026/digital/news/spotify-bans-ai-generated-podcasts-impersonate-verified-badges-1236752944/), [Apple guidelines](https://podcasters.apple.com/support/891-content-and-subscription-guidelines), [Radio Ink on iHeart](https://radioink.com/?p=97798), [Freakonomics Ep. 690](https://freakonomics.com/podcast/its-show-business-baby/). Tier B rows rest on recall: see the [research note](../research/notes/competitive-landscape.md), landing pages only.
