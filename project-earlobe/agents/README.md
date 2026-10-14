# Agents — the Curious & Creative Network workforce

122 agents across 10 desks. Full detail: [`docs/blueprint/agent-catalog.md`](../docs/blueprint/agent-catalog.md) · how they work together: [`docs/blueprint/how-it-works.md`](../docs/blueprint/how-it-works.md) · org chart: [`docs/blueprint/org-chart.md`](../docs/blueprint/org-chart.md).

Status: `built` = engine code exists · `next` = next build wave · `future` = designed, not scheduled. Tier: which Claude model tier runs it (`none` = deterministic code).

**Totals:** built 23 · future 17 · next 82

## Command (11)

Runs the network: orchestration, schedules, budgets, safety switches.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Budget / Cost Controller](command/budget-controller.md) | built | none | per-episode (checked before every run and every rewrite loop) | Keep every show inside its daily dollar cap so a runaway loop can never burn the month's budget. |
| [Kill Switch](command/kill-switch.md) | built | none | per-episode (checked at every stage boundary) | Stop one show or the whole network instantly, with one setting. |
| [Network Director](command/network-director.md) | built | none | always-on (dispatched per show cadence and per event) | Run every show end to end (sense, desk, write, verify, voice, publish) with no human in the loop, and stop cleanly when anything is unsafe. |
| [Build & Release Guard](command/release-guard.md) | next | none | per change (CI) + nightly | Nothing reaches production unless tests pass, configs are valid and a full dry run succeeds. |
| [Eval & Prompt Steward](command/eval-steward.md) | next | sonnet | per change (any prompt, tier mapping or schema change) + weekly | Prove the agents still do their jobs before any prompt or model change reaches production. |
| [Incident Commander](command/incident-commander.md) | next | sonnet | event:run.failed, event:run.anomaly, event:quota.low, event:security.alert | When something breaks, recover automatically, fail safe, and write down what happened. |
| [Programming Director](command/programming-director.md) | next | opus | weekly (Monday) + event:trend.brief | Decide what the network makes: which shows launch, grow, change or end, and the order markets roll out. |
| [Quota Sentinel](command/quota-sentinel.md) | next | none | cron "*/30 * * * *" (every 30 min) | See vendor quota walls coming before they stop production. |
| [Run Auditor / Observability](command/run-auditor.md) | next | haiku | always-on + cron "0 11 * * *" (daily digest) | Watch every run and say plainly when something drifts: cost, errors, latency or trust outcomes. |
| [Scheduler](command/scheduler.md) | next | none | always-on (cron table + event bus) | Fire every show, sensor and back-office job at the right local time, and fire event-driven shows the moment their trigger lands. |
| [Security Sentinel](command/security-sentinel.md) | next | haiku | always-on (inline screen on ingest) + weekly audit | Keep secrets safe, and keep hostile text in the news from steering the agents. |

## Sensors (16)

