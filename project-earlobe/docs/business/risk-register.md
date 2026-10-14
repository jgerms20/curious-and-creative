# Risk register: what could go wrong, how likely, how bad, and who is watching

**The Curious & Creative Network · as of 2026-10-12 · DRAFT for Joshua and Janel.** Built from the [facts sheet](../research/facts-and-figures.md) (IDs like `F-LEGAL-11`), [legal and compliance](legal-and-compliance.md), [competitive landscape](competitive-landscape.md), [go-to-market](go-to-market.md), the [standards](../standards/README.md), the [agent roster](../../agents/README.md) and [`config/`](../../config/). **Not legal advice.** Scores are our judgement *(inference)*. *Costs, prices and platform rules: as of Oct 2026 — verify before buying.*

**How to read it.** Likelihood (L) and Impact (I): Low = 1, Med = 2, High = 3. Score = L x I, sorted high to low. **Owner agent** = the roster agent who watches the risk; names match the roster. Status tags in the mitigation column: **built** = in code today; **next** = designed, not built, so a gap today (23 of 122 agents are built); **decision** = needs Joshua or Janel. The Chief of Staff carries the top five into the Sunday founder memo, and scores are redone monthly.

## The short version

| Rank | Risk | Why it leads |
|---|---|---|
| 1 | **Audience stalls** | Thin AI feeds average about 69 downloads an episode (F-IPA-07). Our base case is 120 and the conservative case 40, all inference (F-AUD-03). Everything else matters only if people listen |
| 2 | **Defamation in court and crime coverage** | One wrong name on a crime story is the one event that can cost real money and trust |
| 3 | **Platform delisting** | Castro, the Podcast Index and Listen Notes already filter AI feeds (F-HOST-18) |
| 4 | **Ads do not accept or pay for AI audio** | The largest audio seller markets "human" as premium (F-HOST-17); Inception Point's synthetic shows are "no longer a revenue source" (F-IPA-08) |
| 5 | **Voice vendor and the human-show brand** | One vendor voices every show; a network scandal could rub off on the founders' human shows |

## The register

