# Verification Protocol: how we confirm a claim before it airs

| | |
|---|---|
| **Applies to** | Every claim in every episode on every Curious & Creative Network show |
| **Agent** | Source Verifier (Trust Stack), status `next`, module `earlobe/trust/verifier.py` |
| **Enforced by** | Standards Editor gate, status `built`, [`earlobe/trust/gate.py`](../../earlobe/trust/gate.py) rules **V0–V4** |
| **Contracts** | `VerifierReport`, `VerifierFinding`, `EvidenceSource`, `SOURCE_TIERS` in [`earlobe/schemas.py`](../../earlobe/schemas.py) |
| **Config it reads** | [`config/owners.yaml`](../../config/owners.yaml), `config/sources/<market>.yaml`, [`config/markets.yaml`](../../config/markets.yaml), [`config/shows.yaml`](../../config/shows.yaml) |
| **Last reviewed** | October 2026 |

---

## The short version

> "You have to see it in two or three places." That's the rule Joshua brought from journalism school, and it's the rule this whole document turns into code.

The Curious & Creative Network is fully automated. No person reads an episode before it goes out. Our hosts (Mara, Theo, Lena, Marcus, Ava and June) are original synthetic voices, and every episode ends with a spoken AI disclosure that is also carried in the feed metadata. Because nobody reviews the episode before it airs, the checking has to be stricter than it would be in a newsroom where an editor reads everything.

| | |
|---|---|
| **What it does** | For every factual claim in a script, a separate agent goes and finds its **own** sources, without seeing the writer's. It works out who really owns each source and where each story first came from, then writes down exactly what it found. |
| **Why it matters** | If the checker could see the writer's sources, it would tend to confirm them. Searching blind means two separate searches have to agree before anything airs. Counting owners instead of logos stops five rewrites of one press release from passing as five confirmations. |
| **What it costs** | Web searches. The default is a budget of 20 per script (`verify(..., max_searches=20)`). Section 7 gives the limit per claim and per lane. Prices for searches are in the facts sheet, not here. |
| **What happens when it can't confirm** | The claim is cut, rewritten, or (on The Breaking Desk only) held and checked again every 15 minutes. If it still can't be confirmed, it doesn't air. |

**Our promises to listeners**

1. **We find our own sources.** The checker never starts from the writer's links.
2. **We count owners, not logos.** Three stations owned by one company count as one source. Wire copy counts as the wire.
3. **We go back to the original.** We follow "according to" until we reach the document, the statement, or the first report.
4. **We know when a source has gone stale.** A road closure from yesterday is not a road closure today.
5. **When we can't confirm, we wait or we stay quiet.** The Breaking Desk does not air "unconfirmed reports." If it isn't confirmed, Ava doesn't say it.

Some of these standards are stricter than the code that enforces them today. Those gaps are listed in the **Not yet enforced in code** box near the end. We'd rather show you the gaps than paper over them.

---

## 0. Where the Verifier sits

```
Producer (writes script + claim map)
   → Claim extractor (independent pass, adds missed claims)
   → SOURCE VERIFIER (blind)  ──┐
   → Fact Checker (reads the Verifier's report)
   → Bias Checker, Legal Screener (each in isolation)
   → Standards Editor gate (deterministic code: PUBLISH / REWRITE / HOLD / KILL)
   → after publish: Monitor re-checks published claims for 7 days
```

The Verifier makes no decisions. It produces evidence. The gate is plain Python with no AI in it, and it turns that evidence into a decision using fixed rules. Given the same inputs, it makes the same decision every time.

### How the Verifier's output becomes a gate decision

