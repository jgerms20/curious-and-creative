# The four products: who buys, what they get, what it might cost

**The Curious & Creative Network · as of 2026-10-12 · DRAFT for Joshua and Janel (Curious & Creative LLC).** Numbers cite the [facts sheet](../research/facts-and-figures.md) by ID. Our own reasoning is marked *(inference)*. Companions: [advertising plan](advertising-plan.md), [market research](../research/market-research.md), [competitive landscape](competitive-landscape.md). Prices are **as of Oct 2026 — verify before buying or quoting**.

**Evidence status (read first).** Only product 1 has sourced ingredients. Products 2 to 4 have price anchors or hypotheses at best, and nobody has validated a price with a buyer. Every price below is a **hypothesis to test with 2 or 3 real buyers**, not a quote.

## The short version

| # | Product | Who buys | What they get | How it earns (hypothesis) | Evidence | Status |
|---|---|---|---|---|---|---|
| 1 | **The Network** | Listeners (free), local sponsors, advertisers; later radio and platform licensees | Verified local, courts, crime and archive audio, every episode labeled AI | Sponsors first, programmatic second, licensing and memberships later | Partly sourced (F-ADS, F-AUD) | Engine v1 built; revenue agents `next` |
| 2 | **Trust Stack** | Publishers, AI-audio makers, ad buyers, platforms | Verification as a service: claim checks, a pass/hold/kill decision, an audit trail | Free or at-cost audits first, then metered per script | None; cost floor only | Runs inside the Network (8 of 14 agents built); product is `future` |
| 3 | **Earlobe Engine** | Newspapers, universities, companies | Their own automated audio product, built from their content, under their brand | Pilot fee plus a per-episode managed fee | Competitor list prices only (F-IPA-09) | `future` |
| 4 | **C&C Studio Services** | Local businesses, creators, nonprofits, schools | Podcast setup, distribution and coaching, in person and remote | Project fees, then monthly production | None ($1,500 to $5,000 is a model guess) | `next` |

**The order.** Build and dominate the Network first. Sell Studio Services now because it makes cash with no product risk. Sell the two tools later, once the Network has proven them in public.

## 1. The Network

**What it is.** Owned shows under the Curious & Creative Network label. Seven are live-ready in wave 0 ([shows.yaml](../../config/shows.yaml)). NYC Daily and Chicago Daily are configured and switched off (wave 1). Hyper-specific always-on feeds are `future` and roll out slowly.

| Show | Lane | Cadence | Best revenue fit | Ad stance |
|---|---|---|---|---|
| Columbia Daily | standard | Weekdays, 06:00 ET | Local sponsors | Ads on |
| LA Daily | standard | Weekdays, 06:00 PT | Local sponsors | Ads on |
| The Breaking Desk | breaking | On events | Trust brand, licensing to partners | Ad-free for deaths and attacks |
| LA Courts Roundup | strict | Tue to Sat | B2B and licensing; opt-in sponsors | Opt-in only |
| Case Tracker | strict | Weekly plus flashes | Memberships later; opt-in sponsors | Opt-in only |
| Cold Case Files | strict | Tue and Thu | Series sponsor; licensing | Opt-in only |
| History of Hollywood | archive | Mon, Wed, Fri | Evergreen sponsors; licensing | Ads on |

**Revenue lines.** Details and rate card are in the [advertising plan](advertising-plan.md). *As of Oct 2026 — verify before buying.*

| Line | Status | Note |
|---|---|---|
| Local direct sponsors | `next` | Flat monthly packages priced from downloads. About $90 a slot at 120 downloads per episode |
| Programmatic via host DAI | `next` | Planning net $8.60 per 1,000 downloads at the base case (F-ADS-12). Fills unsold slots only |
| Network and category sponsors | `next` | Worth selling when brand-safe downloads pass about 25,000 a month *(inference)* |
| Licensing and syndication (radio, smart speakers, news sites) | `future` | Content Licensing Agent and Syndication Packager |
| Memberships (ad-free, early access) | `future` | Apple keeps 30% then 15%; Patreon nets about 80% to 85% (F-HOST-11, -12, recall) |
| Grants | `next` | Some funders may exclude AI-produced news *(inference)* |

**The honest economics.** A 7-minute brief costs about $2.56 to $3.16 (F-LLM-07, F-TTS-17). Ads earn about $1.03 at 120 downloads, so ads lose about $1.50 to $2.10 an episode (facts sheet, "Model assumptions"). Ads alone break even only near 300 to 370 downloads per episode. The closest rival learned this: its CEO said fully synthetic content was "no longer a revenue source" (Lead Balloon Ep. 73, 2026-09-29; F-IPA-08). Wave 0 is a learning stage, not a revenue stage.

**Rules that protect the Network.** Few feeds, at a human-plausible pace, because flooding drew Castro, Podcast Index and Listen Notes filters (F-IPA-10, F-HOST-18, F-AUD-01). AI disclosure at the end of every episode ([standard](../standards/ai-disclosure.md)). Sponsors never touch coverage (Editorial Standards section 12).

