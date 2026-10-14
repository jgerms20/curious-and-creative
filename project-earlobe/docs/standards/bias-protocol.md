# Bias Protocol

**The Curious & Creative Network: how the Bias Checker scores balance and flags slanted lines**

| | |
|---|---|
| **Applies to** | Every show: Columbia Daily, LA Daily, The Breaking Desk, LA Courts Roundup, Case Tracker, Cold Case Files, History of Hollywood, and every city show added later |
| **Run by** | The **Bias Checker** (Sonnet tier, `earlobe/trust/bias.py`). It reads the script only: no sources, no other checker's report |
| **Read by** | The **Standards Editor** gate ([`earlobe/trust/gate.py`](../../earlobe/trust/gate.py)) through rules `B1` (balance score) and `B2` (any high-severity issue) |
| **Contracts** | [`earlobe/schemas.py`](../../earlobe/schemas.py): `BIAS_TYPES`, `SEVERITY`, `BiasIssue`, `BiasReport` |
| **Parent page** | [Editorial Standards](editorial-standards.md) §6 (FAIR-1 to FAIR-12). If the two disagree, the Editorial Standards win |
| **Version** | 1.0, October 12, 2026 (as of Oct 2026). Example sentences are made up to show phrasing, not news reports |

**The 30-second version**

- Fair does not mean "two equal sides." It means accurate description, neutral words, a response from anyone we accuse, and no debate staged over settled facts.
- The checker returns a **balance score** (0 to 100) and a list of flagged lines. The gate blocks on a score under the lane minimum **or** any **high** issue. Medium and low issues don't block.
- Strict standards for people who can't answer back: private citizens, people charged with crimes, victims.
- "Said" is the default verb. Bad news told plainly is balanced; we never deduct for an unpleasant story.

---

## 1. The eight bias types

These are the exact `BIAS_TYPES`. Each row shows a made-up spoken line and its neutral rewrite.

| Type | Spoken example (made up) | Neutral rewrite | Usually **high** when |
|---|---|---|---|
| `loaded_language` | "The councilmember slammed the budget and refused to answer questions." | "The councilmember said she opposes the budget." | A loaded verb or label is aimed at a named person or group, or the line treats an accusation as fact ("the alleged killer") |
| `one_sided` | "Tenants say the landlord ignored repairs for months." | "Tenants say the landlord ignored repairs for months. We did not find a public response from the landlord." | An accusation airs with no response **and** no "we did not find a public response" |
| `missing_perspective` | A transit cut story where only the agency speaks | Add the affected riders' public comments from the board record: "Riders spoke against the cut at Tuesday's meeting, according to the minutes." | The absent group is plainly central and the story reads as a verdict without them |
| `framing` | "Crime is out of control downtown, with 12 break-ins this month." | "Police reported 12 break-ins downtown this month, up from 9 a year ago, according to the department." | The lead, order or kicker steers to a conclusion the facts don't carry; a host opinion or endorsement |
| `speculation` | "He likely panicked and ran." | "Police said he left before officers arrived." (or cut) | Motive, cause or intent is guessed at in the host's own voice |
| `sensationalism` | "A horrifying scene of blood and chaos." | "Two people were taken to the hospital, the fire department said." | Graphic detail about a victim that serves shock, or a cliffhanger over a death |
| `stereotype` | "The suspect, a recent immigrant, was arrested..." | "A 34-year-old man was arrested on suspicion of theft, police said." | Group traits, or race, religion, immigration status, gender identity, disability or health mentioned without relevance and confirmation |
| `false_balance` | "The state counts 40 cases, but others say it could be 400." | "The state health department counted 40 cases." | An official count, ruling or scientific consensus is staged as one side of a debate |