| What the Verifier reports for a claim | Gate rule | Kind of block | What happens |
|---|---|---|---|
| No finding at all for a claim that needs checking | **V0** | hard | REWRITE ("drop or re-source"), then KILL. Never HOLD. |
| `status: "contradicted"` | **V1** | hard | REWRITE ("correct or remove"). The finding's `note` is passed to the Producer word for word. |
| `status: "unsupported"` | **V2** | hard | REWRITE ("remove"). |
| Supported, but not enough independent sources for the lane | **V3** | threshold | HOLD on the breaking lane. REWRITE elsewhere. |
| Enough sources, but a sensitive claim lacks an official record on a lane that needs one | **V4** | threshold | HOLD on the breaking lane. REWRITE elsewhere. |
| (Script problem, not the Verifier's) a prediction with no attribution | **V5** | hard | REWRITE ("attribute or cut"). |

**Which claims need checking.** Claims whose `type` is in `NEEDS_CORROBORATION`: `fact`, `number`, `quote`, `attribution`, `allegation`, `legal_status`. `context` and `prediction` claims are not counted by V0–V4. See box item 9.

**Which claims are "sensitive".** In code, a claim is sensitive if its type is in `SENSITIVE_TYPES` (`allegation`, `legal_status`), or if it carries any flag in `SENSITIVE_FLAGS`: `crime`, `legal_proceeding`, `named_private_person`, `minor`, `victim`, `death`. The flags `health`, `election`, `financial` and `breaking` do **not** make a claim sensitive.

---

## 1. Blind re-sourcing, step by step

**In plain language.** The Verifier gets the claims, but not the writer's homework. It treats each claim as something a stranger told it, and goes looking: first for the official record, then for independent reporting, then for anything that proves the claim wrong. It reads every source it counts, works out who owns it and where its information came from, and only then decides whether the claim holds up.

### Rules

**Intake**

- **VP-1.1 The blind packet.** The Verifier receives only:
  - each claim's `id`, `text`, `type`, `risk_flags`, `attributed` and `entities`;
  - the text of the script lines the claim appears in, for context;
  - `show_id`, `lane_policy`, market, `episode_date` and render time;
  - on the breaking lane, the story's `first_seen` time.

  It must **not** receive any of these: `Script.sources`, `Claim.source_ids`, `Script.notes_for_checkers`, the research pack, the Story's `signal_ids`, `source_ids` or `outlets`, or any other checker's report. *Test:* no URL or source id from `Script.sources` or `Story.source_ids` appears anywhere in the Verifier's input.
- **VP-1.2 HOLD-recheck exception.** On a breaking-lane recheck, the Verifier may also receive **its own** previous report for the same script, so it can re-read sources it already counted (section 6.4). This is the only prior output it ever sees.
- **VP-1.3 Coverage.** Return exactly one finding for every claim whose type is in `NEEDS_CORROBORATION`. The finding's `claim_id` must match the script's claim id exactly. A missing finding fires V0. A duplicate is a contract violation, because the gate keeps only the last one.
- **VP-1.4 Low-priority claims.** Check `context` claims only with budget left after all must-check claims are done, and always report a contradiction you find along the way. The Fact Checker reads your report. For `prediction` claims, check only that the named person or body actually made the prediction.

**Working each claim**

- **VP-1.5 Order of work.** Work in this order:
  1. sensitive claims;
  2. numbers and quotes in the lead story;
  3. remaining `fact`, `number` and `quote` claims;
  4. `attribution` claims;
  5. `context` claims.
- **VP-1.6 Break the claim into parts.** Split each claim into checkable parts: who, what, when, where, how many, the exact words, and a **time anchor** (as of when must this be true?). The claim's status is the **worst** status among its parts, ranked `contradicted` < `unsupported` < `single_source` < `corroborated`.
- **VP-1.7 Primary first.** The first search for each claim aims at where the official record would be. Section 5 lists that place for each beat.
- **VP-1.8 Independent coverage second.** Next, search for reporting from **other owner groups**. Prefer outlets listed in `config/sources/<market>.yaml`.
- **VP-1.9 Try to prove it wrong.** Run at least one search designed to prove the claim wrong: a denial, a correction, a hoax debunk, an older date, a different number. This is **required** for sensitive claims, for every breaking-lane claim, and for every number in the lead story.
- **VP-1.10 Read it.** A source supports a claim only if its **body** states it. A headline, a search snippet or a URL slug never counts. If you could not open and read a source, record it as `not_counted:unreadable`.
- **VP-1.11 Classify every source** you record by tier (section 2), owner group (section 3), `kind` (one of `SOURCE_KINDS`), published and updated time (section 4), and role (section 8).
- **VP-1.12 Trace and count.** Trace each source to the original and collapse the sources into independent groups (sections 3.4 and 3.5).

**Status, precision and limits**

- **VP-1.13 Status.** Use the first of these that applies.

  | Status | When |
  |---|---|
  | `contradicted` | A tier 1 or tier 2 source, inside the recency window, states something that conflicts with any part of the claim as worded, and no higher-tier or newer same-tier source settles it in the claim's favor. Also used when tier ≤2 sources disagree with each other and nothing settles it (flag `CONFLICT`). |
  | `corroborated` | Not contradicted, and `independent_count ≥ 2`. |
  | `single_source` | Not contradicted, and `independent_count = 1`. |
  | `unsupported` | `independent_count = 0`, including when the only sources are tier 4 or not counted. |

  A tier-3 source that conflicts with the claim does not make it `contradicted` on its own. It triggers another search to try to prove the claim wrong, and you mention it in the note.
- **VP-1.14 Precision.**
  - **Numbers** match at the precision the script states. "About 40" is supported by 38–42. "More than 40" needs a number above 40.
  - **Quotes** need the exact words. Filler words ("um", "uh") may be dropped. Any other difference is `contradicted`, with the correct words in the note.
  - **Attribution** claims are about the *saying*. The named party must have said it.
  - **Allegations** are checked for *who alleged what, where* (filing, statement, hearing). The truth of the allegation is never checked or reported as fact.
  - **Legal status** must match the exact stage: arrested/booked, charged, arraigned, indicted, pleaded, convicted, sentenced, acquitted, dismissed. A different stage is `contradicted`.
- **VP-1.15 When to stop.** Stop working a claim once the lane threshold is met (section 6) **and** any required try-to-prove-it-wrong search is done, or once its search ceiling is reached (section 7). Stopping early never changes how the status is worked out.
- **VP-1.16 What you know is not evidence.** Your own memory never supports or contradicts a claim. Only sources found during this run count. If memory says a claim is wrong, search for proof.
- **VP-1.17 Stay in your lane.** Never edit the script. Never suggest new wording, beyond stating the correct fact in the note. Never judge whether a story is newsworthy, fair or legal. The other checkers own those questions.

---

## 2. Source tiers

**In plain language.** Not all sources are equal. A court filing beats a newspaper story about the filing, and a newspaper story beats a tweet. We sort sources into four tiers. Only the top three can ever count, and the bottom tier is just a lead to something better.

These definitions come straight from `SOURCE_TIERS` in `earlobe/schemas.py`:

| Tier | Definition (from code) | Counts toward `independent_count`? |
|---|---|---|
| **1** | primary/official record (court filing, government release, original data, on-record statement) | Yes. Also sets `has_official` |
| **2** | wire service or established newsroom with editorial standards | Yes |
| **3** | local/specialist outlet, trade press, verified expert | Yes. Breaking standard excludes it (box item 1) |
| **4** | aggregator, blog, social post, unverified | **Never** ("never counts toward corroboration alone") |

### Rules

- **VP-2.1 Config wins.** If an outlet is listed in `config/sources/<market>.yaml`, use that tier. Until those files are filled in, the seed lists below are the defaults.
- **VP-2.2 Unknown outlets start at tier 4.** An unlisted outlet can be promoted to **tier 3, never higher**, in a single run, and only if it passes all of these:
  - named staff with a visible byline history;
  - an about page naming its owner;
  - a corrections policy, or visible corrections;
  - original reporting, not only rewrites;
  - a publishing history of at least a year.

  Record any promotion with the flag `NEW_OUTLET` so the Industry Intel agent can add the outlet to config.
- **VP-2.3 Tier 1 must be authentic.** A source is tier 1 only if it was published on a channel the official body controls: its own domain, or an account linked from that domain or listed in config. A screenshot, a re-hosted PDF, a forwarded email, or a "statement" posted by someone else is not tier 1 until you find it on the official channel.
- **VP-2.4 Tier 1 is the record, not the verdict.** A company release is tier 1 for "the company announced X", not for contested facts like "the product is safe". A police account of a contested incident is tier 1 for "police said X". If another tier ≤2 source disputes it, flag `CONFLICT`.
- **VP-2.5 Recording tier-4 sources.** A tier-4 source is always recorded with `supports: false` and `role=not_counted:tier4` (or a more specific reason). It may still be the place the claim started, which goes in the finding's `origin=` (section 8).
- **VP-2.6 Wikipedia is tier 4.** Use it only to find its citations, then evaluate those.
- **VP-2.7 Video of officials.** An official's own livestream or recording of a press conference is tier 1. An outlet's report of the press conference is that outlet's tier.
- **VP-2.8 State-run media.** State-controlled media count as the voice of their government: tier 1 for "the government says", **never** an independent confirmation of the underlying fact.

### Seed examples by market

Seed lists for `config/sources/*.yaml`. Outlets are shown with their owner group from `config/owners.yaml` where it lists one.

**Columbia, SC** (`columbia-sc`)

| Tier | Examples |
|---|---|
| 1 | Columbia Police Department; Richland County and Lexington County Sheriff's Departments; SC Law Enforcement Division (SLED); Richland County Coroner; City of Columbia council agendas, minutes and votes; Richland County Council; SC Governor's Office; SC General Assembly bill text and votes; **SC Judicial Branch / Richland County Public Index** (state courts); U.S. District Court for the District of South Carolina docket (`dsc`); SC Election Commission results; National Weather Service Columbia office; SC Emergency Management Division; University of South Carolina and Gamecocks athletics official releases; school district statements; state WARN layoff notices |
| 2 | The State (McClatchy); The Post and Courier / Post and Courier Columbia (Evening Post Industries); WIS (Gray Media); WLTX (TEGNA); SC Daily Gazette (States Newsroom); AP's South Carolina coverage |
| 3 | Free Times (Evening Post Industries, so it is the **same group** as The Post and Courier); trade and specialist outlets; university experts quoted on the record; hyperlocal sites that pass VP-2.2 |
| 4 | Neighborhood Facebook groups and Nextdoor; scanner-feed accounts; unattributed social video; aggregator pages |

**Los Angeles** (`los-angeles`)

| Tier | Examples |
|---|---|
| 1 | LAPD; LA County Sheriff's Department; LAFD; LA County Fire; CAL FIRE incident pages; LA County Department of Medical Examiner; Mayor's office and City Clerk council files; LA County Board of Supervisors; LA County District Attorney; LA City Attorney; **LA Superior Court portal**; U.S. District Court, Central District of California (`cacd`); U.S. Attorney's Office (C.D. Cal.); LA Metro; LAUSD; Caltrans; NWS Los Angeles; USGS earthquake pages; LA County Registrar-Recorder/County Clerk results; California EDD WARN reports; studio and company newsrooms and SEC filings |
| 2 | Los Angeles Times (LA Times); LAist / KPCC (Southern California Public Radio); KTLA (Nexstar); NBC4 and Telemundo 52 (Comcast NBCUniversal, **one group**); ABC7 (Disney); CBS Los Angeles and KCAL (Paramount, **one group**); Los Angeles Daily News, Orange County Register and Press-Telegram (MediaNews Group, **one group**); AP and Reuters LA coverage; City News Service (a regional wire, so treat it as a wire, VP-3.6) |
| 3 | Variety, The Hollywood Reporter and Deadline (trade press, commonly reported to share one owner, Penske Media; *verify and add to owners.yaml*); celebrity-news sites; neighborhood outlets that pass VP-2.2 |
| 4 | Crowd-sourced incident apps and scanner accounts; "BREAKING" aggregator accounts; unverified social posts; AI-written local-news lookalike sites |

**National / Global** (`national`)

| Tier | Examples |
|---|---|
| 1 | White House and federal agency releases; **Supreme Court opinions and orders** (`scotus`); federal dockets (PACER/CourtListener); Congress.gov bill text and roll calls; SEC EDGAR filings; BLS, Census and BEA data releases; NWS, National Hurricane Center, USGS, NASA; league and team official announcements; company statements on their own channels; foreign governments' official channels; UN agencies |
| 2 | Wires: Associated Press, Reuters, AFP, Bloomberg (`owners.yaml: wires`); The New York Times (NYT Company); NBC News (Comcast NBCUniversal, the **same group as NBC4 LA**); ABC News (Disney, the **same group as ABC7**); CBS News (Paramount, the **same group as KCAL**); The Hill (Nexstar, the **same group as KTLA**) |
| 3 | Specialist legal, science and business outlets; trade press; verified experts on the record |
| 4 | Wikipedia; content farms; satire (section 9); social posts from non-official accounts; aggregator pages (Yahoo News, MSN, Apple News, Google News) |

When New York and Chicago launch (wave 1), their lists go in `config/sources/new-york.yaml` and `chicago.yaml`. `owners.yaml` already groups the Chicago Sun-Times and WBEZ as **one** source (Chicago Public Media).

---

## 3. Independence: counting owners, not logos

**In plain language.** "Two or three places" only means something if those places found it out separately. Three TV stations owned by one company often share one newsroom's work. Ten websites running the same AP story are one AP story. Five outlets rewriting the same sheriff's press release are really one release, plus the fact that newsrooms chose to run it. Before we count, we collapse everything that came from the same place.

### 3.1 Owner groups

- **VP-3.1 Use the owners file.** An outlet's group is the group name in `config/owners.yaml` (e.g. `Nexstar`, `Comcast NBCUniversal`). An outlet not listed there is its own group, written as the outlet name. That is the file's own rule.
- **VP-3.2 Official bodies.** An official body is its own group, named for the issuing body (e.g. `Los Angeles Fire Department`). A **joint** statement from several bodies is one source. Two different bodies that each published their own statement are two groups.
- **VP-3.3 When in doubt, merge.** If you find evidence that two outlets share an owner or a content partnership that `owners.yaml` doesn't reflect, count them as **one** and add the flag `OWNER_UPDATE` so Industry Intel can review it. Merging is always the safe direction, because it can only make us count fewer sources.

  Ownership changes. For example, `owners.yaml` puts CNBC and MSNBC in the Comcast NBCUniversal group. Comcast announced in 2024 that it would spin most of its cable networks off into a separate company *(inference: verify current ownership before relying on this grouping)*.
- **VP-3.4 Shared content.** Content shared under a republishing arrangement counts as the newsroom that produced it. Examples: SC Daily Gazette stories republished by other South Carolina papers; statewide nonprofit stories republished across California papers; a local station airing its network's report.

### 3.2 Wires and syndication

- **VP-3.5 Wire copy counts as the wire.** Wire copy republished by an outlet counts as **the wire**, not the outlet (`owners.yaml: wires`: Associated Press, Reuters, AFP, Bloomberg). You can recognize wire copy by a wire byline or credit line, a "(AP) —" dateline, or text identical to the wire's own version.

  Record **one** entry with `outlet` and `owner_group` set to the wire and `url` set to the wire's own copy if you can find it (otherwise the republisher's), plus `via=<republisher>` in the note. Set `outlet` to the wire even when the URL is the republisher's. Then the count comes out right however the engine derives the group.
