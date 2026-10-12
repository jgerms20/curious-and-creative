"""Data contracts: dataclass round-trips, JSON Schemas, validate(), and the dry-run fixtures.

Sections
  round trips   every dataclass survives to_dict / from_dict (and JSON), nested contracts included
  helpers       make_id, Script counters, vocabularies
  json schemas  each entry is valid Draft 2020-12, strict, and in sync with the dataclasses
  validate      error reporting, with and without the jsonschema package
  fixtures      fixtures.fake(kind) validates for every kind (skipped until fixtures import)
"""
import dataclasses
import json
import sys

import pytest

from earlobe import schemas
from earlobe.schemas import (
    BIAS_TYPES,
    CLAIM_TYPES,
    DECISIONS,
    EPISODE_STATUS,
    FACT_RATINGS,
    JSON_SCHEMAS,
    LANE_POLICIES,
    LEGAL_RISKS,
    RISK_FLAGS,
    SEVERITY,
    SOURCE_KINDS,
    SOURCE_TIERS,
    VERIFY_STATUS,
    AgentRun,
    BiasIssue,
    BiasReport,
    Claim,
    Contract,
    Correction,
    Episode,
    EvidenceSource,
    FactCheckFinding,
    FactCheckReport,
    GateDecision,
    GateReason,
    LegalIssue,
    LegalReport,
    Script,
    ScriptLine,
    Signal,
    Source,
    Story,
    VerifierFinding,
    VerifierReport,
    make_id,
    validate,
)

try:
    from earlobe import fixtures
except ImportError:      # module not written yet (or a dependency missing): skip those checks only
    fixtures = None
needs_fixtures = pytest.mark.skipif(fixtures is None, reason="earlobe.fixtures not importable yet")


# ---------------------------------------------------------------- sample objects
# Every optional field is set to a NON-default value so a round trip that drops it would fail.
def _source():
    return Source(id="src_1", url="https://sample.invalid/a", outlet="Sample Gazette", title="Council votes",
                  published_at="2026-10-12T09:00:00Z", retrieved_at="2026-10-12T09:05:00Z", tier=1,
                  kind="court_record", owner_group="Sample Media", syndicated_from="Associated Press",
                  excerpt="Council approved the budget.", market="columbia-sc")


def _signal():
    return Signal(id="sig_1", sensor="beat-columbia-sc", market="columbia-sc", beat="government",
                  title="Council votes", url="https://sample.invalid/a", outlet="Sample Gazette",
                  published_at="2026-10-12T09:00:00Z", summary="A vote happened.", kind="press_release",
                  tier=2, raw={"event": "columbia-sc-0", "n": [1, 2]})


def _story():
    return Story(id="sty_1", market="columbia-sc", beat="government", headline="Council votes",
                 summary="A vote happened.", first_seen="2026-10-12T09:00:00Z", signal_ids=["sig_1"],
                 source_ids=["src_1"], outlets=["Sample Gazette"], independent_outlets=3,
                 official_confirmation=True, newsworthiness=72, velocity=1.5, breaking=True,
                 risk_flags=["crime"], entities=["Richland County"], assigned_shows=["columbia-daily"])


def _claim():
    return Claim(id="clm_1", text="Council approved $12 million.", type="number", line_ids=["ln_1"],
                 source_ids=["src_1"], entities=["Richland County"], risk_flags=["financial"], attributed=True)


def _line():
    return ScriptLine(id="ln_1", speaker="host_a", text="Council approved $12 million.",
                      claim_ids=["clm_1"], segment="intro")


def _script():
    return Script(id="scr_1", show_id="columbia-daily", episode_date="2026-10-12", title="Tuesday brief",
                  lines=[_line(), ScriptLine(id="ln_2", speaker="host_b", text="This show is AI.",
                                             segment="disclosure")],
                  claims=[_claim(), Claim(id="clm_2", text="Police said X.", type="attribution")],
                  sources=[_source()], story_ids=["sty_1"], lane_policy="strict", revision=2,
                  notes_for_checkers="Check the vote count.")


