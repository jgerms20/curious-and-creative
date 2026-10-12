# Advertising plan: programmatic, local sponsors and the wall between ads and news

**The Curious & Creative Network · as of 2026-10-12 · DRAFT for Joshua and Janel.** Numbers cite the [facts sheet](../research/facts-and-figures.md) by ID; our own reasoning is marked *(inference)*. Companion: [products](products.md). Rates and platform policies are **as of Oct 2026 — verify before buying or quoting**.

**Evidence status.** No ad figure here is measured. CPM, fill and share are two sourced ranges plus our inference (F-ADS-04, -05, -07 to -09). No host page, rate table or advertiser survey was opened. Treat every revenue number as a planning case until the first 90 days of data exist.

**Words used.** CPM = price per 1,000 ad plays. Fill = share of ad slots that sell. DAI = dynamic ad insertion: the host stitches the ad into the file when it downloads. eRPM = what we really earn per 1,000 downloads.

## The short version

| | |
|---|---|
| The honest math | A 7-minute verified brief costs about $2.56 to $3.16 to make (F-LLM-07, F-TTS-17). At the base audience of 120 downloads, programmatic ads earn about $1.03 an episode (F-AUD-03, F-ADS-12). Programmatic alone does not pay for a local brief. |
| So the plan is | Sell local sponsors first. Let programmatic fill only unsold slots. Keep crime and tragedy ad-free unless an advertiser opts in. Never let a sale touch coverage. |
| One sponsor matters | At the base audience one daily-show slot is worth about $90 a month (section 4), close to the $56 to $69 a month the show costs to make *(inference)*. |
| The old sponsor rates | $300 / $750 / $1,500 a month imply a CPM of $92 to $461 (F-ADS-14). They only hold at about 395 / 990 / 1,975 downloads per episode on one slot (section 4). |
| 90-day target | Five signed placements and about $400 a month by day 90, clean campaign reports, and a measured programmatic rate *(inference)*. The goal is proof, not profit. |
| Nothing is built | Every revenue agent is `next`. `config/sponsors.yaml`, the ad segment and gate rule S6 do not exist yet (NE-12, G-4). Until then the founders run these playbooks by hand. |

## 1. Revenue lines in this plan

| Line | How it earns | Run by | Starts |
|---|---|---|---|
| Programmatic (host DAI) | A marketplace fills slots we did not sell | Ad Ops | Test on 2 or 3 shows once a host says yes in writing |
| Local direct sponsors | Flat monthly packages sold to local businesses | Founders, Sponsor Prospector | Selling from pre-launch; first air about week 4 |
| Network and category sponsors | One exclusive sponsor per category across many shows | Founders, Revenue Director | Talks from day 60 |
| Crime-lane sponsors (opt-in only) | Same rate card, advertiser must opt in | Founders | Decide at day 90 |

Licensing, memberships, grants, B2B and Studio Services are covered in [products](products.md), not here.

## 2. Inventory: where ads can sit

| Show type | Slots | Rule |
|---|---|---|
| Daily briefs (6 to 8 min) | Slot A: mid-roll between story blocks. Slot B: end break before the sign-off. Never more than 2 (F-ADS-11) | Launch with **A only**. Open B at day 60 if completion holds within 5 points of the ad-free first weeks *(inference)* |
| Long-form (History of Hollywood, Cold Case Files, Case Tracker, Courts Roundup) | Mid-roll and end break | Crime and court shows: opt-in only (section 8) |
| The Breaking Desk (2 to 4 min flashes) | None at launch | Later, one slot on flashes tagged clear |

- **Ad load.** Total ad time stays under 12% of an episode *(inference)*. Each break is about 10 seconds of required framing plus the read (about 15 seconds on briefs, about 30 on long-form). Two breaks in a 7-minute brief run about 50 seconds, so one slot is the honest launch setting.
- **Position.** Ads sit only in marked breaks, never inside a story (COI-2). The AI disclosure is still the last thing spoken ([ai-disclosure](../standards/ai-disclosure.md) section 3E).
- **How it works.** The Sound Designer marks break points. The host's DAI adds the ad file. The episode audio never contains ad copy, so the Trust Stack never sees it (COI-7).

## 3. Programmatic via host DAI

*As of Oct 2026 — verify before buying. Host terms are all recall (F-HOST-02 to -10).*

