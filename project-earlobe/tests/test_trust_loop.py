"""Producer and trust stack, driven by the dry-run LLM and hand-built reports. No keys, no network.

Sections
  helpers          a dry-run LLM whose checkers can be replaced by hand-built reports, plus script builders
  the loop         PUBLISH, REWRITE then PUBLISH, KILL after max rewrites, HOLD for breaking, fail-closed
  isolation        the verifier is blind; each checker sees only what it is allowed to see
  verifier         the code recount (owner groups, syndication, tier 4) and the late writer comparison
  claims           the independent claim pass merges conservatively
  producer         research pack, writer normalisation, disclosure, copywriter
  hygiene          no model ids in the code, key rules still present in the prompts
"""
import dataclasses
import json
import pathlib
import re

import pytest

from earlobe import config, fixtures
from earlobe.desk.cluster import cluster
from earlobe.llm import LLM
from earlobe.producer import copywriter, disclosure, research_pack, writer
from earlobe.schemas import (
    Claim,
    Script,
    ScriptLine,
    Source,
    Story,
    VerifierReport,
    make_id,
    validate,
)
from earlobe.trust import bias, factcheck, gate, legal, verifier
from earlobe.trust.claims import extract_claims
from earlobe.trust.loop import run_trust_loop
from earlobe.trust.verifier import verify

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOWS = config.load_shows()
VOICES = config.load_voices()
OWNERS = {"wires": ["Associated Press", "Reuters"],
          "groups": {"McClatchy": ["The State"], "Gray Media": ["WIS", "wistv.com"], "TEGNA": ["WLTX"],
                     "Nexstar": ["KTLA", "The Hill"]}}
DAY = "2026-10-12"


# ================================================================== helpers
class ScriptedLLM(LLM):
    """Dry-run LLM. `hooks[agent_id](ctx)` may return a hand-built report (dict); None falls back to
    the fixture. Every prompt is recorded in `calls` so tests can see what each agent was shown."""

    def __init__(self, **hooks):
        super().__init__(dry_run=True)
        self.hooks, self.calls = hooks, []

    def _hook(self, agent_id, system, user, kind, ctx):
        self.calls.append({"agent": agent_id, "system": system, "user": user, "kind": kind, "ctx": ctx})
        hook = self.hooks.get(agent_id)
        return hook(ctx) if hook else None

    def structured(self, agent_id, tier, system, user, kind, effort="medium", *, ctx=None):
        out = self._hook(agent_id, system, user, kind, ctx)
        return out if out is not None else super().structured(agent_id, tier, system, user, kind,
                                                               effort, ctx=ctx)

    def research(self, agent_id, tier, system, user, kind, max_searches=10, *, effort="medium", ctx=None):
        out = self._hook(agent_id, system, user, kind, ctx)
        return out if out is not None else super().research(agent_id, tier, system, user, kind,
                                                             max_searches, effort=effort, ctx=ctx)

    def prompt(self, agent_id) -> str:
        """Everything the agent was shown across all its calls (system + user)."""
        return "\n".join(c["system"] + "\n" + c["user"] for c in self.calls if c["agent"] == agent_id)

    def count(self, agent_id) -> int:
        return sum(c["agent"] == agent_id for c in self.calls)


def build_script(specs, show_id="columbia-daily", lane="standard", revision=0, disclosure_on=True) -> Script:
    """Hand-built script: intro, one body line per claim spec, kicker, outro, and the disclosure.

    spec = (claim_id, text, type, attributed, risk_flags)
    """
    cfg = {**SHOWS[show_id], "id": show_id}
    host = cfg["hosts"][0]
    lines = [ScriptLine("ln_intro", host, "Good morning, here is the news.", [], "intro")]
    cl = []
    for cid, text, ctype, attributed, flags in specs:
        lines.append(ScriptLine(f"ln_{cid}", host, text, [cid], "body"))
        cl.append(Claim(id=cid, text=text, type=ctype, line_ids=[f"ln_{cid}"], risk_flags=list(flags),
                        attributed=attributed))
    lines += [ScriptLine("ln_kick", host, "That is the news for now.", [], "kicker"),
              ScriptLine("ln_out", host, "Thanks for listening.", [], "outro")]
    script = Script(id=f"scr_test_{lane}", show_id=show_id, episode_date=DAY, title="Test episode",
                    lines=lines, claims=cl, lane_policy=lane, revision=revision)
    return disclosure.ensure_disclosure(script, cfg, VOICES) if disclosure_on else script


COUNCIL = ("clm_a", "The Columbia City Council approved a budget amendment for Riverbend Park on Tuesday "
           "in a 5-2 vote.", "number", False, [])
BRIDGE = ("clm_b", "The State reported that the Elm Street Bridge is closed after inspectors found a crack "
          "in a support beam.", "attribution", True, [])
RESIGN = ("clm_bad", "The mayor will resign next month.", "fact", False, [])
STORM = ("clm_h", "The National Hurricane Center said Hurricane Sample made landfall near Cape Marlow as a "
         "Category 3 storm.", "attribution", True, ["breaking"])

_NEWS = [("The State", 2), ("WIS", 2), ("WLTX", 2), ("KTLA", 2)]


def ev(n, official=False):
    """n supporting sources from n different owner groups (plus a tier-1 record if official)."""
    rows = [{"url": f"https://example.invalid/news/{i}", "outlet": o, "tier": t, "owner_group": "",
             "supports": True, "note": ""} for i, (o, t) in enumerate(_NEWS[:n])]
    if official:
        rows.append({"url": "https://example.invalid/record", "outlet": "County Clerk", "tier": 1,
                     "owner_group": "County Clerk", "supports": True, "note": ""})
    return rows


def verifier_with(patches):
    """Verifier hook: the fixture report with per-claim-id patches applied."""
    def hook(ctx):
        report = fixtures.fake("VerifierReport", **ctx)
        for f in report["findings"]:
            f.update(patches.get(f["claim_id"], {}))
        return report
    return hook