def _evidence():
    return EvidenceSource(url="https://sample.invalid/e", outlet="Sample Wire", tier=2,
                          owner_group="Sample Wire Inc", supports=False, note="Contradicts the date.")


def _vfinding():
    return VerifierFinding(claim_id="clm_1", status="single_source", independent_count=1, has_official=True,
                           traced_to_original=True, evidence=[_evidence(), _evidence()], note="One record.")


def _vreport():
    return VerifierReport(script_id="scr_1", findings=[_vfinding()], searches_used=7)


def _ffinding():
    return FactCheckFinding(claim_id="clm_1", rating="misleading", issue="Stale figure.",
                            suggested_fix="Say 2023.")


def _freport():
    return FactCheckReport(script_id="scr_1", findings=[_ffinding()])


def _bissue():
    return BiasIssue(line_id="ln_1", type="loaded_language", severity="high", explanation="Charged word.",
                     suggestion="Use a neutral verb.")


def _breport():
    return BiasReport(script_id="scr_1", balance_score=64, issues=[_bissue()],
                      missing_perspectives=["the tenants"])


def _lissue():
    return LegalIssue(target_id="clm_1", risk="naming_minor", severity="medium", explanation="Names a minor.",
                      fix="Remove the name.")


def _lreport():
    return LegalReport(script_id="scr_1", issues=[_lissue()])


def _reason():
    return GateReason(rule_id="V3", detail="1 independent source(s)", target_id="clm_1", blocking=False)


def _decision():
    return GateDecision(script_id="scr_1", decision="HOLD", lane_policy="breaking", revision=1,
                        reasons=[_reason()], rewrite_instructions=["Find more sourcing."],
                        scores={"corroboration_rate": 0.5, "balance_score": 80}, recheck_after_minutes=15)


def _episode():
    return Episode(id="ep_1", show_id="columbia-daily", script_id="scr_1", title="Tuesday", description="d",
                   show_notes_md="# Notes", audio_path="data/a.mp3", audio_url="https://sample.invalid/a.mp3",
                   duration_sec=421, published_at="2026-10-12T13:00:00Z", guid="g-1", status="published",
                   disclosure_text="AI-generated.", transcript_path="data/a.txt",
                   gate=_decision().to_dict(), source_count=4)


def _correction():
    return Correction(id="cor_1", episode_id="ep_1", description="Wrong vote count.", claim_id="clm_1",
                      reported_by="monitor:recheck", created_at="2026-10-13T08:00:00Z", status="applied",
                      action="reissue")


def _agent_run():
    return AgentRun(agent_id="verifier", run_id="run_1", model_tier="opus", started_at="2026-10-12T09:00:00Z",
                    finished_at="2026-10-12T09:01:00Z", input_tokens=1200, output_tokens=300, web_searches=5,
                    usd_estimate=0.42, ok=False, error="timeout")


SAMPLES = {
    Source: _source, Signal: _signal, Story: _story, Claim: _claim, ScriptLine: _line, Script: _script,
    EvidenceSource: _evidence, VerifierFinding: _vfinding, VerifierReport: _vreport,
    FactCheckFinding: _ffinding, FactCheckReport: _freport, BiasIssue: _bissue, BiasReport: _breport,
    LegalIssue: _lissue, LegalReport: _lreport, GateReason: _reason, GateDecision: _decision,
    Episode: _episode, Correction: _correction, AgentRun: _agent_run,
}
CLASSES = list(SAMPLES)
IDS = [c.__name__ for c in CLASSES]


def _contract_classes():
    return [v for v in vars(schemas).values()
            if isinstance(v, type) and issubclass(v, Contract) and v is not Contract]


# ---------------------------------------------------------------- round trips
def test_every_contract_dataclass_has_a_sample():
    """A new dataclass in schemas.py fails here until it is added to SAMPLES (and so round-tripped)."""
    assert set(_contract_classes()) == set(SAMPLES)