| Planning number | Conservative | Base | Optimistic | ID |
|---|---|---|---|---|
| Gross CPM | $8 | $13 | $20 | F-ADS-07 (sourced anchors: programmatic $12 to $15, DAI $18 to $22, F-ADS-05) |
| Fill | 30% | 55% | 75% | F-ADS-08 |
| Our share after host | 50% | 60% | 70% | F-ADS-09 |
| Net per 1,000 downloads at 2 slots | $2.40 | $8.60 | $21 | F-ADS-12 |
| Per daily show-month (40 / 120 / 400 per episode, 21.7 episodes) | about $2 | about $22 | about $182 | F-AUD-03 *(inference)* |

With one slot at launch, halve every row.

**Rules.**
- Programmatic fills only unsold slots on brand-safe shows. A slot we sold to a sponsor is never also offered to the marketplace.
- It is **off** for the strict lane and the Breaking Desk, and on only where the episode is tagged clear (section 8).
- Test on 2 or 3 dailies for 8 to 12 weeks on a host-integrated marketplace. Record real eRPM, fill and payout timing, then write them into the F-ADS rows ([CONVENTIONS](../CONVENTIONS.md) rule 1).
- Do not plan on the "about $50 CPM" claim (F-ADS-06).
- Marketplaces are moving to curation and episode-level brand-fit scoring (F-ADS-15). A clean brand-safety tag and a public trust record should help us later. Enterprise hosts probably decline an unproven AI catalog until audited audience data exists (F-HOST-09).
- Ad-tech trackers can pull in California privacy duties at 100,000 or more California consumers (F-LEGAL-15). Ask the lawyer before turning on tracking pixels.