def unsupported():
    return {"status": "unsupported", "independent_count": 0, "has_official": False, "evidence": []}


def drop_claim(claim_id):
    """rewrite_fn that deletes one claim and its line, recording every call."""
    def rewrite(script, instructions):
        rewrite.calls.append((script, list(instructions)))
        gone = {l for c in script.claims if c.id == claim_id for l in c.line_ids}
        return dataclasses.replace(script, lines=[l for l in script.lines if l.id not in gone],
                                   claims=[c for c in script.claims if c.id != claim_id])
    rewrite.calls = []
    return rewrite


def unchanged():
    """rewrite_fn that changes nothing, recording every call."""
    def rewrite(script, instructions):
        rewrite.calls.append((script, list(instructions)))
        return dataclasses.replace(script)
    rewrite.calls = []
    return rewrite


def never_called(script, instructions):
    raise AssertionError("rewrite_fn must not be called")


def decisions(reports):
    return [h["decision"] for h in reports["history"]]


# ================================================================== the loop
def test_publish_path_all_dry_run():
    script = build_script([COUNCIL, BRIDGE])
    llm = LLM(dry_run=True)
    final, decision, reports = run_trust_loop(script, never_called, llm, OWNERS)
    assert decision.decision == "PUBLISH" and decision.reasons == []
    assert final.revision == 0 and reports["rewrites"] == 0 and decisions(reports) == ["PUBLISH"]
    assert decision.scores["corroboration_rate"] == 1.0
    assert {r.agent_id for r in llm.runs} == {"claim-extractor", "verifier", "fact-checker",
                                              "bias-checker", "legal-screener"}
    assert {k for k in reports if k != "passes"} >= {"verifier", "factcheck", "bias", "legal", "history"}
    json.dumps(reports)                                   # JSON-safe for the store and the trust log


def test_publish_gate_is_the_only_judge():
    """The loop returns the gate's own decision object for the final pass."""
    script = build_script([COUNCIL])
    final, decision, reports = run_trust_loop(script, never_called, LLM(dry_run=True), OWNERS)
    assert decision.to_dict() == reports["passes"][-1]["gate"]


def test_rewrite_then_publish():
    script = build_script([COUNCIL, RESIGN, BRIDGE])
    llm = ScriptedLLM(verifier=verifier_with({"clm_bad": unsupported()}))
    rewrite = drop_claim("clm_bad")
    final, decision, reports = run_trust_loop(script, rewrite, llm, OWNERS)

    assert decisions(reports) == ["REWRITE", "PUBLISH"]
    assert decision.decision == "PUBLISH" and final.revision == 1 and reports["rewrites"] == 1
    assert len(rewrite.calls) == 1
    seen, instructions = rewrite.calls[0]
    assert seen.revision == 0 and any("clm_bad" in i and "mayor will resign" in i for i in instructions)
    assert {c.id for c in final.claims} == {"clm_a", "clm_b"}
    assert reports["passes"][0]["gate"]["reasons"][0]["rule_id"] == "V2"
    assert final.id != script.id                          # a revision is a new script
    assert any(l.segment == "disclosure" for l in final.lines)


def test_kill_after_max_rewrites():
    script = build_script([COUNCIL, RESIGN])
    llm = ScriptedLLM(verifier=verifier_with({"clm_bad": unsupported()}))
    rewrite = unchanged()
    final, decision, reports = run_trust_loop(script, rewrite, llm, OWNERS)

    max_rewrites = gate.POLICIES["standard"].max_rewrites
    assert decision.decision == "KILL" and final.revision == max_rewrites
    assert decisions(reports) == ["REWRITE"] * max_rewrites + ["KILL"]
    assert len(rewrite.calls) == max_rewrites == reports["rewrites"]
    assert decision.rewrite_instructions == []
    assert "V2" in {r.rule_id for r in decision.reasons}


def test_hold_for_breaking_then_publish_when_confirmed():
    script = build_script([STORM], show_id="breaking-desk", lane="breaking")
    weak = ScriptedLLM(verifier=verifier_with({"clm_h": {"status": "corroborated", "evidence": ev(2)}}))
    final, decision, reports = run_trust_loop(script, never_called, weak, OWNERS)
    assert decision.decision == "HOLD" and decision.recheck_after_minutes == 15
    assert decisions(reports) == ["HOLD"] and final is not None and final.revision == 0
    assert [r.rule_id for r in decision.reasons] == ["V3"]
    assert reports["verifier"]["findings"][0]["independent_count"] == 2   # recounted, not taken on trust

    # the caller waits, calls again with holds_used + 1, and a third independent source has appeared
    strong = ScriptedLLM(verifier=verifier_with({"clm_h": {"status": "corroborated", "evidence": ev(3)}}))
    _, decision, reports = run_trust_loop(script, never_called, strong, OWNERS, holds_used=1)
    assert decision.decision == "PUBLISH" and reports["holds_used"] == 1


def test_breaking_hold_budget_runs_out_then_rewrite_then_kill():
    script = build_script([STORM], show_id="breaking-desk", lane="breaking")
    weak = ScriptedLLM(verifier=verifier_with({"clm_h": {"status": "corroborated", "evidence": ev(2)}}))
    rewrite = unchanged()
    final, decision, reports = run_trust_loop(script, rewrite, weak, OWNERS,
                                              holds_used=gate.POLICIES["breaking"].max_holds)
    assert decisions(reports) == ["REWRITE", "KILL"] and len(rewrite.calls) == 1


