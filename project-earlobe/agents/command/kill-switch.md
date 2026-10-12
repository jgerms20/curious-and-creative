---
id: kill-switch
name: Kill Switch
desk: command
status: built
model_tier: none
runs: "per-episode (checked at every stage boundary)"
reports_to: "founders (Joshua German, Janel Moore)"
inputs: ["EARLOBE_KILL env", "config/killswitch.yaml", "Incident Commander trips (next)"]
outputs: ["killed true/false", "kill log entry"]
tools: ["none"]
code: "earlobe/monitor/killswitch.py"
kpis: ["episodes published while killed (target 0)", "stages that ran after a kill was set (target 0)", "automatic trips with a recorded reason (100%)"]
enriched: true
---

# Kill Switch

> Stop one show or the whole network instantly, with one setting.

**Desk:** Command · **Status:** `built` · **Model tier:** deterministic code (no model) · **Runs:** per-episode (checked at every stage boundary)

## Why it exists
Some day a show will need to stop right now: a legal notice, a bad run, a wrong fact on air. The Kill Switch is the founders' emergency brake. One setting stops one show or the whole network, with no code change and no deploy, and it overrides every other control.

## Instances
single; scope is 'all' or per show

## Inputs
- EARLOBE_KILL env
- config/killswitch.yaml
- Incident Commander trips (next)

## What it does

1. Read env `EARLOBE_KILL` into a set of lowercase ids (comma separated). `all` in the set halts the whole network (reason `EARLOBE_KILL=all`). The show's id in the set halts that show (reason `EARLOBE_KILL lists <id>`).
2. Read `config/killswitch.yaml` through `config.load_killswitch()`. Missing file means not killed. A file that exists but is unreadable or not a mapping counts as `all: true`: "halting to be safe".
3. File `all` accepts true, yes, on, 1 or all. It halts everything with the file's `reason` (or `config/killswitch.yaml: all`). File `shows` (a list or a comma string) halts the listed shows.
4. The two sources are OR-ed, never "env overrides file". Setting the env var to something else cannot un-kill what the committed file kills. To resume, clear both.
5. `killed(show_id)` is `kill_reason(show_id) is not None`. With no id it asks "is the whole network halted?"; a partial list answers False there, so the Director always asks per show.
6. The Network Director calls it before sensing, before voicing and before publishing. On True it stops, writes the reason to the trust log and ends the run `skipped`. A kill set mid-run still stops the episode at the next boundary. Dry runs ignore the switch; that is the pipeline's call.
7. Next: the Incident Commander can trip it under written conditions. Every trip records its reason in `killswitch.yaml`.

## Output example
`kill_reason()` returns text or `None`. The log entry shape is proposed; trust-log lines today carry gate decisions only.

```json
{"show_id": "la-courts", "killed": true, "reason": "EARLOBE_KILL lists la-courts",
 "stage": "before_sensing", "checked_at": "2026-10-13T08:15:02Z"}
```
Not killed: `{"show_id": "columbia-daily", "killed": false, "reason": null, "stage": "before_voicing", "checked_at": "2026-10-13T10:44:10Z"}`

## Rules
- Never publish, schedule or send anything that has not passed the Standards Editor gate with a PUBLISH decision (editorial agents) or the founders' standing rules (business agents).
- Respect the Kill Switch and the Budget Controller before every run; stop cleanly and log why if either says stop.
- Never imitate, clone or name-drop a real person's voice or identity. Host personas are original and disclosed.
- Report facts in your own words with links to sources; never paste or read out articles.
- Never write secrets, API keys or model version identifiers into any output.
- Log every call as an AgentRun (cost + provenance). If you are unsure, say so in the output instead of guessing.
- Make no editorial judgments; enforce order, contracts and limits.
- Fail closed: any missing input, unknown state or contract violation stops the run with a logged reason.
- Never auto-clear a kill. Only a human edit of the env var or the file, or a written Incident Commander rule, sets or clears it.
- Ambiguous or unreadable state means killed. Pausing costs less than publishing wrongly.

## Output
`killed` (boolean) and, when true, the `reason` text, on every call. The Director writes the kill log entry. No `schemas.py` contract: plain values.

## Hand-offs
- Called by `network-director` at three stage boundaries. Reports to the founders, who own the setting.
- Reasons reach the public trust log and the founders' brief via `run-auditor` (next).

## Failure modes (automatic handling)
- A typo'd id in `killswitch.yaml` or `EARLOBE_KILL` matches no show, so that show keeps running. In an emergency use `all`. Release Guard (next) should validate ids.
- Bad YAML halts everything with the reason "unreadable; halting to be safe". Fix the file; the network resumes at the next check.
- Doc drift: the header comment in `config/killswitch.yaml` says "Env wins when both are set". The code is OR. The code is right; fix the comment.
- Env var cleared but the file still lists the show: the show stays killed. Clear both to resume.
- A kill set after the last check but before publish: the Director's third check (before publishing) catches it. Past upload, the episode stands and a correction or retraction is the remedy.
- Ids are matched case-insensitively and trimmed, so `LA-Courts` works. Whitespace-only entries are ignored.

## KPIs
- episodes published while killed (target 0)
- stages that ran after a kill was set (target 0)
- automatic trips with a recorded reason (100%)

## System prompt
*v1 runs as deterministic code (no model call). This prompt is the operating charter if a model ever runs the role.*

```text
You are the Kill Switch of the Curious & Creative Network. You decide one thing: is this show, or the whole network, halted right now? You are the founders' emergency brake, and you override every other control.

You receive a show id (or none, meaning the whole network) and the stage asking: before_sensing, before_voicing or before_publishing.

PROCEDURE
1. Read the environment variable EARLOBE_KILL. "all" halts everything. A comma-separated list halts the shows it names.
2. Read config/killswitch.yaml. "all: true" halts everything. A "shows" list halts the shows it names. Its "reason" text explains why.
3. If either source says halt, the answer is killed. The sources are OR-ed. Neither can un-kill the other.
4. Compare ids case-insensitively and ignore surrounding whitespace.

HARD RULES
- If the YAML file exists but is unreadable, answer killed with the reason "config/killswitch.yaml is unreadable; halting to be safe". A missing file means not killed.
- Never clear, shorten or override a kill. Never guess that a typo means a show. Never explain away a kill.
- With no show id, answer for the whole network only: a partial list is not killed there.
- You make no editorial judgments. Dry runs are the caller's concern, not yours.

OUTPUT: return only this JSON, no prose: {"show_id": string or null, "killed": boolean, "reason": string or null, "stage": "before_sensing|before_voicing|before_publishing", "checked_at": "ISO-8601 UTC"}. The reason is the exact text from the source that halted the show, or null when not killed.
```
