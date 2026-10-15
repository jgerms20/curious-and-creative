# Corrections Policy

**The Curious & Creative Network: how we find, fix and publicly record our mistakes**

| | |
|---|---|
| **Applies to** | Every episode on every show, including show notes, titles, descriptions, transcripts and social copy |
| **Publisher of record** | Curious & Creative LLC. Never "the AI" (AUTO-1) |
| **Run by** | Re-check Monitor, Corrections Agent (Sonnet tier), Transparency Reporter. Specs: [`agents/trust/`](../../agents/trust/). Records: [`earlobe/publish/trustlog.py`](../../earlobe/publish/trustlog.py), `Correction` in [`earlobe/schemas.py`](../../earlobe/schemas.py) |
| **Parent page** | [Editorial Standards](editorial-standards.md) §15 (AUTO-1 to AUTO-10) and NEVER-11. If the two disagree, the Editorial Standards win |
| **Version** | 1.0, October 12, 2026. As of Oct 2026 — verify; timings below are our *settings* *(inference)*, not legal requirements. **Not legal advice** |

**The 30-second version**

- Anyone can report an error. Reports are judged on evidence, not on who sent them or whether they advertise.
- We also check ourselves: published claims are re-verified automatically for **7 days** after air.
- Three fixes: **note** (minor), **reissue** (new audio), **retract** (pull the episode). Never silent.
- Material fixes are said out loud in the next episode of the same show.
- Every correction goes in the public trust log. Every month we publish the numbers, including the bad ones.

---

## 1. How to report an error

| Channel | What happens |
|---|---|
| **Corrections link in every episode's show notes** (`/corrections/<show_id>`, built by `corrections_url()`) | Form or email; becomes a `Correction` |
| **corrections@ mailbox** (and a separate legal-notice contact for demands) | Read by the Corrections Agent, with a human backup for legal items *(inference, from the legal note)* |
| **Comments, social replies, outlet and subject emails** | Community Manager routes them in |

A good report names the **episode**, the **sentence** (or time stamp), **what is wrong**, and **evidence** (a link or document). We act on weaker reports too. We don't publish the reporter's name or address.

- **COR-1.** Every report becomes a `Correction` with `reported_by` set to `listener`, `outlet`, `subject` or `monitor:recheck` (the field is free text, so `subject` needs no schema change). · AUTO-5
- **COR-2.** Reports are judged against evidence. Who complained, and whether they advertise or sponsor, never matters. · AUTO-5, COI-1

---

## 2. The automatic 7-day re-check

Every published episode is re-verified **for at least 7 days** after air (AUTO-4). Agent spec: cron `0 8 * * *` daily, with breaking and strict claims more often in the first 48 hours.

| Re-check | What it looks at | If it moved |
|---|---|---|
| **Counted sources** | Re-read each source we counted; flag a retracted, deleted or changed one; recompute `independent_count` | Source gone: recount. Below the lane bar: open a `Correction` |
| **Legal status** | Latest docket entry for every named case (dismissal, plea, verdict, sealing) | Wrong at air time: correction. Changed after air: an **update** (§5) |
| **Numbers** | Casualty counts, vote tallies, budgets against the newest official release | Same split: error vs. update |
| **Present tense** | "Still unsolved," "remains open," "is in office" in strict and archive episodes | Fresh search within 7 days; fix if stale |
| **Contradiction** | A claim the evidence now contradicts | Open a `Correction` with `reported_by: monitor:recheck` |

*(Setting, proposed.)* Cadence by lane: `breaking` at 1, 6, 24 and 48 hours, then daily; `strict` at 6, 24 and 48 hours, then daily; `standard` and `archive` daily. After day 7, a weekly docket sweep covers everyone we named in Case Tracker and Courts Roundup (see the [crime rules](crime-and-courts-rules.md)).

- **COR-3.** The monitor decides **error vs. update** from dates: was the claim wrong when we aired it, or right then and changed since? It needs dated evidence (FC-NE-9 in the Fact-Check Protocol). Strict and breaking claims are rechecked 100% (agent KPI). · AUTO-4

---

## 3. Severity levels

Severity picks the action. **When in doubt, go up one level.**