def test_breaking_real_problem_rewrites_instead_of_holding():
    script = build_script([STORM], show_id="breaking-desk", lane="breaking")
    contradicted = {"status": "contradicted", "evidence": ev(3), "note": "the agency says Category 2"}
    final, decision, reports = run_trust_loop(script, unchanged(), ScriptedLLM(
        verifier=verifier_with({"clm_h": contradicted})), OWNERS)
    assert decisions(reports) == ["REWRITE", "KILL"]       # breaking allows one rewrite, never a hold here


def test_bias_and_legal_findings_reach_the_gate():
    low_bias = {"balance_score": 55, "issues": [], "missing_perspectives": ["the agency's response"]}
    minor = {"issues": [{"target_id": "ln_clm_a", "risk": "naming_minor", "severity": "low",
                         "explanation": "names a child", "fix": "Remove the child's name."}]}
    llm = ScriptedLLM(**{"bias-checker": lambda ctx: low_bias, "legal-screener": lambda ctx: minor})
    rewrite = unchanged()
    final, decision, reports = run_trust_loop(build_script([COUNCIL]), rewrite, llm, OWNERS)
    first = reports["passes"][0]["gate"]
    assert {r["rule_id"] for r in first["reasons"]} == {"B1", "L2"}
    assert any("agency's response" in i for i in first["rewrite_instructions"])
    assert any("Remove the child's name." in i for i in first["rewrite_instructions"])
    assert decision.decision == "KILL" and final.revision == gate.POLICIES["standard"].max_rewrites


def test_missing_disclosure_is_blocked_then_fixed_by_the_rewrite():
    script = build_script([COUNCIL], disclosure_on=False)
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    rewrite = lambda s, instructions: disclosure.ensure_disclosure(s, cfg, VOICES)
    final, decision, reports = run_trust_loop(script, rewrite, LLM(dry_run=True), OWNERS)
    assert decisions(reports) == ["REWRITE", "PUBLISH"]
    assert reports["passes"][0]["gate"]["reasons"][0]["rule_id"] == "S1"


def test_loop_owns_revision_lane_and_disclosure():
    script = build_script([COUNCIL, RESIGN], lane="strict")
    llm = ScriptedLLM(verifier=verifier_with({"clm_bad": unsupported()}))

    def sloppy(s, instructions):       # tries to reset the budget, switch lane and lose the disclosure
        keep = [l for l in s.lines if l.segment != "disclosure" and l.id != "ln_clm_bad"]
        return dataclasses.replace(s, revision=0, lane_policy="archive", lines=keep,
                                   claims=[c for c in s.claims if c.id != "clm_bad"])

    final, decision, reports = run_trust_loop(script, sloppy, llm, OWNERS)
    assert decision.decision == "PUBLISH" and final.revision == 1 and final.lane_policy == "strict"
    assert any(l.segment == "disclosure" for l in final.lines)
    assert decision.lane_policy == "strict"


def test_checker_failure_fails_closed():
    def boom(ctx):
        raise RuntimeError("model unavailable")
    llm = ScriptedLLM(**{"bias-checker": boom})
    with pytest.raises(RuntimeError):
        run_trust_loop(build_script([COUNCIL]), never_called, llm, OWNERS)


@pytest.mark.parametrize("show_id", sorted(config.load_shows(enabled_only=True)))
def test_dry_run_pipeline_publishes_every_enabled_show(show_id):
    """pack -> writer -> disclosure -> trust loop -> gate -> copy, all fixtures, every lane."""
    cfg = {**SHOWS[show_id], "id": show_id}
    signals = fixtures.sample_signals(cfg["market"])
    stories = cluster(signals, OWNERS)[: cfg.get("max_stories") or 4]
    pack = research_pack.build_pack(stories, signals, OWNERS)
    llm = LLM(dry_run=True)
    script = writer.write_script(show_id, cfg, stories, pack, llm, episode_date=DAY)
    rewrite = writer.make_rewriter(show_id, cfg, stories, pack, llm, episode_date=DAY)
    final, decision, reports = run_trust_loop(script, rewrite, llm, OWNERS)
    assert decision.decision == "PUBLISH", [(r.rule_id, r.detail) for r in decision.reasons]
    assert final.lines[-1].segment == "disclosure"
    copy = copywriter.write_copy(final, cfg, llm)
    assert validate("Copy", copy) == []


# ================================================================== isolation
def test_verifier_is_blind_to_the_writers_sources_and_notes():
    s1 = Source(id="src_ghost1", url="https://writer-only.example/secret-one", outlet="The State")
    s2 = Source(id="src_ghost2", url="https://writer-only.example/secret-two", outlet="WIS")
    script = build_script([COUNCIL, BRIDGE])
    script = dataclasses.replace(script, sources=[s1, s2], notes_for_checkers="WRITER-NOTE-SECRET",
                                 claims=[dataclasses.replace(c, source_ids=["src_ghost1", "src_ghost2"])
                                         for c in script.claims])
    llm = ScriptedLLM()
    verify(script, llm, OWNERS)
    seen = llm.prompt("verifier")
    for secret in ("writer-only.example", "src_ghost", "WRITER-NOTE-SECRET", "Test episode"):
        assert secret not in seen
    assert COUNCIL[1] in seen and BRIDGE[1] in seen                     # claim text is all it gets...
    assert DAY in seen and "Columbia, SC" in seen                       # ...plus the date and the market
    assert "type:" not in llm.calls[0]["user"] and "attributed" not in llm.calls[0]["user"]


def test_each_checker_sees_only_what_it_may():
    note = "VERIFIER-NOTE-XYZ"
    patch = {"clm_a": {"status": "single_source", "evidence": ev(1), "note": note}}
    llm = ScriptedLLM(verifier=verifier_with(patch))
    script = build_script([COUNCIL, BRIDGE])
    script = dataclasses.replace(script, notes_for_checkers="Story desk risk flags: none")
    report = verify(script, llm, OWNERS)
    fact_report = factcheck.fact_check(script, report, llm)
    bias.bias_check(script, llm)
    legal.legal_screen(script, llm)

    fc = llm.prompt("fact-checker")
    assert "https://example.invalid/news/0" in fc                       # the pages the verifier relied on
    assert note not in fc and "single_source" not in fc and "corroborated" not in fc
    for agent in ("bias-checker", "legal-screener"):
        seen = llm.prompt(agent)
        assert "example.invalid" not in seen and note not in seen        # never the verifier's evidence
    assert "balance_score" not in llm.prompt("legal-screener")           # nor each other's reports
    assert "naming_minor" not in llm.prompt("bias-checker")
    assert {f.claim_id for f in fact_report.findings} == {"clm_a", "clm_b"}


