# JSON contracts

> **[`earlobe/schemas.py`](../../earlobe/schemas.py) is the source of truth.** This page is the readable copy for
> founders and agent authors. If the two disagree, the code wins: fix this page in the same change (Convention 8).
> Examples are fictional; ids are real `make_id` output for one made-up story. `†` after an agent id = status
> `next` or `future` in [`config/agents.json`](../../config/agents.json) (not built yet).

## Ground rules

| Rule | Detail |
|---|---|
| Ids | `prefix_` + 12 hex. `schemas.py` lists `src_ sty_ clm_ ln_ scr_ ep_ cor_`; code also mints `sig_` (Signal) and `run_` (AgentRun). `make_id(prefix, *parts)` = SHA-1 of the parts, first 12 hex, so re-runs reproduce the same id and dedupe. |
| Times, scores | ISO-8601 UTC strings (`"2026-10-11T13:00:00Z"`). Scores are 0-100 integers unless noted. |
| Round trip | Every dataclass has `to_dict()`, `to_json()`, `from_dict()`. `from_dict` drops unknown keys and rebuilds nested lists (`_NESTED`): `Script.lines/claims/sources`, `VerifierReport.findings`, `VerifierFinding.evidence`, `FactCheckReport.findings`, `BiasReport.issues`, `LegalReport.issues`, `GateDecision.reasons`. |
| Validation | `validate(kind, data)` checks against `JSON_SCHEMAS[kind]`, returns error strings (`[]` = valid). Uses `jsonschema` if installed, else only checks required keys. |

```
Signal -> Story -> Script -> VerifierReport + FactCheckReport + BiasReport + LegalReport -> GateDecision
 sensors  story-desk  producer              the trust stack (LLM checkers)             standards-editor (plain code)
PUBLISH -> Episode -> trust log + RSS + host -> Correction (if facts move later).   AgentRun wraps every agent call.
```

## Vocabularies

| Name | Values | Used in |
|---|---|---|
| `SOURCE_TIERS` | 1 primary/official record (court filing, government release, original data, on-record statement); 2 wire service or established newsroom; 3 local/specialist outlet, trade press, verified expert; 4 aggregator, blog, social, unverified (never corroborates alone) | `tier` on Source, Signal, EvidenceSource |
| `SOURCE_KINDS` | article, press_release, court_record, official_data, archive, broadcast, social, other | `kind` on Source, Signal |
| `CLAIM_TYPES` | fact, number, quote, attribution, allegation, legal_status, prediction, context | `Claim.type` |
| `RISK_FLAGS` | crime, legal_proceeding, named_private_person, minor, victim, health, election, death, breaking, financial | `risk_flags` on Story, Claim, StoryTriage |
| `VERIFY_STATUS` | corroborated, single_source, unsupported, contradicted | `VerifierFinding.status` |
| `FACT_RATINGS` | accurate, minor_issue, misleading, inaccurate, unverifiable | `FactCheckFinding.rating` |
| `BIAS_TYPES` | loaded_language, one_sided, missing_perspective, framing, speculation, sensationalism, stereotype, false_balance | `BiasIssue.type` |
| `LEGAL_RISKS` | naming_minor, naming_victim, unproven_allegation, presumption_of_innocence, privacy, copyright, medical, other | `LegalIssue.risk` |
| `SEVERITY` | low, medium, high | `BiasIssue`, `LegalIssue` |
| `DECISIONS` | PUBLISH, REWRITE, HOLD, KILL | `GateDecision.decision` |
| `LANE_POLICIES` | standard, strict, breaking, archive | `lane_policy` on Script, GateDecision |
| `EPISODE_STATUS` | draft, gated, rendered, published, corrected, retracted, killed | `Episode.status` |

## Sensing