| # | Risk and evidence | L | I | Score | Mitigation (status) | Owner agent |
|---|---|---|---|---|---|---|
| 1 | **Audience stalls.** Feeds list but few listen; discovery is gated (F-HOST-18); AI share of new feeds is 25% to 45% (F-AUD-01) | 3 | 3 | **9** | Stage gates on measured downloads ([go-to-market](go-to-market.md)); owned channels (newsletter, site, clips) and local partners; Breaking Desk as the audience engine (500 base, F-AUD-04); pause a feed under its floor for 30 days. Growth agents are **next**: until built, the founders watch the numbers by hand | Audience Growth Strategist, Analytics & Insights, Programming Director |
| 2 | **Defamation or wrong-person error in court and crime coverage.** Libel per se if wrong; no Section 230 for our own scripts (F-LEGAL-11); same-name confusion is the classic automated error | 2 | 3 | **6** | Strict lane and Legal Screener (**built**); official-record-only naming and fair-report drafting; E&O plus lawyer review before auto-publish (**decision**); suppress first on a takedown; keep records 3+ years (F-LEGAL-08). **Gaps:** crime items in the dailies run the standard lane (CR-NE-1), no sealed-record marker (CR-NE-5, -6), no per-episode suppress (CR-NE-7) | Legal / Defamation Screener, Standards Editor, Contracts & IP Clerk |
| 3 | **Platform delisting or AI-spam filters.** Castro hid Inception Point; Podcast Index flags "low-effort AI"; YouTube's July 2025 "inauthentic content" rule (F-HOST-13, -18, F-IPA-10) | 2 | 3 | **6** | Pace caps, one feed per market, honest titles; disclosure in audio and metadata (**built**, Disclosure Agent); consolidated YouTube channels; owned feed domain; two hosts at 50+ shows; weekly directory audit; any flag freezes new launches. Catalog Steward and Directory Sync Checker are **next**, so manual until built | Catalog & Platform Standing Steward, Directory Sync Checker, Programming Director |
| 4 | **Ad market rejects or underpays AI content.** iHeart "Guaranteed Human" (F-HOST-17); curated ad stacks likely decline an unproven AI catalog (F-HOST-09); fill never measured (F-ADS-08); no advertiser survey | 2 | 3 | **6** | Local direct sponsors first; a programmatic test on 2 or 3 shows to get real fill; plan CPM $8 / $13 / $20 and never the $50 claim (F-ADS-06, -07); sponsors never see scripts (promise 9); sell "disclosed and verified"; hold 2 or 3 real sponsor talks early. All **next** | Revenue Director, Sponsor Prospector, Ad Ops, Rate Card Manager |
| 5 | **Costs outrun the plan.** A 7-minute brief costs about $2.00 Claude plus $0.56 to $1.16 voice against about $1.03 of ads (F-LLM-07, F-TTS-17, F-ADS-12); insurance, lawyer and PACER were under-budgeted; rewrite loops can run away | 3 | 2 | **6** | Per-show daily caps and a $60 network cap, Budget Controller and Kill Switch (**built**); Batch API for evergreen (F-LLM-05); Flash or hybrid voice (F-TTS-12, -23); apply for the voice grant (F-TTS-22). Wave 1 caps already sum to $59, so more shows need a bigger envelope (**decision**). Finance Reporter **next** | Budget Controller, Finance / Bookkeeping Reporter, Network Director |
| 6 | **Voice-vendor dependence (ElevenLabs).** Starter plans hard-stop (F-TTS-02); concurrency Creator 5, Pro 10, Scale 15 (F-TTS-18); Enterprise price is a placeholder (F-TTS-07); API vs subscription rights unresolved (conflict C1); news-use rules unknown | 2 | 3 | **6** | Studio Voice sits behind an adapter (**built**); qualify a second engine by blind listening before it is needed (Google Chirp 3 HD, about $0.03 a minute, F-TTS-23); keep Voice Design prompts and a persona register so voices can be rebuilt; get news-use terms in writing; the grant reverts to Free after 12 months (F-TTS-22) | Voice Director, Studio Voice, Vendor & Pricing Watch |
| 7 | **Brand risk to the founders' flagship human shows.** A flag, a correction scandal or an "AI slop" label rubs off on shows people value as human-made (90% prefer human-made media, F-AUD-06, advocacy). If human and network shows share an Apple or Spotify account, enforcement may not stop at the AI feeds *(inference)* | 2 | 3 | **6** | Mostly **decisions:** separate feeds, art family and hosts; never clone a founder's or any real person's voice (F-LEGAL-16); cross-promote from human shows to AI feeds only by choice; ask Apple and Spotify whether enforcement is per show or per account, and use separate accounts if per account; the pipeline never touches human-show feeds; a public "How this show is made" page | Brand Guardian, Cross-Promo Planner, Compliance & Platform Policy Watch |
| 8 | **Insurance declined, priced up or AI-excluded.** Automated court and crime may be restricted or declined; a misdescribed pipeline can void cover (F-LEGAL-01) | 2 | 3 | **6** | Broker quotes before any strict-lane auto-publish; ask about generative-AI exclusions; describe the pipeline accurately; use trust-log numbers at renewal. If declined, strict lanes stay naming-light or paused (**decision**). Placeholder $6,000 a year | Contracts & IP Clerk |
| 9 | **A hallucination or factual error reaches air.** About 45% of AI-assistant news answers had a significant issue (F-AUD-07, low-med); no person reads before publish | 3 | 2 | **6** | Claim Extractor, blind Source Verifier, Fact Checker, Bias Checker and Legal Screener, then fixed rules; two independent sources (three for breaking); fail closed; 7-day re-check; dated public corrections (all **built**). Residual: the checkers are all models and may share blind spots *(inference)*: Eval Steward and Hoax Red Team are **next** | Standards Editor, Source Verifier, Fact Checker, Re-check Monitor, Corrections Agent |
| 10 | **Court and government data access.** CourtListener coverage is partial (F-DATA-01); portals often bar bulk automation (F-DATA-10); PACER can reach $450 to $1,800 a month (F-DATA-02); all 43 market feeds are unverified (F-DATA-04); the `dsc` / `scd` id mismatch (C11) | 3 | 2 | **6** | CourtListener first; PACER capped at $150 to $300 a month; clear each portal's terms before scraping; fix feeds by autodiscovery and the court id; dated snapshots; "no data, no episode". Court Watch **built**, the rest **next** | Court Watch, Case Development Watcher, Compliance & Platform Policy Watch, Source Ledger Keeper |
| 11 | **Hoax or poisoned source.** A fake press release, doctored media or hostile text in a feed steers an episode | 2 | 3 | **6** | Signals are untrusted; social posts are leads, never proof; one wire or owner group counts as one source ([`owners.yaml`](../../config/owners.yaml)); Breaking Desk HOLD rule (**built**). Security Sentinel and Hoax Red Team **next**; Media Authenticity Checker `future` | Security Sentinel, Hoax Red Team, Breaking Detector |
| 12 | **Harm to victims, minors and families** (crime, cold cases). Hard stops on naming minors and sexual-assault victims (NEVER-2, -3) | 2 | 3 | **6** | Gate rule L2 and crime rules (**built**); Harm & Sensitivity Reviewer **next**; suppress first on any family or minor complaint; no uncharged suspects | Harm & Sensitivity Reviewer, Standards Editor, Privacy Steward |
| 13 | **Usage limits and quotas.** Claude spend and rate limits, ElevenLabs credits, search at $10 per 1,000 (F-LLM-04), CourtListener about 5,000 calls an hour, GDELT 1 request per 5 seconds (F-DATA-03), about 96,900 Actions minutes a month at Dominate (F-INFRA-02) | 2 | 2 | **4**, 6 at Scale | Quota Sentinel forecasts walls 72 hours out and throttles niche, then evergreen, then dailies, Breaking Desk last (**next**); Scheduler staggers time zones; ask for higher limits before each stage; the fail-safe is to skip an episode (promise 7) | Quota Sentinel, Budget Controller, Scheduler, Incident Commander |
| 14 | **Key-person.** Two founders hold every account, the spending envelope, the kill switch and the legal-threat call | 2 | 2 | **4** | Both founders admin on Apple, Spotify, host, ElevenLabs, Anthropic, GitHub, domain and bank, with recovery codes in a shared vault (**decision**); a runbook and decision log; Chief of Staff yes/no lines carry a default and a deadline; a media lawyer on call; a "pause all" drill (`all: true` in [`killswitch.yaml`](../../config/killswitch.yaml)) | Chief of Staff, Knowledge Base Keeper, Contracts & IP Clerk |
| 15 | **Revenue plan leans on unproven lines.** The model's B2B rate is 46x to 161x the only audio anchor (F-IPA-09); sponsor rates imply a CPM of $92 to $461 against $17 to $22 sourced (F-ADS-14) | 2 | 2 | **4** | Keep B2B, API and services out of the network-only net; validate with 2 or 3 buyers first; plan cash on the conservative case, where the network alone loses about $25k in year 1 | Revenue Director, Tools Productization Strategist, Studio Services Intake |
| 16 | **Copyright, close paraphrase, source licenses.** Facts are free, wording is not (F-LEGAL-12); States Newsroom is CC BY-NC-ND, so own words plus a link (F-DATA-11); AI-only output may be unprotectable | 2 | 2 | **4** | Own words, one short attributed quote at most, credit and link; no scraping of licensed archives; licensing talks with local outlets and AP (P2). **Gap:** no deterministic text-overlap check (NE-10); Originality Checker **next** | Originality Checker, Contracts & IP Clerk |
| 17 | **Name and trademark collision.** *Cold Case Files* is an A&E title; *Columbia Daily* and *LA Daily* echo papers; "Curious" is crowded | 2 | 2 | **4** | Clearance before launch (attorney $500 to $2,000 a mark, F-LEGAL-02); file Class 41 at $350 (F-LEGAL-03); rename early, because late is costly | Contracts & IP Clerk |
| 18 | **A rival moves in.** Google, ElevenLabs GenFM, Spotify, public radio, or Liquid Studios adding verification | 2 | 2 | **4** | Go deeper than they will (courts, municipal documents, visible sourcing); partner with radio first; stay vendor-agnostic; Liquid Studios as vendor or partner is an option | Competitive Watch, Industry Intel |
| 19 | **Rules change.** Platform AI policies move (C9); EU AI Act Art. 50 from 2026-08-02; California SB 942 delays (F-LEGAL-13) | 3 | 1 | **3** | One disclosure standard, spoken at the end and in metadata, already exceeds most rules; weekly policy scan and quarterly legal watch; geo-limit the EU until reviewed | Compliance & Platform Policy Watch, Disclosure Agent |
| 20 | **A persona resembles a real person.** Voice-likeness laws bite (F-LEGAL-16) | 1 | 2 | **2** | Voices designed from scratch and registered as original; no invented backstories; Brand Guardian reviews every public asset | Voice Director, Brand Guardian |