def test_fact_checker_is_not_asked_when_there_is_nothing_to_check():
    script = dataclasses.replace(build_script([]), claims=[])
    llm = ScriptedLLM()
    report = factcheck.fact_check(script, VerifierReport(script_id=script.id), llm)
    assert report.findings == [] and llm.count("fact-checker") == 0


def test_checkers_do_not_filter_unknown_targets():
    """A hard-stop finding with a sloppy id must still reach the gate."""
    sloppy = {"issues": [{"target_id": "no-such-id", "risk": "naming_victim", "severity": "high",
                          "explanation": "x", "fix": ""}]}
    report = legal.legal_screen(build_script([COUNCIL]), ScriptedLLM(**{"legal-screener": lambda c: sloppy}))
    assert report.issues[0].risk == "naming_victim"


# ================================================================== verifier recount
def _verified(evidence, status="corroborated", claimed=3, official=False, extra=None):
    script = build_script([COUNCIL])
    patch = {"clm_a": {"status": status, "independent_count": claimed, "has_official": official,
                       "evidence": evidence, "traced_to_original": True, **(extra or {})}}
    report = verify(script, ScriptedLLM(verifier=verifier_with(patch)), OWNERS)
    return report.findings[0]


def _e(outlet, tier=2, url=None, supports=True, note=""):
    return {"url": url or f"https://example.invalid/{outlet.lower().replace(' ', '-')}", "outlet": outlet,
            "tier": tier, "owner_group": "", "supports": supports, "note": note}


def test_recount_collapses_sister_outlets():
    f = _verified([_e("WIS"), _e("wistv.com", url="https://wistv.com/story")])
    assert f.independent_count == 1 and f.status == "single_source" and "recount" in f.note


def test_recount_collapses_syndicated_wire_copy():
    f = _verified([_e("Associated Press"), _e("The State", note="Republished Associated Press story.")])
    assert f.independent_count == 1 and f.status == "single_source"


def test_recount_counts_distinct_owners_and_ignores_tier_4():
    f = _verified([_e("The State"), _e("WIS"), _e("Some Blog", tier=4)], claimed=3)
    assert f.independent_count == 2 and f.status == "corroborated"


def test_recount_never_upgrades_a_status():
    f = _verified([_e("The State"), _e("WIS"), _e("WLTX")], status="single_source", claimed=1)
    assert f.independent_count == 3 and f.status == "single_source"


def test_recount_official_flag_comes_from_tier_1_evidence_only():
    assert _verified([_e("The State"), _e("County Clerk", tier=1)], official=False).has_official is True
    assert _verified([_e("The State"), _e("WIS")], official=True).has_official is False


def test_recount_tier_1_source_that_conflicts_makes_it_contradicted():
    f = _verified([_e("The State"), _e("WIS"), _e("County Clerk", tier=1, supports=False)])
    assert f.status == "contradicted"


def test_recount_drops_invented_and_duplicate_urls():
    f = _verified([_e("The State", url="not a url"), _e("WIS", url="https://example.invalid/x?utm_source=a"),
                   _e("WIS", url="https://www.example.invalid/x/")])
    assert [e.url for e in f.evidence] == ["https://example.invalid/x?utm_source=a"]
    assert f.independent_count == 1


def test_recount_unreadable_tier_is_clamped_not_trusted():
    f = _verified([_e("The State", tier="banana"), _e("WIS", tier=0)])
    assert [e.tier for e in f.evidence] == [4, 1]


def test_claims_that_need_no_corroboration_are_not_sent_to_the_verifier():
    script = build_script([COUNCIL, ("clm_p", "The weather service expects rain on Sunday.", "prediction", True, []),
                           ("clm_c", "Here is what we know.", "context", False, [])])
    llm = ScriptedLLM()
    report = verify(script, llm, OWNERS)
    assert [f.claim_id for f in report.findings] == ["clm_a"]
    assert "weather service" not in llm.prompt("verifier")


def test_verifier_batches_long_scripts():
    specs = [(f"clm_{i}", f"The council approved item number {i}.", "fact", False, []) for i in range(verifier.BATCH + 3)]
    llm = ScriptedLLM()
    report = verify(build_script(specs), llm, OWNERS)
    assert llm.count("verifier") == 2 and len(report.findings) == verifier.BATCH + 3


def test_writer_comparison_runs_after_the_count_and_never_changes_it():
    s1 = Source(id="src_1", url="https://example.invalid/news/0", outlet="The State")
    s2 = Source(id="src_2", url="https://example.invalid/ghost", outlet="WIS")
    script = build_script([COUNCIL])
    script = dataclasses.replace(script, sources=[s1, s2], claims=[
        dataclasses.replace(script.claims[0], source_ids=["src_1", "src_2"])])
    patch = {"clm_a": {"status": "corroborated", "evidence": ev(1)}}
    report = verify(script, ScriptedLLM(verifier=verifier_with(patch)), OWNERS)
    f = report.findings[0]
    assert f.independent_count == 1                                        # the writer's 2 did not leak in
    assert "writer cited 2 independent source(s); blind verification found 1" in f.note
    row = verifier.compare_sources(script, report, OWNERS)[0]
    assert row["writer_independent"] == 2 and row["verifier_independent"] == 1
    assert row["shared_urls"] == ["example.invalid/news/0"] and row["writer_only_urls"] == ["example.invalid/ghost"]


