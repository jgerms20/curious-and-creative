"""Standards Editor: the deterministic publish gate.

The three checkers (Source Verifier, Fact Checker, Bias Checker) and the Legal
Screener are LLM agents. This module is NOT. It reads their JSON reports and
applies fixed rules, so the publish decision is reproducible, auditable and
testable. Same inputs -> same decision, every time.

Decisions
  PUBLISH  nothing blocking
  REWRITE  blocking issues the Producer can fix; instructions attached (max N loops)
  HOLD     breaking lane only: the story is real-looking but not yet confirmed
           enough; re-check after a delay instead of publishing early
  KILL     still blocked after the rewrite budget, or a hard-stop rule fired
"""
from __future__ import annotations

from dataclasses import dataclass, field

from earlobe.schemas import (BiasReport, FactCheckReport, GateDecision, GateReason,
                             LegalReport, Script, VerifierReport)

NEEDS_CORROBORATION = {"fact", "number", "quote", "attribution", "allegation", "legal_status"}
SENSITIVE_TYPES = {"allegation", "legal_status"}
SENSITIVE_FLAGS = {"crime", "legal_proceeding", "named_private_person", "minor", "victim", "death"}
HARD_STOP_RISKS = {"naming_minor", "naming_victim"}
_SEV = {"low": 1, "medium": 2, "high": 3}


@dataclass
class LanePolicy:
    name: str
    min_independent: int = 2           # distinct owner groups that support the claim
    official_satisfies: bool = True    # one tier-1 primary source is enough on its own
    allow_attributed_single: bool = True   # non-sensitive claim, 1 source, attributed on air
    sensitive_needs_official: bool = False
    min_balance: int = 70
    legal_block_severity: str = "high"
    max_rewrites: int = 2
    max_holds: int = 0
    hold_minutes: int = 15
    extra: dict = field(default_factory=dict)


POLICIES = {
    "standard": LanePolicy("standard"),
    "strict": LanePolicy("strict", min_independent=2, allow_attributed_single=False,
                         sensitive_needs_official=True, min_balance=75,
                         legal_block_severity="medium"),
    "breaking": LanePolicy("breaking", min_independent=3, official_satisfies=False,
                           allow_attributed_single=False, sensitive_needs_official=True,
                           min_balance=70, legal_block_severity="medium", max_rewrites=1,
                           max_holds=6, hold_minutes=15),
    "archive": LanePolicy("archive", min_independent=2, official_satisfies=True,
                          allow_attributed_single=True, min_balance=65),
}


def _corroborated(f, policy: LanePolicy, official_ok: bool) -> bool:
    if f.status == "corroborated" and f.independent_count >= policy.min_independent:
        return True
    if official_ok and f.has_official and f.status in ("corroborated", "single_source"):
        return True
    return False