| Level | Name | It is when | Examples (made up) | Action |
|---|---|---|---|---|
| **C1** | Minor | The meaning of the story and any fact a listener would rely on are unchanged, and no named person in a crime or court story is involved | Misspelled name in the show notes; wrong outlet in the source list; wrong chapter title | `note` |
| **C2** | Material | A fact a listener would rely on changed; **any** error about a named person in a crime or court story; a wrong legal word or status; a missing or misplaced AI disclosure (VOICE-3) | "Charged" when only arrested; wrong number or date; wrong defendant | `reissue` |
| **C3** | Critical | The central claim was wrong, **or** a NEVER rule (§7) was broken | Naming a minor or sexual-assault victim; an invented quote; presenting speculation as fact; claiming reporting we didn't do | `retract` |

C1 to C3 is a working scale for this page. `Correction` has `action` but no `severity` field yet (see COR-NE-1). The action table is Editorial Standards §15.

---

## 4. Timelines

Clocks start when the report arrives or the monitor detects the problem. These are **outer limits**; the Corrections Agent's target is a **median under 4 hours** from opened to applied (agent KPI). All are our settings *(inference)*.

| | Pull from feed | Acknowledge a report | Decide | Public fix live | Said on air |
|---|---|---|---|---|---|
| **C1** | n/a | 24 h | 72 h | Dated note in show notes and trust log within 1 h of the decision | No |
| **C2** | n/a | 24 h | 72 h (24 h if it concerns a named person in a crime or court story) | Show notes and feed text within 1 h; corrected audio within 24 h of the decision | Next episode of the same show |
| **C3** | **Within 1 h** of detection or a credible report. Pull first, review after | 24 h | 24 h | Retraction notice within 1 h of the pull | Next episode of the same show |

- **COR-4.** A credible **legal threat or takedown demand** goes to the owners within 1 hour, in addition to the clocks above. · see [crime rules §7](crime-and-courts-rules.md)
- **COR-5.** A published breach of a hard stop (`naming_minor`, `naming_victim`) is C3, pulled within 1 hour, with an owner alert. · NEVER-2, NEVER-3

---

## 5. Note, audio reissue or retraction

Ask the questions in order. The first yes decides.

| # | Question | Action | What the listener sees |
|---|---|---|---|
| 1 | Is the central claim wrong, or was a NEVER rule broken? | **Retract** (status `retracted`) | Episode leaves the feed on the next rebuild; a retraction notice stays on the corrections page; said on air next episode |
| 2 | Does it change a fact a listener would rely on, or concern a named person in a crime or court story? | **Reissue** (status `corrected`) | Corrected audio replaces the episode; dated note says what changed; said on air next episode |
| 3 | Otherwise | **Note** | Dated line in show notes and the trust log. No new audio |
| 4 | Was the claim right when aired and changed since? | **Update** (labeled "Update," not "Correction") | Dated update in show notes; new episode if it is news |
| 5 | Does the evidence show no error? | **Reject** (status `rejected`) | The reason is logged; the claim and outcome appear in the trust log without the reporter's identity |

- **COR-6.** Reissued audio is a **new publication**. It is regenerated from a corrected script and must pass the full gate with `PUBLISH`. A correction is no shortcut (AUTO-2). Re-releasing archive episodes can restart a defamation clock (F-LEGAL-08).
- **COR-7.** A retracted episode's audio file comes off public hosting. Podcast apps may keep cached copies and we can't recall them. We say so if asked.
- **COR-8.** Corrections never repeat the name of a minor or a sexual-assault victim, and don't repeat a harmful claim beyond what's needed to identify the error. The `description` is **public as written** (the show notes and trust log print it).
- **COR-9.** Every change is dated and says what changed. No silent edits (AUTO-7, NEVER-11).

### The spoken correction

Read by the show's regular host in the **first segment**, not the end. The AI disclosure still closes the episode.

> "A correction. In [day]'s [show], we said [what we said, in plain words]. That was wrong. [What is correct.] The corrected episode and the details are in the show notes."

Say what was wrong and what is right. No passive "mistakes were made," no "the AI got it wrong" (AUTO-1), no new speculation.

---

## 6. The public trust log

One JSON line per event in `data/public/trustlog/<show>.jsonl` (`publish/trustlog.py`). It records **every** decision, not just PUBLISH. Re-appending an identical record does nothing.

| Field | Meaning |
|---|---|
| `show_id`, `event` | Show; `gate` or `correction` |
| `episode_id`, `script_id`, `date` | Which episode (or script, if it never aired) and when |
| `decision`, `lane`, `revision` | PUBLISH, REWRITE, HOLD or KILL; the lane; rewrite count |
| `rules` | Rule ids that fired (`V3`, `B2`, `L2`...) |
| `scores` | `corroboration_rate`, `accuracy_rate`, `balance_score`, `claims` |
| `source_count` | Sources used |
| `corrections` | `id`, `action`, `claim_id`, `reported_by`, `status`, `summary` |
| `history`, `logged_at` | Per-revision decisions; time logged |