# ================================================================== claim pass
def _extractor_output(script, claim_list, claim_ids_by_line):
    return {"title": script.title,
            "lines": [{"id": l.id, "speaker": l.speaker, "text": l.text, "segment": l.segment,
                       "claim_ids": claim_ids_by_line.get(l.id, [])} for l in script.lines],
            "claims": claim_list}


def test_claim_pass_adds_missed_claims_and_takes_the_stricter_type():
    script = build_script([("clm_a", "Police said a man was arrested on suspicion of burglary.", "context", True, [])])
    script.lines.insert(2, ScriptLine("ln_extra", "mara", "The man was charged on Monday, prosecutors said.", [], "body"))
    found = [{"id": "x1", "text": "Police said a man was arrested on suspicion of burglary.", "type": "legal_status",
              "line_ids": ["ln_clm_a"], "source_ids": ["src_made_up"], "risk_flags": ["crime", "bogus"],
              "attributed": False},
             {"id": "x2", "text": "The man was charged on Monday, prosecutors said.", "type": "legal_status",
              "line_ids": ["ln_extra"], "source_ids": [], "risk_flags": ["crime"], "attributed": True},
             {"id": "x3", "text": "A claim on a disclosure line", "type": "fact",
              "line_ids": [script.lines[-1].id], "source_ids": [], "risk_flags": [], "attributed": False}]
    llm = ScriptedLLM(**{"claim-extractor": lambda ctx: _extractor_output(script, found, {})})
    merged = extract_claims(script, llm)

    old = next(c for c in merged.claims if c.id == "clm_a")
    assert old.type == "legal_status" and old.risk_flags == ["crime"]
    assert old.attributed is False                    # both passes must agree for it to count
    new = next(c for c in merged.claims if c.id not in ("clm_a",))
    assert new.type == "legal_status" and new.source_ids == [] and new.line_ids == ["ln_extra"]
    assert len(merged.claims) == 2                    # the disclosure-line claim was discarded
    assert "ln_extra" in [l.id for l in merged.lines if new.id in l.claim_ids]
    assert script.claims[0].type == "context"          # the input script is not mutated


def test_claim_pass_input_never_includes_writer_claims_or_sources():
    script = dataclasses.replace(build_script([COUNCIL]), notes_for_checkers="WRITER-NOTE-SECRET")
    script.claims[0].source_ids = ["src_secret"]
    llm = ScriptedLLM()
    extract_claims(script, llm)
    seen = llm.prompt("claim-extractor")
    assert "src_secret" not in seen and "WRITER-NOTE-SECRET" not in seen
    assert "[clm_a]" not in seen and "CLAIMS" not in seen.split("LINES:")[0]    # the writer's claim list stays home
    assert COUNCIL[1] in seen


# ================================================================== producer: research pack
def _columbia():
    signals = fixtures.sample_signals("columbia-sc")
    return signals, cluster(signals, OWNERS)


def test_pack_counts_independent_sources_and_collapses_wire_copy():
    signals, stories = _columbia()
    pack = research_pack.build_pack(stories, signals, OWNERS)
    by_head = {s["headline"]: s for s in pack["stories"]}
    bridge = next(v for k, v in by_head.items() if "Elm Street Bridge" in k)
    assert len(bridge["source_ids"]) == 3 and bridge["independent_sources"] == 2    # AP + The State copy + WLTX
    council = next(v for k, v in by_head.items() if "Riverbend" in k)
    assert council["independent_sources"] == 4 and council["official_confirmation"] is True
    assert pack["warnings"] == []
    ids = {s["id"] for s in pack["sources"]}
    assert all(i in ids for st in pack["stories"] for i in st["source_ids"])


def test_pack_accepts_objects_and_dicts_and_is_deterministic():
    signals, stories = _columbia()
    a = research_pack.build_pack(stories, signals, OWNERS)
    b = research_pack.build_pack([s.to_dict() for s in stories], [s.to_dict() for s in signals], OWNERS)
    assert a == b


def test_pack_cautions_follow_risk_flags_and_thin_sourcing():
    src = Source(id=make_id("src", "https://blog.invalid/x"), url="https://blog.invalid/x", outlet="Some Blog",
                 tier=4, excerpt="x " * 600)
    story = Story(id="sty_1", market="columbia-sc", beat="public_safety", headline="Teen hurt in crash",
                  summary="", first_seen="", source_ids=[src.id], risk_flags=["minor", "victim"], breaking=True)
    pack = research_pack.build_pack([story], [src], OWNERS)
    cautions = " ".join(pack["stories"][0]["cautions"])
    assert "Do not report this story" in cautions and "under 18" in cautions and "victim" in cautions.lower()
    assert "Unfolding story" in cautions
    assert len(pack["sources"][0]["excerpt"]) <= research_pack.EXCERPT_MAX


def test_pack_warns_about_missing_and_unmatched_sources():
    signals, stories = _columbia()
    stray = Source(id="src_stray", url="https://stray.invalid/", outlet="Stray")
    pack = research_pack.build_pack(stories, signals[:-1] + [stray], OWNERS)
    assert any("were not supplied" in w for w in pack["warnings"])
    assert any("matched no story" in w for w in pack["warnings"])
    assert "src_stray" not in {s["id"] for s in pack["sources"]}


def test_pack_single_independent_source_caution():
    src = Source(id=make_id("src", "https://a.invalid/"), url="https://a.invalid/", outlet="WIS", tier=2)
    story = Story(id="sty_2", market="columbia-sc", beat="government", headline="h", summary="", first_seen="",
                  source_ids=[src.id])
    pack = research_pack.build_pack([story], [src], OWNERS)
    assert "Only one independent source" in pack["stories"][0]["cautions"][0]