def decide(script: Script, verifier: VerifierReport, factcheck: FactCheckReport,
           bias: BiasReport, legal: LegalReport | None = None, *,
           policy: LanePolicy | str | None = None, holds_used: int = 0) -> GateDecision:
    if policy is None or isinstance(policy, str):
        policy = POLICIES[policy or script.lane_policy or "standard"]
    legal = legal or LegalReport(script_id=script.id)

    vf = {f.claim_id: f for f in verifier.findings}
    fc = {f.claim_id: f for f in factcheck.findings}
    reasons: list[GateReason] = []
    fixes: list[str] = []
    threshold_only = True   # every blocking reason is "not enough independent sources yet"
    hard_stop = False

    def block(rule, detail, target="", fix=None, threshold=False):
        nonlocal threshold_only
        reasons.append(GateReason(rule_id=rule, detail=detail, target_id=target))
        if fix:
            fixes.append(fix)
        if not threshold:
            threshold_only = False

    need = [c for c in script.claims if c.type in NEEDS_CORROBORATION]
    good = 0
    for c in script.claims:
        sensitive = c.type in SENSITIVE_TYPES or bool(SENSITIVE_FLAGS & set(c.risk_flags))
        f = vf.get(c.id)
        if c.type in NEEDS_CORROBORATION:
            if f is None:
                block("V0", "verifier did not cover this claim", c.id,
                      f"Drop or re-source claim {c.id}: \"{c.text}\" (no verification on file).")
            elif f.status == "contradicted":
                block("V1", f"evidence contradicts the claim. {f.note}".strip(), c.id,
                      f"Correct or remove {c.id}: \"{c.text}\". Evidence: {f.note or 'see verifier report'}")
            elif f.status == "unsupported":
                block("V2", "no supporting source found", c.id,
                      f"Remove {c.id}: \"{c.text}\" (unsupported).")
            else:
                ok = _corroborated(f, policy, policy.official_satisfies)
                if not ok and policy.allow_attributed_single and not sensitive \
                        and c.attributed and f.status == "single_source":
                    ok = True   # single source, said on air who says it, low risk
                if not ok:
                    block("V3", f"{f.independent_count} independent source(s); "
                                f"policy '{policy.name}' needs {policy.min_independent}", c.id,
                          f"Find more independent sourcing for {c.id} or cut it: \"{c.text}\".",
                          threshold=True)
                elif sensitive and policy.sensitive_needs_official and not f.has_official:
                    block("V4", "sensitive claim (allegation/legal status/crime) lacks an "
                                "official record source", c.id,
                          f"Back {c.id} with a court record or official statement, or cut it.",
                          threshold=True)
                else:
                    good += 1
        elif c.type == "prediction" and not c.attributed:
            block("V5", "prediction stated without attribution", c.id,
                  f"Attribute the prediction in {c.id} to a named source or cut it.")

        r = fc.get(c.id)
        if r is None:
            if c.type in NEEDS_CORROBORATION:
                block("F0", "fact checker did not cover this claim", c.id,
                      f"Re-run fact check for {c.id}.")
        elif r.rating in ("inaccurate", "misleading"):
            block("F1", f"rated {r.rating}: {r.issue}", c.id,
                  r.suggested_fix or f"Fix wording of {c.id}: {r.issue}")
        elif r.rating == "unverifiable":
            block("F2", "unverifiable as worded", c.id, f"Remove or soften {c.id}.")

    if bias.balance_score < policy.min_balance:
        block("B1", f"balance score {bias.balance_score} < {policy.min_balance}",
              fix="Rebalance: " + "; ".join(bias.missing_perspectives or ["neutralize framing"]))
    for i in bias.issues:
        if i.severity == "high":
            block("B2", f"high-severity {i.type}: {i.explanation}", i.line_id,
                  i.suggestion or f"Rewrite line {i.line_id} neutrally.")

    for i in legal.issues:
        if i.risk in HARD_STOP_RISKS:
            hard_stop = hard_stop or script.revision >= policy.max_rewrites
            block("L2", f"{i.risk}: {i.explanation}", i.target_id,
                  i.fix or f"Remove identifying details in {i.target_id}.")
        elif _SEV.get(i.severity, 0) >= _SEV[policy.legal_block_severity]:
            block("L1", f"{i.risk} ({i.severity}): {i.explanation}", i.target_id,
                  i.fix or f"Fix legal issue in {i.target_id}.")

    if not any(l.segment == "disclosure" for l in script.lines):
        block("S1", "missing AI disclosure segment",
              fix="Append the standard AI disclosure outro (Disclosure agent).")

    rated = [r for r in factcheck.findings if r.rating != "unverifiable"]
    scores = {
        "corroboration_rate": round(good / len(need), 3) if need else 1.0,
        "accuracy_rate": round(sum(r.rating in ("accurate", "minor_issue") for r in rated)
                               / len(rated), 3) if rated else 1.0,
        "balance_score": bias.balance_score,
        "claims": len(script.claims),
    }

    blocking = [r for r in reasons if r.blocking]
    if not blocking:
        decision, recheck = "PUBLISH", None
    elif hard_stop:
        decision, recheck = "KILL", None
    elif policy.name == "breaking" and threshold_only and holds_used < policy.max_holds:
        decision, recheck = "HOLD", policy.hold_minutes
    elif script.revision < policy.max_rewrites:
        decision, recheck = "REWRITE", None
    else:
        decision, recheck = "KILL", None

    return GateDecision(script_id=script.id, decision=decision, lane_policy=policy.name,
                        revision=script.revision, reasons=reasons,
                        rewrite_instructions=fixes if decision == "REWRITE" else [],
                        scores=scores, recheck_after_minutes=recheck)