**Ask every host in writing before paying:** its AI-content position (iHeart's "Guaranteed Human" is on record, and whether it covers third-party shows on its Spreaker host is unknown, F-HOST-17); pre, mid and post markers by API; category blocks; revenue share (Spreaker reportedly keeps about 40%, old, F-HOST-07); minimum downloads; whether stats are IAB-certified; and whether ads can be inserted into back-catalog episodes.

## 4. Local direct sponsorships

*As of Oct 2026 — verify before quoting. All rates are hypotheses (F-ADS-10 is inference).*

**Why direct first.** Local money moves on relationships and flat monthly packages, not auctions. The planning CPM for a direct local slot is $20 / $35 / $60 against $8 / $13 / $20 for programmatic (F-ADS-10, F-ADS-07).

**Rate rule (rate card v0).** Monthly price per slot = the show's trailing-30-day downloads x $35 / 1,000, rounded, never below a **$50 floor**. The floor sits inside the $50 to $150 community-package band (F-ADS-10). The Rate Card Manager resets the rule monthly. A sponsor's price is locked for the term.

| Package | What the sponsor gets | Price rule | At 40 / ep | At 120 / ep | At 400 / ep |
|---|---|---|---|---|---|
| Community Spot | One 15-second read, one slot, every episode, one month | 1 x rule | $50 | $90 | $300 |
| Show Sponsor | Both slots, one per category, named in show notes and on the site | 2 x rule x 1.25 *(premium is inference)* | $100 | $230 | $750 |
| Market Bundle | A slot on each brand-safe show in one market, plus the newsletter | Sum of slots less 10% *(inference)*. LA at base: ($91 + $182) less 10% is about $245. Newsletter priced after 60 days of open rates | see rule | see rule | see rule |
| Evergreen Sponsor | A slot on History of Hollywood, back-catalog included if the host allows | 13 episodes x downloads x $35 / 1,000. Its audience is a proxy from F-AUD-04, not researched | $50 | $55 | $180 |

Columns are downloads per daily episode (F-AUD-03); 21.7 episodes a month.

**When the cost model's sponsor rates become true** *(arithmetic on F-ADS-14, $35 CPM)*

| Monthly price | Downloads per episode needed, one slot | Needed, Show Sponsor (2 slots x 1.25) |
|---|---|---|
| $300 | about 395 | about 158 |
| $750 | about 990 | about 395 |
| $1,500 | about 1,975 | about 790 |

**Founding Sponsor offer (first 90 days).** A locked 3-month rate at $50 to $90, "Founding Sponsor" in the show notes and on the website, a weekly download report, one free rewrite, and a credit for any episode we skip or run ad-free (promise 7: we would rather skip a day than be wrong). Day-90 audiences will sit below the month 6 to 12 planning numbers *(inference)*, so we sell trust and early placement, not reach.

**Deal terms** (Contracts & IP Clerk template, founders sign every contract): the AI-voiced-read clause; no personal-experience claims; no editorial influence; no political or issue ads at launch; make-good is a credit; the sponsor can pause its own ads, never delay or soften a story. Outreach emails follow CAN-SPAM: postal address, working opt-out honored within 10 business days (F-LEGAL-14).

## 5. Network-wide and category sponsors

*Rates are hypotheses, as of Oct 2026 — verify before quoting.*

| Offer | What it is | Price rule | When |
|---|---|---|---|
| Network Category Sponsor | One exclusive sponsor per category (bank, health system, real estate, auto, telecom, education) across every brand-safe show, 90-day minimum | Brand-safe monthly downloads x $35 / 1,000 x 1.25 *(inference)* | Sell when trailing 30-day brand-safe downloads pass about 25,000 *(inference)* |
| Wave 0 reality | Columbia Daily + LA Daily + History of Hollywood (audience a proxy) at base is about 10,400 downloads a month | About $455 a month. At 25,000 it is about $1,100 | Not worth a special sales push yet |
| Series Sponsor | A season of History of Hollywood or Cold Case Files, with category exclusivity | Evergreen rule x 1.25 | After 60 days of evergreen download data |

Category exclusivity is per show, one sponsor per category. NYC, Chicago and more markets are what turn this into real money.

## 6. Sponsor-read writing rules

The Sponsor Read Writer (Sonnet tier) and the Legal Screener in ad mode apply these to every read.

| # | Rule | Why |
|---|---|---|
| 1 | Third-person announcer style. Never "I use it", "we love it", "our team tried it" | AI hosts have no experience to report (COI-3; FTC Endorsement Guides, F-LEGAL-14) |
| 2 | Open with "This episode is supported by `{sponsor}`." Close with "That was a message from `{sponsor}`. Sponsors never see or influence our reporting." Add "This ad is read by a synthetic voice." as a precaution | [ai-disclosure](../standards/ai-disclosure.md) 3E; NY synthetic-performer ad law, low confidence |
| 3 | Never voiced by Ava (breaking and disclosure) or June (courts and crime). Use a separate non-news announcer persona, designed by the Voice Director | [voice guide](../standards/voice-and-persona-guide.md) V-4 |
| 4 | Only claims the sponsor substantiates in writing. No health or money-return claims, no "best", "#1" or "guaranteed" without proof, no named competitors | Legal Screener ad mode; COI-7 |
| 5 | One idea, one call to action, one tracked promo code or short link. About 38 words for 15 seconds, about 75 for 30 | Reporting needs a trace |
| 6 | Written for the ear: short sentences, spelled-out numbers and web addresses, local names sent to the Pronunciation Keeper | Voice guide |
| 7 | Must not sound like news: no "breaking", no headline cadence, no news personas' tone, no official-looking seals or names | FTC impersonation rule (F-LEGAL-14); COI-2 |
| 8 | No testimonials, reviews or quotes unless the person is real, consented and their connection to the sponsor is stated | FTC fake-review rule, about $53,088 per violation (F-LEGAL-14) |
| 9 | Default decline at launch: political and issue ads; alcohol, gambling, cannabis, firearms; bail bonds and personal-injury law on court and crime shows | Founders' call *(inference)* |
| 10 | Flow: brief, draft, Legal Screener, sponsor approves their facts, founders approve the order, Studio Voice renders, QA Listener checks, Ad Ops traffics. Sponsors cannot edit the framing lines. Refresh copy every 4 weeks | Fatigue and control *(inference)* |

## 7. The ad and editorial wall

*Rules are in [Editorial Standards](../standards/editorial-standards.md) section 12. This table says how sales respects them.*

| Rule | How we keep it |
|---|---|
| **COI-1** Sponsors never see or influence scripts, story choice or corrections. No sponsored stories | Revenue agents never receive scripts, source packs or the trust log *(design requirement)*. Sponsors learn about coverage when the public does |
| **COI-2** Marked breaks only | Ads are separate files at host markers, never in the script |
| **COI-3** No experience claims | Writing rule 1, plus the ad-mode screen |
| **COI-4** A story about a current sponsor says so on air and in notes | Needs `config/sponsors.yaml` and gate rule S6 (NE-12, not built). Until then the Prospector screens conflicts and the founders check each signing |
| **COI-5, COI-6** Own conflicts disclosed; no gifts for coverage | Studio Services clients are treated like sponsors for conflicts *(inference)* |
| **DISC-8** The disclosure is never for sale and never stripped | No package, discount or clause touches it |
| **COR-2** Corrections ignore who advertises | The Corrections Agent has no access to the sponsor list *(design requirement)* |

- **If we cover a sponsor badly,** we run the story as the facts require. We tell the sponsor nothing in advance. The sponsor may pause its own ads afterward. We never delay, soften or drop a story to keep money.
- **If revenue and standards conflict,** the Revenue Director flags it and standards win. The Standards Editor is never overruled by a sale.
- **Publish the list.** Current sponsors appear on the website and in show notes.

## 8. Brand safety for crime, courts and tragedy

*Default from the revenue agents' rules: no ads next to crime or tragedy unless the advertiser opted in. Breaking Desk coverage of deaths and attacks runs ad-free ([how it works](../blueprint/how-it-works.md)).*

| Show (lane) | Default | Who can buy |
|---|---|---|
| Columbia Daily, LA Daily (standard) | Ads on. Breaks next to tagged stories are restricted | Any sponsor; exclusions honored |
| History of Hollywood (archive) | Ads on; tagged segments (a death, a crime) restrict adjacent breaks | Any sponsor |
| LA Courts Roundup, Case Tracker, Cold Case Files (strict) | Programmatic off. Not sold in the first 90 days *(inference)* | Opt-in advertisers only, calm service categories, no fear appeals, no law firms or bail bonds |
| The Breaking Desk (breaking) | Deaths, attacks, disasters: always ad-free. Other flashes: ad-free at launch | Later, clear flashes only |

**Adjacency steps** *(Ad Ops design; fail closed)*
1. A Haiku-tier classifier tags each story block: crime, death, disaster, politics. Strict and breaking lanes also use the Harm & Sensitivity Reviewer's flags (`next`).
2. A break next to a tagged block is **restricted**. If another break point is clear, use it. If none is, the break runs a house promo or stays empty.
3. Untagged or unclassifiable means restricted.
4. Only opted-in sponsors can fill a restricted break, and never right after violence involving a named victim.
5. Each insertion order lists the advertiser's excluded categories. Programmatic category blocks are used only after the host proves they work in a test.
6. When the Breaking Detector fires an attack or disaster, Ad Ops pauses sponsor and programmatic delivery for the Breaking feed and the next daily in the affected market *(inference)*.
7. Skipped breaks are credited, never billed.
8. Weekly, Ad Ops and the Run Auditor sample 10% of episodes *(inference)*. Target: 0 violations (Ad Ops KPI). A violation means the creative is pulled within the hour, the sponsor is credited and the incident is logged.

## 9. Ad ops workflow by agents

All six agents are `next`. Founders approve every contract, price exception and invoice above the standing limit.

| When | Agent (tier) | Does | Hands to |
|---|---|---|---|
| Monthly | [Rate Card Manager](../../agents/revenue/rate-card-manager.md) (Sonnet) | Reads trailing downloads and the F-ADS CPMs, resets rates and packages, sets discount and make-good rules | Founders for large changes; Media Kit Builder |
| Monthly, day 2 | [Media Kit Builder](../../agents/revenue/media-kit-builder.md) (Sonnet) | Kits per show and market and a network deck. Our logs only, with as-of dates; estimates never shown as data | Prospector, founders |
| Weekly per market | [Sponsor Prospector](../../agents/revenue/sponsor-prospector.md) (Sonnet) | Leads from new business filings, chamber lists and current local advertisers. Scores fit and conflicts. Drafts outreach. Books calls | Founders' calendar |
| Per sale | Founders | Take the call, price within the card, sign | Contracts & IP Clerk |
| Per campaign | [Sponsor Read Writer](../../agents/revenue/sponsor-read-writer.md) (Sonnet) | Drafts the read, runs the section 6 flow | Studio Voice, QA Listener |
| Always on | [Ad Ops](../../agents/revenue/ad-ops.md) (Haiku) | Sets DAI, traffics campaigns, tags episodes, enforces ad load and sections 2 and 8, watches fill and delivery | Campaign Reporter |
| Weekly, then at the end | [Campaign Reporter](../../agents/revenue/campaign-reporter.md) (Haiku) | Delivery report, promo-code results, make-goods. Flags campaigns ready to renew | Prospector, Billing |
| Per order | Billing & Collections (Haiku) | Invoices from the signed order, reminders, reconciliation. Never changes price or terms | Finance Reporter |
| Weekly | Revenue Director (Sonnet) | Revenue memo and targets. Decides where effort goes (direct before programmatic in small markets) | Founders |

Failure handling: if a read is not approved in time, the slot runs a house promo or stays empty. The Kill Switch and Budget Controller apply to every agent.

## 10. Reporting

**To sponsors** (weekly during a campaign, plus a wrap-up): dates and episodes aired; spots delivered; downloads of those episodes (de-duplicated and bot-filtered, IAB-certified if the host offers it, verify); completion where the host reports it; promo-code or link results; credits owed; a renewal note. Every number shows its source and date range. We do not claim listener demographics we cannot measure.

**Inside** (the Revenue Director's weekly memo): revenue by line against plan; revenue per 1,000 downloads by show and slot; sell-through; realized CPM against F-ADS-07; programmatic fill against F-ADS-08; pipeline coverage; ad-free episode count; brand-safety incidents (target 0); days sales outstanding.

**Public:** the sponsor list, plus ad-free and incident counts in the monthly transparency report *(inference)*.

## 11. 90-day sales plan: Columbia and Los Angeles

Day 0 = first daily episode live. Owners are founders until the agents are built; assign one founder per market. *Rates as of Oct 2026 — verify before quoting.*

| Phase | Columbia (Columbia Daily) | Los Angeles (LA Daily, History of Hollywood) | Both |
|---|---|---|---|
| **Pre-launch, weeks -4 to 0** | 60 qualified leads: banks and credit unions, health systems, real estate, home services, restaurants, campus-adjacent shops, plus businesses already advertising locally | 60 leads: real estate, moving and home services, credit unions, theaters and museums for Hollywood history | Host chosen with a written AI-content OK. Media-liability quote (F-LEGAL-01). Insertion-order template with the AI-voice clause. Rate card v0 and media kit v0 built on the trust story. Announcer persona designed. Ad-mode screen on. Sponsor registry and S6 built, or the DAI-only path confirmed |
| **Days 1 to 30** | Episodes run ad-free to set a completion baseline. Founders pitch the Founding offer from the sample episode, about 5 conversations a week | Same, plus pitch History of Hollywood as the evergreen slot | Week 4: first Founding Sponsors go live in Slot A. Day 30: rate card v1 from real downloads. Programmatic test starts if a host has approved |
| **Days 31 to 60** | First weekly reports. Ask for referrals. Second sponsor lined up for Slot B | Same, and a Market Bundle pitch | Objection log kept (AI voice, small audience). Cross-sell Studio Services to any sponsor who wants its own show |
| **Days 61 to 90** | Slot B opens if completion holds. Renewal talks at day 75 | Same | First Network Category Sponsor meetings. Strict-lane sponsor decision. Day-90 review |

**Funnel per market, per 30 days** *(inference)*: 60 leads, 20 conversations, 6 proposals, 2 signed. Columbia has 2 slots to sell by day 90. Los Angeles has 4 (LA Daily A and B, History of Hollywood A and B).

**Target by day 90** *(inference)*: 5 signed placements (Columbia Daily 2, LA Daily 2, History of Hollywood 1). Daily slots at about $75 Founding rate plus History of Hollywood at about $100 is about $400 a month. Conservative is about $250 (all five at the $50 floor). Optimistic is about $950 (dailies at 250 downloads per episode, $190 a slot, plus $180 for History of Hollywood). Inventory, not leads, caps month 1.

| Day-90 result | Then |
|---|---|
| 5 or more paid placements and at least 1 renewal | Keep going. Take the playbook to NYC and Chicago (wave 1) |
| 1 to 4 placements | Keep prospecting. Weigh Studio Services as the faster cash line |
| 0 placements after 30 or more conversations in a market | Sponsors do not value this audience yet. Stop prospecting there and revisit at about 400 downloads per episode |
| Programmatic net under $2.40 per 1,000 downloads | Turn it off where it hurts listening or ties up effort |

## 12. Open questions for the founders

1. Which founder owns Columbia sales and which owns Los Angeles?
2. Is a 12% ad-time cap, and one slot at launch, acceptable?
3. Should strict-lane shows ever carry sponsors?
4. Is the decline list (alcohol, gambling, cannabis, firearms, political) right?
5. Which host, once written quotes are in? Media insurers may price up or decline automated court and crime coverage (F-LEGAL-01).