# ================================================================== producer: writer
def _pack_and_stories(market="columbia-sc"):
    signals = fixtures.sample_signals(market)
    stories = cluster(signals, OWNERS)
    return stories, research_pack.build_pack(stories, signals, OWNERS)


def _raw_script(source_id):
    return {"title": "  My   title ", "lines": [
        {"id": "a", "speaker": "nobody", "text": "  Good   morning. ", "claim_ids": ["c1"], "segment": "intro"},
        {"id": "b", "speaker": "mara", "text": "This was written by AI.", "claim_ids": [], "segment": "disclosure"},
        {"id": "c", "speaker": "mara", "text": "The council voted 5-2.", "claim_ids": [], "segment": "body"},
        {"id": "d", "speaker": "theo", "text": "   ", "claim_ids": ["c2"], "segment": "body"},
        {"id": "e", "speaker": "theo", "text": "The vote was on Tuesday.", "claim_ids": ["c3", "zzz"], "segment": "weird"}],
        "claims": [
            {"id": "c1", "text": "The council voted 5-2.", "type": "number", "line_ids": ["c", "nope"],
             "source_ids": [source_id, "src_invented"], "risk_flags": ["crime", "bogus"], "attributed": False},
            {"id": "c2", "text": "The council voted 5-2.", "type": "fact", "line_ids": ["c"], "source_ids": [],
             "risk_flags": [], "attributed": False},
            {"id": "c3", "text": "The vote was on Tuesday.", "type": "bogus-type", "line_ids": [],
             "source_ids": [], "risk_flags": [], "attributed": True},
            {"id": "c4", "text": "", "type": "fact", "line_ids": [], "source_ids": [], "risk_flags": [],
             "attributed": False}]}


def test_writer_normalises_the_models_output():
    stories, pack = _pack_and_stories()
    sid = pack["sources"][0]["id"]
    llm = ScriptedLLM(producer=lambda ctx: _raw_script(sid))
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    script = writer.write_script("columbia-daily", cfg, stories, pack, llm, episode_date=DAY)

    spoken = [l for l in script.lines if l.segment != "disclosure"]
    assert [l.text for l in spoken] == ["Good morning.", "The council voted 5-2.", "The vote was on Tuesday."]
    assert [l.segment for l in spoken] == ["intro", "body", "body"]            # unknown segment -> body
    assert spoken[0].speaker in cfg["hosts"]                                    # unknown speaker replaced
    assert [l.text for l in script.lines if l.segment == "disclosure"] == disclosure._texts(cfg)   # canonical text
    assert script.lines[-1].segment == "disclosure" and script.title == "My title"
    assert len(script.claims) == 2                                               # duplicate merged, empty dropped
    vote = next(c for c in script.claims if c.text.startswith("The council"))
    assert vote.source_ids == [sid] and vote.risk_flags == ["crime"] and vote.type == "number"
    assert set(vote.line_ids) == {spoken[0].id, spoken[1].id}                    # both directions agree
    assert vote.id in spoken[0].claim_ids and vote.id in spoken[1].claim_ids
    other = next(c for c in script.claims if c is not vote)
    assert other.type == "fact" and other.attributed is True and other.line_ids == [spoken[2].id]
    assert [s.id for s in script.sources] == [sid]
    assert script.revision == 0 and script.lane_policy == "standard" and script.story_ids == [s.id for s in stories]
    assert script.id == make_id("scr", "columbia-daily", DAY, *sorted(s.id for s in stories), 0)


def test_writer_ids_are_stable_for_unchanged_text():
    stories, pack = _pack_and_stories()
    sid = pack["sources"][0]["id"]
    llm = ScriptedLLM(producer=lambda ctx: _raw_script(sid))
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    one = writer.write_script("columbia-daily", cfg, stories, pack, llm, episode_date=DAY)
    two = writer.write_script("columbia-daily", cfg, stories, pack, llm, revision=1, episode_date=DAY)
    assert [l.id for l in one.lines] == [l.id for l in two.lines]
    assert [c.id for c in one.claims] == [c.id for c in two.claims]
    assert one.id != two.id and two.revision == 1


def test_writer_refuses_an_empty_script():
    stories, pack = _pack_and_stories()
    llm = ScriptedLLM(producer=lambda ctx: {"title": "t", "lines": [], "claims": []})
    with pytest.raises(ValueError):
        writer.write_script("columbia-daily", SHOWS["columbia-daily"], stories, pack, llm, episode_date=DAY)


def test_writer_dry_run_gives_every_body_line_claims_and_pack_sources():
    stories, pack = _pack_and_stories()
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    script = writer.write_script("columbia-daily", cfg, stories, pack, LLM(dry_run=True), episode_date=DAY)
    assert all(l.claim_ids for l in script.lines if l.segment == "body")
    pack_ids = {s["id"] for s in pack["sources"]}
    assert script.sources and {s.id for s in script.sources} <= pack_ids
    assert all(set(c.source_ids) <= pack_ids for c in script.claims)
    assert all(set(l.claim_ids) <= {c.id for c in script.claims} for l in script.lines)


def test_writer_escalates_a_standard_show_to_strict_for_crime_stories():
    stories, pack = _pack_and_stories()
    stories[0].risk_flags = ["crime"]
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    script = writer.write_script("columbia-daily", cfg, stories, pack, LLM(dry_run=True), episode_date=DAY)
    assert script.lane_policy == "strict"
    assert "crime" in script.notes_for_checkers