@pytest.mark.parametrize("cls", CLASSES, ids=IDS)
def test_samples_set_every_optional_field_to_a_non_default(cls):
    obj = SAMPLES[cls]()
    for f in dataclasses.fields(cls):
        if f.default is not dataclasses.MISSING:
            assert getattr(obj, f.name) != f.default, f"{cls.__name__}.{f.name} sample equals its default"
        elif f.default_factory is not dataclasses.MISSING:
            assert getattr(obj, f.name) != f.default_factory(), f"{cls.__name__}.{f.name} sample is empty"


@pytest.mark.parametrize("cls", CLASSES, ids=IDS)
def test_round_trip_via_dict(cls):
    obj = SAMPLES[cls]()
    data = obj.to_dict()
    assert isinstance(data, dict) and set(data) == {f.name for f in dataclasses.fields(cls)}
    assert cls.from_dict(data) == obj


@pytest.mark.parametrize("cls", CLASSES, ids=IDS)
def test_round_trip_via_json(cls):
    obj = SAMPLES[cls]()
    text = obj.to_json()
    assert cls.from_dict(json.loads(text)) == obj
    assert json.loads(text) == obj.to_dict()          # to_dict holds only JSON-native values


@pytest.mark.parametrize("cls", CLASSES, ids=IDS)
def test_from_dict_rebuilds_nested_contracts(cls):
    back = cls.from_dict(SAMPLES[cls]().to_dict())
    nested = {field: sub for (owner, field), sub in schemas._NESTED.items() if owner == cls.__name__}
    for field, sub in nested.items():
        items = getattr(back, field)
        assert items, f"{cls.__name__}.{field} sample is empty, so nesting is untested"
        assert all(isinstance(x, sub) for x in items), f"{cls.__name__}.{field} not rebuilt as {sub.__name__}"


def test_deeply_nested_report_keeps_types_at_every_level():
    back = VerifierReport.from_dict(_vreport().to_dict())
    finding = back.findings[0]
    assert isinstance(finding, VerifierFinding)
    assert all(isinstance(e, EvidenceSource) for e in finding.evidence) and len(finding.evidence) == 2
    script = Script.from_dict(_script().to_dict())
    assert [type(x) for x in (script.lines + script.claims + script.sources)] == \
        [ScriptLine, ScriptLine, Claim, Claim, Source]


def test_to_dict_returns_plain_dicts_not_dataclasses():
    data = _script().to_dict()
    assert all(type(x) is dict for x in data["lines"] + data["claims"] + data["sources"])


def test_episode_gate_field_stays_a_plain_dict():
    """Episode.gate holds GateDecision.to_dict() as data; it must not be rebuilt as a contract."""
    back = Episode.from_dict(_episode().to_dict())
    assert type(back.gate) is dict and back.gate["decision"] == "HOLD"


@pytest.mark.parametrize("cls", CLASSES, ids=IDS)
def test_required_fields_only_fills_the_defaults(cls):
    full = SAMPLES[cls]().to_dict()
    required = {f.name for f in dataclasses.fields(cls)
                if f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING}
    obj = cls.from_dict({k: v for k, v in full.items() if k in required})
    assert obj == cls(**{k: getattr(obj, k) for k in required})
    for f in dataclasses.fields(cls):
        if f.name not in required:
            default = f.default if f.default is not dataclasses.MISSING else f.default_factory()
            assert getattr(obj, f.name) == default


def test_from_dict_ignores_unknown_keys():
    data = {**_claim().to_dict(), "surprise": 1, "another": [1]}
    assert Claim.from_dict(data) == _claim()


@pytest.mark.parametrize("bad", [{}, None])
def test_from_dict_without_required_fields_raises(bad):
    with pytest.raises(TypeError):
        Source.from_dict(bad)


def test_mutable_defaults_are_not_shared_between_instances():
    a = Story(id="a", market="m", beat="b", headline="h", summary="s", first_seen="t")
    b = Story(id="b", market="m", beat="b", headline="h", summary="s", first_seen="t")
    a.signal_ids.append("sig_x")
    a.risk_flags.append("crime")
    assert b.signal_ids == [] and b.risk_flags == []
    d1, d2 = GateDecision("s", "PUBLISH", "standard", 0), GateDecision("s", "PUBLISH", "standard", 0)
    d1.scores["x"] = 1
    assert d2.scores == {}


