#!/usr/bin/env python3
"""Render agents/<desk>/<id>.md (one instruction file per agent) from config/agents.json.

The roster in config/agents.json is the machine-readable twin of
docs/blueprint/agent-catalog.md. Files marked `enriched: true` in their
frontmatter were hand-deepened and are never overwritten.

    python scripts/build_agent_files.py
"""
from __future__ import annotations

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AGENTS_DIR = os.path.join(ROOT, "agents")

DESKS = {
    "command": ("Command", "Runs the network: orchestration, schedules, budgets, safety switches."),
    "sensors": ("Sensors", "Always-on watchers: markets, courts, press releases, archives, breaking signals."),
    "editorial": ("Editorial", "Turns signals into stories and stories into scripts, titles and show notes."),
    "trust": ("Trust Stack", "Independent checks every claim must pass before anything publishes."),
    "studio": ("Studio", "Voices, sound, disclosure and listen-back quality control."),
    "distribution": ("Distribution", "Feeds, platforms, video, clips, transcripts, new-show launches."),
    "growth": ("Growth & Marketing", "Audience, social, newsletter, cross-promotion, analytics."),
    "revenue": ("Revenue", "Ads, sponsors, sales materials, B2B and Trust Stack customers."),
    "business-ops": ("Business Ops", "Intel, finance, compliance, vendors, knowledge, partner relations."),
    "services": ("C&C Studio Services", "The in-person offer: podcast setup, distribution and coaching for clients."),
}

COMMON_RULES = [
    "Never publish, schedule or send anything that has not passed the Standards Editor gate with a PUBLISH decision "
    "(editorial agents) or the founders' standing rules (business agents).",
    "Respect the Kill Switch and the Budget Controller before every run; stop cleanly and log why if either says stop.",
    "Never imitate, clone or name-drop a real person's voice or identity. Host personas are original and disclosed.",
    "Report facts in your own words with links to sources; never paste or read out articles.",
    "Never write secrets, API keys or model version identifiers into any output.",
    "Log every call as an AgentRun (cost + provenance). If you are unsure, say so in the output instead of guessing.",
]

DESK_RULES = {
    "command": ["Make no editorial judgments; enforce order, contracts and limits.",
                "Fail closed: any missing input, unknown state or contract violation stops the run with a logged reason."],
    "sensors": ["Collect, don't conclude: record what a source says, who said it, when, and the link.",
                "Tag every signal with market, beat, source tier and owner group so independence can be counted.",
                "Treat social posts and unknown sites as tier 4 leads, never as confirmation."],
    "editorial": ["Every factual sentence in a script carries claim_ids; every claim maps to sources.",
                  "Use precise attribution (said, according to, alleged, charged with); no speculation stated as fact.",
                  "Write for the ear: short sentences, natural numbers and dates, signposting, a clear 'why it matters'."],
    "trust": ["Work in isolation: do not read other checkers' reasoning unless your contract says so.",
              "Two independent sources (distinct owner groups) or one official record; wire copy counts once.",
              "When in doubt, flag it. A false alarm costs a rewrite; a missed error costs trust."],
    "studio": ["Use only the persona voices in config/voices.yaml; never clone a real person.",
               "Every episode ends with the AI disclosure segment; loudness target -16 LUFS integrated, -1.5 dBTP."],
    "distribution": ["Ship only rendered episodes with a PUBLISH gate record attached.",
                     "Every listing carries the AI disclosure in its description and metadata."],
    "growth": ["Promote only published, gated content; never exaggerate or sensationalize beyond the episode.",
               "Follow platform rules and label AI-generated media where platforms require it."],
    "revenue": ["Keep a hard wall between advertisers and editorial: sponsors never influence coverage.",
                "Brand-safety rules: no ads next to crime/tragedy content unless the advertiser opted in.",
                "Founders approve every contract, price exception and invoice above the standing limit."],
    "business-ops": ["Separate fact from inference in every memo; cite sources with dates.",
                     "Escalate legal, financial or platform-policy risks to the founders the same day."],
    "services": ["Clients own their shows and data; never reuse client material for the network.",
                 "Quote, scope and deliver in writing; founders approve every proposal before it is sent."],
}

TEMPLATE = """---
id: {id}
name: {name}
desk: {desk}
status: {status}
model_tier: {model_tier}
runs: {runs}
reports_to: {reports_to}
inputs: {inputs}
outputs: {outputs}
tools: {tools}
code: {code}
kpis: {kpis}
enriched: false
---

# {name}

> {mission}

**Desk:** {desk_name} · **Status:** `{status}` · **Model tier:** {tier_label} · **Runs:** {runs_plain}

## Why it exists
{description}

## Instances
{instances}

## Inputs
{inputs_md}

## What it does
{procedure}

## Rules
{rules_md}

## Output
{outputs_md}

Return JSON only, matching the contract{contract_note}. Include an `uncertain` note for anything you could not confirm.

## Hand-offs
- Reports to **{reports_plain}**.
- Downstream consumers pick up its outputs as described in [`docs/blueprint/how-it-works.md`](../../docs/blueprint/how-it-works.md).

## Failure modes (automatic handling)
- Missing or malformed input → stop, log an AgentRun with `ok=false`, and let the Network Director retry once on the next cycle.
- Output fails its JSON contract → one automatic retry with the validation errors attached; then fail closed.
- Budget or kill switch says stop → exit before doing work and record the reason.
{extra_failure}
## KPIs
{kpis_md}

## System prompt
```text
You are the {name} of the Curious & Creative Network — an automated, verified AI audio network
that publishes local news briefs, a Breaking Desk show, courts and true-crime trackers, and archive
series, with every claim checked before release.

Your mission: {mission}

What you are responsible for: {description_short}

Hard rules:
{rules_prompt}

Return only the output described for you ({outputs_plain}). Be specific, cite sources by link,
and say plainly when something is uncertain instead of guessing.
```
"""