- **COR-10.** A correction is logged within 1 hour of being applied, as its own line (`event: correction`). · AUTO-3, AUTO-7
- **COR-11.** Keep scripts, source packs, trust logs and pre-correction versions for **at least 3 years** (F-LEGAL-08: limitation periods are 1 year in CA, NY and IL and 2 in SC).

---

## 7. Monthly transparency metrics

Published on the 1st of each month by the Transparency Reporter (spec status `next`), by show and lane. Numbers come from the logs; the model writes only the words around them. With fewer than 20 episodes in a month *(setting)*, show counts, not percentages.

| Metric | Source |
|---|---|
| Episodes published, held, killed | `decision` counts |
| First-pass PUBLISH rate; REWRITE, HOLD, KILL rates | `decision`, `revision` |
| Five most-fired gate rules | `rules` |
| Claims checked; mean `corroboration_rate`, `accuracy_rate`, `balance_score` | `scores` |
| Hard-stop catches (`L2` count only, no names) | `rules` |
| Corrections opened, by source (`monitor:recheck`, `listener`, `outlet`, `subject`) | `reported_by` |
| Corrections by action (note, reissue, retract) and, once logged, by severity | `action` |
| Corrections per 100 published claims | corrections / `claims` |
| **Self-detection share**: corrections the monitor found before any outside report | `reported_by` |
| Median and 90th-percentile time to acknowledge, decide and apply; share inside the outer limits | timestamps (COR-NE-1) |
| Significant corrections said on air in the next episode (target 100%) | on-air log |
| Repeat errors of the same type | rule or error category |
| Retractions, with reason category | `retract` lines |
| Takedown and subject requests received, resolved, median days (no names) | request log |
| Rules changed because of errors (AUTO-10), with change-log link | change log |

Also list notable catches (an episode killed by `L2`, a story held then confirmed) in plain language, with no names of private people.

---

## 8. Rules not listed above

- **COR-12.** Each C2 or C3 gets a short root-cause note: why did the gate miss it? The answer is a rule change or a new test fixture, logged in the change log the same day (AUTO-9, AUTO-10).
- **COR-13.** California's retraction statute (Civil Code 48a) limits damages when a correction is demanded within 20 days and made within 3 weeks. Whether it covers a podcast is unsettled (F-LEGAL-11). Our limits sit well inside those windows. **Consult counsel.**

---

## 9. Not yet enforced in code

> **Not yet enforced in code.** Agent specs mark the Re-check Monitor and Corrections Agent `built`, but `earlobe/monitor/` held only `__init__.py` when this page was written (verify). The Editorial Standards list the same gap as **NE-14**. Proposed ids are placeholders.
>
> | # | Standard | The gap today | Proposed check |
> |---|---|---|---|
> | **COR-NE-1** | §3 severity, §4 timelines, §7 time metrics | `Correction` has no `severity`, `acknowledged_at`, `decided_at` or `applied_at`; status is only `open`, `applied`, `rejected` | Add the fields in `schemas.py` and `json-contracts.md` together; log them in the trust log |
> | **COR-NE-2** | §1 intake | `corrections_url()` builds `/corrections/<show_id>`; `publish/` has no page or form behind it | Corrections page with intake form and mailbox routing |
> | **COR-NE-3** | COR-6, AUTO-2 | The publish step isn't built, so nothing proves a reissue passes the gate (**NE-13**) | Publish step refuses anything but `PUBLISH`, corrections included |
> | **COR-NE-4** | COR-8 | `description` prints verbatim in show notes and the log. Nothing checks it for a minor's or victim's name | Run correction text through the Legal Screener and the protected-names list (CR-NE-6 in the crime rules) |
> | **COR-NE-5** | §4 and §5 | No spoken-correction line and no owner alert on KILL, `L2` or retract (**NE-14**) | Producer reads open `reissue`/`retract` items; owner alert |
> | **COR-NE-6** | COR-7, takedowns | Feed drops only `retracted`; no episode-level suppress | `suppressed` status (CR-NE-7 in the crime rules) |
> | **COR-NE-7** | COR-3 | `EvidenceSource` has no dates, so error vs. update can't be decided in code (FC-NE-9) | Add `published_at` and `retrieved_at` to `EvidenceSource` |
> | **COR-NE-8** | §7 | The Transparency Reporter is `next`; no aggregation job | SQL over trust log and store; reconcile counts to the log (agent KPI: 100%) |
