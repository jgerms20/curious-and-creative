---
id: agent-id                 # kebab-case, unique, matches catalog
name: Agent Name
desk: trust                  # command | sensors | editorial | trust | studio | distribution | growth | revenue | business-ops | services
status: built                # built | next | future
model_tier: opus             # opus | sonnet | haiku | none (deterministic code)
runs: per-episode            # always-on | cron "<expr>" | per-episode | event:<name> | weekly | on-demand
reports_to: standards-editor
inputs: [Script]             # contract names from earlobe/schemas.py, or plain descriptions
outputs: [VerifierReport]    # contract names from earlobe/schemas.py
tools: [web_search]          # web_search | web_fetch | rss | courtlistener | gdelt | elevenlabs | ffmpeg | computer_use | host_api | email | sql
code: earlobe/trust/verifier.py   # module that runs it, or "—" if not built yet
kpis: ["...", "..."]
---

# Agent Name

> One-line mission.

## Why it exists
What breaks or is lost without this agent. 2-4 sentences.

## Inputs
What it receives, from whom.

## What it does
Numbered steps — the actual procedure.

## Rules
Hard constraints. Things it must never do.

## Output
The JSON contract it returns (name + a short realistic example).

## Hand-offs
Who consumes its output; what triggers the next step.

## Failure modes (automatic handling)
What goes wrong and what the system does about it with no human in the loop.

## KPIs
How we know it's doing its job.

## System prompt
```text
The exact instructions the engine sends this agent.
```
