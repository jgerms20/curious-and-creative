# History of Hollywood: show bible

**Narrative history of the American film industry and the Los Angeles places around it, told from records and never from the legend.**

| | |
|---|---|
| **Config** | `history-of-hollywood` in [`config/shows.yaml`](../../../config/shows.yaml) and [`config/evergreen/history-of-hollywood.yaml`](../../../config/evergreen/history-of-hollywood.yaml): market `los-angeles`, wave 0, enabled true |
| **Lane · format** | archive · `evergreen_story` |
| **Cadence · length** | Mon, Wed, Fri 02:00 PT (cron `0 9 * * 1,3,5` UTC) · 15-20 min |
| **Hosts · disclosure** | Lena (solo) · Script D ([AI Disclosure](../../standards/ai-disclosure.md) §3), about 14 s, spoken by Ava |

## 1. Premise
Every episode takes one documented moment, from the move west in the 1910s to the studio system, sound, color, the Production Code, the antitrust case and television, and tells it in plain order: the setting, the stakes, the turn, and why it still matters. Where studio publicity and the contemporary press disagree, we say so and attribute both. It is **not** gossip, a film review or a celebrity profile, and it never plays film clips or recreates a voice.

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| Film and Los Angeles history fans; Angelenos curious about landmarks | A true story they can trust, with the legend labeled | Podcast apps, smart speakers, clips |
| Teachers, students and evergreen sponsors *(inference)* | Sourced episodes with dated references; a brand-safe back catalog | Show notes, transcripts, media kit |

## 3. Format and segments
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | Cold open | A documented moment, in scene, from records | 1:00 | Lena |
| 2 | Setting | The place, the time, who was involved | 3:00 | Lena |
| 3 | Stakes | What was at risk and what people wanted | 3:00 | Lena |
| 4 | The turn | What happened, with conflicting accounts attributed | 5:00 | Lena |
| 5 | Legend and record | Label publicity and legend: "the story studio publicists told was..." (FAIR-12) | 2:00 | Lena |
| 6 | Why it matters; close | The link to today; one idea to remember; sources are in the show notes | 3:00 | Lena |
| 7 | **Disclosure** | Script D, always last (DISC-1) | 0:14 | Ava |
The queue holds 15 topics (hh-01 to hh-15), five weeks at three a week. A season plan of 8 to 12 episodes with an arc comes from the Showrunner.

## 4. Sources
Primary records first; dates, box-office figures, counts and quotations only when a listed source states them.
| Tier | Sources | How we use them |
|---|---|---|
| 1 | Library of Congress and Chronicling America (F-DATA-08), National Archives catalog, Calisphere and state and university collections, city and county records, court decisions, institutions' own histories | Facts, documents, dates |
| 2 to 3 | Margaret Herrick Library published finding aids, Media History Digital Library trade papers, contemporary newspapers, reputable published histories | Context and corroboration, in our words |
| Leads only | Encyclopedias, fan sites, blogs, forums | Find the record, then cite the record |
Never scrape or quote licensed archives such as Newspapers.com (F-DATA-11). Quote only public-domain, government or openly licensed items, briefly, source named (COPY-7): published works to 1930 are public domain now and 1931 follows on 2027-01-01 (F-LEGAL-17).

## 5. Lane and trust rules
- **Archive lane:** 2 independent sources, one official record suffices, one attributed source is acceptable for low-risk claims, balance at least 65, 2 rewrites ([Editorial Standards §2](../../standards/editorial-standards.md)).
- **Legends are labeled** (FAIR-12). **Money across years** is adjusted, or the script says "not adjusted for inflation" (NUM-5). The same fairness rules apply to people who have died.
- **People:** public, documented, professional facts only. No health, family or sexual-conduct detail, and no allegation never resolved on the record.
- **Never:** invent dialogue, thoughts or scene detail (NEVER-1); recreate a real person's voice (NEVER-4); play film clips (COPY-7); name a person who was a minor at the time of events in a crime or abuse story (NEVER-2).

## 6. Voice, disclosure and ads
Lena is the unhurried storyteller here, about 145 words a minute. Quotes are read in Lena's own voice and signaled (QUO-5, QUO-6). Film titles are read as titles; archaic or foreign names get lexicon entries from reference sources (for example DeMille: duh-MILL). Music beds are licensed or original (COPY-6, F-LEGAL-06). **Ads:** on, two slots; breaks next to a tagged death or crime segment are restricted (advertising plan §8). Script D says no real person's voice was recreated, true only while we never synthesize one.

## 7. Sample cold open (illustrative; real episodes cite their sources)
> **Lena:** In the early 1910s, filmmakers began leaving the East Coast for Southern California. This is History of Hollywood. Today: why they went, and what Los Angeles offered.
> **Lena:** We tell this from records: newspapers of the time, city documents and trade papers. Where the studios' own story differs from the record, we will say so.

## 8. Sample episode titles (from the queue)
- The move of film production to Southern California in the 1910s
- The Hollywood sign, from a real estate advertisement to a landmark
- The arrival of synchronized sound and the end of the silent era
- The Paramount antitrust case and the end of studio-owned theater chains

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| Downloads per episode | 400 at the cost model's input, unresearched | `finance/build_cost_model.py` |
| Back-catalog listens per month; first-draft PUBLISH rate in the archive lane | rising *(inference)*; tracked | Showrunner KPIs |
| Corrections; episodes with an unlabeled legend | 0; 0 | AUTO-6; FAIR-12 |
| Paid placements by day 90 | 1 (History of Hollywood Slot A) | Advertising plan §11 |
| Cost per 18-minute episode | about $3 to $7 *(inference)*; Batch halves the Claude part | 1.8x F-LLM-07, F-LLM-05, F-TTS-17; as of Oct 2026 — verify before buying |

## 10. Open items
Owner: Showrunner: Evergreen & Archives (`next`), research by the Archive Miner (Sonnet tier, `next`); version 1.0, October 12, 2026. Add a season plan and refill the queue before week 5. Re-check the public-domain line each January. Confirm the music library license before launch.
