# Agent Catalog: the Curious & Creative Network

**Project Earlobe** · Curious & Creative LLC (Joshua German, Janel Moore) · v1.0, October 11, 2026

This is the complete roster of agents that run the network: **122 agents across 10 desks**, covering the whole business, not only the newsroom. **23 are built** (in the v1 engine), **82 are next** (the next build wave, sequenced below) and **17 are future** (designed, not scheduled).

The network publishes with **no human gate**. Sensors find stories, the Producer writes them, and the Trust Stack checks every claim against independent sources. The Standards Editor, which is plain code and not a model, decides PUBLISH, REWRITE, HOLD or KILL. Joshua and Janel get a daily brief and own the decisions that should stay human: money above the approved envelope, new markets, contracts, legal threats and statements in the company's name. They never approve individual episodes.

The roster serves all four products: **(1) the Network** (owned shows, ad revenue), **(2) the Trust Stack** (verification as a product), **(3) the Earlobe Engine** (this workflow as a product) and **(4) C&C Studio Services** (in-person podcast setup and distribution for businesses and people). The plan is to build the network first and sell the tools later, so most agents serve product 1 today and are built to be reused for products 2-4.

## How to read this catalog

1. **Desk summary tables** come first in each desk section: one row per agent with its id, status, tier, cadence and mission.
2. **Detailed entries** follow each table: mission, what it does (3-6 sentences), inputs, outputs, tools, who it reports to, how many instances run, the code module and KPIs.
3. The **[Expansion roster](#expansion-roster)** at the end lists the next 20 markets and more than 40 show and feed ideas, with the agents each one needs.

Every agent `id` is kebab-case and unique. It is also the name of the agent's instruction file, `agents/<desk>/<id>.md` (format: [`agents/_TEMPLATE.md`](../../agents/_TEMPLATE.md)). Contracts named in inputs and outputs are the dataclasses in [`earlobe/schemas.py`](../../earlobe/schemas.py). Names marked *(proposed)* are new contracts. Per Convention 8, each is added to `schemas.py` and `json-contracts.md` together when its agent is built.

### Status

| Status | Meaning | Count |
|---|---|---|
| **built** | Engine module is part of v1, per the module map in [`earlobe/README.md`](../../earlobe/README.md). The `code` field names the module. | 23 |
| **next** | The next build wave. Sequenced in [Build order](#build-order-for-the-next-wave) below. | 82 |
| **future** | Designed and scoped, not scheduled. | 17 |

**Built means the module is in the v1 module map, not that the agent is finished.** Entries describe each one's "next increment". On disk as of this writing, 11 built agents have their modules written (sensors, desk, trust): `beat-agent`, `court-watch`, `breaking-detector`, `story-desk`, `assignment-editor`, `claim-extractor`, `source-verifier`, `fact-checker`, `bias-checker`, `legal-screener`, `standards-editor`. The modules for the other 12 are still landing in the current engine build (`producer/`, `studio/`, `publish/`, `monitor/`, `pipeline.py`): `network-director`, `budget-controller`, `kill-switch`, `producer`, `copywriter`, `corrections-agent`, `recheck-monitor`, `studio-voice`, `sound-designer`, `disclosure-agent`, `publisher`, `feed-manager`. The Knowledge Base Keeper re-checks this split on every change.

### Model tiers

Tiers only, never model version strings (Convention 4). Concrete model IDs live in `EARLOBE_MODEL_OPUS`, `EARLOBE_MODEL_SONNET` and `EARLOBE_MODEL_HAIKU`.

| Tier | Used for | Agents |
|---|---|---|
| **Opus tier** | Script writing, the trust checkers, standards-adjacent judgment, research synthesis, meeting prep | 17 |
| **Sonnet tier** | Beat monitoring, copywriting, show notes, marketing, sales, operations, showrunning | 61 |
| **Haiku tier** | Dedupe, triage, classification, mechanical checks, digests | 27 |
| **none** | Deterministic code with no model call (gate, kill switch, budget, scheduler, TTS, mixer, publisher, feeds) | 17 |

Some agents pair code with a tier. In that case the code makes the decision and the model only writes words, as in the Run Auditor and the Transparency Reporter. The entry says so.

### Cadence (`runs`)

`always-on` = continuous polling or a long-running worker · `cron "<expr>"` = scheduled, in **UTC** unless the entry says local time (the Scheduler converts each show's local time so daylight-saving changes don't shift episodes) · `per-episode` = once per episode run (and per REWRITE loop where noted) · `event:<name>` = fired by an event below · `weekly` / `monthly` · `on-demand`.

### Events

| Event | Fired when |
|---|---|
| `event:budget.exceeded` | a show hit its daily cap |
| `event:case.development` | a tracked case moved (charge, plea, ruling, verdict, sentencing); triggers a Case Tracker flash |
| `event:client.signed` | a services or B2B client signed |
| `event:correction.opened` | a correction was opened (recheck, listener or outlet) |
| `event:desk.breaking` | Breaking Detector flagged a national/global event (shows.yaml trigger for breaking-desk) |
| `event:episode.published` | an episode went live on the host |
| `event:lead.inbound` | a sponsor inquiry arrived |
| `event:lead.services` | a Studio Services inquiry arrived |
| `event:legal.threat` | a legal threat, subpoena or takedown demand arrived |
| `event:market.launch` | a new market is going live |
| `event:ownership.change` | an outlet changed owner group |
| `event:platform.flag` | a directory hid, flagged or delisted one of our feeds |
| `event:policy.change` | a platform or legal policy that affects us changed |
| `event:privacy.request` | a listener asked to access or delete their data |
| `event:qa.mispronunciation` | QA Listener heard a likely mispronunciation |
| `event:quota.low` | a vendor quota wall is within 72 h |
| `event:run.anomaly` | the Run Auditor saw drift from baseline |
| `event:run.failed` | a run, render or directory sync failed |
| `event:security.alert` | possible injection, leaked key or unusual API use |
| `event:show.greenlit` | Programming Director approved a new show |
| `event:trend.brief` | Trend Scout filed a TopicBrief |
| `event:vendor.change` | a vendor changed price, quota or terms |

### Tools

| Tool | What it is | Agents using it |
|---|---|---|
| `sql` | the run store (`store.py`, sqlite now; the Supabase migration later) | 33 |
| `web_search` | model web-search tool (`LLM.research`) | 27 |
| `email` | send/read email (newsletter platform or transactional email) | 26 |
| `web_fetch` | fetch a specific URL (stdlib urllib in `sensors/base.py`, or the model's fetch tool) | 25 |
| `rss` | RSS/Atom polling (`sensors/rss.py`, `sensors/base.py`) | 14 |
| `docs` | read/write documents (repo `docs/`, shared drive) | 13 |
| `host_api` | podcast host API (`publish/hosts.py`: LocalHost, TransistorHost) and directory lookups | 13 |
| `ffmpeg` | ffmpeg on PATH (render, loudness, clips, video) | 8 |
| `none (LLM only)` | a single isolated model call with no tools | 8 |
| `analytics_api` | host, Apple, Spotify, YouTube, newsletter and social analytics | 7 |
| `ci` | CI runner (GitHub Actions): tests, dry runs, schedules | 7 |
| `courtlistener` | CourtListener v4 API (`sensors/courtlistener.py`, `COURTLISTENER_TOKEN`) | 7 |
| `calendar` | founders' calendar (read, book, prep) | 6 |
| `canva` | Canva brand templates (design) | 5 |
| `crm` | customer relationship manager for sponsors, partners and clients | 5 |
| `stt` | speech-to-text (ElevenLabs STT or equivalent; verify) | 5 |
| `ad_server_api` | dynamic ad insertion / ad server API | 4 |
| `elevenlabs` | ElevenLabs API (TTS, voice design, pronunciation dictionaries) | 4 |
| `none` | deterministic code only, no external tool | 4 |
| `social_api` | official social platform APIs, used within their terms | 4 |
| `computer_use` | model computer-use tool driving a web UI | 3 |
| `gdelt` | GDELT DOC 2.0 discovery and velocity (`sensors/gdelt.py`) | 3 |
| `payments_api` | payment processor (invoices, payment links, reconciliation) | 3 |
| `open_data_api` | city/county open data portals (Socrata, ArcGIS) and agency APIs | 2 |
| `youtube_api` | YouTube Data API | 2 |
| `accounting_api` | bookkeeping system | 1 |
| `ad_platform_api` | paid acquisition ad platforms | 1 |
| `image_gen` | image model with a commercial license | 1 |

### Reports to

`reports_to` names the agent whose instructions this one follows and whose KPIs it rolls up into. **founders (Joshua German, Janel Moore)** means the humans: they get it in the Chief of Staff brief. Reporting lines carry instructions and metrics. They never create a human approval step for an episode.

### Proposed contracts

These shapes appear in the roster but are not in `schemas.py` yet: `CaseFile`, `ClipSpec`, `HarmReport`, `InsightReport`, `MeetingDigest`, `QAReport`, `ResearchPack`, `ShowSpec`, `TopicBrief`. Existing contracts used throughout: `Signal`, `Story`, `StoryTriage`, `Script`, `Claim`, `Source`, `VerifierReport`, `FactCheckReport`, `BiasReport`, `LegalReport`, `LegalIssue`, `GateDecision`, `Copy`, `Episode`, `Correction`, `AgentRun`.

## How the desks fit together

```text
COMMAND   scheduler -> kill-switch -> budget-controller -> network-director        run-auditor watches everything
              |                                                                        incident-commander recovers
SENSORS   beat-agent (per market) + court-watch, press, meetings, records, legislature, weather, social, elections
          breaking-detector (national) . archive-miner . cold-case-archivist . trend-scout
              | Signal
EDITORIAL story-desk -> assignment-editor (lane) -> showrunner (rundown) -> researcher -> producer -> copy-editor
              | Script + Claim map (disclosure-agent appends the AI outro)
TRUST     claim-extractor -> [source-verifier (blind) | bias-checker | legal-screener | harm | originality]
          -> fact-checker -> standards-editor (gate.py)
               PUBLISH -> studio      REWRITE -> producer (lane max)      HOLD -> wait 15 min (breaking only)      KILL -> trust log
STUDIO    pronunciation-keeper -> studio-voice -> sound-designer -> qa-listener (PASS / RERENDER / FAIL)
DISTRIB.  publisher -> feed-manager -> directory-sync . website . transcripts . youtube . clips      catalog-steward guards
GROWTH    social . newsletter . cross-promo . community . analytics -> programming-director (what to make next)
REVENUE   ad-ops (markers, brand safety) . sponsors . sponsor reads (legal ad mode) . billing
AFTER     recheck-monitor (7 days) -> corrections-agent -> reissued notes/feed + on-air correction + trust log
BUSINESS  chief-of-staff brief <- finance . intel . compliance . contracts . privacy        SERVICES intake -> setup -> distribution
```

## Build order for the next wave

The next wave is large, so it ships in five steps. Each step makes the network safer or more valuable before the next one starts.

**N1: Protect what's live** (20 agents). Before the Nov 1, 2026 daylight-saving change and the Nov 3, 2026 general election. The seven live shows need audio QA, harm and originality screens, election rules, change control, incident handling and a founders' brief before anything else grows.

`scheduler`, `elections-watcher`, `release-guard`, `eval-steward`, `run-auditor`, `incident-commander`, `quota-sentinel`, `security-sentinel`, `hoax-red-team`, `qa-listener`, `harm-sensitivity-reviewer`, `originality-checker`, `pronunciation-keeper`, `copy-editor`, `compliance-policy-watch`, `contracts-ip-clerk`, `chief-of-staff`, `catalog-steward`, `industry-intel`, `partner-investor-relations`

**N2: Feed the shows already on air** (18 agents). Better sources, research and format owners for Columbia Daily, LA Daily, The Breaking Desk, LA Courts, Case Tracker, Cold Case Files and History of Hollywood.

`press-release-watcher`, `case-development-watcher`, `archive-miner`, `cold-case-archivist`, `researcher`, `case-file-keeper`, `follow-up-editor`, `showrunner-daily`, `showrunner-breaking`, `showrunner-courts`, `showrunner-case-tracker`, `showrunner-evergreen`, `voice-director`, `sonic-brand-librarian`, `source-ledger-keeper`, `transparency-reporter`, `weather-hazard-watcher`, `knowledge-base-keeper`

**N3: Get heard** (18 agents). Distribution polish and the core marketing machine, so the shows find listeners.

`transcript-accessibility`, `seo-metadata`, `website-publisher`, `directory-sync-checker`, `clip-maker`, `youtube-packager`, `art-director`, `headline-tester`, `audience-growth-strategist`, `analytics-insights`, `social-media-manager`, `newsletter-editor`, `community-manager`, `brand-guardian`, `charts-reviews-monitor`, `cross-promo-planner`, `press-pr-agent`, `privacy-steward`

**N4: Earn** (14 agents). Direct local sponsorship, ad ops, billing, books, and Studio Services as the first cash line.

`revenue-director`, `ad-ops`, `sponsor-prospector`, `rate-card-manager`, `media-kit-builder`, `sponsor-read-writer`, `campaign-reporter`, `billing-collections`, `grants-scout`, `finance-reporter`, `vendor-pricing-watch`, `services-intake`, `client-show-setup`, `distribution-setup`

**N5: Scale markets and shows** (12 agents). Wave 1 (NYC, Chicago), then the next 20 markets and the niche-feed layer.

`programming-director`, `trend-scout`, `show-launcher`, `public-meetings-watcher`, `records-filings-watcher`, `legislature-watcher`, `social-signal-watcher`, `localizer`, `spanish-editions-editor`, `market-launch-marketer`, `partnerships-scout`, `competitive-watch`

## Command desk

Runs the machine itself: dispatch, money, safety switches, health monitoring and change control. The Network Director is the desk lead. Every other desk's work starts with a Scheduler dispatch and passes the Kill Switch and the Budget Controller first. *Hosting and CI details (GitHub Actions schedules): as of Oct 2026, verify before relying on them.*

11 agents: 3 built, 8 next, 0 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`network-director`](#network-director) | Network Director | built | none | always-on (dispatched per show cadence and per event) | Run every show end to end (sense, desk, write, verify, voice, publish) with no human in the loop, and stop cleanly when anything is unsafe. |
| [`programming-director`](#programming-director) | Programming Director | next | opus | weekly (Monday) + event:trend.brief | Decide what the network makes: which shows launch, grow, change or end, and the order markets roll out. |
| [`scheduler`](#scheduler) | Scheduler | next | none | always-on (cron table + event bus) | Fire every show, sensor and back-office job at the right local time, and fire event-driven shows the moment their trigger lands. |
| [`budget-controller`](#budget-controller) | Budget / Cost Controller | built | none | per-episode (checked before every run and every rewrite loop) | Keep every show inside its daily dollar cap so a runaway loop can never burn the month's budget. |
| [`quota-sentinel`](#quota-sentinel) | Quota Sentinel | next | none | cron "*/30 * * * *" (every 30 min) | See vendor quota walls coming before they stop production. |
| [`kill-switch`](#kill-switch) | Kill Switch | built | none | per-episode (checked at every stage boundary) | Stop one show or the whole network instantly, with one setting. |
| [`run-auditor`](#run-auditor) | Run Auditor / Observability | next | haiku | always-on + cron "0 11 * * *" (daily digest) | Watch every run and say plainly when something drifts: cost, errors, latency or trust outcomes. |
| [`incident-commander`](#incident-commander) | Incident Commander | next | sonnet | event:run.failed, event:run.anomaly, event:quota.low, event:security.alert | When something breaks, recover automatically, fail safe, and write down what happened. |
| [`eval-steward`](#eval-steward) | Eval & Prompt Steward | next | sonnet | per change (any prompt, tier mapping or schema change) + weekly | Prove the agents still do their jobs before any prompt or model change reaches production. |
| [`release-guard`](#release-guard) | Build & Release Guard | next | none | per change (CI) + nightly | Nothing reaches production unless tests pass, configs are valid and a full dry run succeeds. |
| [`security-sentinel`](#security-sentinel) | Security Sentinel | next | haiku | always-on (inline screen on ingest) + weekly audit | Keep secrets safe, and keep hostile text in the news from steering the agents. |

<a id="network-director"></a>
### `network-director`: Network Director

> Run every show end to end (sense, desk, write, verify, voice, publish) with no human in the loop, and stop cleanly when anything is unsafe.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | always-on (dispatched per show cadence and per event) | founders (Joshua German, Janel Moore) | `earlobe/pipeline.py (run_show, run_breaking, run_evergreen) + earlobe/cli.py` |

The orchestrator. For each show it checks the Kill Switch and the Budget Controller, pulls Signals for the show's market and beats, has the Story Desk cluster and score them, the Assignment Editor build the rundown, the Producer write and the trust loop decide. Only a PUBLISH decision moves on to Studio Voice, the mixer, the Publisher and the Feed Manager; HOLD schedules a re-check and KILL logs and stops. Every agent call is wrapped in an AgentRun envelope, so cost and provenance are recorded for every episode. It makes no editorial judgments of its own: it wires agents together through the contracts in schemas.py and enforces their order.

- **Inputs:** config/shows.yaml; Scheduler dispatch (show_id, slot time); event:desk.breaking; Kill Switch and Budget Controller state
- **Outputs:** Episode; AgentRun (one per agent call); run summary in the store
- **Tools:** `sql`
- **Instances:** single orchestrator; one run per show per cadence slot, shows run in parallel
- **KPIs:**
  - on-time publish rate per show (target >= 98% of scheduled slots)
  - runs that end in a logged decision (target 100%: no silent failures)
  - median minutes from dispatch to published daily brief (target < 30)
  - cost per published episode vs the show's budget

<a id="programming-director"></a>
### `programming-director`: Programming Director

> Decide what the network makes: which shows launch, grow, change or end, and the order markets roll out.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Opus tier | weekly (Monday) + event:trend.brief | `network-director` | — |

Reads the week's InsightReport, TopicBriefs from the Trend Scout, cost per episode from the Finance Reporter and kill/correction rates from the trust log, then writes a one-page programming memo. It greenlights new shows from templates (a ShowSpec handed to the Show Launcher), pauses feeds that have run out of news or audience, and moves shows between waves in shows.yaml. Greenlights inside the approved monthly budget envelope go through automatically; anything that raises the envelope or opens a new market goes to Joshua and Janel as a one-line yes/no in the Chief of Staff brief. Decisions follow written rules (audience trend, cost per listener, source availability), so every call can be explained afterwards.

- **Inputs:** InsightReport (proposed); TopicBrief (proposed); finance ledger; public trust log; config/shows.yaml
- **Outputs:** weekly programming memo; ShowSpec (proposed); shows.yaml change requests (through the Release Guard)
- **Tools:** `sql`, `web_search`
- **Instances:** single
- **KPIs:**
  - launched shows still running after 90 days
  - network weekly listeners, week over week
  - cost per engaged listener by show
  - days from accepted TopicBrief to first episode

<a id="scheduler"></a>
### `scheduler`: Scheduler

> Fire every show, sensor and back-office job at the right local time, and fire event-driven shows the moment their trigger lands.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | none (code) | always-on (cron table + event bus) | `network-director` | — |

Turns each show's cadence in shows.yaml into concrete run times, computing UTC from local_time and tz instead of trusting fixed UTC crons. That matters right now: the current crons are fixed UTC, so when US daylight saving time ends on Nov 1, 2026 the 06:00 daily briefs would start landing at 05:00 local. It also dispatches event cadences (desk.breaking with its 30-minute minimum gap, case.development flashes), staggers jobs so API rate limits are not all hit in the same minute, and logs every dispatch so the Run Auditor can spot missed slots. v1 hosting is GitHub Actions schedules calling the CLI; the same dispatch table can move to a long-running worker later.

- **Inputs:** config/shows.yaml cadences; agent cadences in this catalog; event bus
- **Outputs:** dispatch log; run requests to network-director
- **Tools:** `ci`, `sql`
- **Instances:** single
- **KPIs:**
  - missed or late dispatches (target 0 per week)
  - local-time accuracy across DST changes (target 100%)
  - event-to-dispatch latency for desk.breaking (target < 60 s)

<a id="budget-controller"></a>
### `budget-controller`: Budget / Cost Controller

> Keep every show inside its daily dollar cap so a runaway loop can never burn the month's budget.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode (checked before every run and every rewrite loop) | `network-director` | `earlobe/monitor/budget.py` |

within_budget(store, show_id, day) sums the day's AgentRun usd_estimate for the show and compares it with the cap in config/budgets.yaml. Over budget means the run is skipped and logged, not degraded: the network would rather miss an episode than ship a cheaper, less-checked one. Rewrite loops and breaking-lane HOLD re-checks count against the same cap, which bounds the worst case per show. Next increment: a network-wide monthly envelope and per-desk caps for the growth, revenue and business-ops agents.

- **Inputs:** AgentRun records; config/budgets.yaml
- **Outputs:** allow / deny per run; event:budget.exceeded
- **Tools:** `sql`
- **Instances:** one check per show per run; one cap per show
- **KPIs:**
  - days any show exceeded its cap (target 0)
  - monthly forecast vs actual spend (within 10%)
  - runs skipped for budget (tracked; should trend to 0)

<a id="quota-sentinel"></a>
### `quota-sentinel`: Quota Sentinel

> See vendor quota walls coming before they stop production.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | none (code) | cron "*/30 * * * *" (every 30 min) | `budget-controller` | — |

Budgets are dollars; quotas are hard walls. This agent tracks remaining ElevenLabs character credits, web-search counts, CourtListener rate limits, host storage and email-send limits, and projects when each runs out at the current burn rate. When a wall is less than 72 hours away it throttles in a fixed order: niche feeds first, then evergreen, then dailies, with The Breaking Desk throttled last. It raises event:quota.low for the Incident Commander and puts a line in the Chief of Staff brief.

- **Inputs:** vendor usage endpoints; AgentRun records
- **Outputs:** quota forecast; throttle list; event:quota.low
- **Tools:** `elevenlabs`, `host_api`, `sql`
- **Instances:** single
- **KPIs:**
  - episodes lost to an exhausted quota (target 0)
  - hours of warning before any wall (target >= 72)
  - forecast error on days-to-exhaustion

<a id="kill-switch"></a>
### `kill-switch`: Kill Switch

> Stop one show or the whole network instantly, with one setting.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode (checked at every stage boundary) | founders (Joshua German, Janel Moore) | `earlobe/monitor/killswitch.py` |

killed(show_id) returns true when env EARLOBE_KILL is 'all' or lists the show, or when config/killswitch.yaml says so. The Network Director checks it before sensing, before voicing and before publishing, so a kill takes effect even mid-run. It is the founders' emergency brake and the one control that overrides everything else. Next increment: automatic trips by the Incident Commander under written conditions (for example two corrections on one show inside seven days, or a legal-threat notice), always logged with the reason.

- **Inputs:** EARLOBE_KILL env; config/killswitch.yaml; Incident Commander trips (next)
- **Outputs:** killed true/false; kill log entry
- **Tools:** `none`
- **Instances:** single; scope is 'all' or per show
- **KPIs:**
  - episodes published while killed (target 0)
  - stages that ran after a kill was set (target 0)
  - automatic trips with a recorded reason (100%)

<a id="run-auditor"></a>
### `run-auditor`: Run Auditor / Observability

> Watch every run and say plainly when something drifts: cost, errors, latency or trust outcomes.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Haiku tier | always-on + cron "0 11 * * *" (daily digest) | `network-director` | — |

Reads AgentRun logs, gate decisions and the trust log and keeps the network's health metrics: error rate per agent, tokens and dollars per episode, gate decision mix per show, rewrite loops used, HOLD counts, render failures. It flags anomalies against a rolling baseline, such as a show suddenly killing half its episodes, the verifier using twice its usual searches, or a sensor returning zero Signals. Detection is code; a Haiku-tier pass writes the plain-language daily ops digest. Its metrics are the evidence base for the Incident Commander, the Eval Steward and the public transparency report.

- **Inputs:** AgentRun; GateDecision; trust log JSONL; dispatch log
- **Outputs:** daily ops digest; event:run.anomaly; metrics tables
- **Tools:** `sql`
- **Instances:** single
- **KPIs:**
  - anomalies caught before a listener or partner notices
  - false-alarm share of alerts (target < 20%)
  - digest delivered by 08:00 ET daily

<a id="incident-commander"></a>
### `incident-commander`: Incident Commander

> When something breaks, recover automatically, fail safe, and write down what happened.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Sonnet tier | event:run.failed, event:run.anomaly, event:quota.low, event:security.alert | `network-director` | — |

Owns the failure playbook for a network with no human on call. It retries transient errors with backoff, routes around a dead source feed, re-renders after a TTS failure, and if an episode cannot be produced safely it skips the slot rather than publishing something degraded. It can trip the Kill Switch for a show under written conditions and posts a status line in the Chief of Staff brief. After every incident it writes a short postmortem (what failed, impact, fix, prevention) to the knowledge base.

- **Inputs:** failure and anomaly events; AgentRun; runbooks
- **Outputs:** recovery actions; rule-based kill-switch trips; postmortem notes
- **Tools:** `sql`, `ci`, `email`
- **Instances:** single
- **KPIs:**
  - mean time to recovery
  - repeat incidents with the same cause (target 0)
  - postmortems written within 24 h (100%)

<a id="eval-steward"></a>
### `eval-steward`: Eval & Prompt Steward

> Prove the agents still do their jobs before any prompt or model change reaches production.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Sonnet tier | per change (any prompt, tier mapping or schema change) + weekly | `network-director` | — |

Keeps golden test sets for every LLM agent, weighted toward the trust stack: claims known true and known false, wire copies posing as independent sources, sealed-case and minor-naming traps, loaded-language samples. It runs them on any change to a system prompt, the tier mapping (EARLOBE_MODEL_* env) or a schema, and blocks the rollout through the Release Guard if a catch rate drops. It keeps the agents/*.md system prompts as versioned files, so every published episode can be traced to the exact prompt versions that made it. Scoring is deterministic; the Sonnet tier assembles new cases and summarizes regressions.

- **Inputs:** agent system prompts; golden sets; Hoax Red Team cases
- **Outputs:** eval report per change; pass/block to release-guard
- **Tools:** `ci`, `sql`
- **Instances:** single
- **KPIs:**
  - verifier catch rate on known-false claims (target >= 99%)
  - regressions that reached production (target 0)
  - gate rules covered by at least one golden case (100%)

<a id="release-guard"></a>
### `release-guard`: Build & Release Guard

> Nothing reaches production unless tests pass, configs are valid and a full dry run succeeds.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | none (code) | per change (CI) + nightly | `network-director` | — |

Runs pytest, validates every config file (each show's market, hosts and lane exist; every persona has a voice env name; every market has a sources file) and checks schemas.py against json-contracts.md. It then runs `python -m earlobe run --show <id> --dry-run` for every enabled show. Config changes proposed by other agents (Programming Director, Source Ledger Keeper, Show Launcher) merge only when it passes. Nightly it repeats the suite so drift in external feeds shows up before the morning runs.

- **Inputs:** code and config changes; Eval Steward result
- **Outputs:** pass/fail with reasons; nightly health report
- **Tools:** `ci`, `ffmpeg`
- **Instances:** single
- **KPIs:**
  - broken changes reaching a scheduled run (target 0)
  - config errors caught before merge
  - CI runtime (keep under 10 min)

<a id="security-sentinel"></a>
### `security-sentinel`: Security Sentinel

> Keep secrets safe, and keep hostile text in the news from steering the agents.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Haiku tier | always-on (inline screen on ingest) + weekly audit | `network-director` | — |

Every Signal and fetched page is untrusted text, and a press release or web page can hide instructions aimed at AI agents. This agent screens ingested content for prompt-injection patterns, quarantines suspicious items, makes sure source text is fenced as data in every prompt, and alerts when an agent's output shifts after reading a source. It also scans the repo for secrets, audits dependencies, reviews which API keys exist and who can use them, and flags unusual API usage that could mean a leaked key. Detection is code plus a Haiku-tier classifier.

- **Inputs:** Signal; fetched pages; repo; API usage logs
- **Outputs:** quarantine list; security findings; event:security.alert
- **Tools:** `ci`, `sql`
- **Instances:** single
- **KPIs:**
  - red-team injections that reach a writer or checker unflagged (target 0)
  - secrets committed (target 0)
  - hours to rotate a suspected leaked key (target < 2)

## Sensors desk

Always-on listeners that turn the outside world into `Signal` records: news feeds, official releases, court dockets, meetings, records, weather, social posts and archives. Each market's Beat Agent leads that market's sensors. Every Signal is untrusted text (the Security Sentinel screens it), and tier-4 items such as social posts and tips are leads only; they never count toward corroboration. *API names, access terms and feeds: as of Oct 2026, verify before buying or building.*

16 agents: 3 built, 11 next, 2 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`beat-agent`](#beat-agent) | Beat Agent | built | sonnet | always-on (poll every 15 min; beat memo twice daily) | Obsess over one market: know every outlet, agency and storyline, and surface every signal that matters before the morning brief. |
| [`court-watch`](#court-watch) | Court Watch | built | haiku | always-on (every 30 min on court days) | Never miss a filing, ruling or sentencing that matters in the courts we cover. |
| [`case-development-watcher`](#case-development-watcher) | Case Development Watcher | next | haiku | always-on (every 30 min) | Follow each tracked case across every court and agency, and fire a flash the moment it moves. |
| [`press-release-watcher`](#press-release-watcher) | Press-Release Watcher | next | haiku | always-on (poll every 15 min) | Catch every official announcement in each market minutes after it posts. |
| [`public-meetings-watcher`](#public-meetings-watcher) | Public Meetings Watcher | next | sonnet | always-on (agendas daily; minutes and video after each meeting) | Read every agenda and set of minutes, so the network knows what government is about to do and what it just did. |
| [`records-filings-watcher`](#records-filings-watcher) | Records & Filings Watcher | next | haiku | cron "0 */4 * * *" (every 4 h) | Turn public paperwork into early stories: permits, business filings, licenses, layoffs and big property deals. |
| [`legislature-watcher`](#legislature-watcher) | Legislature Watcher | next | haiku | always-on in session (every 30 min); weekly out of session | Track the bills, votes and hearings in statehouses and Congress that affect our markets. |
| [`civic-data-watcher`](#civic-data-watcher) | Civic Data Watcher | future | sonnet | cron "0 9 * * *" (daily) + weekly deltas | Find stories in the numbers: 311 calls, crime data, transit performance, inspections and budgets. |
| [`weather-hazard-watcher`](#weather-hazard-watcher) | Weather & Hazard Watcher | next | none | always-on (alerts every 5 min; forecasts 4x daily) | Bring official weather, air, fire and earthquake information into the network the moment it is issued. |
| [`social-signal-watcher`](#social-signal-watcher) | Social Signal Watcher | next | haiku | always-on | Hear what is happening on social platforms early, without ever treating a post as proof. |
| [`breaking-detector`](#breaking-detector) | Breaking Detector | built | none | always-on (every 5 min via run_breaking / breaking-scan) | Decide, with fixed rules, when a national or global event is big enough for The Breaking Desk. |
| [`archive-miner`](#archive-miner) | Archive Miner | next | sonnet | weekly per series + on-demand from showrunner-evergreen | Dig public archives for true, sourced, rights-clear stories for the evergreen series. |
| [`cold-case-archivist`](#cold-case-archivist) | Cold-Case Archivist | next | opus | weekly + on-demand | Build careful, fully sourced case files for unsolved cases where telling the story can help. |
| [`trend-scout`](#trend-scout) | Trend & Search-Demand Scout | next | sonnet | weekly + always-on demand alerts | Find topics people are searching for that nobody serves well, and prove it with data. |
| [`sports-watcher`](#sports-watcher) | Sports Watcher | future | haiku | always-on in season | Capture scores, schedules and big sports news for the sports spin-offs and high school feeds. |
| [`elections-watcher`](#elections-watcher) | Elections Watcher | next | haiku | always-on on election nights; daily otherwise | Report official election information only: who is running, who funds them, and what the official count says. |

<a id="beat-agent"></a>
### `beat-agent`: Beat Agent

> Obsess over one market: know every outlet, agency and storyline, and surface every signal that matters before the morning brief.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Sonnet tier | always-on (poll every 15 min; beat memo twice daily) | `assignment-editor` | `earlobe/sensors/__init__.py (run_sensors) + rss.py, press.py, gnews.py, gdelt.py, base.py` |

One instance per market, configured from config/markets.yaml and config/sources/<market>.yaml; it leads that market's other sensors (press releases, meetings, records, courts). v1 (built) is run_sensors(): it polls the market's news feeds and official feeds, runs one Google News RSS search per beat, adds GDELT for the national market and federal dockets where the beats call for them, and returns deduped Signals with outlet, tier and beat. The next increment adds the Sonnet-tier beat memo: what is moving, what is scheduled today (meetings, hearings, openings), which storylines are open and which sources went quiet. It also proposes new sources for its market file, so coverage widens over time instead of staying fixed at launch.

- **Inputs:** config/sources/<market>.yaml; Google News RSS; GDELT (national); Signals from the market's other sensors
- **Outputs:** Signal; beat memo (proposed); source suggestions
- **Tools:** `rss`, `gdelt`, `courtlistener`, `web_search`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); plus one national instance (national/global); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - stories later covered by 2+ local outlets that it surfaced first or in the same hour
  - signal yield: Signals per day that become assigned stories
  - minutes from source publication to Signal (target < 20)
  - active sources per market (growing)

<a id="court-watch"></a>
### `court-watch`: Court Watch

> Never miss a filing, ruling or sentencing that matters in the courts we cover.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Haiku tier | always-on (every 30 min on court days) | `beat-agent` | `earlobe/sensors/courtlistener.py` |

Federal coverage is built: recent_dockets() reads CourtListener v4 for each market's federal courts (dsc, cacd, nysd, nyed, ilnd, plus scotus) with COURTLISTENER_TOKEN. City instances read state and county public calendars and indexes (Richland County Public Index, LA Superior Court portal, NY eCourts/WebCrims, Cook County Clerk) where their terms allow, as cleared by Compliance & Platform Policy Watch. A Haiku-tier pass classifies each entry (new case, ruling, plea, sentencing, hearing set, dismissal) and flags notable parties. Court records are tier-1 sources, but sealed matters, juvenile cases and victim identities are dropped at intake, before any writer sees them.

- **Inputs:** CourtListener v4 API; state and county court portals; config/markets.yaml courts
- **Outputs:** Signal (kind=court_record, tier 1)
- **Tools:** `courtlistener`, `web_fetch`
- **Instances:** one per city court system: Richland County SC, LA Superior Court (wave 0); NY state courts, Cook County Circuit Court (wave 1); plus one federal instance on CourtListener covering every market's district courts and scotus; one more per new market
- **KPIs:**
  - notable rulings caught the same day (target >= 95% on weekly audit)
  - misclassified docket entries
  - juvenile or sealed items reaching a writer (target 0)

<a id="case-development-watcher"></a>
### `case-development-watcher`: Case Development Watcher

> Follow each tracked case across every court and agency, and fire a flash the moment it moves.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Haiku tier | always-on (every 30 min) | `case-file-keeper` | — |

Holds the list of cases the Case Tracker follows (config/cases.yaml, proposed): docket numbers, jurisdictions, agencies and party names. It watches those dockets, prosecutors' and police press pages and news searches, and classifies each hit as a development (charge, plea, ruling, verdict, sentencing, new filing) or noise. Real developments emit event:case.development, which the Scheduler turns into a Case Tracker flash; smaller ones feed the weekly best-of-last-7-days episode. Every development carries the primary record, so the strict lane's official-source rule can be met.

- **Inputs:** config/cases.yaml (proposed); CourtListener dockets; agency press pages; news search
- **Outputs:** Signal; event:case.development
- **Tools:** `courtlistener`, `rss`, `web_fetch`
- **Instances:** single agent; one watch per tracked case
- **KPIs:**
  - developments flashed within 60 min of the record posting
  - false flashes (target 0)
  - developments backed by a primary record (target 100%)

<a id="press-release-watcher"></a>
### `press-release-watcher`: Press-Release Watcher

> Catch every official announcement in each market minutes after it posts.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Haiku tier | always-on (poll every 15 min) | `beat-agent` | — |

Watches official newsrooms: city and county governments, police and sheriff, fire, school districts, universities, hospitals, utilities and the largest employers, plus geo-filtered press-release wires. A v1 official-feed poller already exists (earlobe/sensors/press.py, poll_press; not yet in the module map); this agent adds pages without feeds, agency email lists, the Haiku-tier classification of beat, newsworthiness and embargo times, and newsroom discovery. Government releases enter as tier-1 Signals; company releases count only as 'the company said'. It also notices when an agency that usually posts goes quiet, which the Beat agent treats as a signal in itself.

- **Inputs:** newsroom list in config/sources/<market>.yaml; agency RSS, email lists and pages; press-release wires
- **Outputs:** Signal (kind=press_release)
- **Tools:** `rss`, `web_fetch`, `email`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - median minutes from post to Signal (target < 15)
  - official releases captured (weekly audit sample, target >= 95%)
  - precision: Signals marked newsworthy that were used

<a id="public-meetings-watcher"></a>
### `public-meetings-watcher`: Public Meetings Watcher

> Read every agenda and set of minutes, so the network knows what government is about to do and what it just did.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Sonnet tier | always-on (agendas daily; minutes and video after each meeting) | `beat-agent` | — |

Watches agenda platforms (Legistar, Granicus, CivicPlus, BoardDocs, PrimeGov and similar) for each governing body in a market. When an agenda posts it pulls out the items that matter (votes, contracts, rezonings, budgets, appointments, public hearings) into a meeting preview; after the meeting it reads the minutes and, where captions exist, the meeting video transcript to record outcomes and roll-call votes. Agenda items carry dates, so the Follow-Up Editor can schedule coverage. This is the raw material for the City Council Watch and School Board Watch feeds.

- **Inputs:** agenda and minutes feeds and PDFs; meeting video captions where published
- **Outputs:** Signal (kind=official_data); MeetingDigest (proposed)
- **Tools:** `rss`, `web_fetch`
- **Instances:** one per governing body per market, e.g. Columbia City Council, Richland County Council, Lexington County Council, Richland One and Richland Two school boards; LA City Council, LA County Board of Supervisors, LAUSD board, LA Metro board; then each new market's bodies
- **KPIs:**
  - agendas captured within 2 h of posting (target >= 95%)
  - vote outcomes recorded correctly (audit sample, target 100%)
  - meeting-sourced stories per week per market

<a id="records-filings-watcher"></a>
### `records-filings-watcher`: Records & Filings Watcher

> Turn public paperwork into early stories: permits, business filings, licenses, layoffs and big property deals.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Haiku tier | cron "0 */4 * * *" (every 4 h) | `beat-agent` | — |

Polls records that move before the news does: building and demolition permits, rezoning applications, new business registrations with the Secretary of State, liquor-license applications, food-safety inspection results, WARN layoff notices, large property transfers and SEC filings by companies based in the market. A Haiku-tier pass scores each record against per-market thresholds (project value, employer size, notable names). Results feed the daily briefs and the hyper-local niche feeds (Open & Shut, Permit Pulse, Main Street Ledger). New-business filings also go to the Sponsor Prospector as leads.

- **Inputs:** city and county permit portals and open data; Secretary of State filings; state WARN notice pages; SEC EDGAR
- **Outputs:** Signal (kind=official_data, tier 1); sponsor leads
- **Tools:** `web_fetch`, `rss`, `open_data_api`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - records-sourced stories per week
  - big local openings and closings we reported before other outlets
  - leads passed to the Sponsor Prospector that convert

<a id="legislature-watcher"></a>
### `legislature-watcher`: Legislature Watcher

> Track the bills, votes and hearings in statehouses and Congress that affect our markets.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Haiku tier | always-on in session (every 30 min); weekly out of session | `beat-agent` | — |

Columbia is South Carolina's capital, so the statehouse is a local beat there, not a national one. The agent reads state legislature data (official legislature sites, or bill-tracking APIs where licensed), Congress.gov and the Federal Register, and classifies bills and rules by beat and by the markets they affect. It produces status-change Signals (filed, out of committee, passed, signed, vetoed) and a weekly 'what moved' list. Vote tallies come from official roll calls only.

- **Inputs:** state legislature sites and APIs; Congress.gov API; Federal Register API
- **Outputs:** Signal (kind=official_data); weekly bill tracker
- **Tools:** `web_fetch`, `rss`
- **Instances:** one per state legislature: South Carolina, California (wave 0); New York, Illinois (wave 1); one federal instance; one per new state
- **KPIs:**
  - status changes captured the same day
  - tracked bills that later made news (relevance)
  - wrong vote tallies (target 0)

<a id="civic-data-watcher"></a>
### `civic-data-watcher`: Civic Data Watcher

> Find stories in the numbers: 311 calls, crime data, transit performance, inspections and budgets.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | cron "0 9 * * *" (daily) + weekly deltas | `beat-agent` | — |

Reads open data portals (Socrata and ArcGIS sites such as LA's, NYC's and Chicago's) and transit feeds (GTFS-realtime alerts and on-time data for LA Metro, CTA and MTA). Change detection is code: week-over-week shifts, records broken, outliers by neighborhood. A Sonnet-tier pass writes a short data note with the method and the caveats (preliminary crime data, changes in reporting) so writers don't overclaim. It powers the Transit Minute and Cost of Living Watch feeds and data segments in the dailies.

- **Inputs:** open data portals; GTFS-realtime feeds
- **Outputs:** Signal (kind=official_data); data note with method
- **Tools:** `open_data_api`, `sql`
- **Instances:** one per market with a usable open data portal (los-angeles, new-york, chicago first)
- **KPIs:**
  - data notes that became stories
  - method errors caught by the checkers (trending to 0)
  - watched datasets refreshed on schedule

<a id="weather-hazard-watcher"></a>
### `weather-hazard-watcher`: Weather & Hazard Watcher

> Bring official weather, air, fire and earthquake information into the network the moment it is issued.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | none (code) | always-on (alerts every 5 min; forecasts 4x daily) | `breaking-detector` | — |

Uses official sources only: National Weather Service alerts and forecasts, National Hurricane Center advisories, USGS earthquake feeds, AirNow air quality, wildfire incident feeds, and a licensed pollen source (vendor to be chosen; verify licensing). NWS feeds listed in a market's sources file are already polled as official_data by sensors/press.py; this agent adds thresholds, the other feeds and the structured output. Warnings above set thresholds become tier-1 Signals with official confirmation, which the Breaking Detector can use directly. It also writes the structured weather block every daily brief reads, so hosts never improvise a forecast.

- **Inputs:** NWS API; NHC advisories; USGS feeds; AirNow; wildfire incident feeds; pollen source (TBD)
- **Outputs:** Signal (tier 1, official_confirmation); weather block per market
- **Tools:** `rss`, `web_fetch`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); plus one national instance (national/global); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - minutes from NWS warning to Signal (target < 5)
  - weather blocks ready before every daily run (100%)
  - hazard warnings missed (target 0)

<a id="social-signal-watcher"></a>
### `social-signal-watcher`: Social Signal Watcher

> Hear what is happening on social platforms early, without ever treating a post as proof.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Haiku tier | always-on | `beat-agent` | — |

Monitors official agency accounts (police, fire, emergency management, city halls, school districts), open social feeds and local community forums where the platform's terms allow (cleared by Compliance & Platform Policy Watch). Posts enter as tier-4 Signals that cannot corroborate anything on their own; a post from an account on the Source Ledger's registry of verified official accounts counts as an on-record official statement. A Haiku-tier classifier tags beat, urgency and known hoax patterns. Its value is speed: it tells the Beat agent and the Breaking Detector where to look.

- **Inputs:** official agency accounts; open social feeds; community forums (where terms allow)
- **Outputs:** Signal (tier 4 unless from a verified official account)
- **Tools:** `social_api`, `rss`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); plus one national instance (national/global); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - lead time vs the first professional outlet report
  - social leads later confirmed by tier 1-3 sources
  - hoaxes that reached a script (target 0)

<a id="breaking-detector"></a>
### `breaking-detector`: Breaking Detector

> Decide, with fixed rules, when a national or global event is big enough for The Breaking Desk.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | always-on (every 5 min via run_breaking / breaking-scan) | `showrunner-breaking` | `earlobe/desk/breaking.py (+ earlobe/sensors/gdelt.py velocity)` |

detect(stories, window_minutes=60) flags a story when two things hold. Speed: at least 3 independent tier 1-2 outlets inside the window, or official confirmation plus 2. Class: the headline reads as one of The Breaking Desk's event classes (major death of a prominent figure, attack or attempt, disaster, Supreme Court, federal government, space, mega sports, mega business, world). Independence uses owner groups, so one wire story republished everywhere does not trigger it; the rules favor precision, because a missed story is caught on the next scan while a false one costs a gated episode. A hit fires event:desk.breaking for The Breaking Desk only; local dailies pick a story up only when the Localizer finds a real local angle.

- **Inputs:** Story; Signal (tier-aware count); config/owners.yaml; GDELT velocity; official Signals
- **Outputs:** Story (breaking=true, beat=event class); event:desk.breaking
- **Tools:** `gdelt`, `rss`
- **Instances:** single national instance; per-spin-off thresholds (sports, courts, space) as those feeds launch
- **KPIs:**
  - major events detected (recall on weekly audit)
  - false triggers that ended in KILL
  - minutes from the first tier 1-2 report to trigger

<a id="archive-miner"></a>
### `archive-miner`: Archive Miner

> Dig public archives for true, sourced, rights-clear stories for the evergreen series.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | weekly per series + on-demand from showrunner-evergreen | `showrunner-evergreen` | — |

Searches digitized primary sources: Library of Congress collections (including Chronicling America newspapers), the National Archives catalog, Internet Archive and HathiTrust public-domain texts, Calisphere, the Media History Digital Library for old Hollywood trade papers, and city, university and state digital collections for hometown history. For each episode idea it returns an archive pack: the primary documents, dates, people and places, conflicting accounts, and the rights status of each item. Encyclopedias and blogs are tier-4 leads used only to find primary records, never as sources. Rights flags on every item keep anything copyrighted from being read on air.

- **Inputs:** series outline from showrunner-evergreen; archive APIs and catalogs
- **Outputs:** archive pack (Source list, kind=archive); episode idea list
- **Tools:** `web_search`, `web_fetch`
- **Instances:** one per evergreen series: history-of-hollywood (wave 0); hometown history per market and music history series (next)
- **KPIs:**
  - episode claims backed by a primary document
  - archive packs that pass the archive lane without a rewrite
  - rights problems found after publish (target 0)

<a id="cold-case-archivist"></a>
### `cold-case-archivist`: Cold-Case Archivist

> Build careful, fully sourced case files for unsolved cases where telling the story can help.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Opus tier | weekly + on-demand | `showrunner-evergreen` | — |

Mines NamUs public case data, state and local police cold-case pages, state attorney-general cold-case units, FBI public appeals, the Charley Project and the Doe Network (leads only), and newspaper archives. It favors cases where investigators are publicly asking for tips, so every Cold Case Files episode can end with the official tip line. Each dossier has a timeline with a source for every entry, what investigators have said on record, and a list of rumors that must stay out. Hard rules: never name an uncharged person as a suspect, no graphic detail beyond the official record, and a sensitivity note for the Harm & Sensitivity Reviewer.

- **Inputs:** cold-case databases and agency pages; newspaper archives
- **Outputs:** case dossier (CaseFile, proposed); Source list
- **Tools:** `web_search`, `web_fetch`
- **Instances:** single national instance; regional spin-offs (Carolinas, Southern California) draw on it
- **KPIs:**
  - episodes that carry an active official tip line
  - dossier claims backed by on-record sources (target 100%)
  - legal or harm issues raised at the gate (trending to 0)

<a id="trend-scout"></a>
### `trend-scout`: Trend & Search-Demand Scout

> Find topics people are searching for that nobody serves well, and prove it with data.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Sonnet tier | weekly + always-on demand alerts | `programming-director` | — |

Measures demand from public signals: search trend data, Wikipedia pageview trends, podcast chart categories, YouTube search suggestions and conversation volume in GDELT. It checks supply too: how many podcasts already cover the topic, how recently and how well rated. Then it checks feasibility: are there enough public, verifiable sources to keep a feed going for months? The output is a TopicBrief with a recommended template, cadence and market, which the Programming Director accepts or rejects.

- **Inputs:** search trend data; Wikipedia pageviews API; podcast charts; GDELT
- **Outputs:** TopicBrief (proposed)
- **Tools:** `web_search`, `web_fetch`, `gdelt`
- **Instances:** single, with a per-market pass for local niche ideas
- **KPIs:**
  - TopicBriefs greenlit
  - shows launched from its briefs that hit their 90-day audience target
  - briefs rejected for lack of sources (should fall over time)

<a id="sports-watcher"></a>
### `sports-watcher`: Sports Watcher

> Capture scores, schedules and big sports news for the sports spin-offs and high school feeds.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Haiku tier | always-on in season | `beat-agent` | — |

Reads official league, conference, school and state athletic association sources for schedules, final scores and announcements, plus team and league releases for trades, sales and coaching changes. High school results come only from official association and school sources, and students are named only as those sources publish them, under the Legal Screener's rules on minors. Real-time score data is often licensed, so sources are cleared by Compliance first (inference). It feeds The Breaking Desk: Sports, the Friday Night Scoreboard feeds and the dailies' sports beat.

- **Inputs:** official league, school and association sites; team press releases
- **Outputs:** Signal; scoreboard table
- **Tools:** `rss`, `web_fetch`
- **Instances:** one per market for local and high school sports; one national instance for the sports breaking spin-off
- **KPIs:**
  - final scores published accurately (target 100%)
  - minutes from final whistle to Signal
  - licensing issues (target 0)

<a id="elections-watcher"></a>
### `elections-watcher`: Elections Watcher

> Report official election information only: who is running, who funds them, and what the official count says.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Haiku tier | always-on on election nights; daily otherwise | `beat-agent` | — |

Reads election authority sites (county and state election commissions, for example the South Carolina Election Commission and the LA County Registrar-Recorder/County Clerk), candidate filings and campaign finance data (FEC API, state ethics commissions). On election nights it reports official tallies with a timestamp and the share of precincts reporting, and never projects a winner; a race is called on air only when an official source, or a named and licensed call source, has called it. The general election is Nov 3, 2026: if this agent is not live and eval-tested by then, The Breaking Desk does not cover race results that night. Election stories run in the strict lane by default.

- **Inputs:** election authority results pages; FEC API; state campaign finance data; candidate filings
- **Outputs:** Signal (kind=official_data); results table
- **Tools:** `web_fetch`, `rss`
- **Instances:** one per market's election authorities plus one national federal-filings instance
- **KPIs:**
  - results matching the official source (target 100%)
  - projection language on air (target 0)
  - results refreshed within 10 min of an official update

## Editorial desk

Goes from Signals to a finished script: cluster and score, assign, research, plan the rundown, write, line-edit, and package the words that sell the episode. Built today: Story Desk, Assignment Editor, Producer, Copywriter. The showrunners own each format's bible. *Platform features named here (title tests and similar): as of Oct 2026, verify.*

17 agents: 4 built, 12 next, 1 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`story-desk`](#story-desk) | Story Desk | built | haiku | per-episode + always-on for the national/breaking scan | Turn a flood of raw Signals into a short list of distinct, scored stories. |
| [`assignment-editor`](#assignment-editor) | Assignment Editor | built | none | per-episode | Give every show the right stories: right market, right beat, right number, right lane. |
| [`researcher`](#researcher) | Researcher | next | opus | per-episode (deeper packs on-demand) | Hand the Producer the context and primary records behind every story. |
| [`producer`](#producer) | Producer / Scriptwriter | built | opus | per-episode (and per REWRITE loop) | Write the episode script: clear, conversational, and every factual line mapped to its claims. |
| [`copy-editor`](#copy-editor) | Copy Editor (audio) | next | sonnet | per-episode (after the Producer, before the Claim Extractor) | Make every script sound right out loud without changing what it claims. |
| [`copywriter`](#copywriter) | Copywriter | built | sonnet | per-episode (after PUBLISH) | Write the words that get an episode chosen: title, description, hooks, show notes and social posts. |
| [`headline-tester`](#headline-tester) | Headline / Title Tester | next | sonnet | per-episode + weekly learning report | Find out, with data, which titles and hooks actually earn listens. |
| [`localizer`](#localizer) | Localizer | next | sonnet | event:desk.breaking + per-episode for national stories | Find the real local angle on big national stories, or keep them out of the local dailies. |
| [`spanish-editions-editor`](#spanish-editions-editor) | Spanish-Language Editions Editor | next | opus | per-episode (after PUBLISH of the English edition) | Produce Spanish-language editions that are adapted for listeners, not just translated, and verified to the same standard. |
| [`follow-up-editor`](#follow-up-editor) | Follow-Up Editor | next | haiku | per-episode (date extraction) + cron "0 9 * * *" (daily tickler) | Never drop a story: remember every date that matters and bring the story back when it arrives. |
| [`case-file-keeper`](#case-file-keeper) | Case File Keeper | next | opus | event:case.development + weekly | Keep one accurate, sourced, presumption-of-innocence file for every case the Case Tracker follows. |
| [`showrunner-daily`](#showrunner-daily) | Showrunner: Daily Briefs | next | sonnet | per-episode (rundown) + weekly review | Own the morning daily briefs, market by market: format, rundown, tone and length. |
| [`showrunner-breaking`](#showrunner-breaking) | Showrunner: The Breaking Desk | next | sonnet | event:desk.breaking + weekly review | Run The Breaking Desk: fast, calm, and only what is confirmed. |
| [`showrunner-courts`](#showrunner-courts) | Showrunner: Courts Roundups | next | sonnet | per-episode + weekly review | Run the courts roundups: what was filed, ruled and scheduled, in careful, fair language. |
| [`showrunner-case-tracker`](#showrunner-case-tracker) | Showrunner: Case Tracker | next | sonnet | weekly (Friday) + event:case.development | Run the live true-crime Case Tracker: the weekly best of the last 7 days and the development flashes. |
| [`showrunner-evergreen`](#showrunner-evergreen) | Showrunner: Evergreen & Archives | next | sonnet | weekly + per-episode | Plan and run the evergreen series as seasons with arcs, from History of Hollywood to Cold Case Files. |
| [`showrunner-niche`](#showrunner-niche) | Showrunner: Niche Feeds | future | sonnet | per-episode + weekly tuning | Run dozens of small, hyper-specific always-on feeds from templates, and pause any that run dry. |

<a id="story-desk"></a>
### `story-desk`: Story Desk

> Turn a flood of raw Signals into a short list of distinct, scored stories.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Haiku tier | per-episode + always-on for the national/breaking scan | `assignment-editor` | `earlobe/desk/cluster.py, independence.py, score.py` |

cluster(signals, owners) groups Signals about the same event using title shingles and a time window, and computes independent_outlets with owner groups from config/owners.yaml, so five syndicated copies of one wire story count once. score(story, show_cfg) gives a heuristic newsworthiness score from beat fit and recency; an optional Haiku-tier triage (StoryTriage contract) refines the headline, summary, beat, risk flags and entities. Risk flags set here (crime, minor, victim, election and the rest) later decide which trust lane a story goes through.

- **Inputs:** Signal; config/owners.yaml; show config
- **Outputs:** Story; StoryTriage
- **Tools:** `sql`
- **Instances:** one pass per show run; the national pass runs continuously for breaking
- **KPIs:**
  - duplicate stories in one rundown (target 0)
  - cluster precision on weekly audit sample
  - risk flags missed that a checker later caught

<a id="assignment-editor"></a>
### `assignment-editor`: Assignment Editor

> Give every show the right stories: right market, right beat, right number, right lane.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode | `network-director` | `earlobe/desk/assign.py` |

assign(stories, shows) matches stories to shows by market and beat, enforces each show's max_stories, and picks the lane: crime, court and named-private-person stories move to the strict lane, breaking stories to the breaking lane. National events go to The Breaking Desk and never get pushed into every daily; a daily carries one only when the Localizer has found a local angle. It is deterministic, so the same inputs always produce the same rundown.

- **Inputs:** Story; config/shows.yaml
- **Outputs:** assignments: show_id -> [Story] with lane
- **Tools:** `none`
- **Instances:** single; runs per show slot
- **KPIs:**
  - stories assigned to the wrong market or beat (audit, target 0)
  - rundowns under-filled while usable stories went unused
  - lane misroutes caught later at the gate

<a id="researcher"></a>
### `researcher`: Researcher

> Hand the Producer the context and primary records behind every story.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Opus tier | per-episode (deeper packs on-demand) | `producer` | — |

v1 builds a basic pack from each story's own sources (producer/research_pack.py). The Researcher upgrades that with an Opus-tier research call: background, prior coverage, the primary documents (filings, agendas, data), numbers with their source, who the named people are and their roles, and the open questions. Every item becomes a Source with tier, owner group and syndication origin, so the writer's sourcing is clean before the blind verifier ever runs. It summarizes in its own words and never copies article text.

- **Inputs:** Story; Signal sources; archive packs and case files
- **Outputs:** ResearchPack (proposed contract; v1 is a dict); Source
- **Tools:** `web_search`, `web_fetch`, `courtlistener`
- **Instances:** one per story per run (parallel)
- **KPIs:**
  - script claims supported by the pack at first draft
  - REWRITE loops caused by missing sourcing
  - primary (tier-1) sources per story

<a id="producer"></a>
### `producer`: Producer / Scriptwriter

> Write the episode script: clear, conversational, and every factual line mapped to its claims.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Opus tier | per-episode (and per REWRITE loop) | showrunner of the episode's format (assignment-editor until showrunners ship) | `earlobe/producer/writer.py` |

write_script(...) turns the rundown and research pack into a Script in the show's format, with the show's personas, segments (cold open, intro, body, kicker, outro) and target length. Every body line carries claim_ids, which is what makes the whole trust stack possible. On REWRITE it receives the gate's rewrite_instructions and revises only what was flagged. It writes for the ear: short sentences, attribution up front ('police said'), and a plain line on why each story matters.

- **Inputs:** Story; ResearchPack; show config and bible; rundown; GateDecision.rewrite_instructions on revisions
- **Outputs:** Script (with Claim map)
- **Tools:** `none (LLM only)`
- **Instances:** one per episode run
- **KPIs:**
  - first-draft PUBLISH rate
  - average rewrite loops per episode
  - episodes inside target_minutes (target >= 95%)
  - listener completion rate

<a id="copy-editor"></a>
### `copy-editor`: Copy Editor (audio)

> Make every script sound right out loud without changing what it claims.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Sonnet tier | per-episode (after the Producer, before the Claim Extractor) | `producer` | — |

Line-edits for the ear: numbers written the way they are spoken, full names and titles on first reference and short names after, no tongue-twisters, no sentence a listener has to hear twice. It flags unfamiliar names for the Pronunciation Keeper and trims to the target length. It cannot add facts; if an edit changes the meaning of a claim, it keeps the claim_id and marks the claim for re-check so the trust loop sees the new wording. It maintains the network's audio style guide.

- **Inputs:** Script; audio style guide; pronunciation lexicon
- **Outputs:** Script (edited); pronunciation requests
- **Tools:** `none (LLM only)`
- **Instances:** one per episode run
- **KPIs:**
  - QA re-renders caused by script wording
  - duration accuracy vs target
  - claims altered without a re-check flag (target 0)

<a id="copywriter"></a>
### `copywriter`: Copywriter

> Write the words that get an episode chosen: title, description, hooks, show notes and social posts.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Sonnet tier | per-episode (after PUBLISH) | showrunner of the episode's format (assignment-editor until showrunners ship) | `earlobe/producer/copywriter.py` |

write_copy(script, show_cfg, llm) returns the Copy contract: title, description, show_notes_md, social_posts and keywords. It works from a copywriting playbook: clear beats clever, the most specific fact goes in the title, the hook is the first line of the description, no clickbait, and no claim that is not in the gated script. The Headline Tester's results feed back into the playbook every week. Copy is written only after the gate passes, so it can never promise something the trust stack cut.

- **Inputs:** Script (gated); GateDecision; copy playbook; headline test results
- **Outputs:** Copy
- **Tools:** `none (LLM only)`
- **Instances:** one per episode
- **KPIs:**
  - click-through from directory listings and social
  - tested-title win rate vs control
  - copy claims not found in the script (target 0)

<a id="headline-tester"></a>
### `headline-tester`: Headline / Title Tester

> Find out, with data, which titles and hooks actually earn listens.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | per-episode + weekly learning report | `copywriter` | — |

For each episode it writes several title and hook variants inside the copy rules and scores them against the network's history. Where a platform supports live tests it runs them: newsletter subject-line splits, social post variants, and YouTube title and thumbnail tests where available (verify feature availability, as of Oct 2026). Winning patterns become concrete playbook rules for the Copywriter, such as 'lead local titles with the place name'. It also catches variants drifting toward clickbait, which the Brand Guardian would reject.

- **Inputs:** Copy; analytics history
- **Outputs:** title variants; test results; playbook updates
- **Tools:** `analytics_api`, `youtube_api`, `email`
- **Instances:** single
- **KPIs:**
  - CTR lift of tested titles vs the untested baseline
  - tests completed per week
  - playbook rules adopted

<a id="localizer"></a>
### `localizer`: Localizer

> Find the real local angle on big national stories, or keep them out of the local dailies.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Sonnet tier | event:desk.breaking + per-episode for national stories | `assignment-editor` | — |

When a national or breaking story lands, it checks each market for a genuine local connection: a local official's on-record response, local data, a person from the area, a local employer, base, case or law affected. If it finds one, it creates a local Story that must clear the normal sourcing rules on its own. If not, the daily stays local and listeners are pointed to The Breaking Desk. This keeps the dailies about the city, as the show design intends.

- **Inputs:** Story (national or breaking); market source files; beat memo
- **Outputs:** Story (local angle) or a no-angle decision
- **Tools:** `web_search`, `rss`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - local-angle stories that pass the gate
  - national stories in a daily without a local angle (target 0)
  - completion rate on localized segments

<a id="spanish-editions-editor"></a>
### `spanish-editions-editor`: Spanish-Language Editions Editor

> Produce Spanish-language editions that are adapted for listeners, not just translated, and verified to the same standard.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Opus tier | per-episode (after PUBLISH of the English edition) | `showrunner-daily` | — |

Adapts gated scripts into natural Spanish, starting with LA Daily, then a Spanish Breaking Desk, then Houston, Miami and Phoenix as those markets launch, keeping every claim_id mapped to its Spanish line. A back-translation pass by the Fact Checker in 'translation mode' confirms each Spanish claim says exactly what the gated English claim says; any drift is fixed before voicing. It uses two new original Spanish-speaking personas designed by the Voice Director, and keeps local names and institutions in their official form. The AI disclosure outro has an approved Spanish version.

- **Inputs:** Script (gated, English); GateDecision; Spanish style guide
- **Outputs:** Script (es); translation fidelity report
- **Tools:** `none (LLM only)`
- **Instances:** one per Spanish edition: la-daily-es first; then breaking-desk-es; then houston, miami and phoenix editions as those markets launch
- **KPIs:**
  - translation drift caught before publish (and 0 after)
  - Spanish edition audience growth
  - native-speaker quality score on a monthly sample

<a id="follow-up-editor"></a>
### `follow-up-editor`: Follow-Up Editor

> Never drop a story: remember every date that matters and bring the story back when it arrives.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Haiku tier | per-episode (date extraction) + cron "0 9 * * *" (daily tickler) | `assignment-editor` | — |

Extracts future dates from every published story and meeting digest (hearings, votes, deadlines, openings, sentencings, report releases) into a tickler calendar. On the day, it creates a follow-up Story stub with links to our earlier coverage for the Assignment Editor. It also closes loops: when a follow-up shows an earlier story changed, it alerts the Re-check Monitor. Listeners hear continuity: 'Last week we told you the council would vote. It did.'

- **Inputs:** Episode; Story; MeetingDigest (proposed)
- **Outputs:** tickler entries; follow-up Story stubs
- **Tools:** `sql`
- **Instances:** single; one calendar per market
- **KPIs:**
  - scheduled events followed up on the day (target >= 90%)
  - follow-ups that became segments
  - changed facts caught through follow-ups

<a id="case-file-keeper"></a>
### `case-file-keeper`: Case File Keeper

> Keep one accurate, sourced, presumption-of-innocence file for every case the Case Tracker follows.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Opus tier | event:case.development + weekly | `showrunner-case-tracker` | — |

For each tracked case it maintains a CaseFile: parties with their exact legal status (arrested, charged, convicted, acquitted, dismissed), a dated timeline with a primary source for each entry, next hearing dates, and a clear split between what is alleged and what is established. It proposes which cases to track using written criteria (public interest, official records available, no exploitation of victims) and retires cases when they resolve. Every Case Tracker script starts from this file, which keeps the weekly and the flashes consistent with each other.

- **Inputs:** Signal from case-development-watcher; court records; cold-case dossiers
- **Outputs:** CaseFile (proposed); config/cases.yaml updates
- **Tools:** `courtlistener`, `web_search`
- **Instances:** single agent; one CaseFile per tracked case
- **KPIs:**
  - legal-status errors (target 0)
  - timeline entries with a primary source (target 100%)
  - contradictions between flashes and the weekly (target 0)

<a id="showrunner-daily"></a>
### `showrunner-daily`: Showrunner: Daily Briefs

> Own the morning daily briefs, market by market: format, rundown, tone and length.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | per-episode (rundown) + weekly review | `programming-director` | — |

Keeps each daily's show bible (docs/shows/bibles/<show>.md): segment order, host roles (Mara and Theo in Columbia, Lena and Marcus in LA), the weather and 'today' blocks, the kicker style and the 6-8 minute target. Each morning it orders the assigned stories into a rundown and sets a time budget per story before the Producer writes. Weekly it reviews completion by segment, listener mail and gate outcomes, and adjusts beats or max_stories through the Release Guard. It owns the rule that a daily carries breaking news only with a local angle.

- **Inputs:** assignments; InsightReport (proposed); listener mail summary; show bible
- **Outputs:** rundown; show bible updates; shows.yaml change requests
- **Tools:** `sql`
- **Instances:** one per daily brief: columbia-daily, la-daily (wave 0); nyc-daily, chicago-daily (wave 1); one per new market
- **KPIs:**
  - completion rate per daily
  - episodes inside target length
  - follower growth per market

<a id="showrunner-breaking"></a>
### `showrunner-breaking`: Showrunner: The Breaking Desk

> Run The Breaking Desk: fast, calm, and only what is confirmed.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | event:desk.breaking + weekly review | `programming-director` | — |

Owns the breaking_flash format: what we know, what we don't know yet, what happens next; Ava anchors and flashes run 2-4 minutes. It decides whether an event gets one flash, a run of updates or a longer explainer once facts settle, and keeps the 30-minute minimum gap so the feed does not churn. While the gate HOLDs a story (breaking lane: up to six 15-minute holds) it publishes nothing on that story rather than rumor. It plans the spin-off feeds (Sports, Courts, Space, Markets) and their trigger thresholds with the Breaking Detector.

- **Inputs:** Story (breaking); GateDecision (HOLD/PUBLISH); Localizer results
- **Outputs:** flash rundown; update or explainer plan; spin-off proposals
- **Tools:** `sql`
- **Instances:** one for breaking-desk; one per breaking spin-off as launched
- **KPIs:**
  - median minutes from trigger to published flash
  - flashes later corrected (target 0)
  - HOLDs that ended in PUBLISH vs KILL

<a id="showrunner-courts"></a>
### `showrunner-courts`: Showrunner: Courts Roundups

> Run the courts roundups: what was filed, ruled and scheduled, in careful, fair language.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | per-episode + weekly review | `programming-director` | — |

Owns the court_roundup format for LA Courts Roundup and each future city: new filings, rulings, pleas and sentencings, then the week ahead from court calendars, with June as host. Every courts show runs in the strict lane, so allegations need official records and the presumption of innocence is said out loud ('has pleaded not guilty', 'is accused of'). It balances high-profile cases with the civil, housing and government cases that affect more listeners. It also manages the hand-off when a courts story becomes a Case Tracker case.

- **Inputs:** Court Watch Signals; assignments; court calendars
- **Outputs:** rundown; show bible updates
- **Tools:** `sql`
- **Instances:** one per courts roundup: la-courts (wave 0); columbia-courts, nyc-courts, chicago-courts as launched; federal-docket weekly
- **KPIs:**
  - legal-screen issues per episode (trending to 0)
  - corrections (target 0)
  - share of civic (non-celebrity) cases in each episode

<a id="showrunner-case-tracker"></a>
### `showrunner-case-tracker`: Showrunner: Case Tracker

> Run the live true-crime Case Tracker: the weekly best of the last 7 days and the development flashes.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | weekly (Friday) + event:case.development | `programming-director` | — |

Owns the case_weekly format (15-25 minutes, June and Theo) and the short flashes that fire on event:case.development. It picks which developments make the weekly, keeps the tone factual rather than lurid, and makes sure every case segment restates the current legal status. It works from the Case File Keeper's files, so the weekly and the flashes never contradict each other. It enforces the network's true-crime ethics: victims are people, not plot, and families are not speculated about.

- **Inputs:** CaseFile (proposed); case.development events
- **Outputs:** weekly rundown; flash briefs
- **Tools:** `sql`
- **Instances:** single for case-tracker; one per regional tracker if launched
- **KPIs:**
  - weekly completion rate
  - flash latency from development to publish
  - harm and legal gate issues (trending to 0)

<a id="showrunner-evergreen"></a>
### `showrunner-evergreen`: Showrunner: Evergreen & Archives

> Plan and run the evergreen series as seasons with arcs, from History of Hollywood to Cold Case Files.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | weekly + per-episode | `programming-director` | — |

Owns the evergreen_story format for History of Hollywood (Lena), Cold Case Files (June) and the hometown and music history series. It plans seasons of 8-12 episodes with an arc, asks the Archive Miner and Cold-Case Archivist for packs, and sets each episode's structure: scene, stakes, turn, why it still matters. Archive content runs in the archive lane; Cold Case Files stays in the strict lane. It orders releases so each episode stands alone but rewards bingeing.

- **Inputs:** archive packs; case dossiers; TopicBrief (proposed); InsightReport (proposed)
- **Outputs:** season plans; episode outlines; show bible updates
- **Tools:** `sql`
- **Instances:** one per evergreen series: history-of-hollywood, cold-case-files (wave 0); hometown history per market and music history (next)
- **KPIs:**
  - completion rate
  - back-catalog listens per month (long-tail value)
  - first-draft PUBLISH rate in the archive lane

<a id="showrunner-niche"></a>
### `showrunner-niche`: Showrunner: Niche Feeds

> Run dozens of small, hyper-specific always-on feeds from templates, and pause any that run dry.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | per-episode + weekly tuning | `programming-director` | — |

Manages the proposed niche_minute, meeting_watch, data_minute and scoreboard templates used by feeds like City Council Watch, Open & Shut, Permit Pulse, Pollen & Air and Transit Minute. Every feed has a minimum-news rule: no qualifying stories means no episode, never filler. It tunes each feed's thresholds from completion data, merges overlapping feeds, and recommends pausing feeds below their audience target to the Programming Director. One agent can cover many feeds because the templates do the heavy lifting.

- **Inputs:** assignments; InsightReport (proposed); template library
- **Outputs:** rundowns; feed tuning changes; pause and merge recommendations
- **Tools:** `sql`
- **Instances:** single agent managing every niche feed (one config per feed)
- **KPIs:**
  - filler episodes (target 0)
  - niche feeds above their audience target
  - cost per niche episode

## Trust desk

The Trust Stack, which is also product 2. Each checker is a **separate, isolated model call that returns JSON** and never sees another checker's opinion; the verifier never sees the writer's sources. The Standards Editor is plain code (`earlobe/trust/gate.py`): the same reports always produce the same PUBLISH / REWRITE / HOLD / KILL. Lanes (`standard`, `strict`, `breaking`, `archive`) set how much proof is needed. Breaking needs 3 independent owner groups, the others 2, and an official record satisfies the rule outside breaking.

14 agents: 8 built, 5 next, 1 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`claim-extractor`](#claim-extractor) | Claim Extractor | built | opus | per-episode (every revision) | List every checkable assertion in the script, including the ones the writer forgot to map. |
| [`source-verifier`](#source-verifier) | Source Verifier (blind) | built | opus | per-episode | Re-source every claim blind, from scratch, and count only truly independent support. |
| [`fact-checker`](#fact-checker) | Fact Checker | built | opus | per-episode | Check that each claim, as worded, says exactly what the evidence says. |
| [`bias-checker`](#bias-checker) | Bias Checker | built | opus | per-episode | Catch loaded language, one-sided framing and missing perspectives before they air. |
| [`legal-screener`](#legal-screener) | Legal / Defamation Screener | built | opus | per-episode | Screen every script for defamation, privacy and legal risk before it can publish. |
| [`harm-sensitivity-reviewer`](#harm-sensitivity-reviewer) | Harm & Sensitivity Reviewer | next | opus | per-episode (strict and breaking lanes; sampled on the others) | Make sure coverage of crime, death and tragedy does not cause avoidable harm. |
| [`originality-checker`](#originality-checker) | Originality Checker | next | haiku | per-episode | Make sure every script is in our own words, with only short, attributed quotes. |
| [`standards-editor`](#standards-editor) | Standards Editor (rules engine) | built | none | per-episode (after the checkers, every revision) | Make the publish decision with fixed, auditable rules: PUBLISH, REWRITE, HOLD or KILL. |
| [`corrections-agent`](#corrections-agent) | Corrections Agent | built | sonnet | event:correction.opened | Fix mistakes fast and in public: show notes, feeds and on-air corrections. |
| [`recheck-monitor`](#recheck-monitor) | Re-check Monitor | built | opus | cron "0 8 * * *" (daily: recheck --days 7); breaking and strict claims more often in the first 48 h | Keep checking published claims after they air, because stories change. |
| [`source-ledger-keeper`](#source-ledger-keeper) | Source Ledger Keeper | next | haiku | weekly + event:ownership.change | Keep the source map honest: who owns which outlet, which accounts are official, and which sources keep getting it wrong. |
| [`media-authenticity-checker`](#media-authenticity-checker) | Media Authenticity Checker | future | opus | per-episode when photos, video or audio are cited as evidence (mostly breaking) | Check whether photos, video and audio cited as evidence are real, original and unaltered. |
| [`hoax-red-team`](#hoax-red-team) | Hoax Red Team | next | opus | weekly + before major releases | Attack our own trust stack with realistic hoaxes, so we find the holes before bad actors do. |
| [`transparency-reporter`](#transparency-reporter) | Transparency Reporter | next | sonnet | cron "0 14 1 * *" (monthly, on the 1st) | Publish how the trust stack performed, every month, in plain language. |

<a id="claim-extractor"></a>
### `claim-extractor`: Claim Extractor

> List every checkable assertion in the script, including the ones the writer forgot to map.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Opus tier | per-episode (every revision) | `standards-editor` | `earlobe/trust/claims.py` |

extract_claims(script, llm) reads the script cold, in its own isolated call, and lists each assertion as a Claim with a type (fact, number, quote, attribution, allegation, legal status, prediction, context), risk flags, and whether it is attributed on air. It adds any claim the Producer did not map, so nothing slips past verification by being unlabeled. It does not judge truth; it only makes sure the checkers have the complete list.

- **Inputs:** Script
- **Outputs:** Script (complete Claim map)
- **Tools:** `none (LLM only)`
- **Instances:** one isolated call per script revision
- **KPIs:**
  - unmapped assertions found later by checkers or recheck (target 0)
  - claims added per script (trend)
  - claim-type accuracy on the golden set

<a id="source-verifier"></a>
### `source-verifier`: Source Verifier (blind)

> Re-source every claim blind, from scratch, and count only truly independent support.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Opus tier | per-episode | `standards-editor` | `earlobe/trust/verifier.py` |

verify(script, llm, owners, max_searches=20) never sees the writer's sources. For each claim it searches independently, traces wire copy back to its origin, and collapses outlets owned by the same group using config/owners.yaml, so one AP story republished by ten stations counts once. independent_count is recomputed in code, never taken from the model. It records whether a tier-1 primary source (court record, official release, original data) supports the claim, which the strict and breaking lanes require for sensitive claims.

- **Inputs:** Script (claims only, sources withheld); config/owners.yaml
- **Outputs:** VerifierReport
- **Tools:** `web_search`, `web_fetch`, `courtlistener`
- **Instances:** one isolated call per script revision
- **KPIs:**
  - catch rate on known-false golden claims (target >= 99%)
  - wire-duplication counting errors (target 0)
  - searches per claim (cost)

<a id="fact-checker"></a>
### `fact-checker`: Fact Checker

> Check that each claim, as worded, says exactly what the evidence says.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Opus tier | per-episode | `standards-editor` | `earlobe/trust/factcheck.py` |

fact_check(script, verifier_report, llm) compares wording with evidence: numbers and units, dates and tense, quotes word for word, who said what, and legal status ('charged' is not 'convicted'). It rates each claim accurate, minor_issue, misleading, inaccurate or unverifiable, with a suggested fix. Misleading or inaccurate blocks the episode (gate rule F1); unverifiable wording must be softened or cut (F2). In 'translation mode' it also checks Spanish editions against the gated English claims.

- **Inputs:** Script; VerifierReport
- **Outputs:** FactCheckReport
- **Tools:** `web_fetch`
- **Instances:** one isolated call per script revision
- **KPIs:**
  - post-publish corrections traced to wording (target 0)
  - accuracy_rate per show
  - needless rewrites from false positives

<a id="bias-checker"></a>
### `bias-checker`: Bias Checker

> Catch loaded language, one-sided framing and missing perspectives before they air.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Opus tier | per-episode | `standards-editor` | `earlobe/trust/bias.py` |

bias_check(script, llm) reviews every line for loaded language, one-sidedness, missing perspectives, framing, speculation, sensationalism, stereotypes and false balance, and returns a 0-100 balance_score. Any high-severity issue blocks (B2), and a score under the lane minimum blocks (B1) with the missing perspectives the rewrite must add. It checks fairness, not conclusions: when the record is clear, it does not demand false balance.

- **Inputs:** Script
- **Outputs:** BiasReport
- **Tools:** `none (LLM only)`
- **Instances:** one isolated call per script revision
- **KPIs:**
  - average balance_score by show
  - upheld listener bias complaints (target 0)
  - agreement with the Eval Steward's labeled bias set

<a id="legal-screener"></a>
### `legal-screener`: Legal / Defamation Screener

> Screen every script for defamation, privacy and legal risk before it can publish.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Opus tier | per-episode | `standards-editor` | `earlobe/trust/legal.py` |

legal_screen(script, llm) checks names, minors, victims, allegations, presumption of innocence, privacy, copyright and medical claims, and returns issues with severity and a fix. Naming a minor or a victim is a hard stop: if it survives the rewrite budget, the gate KILLs the episode (rule L2). Other issues block at the lane's threshold (high in standard, medium in strict and breaking). In 'ad mode' it also screens sponsor reads for unsubstantiated claims and missing ad disclosure. It is a screen, not a lawyer: real legal threats go to the Contracts & IP Clerk and the founders.

- **Inputs:** Script
- **Outputs:** LegalReport
- **Tools:** `none (LLM only)`
- **Instances:** one isolated call per script revision
- **KPIs:**
  - legal complaints or takedown demands after publish (target 0)
  - hard-stop issues still present at the final revision (target 0)
  - issues per 1,000 words (trend)

<a id="harm-sensitivity-reviewer"></a>
### `harm-sensitivity-reviewer`: Harm & Sensitivity Reviewer

> Make sure coverage of crime, death and tragedy does not cause avoidable harm.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Opus tier | per-episode (strict and breaking lanes; sampled on the others) | `standards-editor` | — |

Separate from legal risk, it reviews scripts against safe-reporting practice for suicide, mass violence (no notoriety for attackers), sexual violence, harm to children and mental illness, plus graphic detail, copycat risk and how victims and families are portrayed. It returns a HarmReport (proposed contract) with issues, severity and fixes, read by the gate through a new rule family (H1/H2, proposed for gate.py). It matters most for Case Tracker, Cold Case Files and breaking coverage of deaths and attacks, which are core formats for this network.

- **Inputs:** Script
- **Outputs:** HarmReport (proposed)
- **Tools:** `none (LLM only)`
- **Instances:** one isolated call per script revision
- **KPIs:**
  - high-severity harm issues reaching publish (target 0)
  - harm-related listener complaints
  - agreement with the Eval Steward's golden harm set

<a id="originality-checker"></a>
### `originality-checker`: Originality Checker

> Make sure every script is in our own words, with only short, attributed quotes.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Haiku tier | per-episode | `standards-editor` | — |

Compares the script with the text of its sources and the verifier's evidence using n-gram overlap in code, then a Haiku-tier pass decides whether each long overlap is fair quotation (short, attributed, in quote marks) or copying. Any unquoted run over a set length (default 12 words) becomes a blocking LegalIssue with risk 'copyright' for the gate. This enforces conventions rule 7 mechanically: report facts in our own words and link sources.

- **Inputs:** Script; Source excerpts and fetched text
- **Outputs:** LegalIssue (risk=copyright)
- **Tools:** `web_fetch`
- **Instances:** one isolated call per script revision
- **KPIs:**
  - copied passages found after publish (target 0)
  - false flags on properly attributed quotes
  - check time per script (target < 30 s)

<a id="standards-editor"></a>
### `standards-editor`: Standards Editor (rules engine)

> Make the publish decision with fixed, auditable rules: PUBLISH, REWRITE, HOLD or KILL.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode (after the checkers, every revision) | `network-director` | `earlobe/trust/gate.py (decide, POLICIES) + earlobe/trust/loop.py (run_trust_loop)` |

decide(...) reads the checkers' JSON reports and applies the lane policy (standard, strict, breaking, archive). It blocks on uncovered, contradicted or unsupported claims (V0-V2), too few independent sources (V3), sensitive claims without an official record (V4), unattributed predictions (V5), fact-check failures (F0-F2), bias (B1-B2), legal issues (L1-L2) and a missing AI disclosure (S1). REWRITE sends instructions back to the Producer up to the lane's limit; HOLD is breaking-only, for stories that look real but are not confirmed enough yet; KILL ends the episode. No model makes this decision, so the same reports always give the same answer, which is what makes the Trust Stack auditable and sellable.

- **Inputs:** Script; VerifierReport; FactCheckReport; BiasReport; LegalReport; HarmReport (next)
- **Outputs:** GateDecision; trust log entry
- **Tools:** `none`
- **Instances:** single rules engine; one policy per lane
- **KPIs:**
  - decisions reproducible from stored reports (100%)
  - post-publish corrections per 100 episodes
  - KILL rate by show (watched for trend)

<a id="corrections-agent"></a>
### `corrections-agent`: Corrections Agent

> Fix mistakes fast and in public: show notes, feeds and on-air corrections.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Sonnet tier | event:correction.opened | `standards-editor` | `earlobe/monitor/corrections.py` |

open_correction(...) records a Correction from the Re-check Monitor, a listener (through the Community Manager) or an outlet. apply_correction(store, correction) reissues the episode's show notes and feed item with a dated correction note, and for significant errors schedules an on-air correction at the top of that show's next episode. A retraction pulls the episode from the feed and replaces it with a notice. Every correction is written to the public trust log.

- **Inputs:** Correction; Episode
- **Outputs:** Correction (applied); reissued notes and feed item; on-air correction line
- **Tools:** `host_api`, `sql`
- **Instances:** single
- **KPIs:**
  - median hours from correction opened to applied (target < 4)
  - significant corrections aired in the next episode (100%)
  - repeat errors of the same type

<a id="recheck-monitor"></a>
### `recheck-monitor`: Re-check Monitor

> Keep checking published claims after they air, because stories change.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | Opus tier | cron "0 8 * * *" (daily: recheck --days 7); breaking and strict claims more often in the first 48 h | `corrections-agent` | `earlobe/monitor/recheck.py` |

recheck(store, llm, days=7) re-verifies the claims in the last week's episodes: charges dropped, casualty counts revised, a quote retracted, a vote reversed. When the record has moved, it opens a Correction or an update with the new evidence. It turns verification from a one-time gate into an ongoing promise.

- **Inputs:** published Episodes and their Scripts; VerifierReport history
- **Outputs:** Correction
- **Tools:** `web_search`, `courtlistener`
- **Instances:** single
- **KPIs:**
  - changed facts caught before a listener reports them
  - strict and breaking claims rechecked (100%)
  - cost per recheck run

<a id="source-ledger-keeper"></a>
### `source-ledger-keeper`: Source Ledger Keeper

> Keep the source map honest: who owns which outlet, which accounts are official, and which sources keep getting it wrong.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Haiku tier | weekly + event:ownership.change | `source-verifier` | — |

Maintains config/owners.yaml (outlet to owner group, plus the wires list) from ownership changes reported by Industry Intel, so independence counts stay right after mergers and sales. Keeps a registry of verified official accounts and domains (police, courts, agencies) and catches lookalike domains used in hoaxes. Tracks each outlet's record of claims later contradicted or corrected, which can lower its tier. Its changes go through the Release Guard like any other config change.

- **Inputs:** Industry Intel ownership news; VerifierReport history; Correction
- **Outputs:** owners.yaml change requests; official account registry; outlet track record
- **Tools:** `web_search`, `sql`
- **Instances:** single
- **KPIs:**
  - ownership changes reflected within 7 days
  - lookalike-domain hoaxes caught
  - unknown outlets appearing in evidence per week (should fall)

<a id="media-authenticity-checker"></a>
### `media-authenticity-checker`: Media Authenticity Checker

> Check whether photos, video and audio cited as evidence are real, original and unaltered.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Opus tier | per-episode when photos, video or audio are cited as evidence (mostly breaking) | `source-verifier` | — |

Breaking news brings recycled photos, edited clips and AI-generated media. This agent checks provenance (content credentials such as C2PA where present), the earliest appearance online, reverse-image search results and signs of manipulation, using vision-capable model calls. Media it cannot authenticate cannot support a claim on air. It also screens our own clips and art for anything that could be mistaken for real footage.

- **Inputs:** media URLs in evidence
- **Outputs:** authenticity findings (proposed)
- **Tools:** `web_search`, `web_fetch`
- **Instances:** one per flagged media item
- **KPIs:**
  - manipulated media caught in red-team tests
  - claims resting on unauthenticated media (target 0)
  - minutes added to breaking flashes

<a id="hoax-red-team"></a>
### `hoax-red-team`: Hoax Red Team

> Attack our own trust stack with realistic hoaxes, so we find the holes before bad actors do.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Opus tier | weekly + before major releases | `eval-steward` | — |

Writes adversarial test cases and runs them in dry-run only, never published: fake press releases on lookalike domains, hoax celebrity deaths, satire presented as news, recycled disaster photos, one wire story republished widely to fake independence, and prompt injections hidden in source pages. It records where each case was stopped (sensor, desk, verifier, gate) or whether it got through, and files the fix. Every case joins the Eval Steward's golden sets, so it is tested forever after.

- **Inputs:** the pipeline in dry-run; real hoax patterns from Industry Intel
- **Outputs:** red-team report; new golden cases
- **Tools:** `web_search`
- **Instances:** single
- **KPIs:**
  - hoaxes stopped before a PUBLISH decision (target 100%)
  - new attack classes added per month
  - days from discovered hole to fix

<a id="transparency-reporter"></a>
### `transparency-reporter`: Transparency Reporter

> Publish how the trust stack performed, every month, in plain language.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | cron "0 14 1 * *" (monthly, on the 1st) | `standards-editor` | — |

Builds a public report from the trust log and the store: claims checked, share corroborated, rewrites, holds, kills, corrections and median time to correct, by show and lane, plus notable catches. It is published on the network website and linked from show notes. It is both an accountability tool and the best sales evidence for the Trust Stack product. Every number is computed from logs; the model only writes the words around them.

- **Inputs:** trust log; GateDecision; Correction
- **Outputs:** monthly transparency report (web page + PDF)
- **Tools:** `sql`
- **Instances:** single
- **KPIs:**
  - report published on the 1st each month
  - numbers that reconcile to logs (100%)
  - Trust Stack leads that cite the report

## Studio desk

Turns gated scripts into broadcast-quality audio with original synthetic personas (Mara, Theo, Lena, Marcus, Ava, June). ElevenLabs is the primary engine. The Studio Operator, which drives UI-only engines through computer use, is an optional second studio. Every episode ends with the spoken AI disclosure and carries it in metadata. *Vendor features and terms (ElevenLabs, NotebookLM, Meta Muse, music libraries): as of Oct 2026, verify before buying.*

9 agents: 3 built, 5 next, 1 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`voice-director`](#voice-director) | Voice Director | next | sonnet | on-demand + weekly review | Cast, design and direct the network's original synthetic voices so each persona is consistent and clearly original. |
| [`pronunciation-keeper`](#pronunciation-keeper) | Pronunciation Keeper | next | haiku | per-episode + event:qa.mispronunciation | Say every local name right, every time. |
| [`studio-voice`](#studio-voice) | Studio Voice (ElevenLabs) | built | none | per-episode (only after PUBLISH) | Turn each approved script line into audio in the right persona's voice. |
| [`studio-operator`](#studio-operator) | Studio Operator (computer use) | future | sonnet | on-demand | Drive UI-only audio engines such as NotebookLM and Meta Muse through computer use, as an optional second studio. |
| [`sound-designer`](#sound-designer) | Sound Designer / Mixer | built | none | per-episode | Assemble each episode: voices, music, transitions and consistent loudness. |
| [`sonic-brand-librarian`](#sonic-brand-librarian) | Sonic Brand Librarian | next | sonnet | on-demand + monthly rotation | Give the network and every show a recognizable, properly licensed sound. |
| [`disclosure-agent`](#disclosure-agent) | Disclosure Agent | built | none | per-episode (before the gate) | Make sure every episode ends with the AI disclosure and carries it in its metadata. |
| [`qa-listener`](#qa-listener) | QA Listener | next | haiku | per-episode (after the mix, before publish) | Listen back to every episode and catch what the script can't show: mispronunciations, glitches, silence and bad levels. |
| [`art-director`](#art-director) | Art Director | next | sonnet | event:show.greenlit + per-episode (episode art)  | Make every show look like part of one network: cover art, episode art, thumbnails and social cards. |

<a id="voice-director"></a>
### `voice-director`: Voice Director

> Cast, design and direct the network's original synthetic voices so each persona is consistent and clearly original.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | on-demand + weekly review | `network-director` | — |

Owns config/voices.yaml and the persona bibles for Mara, Theo, Lena, Marcus, Ava and June, plus new personas (Spanish editions, niche feeds, a non-news voice for sponsor reads). It designs new voices with ElevenLabs voice design tools (as of Oct 2026, verify) and confirms none is modeled on, named after or imitating a real person. It sets delivery direction per format (calm and precise for Ava, measured for June) and checks consistency across episodes using QA Listener reports. It casts personas for new shows and keeps any one voice from being overexposed across feeds.

- **Inputs:** config/voices.yaml; QAReport (proposed); show bibles
- **Outputs:** persona specs; voices.yaml change requests; casting per show
- **Tools:** `elevenlabs`
- **Instances:** single
- **KPIs:**
  - voice consistency flags per week
  - listener sentiment about voice quality
  - personas with a written bible (100%)

<a id="pronunciation-keeper"></a>
### `pronunciation-keeper`: Pronunciation Keeper

> Say every local name right, every time.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Haiku tier | per-episode + event:qa.mispronunciation | `voice-director` | — |

Keeps a pronunciation lexicon per market for place names, streets, officials and local terms that trip up synthetic voices (for example Huger Street, Congaree, Los Feliz, Cahuenga, Goethe Street). Before rendering it marks those words in the script and applies the lexicon through the TTS engine's pronunciation dictionary or alias features (verify against ElevenLabs docs). New names flagged by the Copy Editor are checked against local pronunciation sources, and QA Listener flags are fed back in. A mispronounced street tells local listeners we are not from there; this agent prevents that.

- **Inputs:** Script; QA Listener flags; Copy Editor requests
- **Outputs:** lexicon entries; script with pronunciation markup
- **Tools:** `elevenlabs`, `web_search`
- **Instances:** single agent; one lexicon per market
- **KPIs:**
  - mispronunciations caught in QA per episode (trending to 0)
  - listener pronunciation complaints
  - lexicon entries per market (growing)

<a id="studio-voice"></a>
### `studio-voice`: Studio Voice (ElevenLabs)

> Turn each approved script line into audio in the right persona's voice.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode (only after PUBLISH) | `voice-director` | `earlobe/studio/tts.py` |

ElevenLabsTTS(api_key, model_id).synthesize(text, voice_id) renders each line with the persona's voice_id from env (VOICE_MARA and so on) and the TTS model named in ELEVENLABS_TTS_MODEL; DryRunTTS stands in for tests. Only gated scripts reach it. Character usage is logged to AgentRun for the Budget Controller and the Quota Sentinel. Next increment: caching unchanged lines such as the disclosure outro, and line-level re-renders requested by the QA Listener.

- **Inputs:** Script (gated); config/voices.yaml
- **Outputs:** audio per line
- **Tools:** `elevenlabs`
- **Instances:** one per episode render
- **KPIs:**
  - render failures per 100 episodes
  - characters per finished minute (cost)
  - re-renders requested by QA

<a id="studio-operator"></a>
### `studio-operator`: Studio Operator (computer use)

> Drive UI-only audio engines such as NotebookLM and Meta Muse through computer use, as an optional second studio.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | on-demand | `voice-director` | — |

The interface stub exists in earlobe/studio/operator.py. Some engines only have a web UI, so this agent would operate them with computer use: upload a gated research pack, generate audio, download the result. The catch: those engines write their own words, which breaks the claim map, so their output must be transcribed and sent through the full trust stack (claims, verifier, fact, bias, legal, gate) before it can publish. Platform terms must allow automated use (cleared by Compliance & Platform Policy Watch). Best fit: evergreen deep dives and bonus episodes, not news.

- **Inputs:** ResearchPack (gated); engine credentials from env
- **Outputs:** raw audio; transcript for re-verification
- **Tools:** `computer_use`, `stt`
- **Instances:** one session per job
- **KPIs:**
  - operator jobs completed without manual help
  - operator episodes that pass the gate after transcription
  - terms-of-service issues (target 0)

<a id="sound-designer"></a>
### `sound-designer`: Sound Designer / Mixer

> Assemble each episode: voices, music, transitions and consistent loudness.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode | `voice-director` | `earlobe/studio/mix.py` |

render(script, voices, tts, out_path, music_bed=None) concatenates the rendered lines with ffmpeg, adds the music bed and stings, and normalizes loudness to the network target of -16 LUFS. It returns the file path and duration for the Episode record. Next increment: segment timestamps for chapters and ad markers, so Ad Ops can insert pre-, mid- and post-rolls at clean breaks.

- **Inputs:** line audio; music assets
- **Outputs:** episode MP3; duration_sec; segment timestamps (next)
- **Tools:** `ffmpeg`
- **Instances:** one per episode
- **KPIs:**
  - integrated loudness within 1 LU of target
  - audio artifacts flagged by QA
  - render time per episode

<a id="sonic-brand-librarian"></a>
### `sonic-brand-librarian`: Sonic Brand Librarian

> Give the network and every show a recognizable, properly licensed sound.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | on-demand + monthly rotation | `voice-director` | — |

Owns the network sonic logo, show themes, beds, stings and transitions, including a distinct Breaking Desk sting that signals seriousness without alarm. It keeps a license record for every asset (source, terms, commercial use, attribution) and sources music from royalty-free libraries or AI music tools whose terms allow commercial podcast use (verify terms, as of Oct 2026). It rotates beds to avoid fatigue and supplies sound packages to the Show Launcher. No asset ships without a license record.

- **Inputs:** show bibles; brand book
- **Outputs:** audio asset library; license register
- **Tools:** `web_search`
- **Instances:** single
- **KPIs:**
  - assets without a license record (target 0)
  - copyright claims or takedowns (target 0)
  - days to deliver a new show's sound package

<a id="disclosure-agent"></a>
### `disclosure-agent`: Disclosure Agent

> Make sure every episode ends with the AI disclosure and carries it in its metadata.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode (before the gate) | `standards-editor` | `earlobe/producer/disclosure.py` |

disclosure_lines(show_cfg, voices) and ensure_disclosure(script, show_cfg, voices) append the standard AI disclosure outro at the end of every episode, voiced by the disclosure voice (Ava). The Feed Manager also writes the disclosure into episode metadata. The gate blocks any script without a disclosure segment (rule S1), so an undisclosed episode cannot publish. The text is versioned; changes come from Compliance & Platform Policy Watch.

- **Inputs:** Script; show config; config/voices.yaml
- **Outputs:** Script with disclosure segment; Episode.disclosure_text
- **Tools:** `none`
- **Instances:** one per episode
- **KPIs:**
  - episodes without disclosure (target 0)
  - disclosure audible at the end in QA (100%)
  - policy-required wording updates applied within 7 days

<a id="qa-listener"></a>
### `qa-listener`: QA Listener

> Listen back to every episode and catch what the script can't show: mispronunciations, glitches, silence and bad levels.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Haiku tier | per-episode (after the mix, before publish) | `voice-director` | — |

Transcribes the rendered audio with speech-to-text (ElevenLabs STT; verify against docs) and compares it with the script: word error rate per line, skipped or repeated words, and mispronunciation candidates for the Pronunciation Keeper. ffmpeg measures integrated loudness and true peak, clipping, silences over 2 seconds and duration vs target, and confirms the disclosure is audible at the end. It returns a QAReport (proposed contract): PASS, RERENDER (named lines, up to two tries) or FAIL, and FAIL blocks the Publisher. The model only reads the transcript diff; every audio measurement is code.

- **Inputs:** episode audio; Script
- **Outputs:** QAReport (proposed); re-render requests
- **Tools:** `stt`, `ffmpeg`
- **Instances:** one per episode
- **KPIs:**
  - audio defects that reach listeners (target 0)
  - re-render success rate
  - QA minutes per episode

<a id="art-director"></a>
### `art-director`: Art Director

> Make every show look like part of one network: cover art, episode art, thumbnails and social cards.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | event:show.greenlit + per-episode (episode art)  | `brand-guardian` | — |

Builds show cover art from network templates (one family look, show name legible at thumbnail size, platform size specs verified as of Oct 2026), plus episode art for YouTube and social and templated cards for clips. It works through Canva brand templates or an image model with a commercial license. It never uses a real person's likeness, never makes images that look like news photos of real events, and labels AI imagery where platforms require it. The Brand Guardian checks every asset before it ships.

- **Inputs:** ShowSpec (proposed); brand book; Copy
- **Outputs:** cover art; episode art; thumbnails; social cards
- **Tools:** `canva`, `image_gen`
- **Instances:** single
- **KPIs:**
  - assets rejected by the Brand Guardian
  - YouTube thumbnail CTR
  - days to produce a new show's art

## Distribution desk

Gets every episode everywhere, correctly: host, RSS, directories, website, YouTube, transcripts, clips and partner packages. It also keeps the catalog clean. Quiet Please, Inception Point AI's network, was hidden by Castro and flagged by the Podcast Index for flooding directories, and this desk is built so that never happens to us. *Directory submission flows, YouTube policy and artwork specs: as of Oct 2026, verify.*

11 agents: 2 built, 8 next, 1 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`publisher`](#publisher) | Publisher | built | none | per-episode (after PUBLISH and, once live, QA PASS) | Put the finished episode on the host with complete notes, sources and a verification summary. |
| [`feed-manager`](#feed-manager) | Feed Manager | built | none | per-episode + on every correction or retraction | Keep every show's RSS feed valid, complete and honest. |
| [`show-launcher`](#show-launcher) | Show Launcher | next | sonnet | event:show.greenlit | Spin up a complete new show from a template in a day or two: config, sources, bible, art, trailer and platform listings. |
| [`directory-sync-checker`](#directory-sync-checker) | Directory Sync Checker | next | none | cron "15 * * * *" (hourly) | Confirm every episode actually shows up on every platform, and say so fast when it doesn't. |
| [`seo-metadata`](#seo-metadata) | SEO / Metadata | next | sonnet | per-episode + monthly audit | Make every show and episode easy to find in podcast apps, search engines and YouTube. |
| [`transcript-accessibility`](#transcript-accessibility) | Transcript & Accessibility | next | haiku | per-episode | Publish an accurate transcript, chapters and captions for every episode. |
| [`clip-maker`](#clip-maker) | Clip Maker | next | sonnet | per-episode | Cut the best 30-60 seconds of each episode into audiograms and vertical videos. |
| [`youtube-packager`](#youtube-packager) | YouTube / Video Packager | next | sonnet | per-episode | Turn every episode into a proper YouTube podcast episode: video, chapters, captions and playlists. |
| [`website-publisher`](#website-publisher) | Website Publisher | next | none | event:episode.published + nightly rebuild | Run the network website: a page for every show, episode, source list, correction and trust report. |
| [`syndication-packager`](#syndication-packager) | Syndication Packager | future | haiku | per-episode for partner feeds | Package our briefs for other outlets: radio-ready cuts, smart-speaker briefings and news-site embeds. |
| [`catalog-steward`](#catalog-steward) | Catalog & Platform Standing Steward | next | haiku | per show greenlight + weekly catalog audit + event:platform.flag | Keep the catalog clean so podcast apps treat us as a real network, not a spam farm. |

<a id="publisher"></a>
### `publisher`: Publisher

> Put the finished episode on the host with complete notes, sources and a verification summary.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode (after PUBLISH and, once live, QA PASS) | `network-director` | `earlobe/publish/hosts.py, notes.py, trustlog.py` |

Uploads audio through a HostAdapter (LocalHost for testing; TransistorHost, marked 'verify vs docs'), writes show notes with show_notes(script, decision, copy) including the sources and a plain-language verification summary, and appends the gate decision to the public trust log with trustlog.append(...). It marks the Episode published with its audio URL, GUID and duration. It acts only on episodes with a PUBLISH decision and, once the QA Listener is live, a QA PASS.

- **Inputs:** Episode; GateDecision; Copy; episode audio
- **Outputs:** Episode (published); trust log line; event:episode.published
- **Tools:** `host_api`
- **Instances:** one per episode
- **KPIs:**
  - publish failures per 100 episodes
  - minutes from QA pass to live
  - episodes with complete sources in their notes (100%)

<a id="feed-manager"></a>
### `feed-manager`: Feed Manager

> Keep every show's RSS feed valid, complete and honest.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **built** | none (code) | per-episode + on every correction or retraction | `publisher` | `earlobe/publish/feed.py` |

build_feed(...) and write_feed(...) produce RSS with iTunes and podcast-namespace tags, stable GUIDs, and the AI disclosure in each item's metadata. Feeds rebuild on every publish and every correction or retraction, so directories pick up fixes. `python -m earlobe feeds` rebuilds every feed from the store. It also carries show-level metadata such as category, language and location for local shows.

- **Inputs:** Episode records; show config
- **Outputs:** RSS feed per show
- **Tools:** `host_api`
- **Instances:** one feed per show
- **KPIs:**
  - feed validation errors (target 0)
  - corrections reflected in the feed within 1 h
  - GUID changes on existing items (target 0)

<a id="show-launcher"></a>
### `show-launcher`: Show Launcher

> Spin up a complete new show from a template in a day or two: config, sources, bible, art, trailer and platform listings.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Sonnet tier | event:show.greenlit | `programming-director` | — |

Takes a ShowSpec from the Programming Director and builds the whole package: a shows.yaml entry, a seeded sources file (with that market's Beat agent), a show bible draft (with the showrunner), cover art (Art Director), a sound package (Sonic Brand Librarian), a trailer episode that runs the full trust stack, and the host feed. It has the Contracts & IP Clerk clear the show name first. It then submits the feed to Apple Podcasts, Spotify, YouTube and Amazon Music; any step that needs a one-time account action goes to the Studio Operator or to a founder (verify current submission flows, as of Oct 2026). The Release Guard dry-runs the new show before it is enabled.

- **Inputs:** ShowSpec (proposed); show templates
- **Outputs:** shows.yaml entry; sources file; show bible; trailer Episode; directory submissions
- **Tools:** `host_api`, `computer_use`, `canva`
- **Instances:** one job per greenlit show
- **KPIs:**
  - days from greenlight to first episode (target <= 2)
  - launch checklist completeness (100%)
  - directory approvals on the first try

<a id="directory-sync-checker"></a>
### `directory-sync-checker`: Directory Sync Checker

> Confirm every episode actually shows up on every platform, and say so fast when it doesn't.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | none (code) | cron "15 * * * *" (hourly) | `feed-manager` | — |

After each publish it checks that the episode appears on Apple Podcasts, Spotify, YouTube, Amazon Music and Podcast Index within the expected window, using public lookup endpoints and feed checks. It also validates feeds, artwork and enclosure URLs, and watches for shows that were delisted or flagged. Misses raise event:run.failed for the Incident Commander.

- **Inputs:** Episode; RSS feeds
- **Outputs:** sync status per episode; event:run.failed
- **Tools:** `host_api`, `web_fetch`
- **Instances:** single
- **KPIs:**
  - episodes missing from a platform after 6 h (target 0)
  - hours to detect a delisting
  - false alarms per week

<a id="seo-metadata"></a>
### `seo-metadata`: SEO / Metadata

> Make every show and episode easy to find in podcast apps, search engines and YouTube.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | per-episode + monthly audit | `publisher` | — |

Sets show titles, descriptions, categories and keywords using the Trend Scout's search data, adds podcast-namespace tags such as location (local shows), transcript and chapters, and writes schema.org PodcastSeries and PodcastEpisode data for the website. It checks that episode titles carry the terms people search (the place and the subject) without keyword stuffing or misleading wording. Monthly it audits rankings for key searches per market, such as 'Columbia news podcast' or 'LA court news'.

- **Inputs:** Copy; TopicBrief (proposed); search data
- **Outputs:** metadata updates; structured data; monthly SEO audit
- **Tools:** `web_search`, `analytics_api`
- **Instances:** single
- **KPIs:**
  - ranking for target searches per market
  - organic search visits to episode pages
  - metadata completeness (100%)

<a id="transcript-accessibility"></a>
### `transcript-accessibility`: Transcript & Accessibility

> Publish an accurate transcript, chapters and captions for every episode.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Haiku tier | per-episode | `publisher` | — |

Builds the transcript from the final script, aligned to audio timestamps from the QA Listener's speech-to-text, with speakers labeled by persona name and marked as AI voices. It publishes VTT/SRT files and the podcast:transcript tag, generates chapters from the script segments, and supplies captions for video. It keeps the website's episode pages accessible: headings, alt text, keyboard-friendly players. Transcripts serve deaf and hard-of-hearing listeners, search, and the trust story: every word we said is on the record.

- **Inputs:** Script; STT timestamps; segment timestamps
- **Outputs:** transcript files; chapters JSON; captions
- **Tools:** `stt`
- **Instances:** one per episode
- **KPIs:**
  - episodes with a transcript at publish (100%)
  - transcript vs audio mismatch rate
  - accessibility audit issues open

<a id="clip-maker"></a>
### `clip-maker`: Clip Maker

> Cut the best 30-60 seconds of each episode into audiograms and vertical videos.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | per-episode | `social-media-manager` | — |

Picks moments that stand alone and contain only gated content with the attribution intact, then renders audiograms (waveform, captions, show art) and vertical captioned videos with ffmpeg. Every clip carries an 'AI-voiced' caption and a link to the full episode and its sources. Crime and tragedy are never clipped for shock value. Output goes to the Social Media Manager and the YouTube Packager.

- **Inputs:** episode audio; transcript; Copy
- **Outputs:** ClipSpec (proposed) + audiogram and vertical video files
- **Tools:** `ffmpeg`
- **Instances:** one job per episode
- **KPIs:**
  - clip view-through rate
  - episode listens from clip links
  - clips flagged by the Brand Guardian

<a id="youtube-packager"></a>
### `youtube-packager`: YouTube / Video Packager

> Turn every episode into a proper YouTube podcast episode: video, chapters, captions and playlists.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | per-episode | `publisher` | — |

Renders full-episode videos (show art, waveform, captions) with ffmpeg, uploads through the YouTube Data API or YouTube's RSS podcast ingestion (verify current options, as of Oct 2026), and sets titles, descriptions, chapters, playlists and thumbnails. It applies YouTube's altered-or-synthetic-content disclosure as policy requires. It builds per-market playlists so local listeners can catch up on the week.

- **Inputs:** episode audio; art; Copy; chapters
- **Outputs:** YouTube videos; playlists
- **Tools:** `youtube_api`, `ffmpeg`
- **Instances:** one channel per network brand; one playlist per show
- **KPIs:**
  - watch time per show
  - subscriber growth
  - policy strikes (target 0)

<a id="website-publisher"></a>
### `website-publisher`: Website Publisher

> Run the network website: a page for every show, episode, source list, correction and trust report.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | none (code) | event:episode.published + nightly rebuild | `publisher` | — |

Generates a static site from the store: network home, market pages, show pages, and episode pages with player, transcript, sources, verification summary and correction history. It hosts the public trust log, the monthly transparency report and the newsletter signup. Static generation keeps it cheap, fast and hard to break, and owned pages make the network searchable and give sponsors a place to send people.

- **Inputs:** Episode; transcripts; trust log; transparency reports
- **Outputs:** static website
- **Tools:** `ci`
- **Instances:** single site; one section per market
- **KPIs:**
  - episode pages live within 15 min of publish
  - uptime
  - newsletter signups from the site

<a id="syndication-packager"></a>
### `syndication-packager`: Syndication Packager

> Package our briefs for other outlets: radio-ready cuts, smart-speaker briefings and news-site embeds.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Haiku tier | per-episode for partner feeds | `content-licensing-agent` | — |

Produces radio-ready cuts of local briefs (:60, :90, 2:00) with clean in and out cues and a log, smart-speaker briefing feeds where platforms still support them (verify, as of Oct 2026), and embeddable players for partner news sites. Each package keeps the AI disclosure and credits the Curious & Creative Network. It delivers to each partner on their schedule and format.

- **Inputs:** published episodes; partner specs
- **Outputs:** syndication packages
- **Tools:** `ffmpeg`, `host_api`
- **Instances:** one delivery job per partner
- **KPIs:**
  - partner deliveries on time (100%)
  - partner stations and sites carrying our content
  - syndication revenue

<a id="catalog-steward"></a>
### `catalog-steward`: Catalog & Platform Standing Steward

> Keep the catalog clean so podcast apps treat us as a real network, not a spam farm.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Haiku tier | per show greenlight + weekly catalog audit + event:platform.flag | `programming-director` | — |

This agent exists because of Quiet Please (Inception Point AI, now Liquid Studios). Castro hid every one of its shows from search and charts for 'keying on popular searches in order to flood search results', and the Podcast Index added a /recent/problematic list for low-effort AI shows (docs/research/notes/inception-point-business-model.md). Before any greenlight it checks portfolio rules: no near-duplicate shows, no launching several title variants of one show, titles that describe the show instead of stuffing search terms, and AI disclosure in the show description and every item. Weekly it audits every live feed against its minimum-news rule and audience floor, then has the Programming Director pause or retire dormant feeds instead of leaving them to rot. It checks our feeds against the Podcast Index problematic list and each directory's standing (with the Directory Sync Checker), and can block a Show Launcher job that would break a rule.

- **Inputs:** ShowSpec (proposed); RSS feeds; InsightReport (proposed); Podcast Index API; directory listings
- **Outputs:** catalog rule check (pass/block with reasons); weekly catalog audit; pause and retire list; event:platform.flag
- **Tools:** `web_fetch`, `host_api`, `sql`
- **Instances:** single
- **KPIs:**
  - shows hidden, flagged or delisted by any directory (target 0)
  - near-duplicate or title-variant feeds live (target 0)
  - feeds below their floor for 30+ days still publishing (target 0)
  - feeds with disclosure in show and item metadata (100%)

## Growth desk

Marketing, end to end: growth strategy, launches, social, newsletters, cross-promo, community, brand, analytics, charts, partnerships and PR. Two rules apply everywhere: growth assets use only gated content, and we are always plainly honest that the voices are AI. *Platform and ad-tool details: as of Oct 2026, verify before buying.*

12 agents: 0 built, 11 next, 1 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`audience-growth-strategist`](#audience-growth-strategist) | Audience Growth Strategist | next | sonnet | weekly (Monday) | Set the growth plan for every show and market, and decide where the effort goes each week. |
| [`market-launch-marketer`](#market-launch-marketer) | Market Launch Marketer | next | sonnet | event:market.launch (30-day program) | Launch each new city loudly and locally, so the first month builds a real audience. |
| [`social-media-manager`](#social-media-manager) | Social Media Manager | next | sonnet | always-on (daily schedule) | Run the network's social accounts so local people find our shows where they already scroll. |
| [`newsletter-editor`](#newsletter-editor) | Newsletter Editor | next | sonnet | per-episode (daily per market) + weekly network digest | Send a daily local newsletter that pairs with each brief and builds an audience we own. |
| [`cross-promo-planner`](#cross-promo-planner) | Cross-Promo Planner | next | sonnet | weekly | Use our own shows to grow each other without annoying anyone. |
| [`community-manager`](#community-manager) | Community & Listener Mail | next | sonnet | always-on | Answer listeners, route their corrections and tips, and keep the community healthy. |
| [`brand-guardian`](#brand-guardian) | Brand Guardian | next | sonnet | per-asset (before release) + monthly audit | Keep everything the public sees on-brand, honest about AI, and never impersonating anyone. |
| [`analytics-insights`](#analytics-insights) | Analytics & Insights | next | sonnet | cron "0 10 * * *" (daily ingest) + weekly InsightReport | Turn listening data into decisions: what to make more of, what to fix, what to stop. |
| [`charts-reviews-monitor`](#charts-reviews-monitor) | Charts & Reviews Monitor | next | haiku | cron "0 13 * * *" (daily) | Know where our shows rank and what listeners say about them, every day. |
| [`partnerships-scout`](#partnerships-scout) | Partnerships Scout (local orgs & radio) | next | sonnet | weekly | Find local partners who make us more trusted and more heard: libraries, universities, radio, newsrooms and civic groups. |
| [`press-pr-agent`](#press-pr-agent) | Press & PR Agent | next | sonnet | event:market.launch, event:show.greenlit + weekly | Tell the network's story to the press: launches, milestones and the trust record. |
| [`paid-growth-manager`](#paid-growth-manager) | Paid Growth Manager | future | sonnet | always-on while campaigns run (daily review) | Buy listeners only where it pays back, with hard daily caps. |

<a id="audience-growth-strategist"></a>
### `audience-growth-strategist`: Audience Growth Strategist

> Set the growth plan for every show and market, and decide where the effort goes each week.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | weekly (Monday) | `network-director` | — |

Reads the InsightReport and sets weekly targets per show (followers, listens, completion) and the channel mix: social, newsletter, partnerships, cross-promo, SEO and, later, paid. It keeps an experiment backlog where every test has a hypothesis and a success metric, and stops tests that don't move the numbers. It coordinates the growth desk so launches, clips and newsletters all serve the same plan.

- **Inputs:** InsightReport (proposed); programming memo; growth budget
- **Outputs:** weekly growth plan; experiment backlog
- **Tools:** `analytics_api`, `sql`
- **Instances:** single
- **KPIs:**
  - network weekly listeners, week over week
  - experiments completed per month
  - cost per new follower

<a id="market-launch-marketer"></a>
### `market-launch-marketer`: Market Launch Marketer

> Launch each new city loudly and locally, so the first month builds a real audience.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Sonnet tier | event:market.launch (30-day program) | `audience-growth-strategist` | — |

Runs a 30-day launch program per market: a launch press release, local partner outreach (with the Partnerships Scout), social accounts and first clips, a newsletter seeded from signups, trailer swaps with existing shows, and a launch week of extra local segments. It localizes the pitch around what the city lacks in daily audio news, phrased in the city's own terms (inference until audience data confirms it). It reports results against targets at day 30 and day 90.

- **Inputs:** market config; ShowSpec (proposed); competitor tracker
- **Outputs:** launch plan; launch assets; 30- and 90-day launch reports
- **Tools:** `email`, `social_api`
- **Instances:** one 30-day program per new market or flagship show
- **KPIs:**
  - followers at day 30 and day 90 per market
  - local partners signed at launch
  - launch press mentions

<a id="social-media-manager"></a>
### `social-media-manager`: Social Media Manager

> Run the network's social accounts so local people find our shows where they already scroll.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | always-on (daily schedule) | `audience-growth-strategist` | — |

Schedules clips, quote cards and episode posts per platform (Instagram, TikTok, YouTube Shorts, Facebook for local audiences, Threads, Bluesky, X), using the Copywriter's social_posts and the Clip Maker's output. Account bios disclose that the voices are AI. It posts only gated content, never argues in replies (the Community Manager handles those) and avoids engagement bait. Breaking posts go out only after the episode is published.

- **Inputs:** Copy; clips; growth plan
- **Outputs:** scheduled posts; social metrics
- **Tools:** `social_api`
- **Instances:** network accounts plus one account set per market as it launches
- **KPIs:**
  - followers per market account
  - clip-to-listen conversion (tracked links)
  - posts removed for policy (target 0)

<a id="newsletter-editor"></a>
### `newsletter-editor`: Newsletter Editor

> Send a daily local newsletter that pairs with each brief and builds an audience we own.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | per-episode (daily per market) + weekly network digest | `audience-growth-strategist` | — |

Turns each daily brief into a short morning email: the stories in text, links to sources and the episode, the weather block and what's happening today. A weekly network digest promotes evergreen and Case Tracker episodes. Subject lines are tested with the Headline Tester, and list hygiene and the legal basics (unsubscribe, sender address, consent) are kept with the Privacy Steward. Email is owned reach that no platform algorithm can take away.

- **Inputs:** Script (gated); Copy; weather block
- **Outputs:** newsletter issues; list metrics
- **Tools:** `email`
- **Instances:** one daily edition per market + one weekly network digest
- **KPIs:**
  - open and click rates
  - subscriber growth per market
  - newsletter-to-podcast follow conversion

<a id="cross-promo-planner"></a>
### `cross-promo-planner`: Cross-Promo Planner

> Use our own shows to grow each other without annoying anyone.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | weekly | `audience-growth-strategist` | — |

Plans house promotion across the network: unsold ad slots carry promos for related shows, trailers are dropped into similar feeds, and episodes end with 'if you liked this' pointers. It matches promos by audience overlap, so a Columbia listener hears about Cold Case Files: Carolinas, not an LA transit feed. It caps promo frequency per feed and gives each promo its own tracking link to measure lift.

- **Inputs:** InsightReport (proposed); unsold inventory from Ad Ops
- **Outputs:** promo schedule; promo scripts
- **Tools:** `ad_server_api`, `sql`
- **Instances:** single
- **KPIs:**
  - follows attributed to cross-promo
  - promo-fatigue complaints
  - unsold inventory used for promos

<a id="community-manager"></a>
### `community-manager`: Community & Listener Mail

> Answer listeners, route their corrections and tips, and keep the community healthy.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | always-on | `audience-growth-strategist` | — |

Sorts email, comments and reviews into corrections (sent to the Corrections Agent as a Correction with reported_by 'listener'), news tips (sent to the Story Desk as tier-4 Signals that must be verified), questions, praise, complaints and abuse. It replies within a set time from approved templates and is plainly honest about being an AI network. Legal threats go straight to the Contracts & IP Clerk and the founders. Monthly it suggests mailbag segments, and a listener's message is read on air only with their consent.

- **Inputs:** inbox; comments; reviews
- **Outputs:** replies; Correction; Signal (listener tips); mailbag ideas
- **Tools:** `email`, `social_api`
- **Instances:** single
- **KPIs:**
  - median reply time (target < 24 h)
  - listener corrections logged within 1 h
  - tips that became stories

<a id="brand-guardian"></a>
### `brand-guardian`: Brand Guardian

> Keep everything the public sees on-brand, honest about AI, and never impersonating anyone.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | per-asset (before release) + monthly audit | `network-director` | — |

Owns the brand book: the Curious & Creative Network name and labels, logos, colors, persona usage rules and disclosure language. It checks outward assets automatically before release (art, social copy, ads, newsletters, press releases) and returns fixes, not just rejections. It blocks anything that imitates a real person or outlet, hides that voices are synthetic, or uses clickbait. Monthly it audits a sample of live assets for drift.

- **Inputs:** art; copy; ads; brand book
- **Outputs:** approve/fix decisions; monthly brand audit
- **Tools:** `canva`
- **Instances:** single
- **KPIs:**
  - off-brand assets live (target 0)
  - average time to fix
  - impersonation or disclosure issues (target 0)

<a id="analytics-insights"></a>
### `analytics-insights`: Analytics & Insights

> Turn listening data into decisions: what to make more of, what to fix, what to stop.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | cron "0 10 * * *" (daily ingest) + weekly InsightReport | `audience-growth-strategist` | — |

Pulls host download analytics, Apple Podcasts and Spotify consumption and follower data, YouTube watch time, and newsletter and social metrics into one store. It analyzes completion by segment (using chapters), which story types and lengths hold listeners, time-of-day patterns per market and where growth comes from. The weekly InsightReport (proposed contract) has three to five findings, each with the data behind it and a recommended action for a named agent. Every number carries its source and as-of date.

- **Inputs:** platform analytics; newsletter and social metrics; Episode metadata
- **Outputs:** InsightReport (proposed); dashboards
- **Tools:** `analytics_api`, `sql`
- **Instances:** single
- **KPIs:**
  - recommendations adopted, and their measured effect
  - data freshness (< 24 h)
  - discrepancies vs platform dashboards

<a id="charts-reviews-monitor"></a>
### `charts-reviews-monitor`: Charts & Reviews Monitor

> Know where our shows rank and what listeners say about them, every day.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Haiku tier | cron "0 13 * * *" (daily) | `analytics-insights` | — |

Tracks Apple Podcasts and Spotify chart positions by category and country, YouTube podcast charts where available, and ratings and reviews across platforms. A Haiku-tier classifier tags review sentiment and topic (voice, accuracy, length, AI concerns) and flags review-bombing. Actionable reviews go to the Community Manager, accuracy complaints to Corrections, and chart wins to the Press & PR agent and the media kits.

- **Inputs:** chart pages and endpoints; platform reviews
- **Outputs:** chart log; review digest
- **Tools:** `web_fetch`
- **Instances:** single
- **KPIs:**
  - shows covered in chart tracking (100%)
  - review response time
  - rating trend per show

<a id="partnerships-scout"></a>
### `partnerships-scout`: Partnerships Scout (local orgs & radio)

> Find local partners who make us more trusted and more heard: libraries, universities, radio, newsrooms and civic groups.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Sonnet tier | weekly | `audience-growth-strategist` | — |

Builds a partner list per market: public libraries, journalism schools and student media, public and community radio stations that could air our briefs, local newsrooms that want audio versions in exchange for attribution, chambers of commerce and civic groups. It researches each one, proposes a specific deal (content swap, syndication, events, co-branded feed) and drafts the outreach. Anything that commits money or signs a contract goes to Joshua or Janel. It tracks the partner pipeline in the CRM.

- **Inputs:** market config; competitor tracker
- **Outputs:** partner pipeline; outreach drafts; partnership proposals
- **Tools:** `web_search`, `email`, `crm`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - active partners per market
  - listeners attributed to partners
  - proposal-to-signed ratio

<a id="press-pr-agent"></a>
### `press-pr-agent`: Press & PR Agent

> Tell the network's story to the press: launches, milestones and the trust record.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Sonnet tier | event:market.launch, event:show.greenlit + weekly | `audience-growth-strategist` | — |

Writes press releases for launches, new markets and transparency milestones, pitches podcast trade press and local media, and keeps a press kit (fact sheet, founder bios, how the trust stack works, logos). It answers media inquiries with approved facts and routes interview requests to the founders. Statements in the company's name are approved by Joshua or Janel before release, because they are company speech, not episodes.

- **Inputs:** milestones; transparency reports; chart wins
- **Outputs:** press releases; pitches; press kit
- **Tools:** `email`, `web_search`
- **Instances:** single
- **KPIs:**
  - earned media mentions per month
  - pitch response rate
  - media inquiries answered within 24 h

<a id="paid-growth-manager"></a>
### `paid-growth-manager`: Paid Growth Manager

> Buy listeners only where it pays back, with hard daily caps.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | always-on while campaigns run (daily review) | `audience-growth-strategist` | — |

Runs paid acquisition once organic channels are measured: podcast-app ads, app-store and search ads, and social ads targeted by market. Every campaign has a daily cap enforced by the Budget Controller and a stop-loss rule: if cost per retained follower goes above target, the campaign stops. It reports cost per acquired and retained listener by channel. Platform ad policies on AI content are checked first (verify, as of Oct 2026).

- **Inputs:** growth plan; paid budget
- **Outputs:** campaigns; acquisition cost report
- **Tools:** `ad_platform_api`, `analytics_api`
- **Instances:** single
- **KPIs:**
  - cost per retained listener vs target
  - payback period
  - campaigns stopped by stop-loss (working as designed)

## Revenue desk

Ad operations, direct local sponsorship, sales collateral, billing, grants and, later, memberships, licensing and the two tool products. Our research suggests programmatic ads alone did not cover Inception Point's overhead *(inference, docs/research/notes/inception-point-business-model.md)*, so direct local sponsors come first. Standards beat sales: no revenue agent can overrule the Standards Editor. *Rates, CPMs and vendor terms: cite the facts sheet; as of Oct 2026, verify before buying.*

14 agents: 0 built, 9 next, 5 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`revenue-director`](#revenue-director) | Revenue Director | next | sonnet | weekly | Own the revenue plan across ads, sponsors, grants, services and, later, the tools. |
| [`ad-ops`](#ad-ops) | Ad Ops (DAI, fill, brand safety) | next | haiku | always-on | Run ad insertion cleanly and safely: the right ads, in the right places, never next to tragedy. |
| [`yield-optimizer`](#yield-optimizer) | Programmatic Yield Optimizer | future | sonnet | weekly | Earn the most from every unsold slot without hurting listening. |
| [`sponsor-prospector`](#sponsor-prospector) | Sponsor Prospector (local businesses) | next | sonnet | weekly per market + event:lead.inbound | Find and book local businesses that want to reach local listeners. |
| [`media-kit-builder`](#media-kit-builder) | Sales Deck & Media Kit Builder | next | sonnet | cron "0 15 2 * *" (monthly refresh) + on-demand | Give every sales conversation a current, honest media kit and deck. |
| [`rate-card-manager`](#rate-card-manager) | Rate Card Manager | next | sonnet | monthly + on-demand | Price inventory and sponsorships so we sell out at a fair price. |
| [`sponsor-read-writer`](#sponsor-read-writer) | Sponsor Read Writer | next | sonnet | per-campaign | Write sponsor reads that work for the sponsor, sound natural, and are clearly ads. |
| [`campaign-reporter`](#campaign-reporter) | Campaign Reporter | next | haiku | weekly during each campaign + at campaign end | Show every sponsor exactly what they got. |
| [`billing-collections`](#billing-collections) | Billing & Collections | next | haiku | per insertion order or SOW + weekly AR run | Invoice correctly, collect on time, and reconcile every payment. |
| [`grants-scout`](#grants-scout) | Grants Scout | next | sonnet | weekly | Find and win grants and funding for local news and media innovation. |
| [`premium-membership-manager`](#premium-membership-manager) | Premium & Membership Manager | future | sonnet | weekly | Offer paid tiers superfans want: ad-free, early access and bonus deep dives. |
| [`content-licensing-agent`](#content-licensing-agent) | Content Licensing Agent | future | sonnet | weekly | Earn from the catalog by licensing shows and briefs to radio, platforms and publishers. |
| [`white-label-onboarding`](#white-label-onboarding) | B2B White-Label Onboarding | future | sonnet | event:client.signed (B2B engine customers) | Onboard B2B customers to the Earlobe Engine so their audio product runs on our workflow under their brand. |
| [`trust-api-concierge`](#trust-api-concierge) | Trust-Stack API Concierge | future | sonnet | always-on (support) + weekly account health | Help developers and newsrooms use the Trust Stack API well, and spot misuse. |

<a id="revenue-director"></a>
### `revenue-director`: Revenue Director

> Own the revenue plan across ads, sponsors, grants, services and, later, the tools.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | weekly | `network-director` | — |

Sets monthly revenue targets by line, reviews the sponsor pipeline, sell-through and fill, services bookings and grant timelines, and writes a weekly revenue memo for the founders. It decides where the revenue agents spend their effort (for example, direct local sponsors before programmatic in small markets). When revenue and standards conflict, it flags the conflict and standards win: the Standards Editor is never overruled by a sale. Price changes and contracts go to the founders.

- **Inputs:** finance ledger; sponsor pipeline; InsightReport (proposed); rate card
- **Outputs:** weekly revenue memo; monthly targets
- **Tools:** `sql`, `crm`
- **Instances:** single
- **KPIs:**
  - revenue vs plan by line
  - revenue per episode
  - pipeline coverage of next quarter's target

<a id="ad-ops"></a>
### `ad-ops`: Ad Ops (DAI, fill, brand safety)

> Run ad insertion cleanly and safely: the right ads, in the right places, never next to tragedy.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Haiku tier | always-on | `revenue-director` | — |

Sets up dynamic ad insertion on the host (pre-, mid- and post-roll at the Sound Designer's segment markers), traffics direct campaigns, connects programmatic marketplaces and monitors fill and delivery. A Haiku-tier classifier tags every episode with brand-safety categories (crime, death, disaster, politics), so advertiser exclusions apply automatically. Network policy: Breaking Desk coverage of deaths and attacks runs ad-free by default. It enforces ad-load limits per format.

- **Inputs:** episodes with ad markers; insertion orders; brand-safety rules
- **Outputs:** ad schedule; delivery and fill reports; brand-safety tags per episode
- **Tools:** `ad_server_api`, `host_api`
- **Instances:** single
- **KPIs:**
  - fill rate per show
  - delivered vs booked impressions
  - brand-safety violations (target 0)

<a id="yield-optimizer"></a>
### `yield-optimizer`: Programmatic Yield Optimizer

> Earn the most from every unsold slot without hurting listening.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | weekly | `revenue-director` | — |

Once inventory is large enough, it tunes the mix of direct, programmatic and house promos, sets price floors per show and market, and tests ad load against completion so revenue never costs us the audience. CPM benchmarks come from the facts sheet, cited by ID. It reports revenue per thousand downloads by show and slot.

- **Inputs:** delivery data; completion data; docs/research/facts-and-figures.md
- **Outputs:** floor and mix changes; yield report
- **Tools:** `ad_server_api`, `analytics_api`
- **Instances:** single
- **KPIs:**
  - revenue per thousand downloads
  - completion change after ad-load tests
  - unsold inventory share

<a id="sponsor-prospector"></a>
### `sponsor-prospector`: Sponsor Prospector (local businesses)

> Find and book local businesses that want to reach local listeners.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | weekly per market + event:lead.inbound | `revenue-director` | — |

Builds sponsor leads per market from new business filings and openings (Records & Filings Watcher), businesses already advertising locally, chamber member lists, and categories that fit each show (restaurants for Open & Shut, home services for Permit Pulse). It scores fit and conflict risk: no sponsor the show is actively covering as a news subject in that market. It drafts personalized outreach that follows anti-spam law, books calls on the founders' calendar, and logs every touch in the CRM.

- **Inputs:** sponsor leads from records; market data; rate card
- **Outputs:** qualified leads; outreach sequences; booked calls
- **Tools:** `web_search`, `email`, `crm`, `calendar`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - qualified leads per week per market
  - lead-to-sponsor conversion
  - sponsor conflicts missed (target 0)

<a id="media-kit-builder"></a>
### `media-kit-builder`: Sales Deck & Media Kit Builder

> Give every sales conversation a current, honest media kit and deck.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | cron "0 15 2 * *" (monthly refresh) + on-demand | `revenue-director` | — |

Builds a media kit per show and per market and a network sales deck: audience size and growth (from our analytics, with as-of dates), formats and placements, sample sponsor reads, the trust story with transparency numbers, and pricing from the rate card. It refreshes monthly and makes custom versions for big prospects. Every number comes from our own logs or the facts sheet; estimates are never presented as data.

- **Inputs:** InsightReport (proposed); rate card; transparency report
- **Outputs:** media kits; sales deck
- **Tools:** `canva`
- **Instances:** single; one kit per show and per market
- **KPIs:**
  - kits refreshed monthly (100%)
  - deck-to-meeting conversion
  - out-of-date numbers in circulated kits (target 0)

<a id="rate-card-manager"></a>
### `rate-card-manager`: Rate Card Manager

> Price inventory and sponsorships so we sell out at a fair price.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | monthly + on-demand | `revenue-director` | — |

Maintains rates per show, market and placement (host-read vs produced, pre/mid/post, show sponsorships, newsletter and bundle packages) from Ad Ops' inventory forecast and the market CPM benchmarks in the facts sheet (cite IDs; as of Oct 2026, verify). It sets discount and make-good rules and adjusts monthly based on sell-through. Price changes above a set threshold go to the founders.

- **Inputs:** inventory forecast; facts sheet; sell-through data
- **Outputs:** rate card; package definitions
- **Tools:** `sql`
- **Instances:** single
- **KPIs:**
  - sell-through rate
  - average effective rate vs card
  - how often discounts are used

<a id="sponsor-read-writer"></a>
### `sponsor-read-writer`: Sponsor Read Writer

> Write sponsor reads that work for the sponsor, sound natural, and are clearly ads.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | per-campaign | `revenue-director` | — |

Writes host-read and produced ads from the sponsor's brief, always labeled as sponsored and placed in clearly separate breaks. News voices stay out of ads: Ava (breaking) and June (courts and crime) never read them, and a dedicated non-news persona voices most reads. Every claim in an ad is screened by the Legal Screener in ad mode for substantiation and disclosure. The sponsor approves the final copy.

- **Inputs:** sponsor brief; insertion order
- **Outputs:** ad scripts; approved reads for Studio Voice
- **Tools:** `email`
- **Instances:** one per campaign
- **KPIs:**
  - sponsor approval on the first draft
  - sponsor renewal rate
  - ad-claim issues (target 0)

<a id="campaign-reporter"></a>
### `campaign-reporter`: Campaign Reporter

> Show every sponsor exactly what they got.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Haiku tier | weekly during each campaign + at campaign end | `revenue-director` | — |

Builds a delivery report per campaign: impressions or downloads delivered, placements, listener actions (promo-code redemptions, tracked link visits) and any shortfall with the make-good owed. Numbers come straight from ad-server and host data. Reports go out on schedule, and campaigns ready to renew are flagged to the Sponsor Prospector.

- **Inputs:** delivery data; promo codes; insertion order terms
- **Outputs:** campaign reports; make-good calculations
- **Tools:** `ad_server_api`, `email`
- **Instances:** one per campaign
- **KPIs:**
  - reports on time (100%)
  - billing disputes caused by reporting errors (target 0)
  - renewals after a report

<a id="billing-collections"></a>
### `billing-collections`: Billing & Collections

> Invoice correctly, collect on time, and reconcile every payment.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Haiku tier | per insertion order or SOW + weekly AR run | `revenue-director` | — |

Creates invoices from signed insertion orders and services SOWs, sends payment links through the payment processor, sends polite reminders on a fixed schedule, and reconciles payments with the Finance Reporter. Disputes and anything past a set age go to the founders. It never changes prices or terms on its own.

- **Inputs:** insertion orders; SOWs; campaign reports
- **Outputs:** invoices; reminders; accounts-receivable aging
- **Tools:** `payments_api`, `email`
- **Instances:** single
- **KPIs:**
  - days sales outstanding
  - invoice errors (target 0)
  - bad debt

<a id="grants-scout"></a>
### `grants-scout`: Grants Scout

> Find and win grants and funding for local news and media innovation.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | weekly | `revenue-director` | — |

Tracks local-news funds, journalism foundations, state and city programs and media-innovation grants, and checks eligibility honestly: some funders may exclude AI-produced news (inference, to confirm per funder). It drafts applications built on the trust record and public-service angles (meeting coverage, missing-person appeals, local courts), tracks deadlines and reporting duties, and the founders review and submit. Award conditions go into the Contracts & IP Clerk's register.

- **Inputs:** funder lists; transparency reports; impact metrics
- **Outputs:** grant pipeline; draft applications
- **Tools:** `web_search`, `email`
- **Instances:** single
- **KPIs:**
  - applications submitted per quarter
  - award rate
  - grant revenue

<a id="premium-membership-manager"></a>
### `premium-membership-manager`: Premium & Membership Manager

> Offer paid tiers superfans want: ad-free, early access and bonus deep dives.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | weekly | `revenue-director` | — |

Designs and runs paid offerings through platform subscription features and private-feed tools (verify terms and fees, as of Oct 2026): ad-free versions, early access to evergreen seasons, members-only deep dives and Case Tracker extras. It runs pricing tests, tracks churn and asks departing members why. Paid content goes through the same trust stack as free content.

- **Inputs:** InsightReport (proposed); platform terms
- **Outputs:** membership offers; churn report
- **Tools:** `host_api`, `payments_api`
- **Instances:** single
- **KPIs:**
  - paying members
  - monthly churn
  - revenue per member

<a id="content-licensing-agent"></a>
### `content-licensing-agent`: Content Licensing Agent

> Earn from the catalog by licensing shows and briefs to radio, platforms and publishers.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | weekly | `revenue-director` | — |

Sells and manages licenses for evergreen series (History of Hollywood, Cold Case Files) and local briefs to radio stations, airlines, in-car and smart-speaker platforms and news sites, using packages from the Syndication Packager. It drafts term sheets from standard templates (territory, term, exclusivity, attribution, AI disclosure kept intact). Contracts are signed by the founders.

- **Inputs:** catalog; partner leads
- **Outputs:** licensing pipeline; term sheets
- **Tools:** `email`, `crm`
- **Instances:** single
- **KPIs:**
  - licensing revenue
  - active licensees
  - catalog share under license

<a id="white-label-onboarding"></a>
### `white-label-onboarding`: B2B White-Label Onboarding

> Onboard B2B customers to the Earlobe Engine so their audio product runs on our workflow under their brand.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | event:client.signed (B2B engine customers) | `revenue-director` | — |

For product 3 (Earlobe Engine): a newspaper, university or company that wants an automated audio product built from its own reporting or content. It configures their workspace (sources, personas, brand, lane policies, cadence), runs a pilot in dry-run, trains their staff and sets service levels. Their content runs through the same trust stack, with their own editors as escalation contacts.

- **Inputs:** signed contract; customer content sources
- **Outputs:** configured workspace; pilot episodes; onboarding report
- **Tools:** `host_api`, `email`
- **Instances:** one onboarding per customer
- **KPIs:**
  - days from contract to first live episode
  - pilot-to-paid conversion
  - customer retention at 12 months

<a id="trust-api-concierge"></a>
### `trust-api-concierge`: Trust-Stack API Concierge

> Help developers and newsrooms use the Trust Stack API well, and spot misuse.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | always-on (support) + weekly account health | `revenue-director` | — |

For product 2 (Trust Stack): onboards API customers to claim extraction, blind verification and the gate as a service. It issues keys and quotas, answers integration questions from the docs, watches usage for errors and for misuse (for example, using verification output to make false content look checked), and reports account health. Pricing and contracts come from the founders.

- **Inputs:** API usage logs; API docs; support requests
- **Outputs:** onboarding; support answers; account health reports
- **Tools:** `email`, `sql`
- **Instances:** single
- **KPIs:**
  - time to first successful API call
  - tickets resolved without escalation
  - API revenue retention

## Business Ops desk

The company around the network: the founders' daily brief, industry and competitor intelligence (Liquid Studios included), vendor prices, books, compliance, privacy, contracts and IP, investor relations, the knowledge base and, later, productizing the tools. *Regulatory and vendor statements: as of Oct 2026, verify before relying on them.*

11 agents: 0 built, 10 next, 1 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`chief-of-staff`](#chief-of-staff) | Chief of Staff | next | sonnet | cron "0 11 * * *" (07:00 ET daily brief; follows DST via the Scheduler) + weekly founder memo (Sunday) | Give Joshua and Janel one short morning brief: what shipped, what was stopped and why, money, and the few decisions only they can make. |
| [`industry-intel`](#industry-intel) | Industry Intel | next | sonnet | always-on (daily scan) + weekly synthesis on the Opus tier | Know what is changing in AI audio, podcasting and local news before it hits us, starting with Liquid Studios. |
| [`competitive-watch`](#competitive-watch) | Competitive Watch | next | sonnet | monthly per market + weekly chart and launch scan | Map every competitor for each market and format, and find the gaps we can own. |
| [`vendor-pricing-watch`](#vendor-pricing-watch) | Vendor & Pricing Watch | next | haiku | weekly + event:vendor.change | Catch every price, quota or terms change from our vendors before it hits the budget or breaks a workflow. |
| [`finance-reporter`](#finance-reporter) | Finance / Bookkeeping Reporter | next | sonnet | cron "0 12 * * *" (daily cost rollup) + monthly close (by business day 5) | Know what every show, market and product costs and earns, every day, in numbers an accountant can trust. |
| [`compliance-policy-watch`](#compliance-policy-watch) | Compliance & Platform Policy Watch | next | sonnet | weekly + event:policy.change + on-demand clearances | Keep every show, source and tool inside platform rules and the law, and clear new ones before we use them. |
| [`privacy-steward`](#privacy-steward) | Privacy Steward | next | haiku | weekly + event:privacy.request | Collect as little personal data as we can, protect what we keep, and honor every privacy request on time. |
| [`contracts-ip-clerk`](#contracts-ip-clerk) | Contracts & IP Clerk | next | sonnet | on-demand + event:legal.threat + monthly register review | Keep the company's names, contracts, insurance and legal notices in order, and get real legal threats to a human within the hour. |
| [`partner-investor-relations`](#partner-investor-relations) | Partner / Investor Relations | next | opus | 72 h before each partner or investor meeting (calendar-triggered) + monthly investor update | Walk the founders into every important meeting fully prepared, and keep partners and investors informed. |
| [`knowledge-base-keeper`](#knowledge-base-keeper) | Knowledge Base Keeper | next | sonnet | weekly + per change (docs lint in CI) | Keep the docs, the agent files and the code telling the same story. |
| [`product-strategist`](#product-strategist) | Tools Productization Strategist | future | opus | monthly | Decide when and how the Trust Stack and the Earlobe Engine become products other people pay for. |

<a id="chief-of-staff"></a>
### `chief-of-staff`: Chief of Staff

> Give Joshua and Janel one short morning brief: what shipped, what was stopped and why, money, and the few decisions only they can make.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Sonnet tier | cron "0 11 * * *" (07:00 ET daily brief; follows DST via the Scheduler) + weekly founder memo (Sunday) | founders (Joshua German, Janel Moore) | — |

This is the founders' single window into a network that runs without them. The daily brief has five blocks: published (by show), stopped (KILLs, HOLDs, skipped slots, with the reason in one line), trust (corrections opened and applied), money (spend vs cap, revenue booked, cash) and decisions needed. Each decision is one yes/no line with a default and a deadline (budget increases, new markets, contracts, company statements, legal threats). It reads today's calendar and attaches meeting prep from Partner / Investor Relations, and it tracks the founder to-do list until each item closes. It never decides for the founders; when a decision passes its deadline it applies the documented default and says so.

- **Inputs:** Run Auditor digest; Incident Commander status lines; programming and revenue memos; finance ledger; calendar; founder to-do list
- **Outputs:** daily founder brief; weekly founder memo; decision log
- **Tools:** `email`, `calendar`, `sql`, `docs`
- **Instances:** single
- **KPIs:**
  - brief delivered by 07:00 ET every day (100%)
  - decisions answered before their deadline
  - founder minutes per day spent on network operations (trend down)
  - surprises: issues the founders heard about elsewhere first (target 0)

<a id="industry-intel"></a>
### `industry-intel`: Industry Intel

> Know what is changing in AI audio, podcasting and local news before it hits us, starting with Liquid Studios.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Sonnet tier | always-on (daily scan) + weekly synthesis on the Opus tier | `chief-of-staff` | — |

Watches the businesses and platforms that shape the network. AI audio networks come first: Liquid Studios, the former Inception Point AI and Quiet Please led by Jeanine Wright, whose rise and retreat is documented in docs/research/notes/inception-point-business-model.md. It also tracks podcast platform policy and product changes (Apple, Spotify, YouTube, Amazon, Podcast Index, Castro), the podcast ad market, voice and model vendors, local-news closures that open a market, and media ownership changes. The daily scan is a Sonnet-tier digest; each week an Opus-tier synthesis writes 'what changed and what it means for us', with facts and inferences labeled separately (Convention 3). New numbers go into the facts sheet with source and as-of date before anyone cites them, and ownership changes go to the Source Ledger Keeper.

- **Inputs:** trade press and newsletters; platform blogs and changelogs; company filings and websites; docs/research/notes/
- **Outputs:** daily intel digest; weekly synthesis memo; facts sheet entries (with F-IDs); event:ownership.change
- **Tools:** `web_search`, `web_fetch`, `rss`, `docs`
- **Instances:** single
- **KPIs:**
  - material industry changes flagged within 48 h
  - facts sheet entries with source and as-of date (100%)
  - intel items that led to a decision or config change per month
  - inferences mislabeled as facts (target 0)

<a id="competitive-watch"></a>
### `competitive-watch`: Competitive Watch

> Map every competitor for each market and format, and find the gaps we can own.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N5) | Sonnet tier | monthly per market + weekly chart and launch scan | `industry-intel` | — |

Keeps a competitor tracker per market and per format: local news podcasts, radio and TV station podcasts, newsletters, public-media shows, true-crime and court podcasts, and AI-generated feeds. In Columbia that includes the AI-made 'South Carolina News and Info Tracker' feed noted in our research. For each competitor it records cadence, length, format, hosts (human or AI), ad load, chart position, ratings and last-episode date. Monthly it writes a white-space note for the Programming Director: formats nobody serves, shows that went dormant, and audiences left behind by newsroom cuts. It describes competitors factually and never copies their content or branding.

- **Inputs:** podcast directories and charts; competitor feeds (metadata only); Charts & Reviews Monitor data; Industry Intel digest
- **Outputs:** competitor tracker; monthly white-space note
- **Tools:** `web_search`, `web_fetch`, `rss`
- **Instances:** one per market: columbia-sc, los-angeles (wave 0, live); new-york, chicago (wave 1, configured, enabled: false); next 20: charleston-sc, greenville-sc, charlotte, atlanta, houston, washington-dc, philadelphia, phoenix, dallas-fort-worth, miami, bay-area, seattle, denver, austin, boston, detroit, new-orleans, nashville, las-vegas, twin-cities
- **KPIs:**
  - markets with a tracker updated in the last 30 days (100%)
  - white-space notes that became greenlit shows
  - competitor launches spotted within 7 days

<a id="vendor-pricing-watch"></a>
### `vendor-pricing-watch`: Vendor & Pricing Watch

> Catch every price, quota or terms change from our vendors before it hits the budget or breaks a workflow.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Haiku tier | weekly + event:vendor.change | `finance-reporter` | — |

Watches pricing pages, changelogs and terms for every vendor in the stack: the Anthropic API (by tier), ElevenLabs text-to-speech and speech-to-text, the podcast host, CourtListener, search and data APIs, the email and newsletter platform, social APIs, design tools and the payment processor. When something changes it updates the facts sheet entry (new value, source, as-of date), tells the Budget Controller and Quota Sentinel, and re-estimates cost per episode with the Finance Reporter. It keeps a tested backup for each critical vendor (a second TTS engine, a second host) so the Incident Commander has a failover plan. Every statement it writes carries 'as of <date>, verify before buying' (Convention 2).

- **Inputs:** vendor pricing pages and changelogs; vendor terms of service; AgentRun cost data
- **Outputs:** vendor change alerts; facts sheet updates; backup-vendor register; event:vendor.change
- **Tools:** `web_fetch`, `web_search`, `sql`
- **Instances:** single
- **KPIs:**
  - vendor changes detected within 7 days
  - facts sheet price entries older than 90 days (target 0)
  - critical vendors with a tested backup (100%)

<a id="finance-reporter"></a>
### `finance-reporter`: Finance / Bookkeeping Reporter

> Know what every show, market and product costs and earns, every day, in numbers an accountant can trust.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | cron "0 12 * * *" (daily cost rollup) + monthly close (by business day 5) | `chief-of-staff` | — |

Rolls up AgentRun usd_estimate by show, desk and agent each day and reconciles the estimates against vendor invoices at month end, so the cost model in finance/ stays honest. It records revenue from invoices and payments (Billing & Collections), ad delivery and services, and keeps the finance ledger that the revenue, programming and founder memos read. Monthly it produces the close pack: P&L by product line (Network, Trust Stack, Earlobe Engine, Studio Services), unit economics per show (cost per episode, cost per listener, revenue per episode) and cash runway. It prepares, but does not file, tax and compliance items for the LLC's accountant, and flags anything that needs a professional.

- **Inputs:** AgentRun; vendor invoices; payments and invoices; ad delivery reports; config/budgets.yaml
- **Outputs:** finance ledger; daily cost rollup; monthly close pack; unit economics per show
- **Tools:** `sql`, `accounting_api`, `payments_api`
- **Instances:** single
- **KPIs:**
  - estimated vs invoiced cost variance (target within 10%)
  - monthly close by business day 5
  - shows with a current unit-economics line (100%)
  - reconciliation breaks left open past 30 days (target 0)

<a id="compliance-policy-watch"></a>
### `compliance-policy-watch`: Compliance & Platform Policy Watch

> Keep every show, source and tool inside platform rules and the law, and clear new ones before we use them.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Sonnet tier | weekly + event:policy.change + on-demand clearances | `chief-of-staff` | — |

Tracks the rules that apply to a fully automated AI network: platform policies on AI content and disclosure (Apple, Spotify, YouTube, Amazon), the FTC's endorsement and advertising rules, state laws on AI disclosure and synthetic media (with extra care in election season), and vendor terms (ElevenLabs, NotebookLM, Meta Muse). It runs a clearance register: a court portal, social platform, data source, music library or UI engine is used only after it records that the terms allow our use. When a policy changes, it writes an impact note, updates the disclosure wording through the Disclosure Agent, and proposes standards or gate changes to the Standards Editor. It is not a lawyer; anything with legal exposure goes to the Contracts & IP Clerk and the founders.

- **Inputs:** platform policy pages; regulator announcements; vendor terms; clearance requests from other agents
- **Outputs:** clearance register; policy impact notes; disclosure wording updates; event:policy.change
- **Tools:** `web_search`, `web_fetch`, `docs`
- **Instances:** single
- **KPIs:**
  - sources and tools in use without a clearance record (target 0)
  - policy changes turned into an impact note within 7 days
  - platform strikes, removals or demonetizations (target 0)

<a id="privacy-steward"></a>
### `privacy-steward`: Privacy Steward

> Collect as little personal data as we can, protect what we keep, and honor every privacy request on time.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N3) | Haiku tier | weekly + event:privacy.request | `compliance-policy-watch` | — |

Covers listener data (newsletter lists, emails, tips, analytics) and the personal data that flows through the newsroom (names in court records, tipster identities). It keeps the privacy policy and data map current, sets retention periods (raw Signals and fetched pages expire; tipster contact details are separated and minimized), and makes sure email has consent and a working unsubscribe. It handles access and deletion requests within legal deadlines; the LA market brings California privacy law into scope (verify thresholds, as of Oct 2026). Requests to remove people from published journalism are not privacy requests; those go to the Contracts & IP Clerk and the Standards Editor.

- **Inputs:** data map; privacy requests; newsletter and CRM systems; store retention settings
- **Outputs:** privacy policy updates; retention jobs; request log
- **Tools:** `sql`, `email`, `docs`
- **Instances:** single
- **KPIs:**
  - privacy requests closed within the legal deadline (100%)
  - data held past its retention period (target 0)
  - tipster identities exposed (target 0)

<a id="contracts-ip-clerk"></a>
### `contracts-ip-clerk`: Contracts & IP Clerk

> Keep the company's names, contracts, insurance and legal notices in order, and get real legal threats to a human within the hour.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Sonnet tier | on-demand + event:legal.threat + monthly register review | founders (Joshua German, Janel Moore) | — |

Runs trademark clearance on every show and persona name before launch (USPTO search plus a common-law web search), with a risk note for counsel on anything close. It keeps contract templates (insertion order, services SOW, partnership MOU, licensing term sheet) and a register of every signed contract with renewal dates and obligations, including grant conditions. It tracks media liability and errors-and-omissions insurance, an essential cover for a network that publishes without a human gate. Legal threats, subpoenas and takedown demands are logged, the evidence is preserved, and the matter goes to the founders and outside counsel within one hour. The clerk never answers them on the merits.

- **Inputs:** show and persona names; contract requests; legal notices and demands; Community Manager escalations
- **Outputs:** name clearance notes; contract drafts from templates; contract and insurance register; event:legal.threat
- **Tools:** `web_search`, `email`, `docs`
- **Instances:** single
- **KPIs:**
  - shows launched without name clearance (target 0)
  - legal threats escalated within 1 h (100%)
  - contracts with renewal dates tracked (100%)
  - insurance lapses (target 0)

<a id="partner-investor-relations"></a>
### `partner-investor-relations`: Partner / Investor Relations

> Walk the founders into every important meeting fully prepared, and keep partners and investors informed.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N1) | Opus tier | 72 h before each partner or investor meeting (calendar-triggered) + monthly investor update | `chief-of-staff` | — |

For each meeting on the founders' calendar it builds a prep dossier: who they are, what they have said publicly, what they want, our asks, likely questions and landmines, with facts and inferences labeled. The model case is the Jeanine Wright / Liquid Studios meeting prep, which draws on Industry Intel's research and is careful to separate what is reported from what we infer. After meetings it drafts follow-ups and logs commitments, and it writes a monthly investor and partner update from the finance ledger and transparency report. It keeps the data room current. Every number in it comes from the facts sheet or our own logs.

- **Inputs:** calendar; Industry Intel research; finance ledger; transparency report; CRM notes
- **Outputs:** meeting prep dossiers; follow-up drafts; monthly investor/partner update; data room
- **Tools:** `calendar`, `web_search`, `email`, `docs`
- **Instances:** single; one dossier per meeting
- **KPIs:**
  - dossiers delivered at least 48 h before the meeting (100%)
  - follow-ups sent within 24 h
  - monthly update on time
  - errors found in dossiers after the meeting (target 0)

<a id="knowledge-base-keeper"></a>
### `knowledge-base-keeper`: Knowledge Base Keeper

> Keep the docs, the agent files and the code telling the same story.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N2) | Sonnet tier | weekly + per change (docs lint in CI) | `chief-of-staff` | — |

Checks that this catalog, the agent files in agents/<desk>/<id>.md, the module map in earlobe/README.md and the code agree on ids, statuses and module paths. For example, it would catch that earlobe/sensors/press.py exists but is missing from the module map. It checks that schemas.py and json-contracts.md change together (Convention 8), and it lints the docs for numbers without facts-sheet IDs, missing as-of lines and model version strings (Conventions 1, 2 and 4). It files postmortems and decisions where people will find them, and opens fixes through the Release Guard.

- **Inputs:** docs/; agents/; earlobe/README.md; earlobe/schemas.py; postmortems and decision logs
- **Outputs:** docs drift report; lint results; fix change requests
- **Tools:** `ci`, `docs`
- **Instances:** single
- **KPIs:**
  - catalog vs agent files vs code mismatches (target 0)
  - convention lint violations on main (target 0)
  - drift items closed within 7 days

<a id="product-strategist"></a>
### `product-strategist`: Tools Productization Strategist

> Decide when and how the Trust Stack and the Earlobe Engine become products other people pay for.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Opus tier | monthly | founders (Joshua German, Janel Moore) | — |

The plan is to dominate as a network first and sell the tools later; this agent says when 'later' has arrived. It scores each internal capability for product readiness: a stable interface, a proven track record from the transparency reports, cost per call, and support load. It drafts packaging and pricing hypotheses (cited from the facts sheet), a pilot customer list, and the positioning against B2B players such as Liquid Studios, which turned to 'content transformation infrastructure' for publishers. It hands signed pilots to B2B White-Label Onboarding and the Trust-Stack API Concierge.

- **Inputs:** transparency reports; finance ledger; Industry Intel synthesis; inbound B2B interest
- **Outputs:** product readiness scorecard; packaging and pricing hypotheses; pilot plan
- **Tools:** `web_search`, `sql`, `docs`
- **Instances:** single
- **KPIs:**
  - pilots launched
  - pilot-to-paid conversion
  - product revenue share of total

## Services desk

C&C Studio Services (product 4) is the in-person business: setting up podcasts and distribution for businesses and people, with Joshua and Janel on site in Columbia and LA, then remotely. These agents handle everything around the founders' time: intake, proposals, show kits, platform submissions, post-production, coaching, reporting and field logistics. *Platform submission flows: as of Oct 2026, verify.*

7 agents: 0 built, 3 next, 4 future.

| id | name | status | tier | runs | mission |
|---|---|---|---|---|---|
| [`services-intake`](#services-intake) | Studio Services Intake | next | sonnet | event:lead.services + daily pipeline review | Turn every inquiry about C&C Studio Services into a qualified lead, a clear proposal and a booked call. |
| [`client-show-setup`](#client-show-setup) | Client Show Setup | next | sonnet | event:client.signed | Take a signed client from idea to a launch-ready show kit, so the founders' on-site day goes smoothly. |
| [`distribution-setup`](#distribution-setup) | Distribution Setup | next | sonnet | per client launch | Get each client's show live on Apple Podcasts, Spotify, YouTube and the other major apps, correctly the first time. |
| [`client-post-production`](#client-post-production) | Client Post-Production | future | sonnet | per client episode (on upload) | Turn a client's raw recording into a finished, published episode with notes, transcript and clips. |
| [`client-coaching`](#client-coaching) | Client Coaching / Training | future | sonnet | per session + per client episode (feedback) | Make clients better podcasters: delivery, structure, interviewing and consistency. |
| [`client-reporting`](#client-reporting) | Client Reporting | future | haiku | cron "0 14 3 * *" (monthly, on the 3rd) | Show each client every month how their show is doing and what to do next. |
| [`field-ops-coordinator`](#field-ops-coordinator) | Field Ops Coordinator | future | haiku | per on-site booking + weekly gear check | Make every in-person studio day run on time with the right gear, in the right place. |

<a id="services-intake"></a>
### `services-intake`: Studio Services Intake

> Turn every inquiry about C&C Studio Services into a qualified lead, a clear proposal and a booked call.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | event:lead.services + daily pipeline review | founders (Joshua German, Janel Moore) | — |

The front door and account owner for product 4, where Curious & Creative sets up podcasts and distribution for businesses and people, in person and remotely. It qualifies each inquiry (goal, audience, budget, timeline, location, whether the client wants to host or wants AI voices), proposes a package (Setup, Launch, Monthly Production, Coaching), and drafts the proposal and SOW from the Contracts & IP Clerk's templates. It books the discovery call on the founders' calendar and logs every touch in the CRM. It runs a conflict check: a client who is a current news subject in our markets is flagged, and buying services never buys coverage.

- **Inputs:** inquiry forms and email; CRM; package and pricing sheet; founders' calendar
- **Outputs:** qualified lead; proposal; SOW draft; booked discovery call; event:client.signed
- **Tools:** `email`, `crm`, `calendar`, `docs`
- **Instances:** single; Columbia and LA first (where the founders can be on site), then remote everywhere
- **KPIs:**
  - inquiry to booked call within 48 h
  - proposal acceptance rate
  - conflicts missed (target 0)
  - services revenue booked per month

<a id="client-show-setup"></a>
### `client-show-setup`: Client Show Setup

> Take a signed client from idea to a launch-ready show kit, so the founders' on-site day goes smoothly.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | event:client.signed | `services-intake` | — |

Builds the client's show package from our Show Launcher templates, under the client's brand and ownership: concept and format doc, episode template, name clearance (Contracts & IP Clerk), cover art (Art Director templates, client brand), and a sound package with licensed music (Sonic Brand Librarian). For in-person work it prepares the gear list, room-treatment notes and a recording-day checklist for Joshua or Janel, sized to the client's budget. It writes the client's workflow guide: record, upload, publish, and who does what. Every account and asset is created in the client's name; we never hold their show hostage.

- **Inputs:** signed SOW; intake notes; show templates; client brand assets
- **Outputs:** client show kit (concept, format, art, sound, templates); gear list and recording-day checklist; workflow guide
- **Tools:** `canva`, `docs`, `email`
- **Instances:** one job per client
- **KPIs:**
  - days from signed SOW to launch-ready kit (target <= 10)
  - client revisions per kit
  - client satisfaction at launch

<a id="distribution-setup"></a>
### `distribution-setup`: Distribution Setup

> Get each client's show live on Apple Podcasts, Spotify, YouTube and the other major apps, correctly the first time.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **next** (N4) | Sonnet tier | per client launch | `client-show-setup` | — |

Sets up hosting in the client's own account, validates the RSS feed and artwork, and submits the show to Apple Podcasts, Spotify, YouTube, Amazon Music, iHeart and the Podcast Index (verify current submission flows, as of Oct 2026). Where a platform needs a one-time owner action, it walks the client through it, or uses the Studio Operator with the client's delegated access. It confirms each listing is live (reusing the Directory Sync Checker), connects analytics access, applies AI-content disclosure where the client uses synthetic voices, and hands over a credentials and settings document. Credentials live in the client's password manager or a vault, never in email, chat or the repo.

- **Inputs:** client show kit; client account access (delegated); platform submission requirements
- **Outputs:** live listings per platform; analytics access; handover document
- **Tools:** `host_api`, `computer_use`, `web_fetch`, `email`
- **Instances:** one job per client
- **KPIs:**
  - platforms live within 7 days of launch (100%)
  - submissions accepted on the first try (target >= 95%)
  - credential-handling incidents (target 0)

<a id="client-post-production"></a>
### `client-post-production`: Client Post-Production

> Turn a client's raw recording into a finished, published episode with notes, transcript and clips.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | per client episode (on upload) | `client-show-setup` | — |

For clients on the Monthly Production package: it cleans the audio (noise, levels, loudness to the -16 LUFS target with the same ffmpeg chain as our studio), proposes edits such as long pauses, false starts and filler for the client to approve, and drafts show notes, a transcript and clips by reusing our Copywriter, Transcript & Accessibility and Clip Maker playbooks. Unlike our network, the client is the approver: nothing publishes until they say yes. Factual claims in client shows are the client's responsibility, but it flags obvious legal risks such as an unsubstantiated health claim or a named private person accused of a crime.

- **Inputs:** client raw audio; client show kit; client approval
- **Outputs:** finished episode audio; show notes; transcript; clips; risk flags for the client
- **Tools:** `ffmpeg`, `stt`, `host_api`, `email`
- **Instances:** one job per client episode
- **KPIs:**
  - turnaround from upload to approval-ready (target < 48 h)
  - client revision rounds per episode
  - episodes published on the client's schedule

<a id="client-coaching"></a>
### `client-coaching`: Client Coaching / Training

> Make clients better podcasters: delivery, structure, interviewing and consistency.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Sonnet tier | per session + per client episode (feedback) | founders (Joshua German, Janel Moore) | — |

Builds a training plan for each client from intake goals and their first recordings. After each episode it gives specific, kind feedback from the transcript and audio: speaking pace, filler words, structure, how quickly the hook lands, interview follow-ups, and levels. It keeps a lesson library (mic technique, interview prep, storytelling, show notes that convert) and schedules live sessions with Joshua or Janel, who draws on journalism-school craft for interviewing and storytelling. It tracks progress against the client's own baseline, not against other clients.

- **Inputs:** client recordings and transcripts; intake goals; lesson library
- **Outputs:** training plan; per-episode feedback notes; session agendas
- **Tools:** `stt`, `ffmpeg`, `calendar`, `docs`
- **Instances:** one plan per coaching client
- **KPIs:**
  - client delivery scores vs their baseline after 4 episodes
  - coaching sessions completed as scheduled
  - coaching renewals

<a id="client-reporting"></a>
### `client-reporting`: Client Reporting

> Show each client every month how their show is doing and what to do next.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Haiku tier | cron "0 14 3 * *" (monthly, on the 3rd) | `services-intake` | — |

Pulls each client's host and platform analytics (with their delegated access) into a one-page monthly report: downloads and listeners, platform mix, follower growth, top episodes, completion where available, and three recommendations. It compares results with the goals set at intake and flags clients at renewal risk, or ready for an upsell, to Studio Services Intake. Every number shows its source and date range.

- **Inputs:** client analytics (delegated access); intake goals; SOW terms
- **Outputs:** monthly client report; renewal and upsell flags
- **Tools:** `analytics_api`, `email`, `docs`
- **Instances:** one report per client per month
- **KPIs:**
  - reports delivered on the 3rd (100%)
  - client renewal rate
  - upsells from report recommendations

<a id="field-ops-coordinator"></a>
### `field-ops-coordinator`: Field Ops Coordinator

> Make every in-person studio day run on time with the right gear, in the right place.

| Status | Tier | Runs | Reports to | Code |
|---|---|---|---|---|
| **future** | Haiku tier | per on-site booking + weekly gear check | `services-intake` | — |

Handles the logistics of the in-person side of Studio Services: confirms on-site dates and addresses, plans travel time between Columbia and LA bookings, and builds the day's run sheet. It keeps the equipment inventory (microphones, interfaces, stands, cables, acoustic treatment), checks out gear per booking, orders client purchases from the gear list, and tracks returns and repairs. It sends the client a pre-visit checklist (room choice, noise sources, power, Wi-Fi).

- **Inputs:** booked on-site sessions; gear lists; equipment inventory
- **Outputs:** run sheet per visit; gear checkout log; client pre-visit checklist; purchase list
- **Tools:** `calendar`, `email`, `docs`
- **Instances:** single; Columbia and LA first (where the founders can be on site), then remote everywhere
- **KPIs:**
  - on-site sessions that started on time with complete gear (target 100%)
  - lost or damaged gear per quarter
  - client pre-visit checklists completed

## Expansion roster

*Market and platform statements below: as of Oct 2026, verify. Population, DMA rank and audience figures are left out on purpose. Per Convention 1, they go into `docs/research/facts-and-figures.md` with a source and an F-ID before anyone uses them to rank markets.*

### A. The next 20 markets

Live today: **Columbia, SC** and **Los Angeles** (wave 0), plus the national desk. Configured: **New York City** and **Chicago** (wave 1). Each new market gets a Beat Agent, its sensor set (Court Watch, Press-Release, Public Meetings, Records & Filings, Weather & Hazard, Elections, Social Signal) and a Localizer. It launches with a daily brief and grows courts, history and niche feeds from templates. The Show Launcher and the Market Launch Marketer run the launch.

How we picked them *(inference)*: **wave 2** builds a Southeast cluster around Columbia, so statehouse, court and ownership work is reused, and adds Houston for Spanish. **Wave 3** adds large markets that strengthen national beats (DC, the federal courts) or fit the niche templates. **Wave 4** adds tech, transit and state-capital markets. **Wave 5** adds culture and music-history cities where the archive series are strongest.

| # | Market id | Market | Wave | Why this market | Federal court (CourtListener id, verify) | Local courts / statehouse | Signature shows at launch |
|---|---|---|---|---|---|---|---|
| 1 | `charleston-sc` | Charleston, SC | 2 | Second South Carolina market. It reuses Columbia's statehouse beat, SC court conventions and SC owner-group map, so it is cheap to add. Deep colonial, Civil War and Gullah Geechee history feeds Hometown History. It is exposed to hurricanes. | `dsc` | Charleston County courts (SC Judicial Branch public index); SC statehouse shared with Columbia | Charleston Daily; Hometown History: Charleston; Hurricane Desk |
| 2 | `greenville-sc` | Greenville-Spartanburg, SC | 2 | Completes the South Carolina triangle (Midlands, Lowcountry, Upstate) for a statewide SC network. It is a fast-growing metro with thinner local audio news *(inference; Competitive Watch to confirm)*. | `dsc` | Greenville and Spartanburg County courts; SC statehouse shared | Upstate Daily; Main Street Ledger: Upstate |
| 3 | `charlotte` | Charlotte, NC | 2 | Anchors a Carolinas cluster with Columbia, with a banking and business beat. It adds the North Carolina statehouse and courts *(NC court portal terms to be cleared)*. | `ncwd` | Mecklenburg County courts (NC eCourts); NC General Assembly | Charlotte Daily; Charlotte Courts; Permit Pulse: Charlotte |
| 4 | `atlanta` | Atlanta | 2 | The Southeast media hub, a short drive from the Carolinas cluster. Fulton County cases draw national attention, which is Case Tracker material. Its film and TV industry pairs with the LA entertainment-business beat. It is a state capital. | `gand` | Fulton County Superior Court; Georgia General Assembly | Atlanta Daily; Atlanta Courts; State House Daily: Georgia |
| 5 | `houston` | Houston | 2 | A large Spanish-speaking audience makes it the second Spanish edition after LA *(inference; add Census figures to the facts sheet before citing)*. Harris County courts are very busy. NASA's Johnson Space Center feeds The Breaking Desk: Space. Hurricane coverage. | `txsd` | Harris County District Clerk / courts | Houston Daily; Houston Diario; Hurricane Desk |
| 6 | `washington-dc` | Washington, DC | 3 | The federal government and the Supreme Court are The Breaking Desk's core beats, so a DC Beat agent strengthens national coverage as well as serving a local daily. | `dcd (+ cadc)` | DC Superior Court; Congress and federal agencies | DC Daily; Supreme Court Week; Federal Docket Weekly |
| 7 | `philadelphia` | Philadelphia | 3 | A big market with a strong civic-news culture and founding-era history for Hometown History. The Philadelphia court system is active. | `paed` | Philadelphia Court of Common Pleas; Pennsylvania General Assembly (Harrisburg) | Philly Daily; Hometown History: Philadelphia; Philly Courts |
| 8 | `phoenix` | Phoenix | 3 | Fast growth, Maricopa County courts, heat and air quality (a natural Pollen & Air / Weather Ready market), and a Spanish-language audience. It is a state capital. | `azd` | Maricopa County Superior Court; Arizona Legislature | Phoenix Daily; Phoenix Diario; Weather Ready: Phoenix |
| 9 | `dallas-fort-worth` | Dallas-Fort Worth | 3 | Two cities in one market. Several major-league franchises make it a strong first city for The Breaking Desk: Sports, and it has a big business beat. | `txnd` | Dallas and Tarrant County courts | DFW Daily; The Breaking Desk: Sports; Main Street Ledger: DFW |
| 10 | `miami` | Miami | 3 | A Spanish-language market with real estate and development as signature niches. Hurricanes. Federal court in South Florida handles high-profile cases. | `flsd` | Miami-Dade Clerk of Courts | Miami Daily; Miami Diario; Real Estate Pulse: Miami |
| 11 | `bay-area` | San Francisco Bay Area | 4 | Same state as LA, so it reuses California statehouse coverage, privacy rules and court conventions. Tech business and transit (BART, Muni) beats. | `cand` | San Francisco and Alameda County Superior Courts; California Legislature (shared with LA) | Bay Area Daily; Transit Minute: Bay Area |
| 12 | `seattle` | Seattle | 4 | Tech business, transit and weather beats, with active King County courts and a strong public-records culture *(inference)*. | `wawd` | King County Superior Court | Seattle Daily; Transit Minute: Seattle |
| 13 | `denver` | Denver | 4 | A state capital (the statehouse is a local beat, as in Columbia), with growth, outdoors and weather beats. | `cod` | Denver District Court; Colorado General Assembly | Denver Daily; State House Daily: Colorado; Weather Ready: Front Range |
| 14 | `austin` | Austin | 4 | The Texas capital (legislature beat) with tech growth. Its live-music identity suits a music-history series. | `txwd` | Travis County courts; Texas Legislature | Austin Daily; State House Daily: Texas; Music history: Austin |
| 15 | `boston` | Boston | 4 | Education, health and biotech beats, deep history, active courts, sports. A state capital. | `mad` | Suffolk County courts; Massachusetts General Court | Boston Daily; Hometown History: Boston |
| 16 | `detroit` | Detroit | 5 | Cuts to local news point to unmet audience need *(inference; verify)*. The Motown and Detroit music history archive series. Auto industry business beat. | `mied` | Wayne County Third Circuit Court | Detroit Daily; Motor City Sound (music history) |
| 17 | `new-orleans` | New Orleans | 5 | Music and culture history (the birthplace of jazz), strong true-crime interest, hurricanes, Orleans Parish courts. | `laed` | Orleans Parish courts | New Orleans Daily; Birth of Jazz (music history); Hurricane Desk |
| 18 | `nashville` | Nashville | 5 | Music City history series, music-business beat, growth, and a state capital. | `tnmd` | Davidson County courts; Tennessee General Assembly | Nashville Daily; Music City Stories |
| 19 | `las-vegas` | Las Vegas | 5 | Entertainment business, fast growth, new major-league sports franchises, active Clark County courts. | `nvd` | Clark County (Eighth Judicial District) courts | Las Vegas Daily; Vegas in Court |
| 20 | `twin-cities` | Minneapolis-St. Paul | 5 | A strong civic and public-records culture *(inference)*, weather extremes, and the Minnesota statehouse in St. Paul. | `mnd` | Hennepin and Ramsey County courts; Minnesota Legislature | Twin Cities Daily; Weather Ready: Twin Cities |

### B. Show lanes and always-on feeds

**63 concrete show and feed ideas** across six layers. Each idea names the agents it depends on, so the build order above shows when it becomes possible. Formats marked *(proposed)* (`niche_minute`, `meeting_watch`, `data_minute`, `scoreboard`) are new templates for the Showrunner: Niche Feeds.

**Rules for every niche feed.** These come from the Quiet Please collapse, enforced by the Catalog & Platform Standing Steward:

- **No news, no episode.** A feed with nothing that qualifies publishes nothing that day. No filler.
- **One show per idea.** No launching title variants of the same show to game directory search.
- **Honest, descriptive titles** with the place and subject, no keyword stuffing.
- **AI disclosure** in the show description, in every item's metadata and at the end of every episode.
- **Same Trust Stack, same lanes.** A 90-second pollen report is gated like a daily brief.
- **Audience floor.** A feed under its floor for 30 days is paused or merged, not left to pile up dormant episodes.

#### Local (template per market) (10)

| Show / feed | Cadence | Format | Lane | Key agents | Status |
|---|---|---|---|---|---|
| {City} Daily: Columbia Daily and LA Daily are live; NYC and Chicago are configured | weekdays 06:00 local, 6-8 min | daily_brief | standard | beat-agent, story-desk, producer, showrunner-daily | live / wave 1 |
| {City} Weekend: Saturday look-ahead (events, openings, weather, games) | Sat 07:00 local, 8-10 min | daily_brief (weekend variant) | standard | beat-agent, records-filings-watcher, sports-watcher | next |
| {City} Week in Review: Sunday recap with the week's follow-ups | Sun 08:00 local, 15 min | daily_brief (review variant) | standard | follow-up-editor, showrunner-daily | next |
| State House Daily: South Carolina first (Columbia is the capital), then CA, GA, TX | daily in session | daily_brief | standard (strict for election items) | legislature-watcher | next |
| City Council Watch: one feed per governing body, out within hours of each meeting, plus a Friday preview | per meeting | meeting_watch (proposed) | standard | public-meetings-watcher, follow-up-editor | next |
| School Board Watch: Richland One and Two, LAUSD, and so on | per meeting | meeting_watch (proposed) | standard (minors rule) | public-meetings-watcher, legal-screener | next |
| Election Night {City}: official tallies only, no projections | event (election nights) | breaking_flash | strict | elections-watcher | next (only if eval-tested) |
| {City} Diario: Spanish daily, LA first, then Houston, Miami, Phoenix | weekdays 06:30 local | daily_brief (es) | standard | spanish-editions-editor, voice-director | next |
| Neighborhood Notes: one neighborhood per week, from records, meetings and history | weekly | evergreen_story (short) | standard | records-filings-watcher, archive-miner | future |
| Campus Beat: UofSC, UCLA, USC, then each market's universities | weekly in term | daily_brief (campus variant) | standard | press-release-watcher | future |

#### Breaking Desk spin-offs (8)

| Show / feed | Cadence | Format | Lane | Key agents | Status |
|---|---|---|---|---|---|
| The Breaking Desk (main feed) | event: desk.breaking, 30-min gap | breaking_flash | breaking | breaking-detector, showrunner-breaking | live |
| The Breaking Desk: Courts (landmark Supreme Court rulings, major verdicts within minutes) | event | breaking_flash | breaking | court-watch, breaking-detector | next |
| The Breaking Desk: Weather & Disasters (hurricanes, earthquakes, wildfires; official sources only) | event | breaking_flash | breaking | weather-hazard-watcher | next |
| The Breaking Desk: Sports (franchise sales, superstar trades, coaching firings, titles) | event | breaking_flash | breaking | sports-watcher | future |
| The Breaking Desk: Space (launches, landings, crewed missions, a moon landing) | event | breaking_flash | breaking | breaking-detector | future |
| The Breaking Desk: Markets (mega-mergers, crashes, CEO exits) | event | breaking_flash | breaking | records-filings-watcher (SEC) | future |
| La Mesa de Última Hora (Breaking Desk in Spanish) | event | breaking_flash (es) | breaking | spanish-editions-editor | future |
| Decision Day: same-day Supreme Court opinion flashes in opinion season | event (opinion days) | breaking_flash | breaking | court-watch (scotus) | future |

#### Courts (per city + federal) (9)

| Show / feed | Cadence | Format | Lane | Key agents | Status |
|---|---|---|---|---|---|
| LA Courts Roundup | Tue-Sat 17:00 PT (prev day) | court_roundup | strict | court-watch, showrunner-courts | live |
| Columbia Courts (Richland, Lexington, D.S.C.) | weekly | court_roundup | strict | court-watch | next |
| NYC Courts Roundup (state courts, S.D.N.Y., E.D.N.Y.) | weekdays | court_roundup | strict | court-watch | next (wave 1) |
| Cook County Courts (with N.D. Ill.) | weekdays | court_roundup | strict | court-watch | next (wave 1) |
| Federal Docket Weekly: notable new federal suits and rulings nationwide | weekly | court_roundup | strict | court-watch (CourtListener) | next |
| Supreme Court Week: arguments, orders and opinions, in term | weekly in term | court_roundup | strict | court-watch (scotus) | next |
| Hollywood in Court: entertainment litigation in LA Superior and C.D. Cal. | weekly | court_roundup | strict | court-watch | future |
| Bankruptcy Watch: major business bankruptcies | weekly | court_roundup | strict | court-watch, records-filings-watcher | future |
| Appeals Watch: Fourth and Ninth Circuits (our first two markets' circuits) | weekly | court_roundup | strict | court-watch | future |

#### True crime (9)

| Show / feed | Cadence | Format | Lane | Key agents | Status |
|---|---|---|---|---|---|
| Case Tracker: weekly best-of-last-7-days plus development flashes | Fri 10:00 ET + event: case.development | case_weekly | strict | case-development-watcher, case-file-keeper | live |
| Cold Case Files | Tue/Thu | evergreen_story | strict | cold-case-archivist, showrunner-evergreen | live |
| Cold Case Files: Carolinas | weekly | evergreen_story | strict | cold-case-archivist | next |
| Cold Case Files: Southern California | weekly | evergreen_story | strict | cold-case-archivist | future |
| Missing: {Region}: official missing-person appeals with the tip line, short and respectful | weekly + event | niche_minute (proposed) | strict | cold-case-archivist, harm-sensitivity-reviewer | next |
| Trial Day: a temporary daily feed for one major trial, ending at the verdict | trial days | court_roundup | strict | case-file-keeper, court-watch | future |
| The Verdict: weekly verdicts and sentencings across our markets | weekly | court_roundup | strict | court-watch | future |
| Solved: cold cases closed by new evidence, from official announcements | biweekly | evergreen_story | strict | cold-case-archivist | future |
| Exonerated: wrongful convictions overturned, from court records | biweekly | evergreen_story | strict | court-watch, archive-miner | future |

#### Archives & evergreen (10)

| Show / feed | Cadence | Format | Lane | Key agents | Status |
|---|---|---|---|---|---|
| History of Hollywood | Mon/Wed/Fri | evergreen_story | archive | archive-miner, showrunner-evergreen | live |
| Hometown History: Columbia (from the Congaree to the 1865 burning to the modern capital) | weekly | evergreen_story | archive | archive-miner | next |
| Lost Los Angeles: vanished landmarks, neighborhoods and streetcar lines | weekly | evergreen_story | archive | archive-miner | next |
| Central Avenue: LA's jazz history | weekly (season of 10) | evergreen_story | archive | archive-miner, sonic-brand-librarian | next |
| Front Page, 100 Years Ago: public-domain newspaper stories retold for today | daily, 3 min | evergreen_story (short) | archive | archive-miner (Chronicling America) | next |
| On This Day in {City} | daily, 2 min | evergreen_story (short) | archive | archive-miner | future |
| Landmark Cases: Supreme Court decisions that changed daily life | weekly | evergreen_story | archive (strict for crime facts) | archive-miner, court-watch | future |
| Music history series: Motor City Sound (Detroit), Birth of Jazz (New Orleans), Music City Stories (Nashville) | weekly per series | evergreen_story | archive | archive-miner | future (with wave 5) |
| Hometown History: one per new market (Charleston, Philadelphia, Boston first) | weekly | evergreen_story | archive | archive-miner | future |
| Sports History: This Week | weekly | evergreen_story | archive | archive-miner, sports-watcher | future |

#### Hyper-specific always-on niche feeds (17)

| Show / feed | Cadence | Format | Lane | Key agents | Status |
|---|---|---|---|---|---|
| Open & Shut: restaurant and shop openings and closings | 3x weekly | niche_minute (proposed) | standard | records-filings-watcher | next |
| Permit Pulse: notable building permits and development | weekly | data_minute (proposed) | standard | records-filings-watcher | next |
| Main Street Ledger: new business filings, layoffs (WARN), big hires | weekly | data_minute (proposed) | standard | records-filings-watcher | next |
| Pollen & Air: daily pollen and air quality (Columbia's pollen season, LA smog) | daily in season, 90 s | data_minute (proposed) | standard | weather-hazard-watcher | next |
| Weather Ready: publishes only when official warnings fire | event | breaking_flash (local) | standard | weather-hazard-watcher | next |
| Recall Roundup: FDA, USDA, CPSC and NHTSA recalls, all official data | daily | data_minute (proposed) | standard | press-release-watcher | next |
| Transit Minute: LA Metro, CTA and MTA service changes | weekday mornings | data_minute (proposed) | standard | civic-data-watcher | future |
| Cost of Living Watch: gas, rent, utilities and prices from official data | weekly | data_minute (proposed) | standard | civic-data-watcher | future |
| Friday Night Scoreboard: high school football, SC first | Fri night/Sat morning in season | scoreboard (proposed) | standard (minors rule) | sports-watcher | future |
| Real Estate Pulse: big sales, development and market data | weekly | data_minute (proposed) | standard | records-filings-watcher, civic-data-watcher | future |
| Wildfire Watch LA (seasonal) | event + daily in season | breaking_flash (local) | standard | weather-hazard-watcher | future |
| Hurricane Desk: Carolinas, Gulf and Florida, Jun-Nov | event + daily in season | breaking_flash (regional) | standard | weather-hazard-watcher | future |
| Film Permits LA: what's shooting where (terms to be cleared) | weekly | data_minute (proposed) | standard | records-filings-watcher | future |
| Liquor License Watch: which bars and restaurants are coming | weekly | data_minute (proposed) | standard | records-filings-watcher | future |
| Health Inspection Report: official inspection results only | weekly | data_minute (proposed) | strict (named businesses) | records-filings-watcher | future |
| Jobs Day: BLS release days, national plus each market's numbers | event (release days) | data_minute (proposed) | standard | civic-data-watcher | future |
| Community Calendar: free and cheap things to do this week | weekly | niche_minute (proposed) | standard | beat-agent, press-release-watcher | future |

### C. Where this catalog goes next

- **Agent files.** Every id above gets an instruction file at `agents/<desk>/<id>.md` with the template's sections (why it exists, procedure, rules, output contract, hand-offs, failure modes, KPIs, system prompt).
- **Contracts.** The *(proposed)* contracts listed in the intro land in `earlobe/schemas.py` and `docs/blueprint/json-contracts.md` as their agents are built.
- **Module map.** `earlobe/sensors/press.py` (official-feed poller) exists but is not yet listed in `earlobe/README.md`. The Knowledge Base Keeper's first fix.
- **Daylight saving.** The Scheduler is first in N1. The fixed-UTC crons in `shows.yaml` will shift the 06:00 dailies to 05:00 local when US daylight saving time ends on Nov 1, 2026.