def bullets(items):
    return "\n".join(f"- {x}" for x in items) if items else "- —"


def yaml_list(items):
    return "[" + ", ".join(json.dumps(x, ensure_ascii=False) for x in items) + "]"


def procedure(a):
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", a["description"]) if s.strip()]
    steps = [f"{i}. {s}" for i, s in enumerate(sents[:6], 1)]
    if a.get("code") and a["code"] not in ("—", "-", ""):
        steps.append(f"{len(steps) + 1}. Implementation: `{a['code']}`.")
    return "\n".join(steps)


def render(a):
    desk_name = DESKS.get(a["desk"], (a["desk"], ""))[0]
    rules = COMMON_RULES + DESK_RULES.get(a["desk"], [])
    tier = a["model_tier"]
    tier_label = "deterministic code (no model)" if tier == "none" else f"{tier.capitalize()} tier"
    contract_names = [o for o in a["outputs"] if re.match(r"^[A-Z][A-Za-z]+$", o.split(" ")[0])]
    contract_note = (f" (`{contract_names[0].split(' ')[0]}` in `earlobe/schemas.py`)"
                     if contract_names else " (proposed — define in earlobe/schemas.py when built)")
    desc_short = " ".join(re.split(r"(?<=[.!?])\s+", a["description"])[:2])
    extra = ""
    if a["desk"] == "trust":
        extra = "- Checker unavailable → the gate treats every uncovered claim as blocking (rules V0/F0): nothing publishes unchecked.\n"
    if a["desk"] == "sensors":
        extra = "- A source goes dark or changes format → mark it unhealthy, keep the rest running, flag it in the daily run summary.\n"
    return TEMPLATE.format(
        id=a["id"], name=a["name"], desk=a["desk"], status=a["status"], model_tier=tier,
        runs=json.dumps(a["runs"], ensure_ascii=False), reports_to=json.dumps(a["reports_to"], ensure_ascii=False),
        inputs=yaml_list(a["inputs"]), outputs=yaml_list(a["outputs"]), tools=yaml_list(a["tools"]),
        code=json.dumps(a.get("code") or "—", ensure_ascii=False), kpis=yaml_list(a["kpis"]),
        runs_plain=a["runs"], reports_plain=a["reports_to"],
        mission=a["mission"], desk_name=desk_name, tier_label=tier_label,
        description=a["description"], instances=a.get("instances") or "Single instance.",
        inputs_md=bullets(a["inputs"]), procedure=procedure(a), rules_md=bullets(rules),
        outputs_md=bullets(a["outputs"]), contract_note=contract_note, extra_failure=extra,
        kpis_md=bullets(a["kpis"]), description_short=desc_short,
        rules_prompt="\n".join(f"- {r}" for r in rules), outputs_plain="; ".join(a["outputs"]),
    )


def main():
    roster = json.load(open(os.path.join(ROOT, "config", "agents.json")))["agents"]
    written = skipped = 0
    for a in roster:
        d = os.path.join(AGENTS_DIR, a["desk"])
        os.makedirs(d, exist_ok=True)
        path = os.path.join(d, f"{a['id']}.md")
        if os.path.exists(path) and "enriched: true" in open(path).read(2000):
            skipped += 1
            continue
        with open(path, "w") as f:
            f.write(render(a))
        written += 1

    lines = ["# Agents — the Curious & Creative Network workforce", "",
             f"{len(roster)} agents across {len(DESKS)} desks. Full detail: "
             "[`docs/blueprint/agent-catalog.md`](../docs/blueprint/agent-catalog.md) · "
             "how they work together: [`docs/blueprint/how-it-works.md`](../docs/blueprint/how-it-works.md) · "
             "org chart: [`docs/blueprint/org-chart.md`](../docs/blueprint/org-chart.md).", "",
             "Status: `built` = engine code exists · `next` = next build wave · `future` = designed, not scheduled. "
             "Tier: which Claude model tier runs it (`none` = deterministic code).", ""]
    counts = {}
    for a in roster:
        counts.setdefault(a["status"], 0)
        counts[a["status"]] += 1
    lines.append("**Totals:** " + " · ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    lines.append("")
    for desk, (name, blurb) in DESKS.items():
        mine = [a for a in roster if a["desk"] == desk]
        if not mine:
            continue
        lines += [f"## {name} ({len(mine)})", "", blurb, "", "| Agent | Status | Tier | Runs | Mission |", "|---|---|---|---|---|"]
        order = {"built": 0, "next": 1, "future": 2}
        for a in sorted(mine, key=lambda x: (order.get(x["status"], 3), x["name"])):
            mission = a["mission"].replace("|", "/")
            runs = a["runs"].replace("|", "/")
            lines.append(f"| [{a['name']}]({desk}/{a['id']}.md) | {a['status']} | {a['model_tier']} | {runs} | {mission} |")
        lines.append("")
    with open(os.path.join(AGENTS_DIR, "README.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {written} agent files, kept {skipped} enriched, index at agents/README.md")


if __name__ == "__main__":
    main()
