# The Breaking Desk: show bible

**Short, calm updates on major national and global events that say what is confirmed, who confirmed it, and what is still unknown.**

| | |
|---|---|
| **Config** | `breaking-desk` in [`config/shows.yaml`](../../../config/shows.yaml): market `national`, wave 0, enabled true |
| **Lane · format** | breaking · `breaking_flash` |
| **Cadence · length** | Event trigger `desk.breaking`, at least 30 min between flashes · 2-4 min |
| **Hosts · disclosure** | Ava (breaking anchor, solo) · Script B ([AI Disclosure](../../standards/ai-disclosure.md) §3), about 11 s, also Ava |

## 1. Premise
The first hour of a big story is when wrong names, wrong death tolls and rumors spread. The Breaking Desk waits for confirmation, then tells you three things: what is confirmed, by whom, and what is not yet known. If a story is real but unconfirmed, we say nothing yet. It is **not** a live blog, a rumor tracker or a push-alert factory. Beats: major deaths, attacks, disasters, the Supreme Court, the federal government, space, mega sports, mega business and world events.

## 2. Audience
| Who | What they need | Where they listen |
|---|---|---|
| Anyone who hears "something happened" | One calm, reliable update in three minutes | Podcast apps, smart speakers, clips |
| Our local listeners; later, partners *(inference)* | The national event with a local angle (the Localizer routes it to the dailies); a verified-first feed to carry | The city dailies; syndication (`future`) |

## 3. Format and segments
A flash is one run of five beats; a later flash on the same event says what changed (BRK-12). Once facts settle, the Showrunner may fold a run of flashes into one explainer.
| # | Segment | Job | Time | Voice |
|---|---|---|---|---|
| 1 | Headline and time | "As of {time} {zone}, {what happened}, {where}" | 0:10 | Ava |
| 2 | Confirmed | Each fact, with the named official source | 1:00 | Ava |
| 3 | Not yet known | Specific open questions, no guessing | 0:30 | Ava |
| 4 | What happens next | Only scheduled items (a briefing, a hearing, a launch window) | 0:20 | Ava |
| 5 | Close | "We will update when more is confirmed" | 0:10 | Ava |
| 6 | **Disclosure** | Script B, always last (DISC-1) | 0:11 | Ava |

## 4. Sources
Feeds are in `config/sources/national.yaml`, all `verified: false` (F-DATA-04). The Breaking Detector scans every 5 minutes on fixed rules (BRK-1).
| Tier | Sources | How we use them |
|---|---|---|
| 1 official | NWS (extreme), National Hurricane Center, USGS, White House, DOJ, Supreme Court (CourtListener `scotus`), NASA, SEC, CDC, coroner and police releases | Confirmation. Casualty numbers and names come only from here |
| 2 | NPR, BBC, NYT, Guardian, CBS, ABC, NBC, PBS, Al Jazeera; AP and Reuters through the news and GDELT sensors (F-DATA-03) | Independent confirmation. Wire copy counts as the wire; one owner group counts once |
| Leads only | Social posts, viral video | Never proof (NEVER-6) |

## 5. Lane and trust rules
- **3 independent owner groups** per claim; one official record does **not** substitute (BRK-2). No single-source claims, even attributed (BRK-4). **Sensitive claims** (deaths, crimes, suspects, victims, legal status, named private people, minors) also need an official record (BRK-3).
- **Hold, do not guess:** if only the confirmation rules block, the gate waits 15 minutes and checks again, up to 6 times (90 minutes), then cuts what is unconfirmed or the flash does not air (BRK-5). One rewrite, then KILL (BRK-6). Medium-severity legal issues block (BRK-7).
- **Casualty numbers:** official, attributed, "at least", time-stamped (BRK-8). **No suspect names, motives or ideologies** until an official source states them on the record (BRK-9). **Names of the dead** only after an official release or an on-record family statement (BRK-10).
- Every flash says what is confirmed, by whom, and what is unknown (BRK-11).
- **Never:** "developing", "sources say", "reportedly" with no outlet (ATT-7); speculation about cause; a guess at a number.

## 6. Voice, disclosure and ads
Ava is flat-calm, short declaratives, time-stamped, no hype (Guide §2, §3). No bed under facts; one short alert tone at most. Ava is also the network's one disclosure voice. **Ads:** none at launch. Deaths, attacks and disasters stay ad-free for good, and sponsor delivery pauses on the affected market's next daily *(inference)* (advertising plan §2, §8).

## 7. Sample cold open (illustrative; braces are placeholders, not real events)
> **Ava:** This is The Breaking Desk. As of {time} {zone}, {event} in {place}.
> **Ava:** Confirmed: {fact}, according to {named official source}. {Second fact}, according to {second source}.
> **Ava:** Not yet known: {open question}. We will update when more is confirmed.

## 8. Sample episode titles
- {Event} in {place}: what is confirmed as of {time} {zone}
- Update: {coroner or agency} gives a figure for the {event}; what changed since {earlier time}
- Supreme Court rules in {case}: what the opinion says
- {Storm}: {agency} warnings in effect for {region}

## 9. KPIs
| KPI | Target | Basis |
|---|---|---|
| Downloads per flash | 150 / 500 / 2,000 (cons / base / opt) | F-AUD-04 *(inference)* |
| Flashes later corrected; flashes with confirmed / by whom / not-yet-known | 0; 100% | Showrunner KPI; AUTO-6; BRK-11 |
| Minutes from trigger to published flash (median); holds ending in PUBLISH versus KILL | set after the first 30 flashes, no sourced number; tracked | Showrunner KPIs *(inference)* |
| Cost | about 30 flashes a month in the cost model | `finance/build_cost_model.py`, as of Oct 2026 — verify before buying |

## 10. Open items
Owner: Showrunner: The Breaking Desk (`next`); version 1.0, October 12, 2026. Feeds unverified. Spin-offs (Weather & Disasters, Courts, Sports, Space, Markets, Spanish) wait for volume; see the [lineup](../network-lineup.md). Many near-identical short episodes can trip YouTube's "inauthentic content" rule (F-HOST-13), so titles stay specific. Re-check platform AI rules quarterly (F-HOST-15 to 17).
