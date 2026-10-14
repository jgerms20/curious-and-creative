# Cold Case Files: show bible

**One unsolved case per episode, told from official and press records, ending with the agency's own tip line.**

| | |
|---|---|
| **Config** | `cold-case-files` in [`config/shows.yaml`](../../../config/shows.yaml) and [`config/evergreen/cold-case-files.yaml`](../../../config/evergreen/cold-case-files.yaml): market `national`, wave 0, enabled true |
| **Lane · format** | strict · `evergreen_story` |
| **Cadence · length** | Tue and Thu 05:00 ET (cron `0 9 * * 2,4` UTC) · 18-25 min |
| **Hosts · disclosure** | June (solo) · Script C ([AI Disclosure](../../standards/ai-disclosure.md) §3), about 22 s, spoken by Ava |

## 1. Premise
Some cases stay open because nobody has come forward. This series picks one real, publicly documented case where an agency is currently asking for information, tells what the record shows, says plainly what is unresolved and gives the agency's tip line. It does not solve cases, guess, name theories or invite amateur sleuthing (CR-16). It is **not** entertainment true crime: no monsters, no cliffhangers, no dramatized scenes.

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| Listeners who follow unsolved cases; communities where a case happened (regional spin-offs: Carolinas, Southern California) | Careful, exact telling that treats the victim as a person, and a reminder the case is open | Podcast apps, smart speakers |
| Investigators and families *(inference)* | An accurate, respectful public record that never goes past what the agency said | Show notes with agency links |

## 3. Format and segments
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | Open | The case in one sentence, "unsolved, and the agency is asking for tips" | 0:30 | June |
| 2 | The person | Who the victim was, from official or on-record family words only (CR-14) | 2:30 | June |
| 3 | What happened | Neutral timeline: date, what was reported, by whom | 6:00 | June |
| 4 | The investigation | What investigators have said on the record, what was tested | 6:00 | June |
| 5 | What is unresolved | The gaps in the record. Rumors stay out | 3:30 | June |
| 6 | Tip line and status | The agency's tip line read exactly from its current page; "still unsolved as of {date}" | 1:30 | June |
| 7 | **Disclosure** | Script C, always last (DISC-1) | 0:22 | Ava |

## 4. Sources
The queue holds generic topics (cc-01 to cc-10); the Cold-Case Archivist (Opus tier, `next`) finds one real case per topic. A case qualifies only if an agency has a current public page with a working tip line, the victim was an adult, it is not a sexual-assault, abuse or trafficking case, no living person is publicly named as a suspect, and the facts rest on records.
| Tier | Sources | How we use them |
|---|---|---|
| 1 official | Agency and state cold-case pages, medical examiner and coroner, NamUs public listings (index only, manual, F-DATA-09), FBI appeals (unverified API, F-DATA-07) | The case, the tip line, the status |
| 2 to 3 | Established and local newsrooms | Timeline in our words plus a link. At least 2 sources from different owners, one official |
| Leads only | Charley Project, Doe Network (copyrighted, no scraping), true-crime sites, forums, social posts | Find the record, then cite the record. Murder Accountability Project data is aggregate context only |

## 5. Lane and trust rules
- **Strict lane:** 2 independent sources, an official record for sensitive claims, no single-source claims, balance at least 75 ([Editorial Standards §2](../../standards/editorial-standards.md)).
- **Cold means** the agency calls it cold, or about 3 years with no arrest *(inference)* (CR-20). A pending charge, arrest or trial is not cold: skip.
- **Never name an uncharged suspect.** A genetic-genealogy lead is not a charge; never name or describe the relatives whose DNA matched. A dead suspect an agency named on the record may be named, attributed (CR-17, CR-10).
- **Unidentified remains:** nothing graphic beyond the agency's release, cite the case ID, wait for the agency or medical examiner and next of kin before any identification (CR-18).
- **Tip line** comes from the agency's page, re-verified within 7 days; "still unsolved" is re-checked within 7 days (CR-19). Never rebuild a withheld victim name from obituaries or filings (CR-12).
- **Never:** minors (NEVER-2, CR-21), sexual-assault survivors (NEVER-3), theories (NEVER-1), "brutal", "chilling", "monster".
- A family or subject request suppresses the named content within 24 hours; re-releasing an old episode can restart the defamation clock (Crime and Courts Rules §7; F-LEGAL-08).

## 6. Voice, disclosure and ads
June about 140 words a minute, deliberate, warm and serious, never theatrical. No music sting on an accusation or a victim's name; quiet bed or none. **Ads:** opt-in advertisers only, calm categories, no fear appeals, no law firms or bail bonds, nothing sold in the first 90 days *(inference)* (advertising plan §8). Best fit is a series sponsor or licensing ([products](../../business/products.md)).

## 7. Sample cold open (illustrative; braces are placeholders, not real events)
> **June:** This is Cold Case Files. In {month year}, {agency} began investigating the death of {an adult} in {county}. The case has not been solved, and {agency} is still asking the public for information.
> **June:** We tell this story from public records. We do not guess, and we do not name anyone investigators have not named. The agency's contact information is at the end of this episode.

## 8. Sample episode titles
- An unsolved 1980s homicide in {county}: what {agency} says, and how to reach them
- A disappearance after leaving work in the 1990s: the record and the open questions
- Unidentified remains found in {year}: what investigators are asking the public
- New forensic testing in a {decade} case: what {agency} has announced

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| Downloads per episode | 100 / 400 / 1,500 (cons / base / opt) | F-AUD-04 *(inference)* |
| Episodes with a verified tip line; "still unsolved" re-checked in 7 days | 100%; 100% | CR-19 |
| Uncharged people named; minors or survivors named | 0; 0 | CR-17, NEVER-2, NEVER-3 (gate `L2`) |
| Corrections; takedown requests suppressed in 24 hours | 0; 100% | AUTO-6; Crime and Courts Rules §7 |
| Cost per 22-minute episode | about $4 to $8 *(inference)*; Batch halves the Claude part | 2.2x F-LLM-07, F-LLM-05, F-TTS-17; as of Oct 2026 — verify before buying |

## 10. Open items
Owner: Showrunner: Evergreen & Archives (`next`); version 1.0, October 12, 2026. Owner calls still open (CR-21): deceased child victims, sexual-assault homicides, people who were minors in old cases; the safe defaults hold until decided. Media-lawyer review first (F-LEGAL-02). Regional spin-offs wait for waves 2 and 3.