def test_from_dict_passes_through_items_that_are_already_contracts():
    line = _line()
    script = Script.from_dict({"id": "s", "show_id": "x", "episode_date": "d", "title": "t", "lines": [line]})
    assert script.lines == [line]


def test_from_dict_rebuilds_a_nested_dict_value(monkeypatch):
    """The single-object branch (a field holding one contract, not a list)."""
    monkeypatch.setitem(schemas._NESTED, ("Episode", "gate"), GateDecision)
    back = Episode.from_dict(_episode().to_dict())
    assert isinstance(back.gate, GateDecision) and back.gate.decision == "HOLD"


# ---------------------------------------------------------------- helpers and vocabularies
def test_make_id_is_deterministic_and_prefixed():
    a = make_id("clm", "Council", "approved")
    assert a == make_id("clm", "Council", "approved")
    prefix, digest = a.split("_")
    assert prefix == "clm" and len(digest) == 12 and int(digest, 16) >= 0


def test_make_id_changes_with_parts_prefix_and_order():
    base = make_id("clm", "a", "b")
    assert base != make_id("clm", "b", "a")
    assert base != make_id("clm", "a", "c")
    assert base != make_id("clm", "ab")
    assert make_id("clm", "a", "b").split("_")[1] == make_id("sty", "a", "b").split("_")[1]
    assert make_id("sty", "a", "b") != base
    assert make_id("n", 1, 2) == make_id("n", "1", "2")      # parts are stringified


def test_make_id_handles_unicode():
    assert make_id("src", "café ☕").startswith("src_")


def test_script_counters():
    s = Script(id="s", show_id="x", episode_date="d", title="t", lines=[
        ScriptLine(id="1", speaker="a", text="one two three"), ScriptLine(id="2", speaker="b", text="four  five")])
    assert s.word_count() == 5
    assert s.char_count() == len("one two three") + len("four  five")
    assert s.est_duration_sec(wpm=60) == 5
    assert s.est_duration_sec() == round(5 / 155 * 60)
    empty = Script(id="e", show_id="x", episode_date="d", title="t")
    assert (empty.word_count(), empty.char_count(), empty.est_duration_sec()) == (0, 0, 0)


@pytest.mark.parametrize("vocab", [CLAIM_TYPES, RISK_FLAGS, VERIFY_STATUS, FACT_RATINGS, BIAS_TYPES, LEGAL_RISKS,
                                   SEVERITY, DECISIONS, LANE_POLICIES, EPISODE_STATUS, SOURCE_KINDS])
def test_vocabularies_have_no_duplicates(vocab):
    assert len(vocab) == len(set(vocab)) and all(isinstance(v, str) and v for v in vocab)


def test_fixed_vocabularies():
    assert DECISIONS == ["PUBLISH", "REWRITE", "HOLD", "KILL"]
    assert SEVERITY == ["low", "medium", "high"]
    assert sorted(SOURCE_TIERS) == [1, 2, 3, 4]


# ---------------------------------------------------------------- JSON Schemas
def _jsonschema():
    return pytest.importorskip("jsonschema")


def _walk(node, path=()):
    """Yield (path, subschema) for every schema node."""
    yield path, node
    if node.get("type") == "object":
        for key, sub in node["properties"].items():
            yield from _walk(sub, path + (key,))
    elif node.get("type") == "array":
        yield from _walk(node["items"], path + ("[]",))


def _node(kind, *path):
    node = JSON_SCHEMAS[kind]
    for p in path:
        node = node["properties"][p]
        node = node["items"] if node["type"] == "array" else node
    return node


def test_json_schemas_cover_the_agent_outputs():
    assert set(JSON_SCHEMAS) == {"Script", "VerifierReport", "FactCheckReport", "BiasReport", "LegalReport",
                                 "StoryTriage", "Copy", "ArchivePack"}