## Tripwires: what happens automatically

| Trigger | Action | Where it lives |
|---|---|---|
| A show reaches 80% of its daily cap | Warning in the log | [`budgets.yaml`](../../config/budgets.yaml) (**built**) |
| Network reaches $60 a day | Only the Breaking Desk may still run | `budgets.yaml` (**built**) |
| Kill Switch set (`EARLOBE_KILL` or `killswitch.yaml`) | A killed show produces nothing | Kill Switch (**built**) |
| A vendor quota wall is under 72 hours away | Throttle niche, evergreen, dailies; Breaking Desk last | Quota Sentinel (**next**) |
| Published breach of a hard stop, or a credible legal threat | Pull within 1 hour; owners told within 1 hour | Corrections policy C3, COR-4 |
| A directory hides, flags or delists a feed | Freeze all new launches network-wide; audit within 24 hours *(inference)* | Catalog Steward (**next**) |
| A feed sits under its audience floor for 30 days | Pause or merge | Catalog Steward (**next**) |
| Programmatic fill under 30% after 90 days (F-ADS-08) | Stop programmatic growth; lean on sponsors and services *(inference)* | Revenue Director (**next**) |
| Cost per episode above 1.5x the model for 2 weeks | Pause the newest feeds *(inference)* | Budget Controller |