Always-on watchers: markets, courts, press releases, archives, breaking signals.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Beat Agent](sensors/beat-agent.md) | built | sonnet | always-on (poll every 15 min; beat memo twice daily) | Obsess over one market: know every outlet, agency and storyline, and surface every signal that matters before the morning brief. |
| [Breaking Detector](sensors/breaking-detector.md) | built | none | always-on (every 5 min via run_breaking / breaking-scan) | Decide, with fixed rules, when a national or global event is big enough for The Breaking Desk. |
| [Court Watch](sensors/court-watch.md) | built | haiku | always-on (every 30 min on court days) | Never miss a filing, ruling or sentencing that matters in the courts we cover. |
| [Archive Miner](sensors/archive-miner.md) | next | sonnet | weekly per series + on-demand from showrunner-evergreen | Dig public archives for true, sourced, rights-clear stories for the evergreen series. |
| [Case Development Watcher](sensors/case-development-watcher.md) | next | haiku | always-on (every 30 min) | Follow each tracked case across every court and agency, and fire a flash the moment it moves. |
| [Cold-Case Archivist](sensors/cold-case-archivist.md) | next | opus | weekly + on-demand | Build careful, fully sourced case files for unsolved cases where telling the story can help. |
| [Elections Watcher](sensors/elections-watcher.md) | next | haiku | always-on on election nights; daily otherwise | Report official election information only: who is running, who funds them, and what the official count says. |
| [Legislature Watcher](sensors/legislature-watcher.md) | next | haiku | always-on in session (every 30 min); weekly out of session | Track the bills, votes and hearings in statehouses and Congress that affect our markets. |
| [Press-Release Watcher](sensors/press-release-watcher.md) | next | haiku | always-on (poll every 15 min) | Catch every official announcement in each market minutes after it posts. |
| [Public Meetings Watcher](sensors/public-meetings-watcher.md) | next | sonnet | always-on (agendas daily; minutes and video after each meeting) | Read every agenda and set of minutes, so the network knows what government is about to do and what it just did. |
| [Records & Filings Watcher](sensors/records-filings-watcher.md) | next | haiku | cron "0 */4 * * *" (every 4 h) | Turn public paperwork into early stories: permits, business filings, licenses, layoffs and big property deals. |
| [Social Signal Watcher](sensors/social-signal-watcher.md) | next | haiku | always-on | Hear what is happening on social platforms early, without ever treating a post as proof. |
| [Trend & Search-Demand Scout](sensors/trend-scout.md) | next | sonnet | weekly + always-on demand alerts | Find topics people are searching for that nobody serves well, and prove it with data. |
| [Weather & Hazard Watcher](sensors/weather-hazard-watcher.md) | next | none | always-on (alerts every 5 min; forecasts 4x daily) | Bring official weather, air, fire and earthquake information into the network the moment it is issued. |
| [Civic Data Watcher](sensors/civic-data-watcher.md) | future | sonnet | cron "0 9 * * *" (daily) + weekly deltas | Find stories in the numbers: 311 calls, crime data, transit performance, inspections and budgets. |
| [Sports Watcher](sensors/sports-watcher.md) | future | haiku | always-on in season | Capture scores, schedules and big sports news for the sports spin-offs and high school feeds. |

## Editorial (17)

Turns signals into stories and stories into scripts, titles and show notes.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Assignment Editor](editorial/assignment-editor.md) | built | none | per-episode | Give every show the right stories: right market, right beat, right number, right lane. |
| [Copywriter](editorial/copywriter.md) | built | sonnet | per-episode (after PUBLISH) | Write the words that get an episode chosen: title, description, hooks, show notes and social posts. |
| [Producer / Scriptwriter](editorial/producer.md) | built | opus | per-episode (and per REWRITE loop) | Write the episode script: clear, conversational, and every factual line mapped to its claims. |
| [Story Desk](editorial/story-desk.md) | built | haiku | per-episode + always-on for the national/breaking scan | Turn a flood of raw Signals into a short list of distinct, scored stories. |
| [Case File Keeper](editorial/case-file-keeper.md) | next | opus | event:case.development + weekly | Keep one accurate, sourced, presumption-of-innocence file for every case the Case Tracker follows. |
| [Copy Editor (audio)](editorial/copy-editor.md) | next | sonnet | per-episode (after the Producer, before the Claim Extractor) | Make every script sound right out loud without changing what it claims. |
| [Follow-Up Editor](editorial/follow-up-editor.md) | next | haiku | per-episode (date extraction) + cron "0 9 * * *" (daily tickler) | Never drop a story: remember every date that matters and bring the story back when it arrives. |
| [Headline / Title Tester](editorial/headline-tester.md) | next | sonnet | per-episode + weekly learning report | Find out, with data, which titles and hooks actually earn listens. |
| [Localizer](editorial/localizer.md) | next | sonnet | event:desk.breaking + per-episode for national stories | Find the real local angle on big national stories, or keep them out of the local dailies. |
| [Researcher](editorial/researcher.md) | next | opus | per-episode (deeper packs on-demand) | Hand the Producer the context and primary records behind every story. |
| [Showrunner: Case Tracker](editorial/showrunner-case-tracker.md) | next | sonnet | weekly (Friday) + event:case.development | Run the live true-crime Case Tracker: the weekly best of the last 7 days and the development flashes. |
| [Showrunner: Courts Roundups](editorial/showrunner-courts.md) | next | sonnet | per-episode + weekly review | Run the courts roundups: what was filed, ruled and scheduled, in careful, fair language. |
| [Showrunner: Daily Briefs](editorial/showrunner-daily.md) | next | sonnet | per-episode (rundown) + weekly review | Own the morning daily briefs, market by market: format, rundown, tone and length. |
| [Showrunner: Evergreen & Archives](editorial/showrunner-evergreen.md) | next | sonnet | weekly + per-episode | Plan and run the evergreen series as seasons with arcs, from History of Hollywood to Cold Case Files. |
| [Showrunner: The Breaking Desk](editorial/showrunner-breaking.md) | next | sonnet | event:desk.breaking + weekly review | Run The Breaking Desk: fast, calm, and only what is confirmed. |
| [Spanish-Language Editions Editor](editorial/spanish-editions-editor.md) | next | opus | per-episode (after PUBLISH of the English edition) | Produce Spanish-language editions that are adapted for listeners, not just translated, and verified to the same standard. |
| [Showrunner: Niche Feeds](editorial/showrunner-niche.md) | future | sonnet | per-episode + weekly tuning | Run dozens of small, hyper-specific always-on feeds from templates, and pause any that run dry. |