- **VP-3.6 City News Service.** In Los Angeles, City News Service copy runs on many station and newspaper sites. Treat it as a wire *(box item 13: add to `owners.yaml: wires` after verifying)*.
- **VP-3.7 Aggregators never count.** Pages on Yahoo News, MSN, Apple News, Google News and similar sites are tier 4. Follow them to the original publisher and record that instead.

### 3.3 Press-release echo detection

An **echo** is an article whose information comes entirely from someone else's release or statement.

- **VP-3.8 Echo test.** An article is an echo of a release (or an official post) when **both** of these are true:
  1. every fact it states about the claim is also in the release; and
  2. it names no source for those facts other than the release's issuer ("deputies said in a news release", "according to a statement").

  Shared wording, the same quotes in the same order, or publication within minutes of the release are supporting signs. They are not required.
- **VP-3.9 Partial echoes.** An article that rewrites a release **but adds its own confirmation** is independent *for the added facts only*. Examples of added confirmation: "court records reviewed by The State show…", "a WIS crew at the scene saw…", a second named on-record source. Judge this claim by claim.
- **VP-3.10 Counting echoes.** The release is one source: its own issuer group, tier 1 if published on the official channel, `kind=press_release`. **All** echoes of it together are **one** more source. Record the earliest tier ≤2 echo with `role=echo`, `echo_of=<release url>` and `also=<the other echo outlets>`, and do **not** add separate entries for the others.

  **Five outlets rewriting one press release = 1 source + the release.** We give the echo cluster one count because a newsroom running a release under its own name is vouching that the release is real. It is not a second investigation.
- **VP-3.11 "Citing reports" chains.** Outlets that credit another outlet's report ("as first reported by the Los Angeles Times") are **not** an echo cluster that earns a count. They collapse into the original outlet completely, adding zero.
- **VP-3.12 Statements given to a wire.** "The family told the AP" repeated by twenty outlets is **one** source: the AP.

### 3.4 Tracing to the original

- **VP-3.13 Follow the chain.** Follow every "according to", "citing", "first reported by", "told" or link until you reach one of these:
  - a primary document or official channel;
  - a named, on-record source quoted directly by the reporting outlet;
  - the first published report.

  Record it with `role=original`.
- **VP-3.14 When `traced_to_original` is true.** Set `traced_to_original: true` only when that original is in `evidence` **and was read**. If the chain dead-ends (an anonymous source, a deleted post, an unreadable page), set it to `false` and say why in the note. If the original is tier 4 (a viral post, for example), you have still traced it. Set `true`, record it as not counted, and put it in `origin=`.
- **VP-3.15 Archive work.** For archive and cold-case episodes, trace anecdotes to their **earliest published instance**. Five books repeating one 1950s gossip column are one source plus the column (section 9, "History myths").

### 3.5 The counting rule

**VP-3.16.** These are the exact definitions the engine uses to recompute `independent_count` and `has_official` from your evidence. Write your evidence so that this recomputation gives the right answer.

```python
counted           = [e for e in evidence if e.supports and e.tier <= 3]
independent_count = len({e.owner_group for e in counted})      # schemas.py: "distinct owner groups, syndication collapsed, tier<=3"
has_official      = any(e.tier == 1 for e in counted)            # schemas.py: "at least one tier-1 primary source supports it"
t2_groups         = len({e.owner_group for e in counted if e.tier <= 2})   # reported in note; see box item 1
```

This only works if you follow **one entry per independent origin** (VP-3.5, VP-3.10, VP-3.11). The counting rule never collapses anything on its own. Echoes and syndicated copies are collapsed by how you write the evidence.

### Worked example: Columbia, one release, five outlets

The Richland County Sheriff's Department posts a release about an arrest. Within an hour, The State, WIS, WLTX, The Post and Courier and Free Times each run it, adding nothing.