## Mitigations missing today

| Missing | Covers risks | Needed before |
|---|---|---|
| Strict lane for crime items inside the dailies (CR-NE-1); sealed-record marker; per-episode suppress | 2, 12 | T+0 |
| Insurance bound and lawyer review | 2, 8 | T+0 (legal P0) |
| Chief of Staff 07:00 brief, Incident Commander, Quota Sentinel | 5, 13, 14 | T+0 to T+5 weeks |
| Catalog Steward, Directory Sync Checker | 3 | Wave 1 |
| Security Sentinel, Hoax Red Team, Originality Checker | 11, 16 | Wave 1 |
| Analytics & Insights, Transparency Reporter | 1, 9 | Gate A (needed to measure it) |
| Second voice engine qualified; second host | 6, 3 | Gate B |

## Founder decisions that lower risk

| Decision | Risks | Suggested default |
|---|---|---|
| Separate accounts and branding for human shows vs the network; ask the platforms how enforcement works | 3, 7 | Yes, before T+0 |
| Human sign-off on court, crime and Breaking Desk naming for the first 30 clean days | 2, 12 | Yes (legal P0, item 3); an extra input, never a gate override |
| Both founders admin on every account; recovery codes in a shared vault | 14 | Yes, this week |
| Name an accountable editor of record and a deputy | 2, 14 | Yes, before T+0 |
| Walk away from strict lanes if E&O is declined | 2, 8 | Yes: stay naming-light until covered |

*Sources: the facts sheet and its notes, [legal and compliance](legal-and-compliance.md) sections 1 to 12, [crime and courts rules](../standards/crime-and-courts-rules.md), [corrections policy](../standards/corrections-policy.md), [`budgets.yaml`](../../config/budgets.yaml), [cost-out and ROI](../../finance/cost-out-and-roi.md).*
