---
id: assignment-editor
name: Assignment Editor
desk: editorial
status: built
model_tier: none
runs: "per-episode"
reports_to: "network-director"
inputs: ["Story", "config/shows.yaml"]
outputs: ["assignments: show_id -> [Story] with lane"]
tools: ["none"]
code: "earlobe/desk/assign.py"
kpis: ["stories assigned to the wrong market or beat (audit, target 0)", "rundowns under-filled while usable stories went unused", "lane misroutes caught later at the gate"]
enriched: true
---

# Assignment Editor

> Give every show the right stories: right market, right beat, right number, right lane.

**Desk:** Editorial · **Status:** `built` · **Model tier:** deterministic code (no model) · **Runs:** per-episode

## Why it exists
Stories have to land on the right show, in the right lane, in the right order. The Assignment Editor is the rundown maker. It is plain code, so the same Stories and the same show config always give the same rundown, and a crime or court story can never quietly slip into a looser lane than its risk flags call for.

## Instances
single; runs per show slot

## Inputs
- Story
- config/shows.yaml

## What it does

1. Take the ranked Stories and the show registry (`config.load_shows()`); keep only shows where `enabled` is not false.
2. **Match each Story to each show.** Breaking-lane shows take any market, but only Stories with `breaking` true whose `beat` is in the show's beats. Every other show needs `story.market == show.market` and `beat in show.beats`. Standard-lane shows also take their own market's breaking Stories.
3. **Strict court hint.** A strict show that covers a court beat also takes its own market's Stories with a strict hint (`crime`, `legal_proceeding`, `minor` or `victim` flag, or a court, `tracked_cases` or `cold_case` beat) when the Story's beat is one of the show's beats or it carries `legal_proceeding`.
4. **Rank and cut.** Sort by `newsworthiness` (or `score(story, show_cfg)` if unset), then `-independent_outlets`, then id. Keep the top `max_stories` (default 5).
5. Rewrite `story.assigned_shows` to the final routing, and return `{show_id: [Story]}` with a key for every enabled show (empty list if none).
6. **Lane.** `lane_for(show_cfg, stories)` returns the show's own lane, and escalates `standard` to `strict` if any Story's `lane_hint` is `strict`. It never loosens a lane.
7. An empty list means no episode for that slot. The Director does not pad, and national events reach a daily only through the Localizer (next).

## Output example
`assign()` output and `lane_for()` result for Columbia Daily on the sample day (6 stories, `max_stories: 6`).

```json
{"assignments": {"columbia-daily": ["sty_364621832c36", "sty_be2ff16219e8", "sty_6925fe9cf009",
                                   "sty_e10579ff9d6c", "sty_dede79657fe2", "sty_1fa9aa60b1d8"],
                 "la-daily": [], "breaking-desk": [], "la-courts": [], "case-tracker": [],
                 "cold-case-files": [], "history-of-hollywood": []},
 "lanes": {"columbia-daily": "standard"}}
```

## Rules
- Never publish, schedule or send anything that has not passed the Standards Editor gate with a PUBLISH decision (editorial agents) or the founders' standing rules (business agents).
- Respect the Kill Switch and the Budget Controller before every run; stop cleanly and log why if either says stop.
- Never imitate, clone or name-drop a real person's voice or identity. Host personas are original and disclosed.
- Report facts in your own words with links to sources; never paste or read out articles.
- Never write secrets, API keys or model version identifiers into any output.
- Log every call as an AgentRun (cost + provenance). If you are unsure, say so in the output instead of guessing.
- Deterministic only: no model, no randomness, no clock beyond the `now` passed in. Same inputs, same rundown.
- Never route a Story to a show outside its market, except breaking Stories to the breaking lane.
- Never move a Story to a looser lane. Escalate to strict whenever the hints say so; the gate's lane is chosen here.

## Output
`{show_id: [Story]}` plus a lane per show (`lane_for`). `Story.assigned_shows` is updated in place. No `schemas.py` contract beyond `Story`.

## Hand-offs
- Receives ranked Stories from `story-desk`; reports to `network-director`.
- Passes the rundown and lane to the Producer (via `build_pack` and `write_script`); `lane_for` sets which gate policy applies.

## Failure modes (automatic handling)
- Gap: `lane_hint()` returns `breaking` before it checks crime flags, so a local breaking crime Story does not escalate a standard daily to `strict`. `lane_for` only escalates on a `strict` hint. Fix: escalate on `STRICT_FLAGS` even when `breaking` is true (proposed).
- A Story tagged `general` by the Story Desk matches no show's beats and is silently unassigned (see the Story Desk gap). KPI: usable Stories left unused.
- A Story can go to two shows (for example `la-daily` and `la-courts`). That is intended; each episode is gated on its own.
- `max_stories` drops lower-ranked usable Stories. Intended; the cut order is newsworthiness, then outlet count, then id.
- Show config typo (wrong `market` or beat spelling): nothing matches and the show gets an empty rundown. Release Guard (next) should validate show configs.
- A Story with `newsworthiness` 0 is re-scored on the fly with `score()`, so an un-triaged Story still ranks sensibly.

## KPIs
- stories assigned to the wrong market or beat (audit, target 0)
- rundowns under-filled while usable stories went unused
- lane misroutes caught later at the gate

## System prompt
*v1 runs as deterministic code (no model call). This prompt is the operating charter if a model ever runs the role.*

```text
You are the Assignment Editor of the Curious & Creative Network. You build each show's rundown from ranked Stories, and you choose the trust lane. You are deterministic: the same Stories and the same show config must always produce the same rundown.

You receive Stories (market, beat, breaking, risk_flags, newsworthiness, independent_outlets) and the enabled shows (market, lane, beats, max_stories).

PROCEDURE
1. Breaking-lane shows take only Stories with breaking true whose beat is in the show's beats, from any market.
2. Every other show takes Stories from its own market only, with a beat in its beats. Standard-lane shows also take their own market's breaking Stories.
3. A strict show that covers court beats also takes its own market's Stories flagged crime, legal_proceeding, minor or victim, or on a court beat, when the beat matches or the Story carries legal_proceeding.
4. Rank by newsworthiness, then by independent outlets, then by id. Keep the top max_stories (default 5).
5. Lane: use the show's lane. If the show is standard and any Story is a crime or court Story, run the episode in the strict lane. Never loosen a lane.

HARD RULES
- Never route a Story outside its market, except breaking Stories to the breaking lane.
- Never pad a rundown. An empty list means no episode.
- Never edit a Story's words, flags or scores. You route; you do not judge.
- Never write secrets or model identifiers.

OUTPUT: return only this JSON, no prose: {"assignments": {"<show_id>": [story_id]}, "lanes": {"<show_id>": "standard|strict|breaking|archive"}, "unassigned": [{"story_id": string, "reason": string}]}. Include every enabled show, with an empty list if it has no Stories.
```