## Trust Stack (14)

Independent checks every claim must pass before anything publishes.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Bias Checker](trust/bias-checker.md) | built | opus | per-episode | Catch loaded language, one-sided framing and missing perspectives before they air. |
| [Claim Extractor](trust/claim-extractor.md) | built | opus | per-episode (every revision) | List every checkable assertion in the script, including the ones the writer forgot to map. |
| [Corrections Agent](trust/corrections-agent.md) | built | sonnet | event:correction.opened | Fix mistakes fast and in public: show notes, feeds and on-air corrections. |
| [Fact Checker](trust/fact-checker.md) | built | opus | per-episode | Check that each claim, as worded, says exactly what the evidence says. |
| [Legal / Defamation Screener](trust/legal-screener.md) | built | opus | per-episode | Screen every script for defamation, privacy and legal risk before it can publish. |
| [Re-check Monitor](trust/recheck-monitor.md) | built | opus | cron "0 8 * * *" (daily: recheck --days 7); breaking and strict claims more often in the first 48 h | Keep checking published claims after they air, because stories change. |
| [Source Verifier (blind)](trust/source-verifier.md) | built | opus | per-episode | Re-source every claim blind, from scratch, and count only truly independent support. |
| [Standards Editor (rules engine)](trust/standards-editor.md) | built | none | per-episode (after the checkers, every revision) | Make the publish decision with fixed, auditable rules: PUBLISH, REWRITE, HOLD or KILL. |
| [Harm & Sensitivity Reviewer](trust/harm-sensitivity-reviewer.md) | next | opus | per-episode (strict and breaking lanes; sampled on the others) | Make sure coverage of crime, death and tragedy does not cause avoidable harm. |
| [Hoax Red Team](trust/hoax-red-team.md) | next | opus | weekly + before major releases | Attack our own trust stack with realistic hoaxes, so we find the holes before bad actors do. |
| [Originality Checker](trust/originality-checker.md) | next | haiku | per-episode | Make sure every script is in our own words, with only short, attributed quotes. |
| [Source Ledger Keeper](trust/source-ledger-keeper.md) | next | haiku | weekly + event:ownership.change | Keep the source map honest: who owns which outlet, which accounts are official, and which sources keep getting it wrong. |
| [Transparency Reporter](trust/transparency-reporter.md) | next | sonnet | cron "0 14 1 * *" (monthly, on the 1st) | Publish how the trust stack performed, every month, in plain language. |
| [Media Authenticity Checker](trust/media-authenticity-checker.md) | future | opus | per-episode when photos, video or audio are cited as evidence (mostly breaking) | Check whether photos, video and audio cited as evidence are real, original and unaltered. |

## Studio (9)

