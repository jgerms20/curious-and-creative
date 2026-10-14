"""The trust loop: extract claims, run the checkers in isolation, apply the gate, rewrite.

  extract_claims -> verifier | bias | legal  (independent calls, run side by side)
                 -> fact checker             (may read the verifier's evidence URLs, nothing else)
                 -> gate.decide              (deterministic; this module never second-guesses it)

  PUBLISH  return
  REWRITE  rewrite_fn(script, instructions) -> revised script (revision + 1), then go again
  HOLD     return at once (breaking lane): the caller waits decision.recheck_after_minutes
           and calls again with holds_used + 1
  KILL     return

Fail closed: if any checker raises (refusal, bad output, no model), the exception
propagates and nothing is published. The loop owns revision counting and the lane, so a
rewrite cannot reset the gate's rewrite budget or switch to an easier lane, and it carries
the disclosure segment over if a rewrite dropped it.
"""
from __future__ import annotations

import dataclasses
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from earlobe.schemas import GateDecision, GateReason, Script, make_id
from earlobe.trust import gate
from earlobe.trust.bias import bias_check
from earlobe.trust.claims import extract_claims
from earlobe.trust.factcheck import fact_check
from earlobe.trust.legal import legal_screen
from earlobe.trust.verifier import compare_sources, verify

MAX_PASSES = 6      # hard stop on spend: the gate's rewrite budget ends the loop long before this


def run_checkers(script: Script, llm, owners: dict) -> dict:
    """One isolated call per checker. Returns {"verifier", "factcheck", "bias", "legal"} report objects."""
    with ThreadPoolExecutor(max_workers=3) as pool:
        verifier = pool.submit(verify, script, llm, owners)
        bias = pool.submit(bias_check, script, llm)
        legal = pool.submit(legal_screen, script, llm)
        verifier_report = verifier.result()
        factcheck_report = fact_check(script, verifier_report, llm)
        return {"verifier": verifier_report, "factcheck": factcheck_report,
                "bias": bias.result(), "legal": legal.result()}


def _advance(prev: Script, new: Script) -> Script:
    """Accept a rewrite: the loop sets revision and lane, and keeps the AI disclosure at the end."""
    lines = list(new.lines)
    if not any(l.segment == "disclosure" for l in lines):
        lines += [dataclasses.replace(l, claim_ids=[]) for l in prev.lines if l.segment == "disclosure"]
    revision = prev.revision + 1
    script_id = new.id if new.id != prev.id else make_id("scr", prev.id, "rev", revision)
    return dataclasses.replace(new, id=script_id, lines=lines, revision=revision,
                               lane_policy=prev.lane_policy)


def _killed(script: Script, why: str) -> GateDecision:
    return GateDecision(script_id=script.id, decision="KILL", lane_policy=script.lane_policy,
                        revision=script.revision, reasons=[GateReason(rule_id="LOOP", detail=why)])


def _summary(script: Script, decision: GateDecision) -> dict:
    return {"revision": script.revision, "script_id": script.id, "decision": decision.decision,
            "rules": [r.rule_id for r in decision.reasons], "scores": decision.scores}


def run_trust_loop(script: Script, rewrite_fn: Callable[[Script, list], Script], llm, owners: dict, *,
                   policy=None, holds_used: int = 0) -> tuple[Script, GateDecision, dict]:
    """Check `script` until the gate says PUBLISH, HOLD or KILL.

    Returns (final script, final GateDecision, reports). `reports` is JSON-safe:
      verifier, factcheck, bias, legal   the final pass's reports (to_dict)
      source_comparison                  writer sources vs what the blind verifier found
      passes                             every pass: {revision, script_id, decision, reports...}
      history                            one summary row per pass (revision, decision, rule ids, scores)
      rewrites, holds_used
    `policy` (a gate.LanePolicy or lane name) and `holds_used` are passed straight to the gate.
    """
    passes: list[dict] = []
    decision = None
    for _ in range(MAX_PASSES):
        script = extract_claims(script, llm)
        reports = run_checkers(script, llm, owners)
        decision = gate.decide(script, reports["verifier"], reports["factcheck"], reports["bias"],
                               reports["legal"], policy=policy, holds_used=holds_used)
        passes.append({**_summary(script, decision),
                       "claims": len(script.claims),
                       "source_comparison": compare_sources(script, reports["verifier"], owners),
                       **{k: v.to_dict() for k, v in reports.items()},
                       "gate": decision.to_dict()})
        if decision.decision != "REWRITE":
            break
        script = _advance(script, rewrite_fn(script, list(decision.rewrite_instructions)))
    else:
        decision = _killed(script, f"no PUBLISH, HOLD or KILL after {MAX_PASSES} passes")

    last = passes[-1]
    out = {k: last[k] for k in ("verifier", "factcheck", "bias", "legal", "source_comparison")}
    out.update(passes=passes, history=[{k: p[k] for k in ("revision", "script_id", "decision", "rules", "scores")}
                                       for p in passes],
               rewrites=len(passes) - 1, holds_used=holds_used)
    return script, decision, out