def test_writer_prompt_carries_lane_rules_pack_and_revision_context():
    stories, pack = _pack_and_stories()
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    llm = ScriptedLLM()
    first = writer.write_script("columbia-daily", cfg, stories, pack, llm, episode_date=DAY)
    rewrite = writer.make_rewriter("columbia-daily", cfg, stories, pack, llm, episode_date=DAY)
    second = rewrite(first, ["Remove clm_zzz: \"made up\" (unsupported)."])

    assert second.revision == 1
    one, two = llm.calls[0]["user"], llm.calls[1]["user"]
    assert "Lane 'standard'" in one
    assert "2 independent sources" in one and "Monday" in one and "mara" in one and "theo" in one
    assert pack["stories"][0]["story_id"] in one
    assert "PREVIOUS SCRIPT" not in one and "FIX INSTRUCTIONS" not in one
    assert "PREVIOUS SCRIPT (revision 0)" in two and "Remove clm_zzz" in two
    assert first.claims[0].text in two


def test_lane_rules_are_generated_from_the_gate_policies():
    assert "3 independent sources" in writer.lane_rules("breaking") and "does NOT replace" in writer.lane_rules("breaking")
    assert "No single-source claims" in writer.lane_rules("strict") and "official record" in writer.lane_rules("strict")
    assert "75" in writer.lane_rules("strict") and "1 rewrite" in writer.lane_rules("breaking")
    assert writer.lane_rules("nonsense") == writer.lane_rules("standard")


def test_word_budget_leaves_room_for_the_disclosure():
    lo, hi = writer.word_budget(SHOWS["columbia-daily"])
    spare = len(disclosure.disclosure_text(SHOWS["columbia-daily"]).split())
    assert (lo, hi) == (6 * 155 - spare, 8 * 155 - spare)


# ================================================================== producer: disclosure
@pytest.mark.parametrize("show_id,variant", [
    ("columbia-daily", "daily"), ("la-daily", "daily"), ("la-courts", "daily"), ("breaking-desk", "breaking"),
    ("case-tracker", "archive"), ("cold-case-files", "archive"), ("history-of-hollywood", "archive")])
def test_disclosure_variant_by_show_format(show_id, variant):
    assert disclosure.variant_for(SHOWS[show_id]) == variant


def test_disclosure_variant_falls_back_to_lane():
    assert disclosure.variant_for({"lane": "breaking"}) == "breaking"
    assert disclosure.variant_for({"format": "mystery", "lane": "archive"}) == "archive"
    assert disclosure.variant_for({}) == "daily"


@pytest.mark.parametrize("show_id", sorted(SHOWS))
def test_disclosure_says_what_the_standards_require(show_id):
    text = disclosure.disclosure_text(SHOWS[show_id]).lower()
    for needed in ("ai-generated voices", "automated newsroom", "synthetic", "independent sources",
                   "show notes", "report-an-error", "correct it in public", "curious and creative llc",
                   "curious and creative network"):
        assert needed in text, needed
    assert "&" not in text                                                    # it is read aloud
    assert len(text.split()) < 140


def test_disclosure_variants_differ_where_they_should():
    breaking = disclosure.disclosure_text(SHOWS["breaking-desk"]).lower()
    archive = disclosure.disclosure_text(SHOWS["history-of-hollywood"]).lower()
    assert "details may change" in breaking and "details may change" not in archive
    assert "where the record is thin" in archive and "where the record is thin" not in breaking


def test_disclosure_presumption_line_only_for_strict_lane():
    assert "presumed innocent" in disclosure.disclosure_text(SHOWS["la-courts"])
    assert "presumed innocent" in disclosure.disclosure_text(SHOWS["cold-case-files"])
    for show_id in ("columbia-daily", "breaking-desk", "history-of-hollywood"):
        assert "presumed innocent" not in disclosure.disclosure_text(SHOWS[show_id])
    strict = disclosure._texts(SHOWS["la-courts"])
    assert strict[-2] == disclosure.PRESUMPTION and "responsible" in strict[-1]       # sign-off stays last


def test_disclosure_lines_use_the_disclosure_voice_and_carry_no_claims():
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    lines = disclosure.disclosure_lines(cfg, VOICES)
    assert lines and {l.speaker for l in lines} == {VOICES["disclosure_voice"]}
    assert {l.segment for l in lines} == {"disclosure"} and all(l.claim_ids == [] for l in lines)
    assert len({l.id for l in lines}) == len(lines)
    assert lines == disclosure.disclosure_lines(cfg, VOICES)                     # deterministic


def test_disclosure_voice_must_exist():
    with pytest.raises(ValueError):
        disclosure.disclosure_lines(SHOWS["columbia-daily"], {})
    assert disclosure.disclosure_lines(SHOWS["columbia-daily"], {"personas": {"zed": {}}})[0].speaker == "zed"


def test_ensure_disclosure_is_idempotent_last_and_replaces_stale_wording():
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    stale = ScriptLine("ln_old", "mara", "Old disclosure wording.", ["clm_old"], "disclosure")
    script = build_script([COUNCIL], disclosure_on=False)
    script.lines.insert(1, stale)                                  # in the middle, with a stray claim
    script.claims.append(Claim(id="clm_old", text="Old wording.", line_ids=["ln_old"]))
    once = disclosure.ensure_disclosure(script, cfg, VOICES)
    twice = disclosure.ensure_disclosure(once, cfg, VOICES)
    assert once == twice
    n = len(disclosure.disclosure_lines(cfg, VOICES))
    assert [l.segment for l in once.lines][-n:] == ["disclosure"] * n
    assert sum(l.segment == "disclosure" for l in once.lines) == n
    assert all(l.id != "ln_old" for l in once.lines) and {c.id for c in once.claims} == {"clm_a"}
    assert any(l.id == "ln_old" for l in script.lines)                           # input untouched


def test_gate_blocks_without_disclosure_and_passes_with_it():
    cfg = {**SHOWS["columbia-daily"], "id": "columbia-daily"}
    bare = build_script([COUNCIL], disclosure_on=False)
    llm = LLM(dry_run=True)

    def decide(script):
        v = verify(script, llm, OWNERS)
        return gate.decide(script, v, factcheck.fact_check(script, v, llm), bias.bias_check(script, llm),
                           legal.legal_screen(script, llm))

    assert "S1" in {r.rule_id for r in decide(bare).reasons}
    assert decide(disclosure.ensure_disclosure(bare, cfg, VOICES)).decision == "PUBLISH"