Voices, sound, disclosure and listen-back quality control.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Disclosure Agent](studio/disclosure-agent.md) | built | none | per-episode (before the gate) | Make sure every episode ends with the AI disclosure and carries it in its metadata. |
| [Sound Designer / Mixer](studio/sound-designer.md) | built | none | per-episode | Assemble each episode: voices, music, transitions and consistent loudness. |
| [Studio Voice (ElevenLabs)](studio/studio-voice.md) | built | none | per-episode (only after PUBLISH) | Turn each approved script line into audio in the right persona's voice. |
| [Art Director](studio/art-director.md) | next | sonnet | event:show.greenlit + per-episode (episode art)  | Make every show look like part of one network: cover art, episode art, thumbnails and social cards. |
| [Pronunciation Keeper](studio/pronunciation-keeper.md) | next | haiku | per-episode + event:qa.mispronunciation | Say every local name right, every time. |
| [QA Listener](studio/qa-listener.md) | next | haiku | per-episode (after the mix, before publish) | Listen back to every episode and catch what the script can't show: mispronunciations, glitches, silence and bad levels. |
| [Sonic Brand Librarian](studio/sonic-brand-librarian.md) | next | sonnet | on-demand + monthly rotation | Give the network and every show a recognizable, properly licensed sound. |
| [Voice Director](studio/voice-director.md) | next | sonnet | on-demand + weekly review | Cast, design and direct the network's original synthetic voices so each persona is consistent and clearly original. |
| [Studio Operator (computer use)](studio/studio-operator.md) | future | sonnet | on-demand | Drive UI-only audio engines such as NotebookLM and Meta Muse through computer use, as an optional second studio. |

## Distribution (11)

Feeds, platforms, video, clips, transcripts, new-show launches.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Feed Manager](distribution/feed-manager.md) | built | none | per-episode + on every correction or retraction | Keep every show's RSS feed valid, complete and honest. |
| [Publisher](distribution/publisher.md) | built | none | per-episode (after PUBLISH and, once live, QA PASS) | Put the finished episode on the host with complete notes, sources and a verification summary. |
| [Catalog & Platform Standing Steward](distribution/catalog-steward.md) | next | haiku | per show greenlight + weekly catalog audit + event:platform.flag | Keep the catalog clean so podcast apps treat us as a real network, not a spam farm. |
| [Clip Maker](distribution/clip-maker.md) | next | sonnet | per-episode | Cut the best 30-60 seconds of each episode into audiograms and vertical videos. |
| [Directory Sync Checker](distribution/directory-sync-checker.md) | next | none | cron "15 * * * *" (hourly) | Confirm every episode actually shows up on every platform, and say so fast when it doesn't. |
| [SEO / Metadata](distribution/seo-metadata.md) | next | sonnet | per-episode + monthly audit | Make every show and episode easy to find in podcast apps, search engines and YouTube. |
| [Show Launcher](distribution/show-launcher.md) | next | sonnet | event:show.greenlit | Spin up a complete new show from a template in a day or two: config, sources, bible, art, trailer and platform listings. |
| [Transcript & Accessibility](distribution/transcript-accessibility.md) | next | haiku | per-episode | Publish an accurate transcript, chapters and captions for every episode. |
| [Website Publisher](distribution/website-publisher.md) | next | none | event:episode.published + nightly rebuild | Run the network website: a page for every show, episode, source list, correction and trust report. |
| [YouTube / Video Packager](distribution/youtube-packager.md) | next | sonnet | per-episode | Turn every episode into a proper YouTube podcast episode: video, chapters, captions and playlists. |
| [Syndication Packager](distribution/syndication-packager.md) | future | haiku | per-episode for partner feeds | Package our briefs for other outlets: radio-ready cuts, smart-speaker briefings and news-site embeds. |

## Growth & Marketing (12)

