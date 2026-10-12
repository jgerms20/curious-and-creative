# Crime and Courts Rules

**The Curious & Creative Network: how we report accusations, arrests, cases and victims**

| | |
|---|---|
| **Applies to** | Every crime or court item on any show. Strict-lane shows: LA Courts Roundup, Case Tracker, Cold Case Files. Also crime items in Columbia Daily, LA Daily, any city daily, and The Breaking Desk |
| **Enforced by** | Gate rules `V3`, `V4`, `F1`, `B2`, `L1`, `L2` ([`earlobe/trust/gate.py`](../../earlobe/trust/gate.py)); `L1` and `L2` come from the Legal Screener, `F1` from the Fact Checker |
| **Parent page** | [Editorial Standards](editorial-standards.md) §5, §6, §7. If the two disagree, the Editorial Standards win |
| **Version** | 1.0, October 12, 2026. **Not legal advice.** As of Oct 2026 — verify; have a media lawyer review this page (F-LEGAL-02) |

**The 30-second version**

- A charge is an accusation, never a finding. We never say or imply guilt before a verdict or plea.
- Every legal word matches the court record **as of air time**, and never runs ahead of it.
- Allegations come from **official records** or on-record official statements, and we name who is alleging.
- We never name minors, people who say they were sexually assaulted, or people who haven't been arrested or charged.
- Victims are people. If a case ends well for the accused, we say so, with the same prominence.

---

## 1. The legal-word ladder

Say the word for the step the **record** shows, never a higher one. (Wording matches FC-LEGAL and Editorial Standards §5.)

| Step | Say | Only when the record shows | Never say |
|---|---|---|---|
| 1 | **arrested on suspicion of** | A booking or on-record police statement; no charges filed | "arrested for," "the suspect did" |
| 2 | **charged with** | Prosecutors filed a complaint or information (court record or prosecutor on the record) | "charged" after only an arrest; charges the record doesn't list |
| 3 | **indicted** | A grand jury returned an indictment | "indicted" for a complaint |
| 4 | **pleaded not guilty / guilty / no contest** | The plea entered, per the court record | "denied everything" in place of the plea |
| 5 | **convicted / found guilty** | A verdict, or a guilty plea accepted by the court | "convicted" at the plea hearing stage if not yet accepted |
| 6 | **sentenced** | A sentencing order | "faces up to 25 years" worded as a sentence |
| 7 | **acquitted / found not guilty** | A not-guilty verdict | "cleared," "got off," "walked," "innocent" |
| 8 | **dismissed / charges dropped / prosecutors declined** | A court order or the prosecutor on the record; say "with" or "without prejudice" if the record does | "cleared" unless the record says so |
| 9 | **mistrial** | A court order | "acquitted" |

- **CR-1.** Never higher than the record. A word above the best evidence is `inaccurate`; with no record of the stage it is `unverifiable`. · Gate: `F1`, `F2` · FC-LEGAL-2
- **CR-2.** Status as of air time. If the newest record is older than 7 days *(setting)* and the line states status flatly, check the docket or add the as-of date ("as of the last public docket entry on..."). · Gate: `F1`, `F2` · FC-LEGAL-3
- **CR-3.** Charge names, counts, defendants and penalties are exact, in the right court and case; same-name defendants are matched on more than a name. "Faces up to" is a maximum. Not guilty is not innocent. A settlement is not a finding. · Gate: `F1` · FC-LEGAL-4 to -6

---

## 2. Allegations come from official records only

**In plain words.** A police report shows what police say. A complaint shows what one side says. We report that they said it, not that it happened.

| Counts as an official record (tier 1) | Does **not** count |
|---|---|
| Court filings and dockets; charging documents; indictments | Social posts, except an official account on our source registry (SRC-11) |
| A prosecutor's or police department's on-record statement or release | Unnamed sources, in any outlet (ANON-2) |
| A coroner or medical examiner release | Aggregators, people-search and mugshot sites, forums, "justice for" pages, crowdfunding pages (NEVER-6) |
| Agency data and booking logs on the agency's own site | A viral video until tier 1-2 sources confirm its origin |

- **CR-5.** Every allegation names who is alleging it, in the same or the preceding sentence. "Allegedly" with no accuser is not attribution. Police and prosecutor narratives are "police said," "according to the complaint." · Gate: `L1` (`unproven_allegation`, `presumption_of_innocence`), `F1` · ATT-3, ATT-5 · see NE-6 in the Editorial Standards
- **CR-6.** In `strict` and `breaking`, every sensitive claim (crime, legal proceeding, named private person, minor, victim, death, or type `allegation` / `legal_status`) also needs an official record. · Gate: `V4` · SRC-9
- **CR-7.** Report the defendant's side when it exists on the record (plea, filing, statement). If none, say "We did not find a public response from..." We never say we "reached out" (we don't). · Gate: `B2` · FAIR-3
- **CR-8.** "Suspect" follows the agency's own on-record label. "Person of interest" names are not used. · Gate: `F1` · FC-LEGAL-8, FAIR-5

### Fair-report practice

