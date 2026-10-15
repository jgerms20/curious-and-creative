"""earlobe.llm without keys or network.

Part 1 exercises dry-run (fixtures only). Part 2 drives the real-call code paths
(structured retry, refusal, pause_turn, repair, cost) with a scripted stand-in for the
SDK client, so nothing here needs ANTHROPIC_API_KEY or a connection.
"""
import json
import sys
from types import SimpleNamespace

import pytest

from earlobe import config, llm
from earlobe.schemas import JSON_SCHEMAS, validate

GOOD_COPY = {"title": "T", "description": "D", "show_notes_md": "N",
             "social_posts": ["p"], "keywords": ["k"]}


@pytest.fixture
def fixtures():
    return pytest.importorskip("earlobe.fixtures")


# ---------------------------------------------------------------- part 1: dry-run
def test_dry_run_structured_returns_fixture_and_logs_run(fixtures):
    client = llm.LLM(dry_run=True)
    out = client.structured("copywriter", "sonnet", "sys", "user", "Copy")
    assert out == fixtures.fake("Copy")
    assert len(client.runs) == 1
    run = client.runs[0]
    assert (run.agent_id, run.model_tier, run.ok) == ("copywriter", "sonnet", True)
    assert run.input_tokens == run.output_tokens == run.web_searches == 0
    assert run.usd_estimate == 0 and run.finished_at


def test_dry_run_research_returns_fixture(fixtures):
    client = llm.LLM(dry_run=True)
    out = client.research("verifier", "opus", "sys", "user", "VerifierReport", max_searches=3)
    assert out == fixtures.fake("VerifierReport")
    assert client.runs[0].agent_id == "verifier"


def test_dry_run_passes_ctx_to_fixtures(fixtures, monkeypatch):
    seen = []
    monkeypatch.setattr(fixtures, "fake", lambda kind, **ctx: seen.append((kind, ctx)) or {})
    client = llm.LLM(dry_run=True)
    client.structured("a", "haiku", "s", "u", "Copy", ctx={"show_id": "columbia-daily"})
    client.research("b", "haiku", "s", "u", "BiasReport", ctx={"script_id": "scr_1"})
    assert seen == [("Copy", {"show_id": "columbia-daily"}), ("BiasReport", {"script_id": "scr_1"})]


@pytest.mark.parametrize("kind", sorted(JSON_SCHEMAS))
def test_dry_run_fixture_matches_schema(fixtures, kind):
    out = llm.LLM(dry_run=True).structured("a", "sonnet", "s", "u", kind)
    assert validate(kind, out) == []