| Count it as… | Result | Why |
|---|---|---|
| Logos | 6 | Wrong: it counts websites |
| Owner groups | 5 (RCSD, McClatchy, Gray, TEGNA, Evening Post ×2) | Still wrong: these are echoes |
| **This protocol** | **2**, `has_official: true` | The release, plus one echo cluster (VP-3.10) |

The gate's verdict depends on the lane:

- **Standard** (Columbia Daily): passes, because an official record is enough.
- **Strict**: passes, because there is an official record.
- **Breaking**: `2 < 3`, so V3 fires and the story is **held**.

Suppose WIS later reports that the county jail's online booking record shows the arrest. That booking record is a separate official record from a different body. The count becomes 3 and the breaking lane can clear.

---

## 4. Recency windows

**In plain language.** Something true yesterday may not be true this morning. A source has to be fresh enough for the kind of claim it's backing up. Fires grow, people are released, charges are dropped, numbers get revised. A stale source doesn't count. It is recorded and marked "stale".

| Claim kind | Evidence must be published or updated within… | Lanes |
|---|---|---|
| **Live status**: containment, evacuations, closures, in custody / at large, casualty counts | **60 min** before each gate check (breaking); **12 h** before render (daily) | breaking, standard |
| **New event facts**: what happened | Published **after the event**, and within **72 h** of air for daily shows | standard, breaking |
| **Legal status**: charges, plea, verdict, sentence, next hearing, case status | Docket or primary record checked within **24 h** of render | all lanes |
| **Official statistics**: unemployment, crime figures, budgets | The **latest release** in that series. An older release is stale even if it's recent. | all |
| **Titles and offices**: who holds which job | A source within **30 days**, or the official roster | all |
| **Present tense in evergreen episodes**: "still unsolved", "remains at large", "still standing" | A fresh search within **7 days** of publish | strict (Cold Case Files), archive |
| **Historical facts** | No window. Prefer contemporaneous records. A later correction or official finding wins. | archive, strict |
| **Weather and hazard alerts** | The issuing agency's product is **active at render time** | all |

### Rules

- **VP-4.1 Dates on every entry.** Every evidence entry records `published=` (ISO-8601 UTC, or `unknown`) and, if the source shows one, `updated=`. A source dated `unknown` can't support a live-status claim or a breaking-lane claim.
- **VP-4.2 Stale sources.** Record a stale source with `supports: false` and `role=not_counted:stale`. If the claim's **only** support is stale, flag `STALE_ONLY`. The status is then `unsupported` (V2), or `contradicted` (V1) if newer evidence says otherwise.
- **VP-4.3 Which source wins.** Within a tier, the newest wins. Tier 1 beats tier 2 whatever the timing, unless the tier-2 source is reporting a **newer official update**. In that case, find and cite the update itself.
- **VP-4.4 Breaking event window.** On the breaking lane, only sources published at or after the event's start time (taken from the earliest credible report) count. If the earliest report of "this event" is more than 24 hours older than the claimed event time, flag `RECYCLED` (section 9).
- **VP-4.5 What the window means for the gate.** The gate can't see dates yet (box item 4). The window is enforced through `supports` and `status`, so it reaches the gate as V1, V2 or V3.

---

## 5. What counts as official confirmation, beat by beat

**In plain language.** "Official" means the organization that actually holds the record said so, on a channel it controls. A reporter's tweet that "police tell me…" is good reporting, but it is that reporter's tier, not the police record. Only a tier-1 source sets `has_official`.

| Beat (from `shows.yaml`) | Official confirmation (tier 1) | Not official confirmation |
|---|---|---|
| **Police and public safety** (`public_safety`, `da_press`, `attack_or_attempt`) | The agency's own release, alert or verified post; booking record; prosecutor's charging announcement; a federal agency's statement on federal cases | Scanner traffic; witness posts; union statements; a reporter's "police tell me" (tier 2, attributed) |
| **Courts** (`criminal_court`, `civil_court`, `federal_court`, `scotus`, `tracked_cases`, `cold_case`) | Docket entry, filed document, minute order, judgment, opinion, order; court public-information officer; prosecutor's on-record statement about charges | Either side's lawyer (a party, so attribute it); a defendant's social posts; courtroom-watcher accounts |
| **Government** (`government`, `education`, `housing`, `transit`, `development`, `federal_government`) | Agenda, minutes, roll-call record, official meeting video; bill text and status from the legislature; signed order or law; agency release; results from the election authority | Campaign statements; one member's post about how a vote went; leaked drafts (attribute them, never state as fact) |
| **Sports** (`sports`, `sports_mega`) | League or team announcement; official injury report; official box score or stats feed; league discipline release | "Per sources" insider reports (attribute them); fan accounts; betting lines |
| **Companies** (`business`, `entertainment_business`, `business_mega`) | SEC filing (8-K, 10-Q…); company newsroom or investor-relations release; WARN notice; on-record spokesperson statement published by the company | Analyst notes; "people familiar with"; a stock move as proof that something happened; employees' personal posts |
| **Weather and disaster** (`weather`, `disaster`) | NWS and National Hurricane Center products; USGS event pages; CAL FIRE or agency incident pages; emergency-management orders | Weather-influencer posts; app alerts that don't name the issuing agency |
| **Space** (`space`) | NASA, other space agencies, and the launch provider's official channels | Launch-watcher accounts |
| **World** (`world`) | That government's official channels; UN agencies | State-run media as independent confirmation (VP-2.8) |
| **Elections** (risk flag `election`) | The election authority's results and certification. Race calls are attributed: "the AP has called…" | A candidate's claim of victory |
| **Deaths** (`major_death`, flag `death`) | See 5.1 below | |

**Legal-status words are not interchangeable.** *Detained* is not *arrested*, which is not *charged*, which is not *convicted*. Each stage needs its own record. The Verifier marks a mismatch as `contradicted` (VP-1.14).

### 5.1 Deaths

**In plain language.** Reporting that someone has died is the claim we most need to get right. A family deserves to hear it from people who love them, not from a synthetic anchor working off a trending hashtag. We'd rather be second and right.

**A "major figure"** is a named person whose death national outlets would report: current or former officeholders, entertainers, athletes, and business and cultural leaders. It also includes any named person in a Breaking Desk `major_death` story.

- **VP-5.1 What counts as support for a death.** For a death claim about a named person, only these count:
  1. a **tier-1 statement** from the family, a representative (publicist, agent, attorney, estate, management), the organization the person led or played for, a coroner or medical examiner, police, or a government office; or
  2. a **tier ≤2 outlet that explicitly attributes** the death to one of those parties (`cites=<who>` in the note), or that got its own on-record confirmation from one ("the publicist confirmed to Reuters").

  Anything else is recorded with `supports: false` and `role=not_counted:unattributed_death`.
- **VP-5.2 The network standard, all lanes.** A major-figure death needs **either** (a) the family's, representative's or official's statement itself, **or** (b) **three** independent tier ≤2 outlets each citing such a statement, counted **after** wire and echo collapse. Twenty outlets repeating "the family told the AP" is one (VP-3.12).

  Record the count in the finding note as `cited_statement=<n>` and flag `DEATH_STATEMENT_CITED`. The lane thresholds in section 6 still apply on top of this.