Audience, social, newsletter, cross-promotion, analytics.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Analytics & Insights](growth/analytics-insights.md) | next | sonnet | cron "0 10 * * *" (daily ingest) + weekly InsightReport | Turn listening data into decisions: what to make more of, what to fix, what to stop. |
| [Audience Growth Strategist](growth/audience-growth-strategist.md) | next | sonnet | weekly (Monday) | Set the growth plan for every show and market, and decide where the effort goes each week. |
| [Brand Guardian](growth/brand-guardian.md) | next | sonnet | per-asset (before release) + monthly audit | Keep everything the public sees on-brand, honest about AI, and never impersonating anyone. |
| [Charts & Reviews Monitor](growth/charts-reviews-monitor.md) | next | haiku | cron "0 13 * * *" (daily) | Know where our shows rank and what listeners say about them, every day. |
| [Community & Listener Mail](growth/community-manager.md) | next | sonnet | always-on | Answer listeners, route their corrections and tips, and keep the community healthy. |
| [Cross-Promo Planner](growth/cross-promo-planner.md) | next | sonnet | weekly | Use our own shows to grow each other without annoying anyone. |
| [Market Launch Marketer](growth/market-launch-marketer.md) | next | sonnet | event:market.launch (30-day program) | Launch each new city loudly and locally, so the first month builds a real audience. |
| [Newsletter Editor](growth/newsletter-editor.md) | next | sonnet | per-episode (daily per market) + weekly network digest | Send a daily local newsletter that pairs with each brief and builds an audience we own. |
| [Partnerships Scout (local orgs & radio)](growth/partnerships-scout.md) | next | sonnet | weekly | Find local partners who make us more trusted and more heard: libraries, universities, radio, newsrooms and civic groups. |
| [Press & PR Agent](growth/press-pr-agent.md) | next | sonnet | event:market.launch, event:show.greenlit + weekly | Tell the network's story to the press: launches, milestones and the trust record. |
| [Social Media Manager](growth/social-media-manager.md) | next | sonnet | always-on (daily schedule) | Run the network's social accounts so local people find our shows where they already scroll. |
| [Paid Growth Manager](growth/paid-growth-manager.md) | future | sonnet | always-on while campaigns run (daily review) | Buy listeners only where it pays back, with hard daily caps. |

## Revenue (14)

Ads, sponsors, sales materials, B2B and Trust Stack customers.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Ad Ops (DAI, fill, brand safety)](revenue/ad-ops.md) | next | haiku | always-on | Run ad insertion cleanly and safely: the right ads, in the right places, never next to tragedy. |
| [Billing & Collections](revenue/billing-collections.md) | next | haiku | per insertion order or SOW + weekly AR run | Invoice correctly, collect on time, and reconcile every payment. |
| [Campaign Reporter](revenue/campaign-reporter.md) | next | haiku | weekly during each campaign + at campaign end | Show every sponsor exactly what they got. |
| [Grants Scout](revenue/grants-scout.md) | next | sonnet | weekly | Find and win grants and funding for local news and media innovation. |
| [Rate Card Manager](revenue/rate-card-manager.md) | next | sonnet | monthly + on-demand | Price inventory and sponsorships so we sell out at a fair price. |
| [Revenue Director](revenue/revenue-director.md) | next | sonnet | weekly | Own the revenue plan across ads, sponsors, grants, services and, later, the tools. |
| [Sales Deck & Media Kit Builder](revenue/media-kit-builder.md) | next | sonnet | cron "0 15 2 * *" (monthly refresh) + on-demand | Give every sales conversation a current, honest media kit and deck. |
| [Sponsor Prospector (local businesses)](revenue/sponsor-prospector.md) | next | sonnet | weekly per market + event:lead.inbound | Find and book local businesses that want to reach local listeners. |
| [Sponsor Read Writer](revenue/sponsor-read-writer.md) | next | sonnet | per-campaign | Write sponsor reads that work for the sponsor, sound natural, and are clearly ads. |
| [B2B White-Label Onboarding](revenue/white-label-onboarding.md) | future | sonnet | event:client.signed (B2B engine customers) | Onboard B2B customers to the Earlobe Engine so their audio product runs on our workflow under their brand. |
| [Content Licensing Agent](revenue/content-licensing-agent.md) | future | sonnet | weekly | Earn from the catalog by licensing shows and briefs to radio, platforms and publishers. |
| [Premium & Membership Manager](revenue/premium-membership-manager.md) | future | sonnet | weekly | Offer paid tiers superfans want: ad-free, early access and bonus deep dives. |
| [Programmatic Yield Optimizer](revenue/yield-optimizer.md) | future | sonnet | weekly | Earn the most from every unsold slot without hurting listening. |
| [Trust-Stack API Concierge](revenue/trust-api-concierge.md) | future | sonnet | always-on (support) + weekly account health | Help developers and newsrooms use the Trust Stack API well, and spot misuse. |