def test_dry_run_needs_no_env_or_sdk(fixtures, monkeypatch):
    for var in ("ANTHROPIC_API_KEY", "EARLOBE_MODEL_OPUS", "EARLOBE_MODEL_SONNET",
                "EARLOBE_MODEL_HAIKU", "EARLOBE_FALLBACKS"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setitem(sys.modules, "anthropic", None)    # any import of the SDK would raise
    assert llm.LLM(dry_run=True).structured("a", "opus", "s", "u", "Copy")


def test_unknown_kind_is_rejected():
    with pytest.raises(llm.LLMError, match="unknown schema kind"):
        llm.LLM(dry_run=True).structured("a", "opus", "s", "u", "NoSuchKind")


# ---------------------------------------------------------------- part 2: stubbed client
def text_block(text):
    return SimpleNamespace(type="text", text=text)


def reply(*blocks, stop="end_turn", inp=100, out=50, searches=0, details=None):
    usage = SimpleNamespace(input_tokens=inp, output_tokens=out,
                            cache_creation_input_tokens=0, cache_read_input_tokens=0,
                            server_tool_use=SimpleNamespace(web_search_requests=searches))
    return SimpleNamespace(content=list(blocks), stop_reason=stop, usage=usage,
                           stop_details=details)


class FakeClient:
    """Scripted replacement for anthropic.Anthropic; records every create() call."""

    def __init__(self, *replies):
        self.replies = list(replies)
        self.calls = []        # (namespace, kwargs)
        self.messages = SimpleNamespace(create=lambda **kw: self._next("messages", kw))
        self.beta = SimpleNamespace(
            messages=SimpleNamespace(create=lambda **kw: self._next("beta", kw)))

    def _next(self, ns, kwargs):
        self.calls.append((ns, kwargs))
        return self.replies.pop(0)


@pytest.fixture(autouse=True)
def stub_models(monkeypatch):
    monkeypatch.setattr(config, "model_for", lambda tier: f"stub-model-{tier}")
    monkeypatch.delenv("EARLOBE_FALLBACKS", raising=False)
    monkeypatch.delenv("EARLOBE_MODEL_FALLBACK", raising=False)


def make(*replies):
    client = FakeClient(*replies)
    return llm.LLM(client=client), client


def test_structured_request_shape_and_cost(monkeypatch):
    monkeypatch.setattr(config, "PRICES",
                        {"sonnet": {"input": 2.0, "output": 10.0}, "web_search": 0.01},
                        raising=False)
    model, client = make(reply(text_block(json.dumps(GOOD_COPY)), inp=1_000_000, out=500_000))
    assert model.structured("copywriter", "sonnet", "SYS", "USER", "Copy", effort="high") == GOOD_COPY
    ns, kw = client.calls[0]
    assert ns == "messages" and kw["model"] == "stub-model-sonnet"
    assert kw["max_tokens"] == 16000 and kw["system"] == "SYS"
    assert kw["messages"] == [{"role": "user", "content": "USER"}]
    assert kw["thinking"] == {"type": "adaptive"}
    assert kw["output_config"] == {"format": {"type": "json_schema", "schema": JSON_SCHEMAS["Copy"]},
                                   "effort": "high"}
    assert "tools" not in kw
    run = model.runs[0]
    assert (run.input_tokens, run.output_tokens, run.ok) == (1_000_000, 500_000, True)
    assert run.usd_estimate == pytest.approx(2.0 + 5.0)


def test_structured_retries_once_with_errors_appended():
    bad = {k: v for k, v in GOOD_COPY.items() if k != "keywords"}
    model, client = make(reply(text_block(json.dumps(bad)), inp=10, out=5),
                         reply(text_block(json.dumps(GOOD_COPY)), inp=20, out=7))
    assert model.structured("a", "haiku", "s", "u", "Copy") == GOOD_COPY
    retry_msgs = client.calls[1][1]["messages"]
    assert [m["role"] for m in retry_msgs] == ["user", "assistant", "user"]
    assert "keywords" in retry_msgs[-1]["content"]
    assert len(model.runs) == 1                                 # one AgentRun per call
    assert (model.runs[0].input_tokens, model.runs[0].output_tokens) == (30, 12)


def test_structured_gives_up_after_one_retry():
    bad = text_block(json.dumps({"title": "only"}))
    model, client = make(reply(bad), reply(bad))
    with pytest.raises(llm.LLMError, match="failed Copy validation"):
        model.structured("a", "haiku", "s", "u", "Copy")
    assert len(client.calls) == 2
    assert model.runs[0].ok is False and "validation" in model.runs[0].error


def test_refusal_is_checked_before_content():
    details = SimpleNamespace(category="cyber", explanation="declined")
    model, _ = make(reply(text_block("not json"), stop="refusal", details=details))
    with pytest.raises(llm.LLMRefusal, match="cyber"):
        model.structured("a", "opus", "s", "u", "Copy")
    assert model.runs[0].ok is False


def test_max_tokens_is_an_error_not_a_retry():
    model, client = make(reply(text_block('{"title": "cut off'), stop="max_tokens"))
    with pytest.raises(llm.LLMError, match="max_tokens"):
        model.structured("a", "opus", "s", "u", "Copy")
    assert len(client.calls) == 1


def test_missing_model_names_the_env_var(monkeypatch):
    monkeypatch.undo()                                          # use the real config.model_for
    monkeypatch.delenv("EARLOBE_MODEL_OPUS", raising=False)
    model, client = make()
    with pytest.raises(llm.LLMError, match="EARLOBE_MODEL_OPUS"):
        model.structured("a", "opus", "s", "u", "Copy")
    assert client.calls == []


def test_research_request_shape_and_parse():
    answer = "Findings in prose.\n```json\n" + json.dumps(GOOD_COPY) + "\n```\n"
    model, client = make(reply(text_block(answer), searches=4, inp=300, out=80))
    out = model.research("verifier", "opus", "SYS", "USER", "Copy", max_searches=7)
    assert out == GOOD_COPY
    kw = client.calls[0][1]
    assert kw["tools"] == [{"type": "web_search_20260209", "name": "web_search", "max_uses": 7}]
    assert "format" not in kw["output_config"]
    assert kw["system"].startswith("SYS") and json.dumps(JSON_SCHEMAS["Copy"]) in kw["system"]
    assert model.runs[0].web_searches == 4 and len(model.runs) == 1


def test_research_resumes_on_pause_turn():
    paused = SimpleNamespace(type="server_tool_use", name="web_search")
    model, client = make(
        reply(text_block("searching"), paused, stop="pause_turn", searches=2, inp=10, out=1),
        reply(text_block("```json\n" + json.dumps(GOOD_COPY) + "\n```"), searches=1, inp=20, out=2))
    assert model.research("a", "opus", "s", "USER", "Copy") == GOOD_COPY
    resumed = client.calls[1][1]["messages"]
    assert [m["role"] for m in resumed] == ["user", "assistant"]    # no extra "continue" turn
    assert resumed[1]["content"][-1] is paused
    run = model.runs[0]
    assert (run.web_searches, run.input_tokens, run.output_tokens) == (3, 30, 3)


def test_research_pause_loop_is_capped():
    paused = reply(text_block("."), stop="pause_turn")
    model, client = make(*[paused] * (llm.MAX_CONTINUATIONS + 1))
    with pytest.raises(llm.LLMError, match="still paused"):
        model.research("a", "opus", "s", "u", "Copy")
    assert len(client.calls) == llm.MAX_CONTINUATIONS + 1


def test_research_repairs_unparseable_output_via_structured():
    model, client = make(reply(text_block("I found things but forgot the JSON."), searches=2),
                         reply(text_block(json.dumps(GOOD_COPY))))
    assert model.research("verifier", "opus", "s", "u", "Copy") == GOOD_COPY
    assert [r.agent_id for r in model.runs] == ["verifier", "verifier.repair"]
    repair_kw = client.calls[1][1]
    assert repair_kw["output_config"]["format"]["schema"] == JSON_SCHEMAS["Copy"]
    assert "forgot the JSON" in repair_kw["messages"][0]["content"]
    assert "tools" not in repair_kw


def test_research_repairs_schema_invalid_json():
    wrong = "```json\n" + json.dumps({"title": "x"}) + "\n```"
    model, _ = make(reply(text_block(wrong)), reply(text_block(json.dumps(GOOD_COPY))))
    assert model.research("a", "opus", "s", "u", "Copy") == GOOD_COPY


def test_extract_json_accepts_bare_object_and_last_fence():
    assert llm._extract_json('noise {"a": 1} tail') == {"a": 1}
    assert llm._extract_json('```json\n{"a": 1}\n```\ntext\n```json\n{"a": 2}\n```') == {"a": 2}
    with pytest.raises(ValueError):
        llm._extract_json("nothing here")


def test_fallbacks_are_off_by_default_and_env_toggled(monkeypatch):
    model, client = make(reply(text_block(json.dumps(GOOD_COPY))))
    model.structured("a", "opus", "s", "u", "Copy")
    assert client.calls[0][0] == "messages" and "fallbacks" not in client.calls[0][1]

    monkeypatch.setenv("EARLOBE_FALLBACKS", "1")
    monkeypatch.setenv("EARLOBE_MODEL_FALLBACK", "stub-fallback")
    model, client = make(reply(text_block(json.dumps(GOOD_COPY))))
    model.structured("a", "opus", "s", "u", "Copy")
    ns, kw = client.calls[0]
    assert ns == "beta" and kw["fallbacks"] == [{"model": "stub-fallback"}]
    assert kw["betas"] == [llm.FALLBACK_BETA]


def test_fallbacks_toggle_without_model_is_a_clear_error(monkeypatch):
    monkeypatch.setenv("EARLOBE_FALLBACKS", "1")
    model, _ = make()
    with pytest.raises(llm.LLMError, match="EARLOBE_MODEL_FALLBACK"):
        model.structured("a", "opus", "s", "u", "Copy")