**Severity** (from the checker's instructions): **high** = should not air as written; **medium** = a noticeable slant, fix it; **low** = polish. "High" is never used for matters of taste, and "low" is never used to dodge a plainly one-sided line.

**Do not flag:** plain, attributed negative information (a report that criticizes an official, correctly credited), the verb "said," accurate legal terms, the specifics a story needs, or the `disclosure` segment. An empty issue list is a valid answer.

---

## 2. Balance score anchors and lane thresholds

The score covers the whole script, 0 to 100, higher is more balanced. A short, plain script with nothing to balance scores high.

| Score | Anchor | Sounds like | Standard (70) | Strict (75) | Breaking (70) | Archive (65) |
|---|---|---|---|---|---|---|
| 90-100 | Exemplary | Neutral words; every accusation has a response or "none found"; all claims attributed | pass | pass | pass | pass |
| 80-89 | Good | Sound, with minor polish available | pass | pass | pass | pass |
| 75-79 | Acceptable | Some slant, a missing perspective or a few loaded words | pass | pass | pass | pass |
| 70-74 | Borderline | Same, a little more of it | pass | **fail** | pass | pass |
| 65-69 | Noticeably one-sided or loaded | A pattern of slanted lines | fail | fail | fail | **pass** |
| 60-64 | Noticeably one-sided or loaded | Same | fail | fail | fail | fail |
| Under 60 | Advocacy or sensational | Reads as an argument or a thriller | fail | fail | fail | fail |

The checker's own bands are 90-100, 80-89, 70-79, 60-69 and under 60; we split 70-79 and 60-69 at 75 and 65 because that is where the lane minimums fall. The lane columns are the `min_balance` values in `POLICIES`. A fail at `B1` sends the Producer the checker's `missing_perspectives` as fix instructions.

**Lane settings that touch fairness** (`POLICIES` in `gate.py`; the lane table is in Editorial Standards §2)

| Lane | Shows | `min_balance` | `legal_block_severity` | `max_rewrites` |
|---|---|---|---|---|
| `standard` | Columbia Daily, LA Daily, city dailies | 70 | high | 2 |
| `strict` | LA Courts Roundup, Case Tracker, Cold Case Files | **75** | **medium** | 2 |
| `breaking` | The Breaking Desk | 70 | **medium** | 1 (plus up to 6 holds, only for sourcing) |
| `archive` | History of Hollywood | 65 | high | 2 |

*(Inference)* Archive's lower bar gives history a little more narrative voice. It also means a 65-69 script, which the checker describes as "noticeably one-sided or loaded," can air in that lane. High-severity issues still block there, so the real protection is `B2`.

---

## 3. Missing-perspectives checklist by beat

The checker lists perspectives that **exist, matter and are absent**. It never lists ones that can't exist (the response of someone who has died). Use this as the question list. Beats are from `config/shows.yaml`.

| Beat | Ask before airing |
|---|---|
| `government`, `federal_government` | The decision-maker's stated reason; opposition or dissenting votes; the people affected; the agency's own explanation of the numbers |
| `scotus` | Both parties' arguments; the dissent; what the ruling does and doesn't decide |
| `public_safety` | The agency's account; the response of anyone charged (plea, statement, or "none found"); residents affected; agency and time period for any statistic |
| `criminal_court`, `da_press`, `tracked_cases` | Prosecution **and** defense positions; the plea; the judge's ruling; the docket date we are current as of; the victim's or family's public statement only if it is on the record and respects dignity rules |
| `civil_court`, `federal_court` | Plaintiff's claim **and** defendant's answer or response; settlement terms, with "without admitting wrongdoing" if the record says so |
| `cold_case` | The agency's current status and tip line; the family's public statements only; no suspect theories |
| `education` | District or school; teachers and staff; parents; students as a group, never a named minor in a crisis story |
| `business`, `business_mega`, `entertainment_business` | The company's statement; workers and customers; the regulator; any conflict with our own AI, voice or hosting vendors (COI-5) |
| `development`, `housing` | Developer; neighbors and residents; city planners; tenants **and** landlords |
| `transit` | The agency; riders; workers; where the money comes from |
| `weather`, `disaster`, `major_death`, `attack_or_attempt` | The official forecast, advisory or release; who is affected; emergency management. For deaths, an on-record family statement only |
| `sports`, `sports_mega` | Both teams or the league and the athlete; no fan speculation |
| `culture`, `hollywood_history` | Practitioners or estates; contemporaneous records; studio publicity labeled as publicity (FAIR-12). Fairness rules still apply to people who have died |
| `space`, `world` | The agency and independent experts; each government's own statement |

---

## 4. Loaded-word list

Words that take a side when **we** say them. † = already in the Bias Checker's instructions today; the rest are our proposed extension *(inference)*. Inside an accurate, attributed quote they are fine (QUO rules); the host's lead-in stays neutral ("In her words...").

| Group | Avoid | Use instead |
|---|---|---|
| Attribution verbs | claimed†, admitted†, insisted†, conceded†, slammed†, blasted†, ripped†, refused†, came clean†, lashed out, fired back, took aim | **said**, or "according to" for documents |
| Judgments | shocking†, outrageous†, brazen†, heartbreaking†, controversial† (as a label), stunning, bombshell, troubling | Delete the adjective and state the fact |
| Labels for people | thug†, illegal alien†, addict†, regime†, so-called†, junkie, mastermind, ringleader, predator, monster | The person's role or the charge: "a man charged with burglary," "the government of..." |
| Guilt implied | the alleged killer†, the killer, the burglar, "murdered" when only charged, got off, walked free, cleared, "suspect" for someone uncharged | "the man charged with murder," "was found not guilty" (ladder in the [crime rules](crime-and-courts-rules.md)) |
| Speculation | apparently, appears to, likely, may have been trying to, reportedly (no outlet), sources say | Attribute to a named source, or cut |
| Drama | horrific, gruesome, bloodbath, rampage, carnage, savage, chilling (as a kicker) | The count and the official source |
| Policy spin | slashed, gutted, crackdown, scheme, giveaway, loophole | cut, reduced, new rule, plan, as the record names it |

A loaded word aimed at a **named person or group** in the host's voice is **high**. Elsewhere it is usually **medium**.

---

## 5. Rules

Rule ids `BIAS-n` are new here. `FAIR-n`, `ATT-n` and `COI-n` are in the Editorial Standards.

- **BIAS-1.** Score honestly in both directions: no inflation to be agreeable, no deduction because the news is bad. · Gate: `B1`
- **BIAS-2.** Every accusation or criticism of a named person or body carries their public response or "We did not find a public response from..." (FAIR-3). · Gate: `B2` (`one_sided`, `missing_perspective`)
- **BIAS-3.** "Said" is the default verb. Loaded attribution verbs and labels in the host's voice are flagged (ATT-6). · Gate: `B2` (`loaded_language`)
- **BIAS-4.** The checker returns `missing_perspectives` from the §3 checklist, named in short phrases the Producer can act on. · Gate: `B1` fix text
- **BIAS-5.** Crime and court lines use the legal ladder and the presumption of innocence (FAIR-4). Implied guilt is **high**. · Gate: `B2`, `L1`
- **BIAS-6.** Hosts give no personal opinions on contested questions and never endorse candidates or ballot measures (FAIR-9). · Gate: `B2` (`framing`, `one_sided`)
- **BIAS-7.** A story involving Curious & Creative LLC, its owners, or our AI, voice or hosting providers says so on air (COI-5). · Gate: `B2`
- **BIAS-8.** An established fact is stated once, attributed, and not staged as a debate (FAIR-7). · Gate: `B2` (`false_balance`)
- **BIAS-9.** Identity traits (race, religion, immigration status, disability, health) appear only when relevant **and** confirmed (FAIR-8). · Gate: `B2` (`stereotype`), `L1`
- **BIAS-10.** Fixes are neutral wording in a spoken style, never "make it more positive." A fix may add a missing response; it may not invent one (NEVER-4, NEVER-7). · Producer
- **BIAS-11.** Titles, descriptions, show notes and social copy follow the same word rules as the script. · see BIAS-NE-4

---

## 6. Not yet enforced in code

> **Not yet enforced in code.** The gate sees only a score and issue severities. Everything below depends on the Bias Checker's judgment until the check lands. Proposed ids are placeholders.
>
> | # | Standard | The gap today | Proposed check |
> |---|---|---|---|
> | **BIAS-NE-1** | §4 loaded words | No deterministic word screen; an AI judges every line | **B3**: a word-list pass in code. Medium issue on a hit, high when the word sits in the same sentence as a named entity in the host's voice |
> | **BIAS-NE-2** | FAIR-2: medium and low issues are fed back | The gate only emits blocking reasons, so medium/low issues never reach the trust log | Emit non-blocking `GateReason`s (`blocking=False`) for medium issues so they are logged |
> | **BIAS-NE-3** | BIAS-2, FAIR-3 | No check that an accusation has a response line (see **NE-4** in the Editorial Standards) | **B4**: any `allegation` claim needs a response line or a "did not find" line within the story |
> | **BIAS-NE-4** | BIAS-11 | The checker receives script lines only; titles, descriptions and social copy are never scored | Score all public text at the publish step |
> | **BIAS-NE-5** | BIAS-1 | No calibration set, so scores could drift | Golden scripts at each anchor band; run monthly; track mean score by show |
> | **BIAS-NE-6** | §3 checklist | The checker's instructions describe perspectives in general, not by beat | `config/beats.yaml` checklists injected into the prompt by show beat |