# ================================================================== producer: copywriter
def _gated_script():
    return build_script([COUNCIL, BRIDGE])


def test_copywriter_dry_run_is_schema_valid_and_sees_no_disclosure():
    llm = ScriptedLLM()
    copy = copywriter.write_copy(_gated_script(), SHOWS["columbia-daily"], llm)
    assert validate("Copy", copy) == []
    assert "synthetic" not in llm.prompt("copywriter") and "Riverbend" in llm.prompt("copywriter")
    assert llm.calls[0]["system"] == copywriter.COPY_SYSTEM


def test_copywriter_retries_once_on_a_number_not_in_the_script():
    good = {"title": "Council approves Riverbend Park money", "description": "A 5-2 vote on Tuesday.",
            "show_notes_md": "## In this episode\n- A 5-2 vote.", "social_posts": ["The council voted 5-2."],
            "keywords": ["columbia", "riverbend park"]}
    bad = {**good, "title": "7 things to know about Riverbend Park"}
    answers = iter([bad, good])
    llm = ScriptedLLM(copywriter=lambda ctx: next(answers))
    copy = copywriter.write_copy(_gated_script(), SHOWS["columbia-daily"], llm)
    assert llm.count("copywriter") == 2 and copy["title"] == good["title"]
    assert "7" in llm.calls[1]["user"]                           # the retry says which number was wrong


def test_copywriter_falls_back_to_plain_copy_when_numbers_keep_straying():
    bad = {"title": "Top 9 stories", "description": "9 big things.", "show_notes_md": "- 9 things",
           "social_posts": ["9 things you need", "The council voted 5-2."], "keywords": ["top 9", "columbia"]}
    llm = ScriptedLLM(copywriter=lambda ctx: bad)
    script = _gated_script()
    copy = copywriter.write_copy(script, SHOWS["columbia-daily"], llm)
    assert llm.count("copywriter") == 2
    assert copy["title"] == script.title and "9" not in copy["description"]
    assert copy["social_posts"] == ["The council voted 5-2."] and copy["keywords"] == ["columbia"]
    assert validate("Copy", copy) == []


def test_copywriter_clamps_lengths_and_dedupes_keywords():
    long = {"title": "T " * 200, "description": "D " * 600, "show_notes_md": " notes ",
            "social_posts": ["p " * 300, "  "], "keywords": ["A", "a ", "b"] + [f"word {c}" for c in "cdefghijklmnopqrstuvwxyz"]}
    copy = copywriter.write_copy(_gated_script(), SHOWS["columbia-daily"], ScriptedLLM(copywriter=lambda c: long))
    assert len(copy["title"]) <= copywriter.LIMITS["title"] and len(copy["description"]) <= copywriter.LIMITS["description"]
    assert len(copy["social_posts"]) == 1 and len(copy["social_posts"][0]) <= copywriter.LIMITS["social"]
    assert copy["keywords"][:2] == ["a", "b"] and len(copy["keywords"]) == copywriter.LIMITS["keywords"]


# ================================================================== hygiene
MODEL_ID = re.compile("clau" + r"de-(?:opus|sonnet|haiku|[0-9])|(?:opus|sonnet|haiku)-[0-9]", re.IGNORECASE)
MY_FILES = [*sorted((ROOT / "earlobe" / "producer").glob("*.py")), *sorted((ROOT / "earlobe" / "trust").glob("*.py")),
            pathlib.Path(__file__)]


@pytest.mark.parametrize("path", MY_FILES, ids=lambda p: p.name)
def test_no_model_ids_or_secrets_in_code(path):
    text = path.read_text(encoding="utf-8")
    assert not MODEL_ID.search(text)
    assert not re.search(r"sk-[A-Za-z0-9_-]{16,}|api[_-]?key\s*=\s*[\"'][^\"']+[\"']", text)


def test_agents_use_the_documented_tiers():
    tiers = {}
    stub = ScriptedLLM()
    script = build_script([COUNCIL])
    stories, pack = _pack_and_stories()
    writer.write_script("columbia-daily", SHOWS["columbia-daily"], stories, pack, stub, episode_date=DAY)
    run_trust_loop(script, never_called, stub, OWNERS)
    copywriter.write_copy(script, SHOWS["columbia-daily"], stub)
    for r in stub.runs:
        tiers[r.agent_id] = r.model_tier
    assert tiers == {"producer": "opus", "claim-extractor": "opus", "verifier": "opus", "fact-checker": "opus",
                     "bias-checker": "sonnet", "legal-screener": "opus", "copywriter": "sonnet"}


def test_system_prompts_still_carry_the_core_rules():
    w = writer.WRITER_SYSTEM
    for phrase in ("claim_ids", "arrested on suspicion of", "charged with", "under 18", "sexually assaulted",
                   "presumption", "independent", "wire copy", "NEVER \"disclosure\"", "spoken", "why it matters"):
        assert phrase.lower() in w.lower(), phrase
    v = verifier.VERIFIER_SYSTEM.lower()
    for phrase in ("trace", "wire", "tier 4", "have not been shown the writer", "never invent a url"):
        assert phrase in v, phrase
    assert "separate" in factcheck.FACTCHECK_SYSTEM.lower() or "second" in factcheck.FACTCHECK_SYSTEM.lower()
    assert "balance_score" in bias.BIAS_SYSTEM and "hard stop" in legal.LEGAL_SYSTEM.lower()
    assert "naming_minor" in legal.LEGAL_SYSTEM and "naming_victim" in legal.LEGAL_SYSTEM
    assert "never" in copywriter.COPY_SYSTEM.lower() and "exclamation" in copywriter.COPY_SYSTEM