**In plain words.** Many states protect a fair and accurate report of an official proceeding or record. The rule differs by state and the protection can be lost. We work in a way that keeps us inside it *(inference from F-LEGAL-10)*:

| Do | Don't (how protection is lost) |
|---|---|
| Attribute to the record or proceeding | Drop the attribution and state it as fact |
| Match the legal word and the current stage | Overstate the record or report a stale status |
| Include the plea or denial when it is on the record | Add our own embellishment, motive or color |
| Report the official act (a filing, a ruling) | Repeat a third party's side comment as if the court said it |

Basis by state (F-LEGAL-10, recalled, medium confidence): California Civil Code 47(d); New York Civil Rights Law 74; Illinois common law; South Carolina common law (confirm).

Private people charged with crimes are our most exposed subjects (F-LEGAL-09). Section 230 does not shield our own scripts (F-LEGAL-11). **Consult counsel** on state differences before Case Tracker and Courts Roundup go live.

---

## 3. Who we never name

| Who | Rule | Gate | Notes |
|---|---|---|---|
| **Minors** in any role (suspect, defendant, victim, witness), including people who were minors at the time of old events, and "jigsaw" pieces (parent's name, address, school plus detail) | NEVER-2 | `L2` `naming_minor`, **any severity, every lane** | Stricter than the law on purpose: juvenile court files are generally confidential |
| **People who say they were sexually assaulted, abused or trafficked**, and identifying details | NEVER-3 | `L2` `naming_victim`, any severity, every lane | No exceptions today, even if another outlet named them |
| **Uncharged suspects** and "persons of interest" | FAIR-5 | `V4` (strict, breaking), `L1` | Name only after arrest or charge, or when an agency names them on the record |
| **The dead**, before an official release or on-record family statement | BRK-10 | `V4` (`death`), strict and breaking only | Next of kin must be notified first. See NE-9 |
| **Private people in low-level matters** | FAIR-6 | `V3`, `V4`, `L1` (`privacy`) | Name only when the story can't be understood without it |
| **Juvenile, family, probate, sealed or expunged records** | Proposed | None | Stop naming once sealed, expunged or diverted. See CR-NE-5 |

- **CR-9.** When the Legal Screener is unsure whether something is a hard-stop category, it flags it. A name flagged by `L2` can never publish. · Gate: `L2`
- **CR-10.** Evergreen shows (Cold Case Files, History of Hollywood) never name a living private person who is only accused; they can't keep that story current. *(Inference, from research.)* · see CR-NE-4

---

## 4. Victims and families

- **CR-11.** The victim is a person, not a plot device. No graphic detail beyond what the story needs. No cliffhangers over a death. · Gate: `B2` (`sensationalism`) · FAIR-10
- **CR-12.** Name a victim only after an official release (police, coroner, medical examiner) and next-of-kin notification, and never in the excluded categories above. Do not reconstruct a withheld name from obituaries or filings. · Gate: `V4` · BRK-10
- **CR-13.** Cause and manner of death come from the coroner or medical examiner, attributed. We don't guess. · Gate: `B2` (`speculation`), `F1`
- **CR-14.** Nothing about a victim's clothing, past, lifestyle or condition unless an official finding makes it relevant. Never invent a family quote or characterize grief; use only what the family said publicly, word for word. · Gate: `B2`, `F1` · NEVER-4
- **CR-15.** Episode titles, descriptions, show notes and social copy follow the same rules. No verdict words unless a verdict exists: "faces charges," "is accused," "is charged." No titles like "The Man Who Killed..." **No mugshots** in show notes, art or social posts, and mugshot sites are not sources. · see CR-NE-2

---

## 5. When charges drop: follow-through

If we reported an arrest or charge, we report how it ended (FAIR-11). All timings are *settings* from the research notes, not facts *(inference)*.

| Outcome | What we do | Target |
|---|---|---|
| Dismissed, declined, charges dropped, acquitted | Follow-up with the **same prominence** as the original. Original episode gets an update `note`; for a private person, a `reissue` with the name removed | Follow-up within 72 hours of learning of it |
| Diverted, sealed or expunged | Stop naming the person. Do not republish the old name | Same day |
| Convicted or sentenced | Report it, with the legal word from the order | Next relevant episode |
| Not yet known | Weekly docket sweep for **every** person we have named in Case Tracker or Courts Roundup | Weekly |

Never edit silently (AUTO-7). Procedure: [Corrections Policy](corrections-policy.md). · see NE-14

---

## 6. Cold-case care

- **CR-16.** No solving, speculating or crowdsourcing. No theories from forums or amateur sites (NEVER-1, NEVER-6). · Gate: `B2` (`speculation`)
- **CR-17.** Never name an uncharged suspect. A genetic-genealogy lead is not a charge. Never name or describe the relatives whose DNA matched. A dead suspect an agency named on the record may be named, attributed. · FAIR-5
- **CR-18.** Unidentified remains: nothing graphic beyond what the agency published; cite the case ID; wait for the agency or medical examiner and next-of-kin before an identification.
- **CR-19.** Every episode ends with the agency's own tip line, read from its current page and re-verified within 7 days. "Still unsolved" is also re-checked within 7 days. · VP rules
- **CR-20.** Treat a case as "cold" only when the agency calls it cold, or it is about 3 years old with no arrest *(inference; confirm with counsel or a former investigator)*. Otherwise it is an active investigation.
- **CR-21.** Open owner decisions, with safe defaults for launch: missing **minors** (exclude entirely); deceased **child** victims (keep the hard stop: "a nine-year-old girl," agency tip line); deceased victims of **sexual-assault** homicides (default no name); people who were minors in old cases (keep the stop).

---

## 7. Takedown and subject requests

A family, a named person or an outlet can ask us to correct, remove a name, or remove a detail. *(Inference: all numbers are recommended settings; the intake channel is not built.)*

| Step | Rule |
|---|---|
| Intake | Visible contact on every show page and feed. Every request becomes a `Correction` (`reported_by`: `subject`, `listener` or `outlet`) |
| Immediate | If it involves a minor or a sexual-assault victim, or a credible legal threat: **suppress the feed item first, review after**, and alert the owners within 1 hour |
| Credible request | Suppress the named content within 24 hours; decide within 7 days |
| Decision | Judge the evidence, not who asked. Factual error: [Corrections Policy](corrections-policy.md). Accurate but harmful (dismissed charge, private person): consider removing the name |
| Record | The answer goes in the public trust log, without repeating the name of a minor or a sexual-assault victim |

---

## 8. Map to the gate

Strict lane values (`POLICIES["strict"]`) beside the standard lane the dailies run in:

| Setting | `strict` (Courts, Case Tracker, Cold Case) | `standard` (dailies) | `breaking` |
|---|---|---|---|
| `min_independent` | 2 | 2 | 3 |
| `official_satisfies` | yes | yes | no |
| `allow_attributed_single` | **no** | yes | no |
| `sensitive_needs_official` (**V4**) | **yes** | no | yes |
| `min_balance` (**B1**) | **75** | 70 | 70 |
| `legal_block_severity` (**L1**) | **medium** | high | medium |

| Gate rule | What it does here | Standards |
|---|---|---|
| `V3` | Needs the lane's independent sources, or one official record where allowed | CR-5, CR-6 |
| `V4` | Strict and breaking: a sensitive claim needs a tier-1 record | CR-6, CR-8, CR-12 |
| `F1` / `F2` | Ladder word, status, counts, names and court must match the record | CR-1 to CR-3, CR-13 |
| `B1` / `B2` | Score of 75 on strict; high-severity implied guilt, speculation, sensationalism | CR-7, CR-11, CR-14, CR-16 |
| `L1` | Medium or higher blocks on strict and breaking (`unproven_allegation`, `presumption_of_innocence`, `privacy`) | CR-5, CR-8, CR-10 |
| `L2` | `naming_minor` / `naming_victim`: blocks at any severity, rewrite, then KILL | CR-9 |

---

## 9. Not yet enforced in code

> **Not yet enforced in code.** Until these checks land, these rules rely on the agents' instructions and on rechecks after publication. Proposed ids are placeholders. See also **NE-6, NE-9, NE-14** in the Editorial Standards.
>
> | # | Standard | The gap today | Proposed check |
> |---|---|---|---|
> | **CR-NE-1** | Strict handling of crime stories | The dailies run `standard`: `V4` is off and `L1` blocks only at high, so a medium `presumption_of_innocence` or `unproven_allegation` issue can air in a daily | **Lane escalation**: any script with a claim flagged `crime`, `legal_proceeding`, `victim` or `minor` is gated with strict `V4` and `L1` values, whatever the show lane |
> | **CR-NE-2** | CR-15: titles and social copy | The Legal Screener sees script lines and claims only | Run title, description, notes, transcript and social copy through the Legal Screener and Bias Checker; title word check |
> | **CR-NE-3** | Sensitive means flagged | `V4` fires only on `allegation` / `legal_status` types or risk flags. A crime fact typed `fact` with no `crime` flag skips it | Claim extractor forces type `legal_status` and flag `crime` when claim text contains ladder words (arrested, charged, indicted, pleaded, convicted, sentenced, acquitted, dismissed) |
> | **CR-NE-4** | CR-10: evergreen rule | The Legal Screener isn't told the show's format | Pass `show_id` / format to the screener; treat an accused living private person as high in evergreen shows |
> | **CR-NE-5** | Sealed, expunged, juvenile | No `sealed` marker on sources or claims; court portals can seal records or hide juvenile files (F-DATA-10) | Sweep marks sealed/expunged; a protected-names list blocks the name in every later script and title |
> | **CR-NE-6** | CR-9: hard stops rest on an AI's reading | `L2` fires only if the Legal Screener flags it. No deterministic name list | **L3**: once a minor or victim is identified in any run, store a protected list and scan future text (exact and fuzzy) |
> | **CR-NE-7** | Section 7: takedowns | No intake channel, no per-episode suppress. Kill switch is per show or whole network; feed drops only `retracted` | Add a `suppressed` episode status excluded from the feed (needs `schemas.py` and `json-contracts.md` together) |