## 2. Trust Stack (verification as a product)

**What it is.** The chain every script already passes: claim extractor, blind source verifier, fact checker, bias and legal screens, a rules-engine gate that fails closed, and a 7-day re-check. Two independent owner groups per claim, three for breaking ([trust gate](../blueprint/trust-gate.md)).

| Who might buy *(inference)* | Their pain | Signal in our sources |
|---|---|---|
| Publishers adding AI audio or summaries | Wrong or unsourced AI output | About 45% of AI-assistant news answers had a significant issue (F-AUD-07, low-med) |
| AI-audio makers, including Liquid Studios | Trust, glitches, accuracy complaints | Rival turned to B2B publishers (F-IPA-09); see the [meeting prep](meeting-jeanine-wright.md) |
| Ad buyers and marketplaces | Brand safety on synthetic shows | Curation and episode-level brand-fit scoring (F-ADS-15) |
| Platforms and distributors | Telling real shows from spam | Spotify "Verified" badges, Apple disclosure rule (F-HOST-16, -15) |

**What they could get, and a price hypothesis** *(inference; no market price exists; as of Oct 2026 — verify before buying)*

| Package | Contents | Price logic |
|---|---|---|
| Sample audit | We run the stack on 25 to 100 episodes of a customer's catalog and write a plain report | Our cost is about $1 to $2 per 7-minute script (F-LLM-07), so 25 episodes cost us $26 to $50. Run the first ones free or at cost for a case study |
| Metered API | A decision (publish, rewrite, hold, kill), the claim list and a trust log per script | Cost-plus: 3x our $1.04 to $2.00 gives about $3 to $6 per 7-minute script. Volume tiers later |
| Monitor | The 7-day re-check plus a monthly transparency report for the customer's shows | Per active show per month; set after pilots |
| Scorecard or badge license | A "checked by" mark | Only after an outside audit of our own numbers. Never before |

**Before we sell it:** a stable interface; at least 6 monthly public transparency reports; a known cost per call; a support plan; and a plain scope statement. We check claims against sources. We do not guarantee truth. The Tools Productization Strategist (`future`) scores readiness monthly. Pilots then go to the Trust-Stack API Concierge (`future`).

## 3. Earlobe Engine (our workflow as a product)

**What it is.** The pipeline that runs the Network, configured for a customer: their sources, personas, brand, lane policies and cadence, with the Trust Stack on their content and their own editors as escalation contacts.

| Buyer *(inference)* | Why they would pay |
|---|---|
| Newspapers and local TV or radio groups | They own the local news habit and have no verified audio brief. Offer partnership before they build their own (competitive note) |
| Universities, public media, nonprofits | Audio from content they already publish |
| Companies with a content archive | Briefs and explainers from existing material |

**Price anchors.** Liquid Studios lists $10 per finished video minute (about $600 for a 60-minute episode) and about $1 per audio episode. It has no named customers, and its live page was not read (F-IPA-09). Our cost for one verified 7-minute brief is $2.56 to $3.16, so $1 is below our cost. The cost model's guess of $1,000 to $3,500 per client per month is 46x to 161x the audio anchor and is unsupported.

**Hypothesis** *(inference; as of Oct 2026 — verify before buying)*

| Piece | Price logic |
|---|---|
| Pilot, 4 to 6 weeks (dry run, about 20 episodes, staff training) | $2,500 to $5,000 fixed, matching the Services range |
| Managed run | 3x to 5x our cost: about $8 to $16 per verified 7-minute brief, or about $170 to $340 a month for a weekday show |
| Platform fee for support and uptime | $500 to $1,500 a month, set after the first pilot |

That totals about $670 to $1,840 a month for a daily show, partly below the model's $1,000 floor. A buyer has to confirm it.

**Open blockers.** Whether our voice vendor's license lets us resell audio made for a client (ask sales whether API and subscription rights match, conflict C1). LLM vendors' usage terms for news content. Who is the accountable publisher: the customer, not us. Status `future`; White-Label Onboarding is the matching agent.

## 4. C&C Studio Services

**What it is.** The in-person offer: Joshua and Janel set up podcasts and distribution for businesses and people in Columbia and Los Angeles, and remotely. Services Intake qualifies each lead and drafts the proposal. Client Show Setup and Distribution Setup do the prep and the platform work.

**Who buys** *(inference)*: local businesses that want a branded show (often the same owners we call as sponsors), creators, nonprofits and schools, individuals with a story.