- **VP-5.3 What never counts.** Social media tributes; trending topics; Wikipedia edits; condolence posts from other public figures (unless that person is the official source, such as a governor announcing a state official's death); a single outlet; "sources say"; tier 3 or tier 4 sources on their own.
- **VP-5.4 Mandatory checks for hoaxes.** Every death claim gets at least one search for "<name> alive", "<name> death hoax" or "<representative> denies".
- **VP-5.5 Not the same as dead.** "Hospitalized", "critical condition" and "unresponsive" are not death. "Reportedly died" is never voiced as fact.
- **VP-5.6 Private individuals** (for example, crime or accident victims). Only a coroner, medical examiner or police counts. Record whether next of kin has been notified (`nok=notified` or `nok=unknown`). Whether a victim is named is the Legal Screener's call (`naming_victim` is a hard stop, rule L2).

---

## 6. How much is enough: lanes, breaking thresholds and HOLD

**In plain language.** Each show runs in a "lane" that sets how strict the gate is.

- **Standard** (daily briefs): two independent sources or one official record. A low-risk fact with one solid source can air if the host says where it came from ("according to WIS").
- **Strict** (courts, case tracking, cold cases): no single-source shortcut, and anything about crime, allegations, victims or legal status needs an official record.
- **Breaking**: three independent sources. An official statement alone isn't enough, because official accounts get hacked. Anything sensitive also needs an official record. If the only problem is "not enough sources yet", we wait 15 minutes and look again, up to six times.
- **Archive** (history): same as standard.

### 6.1 Lane policies exactly as coded (`POLICIES` in `gate.py`)

| `LanePolicy` field | `standard` | `strict` | `breaking` | `archive` |
|---|---|---|---|---|
| `min_independent` | 2 | 2 | **3** | 2 |
| `official_satisfies` | True | True | **False** | True |
| `allow_attributed_single` | True | False | False | True |
| `sensitive_needs_official` | False | True | True | False |
| `max_rewrites` | 2 | 2 | 1 | 2 |
| `max_holds` / `hold_minutes` | 0 / – | 0 / – | **6 / 15** | 0 / – |
| `min_balance` *(Bias Checker)* | 70 | 75 | 70 | 65 |
| `legal_block_severity` *(Legal Screener)* | high | medium | medium | high |
| **Shows** (`shows.yaml`) | Columbia Daily, LA Daily (NYC Daily, Chicago Daily in wave 1) | LA Courts Roundup, Case Tracker, Cold Case Files | The Breaking Desk | History of Hollywood |

**The pass test the gate applies to each must-check claim** (from `_corroborated` and `decide`):

```
contradicted → V1        unsupported → V2        no finding → V0
ok = (status == corroborated and independent_count >= min_independent)
  or (official_satisfies and has_official and status in {corroborated, single_source})
  or (allow_attributed_single and not sensitive and claim.attributed and status == single_source)
not ok                                                     → V3 (threshold)
ok and sensitive and sensitive_needs_official and not has_official → V4 (threshold)
```

**The decision order:**

1. **PUBLISH** if nothing blocks.
2. **KILL** if a hard stop fired.
3. **HOLD** if the lane is breaking, *every* block is V3 or V4, and `holds_used < 6`.
4. **REWRITE** if `revision < max_rewrites`.
5. Otherwise **KILL**.

### 6.2 Breaking: detection threshold and publish threshold

There are two different moments on the breaking lane, and they use different thresholds:

| Moment | Who | Threshold |
|---|---|---|
| **Trigger:** should the Breaking Desk start a flash? | Breaking detector, `desk/breaking.py` (`next`) | The event class is on The Breaking Desk's beat list, **and either** ≥3 independent tier ≤2 outlets, **or** an official confirmation plus ≥1 independent tier ≤2 outlet. Velocity (outlets per hour) is used for ranking only and is never verification. |
| **Publish:** can this script air? | Standards Editor gate (`built`) | Every must-check claim: `corroborated` with `independent_count ≥ 3`; an official source alone is not enough; no single-source shortcut; sensitive claims also need `has_official`. |

**The standard** for publishing a breaking claim is **3 independent tier ≤2 sources, or an official source plus 1 independent tier ≤2 source.** The gate today is looser on tier (it counts tier 3) and stricter on "official + 1" (it wants 3). Both are in the box (items 1 and 2).

**VP-6.1 Report tier-2 groups.** On the breaking lane, every finding note includes `t2_groups=<n>`, the count of tier 1–2 owner groups, so the stricter tier rule can be enforced as soon as the gate reads it.

### 6.3 HOLD and recheck schedule (breaking lane only)

The schedule below follows `decide(..., holds_used=n)`. Here "short" means that every blocking reason is V3 or V4.

| Check | Minutes after first check | `holds_used` passed in | If still short… |
|---|---|---|---|
| 1 | 0 | 0 | HOLD, `recheck_after_minutes: 15` |
| 2 | 15 | 1 | HOLD |
| 3 | 30 | 2 | HOLD |
| 4 | 45 | 3 | HOLD |
| 5 | 60 | 4 | HOLD |
| 6 | 75 | 5 | HOLD |
| 7 | 90 | 6 | **REWRITE**: the Producer cuts what isn't confirmed (revision 0 → 1) |
| 8 | after the rewrite | 6 | PUBLISH if clean, otherwise **KILL** |

Any **other** blocking rule (V0, V1, V2, F, B, L or S1) skips HOLD and goes straight to REWRITE or KILL. If an official denial turns up during a hold, the claim becomes `contradicted` (V1) and the hold ends.

### 6.4 What the Verifier does on each recheck

- **VP-6.2 Fresh search, for held claims only.** Each recheck re-runs the blind search for the claims blocked by V3 or V4 only, using the recheck ceiling (section 7). The pipeline must call the Verifier again. It must never reuse the previous report (box item 11).
- **VP-6.3 Re-read what you already counted.** Re-read every source you counted last time. If it was corrected, retracted, deleted or materially changed, record it with `supports: false` and `role=not_counted:retracted`, and flag `RETRACTED`. Sources that still check out carry forward with their `updated=` refreshed.
- **VP-6.4 Live status expires.** Live-status claims must be re-confirmed at **every** check, inside the 60-minute window (section 4).

---

## 7. Search budget

**In plain language.** Searching costs money and time. Each claim gets a limit, the riskiest claims are checked first, and one good search can back up several claims. If we run out before a claim is confirmed, that claim doesn't air. We never call something confirmed because we stopped looking.

One **search** is one web-search call. Reading a result you already have is not a search.

| Lane | Per-claim ceiling (first pass) | Per-claim ceiling (each HOLD recheck) | Script cap (`max_searches`) |
|---|---|---|---|
| standard | 3 (5 if sensitive, or a number or quote in the lead story) | – | 20 *(code default)* |
| strict | 5 | – | 30 *(passed by pipeline, box item 10)* |
| breaking | 5 | 2 | 20 per pass |
| archive | 5 | – | 30 *(passed by pipeline)* |

### Rules

- **VP-7.1 Charging searches.** A search is charged to the first claim that needed it. Its results may back up any number of other claims, and those claims are not charged.
- **VP-7.2 Spend in priority order.** Spend in the VP-1.5 order. The try-to-prove-it-wrong search (VP-1.9) comes out of the claim's own ceiling, so reserve one for it.
- **VP-7.3 Running out.** If a claim hits its ceiling, or the script hits its cap, report the status you **actually** have (`single_source` if you found one counted source, `unsupported` if you found none) and flag `BUDGET_EXHAUSTED`. Never leave the finding out, because a missing finding fires V0. On the breaking lane, a `single_source` result still leads to a HOLD (V3), which gets a fresh budget.
- **VP-7.4 Logging searches.** Put `searches=<n>` in each finding note. The engine fills `VerifierReport.searches_used` from the run log (`AgentRun.web_searches`).

---

## 8. The evidence JSON

**In plain language.** Everything the Verifier finds goes into a fixed format, so the gate can apply its rules, the Fact Checker can read it, and the public trust log can show its work. Everything the Verifier counted has a link, an outlet, an owner and a tier, and a short reason written in our own words.

### 8.1 The contract

The Verifier's structured output must match `JSON_SCHEMAS["VerifierReport"]` exactly: every field is required and no extra fields are allowed. The engine adds `script_id` and `searches_used` to build the `VerifierReport` dataclass.

```text
VerifierReport.findings[]   (one per must-check claim, VP-1.3)
  claim_id            string   the script's claim id
  status              enum     corroborated | single_source | unsupported | contradicted   (VP-1.13)
  independent_count   int      VP-3.16
  has_official        bool     VP-3.16
  traced_to_original  bool     VP-3.14
  evidence[]
    url               string   a page you actually retrieved this run (VP-8.2)
    outlet            string   publishing organization; the wire for wire copy; the issuing body for officials
    tier              int      1-4 (section 2)
    owner_group       string   owners.yaml group; the wire; the issuing body; else the outlet name
    supports          bool     true = counts as support under this protocol (VP-8.3)
    note              string   summary + [tokens]  (VP-8.4)
  note                string   summary + [tokens]  (VP-8.5)
```

### 8.2 Field rules

- **VP-8.1 Fields agree with the evidence.** `independent_count`, `has_official` and `status` must agree with `evidence` under VP-3.16 and VP-1.13. The engine recomputes the count, so a mismatch is a bug in your report, not a judgment call.
- **VP-8.2 No invented links.** Every `url` must be a page returned or opened during **this** run. Never build, guess or "remember" a URL (box item 7). Link to the original, not a reprint (VP-3.5).
- **VP-8.3 What `supports` means.** `supports: true` means the source states the claim as worded, on its own authority or through attribution this protocol accepts, inside the recency window, and it is not a duplicate of another entry. `supports: false` covers two cases: a **contradiction** (`role=contradicts`), or a relevant source **not counted** (`role=not_counted:<reason>`). Always include contradictions. Include not-counted sources when they explain the outcome (the viral post, the stale report, the satire piece).
- **VP-8.4 The evidence note.** One or two sentences in **our own words** (at most 280 characters) that never copy article text, then one bracketed block of tokens. For quote claims, you may include the exact quoted words (at most 40), in double quotes.

  | Token | Required | Values |
  |---|---|---|
  | `role` | yes | `original`, `independent`, `echo`, `contradicts`, `not_counted:<reason>`. Reasons: `tier4`, `stale`, `satire`, `fabricated`, `lookalike`, `image_only`, `viral`, `retracted`, `anonymous`, `aggregator`, `unattributed_death`, `hacked`, `unreadable`, `duplicate` |
  | `kind` | yes | one of `SOURCE_KINDS`: `article`, `press_release`, `court_record`, `official_data`, `archive`, `broadcast`, `social`, `other` |
  | `published` | yes | ISO-8601 UTC, or `unknown` |
  | `updated` | if shown | ISO-8601 UTC |
  | `echo_of` | when `role=echo` | URL of the release or post being echoed |
  | `also` | optional | the other outlets collapsed into this entry |
  | `via` | wire copy | the republishing outlet |
  | `cites` | optional; required for death claims | who the source attributes the fact to |
  | `anon` | optional | `yes` if the source relies on anonymous sourcing |
  | `nok` | private-person deaths | `notified` or `unknown` |

- **VP-8.5 The finding note.** A plain summary first, because on V1 the gate passes this note to the Producer **word for word**. When the claim is wrong, state the correct fact. Then one bracketed block:

  | Token | Required | Values |
  |---|---|---|
  | `flags` | yes | comma-separated flags from the table below, or `none` |
  | `basis` | yes | `official`, `official+<n>`, `independent:<n>`, `none` |
  | `origin` | yes | URL of the original (VP-3.13), or `unknown` |
  | `searches` | yes | searches charged to this claim |
  | `t2_groups` | breaking lane | VP-6.1 |
  | `cited_statement` | death claims | VP-5.2 |

**Flags**

| Flag | Meaning | Usual status, then gate rule |
|---|---|---|
| `ECHO_COLLAPSED` | Echoes of a release collapsed into one entry (VP-3.10) | any (informational) |
| `SYNDICATION_COLLAPSED` | Wire or partner copy collapsed (VP-3.4, VP-3.5) | any |
| `CONFLICT` | Tier ≤2 sources disagree with no resolution | contradicted, V1 |
| `STALE_ONLY` | All support is outside the recency window | unsupported, V2 |
| `RECYCLED` | An old story presented as new | contradicted, V1 (or unsupported, V2) |
| `SATIRE` | The claim started at a satire source | unsupported, V2 |
| `FABRICATION_SUSPECTED` | Signs of fake or AI-generated news | unsupported, V2 |
| `LOOKALIKE_DOMAIN` | Fake "official" site or account | unsupported, V2 |
| `IMAGE_ONLY` | Only an image or video, with no text record | unsupported, V2 |
| `VIRAL_UNCONFIRMED` | Spreading socially, no counted source | unsupported, V2 (V3 if one source) |
| `HACK_SUSPECTED` | An official channel may be compromised | not counted. Usually V3 |
| `RETRACTED` | A counted source was corrected, retracted or deleted | recomputed |
| `ANON_ONLY` | Every counted source relies on anonymous sourcing | any (informational) |
| `BUDGET_EXHAUSTED` | Search ceiling or cap reached (VP-7.3) | whatever was found |
| `OWNER_UPDATE` | Ownership or partnership not in `owners.yaml` (VP-3.3) | any; routed to Industry Intel |
| `NEW_OUTLET` | Unlisted outlet promoted to tier 3 (VP-2.2) | any; routed to Industry Intel |
| `DEATH_STATEMENT_CITED` | Death confirmed through outlets citing a statement (VP-5.2) | any |

### 8.3 A complete example, and what the gate does with it

*Illustrative only. The fire, the URLs (`.example`) and the numbers are invented. The outlet names show how owner groups collapse.*

LA Daily (standard lane) reports on a brush fire in Sun Valley. The Producer's script makes four must-check claims:

- `clm_fire_acres`: "LAFD says the fire burned about 40 acres" (`number`, attributed)
- `clm_evac_lifted`: "The evacuation warning has been lifted" (`fact`, attributed)
- `clm_homes`: "Four homes were damaged" (`number`)
- `clm_video`: "Video shows flames jumping the freeway" (`fact`)

```json
{
  "findings": [
    {
      "claim_id": "clm_fire_acres", "status": "corroborated", "independent_count": 3,
      "has_official": true, "traced_to_original": true,
      "evidence": [
        {"url": "https://lafd.example/news/brush-fire-update-2", "outlet": "Los Angeles Fire Department",
         "tier": 1, "owner_group": "Los Angeles Fire Department", "supports": true,
         "note": "LAFD's second update puts the fire at about 40 acres. [role=original; kind=press_release; published=2026-10-11T11:40:00Z]"},
        {"url": "https://ktla.example/news/sun-valley-brush-fire", "outlet": "KTLA",
         "tier": 2, "owner_group": "Nexstar", "supports": true,
         "note": "Rewrite of the LAFD update with no added sourcing. [role=echo; kind=article; published=2026-10-11T12:05:00Z; echo_of=https://lafd.example/news/brush-fire-update-2; also=NBC4, ABC7 Los Angeles, CBS Los Angeles, Los Angeles Daily News]"},
        {"url": "https://latimes.example/california/sun-valley-fire", "outlet": "Los Angeles Times",
         "tier": 2, "owner_group": "LA Times", "supports": true,
         "note": "Times reporter on scene; a battalion chief confirmed about 40 acres on the record. [role=independent; kind=article; published=2026-10-11T12:30:00Z; cites=LAFD battalion chief]"}
      ],
      "note": "About 40 acres, confirmed by LAFD and by independent Times reporting. [flags=ECHO_COLLAPSED; basis=official+2; origin=https://lafd.example/news/brush-fire-update-2; searches=2]"
    },
    {
      "claim_id": "clm_evac_lifted", "status": "single_source", "independent_count": 1,
      "has_official": true, "traced_to_original": true,
      "evidence": [
        {"url": "https://lafd.example/alerts/evac-warning-lifted", "outlet": "Los Angeles Fire Department",
         "tier": 1, "owner_group": "Los Angeles Fire Department", "supports": true,
         "note": "Official alert lifting the evacuation warning. [role=original; kind=official_data; published=2026-10-11T12:50:00Z]"}
      ],
      "note": "Lifted per an LAFD alert issued 10 minutes before render. [flags=none; basis=official; origin=https://lafd.example/alerts/evac-warning-lifted; searches=1]"
    },
    {
      "claim_id": "clm_homes", "status": "contradicted", "independent_count": 1,
      "has_official": false, "traced_to_original": true,
      "evidence": [
        {"url": "https://lafd.example/news/brush-fire-update-2", "outlet": "Los Angeles Fire Department",
         "tier": 1, "owner_group": "Los Angeles Fire Department", "supports": false,
         "note": "LAFD says two structures were damaged, not four homes. [role=contradicts; kind=press_release; published=2026-10-11T11:40:00Z]"},
        {"url": "https://neighborhood-news.example/fire", "outlet": "neighborhood-news.example",
         "tier": 3, "owner_group": "neighborhood-news.example", "supports": true,
         "note": "Early post said four homes, written before LAFD's update. [role=independent; kind=article; published=2026-10-11T09:15:00Z]"}
      ],
      "note": "LAFD's latest update says two structures were damaged, not four homes. [flags=CONFLICT; basis=none; origin=https://lafd.example/news/brush-fire-update-2; searches=1]"
    },
    {
      "claim_id": "clm_video", "status": "unsupported", "independent_count": 0,
      "has_official": false, "traced_to_original": true,
      "evidence": [
        {"url": "https://social.example/post/88812", "outlet": "social.example",
         "tier": 4, "owner_group": "social.example", "supports": false,
         "note": "Unattributed clip; the earliest copy found is from a 2024 fire. [role=not_counted:image_only; kind=social; published=2024-09-02T00:00:00Z]"}
      ],
      "note": "The only source is a recycled video; no outlet or agency reports flames crossing the freeway. [flags=IMAGE_ONLY,RECYCLED; basis=none; origin=https://social.example/post/88812; searches=3]"
    }
  ]
}
```

Without collapsing, `clm_fire_acres` would look like **7** sources (LAFD + five echo outlets from five owner groups + the Times). Collapsed, it is **3**.

This JSON validates against `JSON_SCHEMAS["VerifierReport"]`. Run through `decide()` (standard lane, with the Fact Checker rating `clm_homes` inaccurate and `clm_video` unverifiable), the gate returns:

```text
decision: REWRITE
reasons:  V1 clm_homes, F1 clm_homes, V2 clm_video, F2 clm_video
rewrite_instructions[0]:
  Correct or remove clm_homes: "Four homes were damaged". Evidence: LAFD's latest update says two
  structures were damaged, not four homes. [flags=CONFLICT; basis=none; origin=https://lafd.example/news/brush-fire-update-2; searches=1]
```

`clm_fire_acres` passes on V3 (3 ≥ 2). `clm_evac_lifted` passes because `official_satisfies` is true and `has_official` is true.

---

## 9. Tricky cases

**In plain language.** Most bad information isn't a clever lie. It's a joke taken seriously, an old story recirculating, a photo without context, or something that spread before anyone checked. Here is how the Verifier handles each one.

**Satire sites.** Real satire outlets (The Onion, The Babylon Bee, and local equivalents) write convincing fake headlines, and screenshots of them circulate with the logo cropped off.
- **VP-9.1** Keep a satire denylist (`kind: satire`) in `config/sources/national.yaml` and in each market file.
- **VP-9.2** Search the exact headline. If its earliest instance is a satire site, record that entry as `not_counted:satire`, flag `SATIRE`, and set status `unsupported` (V2), unless real reporting independently supports the claim.

**AI-generated fake news and lookalike sites.** These are sites that look like local papers but have no staff, publish at inhuman volume, use templated text and AI-made author photos, have no corrections, and run stories that appear nowhere else. Some imitate official sites or accounts with a near-miss domain or handle.
- **VP-9.3** Unknown sites start at tier 4 (VP-2.2).
- **VP-9.4** A claim found **only** on such sites is flagged `FABRICATION_SUSPECTED` and is `unsupported`.
- **VP-9.5** A near-miss "official" domain or handle is recorded as `not_counted:lookalike` and flagged `LOOKALIKE_DOMAIN`.
- **VP-9.6** A quote attributed to an official counts only if it appears on the official's own channel or in a tier ≤2 outlet. AI-fabricated quotes are a known pattern.

**Recycled old stories.** A real story from years ago (a flood photo, a shark sighting, a celebrity arrest) resurfaces as if it were new.
- **VP-9.7** For every event claim, run one search with no date limit to find the **earliest instance**. Check the article date, the date in the URL path, and dated details in the text.
- **VP-9.8** If the event predates the claimed time, flag `RECYCLED`. If the script says or implies it is new ("today", "this morning"), set `contradicted` and put the real date in the note. If it doesn't, set `unsupported`.

**Image-only claims.** A photo, video or screenshot with no text record behind it. In May 2023, an AI-generated image of an "explosion" near the Pentagon spread from verified accounts until the local fire department said nothing had happened.
- **VP-9.9** An image or video on its own is tier 4, whoever posted it.
- **VP-9.10** It counts only through the reporting of a tier ≤2 outlet that says it verified the footage (where and when it was taken), or an official body that publishes it. Count that outlet or body at its own tier.
- **VP-9.11** We never report what a picture "shows" unless the underlying event is confirmed by text sources. Image-only claims are flagged `IMAGE_ONLY` and are `unsupported`.

**Viral posts.** Trending is not the same as true. Death hoaxes, "BREAKING" aggregator accounts and screenshots of supposed alerts all spread faster than corrections.
- **VP-9.12** How fast something spreads, how often it is shared, and verification badges never count toward verification. The breaking detector may use velocity to *notice* a story (section 6.2). The Verifier still needs counted sources.
- **VP-9.13** A claim with no counted source is flagged `VIRAL_UNCONFIRMED`: `unsupported`, or `single_source` if one counted source exists.

**Hacked or spoofed official accounts.** In April 2013, hackers took over the AP's Twitter account and posted a false report of explosions at the White House. Markets dipped before it was corrected. This is why the breaking lane sets `official_satisfies=False`.
- **VP-9.14** If an official post is out of character, contradicts the body's own website, or is soon deleted, flag `HACK_SUSPECTED` and record it as `not_counted:hacked`.

**Conflicting numbers.** Death tolls, acreage and crowd sizes change fast, and different sources report different figures.
- **VP-9.15** The latest official figure wins (VP-4.3).
- **VP-9.16** If the script's number doesn't match it, set `contradicted` and give the current figure, with its time, in the note ("as of 2:10 p.m., LAFD says…").
- **VP-9.17** If tier ≤2 sources disagree and there's no official figure, flag `CONFLICT`, so the writer can attribute each figure separately or cut the number.

**Updated, corrected or deleted stories.** Breaking stories get rewritten under the same URL.
- **VP-9.18** Re-read counted sources on every recheck (VP-6.3). After publication, `monitor/recheck.py` re-checks published claims for 7 days and opens a `Correction` when a claim fails.

**Anonymous sourcing.**
- **VP-9.19** A tier ≤2 outlet's anonymously sourced report counts as that outlet's reporting, marked `anon=yes`, **except** for deaths (VP-5.1), arrests or charges of a named person, and allegations. In those cases record it as `not_counted:anonymous`.
- **VP-9.20** If every counted source is anonymous, flag `ANON_ONLY`.

**History myths** (History of Hollywood, Cold Case Files). Famous anecdotes get repeated from book to book until they feel like fact.
- **VP-9.21** Trace each anecdote to its earliest published instance (VP-3.15). Books and articles that repeat one source collapse into that source.
- **VP-9.22** If the trail ends in gossip, a press agent's story or a later memoir, the claim can air only as attribution ("the studio's publicity department claimed…") or as legend. Its claim type must say so.

---

## 10. When things go wrong (automatic handling)

Nobody steps in by hand. Each failure has a built-in result, and every one of them fails safe: the claim is cut, or the episode doesn't air.

| Failure | What happens |
|---|---|
| Search tool down, or the Verifier times out | No findings. V0 fires on every must-check claim: REWRITE, then KILL. V0 is not a threshold reason, so the breaking lane does not HOLD. The pipeline may retry the Verifier once before the gate runs *(pipeline, `next`)*. |
| Invalid JSON | `validate("VerifierReport", ...)` fails, then `llm.research` runs one structured repair pass. If that also fails, the result is treated as no report (V0). |
| Some claims missed | V0 for those claims only. The REWRITE instruction is "drop or re-source". |
| A counted source disappears | On recheck it is recorded as `not_counted:retracted` with the flag `RETRACTED`, and the count is recomputed. After publication, the 7-day recheck opens a `Correction` (`note`, `reissue` or `retract`). |
| An unknown outlet | Treated as its own group, starting at tier 4. Flagged `NEW_OUTLET` or `OWNER_UPDATE` for Industry Intel. |
| The writer and the Verifier fall for the same wrong wire story | Reduced by searching the primary source first (VP-1.7), the try-to-prove-it-wrong search (VP-1.9) and the 7-day recheck. The correction is logged publicly. |
| Budget runs out | VP-7.3: the claim gets the status that was actually found and the flag `BUDGET_EXHAUSTED`. It is never left out. |

---

## 11. How we measure it, and what listeners can see

**Measures.** These are tracked per show, per week, from gate `scores` and the run log:

- `corroboration_rate` (from the gate);
- share of claims with `traced_to_original: true`;
- share of strict-lane sensitive claims with `has_official: true`;
- searches per claim;
- V0 rate (target: zero);
- HOLD-to-PUBLISH conversion and median time to confirm;
- corrections per 100 published claims (Monitor).

**What listeners can see.** Show notes list our sources and summarize how they were verified (`publish/notes.py`). Every gate decision goes to the public trust log (`publish/trustlog.py`). Corrections are posted against the episode. The AI disclosure is spoken at the end of every episode and carried in the feed metadata.

---

> [!WARNING]
> ### Not yet enforced in code
>
> These standards are not yet fully enforced by `earlobe/trust/gate.py`, or by the engine modules that are still `next`. **"Looser"** means the code can currently publish something this protocol would not. **"Stricter"** means the code holds or kills something this protocol would allow. That is safe, but it costs us stories. Each fix touches `schemas.py`, `gate.py` and `docs/blueprint/json-contracts.md` together (CONVENTIONS rule 8).
>
> | # | Standard | Code today | Direction | Proposed fix |
> |---|---|---|---|---|
> | 1 | Breaking counts **tier ≤2 only** toward 3 (§6.2) | `independent_count` counts tier ≤3; the gate can't see tiers | **Looser.** Two tier-2 sources plus one tier-3 source can publish. Partly limited by the detector's tier ≤2 trigger and by V4 (official record required) for sensitive claims. | Add `LanePolicy.max_count_tier` (breaking = 2), and have the gate recount from `evidence`. Meanwhile, the Verifier reports `t2_groups=` (VP-6.1). |
> | 2 | Breaking: **official + 1** independent tier ≤2 source is enough (§6.2) | `official_satisfies=False`, `min_independent=3` | **Stricter.** Holds until a third group appears, or kills at 90 min. | Add `LanePolicy.official_plus=1` for breaking: pass if `has_official` and there is ≥1 non-official tier ≤2 group. |
> | 3 | Named-person death: **statement, or 3 tier ≤2 outlets citing one**, on all lanes (VP-5.2) | Standard and archive: 2 independent sources or an official record. Strict and breaking: V4 requires a tier-1 statement, with no "3 citing" path. | **Looser** on standard and archive (2 sources, not 3). **Stricter** on breaking: if the family's statement is only published via a wire, the story can be lost. | New rule **V6** (proposed): a claim with the `death` flag needs `has_official` or `cited_statement ≥ 3`. Add a `cited_statement_count` field to `VerifierFinding`, and let it satisfy V4 for deaths. |
> | 4 | Recency windows (§4) | `EvidenceSource` has no `published_at`, so the gate can't check dates | Relies on the Verifier | Add `EvidenceSource.published_at`. `trust/verifier.py` checks the windows. |
> | 5 | Echo and syndication collapse (§3.2, §3.3) | `EvidenceSource` has no `derived_from` or `syndicated_from` field. Collapse depends on the Verifier writing one entry per origin. | Relies on the Verifier | Add `EvidenceSource.derived_from`, and have `desk/independence.py` collapse on it. |
> | 6 | `has_official` and `status` must agree with the evidence (VP-8.1) | The gate trusts the flags it is given | Relies on the Verifier | `trust/verifier.py` recomputes `has_official` and downgrades `status` when the evidence doesn't back it. |
> | 7 | No invented URLs (VP-8.2) | Not checked | Relies on the Verifier | `trust/verifier.py` drops evidence whose `url` isn't in this run's search or fetch log, then recomputes. |
> | 8 | Tracing to the original (§3.4) | `traced_to_original` is recorded but never read by the gate | Looser | Proposed: the strict lane requires `traced_to_original` for `allegation` and `legal_status` claims (a threshold reason, like V3). |
> | 9 | Contradicted background facts must not air (VP-1.4) | V1 fires only for `NEEDS_CORROBORATION` types. A contradicted `context` claim publishes unless the Fact Checker gives it F1. | Looser | Apply V1 to every claim type. |
> | 10 | Per-claim ceilings and per-lane caps (§7) | Only `verify(..., max_searches=20)` per script | Relies on the Verifier | The pipeline passes the per-lane caps, and `trust/verifier.py` enforces the per-claim ceilings. |
> | 11 | Each HOLD recheck re-runs the Verifier and re-reads counted sources (§6.4) | `decide()` takes `holds_used`. Re-running is the pipeline's job (`pipeline.py`, `next`). | Not yet built | `run_breaking` must call `verify` again on every recheck and never reuse the old report. |
> | 12 | Blindness (VP-1.1) | Not built yet (`trust/verifier.py`, `next`) | Not yet built | A unit test asserting that no URL or id from `Script.sources` or `Story.source_ids` reaches the Verifier's input. |
> | 13 | Merge when in doubt; City News Service counts as a wire; trade-press ownership (VP-3.3, VP-3.6) | `owners.yaml` treats unknown outlets as their own group, and its wires list has no City News Service | Looser | Industry Intel verifies these and updates `owners.yaml`. The `OWNER_UPDATE` and `NEW_OUTLET` flags feed its queue. |

---

## Change control

- This document, `earlobe/trust/gate.py` and `earlobe/schemas.py` change **together**. If a rule ID, lane field or enum changes in code, update the matching section here in the same change, and move any item that the code now enforces out of the box.
- Owner and tier data live in `config/owners.yaml` and `config/sources/<market>.yaml`, not in this document. The examples here are seeds.
- Model tiers are named only as Opus tier, Sonnet tier and Haiku tier (CONVENTIONS rule 4). No model IDs appear in this document.