### Source
One citable thing (article, filing, release, record). Excerpts are our own words, never full text (Convention 7).
**Producers:** `researcher`† (v1: `producer/research_pack.py` builds Sources from a story's Signals), `archive-miner`†, `cold-case-archivist`†. **Consumers:** `producer` (cites `source_ids`), `fact-checker`, `publisher` (show-notes sources). `source-verifier` never sees Sources: its check is blind.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id`, `url`, `outlet` | str | required | `id` = `make_id("src", url)` |
| `title`, `excerpt`, `market` | str | `""` | Excerpt = short own-words summary |
| `published_at`, `retrieved_at` | str or null | `null` | |
| `tier`, `kind` | int, str | `3`, `"article"` | SOURCE_TIERS, SOURCE_KINDS |
| `owner_group`, `syndicated_from` | str | `""` | Parent company (same group = not independent); outlet or URL a wire copy came from |
```json
{"id":"src_b2f5f036703c","url":"https://sample-gazette.example/library-hours","outlet":"Sample Gazette","title":"Council weighs library hours","published_at":"2026-10-12T21:40:00Z",
 "retrieved_at":"2026-10-13T09:30:00Z","tier":3,"kind":"article","owner_group":"Sample Media Co","syndicated_from":"","excerpt":"Council to vote on library budget.","market":"columbia-sc"}
```

### Signal
One raw item a sensor picked up (feed entry, docket entry, release, search hit). Sensors never publish.
**Producers:** `beat-agent`, `court-watch` (built: `sensors/base.py`, `gdelt.py`, `courtlistener.py`); `press-release-watcher`†, `case-development-watcher`†, `public-meetings-watcher`†, `records-filings-watcher`†, `legislature-watcher`†, `civic-data-watcher`†, `weather-hazard-watcher`†, `social-signal-watcher`†, `sports-watcher`†, `elections-watcher`†, `community-manager`† (tips). **Consumers:** `story-desk`, `breaking-detector`, `security-sentinel`†, `case-file-keeper`†, `researcher`†.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id`, `sensor` | str | required | `id` = `make_id("sig", url)`; `sensor` = agent id |
| `market`, `beat`, `title`, `url`, `outlet` | str | required | |
| `published_at`, `summary` | str or null, str | `null`, `""` | |
| `kind`, `tier` | str, int | `"article"`, `3` | SOURCE_KINDS, SOURCE_TIERS |
| `raw` | dict | `{}` | Sensor-specific extras |
```json
{"id":"sig_b2f5f036703c","sensor":"beat-agent","market":"columbia-sc","beat":"government","title":"Council weighs library hours","url":"https://sample-gazette.example/library-hours",
 "outlet":"Sample Gazette","published_at":"2026-10-12T21:40:00Z","summary":"Council to vote on library budget.","kind":"article","tier":3,"raw":{}}
```

### Story
A clustered news event after dedupe: the Story Desk's unit of work.
**Producers:** `story-desk`, `breaking-detector` (sets `breaking`), `localizer`†, `follow-up-editor`† (stubs). **Consumers:** `assignment-editor`, `producer`, `researcher`†, `showrunner-breaking`†.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id`, `market`, `beat`, `headline`, `summary`, `first_seen` | str | required | `id` = `make_id("sty", market, first signal id)` |
| `signal_ids`, `source_ids`, `outlets` | list | `[]` | `source_ids` are `src_` ids from signal URLs |
| `independent_outlets` | int | `0` | Distinct owner groups (`config/owners.yaml`); syndicated copies count once |
| `official_confirmation`, `breaking` | bool | `false` | |
| `newsworthiness`, `velocity` | int, float | `0`, `0.0` | 0-100; independent outlets per hour in the detector window |
| `risk_flags`, `entities`, `assigned_shows` | list | `[]` | RISK_FLAGS; names; show ids |
```json
{"id":"sty_d9a27e616531","market":"columbia-sc","beat":"government","headline":"County council approves library budget","summary":"Council voted 5-2 on Monday.",
 "first_seen":"2026-10-12T21:45:00Z","signal_ids":["sig_b2f5f036703c","sig_a1190f6a41a5"],"source_ids":["src_b2f5f036703c","src_a1190f6a41a5"],
 "outlets":["Sample Gazette","Sample County"],"independent_outlets":2,"official_confirmation":true,"newsworthiness":62,"velocity":0.0,"breaking":false,
 "risk_flags":[],"entities":["Sample County Council"],"assigned_shows":["columbia-daily"]}
```

## Production

### Script (with ScriptLine, Claim)
The episode text, its claim map and its sources. Every factual line points at its claims; that map is what lets the trust stack run. The AI disclosure outro must be present (gate rule S1).
**Producers:** `producer` (draft, rewrites), `claim-extractor` (re-emits it with a complete claim map), `disclosure-agent`, `copy-editor`†, `spanish-editions-editor`† (es). **Consumers:** `source-verifier` (claims only), `fact-checker`, `bias-checker`, `legal-screener`, `standards-editor`, `copywriter`, `studio-voice`, `newsletter-editor`†, `transcript-accessibility`†.
Methods: `word_count()`, `char_count()`, `est_duration_sec(wpm=155)`.

| Contract | Field | Type | Default | Notes |
|---|---|---|---|---|
| Script | `id`, `show_id`, `episode_date`, `title` | str | required | `id` = `make_id("scr", show, date, sorted story ids, revision)`; date `YYYY-MM-DD` |
| | `lines`, `claims`, `sources` | list | `[]` | ScriptLine, Claim, Source |
| | `story_ids`, `notes_for_checkers`, `lane_policy`, `revision` | list, str, str, int | `[]`, `""`, `"standard"`, `0` | `lane_policy` from LANE_POLICIES; `revision` = rewrite-loop counter |
| ScriptLine | `id`, `speaker`, `text` | str | required | `id` = `ln_` hash; `speaker` = persona id in `config/voices.yaml` |
| | `claim_ids` | list | `[]` | Claims the line states |
| | `segment` | str | `"body"` | cold_open, intro, body, kicker, disclosure, outro |
| Claim | `id`, `text` | str | required | One checkable assertion as worded in the script |
| | `line_ids`, `source_ids` | list | `[]` | Lines that state it; writer's sources (hidden from the verifier) |
| | `entities`, `risk_flags` | list | `[]` | `entities` is not in the `Script` JSON Schema |
| | `type`, `attributed` | str, bool | `"fact"`, `false` | CLAIM_TYPES; `attributed` = script says who claims it ("police said") |
```json
{"id":"scr_296da172ac2b","show_id":"columbia-daily","episode_date":"2026-10-13","title":"Columbia Daily, Oct 13",
 "lines":[{"id":"ln_14cba5be73b7","speaker":"mara","text":"The council approved the library budget on Monday.","claim_ids":["clm_324a5b56cd69"],"segment":"body"},
          {"id":"ln_b0051d99d5b4","speaker":"theo","text":"(standard AI disclosure outro)","claim_ids":[],"segment":"disclosure"}],
 "claims":[{"id":"clm_324a5b56cd69","text":"The council approved the library budget on Monday.","type":"fact","line_ids":["ln_14cba5be73b7"],"source_ids":["src_b2f5f036703c"],
            "entities":["Sample County Council"],"risk_flags":[],"attributed":false}],
 "sources":[{"id":"src_b2f5f036703c","url":"https://sample-gazette.example/library-hours","outlet":"Sample Gazette"}],
 "story_ids":["sty_d9a27e616531"],"lane_policy":"standard","revision":0,"notes_for_checkers":""}
```

## Trust stack

### VerifierReport (with VerifierFinding, EvidenceSource)
Blind check: the verifier gets claims only, searches for itself, and reports who independently supports each one.
**Producer:** `source-verifier`. **Consumers:** `fact-checker`, `standards-editor`, `recheck-monitor` and `source-ledger-keeper`† (history).

| Contract | Field | Type | Default | Notes |
|---|---|---|---|---|
| VerifierReport | `script_id`, `findings`, `searches_used` | str, list, int | required, `[]`, `0` | VerifierFinding; `searches_used` is an engine count, not in the JSON Schema |
| VerifierFinding | `claim_id`, `status` | str | required | VERIFY_STATUS |
| | `independent_count` | int | `0` | Distinct owner groups, syndication collapsed, tier <= 3 |
| | `has_official`, `traced_to_original` | bool | `false` | `has_official` = at least one tier-1 source supports it |
| | `evidence`, `note` | list, str | `[]`, `""` | EvidenceSource |
| EvidenceSource | `url`, `outlet` | str | required | |
| | `tier`, `owner_group`, `supports`, `note` | int, str, bool, str | `3`, `""`, `true`, `""` | `supports: false` = source contradicts the claim |
```json
{"script_id":"scr_296da172ac2b","searches_used":3,"findings":[{"claim_id":"clm_324a5b56cd69","status":"corroborated","independent_count":2,"has_official":true,
 "traced_to_original":true,"note":"","evidence":[{"url":"https://sample-county.example/council/minutes-2026-10-12","outlet":"Sample County","tier":1,"owner_group":"Sample County","supports":true,"note":"Minutes record the vote"},
 {"url":"https://sample-gazette.example/library-hours","outlet":"Sample Gazette","tier":3,"owner_group":"Sample Media Co","supports":true,"note":""}]}]}
```

### FactCheckReport, BiasReport, LegalReport (with their item contracts)
**Producers:** `fact-checker` (second opinion on accuracy, given the script and the VerifierReport), `bias-checker`, `legal-screener` (defamation, privacy, minors, victims, presumption of innocence); `originality-checker`† will add issues with `risk: "copyright"`. **Consumer of all three:** `standards-editor`. Examples below, one per line, in that order.

| Contract | Field | Type | Default | Notes |
|---|---|---|---|---|
| FactCheckReport | `script_id`, `findings` | str, list | required, `[]` | FactCheckFinding |
| FactCheckFinding | `claim_id`, `rating` | str | required | FACT_RATINGS |
| | `issue`, `suggested_fix` | str | `""` | |
| BiasReport | `script_id`, `balance_score` | str, int | required, `100` | `balance_score` is 0-100, higher = more balanced and neutral |
| | `issues`, `missing_perspectives` | list | `[]` | BiasIssue; list of str |
| BiasIssue | `line_id`, `type`, `severity` | str | required | BIAS_TYPES, SEVERITY |
| | `explanation`, `suggestion` | str | `""` | |
| LegalReport | `script_id`, `issues` | str, list | required, `[]` | LegalIssue |
| LegalIssue | `target_id`, `risk`, `severity` | str | required | `target_id` = claim id or line id; LEGAL_RISKS, SEVERITY |
| | `explanation`, `fix` | str | `""` | |

```json
{"script_id":"scr_296da172ac2b","findings":[{"claim_id":"clm_3853a1294aea","rating":"minor_issue","issue":"Vote count rests on one outlet.","suggested_fix":"Attribute the 5-2 count to the council minutes."}]}
{"script_id":"scr_296da172ac2b","balance_score":88,"missing_perspectives":["Library staff view"],"issues":[{"line_id":"ln_14cba5be73b7","type":"framing","severity":"low","explanation":"Only the council side is quoted.","suggestion":"Add one line on library staff."}]}
{"script_id":"scr_296da172ac2b","issues":[{"target_id":"ln_14cba5be73b7","risk":"privacy","severity":"low","explanation":"Illustrative: names a private resident's street.","fix":"Say the neighborhood instead."}]}
```

### GateDecision (with GateReason)
The publish decision, made by fixed rules in `trust/gate.py`, never by a model: same inputs, same decision.
**Producer:** `standards-editor`. **Consumers:** `network-director` (routing), `producer` (`rewrite_instructions`), `copywriter`, `publisher`, `showrunner-breaking`†, `run-auditor`†, `transparency-reporter`†. Copied into `Episode.gate` and the public trust log.

| Contract | Field | Type | Default | Notes |
|---|---|---|---|---|
| GateDecision | `script_id`, `decision`, `lane_policy`, `revision` | str, str, str, int | required | DECISIONS, LANE_POLICIES |
| | `reasons`, `rewrite_instructions` | list | `[]` | GateReason; fix text for the Producer, filled only on REWRITE |
| | `scores` | dict | `{}` | Gate writes `corroboration_rate`, `accuracy_rate` (0-1 floats), `balance_score` (0-100), `claims` (count) |
| | `recheck_after_minutes` | int or null | `null` | Set only on HOLD (breaking lane) |
| GateReason | `rule_id`, `detail` | str | required | |
| | `target_id`, `blocking` | str, bool | `""`, `true` | Claim or line id |

Rule ids (`trust/gate.py`): V0 claim not verified, V1 contradicted, V2 unsupported, V3 too few independent sources, V4 sensitive claim lacks an official record, V5 unattributed prediction, F0 not fact-checked, F1 rated inaccurate or misleading, F2 unverifiable, B1 balance below lane minimum, B2 high-severity bias, L1 legal issue at or above lane severity, L2 naming a minor or victim (hard stop), S1 missing AI disclosure.
```json
{"script_id":"scr_296da172ac2b","decision":"REWRITE","lane_policy":"standard","revision":0,
 "reasons":[{"rule_id":"B1","detail":"balance score 64 < 70","target_id":"","blocking":true}],"rewrite_instructions":["Rebalance: neutralize framing"],
 "scores":{"corroboration_rate":1.0,"accuracy_rate":1.0,"balance_score":64,"claims":2},"recheck_after_minutes":null}
```

## Publishing and operations

### Episode
One produced episode. Only an episode whose `gate.decision` is `PUBLISH` (status not `retracted` or `killed`) can go to a host; no override. The RSS feed lists only episodes with an `audio_url` and a status other than `draft`, `gated`, `retracted`, `killed`.
**Producers:** `network-director` (assembles), `copywriter` (title, description, notes), `disclosure-agent` (`disclosure_text`), `sound-designer` (audio, duration), `transcript-accessibility`†, `publisher` (published fields). **Consumers:** `publisher`, `feed-manager`, `recheck-monitor`, `corrections-agent`, `directory-sync-checker`†, `website-publisher`†, `follow-up-editor`†, `clip-maker`†, `analytics-insights`†.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id`, `show_id`, `script_id`, `title`, `description` | str | required | `id` = `ep_` hash |
| `show_notes_md`, `transcript_path` | str | `""` | Markdown with sources |
| `audio_path`, `audio_url` | str | `""` | Local file; public URL |
| `duration_sec`, `source_count` | int | `0` | `source_count` goes to the trust log |
| `published_at`, `guid` | str or null, str | `null`, `""` | Feed falls back to `id` when `guid` is empty |
| `status` | str | `"draft"` | EPISODE_STATUS |
| `disclosure_text` | str | `""` | Disclosure must also be in metadata (Convention 6) |
| `gate` | dict | `{}` | `GateDecision.to_dict()` |
```json
{"id":"ep_f79e1f1cc7f7","show_id":"columbia-daily","script_id":"scr_296da172ac2b","title":"County council approves library budget","description":"Today in Columbia: the library budget vote.",
 "show_notes_md":"## In this episode\n- Library budget vote","audio_path":"data/public/audio/ep_f79e1f1cc7f7.mp3","audio_url":"https://earlobe.invalid/audio/ep_f79e1f1cc7f7.mp3","duration_sec":412,
 "published_at":"2026-10-13T10:00:00Z","guid":"","status":"published","disclosure_text":"(standard AI disclosure text)","transcript_path":"","gate":{"decision":"PUBLISH","lane_policy":"standard","revision":1},"source_count":2}
```

### Correction
A fix to something we published. **Producers:** `recheck-monitor` (`reported_by` `"monitor:recheck"`), `community-manager`† (`"listener"`), outlet reports (`"outlet"`). **Consumers:** `corrections-agent` (applies it), `publisher` (show notes list applied fixes), `transparency-reporter`†, `source-ledger-keeper`†.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id`, `episode_id`, `description` | str | required | `id` = `cor_` hash |
| `claim_id`, `reported_by`, `created_at` | str | `""` | |
| `status`, `action` | str | `"open"`, `"note"` | open/applied/rejected; note/reissue/retract |
```json
{"id":"cor_0e83a5e0ba8d","episode_id":"ep_f79e1f1cc7f7","description":"Vote was 4-3, not 5-2, per amended minutes.","claim_id":"clm_3853a1294aea",
 "reported_by":"monitor:recheck","created_at":"2026-10-15T10:05:00Z","status":"open","action":"reissue"}
```

### AgentRun
Envelope every agent call is logged in (`Store.log_run`). **Producer:** the LLM wrapper (`earlobe/llm.py`), under `network-director`; dry runs log zero-cost runs like the example. **Consumers:** `budget-controller` (sums `usd_estimate` per show per day), `run-auditor`†, `finance-reporter`†, `quota-sentinel`†, `incident-commander`†, `vendor-pricing-watch`†. `model_tier` holds a tier name (`opus`, `sonnet`, `haiku`), never a model ID (Convention 4). `agent_id` is the call label in code and can differ from the catalog id (for example `verifier` is `source-verifier`).

| Field | Type | Default | Notes |
|---|---|---|---|
| `agent_id`, `run_id`, `model_tier`, `started_at` | str | required | `run_id` = `run_` + 12 hex |
| `finished_at`, `error` | str | `""` | |
| `input_tokens`, `output_tokens`, `web_searches` | int | `0` | |
| `usd_estimate`, `ok` | float, bool | `0.0`, `true` | Cost estimate from the price table in `earlobe/config.py` |
```json
{"agent_id":"producer","run_id":"run_1a2b3c4d5e6f","model_tier":"opus","started_at":"2026-10-13T09:40:02Z","finished_at":"2026-10-13T09:40:02Z",
 "input_tokens":0,"output_tokens":0,"web_searches":0,"usd_estimate":0.0,"ok":true,"error":""}
```

## JSON_SCHEMAS (structured model outputs)

Seven schemas are sent to the model as its output format and re-checked with `validate()`; bad output gets one retry. Each schema object is `additionalProperties: false` with every property required, so a model must return every field; enums are enforced here only (dataclass fields are plain strings). A schema holds only what the model must produce; the engine fills the rest. The examples above for these five contracts are the engine-side dataclass shape, so they carry extra fields (last column).

| Key | Call | Agent | Model returns | Engine adds |
|---|---|---|---|---|
| `Script` | structured | `producer`, `claim-extractor` | `title`, `lines[]` (id, speaker, text, claim_ids, segment), `claims[]` (id, text, type, line_ids, source_ids, risk_flags, attributed) | `id`, `show_id`, `episode_date`, `sources`, `story_ids`, `lane_policy`, `revision`, `notes_for_checkers`, `Claim.entities` |
| `VerifierReport` | research (web search) | `source-verifier` | `findings[]` incl. `evidence[]` | `script_id`, `searches_used` |
| `FactCheckReport` | research (web search) | `fact-checker` | `findings[]` | `script_id` |
| `BiasReport` | structured | `bias-checker` | `balance_score`, `issues[]`, `missing_perspectives` | `script_id` |
| `LegalReport` | structured | `legal-screener` | `issues[]` | `script_id` |
| `StoryTriage` | structured | `story-desk` | `stories[]` | merged into Story |
| `Copy` | structured | `copywriter` | all five fields | copied into Episode |

### StoryTriage
Optional Haiku-tier read of the Story Desk's clusters; no dataclass. **Producer and consumer:** `story-desk` (merges it into `Story`), then `assignment-editor`. In v1 (`desk/score.py`) it blends newsworthiness 60/40 with the heuristic and may add `risk_flags` and `entities`; it never rewrites headlines or summaries.

| Field (items of `stories[]`) | Type | Notes |
|---|---|---|
| `cluster_key` | str | The Story `id` the item refers to |
| `headline`, `summary`, `beat`, `newsworthiness` | str, str, str, int | Newsworthiness is 0-100 |
| `risk_flags`, `entities`, `signal_ids` | list of str | RISK_FLAGS; names; `sig_` ids |
```json
{"stories":[{"cluster_key":"sty_d9a27e616531","headline":"County council approves library budget","summary":"Council voted 5-2 on Monday.","beat":"government",
 "newsworthiness":58,"risk_flags":[],"entities":["Sample County Council"],"signal_ids":["sig_b2f5f036703c","sig_a1190f6a41a5"]}]}
```

### Copy
Listener-facing words, written only after the gate passes, from the gated script; no dataclass.
**Producer:** `copywriter`. **Consumers:** `publisher` (becomes Episode title, description, notes), `headline-tester`†, `social-media-manager`†, `seo-metadata`†, `newsletter-editor`†, `art-director`†, `brand-guardian`†.

| Field | Type | Notes |
|---|---|---|
| `title`, `description` | str | Most specific fact in the title; hook first in the description; no claim outside the script |
| `show_notes_md` | str | Markdown |
| `social_posts`, `keywords` | list of str | |
```json
{"title":"County council approves library budget","description":"The council voted Monday on library funding. Here is what changes.",
 "show_notes_md":"## In this episode\n- Library budget vote","social_posts":["New episode: County council approves library budget"],"keywords":["Columbia","county council","library"]}
```

## Not in `schemas.py` yet, and changing a contract

`agents.json` names these as *(proposed)*: `ResearchPack` (v1 is a plain dict), `HarmReport`, `CaseFile`, `TopicBrief`, `InsightReport`, `ShowSpec`, `MeetingDigest`, `QAReport`, `ClipSpec`. Each is added to `schemas.py` and to this page together when its agent is built.
To change a contract: (1) edit `schemas.py` (dataclass, `JSON_SCHEMAS` entry if a model produces it, `_NESTED` if it nests); (2) update this page in the same change; (3) keep the `fixtures.py` builders schema-valid and run the tests; (4) `release-guard`† checks `schemas.py` against this page and `eval-steward`† re-runs golden sets on any schema change.