@pytest.mark.parametrize("kind", sorted(JSON_SCHEMAS))
def test_schema_is_valid_draft_2020_12(kind):
    jsonschema = _jsonschema()
    jsonschema.Draft202012Validator.check_schema(JSON_SCHEMAS[kind])      # raises SchemaError if not
    json.dumps(JSON_SCHEMAS[kind])                                        # and is plain JSON


@pytest.mark.parametrize("kind", sorted(JSON_SCHEMAS))
def test_every_object_is_closed_and_requires_only_declared_properties(kind):
    """Structured outputs need additionalProperties false; a required name must be a real property."""
    objects = [(p, n) for p, n in _walk(JSON_SCHEMAS[kind]) if n.get("type") == "object"]
    assert objects
    for path, node in objects:
        where = f"{kind}/{'/'.join(path)}"
        assert node["additionalProperties"] is False, where
        assert set(node["required"]) <= set(node["properties"]), where


@pytest.mark.parametrize("kind", sorted(JSON_SCHEMAS))
def test_every_property_is_required(kind):
    for path, node in _walk(JSON_SCHEMAS[kind]):
        if node.get("type") == "object":
            assert set(node["required"]) == set(node["properties"]), f"{kind}/{'/'.join(path)}"


@pytest.mark.parametrize("kind, path, vocab", [
    ("Script", ("lines", "segment"), ["cold_open", "intro", "body", "kicker", "disclosure", "outro"]),
    ("Script", ("claims", "type"), CLAIM_TYPES),
    ("Script", ("claims", "risk_flags"), RISK_FLAGS),
    ("VerifierReport", ("findings", "status"), VERIFY_STATUS),
    ("FactCheckReport", ("findings", "rating"), FACT_RATINGS),
    ("BiasReport", ("issues", "type"), BIAS_TYPES),
    ("BiasReport", ("issues", "severity"), SEVERITY),
    ("LegalReport", ("issues", "risk"), LEGAL_RISKS),
    ("LegalReport", ("issues", "severity"), SEVERITY),
    ("StoryTriage", ("stories", "risk_flags"), RISK_FLAGS),
], ids=lambda v: "/".join(v) if isinstance(v, tuple) and all(isinstance(x, str) for x in v) else None)
def test_schema_enums_match_the_vocabularies(kind, path, vocab):
    node = _node(kind, *path)
    node = node["items"] if node.get("type") == "array" else node
    assert node["enum"] == list(vocab)


DATACLASS_FOR = [
    ("Script", (), Script), ("Script", ("lines",), ScriptLine), ("Script", ("claims",), Claim),
    ("VerifierReport", ("findings",), VerifierFinding),
    ("VerifierReport", ("findings", "evidence"), EvidenceSource),
    ("FactCheckReport", (), FactCheckReport), ("FactCheckReport", ("findings",), FactCheckFinding),
    ("BiasReport", (), BiasReport), ("BiasReport", ("issues",), BiasIssue),
    ("LegalReport", ("issues",), LegalIssue),
]


@pytest.mark.parametrize("kind, path, cls", DATACLASS_FOR,
                         ids=[f"{k}/{'/'.join(p)}->{c.__name__}" for k, p, c in DATACLASS_FOR])
def test_schema_properties_are_dataclass_fields(kind, path, cls):
    """Schema and dataclass drift apart silently otherwise; from_dict would drop the extra keys."""
    props = set(_node(kind, *path)["properties"])
    assert props <= {f.name for f in dataclasses.fields(cls)}, props - {f.name for f in dataclasses.fields(cls)}


@pytest.mark.parametrize("kind, path, cls", [d for d in DATACLASS_FOR if d[1]],
                         ids=[f"{k}/{'/'.join(p)}" for k, p, _ in DATACLASS_FOR if p])
def test_required_dataclass_fields_are_in_the_item_schema(kind, path, cls):
    required = {f.name for f in dataclasses.fields(cls)
                if f.default is dataclasses.MISSING and f.default_factory is dataclasses.MISSING}
    assert required <= set(_node(kind, *path)["properties"])