| Package | What the client gets | Price hypothesis *(inference; as of Oct 2026 — verify)* |
|---|---|---|
| Setup | Concept and format, name check, cover art, licensed sound package, hosting in the client's own account, feed and directory submission | $1,500 to $2,500 |
| Launch | Setup plus an on-site recording day, first 4 episodes produced, distribution live, analytics access | $3,000 to $5,000 |
| Monthly Production | Client uploads raw audio; we clean, propose edits, write notes, transcript and clips; client approves | Per delivered episode, set after two clients show real hours |
| Coaching | Delivery, structure and interviewing feedback plus live sessions | Per session or 4-session bundle, set from hours |

The $1,500 to $5,000 envelope is the cost model's unsupported guess. Pass-through costs the client pays: hosting about $19 to $99 a month (F-HOST-02, -03, low confidence), and the Apple Podcasters Program at $19.99 a year only if they sell subscriptions (F-LEGAL-07). One $1,500 project covers about three months of the $500-a-month insurance placeholder (F-LEGAL-01).

**Guard rails.** Accounts and assets are in the client's name; we never hold a show hostage. The client approves every episode and answers for its facts, and we flag obvious legal risks. If the client uses synthetic voices, we apply each platform's disclosure rule (F-HOST-15 to -17). A client who is a news subject in our markets is flagged, and buying services never buys coverage. Client shows are not Network shows and do not carry the network label *(inference)*.

**Limit.** It runs on founder hours on site *(inference)*. Field Ops Coordinator, Client Coaching, Client Post-Production and Client Reporting are `future`. Keep it to a few clients until Phase 1 of the roadmap is done.

## 5. How the four feed each other

| From | To | What flows | Guard rail |
|---|---|---|---|
| Network | Trust Stack | Public scorecard, corrections log, monthly transparency reports: the proof and the first case study | Publish bad numbers too, or the proof is worthless |
| Network | Engine | The pipeline running 7+ shows is the demo; real cost per episode is measured | Do not leak one client's content into another's |
| Trust Stack | Network | "Verified" is why sponsors, platforms and partners trust us over volume rivals | One public accuracy failure hurts every product |
| Engine | Network | Each new market is a template launch; client use finds bugs | Client data stays with the client |
| Studio Services | Network | Local business relationships become sponsors; founders hear real demand | Buying services never buys coverage or ad priority |
| Network | Studio Services | Sponsors who like audio ask for their own show; sponsor reads are a portfolio | Conflict check on every client |
| Studio Services | Engine, Trust Stack | A client who outgrows do-it-yourself becomes an Engine pilot; a client with news content becomes an audit | Sell only when the readiness checks pass |

**In one line:** the Network makes the proof, the proof sells the tools, and Studio Services pays the bills and finds the local sponsors while that happens.

## 6. Roadmap

Dates are targets *(inference)*, not commitments. Each phase needs its gate before the next starts.

| Phase | When | Network | Trust Stack | Engine | Studio Services | Gate to next phase |
|---|---|---|---|---|---|---|
| **1. Prove it** | Now to Jan 2027 (days 0 to 90) | Wave 0 live; first sponsors; programmatic test | Public scorecard and corrections log; first monthly transparency report | Nothing sold; keep the interface clean | First 1 or 2 clients | 5 or more paid placements; 3 months of public trust numbers; insurance bound |
| **2. Widen** | Feb to Jun 2027 | NYC and Chicago Dailies; second host; category sponsor; first licensing talks | Free or at-cost audits for 2 or 3 outside publishers | 2 or 3 priced buyer conversations | 3 to 5 clients on a standard order form | Buyers confirm a price; 6 monthly reports published |
| **3. Productize** | H2 2027 | Wave 2 markets; niche feeds slowly; membership test | Paid API pilot | Paid pilot with one customer | Hire or contract help if demand exceeds founder hours | Readiness scorecard passes: stable interface, track record, known cost per call, support load |
| **Later** | 2028 on | More markets and shows | Scorecard or badge, only after an outside audit | Self-serve tier | Franchise the playbook | Founders' call |

## 7. Risks and decisions

| Risk | Why it matters | Mitigation |
|---|---|---|
| Platforms filter AI shows | Discovery is the scarce thing (F-HOST-18) | Few feeds, full disclosure, public proof |
| Insurance priced up or declined for automated crime coverage | No cover, no strict-lane shows (F-LEGAL-01) | Quotes first; start with the dailies |
| Thin ad revenue | Ads lose money per episode at base audiences | Sponsors, Studio Services, cost discipline |
| Voice or LLM vendor terms block resale | Kills the Engine | Written answers before any pilot; swappable vendors (F-TTS-12, -23) |
| One public accuracy or defamation failure | Sinks the Trust Stack story | Strict lane, fail-closed gate, fast public corrections |
| Founder hours | Services and sales compete with building | Cap Services clients; agents prepare, founders attend |

**Decisions for the founders:** (1) Start Studio Services now, and how many clients at once? (2) Open a Trust Stack conversation with Liquid Studios, or wait? (3) Free audits as a case-study trade? (4) Who is the named accountable editor of record? (5) Which two or three buyers do we ask first for a price check?
