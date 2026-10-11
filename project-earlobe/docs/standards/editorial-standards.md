# Editorial Standards

**The Curious & Creative Network — the master rulebook**

| | |
|---|---|
| **Publisher** | Curious & Creative LLC |
| **Applies to** | Every show on the network: Columbia Daily, LA Daily, The Breaking Desk, LA Courts Roundup, Case Tracker, Cold Case Files, History of Hollywood, and every city show we add later |
| **Enforced by** | The Trust Stack: Source Verifier, Fact Checker, Bias Checker and Legal Screener report to the **Standards Editor**, a deterministic publish gate ([`earlobe/trust/gate.py`](../../earlobe/trust/gate.py)) |
| **Contracts** | [`earlobe/schemas.py`](../../earlobe/schemas.py) · lane per show: [`config/shows.yaml`](../../config/shows.yaml) · owner groups: [`config/owners.yaml`](../../config/owners.yaml) · voices: [`config/voices.yaml`](../../config/voices.yaml) |
| **Version** | 1.0, October 11, 2026 |

> **How to read this page.** Each section opens with a plain-language explanation for listeners and for
> the people who run the company. Below that are the **rules**: numbered, testable instructions the
> agents follow. Each rule names the gate check that enforces it (`V3`, `L2` and so on; the full
> list is in [§16](#16-gate-rule-map)). A rule that the code can't check yet is marked
> **not yet in code** and listed in the [Not yet enforced in code](#17-not-yet-enforced-in-code) box. We'd
> rather show you the gap than pretend it isn't there. Example sentences in quotes are made up to show
> phrasing. They aren't news reports.

---

## 1. Our mission and our promises to you

The Curious & Creative Network makes local news, court coverage, true crime and history for your ears.
Software writes and voices our shows, and software checks them. **No person reads each episode before
it airs.** We built it that way on purpose, and it's why this page matters so much. When nobody reviews
the work by hand, the rules have to be clear, they have to be strict, and they have to run every
single time.

Our founder learned the first rule in journalism school: **you have to see it in two or three
places.** That rule is now code. Before a fact can air, our system has to find it in at least two
sources owned by different companies. For breaking news, it has to find it in three.

**Our promises**

1. **We'll tell you how we know.** Every episode's show notes list and link its sources.
2. **Two places, minimum. Three for breaking news.** If a fact can't clear that bar, we leave it out.
3. **We'll tell you we're AI, every time.** Every episode ends with a spoken AI disclosure, and the
   same disclosure is in the episode's details.
4. **We'll never fake a voice, a quote or a source.** Our hosts are original synthetic voices. Every
   quote is real, word for word, and credited to the person who said it.
5. **We'll be fair, most of all to people who can't answer back:** people accused of crimes,
   victims and their families.
6. **We'll say when we're wrong, publicly.** Corrections are dated, visible and never silent.
7. **We'd rather be late, or skip a day, than be wrong.** Missing an episode is acceptable.
   Publishing a wrong one is not.

---

## 2. How an episode gets made

1. **Sensors** watch news feeds, court dockets and public records.
2. **The Story Desk** groups those into stories and assigns them to shows.
3. **The Producer** writes a script. Every checkable statement in the script is logged as a **claim**,
   tagged with its type (fact, number, quote, allegation…) and its risks (crime, minor, death…).
4. **The Trust Stack** checks the script. The **Source Verifier** works *blind*: it never sees the
   writer's sources and has to find its own. The **Fact Checker** rates each claim. The **Bias
   Checker** scores balance and flags slanted lines. The **Legal Screener** flags legal risks.
5. **The Standards Editor** (the gate) reads those four reports and applies fixed rules. It isn't an AI
   model. It's ordinary code, so the same inputs always produce the same decision. It returns one of four
   decisions:

| Decision | What it means |
|---|---|
| **PUBLISH** | Nothing blocking. The episode goes to the studio and then to your feed. |
| **REWRITE** | Fixable problems. The Producer gets exact fix instructions and tries again, within a fixed budget. |
| **HOLD** | Breaking news only. The story looks real but isn't confirmed by enough sources yet. Wait 15 minutes, then check again. |
| **KILL** | Still blocked after the rewrite budget runs out. The episode does not air. |

### Lanes: one rulebook, four strictness settings

Each show runs in a **lane** (`config/shows.yaml`). The lane sets how much proof the gate demands.
These values come straight from `POLICIES` in `gate.py`:

| Setting | `standard` | `strict` | `breaking` | `archive` |
|---|---|---|---|---|
| **Shows** | Columbia Daily, LA Daily (and future city dailies) | LA Courts Roundup, Case Tracker, Cold Case Files | The Breaking Desk | History of Hollywood |
| Independent sources needed (`min_independent`) | 2 | 2 | **3** | 2 |
| One official record is enough on its own (`official_satisfies`) | yes | yes | **no** | yes |
| One source is OK if said on air, low-risk claims only (`allow_attributed_single`) | yes | **no** | **no** | yes |
| Sensitive claims also need an official record (`sensitive_needs_official`) | no | **yes** | **yes** | no |
| Minimum balance score (`min_balance`) | 70 | **75** | 70 | 65 |
| Legal issues that block (`legal_block_severity`) | high | **medium and up** | **medium and up** | high |
| Rewrites allowed (`max_rewrites`) | 2 | 2 | 1 | 2 |
| Holds allowed (`max_holds` × `hold_minutes`) | 0 | 0 | **6 × 15 min** | 0 |

**Why the lanes differ.** Court and crime shows put real people's names next to accusations, so they
get the strict lane. Breaking news is when early reports are most often wrong, so it needs three
sources, and an official statement alone isn't enough, because first official numbers change too.
History is told from records that are decades old and rarely has two live "sides," so the archive
lane allows a little more narrative voice.

### Words this page uses exactly

- **Claims that need corroboration**: claim types `fact`, `number`, `quote`, `attribution`,
  `allegation`, `legal_status` (`NEEDS_CORROBORATION` in `gate.py`).
- **Sensitive claim**: type `allegation` or `legal_status`, **or** any of the risk flags `crime`,
  `legal_proceeding`, `named_private_person`, `minor`, `victim`, `death` (`SENSITIVE_TYPES`,
  `SENSITIVE_FLAGS`).
- **Independent sources**: sources from **distinct owner groups** (see §3), with wire copy collapsed
  and tier 4 excluded. This is the Verifier's `independent_count`.
- **Official record**: at least one **tier 1** source supports the claim (`has_official`).
- **Attributed**: the script says on air who is making the claim (`Claim.attributed = true`).

---

## 3. Sourcing

**In plain words.** A fact is ready to air when we've seen it in at least two places that don't
share an owner. If two TV stations belong to the same parent company, they count as one source. If
ten newspapers print the same Associated Press story, that's one source: AP. Court filings,
government releases and original data are the strongest sources we have, because they're the
original record, not someone's account of it. Blog posts, aggregators and social media posts never
count toward the bar on their own.

**Source tiers** (from `SOURCE_TIERS` in `schemas.py`):

| Tier | What it is | Counts toward "two places"? |
|---|---|---|
| **1** | Primary/official record: court filing, government release, original data, on-record statement | Yes, and in most lanes one tier-1 record can carry a claim alone |
| **2** | Wire service or established newsroom with editorial standards | Yes |
| **3** | Local/specialist outlet, trade press, verified expert | Yes |
| **4** | Aggregator, blog, social post, unverified | **Never on its own** |

**What "independent" means in practice** (`config/owners.yaml`):

- The State (McClatchy) and WIS (Gray Media) are independent: **two sources**.
- The Post and Courier Columbia and Free Times are both Evening Post Industries: **one source**.
- KTLA and The Hill are both Nexstar: **one source**.
- NBC Los Angeles and Telemundo 52 are both Comcast NBCUniversal: **one source**.
- An Associated Press story carried by The State, WIS and WLTX: **one source, AP.**

### Rules

- **SRC-1.** Every claim that needs corroboration must meet its lane's bar from §2, or it's cut.
  · Gate: `V3` · Checked by: Source Verifier
- **SRC-2.** Independence is counted by **owner group**, using `config/owners.yaml`. Outlets in the
  same group count once. An outlet not yet in the file counts as its own group until the Industry
  Intel agent researches its owner. · Gate: `V3` (via `independent_count`)
- **SRC-3.** **Wire copy counts once**, as the wire (Associated Press, Reuters, AFP, Bloomberg), no
  matter how many outlets republish it. A source with `syndicated_from` set counts as its origin.
  · Gate: `V3` (via `independent_count`)
- **SRC-4.** **Tier 4 never counts** toward `independent_count`. Only tiers 1–3 count.
  · Gate: `V3`; see [NE-5](#17-not-yet-enforced-in-code) for the one path that doesn't check tier yet
- **SRC-5.** **Echoes count once.** If several outlets are all repeating the same original (one press
  release, one outlet's scoop), they count as that original. The Verifier traces the claim to its
  origin and records `traced_to_original`. · Gate: `V3` · Verifier judgment
- **SRC-6.** **Official records.** In the `standard`, `strict` and `archive` lanes, one tier-1 source
  that supports the claim is enough on its own (`official_satisfies`). In the `breaking` lane it isn't;
  the claim still needs three independent groups. · Gate: `V3`
- **SRC-7.** An official record shows what an institution *asserts*. A police report shows what police
  say happened. A lawsuit shows what one side claims. Accounts of events from an official record are
  attributed on air ("police said," "according to the complaint"). Official *acts* (a vote, a ruling,
  a filing) can be stated directly. · Gate: `F1` (misleading) · see [NE-6](#17-not-yet-enforced-in-code)
- **SRC-8.** **When one source is acceptable.** One source is enough only when **all** of these are
  true: the lane is `standard` or `archive`; the claim is **not sensitive**; the Verifier's status is
  `single_source`; and the script **says on air who says it** (`attributed: true`). Never in `strict`
  or `breaking`. · Gate: `V3` (the `allow_attributed_single` path)
- **SRC-9.** In `strict` and `breaking`, a **sensitive** claim also needs an official record, even when
  it has enough independent sources. · Gate: `V4`
- **SRC-10.** A source only counts for what our agents could actually read through feeds, public
  pages, public records and public APIs. We never get around a paywall or a login. A headline is not
  evidence for the body of an article we couldn't read. · Verifier rule
- **SRC-11.** A social post counts as a **tier 1 on-record statement** only when it comes from the
  official account of the person or agency speaking **and** that account is listed in our source
  registry (`config/sources/`) or linked from the agency's own website. Every other social post is
  tier 4. · Verifier rule · Gate: `V3`
- **SRC-12.** When a news report cites a document (a filing, a study, a release), the Verifier looks for
  the document itself and prefers it over the report. · Verifier rule
- **SRC-13.** Every source the episode relied on is listed and linked in its show notes, with outlet,
  title and link. · Publish step (`publish/notes.py`)

---

## 4. Accuracy

**In plain words.** Every checkable sentence in a script becomes a claim, and every claim gets
checked twice: once by the Source Verifier, who finds sources from scratch without seeing what the
writer used, and once by the Fact Checker, who checks the exact wording against the evidence. If a
claim is contradicted, it's corrected or cut. If it can't be supported, it's cut. If the wording
overstates the evidence, the wording changes. Speed never wins over accuracy.

### Rules

- **ACC-1.** Every checkable statement is logged as a `Claim` with a type from `CLAIM_TYPES` and its
  risk flags from `RISK_FLAGS`. Every body line lists the claims it contains (`claim_ids`). An
  independent claim-extraction pass adds any claims the writer missed. · Producer + claim extractor
- **ACC-2.** Every claim that needs corroboration must have a Verifier finding, or the episode is
  blocked. · Gate: `V0`
- **ACC-3.** Every claim that needs corroboration must have a Fact Checker rating, or the episode is
  blocked. · Gate: `F0`
- **ACC-4.** A claim the evidence **contradicts** is corrected or removed. · Gate: `V1`
- **ACC-5.** A claim with **no supporting source** is removed. · Gate: `V2`
- **ACC-6.** A claim rated **inaccurate** or **misleading** is fixed. True-but-misleading counts as
  wrong. · Gate: `F1`
- **ACC-7.** A claim that is **unverifiable as worded** is removed or reworded to what the evidence
  supports ("one of the largest," not "the largest"). · Gate: `F2`
- **ACC-8.** The Source Verifier is **blind**: it is never shown the writer's sources. It re-sources
  every claim itself. · Verifier design (`trust/verifier.py`)
- **ACC-9.** Names, titles, ages, places and dates are checked against tier 1–2 sources and spelled
  the way the source spells them. · Gate: `F1`
- **ACC-10.** Time words ("today," "yesterday," "this week") must be true at the episode's scheduled
  air time in the show's time zone. · Gate: `F1`
- **ACC-11.** Legal status is current as of air time. A case that has moved on is described as it
  stands now. · Gate: `F1`, `V4` (strict/breaking)
- **ACC-12.** When a story can't clear the gate, it's cut, not stretched. A killed episode is an
  acceptable outcome. · Gate decision `KILL`
- **ACC-13.** Claims typed `context` and `prediction` aren't run through corroboration. Writers may
  not type a checkable fact as `context` to skip checks. · Claim extractor · see
  [NE-11](#17-not-yet-enforced-in-code)

---

## 5. Attribution language guide

**In plain words.** On audio, you can't see quotation marks or footnotes, so the words we choose
carry the sourcing. "Said" is neutral. "According to" points to a document. "Alleged" means not
proven, and it always comes with *who* is alleging. "Charged with" means prosecutors actually filed
charges. Getting these wrong can hurt a real person, so we treat them as rules.

| Say | Use it when | Example | Don't |
|---|---|---|---|
| **said** | The default for anything a named person or organization stated on the record | "The mayor said the budget is balanced." | "claimed," "admitted," "insisted," "slammed," "blasted": each one takes a side |
| **according to** | Documents, data, records, reports | "According to the coroner's report…" · "according to county data" | Use it for a person's spoken words (use *said*) |
| **reported** | Another newsroom's original reporting; always name the outlet | "The State first reported…" | "Reportedly" with no outlet named |
| **alleges / alleged** | An accusation not proven in court; name who alleges it | "Prosecutors allege…" · "The lawsuit alleges…" | "Allegedly" as a shield with no accuser; "the alleged killer" |
| **accused of** | Someone has formally or publicly accused a person; name the accuser | "…accused by the district attorney's office of fraud" | Unnamed accusers |
| **arrested on suspicion of** | Arrested or booked, no charges filed yet | "He was arrested on suspicion of burglary, police said." | "Arrested for burglary" (sounds like guilt) |
| **charged with** | Only after prosecutors file charges, confirmed by court record or the prosecutor | "She is charged with two counts of fraud." | Using it after only an arrest |
| **indicted** | A grand jury returned an indictment | "A grand jury indicted him on…" | Using it for a complaint or arrest |
| **pleaded not guilty / guilty / no contest** | As entered, per the court record | "He pleaded not guilty Tuesday." | "Denied everything" in place of the plea |
| **convicted / found guilty** | After a verdict or a guilty plea | "A jury found her guilty of…" | Using it before the verdict |
| **acquitted / found not guilty** | After a not-guilty verdict | "He was found not guilty." | "Cleared," "got off," "walked" |
| **sued / the lawsuit says** | Civil filings, which are one side's claims | "The lawsuit says the landlord…" | "Found liable" before a judgment |
| **settled** | A settlement; say "without admitting wrongdoing" if the record says so | "The city settled for $2 million." | Implying a settlement is an admission |
| **confirmed** | A named source confirmed it on the record | "The fire department confirmed two injuries." | "Sources confirm" |
| **expects / projects / forecasts** | Predictions, always with whose prediction | "The National Weather Service expects…" | Unattributed "will" about uncertain events |
| **we did not find a public response from** | We searched and found no public statement | "We did not find a public response from the company." | "Did not respond to a request for comment" (we don't make requests; see §11) |

### Rules

- **ATT-1.** Any claim about what a person or organization says, alleges, believes or predicts names
  them in the same sentence or the one before, and is marked `attributed: true`. · Gate: `V3`
  (single-source path), `V5` · Fact Checker checks the flag matches the words
- **ATT-2.** Every prediction names whose prediction it is. · Gate: `V5`
- **ATT-3.** Every allegation names who is alleging it. "Allegedly" without an accuser is not
  attribution. · Gate: `L1` (`unproven_allegation`) · see [NE-6](#17-not-yet-enforced-in-code)
- **ATT-4.** Legal words (arrested, charged, indicted, pleaded, convicted, acquitted, sentenced,
  sued, settled) must match the court record or the prosecutor's on-record statement as of air time.
  · Gate: `F1`, `V4` (strict/breaking), `L1` (`presumption_of_innocence`)
- **ATT-5.** Police and prosecutor narratives are attributed as accounts ("police said") and never
  stated as settled fact. · Gate: `F1` (misleading), `L1` (`presumption_of_innocence`)
- **ATT-6.** "Said" is the default verb. Loaded attribution verbs are a bias issue.
  · Gate: `B2` (`loaded_language`)
- **ATT-7.** "Reportedly" and "sources say" are not used unless the outlet is named in the same
  sentence. · Gate: `F2` / Bias Checker
- **ATT-8.** When one outlet broke a story with its own reporting, we credit it by name ("first
  reported by…"). · Gate: `F1` / Copyright (§13)

---

## 6. Fairness and balance

**In plain words.** Fair doesn't mean every story gets two equal sides. It means we describe people
and disputes accurately, use neutral words, include the response of anyone we report an accusation
against when a response exists, and don't treat settled facts as a debate. We hold ourselves to a
higher standard with people who have less power to answer back: private citizens, people charged
with crimes, victims and their families.

The **Bias Checker** gives every script a **balance score** from 0 to 100 (higher is more balanced)
and flags lines by type: `loaded_language`, `one_sided`, `missing_perspective`, `framing`,
`speculation`, `sensationalism`, `stereotype`, `false_balance` (`BIAS_TYPES`).

### Rules

- **FAIR-1.** The balance score must meet the lane minimum: 70 standard, 75 strict, 70 breaking,
  65 archive. · Gate: `B1`
- **FAIR-2.** No line may carry a **high-severity** bias issue of any type. Medium and low issues are
  logged and fed back to the Producer but don't block. · Gate: `B2`
- **FAIR-3.** When a story reports an accusation or criticism of a named person or organization, the
  script includes their public response if one exists (a statement, a court filing, a plea). If the
  Verifier found none, the script says so plainly ("We did not find a public response from…").
  · Gate: `B1`/`B2` (`missing_perspective`) · see [NE-4](#17-not-yet-enforced-in-code)
- **FAIR-4.** **Presumption of innocence.** Charges are accusations. Scripts never imply guilt before a
  verdict or plea. · Gate: `L1` (`presumption_of_innocence`)
- **FAIR-5.** **Uncharged people aren't named as suspects.** We name a person as a suspect only once
  they've been arrested or charged, or when a law enforcement agency has publicly named them as a
  suspect on the record. "Person of interest" names are not used. · Gate: `V4` (strict/breaking),
  `L1` (`unproven_allegation`, `privacy`)
- **FAIR-6.** **Private people get more protection than public figures.** A private person is named
  only when the story can't be understood without the name. Claims about them are sensitive
  (`named_private_person`). · Gate: `V3`, `V4` (strict/breaking), `L1` (`privacy`)
- **FAIR-7.** **No false balance.** Established facts aren't framed as one side of a debate.
  · Gate: `B2` (`false_balance`)
- **FAIR-8.** Race, religion, ethnicity, immigration status, gender identity, sexual orientation,
  disability and health are mentioned only when they're relevant to the story and confirmed.
  · Gate: `B2` (`stereotype`), `L1` (`medical`, `privacy`)
- **FAIR-9.** Our hosts don't offer personal opinions on contested political or social questions and
  never endorse candidates or ballot measures. · Gate: `B1`, `B2` (`framing`, `one_sided`)
- **FAIR-10.** **Victims and families.** No graphic detail beyond what the story needs. No
  sensational language. In true crime, the victim is a person, not a plot device.
  · Gate: `B2` (`sensationalism`)
- **FAIR-11.** **Follow-through.** If we reported that someone was arrested or charged, we report how
  the case ended when we learn it (dismissal, acquittal, conviction). · Case Tracker · see
  [NE-14](#17-not-yet-enforced-in-code)
- **FAIR-12.** **History is still about people.** In History of Hollywood, legends and studio
  publicity are labeled as such ("the story studio publicists told was…"), and the same fairness rules
  apply to people who have died. · Gate: `F1`, `F2`, `B2`

---

## 7. What we never do

**In plain words.** Some lines don't move, whatever the lane and whatever the story. These are them.

- **NEVER-1. Present speculation as fact.** No guessing at motives, causes or outcomes in our own
  voice. Predictions are attributed or cut. We don't "solve" cold cases on air or point at people
  investigators haven't named.
  · Gate: `B2` (`speculation`), `F1` (misleading), `F2`, `V5`
- **NEVER-2. Name or identify a minor in a story about crime, courts, accidents, abuse, health or a
  family crisis**, whether as suspect, defendant, victim or witness. That includes people who were
  minors at the time of the events (Cold Case Files included). It also includes *jigsaw*
  identification: a parent's name, an address, a school plus a detail that together point to the
  child. The only time we name a living minor is a young public figure (an athlete, a performer) in
  a story about their public work, using the name their league, school or production uses, and never
  in any of the contexts above.
  · Gate: `L2` (`naming_minor`). Blocks at **any** severity in **every** lane. A claim flagged
  `minor` is sensitive (`V3`, `V4`).
- **NEVER-3. Name or identify a person who says they were sexually assaulted** or sexually abused or
  trafficked, even if another outlet has named them. Some adult survivors choose to tell their story
  publicly under their own name. Our system can't yet reliably tell those cases apart, so **today this
  rule has no exceptions.** · Gate: `L2` (`naming_victim`). Any severity, every lane.
- **NEVER-4. Use AI to impersonate a real person.** No cloned or imitated voices. No synthetic audio of
  a real person, including reading their own quote in their own voice. No invented quotes. No host
  modeled on a real broadcaster. No simulated interviews.
  · Config: `config/voices.yaml` (original personas only) · Gate: quotes need corroboration (`V0`–`V3`,
  `F1`) · see [NE-3](#17-not-yet-enforced-in-code)
- **NEVER-5. Read articles aloud, paywalled or not, or get around a paywall.** We report facts in our
  own words and link the source (§13). · Gate: `L1` (`copyright`) · see
  [NE-10](#17-not-yet-enforced-in-code)
- **NEVER-6. Publish unverified social posts.** We don't air a claim whose only basis is a social
  post, read out posts from unverified accounts, or describe a viral video as showing something until
  its origin is confirmed by tier 1–2 sources. · Gate: tier 4 excluded from `independent_count`
  (`V2`, `V3`) · see [NE-5](#17-not-yet-enforced-in-code)
- **NEVER-7. Pretend to be human, or claim reporting we didn't do.** Our hosts never say they were at
  a scene, spoke to someone, called for comment or saw something. There's no "our reporter."
  · see [NE-4](#17-not-yet-enforced-in-code)
- **NEVER-8. Use anonymous sources** (§11).
- **NEVER-9. Take money, gifts or favors in exchange for coverage** (§12).
- **NEVER-10. Publish anything the gate didn't pass.** No one at Curious & Creative LLC, founders
  included, can override a REWRITE, HOLD or KILL to force an episode out. People can stop the system,
  but they can't push an episode past the gate. · see [NE-13](#17-not-yet-enforced-in-code)
- **NEVER-11. Correct silently.** Every change to a published episode is noted publicly (§15).

---

## 8. Breaking news

**In plain words.** Breaking news is when mistakes happen most: the wrong suspect, the wrong death
toll, the rumor that spreads before anyone checks it. The Breaking Desk runs on its own, stricter
lane. A fact needs **three** independent sources, not two. An official statement alone isn't
enough, because first official numbers often change too. Anything about deaths, crimes, suspects or
victims needs three sources **and** an official record. If a story is real but not confirmed yet, we
don't guess. We wait 15 minutes and check again, up to six times. If it still isn't confirmed after
90 minutes, the unconfirmed parts are cut or the flash doesn't air. Ava, our breaking anchor, says
what's confirmed, who confirmed it and what isn't known yet.

### Rules

- **BRK-1.** The Breaking Desk runs in the `breaking` lane. A flash is triggered by the Story Desk's
  breaking detector (`desk/breaking.py`: velocity, independent tier ≤2 outlets, official
  confirmation and event class), with at least 30 minutes between flashes (`min_gap_minutes`).
- **BRK-2.** Every claim that needs corroboration has **3 independent owner groups**. One official
  record does not substitute (`official_satisfies = false`). · Gate: `V3`
- **BRK-3.** Every **sensitive** claim (deaths, crimes, suspects, victims, legal status, named private
  people, minors) also has an **official record**. · Gate: `V4`
- **BRK-4.** **No single-source claims, even attributed** (`allow_attributed_single = false`).
  "Unconfirmed reports" never air. · Gate: `V3`
- **BRK-5.** **Hold, don't guess.** If the only blocking reasons are `V3`/`V4` (not enough
  confirmation yet), the gate returns **HOLD** and re-checks after **15 minutes**, up to **6 holds**
  (90 minutes). After that, the script gets its rewrite (cut what's unconfirmed), then it's killed if
  it's still blocked. · Gate decision `HOLD` (`max_holds = 6`, `hold_minutes = 15`)
- **BRK-6.** Any other blocking problem gets **one** rewrite (`max_rewrites = 1`), then **KILL**.
- **BRK-7.** Legal issues of **medium** severity or higher block. · Gate: `L1`
- **BRK-8.** **Casualty numbers** come only from official sources, are attributed, use "at least" and
  carry the time they were given ("at least four people died, the county coroner said as of 3 p.m.
  Eastern"). · Gate: `V4` (`death`), `F1`, `V5`
- **BRK-9.** **No suspect names, motives or ideologies** until an official source states them on the
  record, and then attributed to that source. · Gate: `V4`, `L1` (`unproven_allegation`), `B2`
  (`speculation`)
- **BRK-10.** **Names of the dead** air only after an official release (coroner, medical examiner,
  police) or an on-record family statement. · Gate: `V4` (`death`)
- **BRK-11.** Each flash states what is confirmed and by whom, and what is still unknown.
  · Fact Checker (`F1` for overstatement)
- **BRK-12.** When facts change, the next flash says what changed, and earlier flash notes are
  corrected through §15. · Recheck monitor

---

## 9. Numbers and statistics

**In plain words.** Numbers sound precise, which is why a wrong one does so much damage. Every
number is a claim and gets the same corroboration as any other fact. On air, we say where a number
came from and what period it covers, round only in ways that stay true, and don't compare things
that can't be compared.

### Rules

- **NUM-1.** Every number is a claim of type `number` and needs corroboration like any fact.
  · Gate: `V0`–`V4`, `F0`–`F2`
- **NUM-2.** Say the **source**, the **unit** and the **time period** on air ("The county
  recorded [number] crashes last year, according to the state Department of Public Safety").
  · Gate: `F1` (misleading without context)
- **NUM-3.** Rounding for the ear is fine only if the direction word stays true: "more than 4
  million" only if it's above 4 million, "nearly" only if it's below. · Gate: `F1`
- **NUM-4.** Percent and percentage points are different. Rates and counts are different. Comparing
  places of different sizes uses per-person rates. · Gate: `F1`
- **NUM-5.** Compare like with like. Money across years is adjusted for inflation, or we say it isn't
  ("not adjusted for inflation"). This matters most in History of Hollywood. · Gate: `F1`
- **NUM-6.** **Polls**: name who ran it, when, and the margin of error. A gap inside the margin of
  error is not a lead. · Gate: `F1`, `B2` (`framing`)
- **NUM-7.** **Crime statistics**: name the agency and the period. One period is not a trend.
  Reported crimes aren't the same as all crimes. · Gate: `F1`, `B2` (`sensationalism`)
- **NUM-8.** **Casualty counts**: see BRK-8; the same rule applies on every show.
- **NUM-9.** Estimates, projections and forecasts are predictions and are attributed. · Gate: `V5`
- **NUM-10.** If we do our own math ("that works out to about one in five"), we say so, and the inputs
  must be corroborated numbers. · Gate: `F1`, `F2`
- **NUM-11.** No number comes only from a tier 4 source. · Gate: `V3`

---

## 10. Quotes

**In plain words.** A quote is someone's exact words. We use them only when we can show they were
said, word for word, by the person we credit. Our hosts read quotes in their own voices and make it
clear you're hearing a quote. We never make it sound like the real person is speaking.

### Rules

- **QUO-1.** **Verbatim only.** A quote matches its source word for word. A paraphrase is never
  presented as a quote. · Gate: `F1` (inaccurate), `V1`
- **QUO-2.** **Always attributed**: the speaker's name, their role, and where they said it ("in a
  statement," "in court Tuesday," "on the department's official account"). · Gate: `V3`
  (attributed path) · see [NE-7](#17-not-yet-enforced-in-code)
- **QUO-3.** **Traced to the original**: the statement, transcript, filing or recording itself, or a
  tier 1–2 outlet that heard it directly. · Verifier (`traced_to_original`) · see
  [NE-7](#17-not-yet-enforced-in-code)
- **QUO-4.** Every quote is a `quote` claim and needs corroboration like any fact.
  · Gate: `V0`–`V3`, `F0`
- **QUO-5.** **Signal it for the ear**: "In her words…," "quote… end quote," or a clear pause and
  attribution. A listener must always know where the quote starts and stops. · Gate: `F1`
- **QUO-6.** **Read by our host, never in the speaker's voice.** No synthetic version of a real
  person's voice, ever (NEVER-4).
- **QUO-7.** **Short and in context.** A sentence or two, without changing the meaning by what's left
  out. · Gate: `F1` (misleading)
- **QUO-8.** We quote newsmakers, not journalists. A reporter's sentences are their work, not a
  quote we can borrow (§13). · Gate: `L1` (`copyright`)
- **QUO-9.** Quotes from social posts come only from accounts that meet SRC-11. · Gate: `V3`

---

## 11. Anonymous sources

**In plain words.** We don't use them, and the reason is simple. Using an anonymous source means a
reporter knows who the person is, has judged that they're in a position to know, and has promised to
protect them. **We don't have reporters.** Our system can't meet anyone, can't check who they are and
can't make or keep a promise of confidentiality. So we don't pretend to.

This also covers other newsrooms' anonymous sources. When another outlet reports something based
only on unnamed sources, we wait until it's confirmed on the record or by an official record. Two
outlets citing unnamed officials may be hearing from the same person, so that isn't "two places."

### Rules

- **ANON-1.** We have no confidential sources and never claim to. Scripts never say "a source told
  us," "sources say" or "we've learned." · see [NE-4](#17-not-yet-enforced-in-code)
- **ANON-2.** Evidence that rests only on unnamed sources (in any outlet) does **not** count toward
  `independent_count`, and a claim supported only that way does not air. · Verifier rule · Gate:
  `V2`/`V3` · see [NE-8](#17-not-yet-enforced-in-code)
- **ANON-3.** Once the same fact is confirmed on the record or by an official record, it may air,
  attributed to the on-record source. · Gate: `V3`, `V4`

---

## 12. Conflicts of interest, sponsors and advertising

**In plain words.** Advertisers pay for ad time. They don't buy coverage, they don't see scripts
ahead of time, and they can't get a story changed, softened or removed. Ads are clearly marked and
kept separate from the news. Our hosts are AI, so when a host reads an ad, it never claims to have
used the product. When a story involves a sponsor, the company, its owners, or the AI and voice
providers we use to make the shows, we say so on air.

### Rules

- **COI-1.** Sponsors and advertisers never see, approve or influence scripts, story choice or
  corrections. No paid placement in news. No "sponsored stories." · Policy; see
  [NE-12](#17-not-yet-enforced-in-code)
- **COI-2.** Ads run only in marked ad breaks, never inside a story, and are introduced as ads
  ("This episode is supported by…").
- **COI-3.** A host reading an ad never claims personal experience with the product ("I use it every
  day"). Our hosts are AI and have none. · see [NE-4](#17-not-yet-enforced-in-code)
- **COI-4.** When a story involves a current sponsor, the script says so on air and in the show notes.
  · see [NE-12](#17-not-yet-enforced-in-code)
- **COI-5.** When a story involves Curious & Creative LLC, its owners or their other businesses, or a
  company whose products we use to make the network (AI model, voice and hosting providers), the
  script says so on air. · Bias Checker (`B2` `framing`/`one_sided`) · see
  [NE-12](#17-not-yet-enforced-in-code)
- **COI-6.** We accept no payment, gifts or favors in exchange for coverage. A press release is a lead
  and a tier-1 statement of what its author says, attributed as such, not a story by itself.
  · Gate: `V3`, `F1`
- **COI-7.** Ads are written and scheduled outside the episode script, so the Trust Stack never sees
  them. Ad copy needs its own check against COI-2 and COI-3 before it runs. · see
  [NE-12](#17-not-yet-enforced-in-code)

---

## 13. Copyright

**In plain words.** Facts belong to everyone. The way a journalist writes them up belongs to that
journalist and their outlet. We report the facts in our own words, credit the outlets whose original
reporting we rely on, and link every source so you can read the full story there. We don't read
articles aloud, paste them or closely paraphrase them, whether or not they're behind a paywall.

### Rules

- **COPY-1.** Facts in our own words. No reading, pasting or close paraphrasing of any article's text.
  · Gate: `L1` (`copyright`) · see [NE-10](#17-not-yet-enforced-in-code)
- **COPY-2.** We never get around paywalls, logins or access controls, and never summarize a paywalled
  article so closely that it stands in for reading it. · Gate: `L1` (`copyright`)
- **COPY-3.** We credit original reporting by name ("first reported by…") and link it. · Gate: `F1`
- **COPY-4.** Every source is linked in the show notes. · Publish step (`publish/notes.py`)
- **COPY-5.** We store our own summary or a short excerpt of a source, never its full text
  (`Source.excerpt`). · Schema contract
- **COPY-6.** No third-party audio (news clips, film or TV clips, songs) without a license. Music beds
  are licensed or original.
- **COPY-7.** History of Hollywood describes films and scenes. It doesn't play them. Public-domain
  material may be quoted briefly with its source named. · Gate: `L1` (`copyright`)
- **COPY-8.** Sensors gather through feeds, public APIs and public records only.

---

## 14. Our voices and the AI disclosure

**In plain words.** Every voice you hear on our network is an original synthetic persona: Mara, Theo,
Lena, Marcus, Ava and June. None of them is modeled on, named after or imitating a real person. At the
end of every episode, you'll hear a short disclosure that the episode was made with AI, and the same
disclosure is in the episode's details in your podcast app.

### Rules

- **VOICE-1.** Every host is an original persona in `config/voices.yaml`. No persona may be modeled on,
  named after or imitate a real person. · Config
- **VOICE-2.** Every script line's `speaker` is one of those personas. · see
  [NE-3](#17-not-yet-enforced-in-code)
- **VOICE-3.** **Every episode ends with the spoken AI disclosure**, voiced by the network's
  disclosure voice (Ava, `disclosure_voice`). Without a `disclosure` segment, the episode is blocked.
  · Gate: `S1` (presence) · see [NE-1](#17-not-yet-enforced-in-code) (position)
- **VOICE-4.** The disclosure must say that: (a) the episode was written and voiced using AI;
  (b) the voices are synthetic and not real people; (c) facts were checked by automated systems
  against independent sources; (d) sources and corrections are in the show notes; (e) the network is
  published by Curious & Creative LLC. · Disclosure step (`producer/disclosure.py`)
- **VOICE-5.** The disclosure also appears in the episode's metadata: description/show notes and the
  RSS feed (`Episode.disclosure_text`, `publish/feed.py`). · see [NE-2](#17-not-yet-enforced-in-code)
- **VOICE-6.** Hosts never claim to be human or to have human experiences (NEVER-7).

---

## 15. Automation accountability: who's responsible and how we fix mistakes

**In plain words.** **Curious & Creative LLC is responsible for everything this network publishes.**
Not the software, not a vendor, not "the AI." We chose to run without a human approving each
episode, so the company owns the rules, owns the results and owns the mistakes.

Here's how that works without anyone reading scripts before they air:

- **The rules are code.** The gate makes the same decision from the same inputs every time, and
  every decision, with its reasons and scores, is recorded.
- **We show our work.** Every published episode's gate decision goes into a public **trust log**, and
  its show notes list its sources with a verification summary.
- **We keep checking after we publish.** A recheck monitor re-verifies published claims after air
  and opens a correction when the evidence changes.
- **You can tell us.** Listener, outlet and subject reports go into the same correction queue as our
  own automated findings.
- **People can stop it.** The owners can halt any show, or the whole network, at any moment, and
  every show has a daily spending cap. What people can't do is force an episode past the gate.

**How we fix errors**

| Action (`Correction.action`) | When we use it | What you'll see |
|---|---|---|
| **note** | A minor error that doesn't change the story's meaning (a wrong title, a misspelled name in the notes) | A dated correction in the show notes and the trust log |
| **reissue** | An error that changes a fact a listener would rely on, or **any** error about a named person in a crime or court story | Corrected audio replaces the episode (status `corrected`), a dated note says what changed, and the next episode of that show says the correction out loud |
| **retract** | The central claim was wrong, or the episode broke a NEVER rule (§7) | The episode is removed from the feed (status `retracted`), a retraction notice stays up, and the next episode of that show says the correction out loud |

### Rules

- **AUTO-1.** Curious & Creative LLC is the publisher of record and is responsible for every episode.
  "The AI made a mistake" is never offered as an excuse, on air or off.
- **AUTO-2.** No episode publishes unless the gate's decision is `PUBLISH`. There is no override that
  forces publication. · Gate · see [NE-13](#17-not-yet-enforced-in-code)
- **AUTO-3.** Every gate decision (PUBLISH, REWRITE, HOLD, KILL) is stored with its `reasons`
  (rule ids), `scores` (`corroboration_rate`, `accuracy_rate`, `balance_score`, `claims`) and lane.
  Published episodes' decisions go to the public trust log (`publish/trustlog.py`).
- **AUTO-4.** Published claims are re-verified after air for at least 7 days (`monitor/recheck.py`).
  A claim that becomes contradicted opens a `Correction`.
- **AUTO-5.** Anyone can report an error. Every report becomes a `Correction` record with
  `reported_by` set (`listener`, `outlet`, `monitor:recheck`) and is checked against evidence, not
  against who complained or whether they advertise.
- **AUTO-6.** Corrections use the note / reissue / retract rules in the table above. Reissues and
  retractions are spoken in the next episode of the same show. · see
  [NE-14](#17-not-yet-enforced-in-code)
- **AUTO-7.** We never edit silently. Every correction carries its date and what changed.
- **AUTO-8.** The kill switch (`monitor/killswitch.py`) stops any show or the whole network
  immediately. When a show is killed, nothing publishes for it. Per-show daily budgets
  (`monitor/budget.py`) stop runaway costs.
- **AUTO-9.** Any change to a gate rule or lane policy is made in code with tests and recorded in this
  page's change log the same day. Code and this page must agree.
- **AUTO-10.** An error that reveals a missing rule leads to a rule change, not just a fix, and the
  change log says so.

---

## 16. Gate rule map

Every rule id `gate.py` can return today. **All of them are blocking.** There are no warning-only
rules yet.

| Rule | Checks | Fires when | Lanes | Standards it enforces |
|---|---|---|---|---|
| `V0` | Verifier coverage | A claim of a corroboration-needing type has no Verifier finding | all | ACC-2, NUM-1, QUO-4 |
| `V1` | Contradiction | The Verifier's evidence contradicts the claim | all | ACC-4, QUO-1 |
| `V2` | Support | No supporting source found | all | ACC-5, NEVER-6, ANON-2 |
| `V3` | Corroboration threshold | Fewer independent owner groups than the lane needs, and neither the official path nor the attributed single-source path applies | all (2 / 2 / **3** / 2) | SRC-1–6, SRC-8, SRC-11, ATT-1, BRK-2, BRK-4, NUM-1, NUM-11, QUO-2, QUO-4, QUO-9, ANON-2/3, NEVER-2, NEVER-6, FAIR-6, COI-6 |
| `V4` | Official record for sensitive claims | A sensitive claim clears `V3` but has no tier-1 source | strict, breaking | SRC-9, ACC-11, ATT-4, FAIR-5, FAIR-6, BRK-3, BRK-8–10, NEVER-2 |
| `V5` | Predictions | A `prediction` claim isn't attributed | all | ATT-1, ATT-2, NUM-9, BRK-8, NEVER-1 |
| `F0` | Fact-check coverage | A corroboration-needing claim has no Fact Checker rating | all | ACC-3, NUM-1, QUO-4 |
| `F1` | Accuracy | Rated `inaccurate` or `misleading` | all | ACC-6, ACC-9–11, SRC-7, ATT-4/5, NUM-2–7, NUM-10, QUO-1, QUO-5, QUO-7, BRK-8, BRK-11, FAIR-12, COPY-3, NEVER-1 |
| `F2` | Verifiability | Rated `unverifiable` | all | ACC-7, ATT-7, NUM-10, FAIR-12, NEVER-1 |
| `B1` | Balance | `balance_score` below lane minimum (70 / **75** / 70 / 65) | all | FAIR-1, FAIR-3, FAIR-9 |
| `B2` | Bias | Any **high**-severity bias issue | all | ATT-6, FAIR-2, FAIR-3, FAIR-7–10, FAIR-12, NUM-6, NUM-7, BRK-9, NEVER-1, COI-5 |
| `L1` | Legal | A legal issue (`unproven_allegation`, `presumption_of_innocence`, `privacy`, `copyright`, `medical`, `other`) at or above lane severity (high / **medium** / **medium** / high) | all | ATT-3–5, FAIR-4–6, FAIR-8, BRK-7, BRK-9, QUO-8, COPY-1, COPY-2, COPY-7, NEVER-5 |
| `L2` | Hard-stop legal | `naming_minor` or `naming_victim`, **any severity** | all | NEVER-2, NEVER-3 |
| `S1` | AI disclosure | No line in the `disclosure` segment | all | VOICE-3 |

**How the gate picks a decision** (in this order):

1. No reasons → **PUBLISH**.
2. `L2` fired and the script is at or past its lane's rewrite budget → **KILL**. (Before that, `L2`
   forces a rewrite that removes the identifying details. A name flagged by `L2` can never publish.)
3. Lane is `breaking`, **every** reason is `V3` or `V4`, and fewer than 6 holds used → **HOLD**,
   re-check in 15 minutes.
4. Script revision below the lane's rewrite budget → **REWRITE**, with fix instructions attached.
5. Otherwise → **KILL**.

**Where the gate relies on judgment.** The gate is deterministic, but its inputs come from AI
checkers. Whether a script names a minor, for example, depends on the Legal Screener flagging it. We
reduce that risk by keeping the Verifier blind to the writer's sources, by counting independence in
code from `config/owners.yaml` instead of trusting a model's count (`desk/independence.py`), by
re-checking after publication, and by testing the gate against fixed fixtures.

---

## 17. Not yet enforced in code

> **Not yet enforced in code**
>
> These standards are part of this rulebook today, but `gate.py` (or the code around it) doesn't check
> them yet. Until it does, they rely on the agents' instructions and on rechecks after publication. Each
> item names the check we propose. Proposed rule ids are placeholders until the code lands.
>
> | # | Standard | The gap today | Proposed check |
> |---|---|---|---|
> | **NE-1** | VOICE-3: the disclosure comes **at the end** | `S1` only checks that a `disclosure` line exists somewhere | **S2**: the last `ScriptLine` has `segment == "disclosure"` |
> | **NE-2** | VOICE-5: the disclosure is **in metadata** | The gate never sees `Episode.disclosure_text` or the feed item | **S3** (publish step): refuse to publish if `disclosure_text` is empty or missing from the RSS item |
> | **NE-3** | VOICE-1/2, NEVER-4: only original personas speak | No check that `speaker` is a persona in `voices.yaml`, or that the disclosure uses `disclosure_voice` | **S4**: every `speaker` ∈ `voices.yaml` personas; disclosure lines spoken by `disclosure_voice` |
> | **NE-4** | NEVER-7, ANON-1, FAIR-3, COI-3: no false claims of presence, contact or experience | No phrase check | **S5**: deterministic phrase list ("we reached out," "did not respond to a request for comment" without a named outlet, "our reporter," "at the scene," "I spoke with," "sources told us," "exclusive," "I use it") |
> | **NE-5** | SRC-4, NEVER-6: tier 4 never carries a claim | The attributed single-source path checks `status == "single_source"` but not the source's tier, so a social-post-only claim could pass in `standard`/`archive` if the Verifier labels it that way | **V6**: the attributed single-source path also requires `independent_count >= 1` or `has_official` |
> | **NE-6** | ATT-3, SRC-7: allegations are always attributed | No lane checks `attributed` on `allegation`/`legal_status` claims; the official-record path passes them unattributed | **V7**: block any `allegation` or `legal_status` claim with `attributed == false`, in every lane |
> | **NE-7** | QUO-2, QUO-3: quotes are attributed and traced | `traced_to_original` is in the schema but the gate ignores it; `attributed` isn't required for quotes | **V8**: block any `quote` claim unless `attributed == true` and `traced_to_original == true` |
> | **NE-8** | ANON-2: anonymous sourcing doesn't count | `EvidenceSource` has no way to mark "rests on unnamed sources" | Schema: add `EvidenceSource.anonymous_basis: bool`; independence code excludes it from `independent_count` |
> | **NE-9** | BRK-10 on every show: names of the dead only after official release | `V4` applies only in `strict` and `breaking`; in `standard`/`archive`, two independent outlets can carry a death identification | **V9**: claims flagged `death` together with `named_private_person` need `has_official` in every lane |
> | **NE-10** | COPY-1, NEVER-5: no reading articles aloud | Relies on the Legal Screener; `copyright` issues of **medium** severity don't block in `standard`/`archive`; no text-overlap check | **C1**: deterministic overlap check between script lines and retrieved source text (outside attributed quotes), and treat `copyright` like `L2` (block at any severity) |
> | **NE-11** | ACC-13: nothing escapes checking | Claims typed `context` skip `V0`–`V4`, and `F0` only covers corroboration-needing types | Extend `F0` to every claim type; claim extractor re-types facts mislabeled as `context` |
> | **NE-12** | COI-1, COI-4, COI-5, COI-7: sponsor separation and disclosure | No sponsor registry; no `ad` segment; ads never pass through the Trust Stack | `config/sponsors.yaml`; **S6**: a script naming a current sponsor or a listed conflict must include a disclosure line; separate ad-copy check before scheduling |
> | **NE-13** | NEVER-10, AUTO-2: nothing publishes without PUBLISH | The publish step isn't built yet, so "refuse anything that isn't PUBLISH, no override flag" and "log every decision, including KILL" aren't enforced in code | Publish step asserts `decision == "PUBLISH"`; tests prove no override path exists; trust log records every decision |
> | **NE-14** | AUTO-6, FAIR-11: spoken corrections and follow-through | The correction and recheck monitors aren't built yet; nothing makes the next episode carry a spoken correction, tracks case outcomes for people we named, or alerts the owners on a KILL, an `L2` hit or a retraction | Producer reads open `reissue`/`retract` corrections for the show and adds a correction line; Case Tracker keeps a follow-up list of named defendants; owner alert on KILL/`L2`/retract |

---

## 18. Changing these standards

This page and the code have to say the same thing. When `gate.py` or `schemas.py` changes, this page
changes the same day, and when a standard here changes, the code and its tests change with it.
Moving an item out of §17 means writing the check, writing the test, and updating the rule's
enforcement tag.

**Change log**

| Date | Version | Change |
|---|---|---|
| 2026-10-11 | 1.0 | First edition. Mapped to gate rules `V0`–`V5`, `F0`–`F2`, `B1`–`B2`, `L1`–`L2`, `S1` and lanes `standard`, `strict`, `breaking`, `archive`. 14 standards listed as not yet enforced in code. |

*Where this page is silent, we follow widely used newsroom style. Where the two conflict, this page
wins.*