# ---------------------------------------------------------------- validate()
GOOD = {
    "Script": {"title": "t", "lines": [{"id": "ln_1", "speaker": "host_a", "text": "hi", "claim_ids": ["clm_1"],
                                        "segment": "body"}],
               "claims": [{"id": "clm_1", "text": "x", "type": "fact", "line_ids": ["ln_1"], "source_ids": [],
                           "risk_flags": ["crime"], "attributed": False}]},
    "VerifierReport": {"findings": [{"claim_id": "clm_1", "status": "corroborated", "independent_count": 2,
                                     "has_official": False, "traced_to_original": True, "note": "",
                                     "evidence": [{"url": "u", "outlet": "o", "tier": 2, "owner_group": "g",
                                                   "supports": True, "note": ""}]}]},
    "FactCheckReport": {"findings": [{"claim_id": "clm_1", "rating": "accurate", "issue": "", "suggested_fix": ""}]},
    "BiasReport": {"balance_score": 80, "issues": [{"line_id": "ln_1", "type": "framing", "severity": "low",
                                                    "explanation": "", "suggestion": ""}],
                   "missing_perspectives": []},
    "LegalReport": {"issues": [{"target_id": "clm_1", "risk": "privacy", "severity": "low", "explanation": "",
                                "fix": ""}]},
    "StoryTriage": {"stories": []},
    "Copy": {"title": "t", "description": "d", "show_notes_md": "m", "social_posts": ["p"], "keywords": ["k"]},
    "ArchivePack": {"subject": "s", "summary": "m", "risk_flags": [], "uncertain": [],
                    "sources": [{"url": "u", "outlet": "o", "title": "t", "published_at": "1927-05-18",
                                 "tier": 1, "kind": "archive", "excerpt": ""}]},
}


def test_good_examples_cover_every_schema():
    assert set(GOOD) == set(JSON_SCHEMAS)


@pytest.mark.parametrize("kind", sorted(GOOD))
def test_validate_accepts_a_well_formed_document(kind):
    assert validate(kind, GOOD[kind]) == []


@pytest.mark.parametrize("kind", sorted(GOOD))
def test_validate_rejects_a_missing_top_level_field(kind):
    data = dict(GOOD[kind])
    data.pop(next(iter(data)))
    errors = validate(kind, data)
    assert errors and any("required" in e.lower() or "missing" in e.lower() for e in errors)


def test_validate_reports_the_path_of_a_bad_nested_value():
    data = json.loads(json.dumps(GOOD["VerifierReport"]))
    data["findings"][0]["status"] = "probably"
    errors = validate("VerifierReport", data)
    assert len(errors) == 1 and errors[0].startswith("findings/0/status:")


@pytest.mark.parametrize("mutate, fragment", [
    (lambda d: d.update(balance_score="80"), "balance_score"),            # wrong type
    (lambda d: d.update(extra=1), "extra"),                               # additionalProperties
    (lambda d: d["issues"][0].update(severity="severe"), "issues/0/severity"),
    (lambda d: d["issues"][0].pop("type"), "issues/0"),
], ids=["wrong-type", "extra-property", "bad-enum", "missing-nested"])
def test_validate_flags_bad_documents(mutate, fragment):
    _jsonschema()
    data = json.loads(json.dumps(GOOD["BiasReport"]))
    mutate(data)
    errors = validate("BiasReport", data)
    assert errors and any(fragment in e for e in errors)


def test_validate_root_errors_use_a_root_marker():
    _jsonschema()
    errors = validate("LegalReport", [])
    assert errors and errors[0].startswith("<root>:")


def test_validate_unknown_kind_raises_key_error():
    with pytest.raises(KeyError):
        validate("NoSuchKind", {})


def test_validate_falls_back_to_a_structural_check_without_jsonschema(monkeypatch):
    monkeypatch.setitem(sys.modules, "jsonschema", None)         # makes `import jsonschema` raise ImportError
    assert validate("LegalReport", {"issues": []}) == []
    assert validate("BiasReport", {"balance_score": 1}) == ["missing field: issues", "missing field: missing_perspectives"]
    assert validate("Copy", None) == [f"missing field: {k}" for k in JSON_SCHEMAS["Copy"]["required"]]