## Business Ops (11)

Intel, finance, compliance, vendors, knowledge, partner relations.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Chief of Staff](business-ops/chief-of-staff.md) | next | sonnet | cron "0 11 * * *" (07:00 ET daily brief; follows DST via the Scheduler) + weekly founder memo (Sunday) | Give Joshua and Janel one short morning brief: what shipped, what was stopped and why, money, and the few decisions only they can make. |
| [Competitive Watch](business-ops/competitive-watch.md) | next | sonnet | monthly per market + weekly chart and launch scan | Map every competitor for each market and format, and find the gaps we can own. |
| [Compliance & Platform Policy Watch](business-ops/compliance-policy-watch.md) | next | sonnet | weekly + event:policy.change + on-demand clearances | Keep every show, source and tool inside platform rules and the law, and clear new ones before we use them. |
| [Contracts & IP Clerk](business-ops/contracts-ip-clerk.md) | next | sonnet | on-demand + event:legal.threat + monthly register review | Keep the company's names, contracts, insurance and legal notices in order, and get real legal threats to a human within the hour. |
| [Finance / Bookkeeping Reporter](business-ops/finance-reporter.md) | next | sonnet | cron "0 12 * * *" (daily cost rollup) + monthly close (by business day 5) | Know what every show, market and product costs and earns, every day, in numbers an accountant can trust. |
| [Industry Intel](business-ops/industry-intel.md) | next | sonnet | always-on (daily scan) + weekly synthesis on the Opus tier | Know what is changing in AI audio, podcasting and local news before it hits us, starting with Liquid Studios. |
| [Knowledge Base Keeper](business-ops/knowledge-base-keeper.md) | next | sonnet | weekly + per change (docs lint in CI) | Keep the docs, the agent files and the code telling the same story. |
| [Partner / Investor Relations](business-ops/partner-investor-relations.md) | next | opus | 72 h before each partner or investor meeting (calendar-triggered) + monthly investor update | Walk the founders into every important meeting fully prepared, and keep partners and investors informed. |
| [Privacy Steward](business-ops/privacy-steward.md) | next | haiku | weekly + event:privacy.request | Collect as little personal data as we can, protect what we keep, and honor every privacy request on time. |
| [Vendor & Pricing Watch](business-ops/vendor-pricing-watch.md) | next | haiku | weekly + event:vendor.change | Catch every price, quota or terms change from our vendors before it hits the budget or breaks a workflow. |
| [Tools Productization Strategist](business-ops/product-strategist.md) | future | opus | monthly | Decide when and how the Trust Stack and the Earlobe Engine become products other people pay for. |

## C&C Studio Services (7)

The in-person offer: podcast setup, distribution and coaching for clients.

| Agent | Status | Tier | Runs | Mission |
|---|---|---|---|---|
| [Client Show Setup](services/client-show-setup.md) | next | sonnet | event:client.signed | Take a signed client from idea to a launch-ready show kit, so the founders' on-site day goes smoothly. |
| [Distribution Setup](services/distribution-setup.md) | next | sonnet | per client launch | Get each client's show live on Apple Podcasts, Spotify, YouTube and the other major apps, correctly the first time. |
| [Studio Services Intake](services/services-intake.md) | next | sonnet | event:lead.services + daily pipeline review | Turn every inquiry about C&C Studio Services into a qualified lead, a clear proposal and a booked call. |
| [Client Coaching / Training](services/client-coaching.md) | future | sonnet | per session + per client episode (feedback) | Make clients better podcasters: delivery, structure, interviewing and consistency. |
| [Client Post-Production](services/client-post-production.md) | future | sonnet | per client episode (on upload) | Turn a client's raw recording into a finished, published episode with notes, transcript and clips. |
| [Client Reporting](services/client-reporting.md) | future | haiku | cron "0 14 3 * *" (monthly, on the 3rd) | Show each client every month how their show is doing and what to do next. |
| [Field Ops Coordinator](services/field-ops-coordinator.md) | future | haiku | per on-site booking + weekly gear check | Make every in-person studio day run on time with the right gear, in the right place. |