# ---------------------------------------------------------------- fixtures (dry-run data)
@needs_fixtures
@pytest.mark.parametrize("kind", sorted(JSON_SCHEMAS))
def test_fake_output_validates_against_its_schema(kind):
    assert validate(kind, fixtures.fake(kind)) == []


@needs_fixtures
@pytest.mark.parametrize("kind", sorted(JSON_SCHEMAS))
def test_fake_is_deterministic(kind):
    assert fixtures.fake(kind) == fixtures.fake(kind)


@needs_fixtures
def test_fake_unknown_kind_is_a_clear_error():
    with pytest.raises(ValueError, match="NoSuchKind"):
        fixtures.fake("NoSuchKind")


@needs_fixtures
def test_fake_script_loads_as_contracts():
    script = Script.from_dict({"id": "scr_fake", "show_id": "columbia-daily", "episode_date": "2026-10-12",
                               **fixtures.fake("Script")})
    assert script.lines and script.claims
    assert all(isinstance(x, ScriptLine) for x in script.lines)
    assert all(isinstance(x, Claim) for x in script.claims)
    line_ids = {x.id for x in script.lines}
    assert {i for c in script.claims for i in c.line_ids} <= line_ids
    assert {i for x in script.lines for i in x.claim_ids} <= {c.id for c in script.claims}


@needs_fixtures
def test_fake_reports_load_as_contracts():
    v = VerifierReport.from_dict({"script_id": "scr_fake", **fixtures.fake("VerifierReport", claim_ids=["clm_a"])})
    assert [f.claim_id for f in v.findings] == ["clm_a"] and isinstance(v.findings[0], VerifierFinding)
    assert all(isinstance(e, EvidenceSource) for e in v.findings[0].evidence)
    f = FactCheckReport.from_dict({"script_id": "scr_fake", **fixtures.fake("FactCheckReport", claim_ids=["clm_a"])})
    assert isinstance(f.findings[0], FactCheckFinding)
    b = BiasReport.from_dict({"script_id": "scr_fake", **fixtures.fake("BiasReport")})
    assert 0 <= b.balance_score <= 100
    legal = LegalReport.from_dict({"script_id": "scr_fake", **fixtures.fake("LegalReport")})
    assert legal.issues == []


@needs_fixtures
@pytest.mark.parametrize("kind", ["VerifierReport", "FactCheckReport"])
def test_fake_checker_reports_cover_the_claims_of_the_script_they_are_given(kind):
    script = _script()
    ids = [f["claim_id"] for f in fixtures.fake(kind, script=script)["findings"]]
    assert ids == [c.id for c in script.claims]


@needs_fixtures
def test_fake_verifier_evidence_agrees_with_its_own_count():
    for f in fixtures.fake("VerifierReport", claim_ids=["clm_a", "clm_b", "clm_c"])["findings"]:
        assert len(f["evidence"]) == f["independent_count"]
        assert len({e["owner_group"] for e in f["evidence"]}) == f["independent_count"]
        assert f["has_official"] == any(e["tier"] == 1 for e in f["evidence"])


@needs_fixtures
@pytest.mark.parametrize("market", ["columbia-sc", "los-angeles", "new-york", "chicago", "national"])
def test_sample_signals_are_valid_signals_that_round_trip(market):
    signals = fixtures.sample_signals(market)
    assert signals and all(isinstance(s, Signal) for s in signals)
    assert len({s.id for s in signals}) == len(signals)
    assert all(s.market == market and s.url.startswith("https://sample.invalid/") for s in signals)
    assert all(s.tier in SOURCE_TIERS and s.kind in SOURCE_KINDS for s in signals)
    assert all(Signal.from_dict(s.to_dict()) == s for s in signals)


@needs_fixtures
def test_sample_signals_unknown_market_is_a_clear_error():
    with pytest.raises(ValueError, match="nowhere"):
        fixtures.sample_signals("nowhere")
