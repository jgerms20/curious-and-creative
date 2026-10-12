"""End to end, no keys and no network: the pipeline, the evergreen queues and the command line.

Every test runs against a temp data dir (config.DATA_DIR is monkeypatched), so nothing touches data/.
Dry runs swap Claude, ElevenLabs and the host for fixtures; a few tests hand the pipeline a dry-run LLM
whose checkers disagree, to reach the HOLD and KILL paths that a clean fixture never takes.

Sections
  helpers          temp data/config, LLMs that disagree, signals for a second breaking story
  scheduled shows  columbia-daily and la-daily: episode, notes, feed, trust log, audio, store, costs
  gate outcomes    KILL after rewrites, HOLD on the breaking lane and its retry bookkeeping
  guards           kill switch, budget, missing settings, unknown and disabled shows
  breaking         the scan, "already covered", the gap between flashes
  evergreen        the topic queues, advancing, cooling down after a bad research pass
  cli              every command, exit codes, python -m earlobe, the commands the docs and workflows use
  hygiene          no model ids or secrets in what this module owns
"""
import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import pytest
import yaml

from earlobe import cli, config, fixtures, pipeline
from earlobe.desk import breaking as desk_breaking
from earlobe.desk import cluster as desk_cluster
from earlobe.llm import LLM
from earlobe.monitor import CORRECTION, EPISODE, SCRIPT, killswitch
from earlobe.pipeline import COVERAGE, GATE, RUN_EVENT, TRUST, PipelineError
from earlobe.publish import public_dir, trustlog
from earlobe.schemas import RISK_FLAGS, AgentRun, Episode, Signal, make_id, validate
from earlobe.store import AGENT_RUN, Store

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT.parent / ".github" / "workflows"
NOW = datetime(2026, 10, 12, 12, 0, tzinfo=timezone.utc)
needs_ffmpeg = pytest.mark.skipif(shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
                                  reason="ffmpeg/ffprobe not installed")
LIVE_REQUIRED = ["EARLOBE_MODEL_OPUS", "EARLOBE_MODEL_SONNET", "ANTHROPIC_API_KEY", "ELEVENLABS_API_KEY",
                 "ELEVENLABS_TTS_MODEL", "VOICE_MARA", "VOICE_THEO", "VOICE_AVA"]
LIVE_ENV = ["EARLOBE_MODEL_OPUS", "EARLOBE_MODEL_SONNET", "EARLOBE_MODEL_HAIKU", "ANTHROPIC_API_KEY",
            "ANTHROPIC_AUTH_TOKEN", "ELEVENLABS_API_KEY", "ELEVENLABS_TTS_MODEL", "VOICE_MARA", "VOICE_THEO",
            "VOICE_LENA", "VOICE_MARCUS", "VOICE_AVA", "VOICE_JUNE", "TRANSISTOR_API_KEY",
            "TRANSISTOR_SHOW_ID", "EARLOBE_HOST", "EARLOBE_PUBLIC_BASE_URL"]


# ================================================================== helpers
@pytest.fixture
def data(tmp_path, monkeypatch):
    """A temp data dir, and an environment with no kill switch, no keys and no public base URL."""
    monkeypatch.setattr(config, "DATA_DIR", tmp_path / "data")
    for name in [*LIVE_ENV, killswitch.ENV_VAR]:
        monkeypatch.delenv(name, raising=False)
    return tmp_path / "data"


@pytest.fixture
def conf(tmp_path, monkeypatch, data):
    """A temp copy of config/ that tests may edit."""
    target = tmp_path / "config"
    shutil.copytree(config.CONFIG_DIR, target)
    monkeypatch.setattr(config, "CONFIG_DIR", target)
    return target


def stored(kind, show_id=None):
    with Store() as store:
        return store.list(kind, show_id=show_id)


def feed_items(show_id):
    return ET.parse(public_dir("feeds") / f"{show_id}.xml").getroot().findall(".//item")


class Contradicting(LLM):
    """Dry-run LLM whose blind verifier finds evidence against every claim."""

    def __init__(self):
        super().__init__(dry_run=True)

    def research(self, agent_id, tier, system, user, kind, max_searches=10, *, effort="medium", ctx=None):
        report = super().research(agent_id, tier, system, user, kind, max_searches, effort=effort, ctx=ctx)
        if agent_id == "verifier":
            for f in report["findings"]:
                f.update(status="contradicted", note="A filing says the opposite.")
        return report


class ThinSourcing(LLM):
    """Dry-run LLM whose verifier finds only two independent sources: not enough for the breaking lane."""

    def __init__(self):
        super().__init__(dry_run=True)

    def research(self, agent_id, tier, system, user, kind, max_searches=10, *, effort="medium", ctx=None):
        report = super().research(agent_id, tier, system, user, kind, max_searches, effort=effort, ctx=ctx)
        if agent_id == "verifier":
            for f in report["findings"]:
                f["evidence"] = f["evidence"][:2]
                f.update(independent_count=2, has_official=False)
        return report


class NothingFound(LLM):
    """Dry-run LLM whose archive research comes back with no usable sources."""

    def __init__(self):
        super().__init__(dry_run=True)

    def research(self, agent_id, tier, system, user, kind, max_searches=10, *, effort="medium", ctx=None):
        report = super().research(agent_id, tier, system, user, kind, max_searches, effort=effort, ctx=ctx)
        if kind == "ArchivePack":
            report.update(sources=[], uncertain=["No case met every rule."])
        return report


def earthquake(now, minutes=(20, 15, 10, 6, 3)):
    """A second breaking cluster (fictional), published inside the last half hour."""
    outlets = ["Associated Press", "Reuters", "BBC News", "The Guardian", "Al Jazeera"]
    signals = []
    for outlet, ago in zip(outlets, minutes):
        title = f"[SAMPLE] Earthquake rattles Port Verity region, officials assess damage, {outlet} reports"
        url = f"https://sample.invalid/national/{outlet.lower().replace(' ', '-')}/port-verity-earthquake"
        signals.append(Signal(
            id=make_id("sig", url), sensor="beat-national", market="national", beat="disaster", title=title,
            url=url, outlet=outlet, published_at=(now - timedelta(minutes=ago)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            summary="A magnitude 7 earthquake struck near Port Verity; emergency officials are assessing "
                    "damage. [Sample data]", kind="article", tier=2, raw={"sample": True}))
    return signals


# ================================================================== scheduled shows
@pytest.mark.parametrize("show_id", ["columbia-daily", "la-daily"])
def test_dry_run_publishes_a_full_episode(data, show_id):
    llm = LLM(dry_run=True)
    ep = pipeline.run_show(show_id, dry_run=True, llm=llm)

    assert isinstance(ep, Episode) and ep.status == "published" and ep.show_id == show_id
    assert ep.gate["decision"] == "PUBLISH" and ep.gate["script_id"] == ep.script_id
    assert ep.title and ep.description and ep.guid == ep.id and ep.source_count > 0
    assert ep.audio_url.startswith("https://earlobe.invalid/audio/")        # a dry run never gets a working URL
    assert "synthetic" in ep.disclosure_text

    notes = (public_dir("notes") / f"{ep.id}.md").read_text(encoding="utf-8")
    assert notes == ep.show_notes_md
    assert "## Sources" in notes and "https://sample.invalid/" in notes and "## How we checked this" in notes
    assert "**AI disclosure:**" in notes

    root = ET.parse(public_dir("feeds") / f"{show_id}.xml").getroot()
    items = root.findall(".//item")
    assert root.tag == "rss" and len(items) == 1
    assert items[0].findtext("guid") == ep.id
    assert items[0].find("enclosure").get("url") == ep.audio_url
    assert "synthetic" in items[0].findtext("description")

    lines = trustlog.read(show_id)
    assert len(lines) == 1
    assert lines[0]["decision"] == "PUBLISH" and lines[0]["episode_id"] == ep.id
    assert lines[0]["script_id"] == ep.script_id and lines[0]["source_count"] == ep.source_count

    assert pathlib.Path(ep.audio_path).stat().st_size > 0
    assert (public_dir("audio") / f"{ep.id}.mp3").stat().st_size > 0
    transcript = (public_dir("transcripts") / f"{ep.id}.txt").read_text(encoding="utf-8")
    assert "synthetic" in transcript and ep.show_id not in transcript.splitlines()[0]     # head: title, show, date
    assert items[0].find("{https://podcastindex.org/namespace/1.0}transcript") is not None


@needs_ffmpeg
def test_dry_run_audio_is_a_real_mp3_of_the_reported_length(data):
    ep = pipeline.run_show("columbia-daily", dry_run=True)
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_name",
                            "-of", "json", ep.audio_path], capture_output=True, text=True, check=True)
    info = json.loads(probe.stdout)
    assert info["streams"][0]["codec_name"] == "mp3"
    assert abs(float(info["format"]["duration"]) - ep.duration_sec) <= 2
    assert ep.duration_sec > 30


def test_everything_is_stored_and_every_agent_run_is_logged_to_the_show(data):
    llm = LLM(dry_run=True)
    ep = pipeline.run_show("columbia-daily", dry_run=True, llm=llm)
    with Store() as store:
        assert store.get(EPISODE, ep.id)["status"] == "published"
        script = store.get(SCRIPT, ep.script_id)
        assert script["show_id"] == "columbia-daily" and script["claims"] and script["sources"]
        assert store.get(GATE, ep.script_id)["decision"] == "PUBLISH"
        assert store.get(TRUST, ep.script_id)["history"][-1]["decision"] == "PUBLISH"
        assert store.get(pipeline.COPY, ep.id)["title"] == ep.title
        assert store.list(pipeline.STORY) and store.list(pipeline.SIGNAL)
        coverage = store.list(COVERAGE, show_id="columbia-daily")
        assert coverage and {c["status"] for c in coverage} == {"published"}

        runs = store.list(AGENT_RUN, show_id="columbia-daily")
        assert len(runs) == len(llm.runs) > 5
        assert {r["run_id"] for r in runs} == {r.run_id for r in llm.runs}
        assert {"producer", "verifier", "fact-checker", "bias-checker", "legal-screener", "copywriter",
                "story-triage"} <= {r["agent_id"] for r in runs}
        assert store.list(AGENT_RUN, show_id="la-daily") == []


def test_a_rerun_overwrites_instead_of_duplicating(data):
    first = pipeline.run_show("columbia-daily", dry_run=True)
    second = pipeline.run_show("columbia-daily", dry_run=True)
    assert first.id == second.id
    assert len(feed_items("columbia-daily")) == 1
    assert len(stored(EPISODE, "columbia-daily")) == 1
    assert len(trustlog.read("columbia-daily")) == 1          # identical records are not appended twice


def test_the_episode_is_dated_in_the_markets_time_zone(data):
    late = datetime(2026, 10, 13, 2, 30, tzinfo=timezone.utc)           # still Oct 12 in Los Angeles
    ep = pipeline.run_show("la-daily", dry_run=True, now=late)
    assert stored(SCRIPT, "la-daily")[0]["episode_date"] == "2026-10-12"
    assert ep.published_at == "2026-10-13T02:30:00Z"


def test_a_pinned_clock_gives_reproducible_sample_data(data):
    a = pipeline.run_show("la-daily", dry_run=True, now=NOW)
    b = pipeline.run_show("la-daily", dry_run=True, now=NOW)
    assert a.id == b.id and a.script_id == b.script_id


# ================================================================== gate outcomes
def test_a_kill_publishes_nothing_but_leaves_the_record(data):
    llm = Contradicting()
    assert pipeline.run_show("columbia-daily", dry_run=True, llm=llm) is None

    with Store() as store:
        assert store.list(EPISODE) == []
        decision = store.list(GATE)[0]
        assert decision["decision"] == "KILL" and decision["revision"] == 2
        assert "V1" in {r["rule_id"] for r in decision["reasons"]}
        report = store.list(TRUST)[0]
        assert report["rewrites"] == 2 and len(report["passes"]) == 3
        assert {c["status"] for c in store.list(COVERAGE)} == {"killed"}
        assert len(store.list(AGENT_RUN, show_id="columbia-daily")) == len(llm.runs)
        assert "copywriter" not in {r.agent_id for r in llm.runs}          # no copy, no voices, no host
    assert not (public_dir("feeds") / "columbia-daily.xml").exists()
    assert list(public_dir("audio").iterdir()) == []
    line = trustlog.read("columbia-daily")[0]
    assert line["decision"] == "KILL" and line["episode_id"] == "" and line["history"]


def test_thin_sourcing_on_the_breaking_lane_holds_and_counts_the_holds(data):
    t0 = NOW
    assert pipeline.run_breaking(True, now=t0, llm=ThinSourcing()) == []
    with Store() as store:
        record = store.list(COVERAGE, show_id="breaking-desk")[0]
        assert record["status"] == "hold" and record["holds_used"] == 1
        assert record["retry_after"] == "2026-10-12T12:15:00Z"
        assert store.list(EPISODE) == []
    assert trustlog.read("breaking-desk")[0]["decision"] == "HOLD"

    early = ThinSourcing()                                      # inside the wait: nothing is even tried
    assert pipeline.run_breaking(True, now=t0 + timedelta(minutes=5), llm=early) == []
    assert early.runs == []

    again = ThinSourcing()                                      # after the wait: checked again, one hold used
    assert pipeline.run_breaking(True, now=t0 + timedelta(minutes=16), llm=again) == []
    with Store() as store:
        assert store.list(TRUST)[-1]["holds_used"] == 1
        assert store.list(COVERAGE, show_id="breaking-desk")[0]["holds_used"] == 2

    done = pipeline.run_breaking(True, now=t0 + timedelta(minutes=33))    # corroborated at last
    assert len(done) == 1 and done[0].gate["lane_policy"] == "breaking"
    with Store() as store:
        assert store.list(COVERAGE, show_id="breaking-desk")[0]["status"] == "published"


# ================================================================== guards
def test_the_kill_switch_stops_a_live_run_before_anything_else(data, monkeypatch):
    monkeypatch.setenv(killswitch.ENV_VAR, "columbia-daily")
    assert pipeline.run_show("columbia-daily") is None                 # no keys needed: it never gets that far
    event = stored(RUN_EVENT, "columbia-daily")[0]
    assert event["rule"] == "KILLSWITCH" and "kill switch" in event["reason"]
    line = trustlog.read("columbia-daily")[0]
    assert line["event"] == "skipped" and line["decision"] == "SKIPPED" and line["rules"] == ["KILLSWITCH"]
    assert stored(EPISODE) == [] and stored(AGENT_RUN) == []

    monkeypatch.setenv(killswitch.ENV_VAR, "all")
    assert pipeline.run_breaking() == []
    assert pipeline.run_evergreen("history-of-hollywood") is None


def test_dry_runs_ignore_the_kill_switch(data, monkeypatch):
    monkeypatch.setenv(killswitch.ENV_VAR, "all")
    assert pipeline.run_show("columbia-daily", dry_run=True).status == "published"


def test_a_live_run_over_budget_stops_before_spending(data):
    with Store() as store:
        store.log_run(AgentRun(agent_id="verifier", run_id="run_big", model_tier="opus",
                               started_at="2026-10-12T09:00:00Z", usd_estimate=99.0), "columbia-daily")
    assert pipeline.run_show("columbia-daily", now=NOW) is None
    event = stored(RUN_EVENT, "columbia-daily")[0]
    assert event["rule"] == "BUDGET" and "$99.00" in event["reason"]
    assert stored(EPISODE) == []
    assert trustlog.read("columbia-daily") == []          # a budget skip is internal, not a trust matter


def test_a_live_run_names_the_settings_it_is_missing(data):
    with pytest.raises(PipelineError) as err:
        pipeline.run_show("columbia-daily")
    text = str(err.value)
    for name in ("EARLOBE_MODEL_OPUS", "EARLOBE_MODEL_SONNET", "ANTHROPIC_API_KEY", "ELEVENLABS_API_KEY",
                 "ELEVENLABS_TTS_MODEL", "VOICE_MARA", "VOICE_THEO", "VOICE_AVA"):
        assert name in text
    assert "VOICE_JUNE" not in text                       # only the voices this show uses
    assert stored(AGENT_RUN) == []                        # nothing was spent finding out


def test_settings_that_are_present_are_not_reported(data, monkeypatch):
    for name in LIVE_REQUIRED:
        monkeypatch.setenv(name, "x")
    missing = pipeline.missing_settings(config.load_shows()["columbia-daily"])
    assert [m for m in missing if m != "ffmpeg (not on PATH)"] == []


def test_unknown_and_disabled_shows(data):
    with pytest.raises(PipelineError, match="unknown show 'nope'.*columbia-daily"):
        pipeline.run_show("nope", dry_run=True)
    with pytest.raises(PipelineError, match="disabled"):
        pipeline.run_show("nyc-daily")
    assert pipeline.run_show("nyc-daily", dry_run=True).show_id == "nyc-daily"      # dry runs may try a wave-1 show


def test_a_dry_run_refuses_a_live_llm(data):
    with pytest.raises(PipelineError, match="dry-run LLM"):
        pipeline.run_show("columbia-daily", dry_run=True, llm=LLM(dry_run=False))


# ================================================================== breaking
def test_breaking_scan_cuts_one_flash_and_remembers_it(data):
    episodes = pipeline.run_breaking(dry_run=True)
    assert len(episodes) == 1
    ep = episodes[0]
    assert ep.show_id == "breaking-desk" and ep.status == "published"
    assert ep.gate["decision"] == "PUBLISH" and ep.gate["lane_policy"] == "breaking"
    assert len(feed_items("breaking-desk")) == 1

    assert pipeline.run_breaking(dry_run=True) == []           # the same story is not covered twice
    assert len(feed_items("breaking-desk")) == 1


def test_flashes_keep_the_shows_gap_apart(data, monkeypatch):
    sample = lambda ctx, market, beats, hours: [*fixtures.sample_signals("national", now=NOW),
                                                *earthquake(NOW)]
    monkeypatch.setattr(pipeline, "_sense", sample)
    signals = sample(None, "national", [], 3)
    flagged = desk_breaking.detect(desk_cluster.cluster(signals, config.load_owners()), signals=signals,
                                   owners=config.load_owners(), now=NOW)
    assert len(flagged) == 2                                    # the hurricane and the earthquake

    first = pipeline.run_breaking(True, now=NOW)
    assert len(first) == 1 and "Hurricane" in stored(pipeline.STORY)[0]["headline"]
    assert [c["status"] for c in stored(COVERAGE, "breaking-desk")] == ["published"]

    assert pipeline.run_breaking(True, now=NOW + timedelta(minutes=10)) == []          # gap is 30 minutes
    second = pipeline.run_breaking(True, now=NOW + timedelta(minutes=31))
    assert len(second) == 1 and second[0].id != first[0].id
    assert len(feed_items("breaking-desk")) == 2
    assert pipeline.run_breaking(True, now=NOW + timedelta(minutes=70)) == []          # both are covered now


def test_one_failed_flash_does_not_stop_the_scan(data, monkeypatch):
    monkeypatch.setattr(pipeline, "_sense", lambda ctx, m, b, h: [*fixtures.sample_signals("national", now=NOW),
                                                                  *earthquake(NOW)])
    calls = []
    real = pipeline._produce

    def flaky(ctx, show_id, show_cfg, stories, signals, **kw):
        calls.append(stories[0].id)
        if len(calls) == 1:
            raise RuntimeError("model unavailable")
        return real(ctx, show_id, show_cfg, stories, signals, **kw)

    monkeypatch.setattr(pipeline, "_produce", flaky)
    with pytest.raises(PipelineError, match="1 breaking flash.*RuntimeError: model unavailable"):
        pipeline.run_breaking(True, now=NOW)
    assert len(calls) == 2                                      # the second story was still tried


# ================================================================== evergreen
@pytest.mark.parametrize("show_id,lane,topics", [("history-of-hollywood", "archive", 15),
                                                 ("cold-case-files", "strict", 10)])
def test_the_topic_queues_are_well_formed(show_id, lane, topics):
    queue = config.load_evergreen(show_id)
    assert queue["agent"] and queue["tier"] in config.TIERS and queue["max_searches"] > 0
    assert queue["brief"].strip() and len(queue["topics"]) == topics
    ids = [t["id"] for t in queue["topics"]]
    assert len(set(ids)) == len(ids)
    assert all(t["title"].strip() and t["angle"].strip() for t in queue["topics"])
    assert set(queue.get("risk_flags", [])) <= set(RISK_FLAGS)
    assert config.load_shows()[show_id]["lane"] == lane


def test_cold_case_topics_name_no_one():
    for topic in config.load_evergreen("cold-case-files")["topics"]:
        for text in (topic["title"], topic["angle"]):
            words = re.findall(r"[A-Za-z']+", text)
            assert not [w for w in words[1:] if w[0].isupper()], topic        # no proper nouns after the first word


def test_evergreen_publishes_the_first_topic_then_moves_down_the_queue(data):
    first = pipeline.run_evergreen("history-of-hollywood", dry_run=True)
    assert first.status == "published" and first.gate["lane_policy"] == "archive"
    assert first.source_count == 4 and first.gate["decision"] == "PUBLISH"
    second = pipeline.run_evergreen("history-of-hollywood", dry_run=True)
    assert second.id != first.id
    topics = config.load_evergreen("history-of-hollywood")["topics"]
    with Store() as store:
        packs = {p["subject"] for p in store.list(pipeline.ARCHIVE_PACK)}
        assert len(packs) == 2 and all(topics[i]["title"][:40] in " ".join(packs) for i in (0, 1))
        covered = {c["story_id"]: c["status"] for c in store.list(COVERAGE, "history-of-hollywood")}
        assert covered == {pipeline._topic_story_id("history-of-hollywood", topics[0]["id"]): "published",
                           pipeline._topic_story_id("history-of-hollywood", topics[1]["id"]): "published"}
        agents = {r["agent_id"] for r in store.list(AGENT_RUN, "history-of-hollywood")}
        assert "archive-miner" in agents
    assert len(feed_items("history-of-hollywood")) == 2
    assert [l["decision"] for l in trustlog.read("history-of-hollywood")] == ["PUBLISH", "PUBLISH"]


def test_cold_case_runs_in_the_strict_lane_with_an_official_source(data):
    ep = pipeline.run_evergreen("cold-case-files", dry_run=True)
    assert ep.gate["lane_policy"] == "strict" and ep.gate["decision"] == "PUBLISH"
    script = stored(SCRIPT, "cold-case-files")[0]
    assert script["lane_policy"] == "strict"
    assert any(s["tier"] == 1 for s in script["sources"])
    assert "presumed innocent" in " ".join(l["text"] for l in script["lines"])      # the strict-lane disclosure line
    assert {r["agent_id"] for r in stored(AGENT_RUN, "cold-case-files")} >= {"cold-case-archivist"}


def test_run_show_hands_an_evergreen_show_to_its_queue(data):
    ep = pipeline.run_show("history-of-hollywood", dry_run=True)
    assert ep.show_id == "history-of-hollywood"
    assert stored(pipeline.ARCHIVE_PACK, "history-of-hollywood")


def test_research_that_finds_nothing_costs_one_call_and_cools_the_topic_down(data):
    thin = NothingFound()
    assert pipeline.run_evergreen("cold-case-files", dry_run=True, now=NOW, llm=thin) is None
    assert [r.agent_id for r in thin.runs] == ["cold-case-archivist"]           # no script, no checks
    topics = config.load_evergreen("cold-case-files")["topics"]
    assert stored(COVERAGE, "cold-case-files")[0]["status"] == "killed"
    assert stored(RUN_EVENT, "cold-case-files")[0]["rule"] == "RESEARCH"

    nxt = pipeline.run_evergreen("cold-case-files", dry_run=True, now=NOW + timedelta(hours=1))
    assert nxt.status == "published"                            # the next topic took the slot
    with Store() as store:
        assert {c["story_id"] for c in store.list(COVERAGE, "cold-case-files")} == {
            pipeline._topic_story_id("cold-case-files", topics[0]["id"]),
            pipeline._topic_story_id("cold-case-files", topics[1]["id"])}

    week_later = pipeline.run_evergreen("cold-case-files", dry_run=True, now=NOW + timedelta(days=8))
    assert week_later.status == "published"                     # the cooldown ended: topic 1 may be tried again
    assert pipeline._topic_story_id("cold-case-files", topics[0]["id"]) in [
        c["story_id"] for c in stored(COVERAGE, "cold-case-files") if c["status"] == "published"]


def test_an_exhausted_queue_ends_quietly(data, conf):
    queue = yaml.safe_load((conf / "evergreen" / "history-of-hollywood.yaml").read_text(encoding="utf-8"))
    queue["topics"] = queue["topics"][:1]
    (conf / "evergreen" / "history-of-hollywood.yaml").write_text(yaml.safe_dump(queue), encoding="utf-8")
    assert pipeline.run_evergreen("history-of-hollywood", dry_run=True) is not None
    assert pipeline.run_evergreen("history-of-hollywood", dry_run=True) is None
    assert stored(RUN_EVENT, "history-of-hollywood")[0]["rule"] == "QUEUE_EMPTY"


def test_an_evergreen_show_without_a_queue_is_a_configuration_error(data, conf):
    (conf / "evergreen" / "cold-case-files.yaml").unlink()
    with pytest.raises(PipelineError, match="no evergreen topic queue"):
        pipeline.run_evergreen("cold-case-files", dry_run=True)


def test_archive_sources_are_cleaned_before_the_writer_sees_them(data):
    with pipeline._session(True, NOW, None, None) as ctx:
        cfg = config.load_shows()["history-of-hollywood"]
        pack = fixtures.fake("ArchivePack", show_id="history-of-hollywood", show_cfg=cfg,
                             topic={"id": "t", "title": "A topic"})
        good = pack["sources"][0]
        original = [s["url"] for s in pack["sources"]]
        pack["sources"] += [dict(good), {**good, "url": "not a url"}, {**good, "url": "https://x.invalid/a", "tier": 4},
                            {**good, "url": "https://x.invalid/b", "kind": "mystery", "tier": 2},
                            {**good, "url": "https://x.invalid/c", "tier": "high"},
                            {**good, "url": "https://x.invalid/d", "tier": 0}]
        sources = pipeline._archive_sources(pack, cfg, ctx)
    assert [s.url for s in sources] == [*original, "https://x.invalid/b"]       # no repeat, bad url or tier 4
    assert sources[-1].kind == "other" and sources[-1].tier == 2                 # an unknown kind is neutralized
    assert all(s.id == make_id("src", s.url) and s.retrieved_at == "2026-10-12T12:00:00Z" for s in sources)
    assert all(1 <= s.tier <= 3 and s.market == "los-angeles" for s in sources)
    assert pipeline._archive_viable(sources, "archive", config.load_owners())
    assert not pipeline._archive_viable([s for s in sources if s.tier > 1][:1], "archive", config.load_owners())
    assert not pipeline._archive_viable([s for s in sources if s.tier > 1], "strict", config.load_owners())


# ================================================================== reports over the store
def test_cost_rows_sum_by_show_and_agent(data):
    with Store() as store:
        for i, (show, agent, usd, tokens, ok) in enumerate([
                ("columbia-daily", "producer", 0.50, 1000, True), ("columbia-daily", "producer", 0.25, 500, False),
                ("columbia-daily", "verifier", 1.00, 2000, True), ("la-daily", "producer", 0.75, 100, True)]):
            store.log_run(AgentRun(agent_id=agent, run_id=f"run_{i}", model_tier="opus",
                                   started_at=f"2026-10-1{i}T09:00:00Z", input_tokens=tokens, output_tokens=tokens // 10,
                                   web_searches=i, usd_estimate=usd, ok=ok), show)
        rows = pipeline.cost_rows(store)
        recent = pipeline.cost_rows(store, since="2026-10-12T00:00:00Z")
    by = {(r["show_id"], r["agent_id"]): r for r in rows}
    assert by[("columbia-daily", "producer")] == {
        "show_id": "columbia-daily", "agent_id": "producer", "runs": 2, "failed": 1, "input_tokens": 1500,
        "output_tokens": 150, "web_searches": 1, "usd": 0.75}
    assert by[("columbia-daily", "verifier")]["usd"] == 1.0 and by[("la-daily", "producer")]["usd"] == 0.75
    assert round(sum(r["usd"] for r in rows), 6) == 2.5
    assert {(r["show_id"], r["agent_id"]) for r in recent} == {("columbia-daily", "verifier"), ("la-daily", "producer")}


def test_rebuild_feeds_recreates_a_lost_feed(data):
    ep = pipeline.run_show("columbia-daily", dry_run=True)
    (public_dir("feeds") / "columbia-daily.xml").unlink()
    with Store() as store:
        built = pipeline.rebuild_feeds(store)
    assert [(b["show_id"], b["items"]) for b in built] == [("columbia-daily", 1)]
    assert feed_items("columbia-daily")[0].findtext("guid") == ep.id


# ================================================================== cli
def run_cli(capsys, *argv):
    code = cli.main([str(a) for a in argv])
    out, err = capsys.readouterr()
    return code, out, err


def test_cli_list_shows(data, capsys):
    code, out, _ = run_cli(capsys, "list-shows")
    assert code == 0
    for sid in config.load_shows():
        assert sid in out
    assert "cold-case-files" in out and "evergreen_story" in out and "no" in out        # nyc-daily is disabled
    code, out, _ = run_cli(capsys, "list-shows", "--json")
    assert code == 0 and [s["id"] for s in json.loads(out)] == list(config.load_shows())


def test_cli_run_dry_run_prints_the_result_and_the_files(data, capsys):
    code, out, err = run_cli(capsys, "run", "--show", "columbia-daily", "--dry-run")
    assert code == 0
    assert out.startswith("published  columbia-daily  ep_")
    for label in ("title", "gate", "audio", "notes", "feed", "trust log", "spend"):
        assert label in out
    assert "gate: PUBLISH" in err and "writing the script" in err         # progress goes to stderr
    assert (data / "public" / "feeds" / "columbia-daily.xml").is_file()
    assert (data / "earlobe.db").is_file()


def test_cli_breaking_scan_evergreen_and_the_evergreen_route_of_run(data, capsys):
    code, out, _ = run_cli(capsys, "breaking-scan", "--dry-run")
    assert code == 0 and "1 flash(es) published" in out
    code, out, _ = run_cli(capsys, "breaking-scan", "--dry-run")
    assert code == 0 and "0 flash(es) published" in out
    code, out, _ = run_cli(capsys, "evergreen", "--show", "history-of-hollywood", "--dry-run")
    assert code == 0 and "published  history-of-hollywood" in out
    code, out, _ = run_cli(capsys, "run", "--show", "cold-case-files", "--dry-run")
    assert code == 0 and "published  cold-case-files" in out


def test_cli_says_so_when_nothing_was_published(data, capsys, monkeypatch):
    monkeypatch.setenv(killswitch.ENV_VAR, "columbia-daily")
    code, out, err = run_cli(capsys, "run", "--show", "columbia-daily")
    assert code == 0 and "no episode published for columbia-daily" in out
    assert "kill switch is on" in err


def test_cli_errors_have_distinct_exit_codes(data, capsys):
    code, _, err = run_cli(capsys, "run", "--show", "nope", "--dry-run")
    assert code == 2 and "unknown show 'nope'" in err
    code, _, err = run_cli(capsys, "run", "--show", "columbia-daily")           # live, nothing configured
    assert code == 2 and "EARLOBE_MODEL_OPUS" in err
    with pytest.raises(SystemExit) as usage:
        cli.main(["run", "--dry-run"])                                          # --show is required
    assert usage.value.code == 2
    with pytest.raises(SystemExit):
        cli.main([])


def test_cli_a_failing_run_exits_1_and_publishes_nothing(data, capsys, monkeypatch):
    def broken(*a, **k):
        raise RuntimeError("the checkers are down")
    monkeypatch.setattr(pipeline, "run_show", broken)
    code, out, err = run_cli(capsys, "run", "--show", "columbia-daily", "--dry-run")
    assert code == 1 and out == "" and "RuntimeError: the checkers are down" in err


def test_cli_data_dir_moves_everything_and_is_restored(tmp_path, data, capsys):
    other = tmp_path / "elsewhere"
    code, _, _ = run_cli(capsys, "run", "--show", "la-daily", "--dry-run", "--data-dir", other)
    assert code == 0 and (other / "earlobe.db").is_file() and (other / "public" / "feeds" / "la-daily.xml").is_file()
    assert not data.exists() and config.DATA_DIR == data
    code, _, _ = run_cli(capsys, "--data-dir", other, "feeds")                  # before the command works too
    assert code == 0


def test_cli_feeds_and_cost_report_after_a_run(data, capsys):
    run_cli(capsys, "run", "--show", "columbia-daily", "--dry-run")
    code, out, _ = run_cli(capsys, "feeds")
    assert code == 0 and "columbia-daily  1 item(s)" in out
    code, out, _ = run_cli(capsys, "cost-report")
    assert code == 0 and "producer" in out and "verifier" in out and "ALL SHOWS" in out
    code, out, _ = run_cli(capsys, "cost-report", "--json", "--days", 1)
    report = json.loads(out)
    assert code == 0 and set(report["by_show"]) == {"columbia-daily"} and report["total_usd"] == 0.0
    assert sum(r["runs"] for r in report["rows"]) > 5


def test_cli_cost_report_and_feeds_on_an_empty_store(data, capsys):
    code, out, _ = run_cli(capsys, "cost-report")
    assert code == 0 and "no agent runs logged yet" in out
    code, out, _ = run_cli(capsys, "feeds")
    assert code == 0 and "nothing to build" in out


def test_cli_cost_report_adds_up_known_runs(data, capsys):
    with Store() as store:
        for i, (show, usd) in enumerate([("columbia-daily", 0.4), ("columbia-daily", 0.6), ("la-daily", 1.25)]):
            store.log_run(AgentRun(agent_id="producer", run_id=f"run_{i}", model_tier="opus",
                                   started_at="2026-10-12T09:00:00Z", usd_estimate=usd), show)
    _, out, _ = run_cli(capsys, "cost-report", "--json")
    assert json.loads(out)["by_show"] == {"columbia-daily": 1.0, "la-daily": 1.25}
    _, out, _ = run_cli(capsys, "cost-report")
    assert "columbia-daily total" in out and "2.2500" in out.splitlines()[-1]


def test_cli_recheck_dry_run_and_apply(data, capsys, monkeypatch):
    ep = pipeline.run_show("columbia-daily", dry_run=True)
    code, out, _ = run_cli(capsys, "recheck", "--days", 7, "--dry-run")
    assert code == 0 and "0 correction(s) opened" in out

    monkeypatch.setattr(cli, "LLM", lambda dry_run: Contradicting())             # a verifier that now disagrees
    code, out, _ = run_cli(capsys, "recheck", "--days", 7, "--dry-run")
    assert code == 0 and f"episode {ep.id}" in out and "run again with --apply" in out
    assert stored(CORRECTION) and {c["status"] for c in stored(CORRECTION)} == {"open"}
    assert stored(EPISODE)[0]["status"] == "published"

    code, out, _ = run_cli(capsys, "recheck", "--days", 7, "--dry-run", "--apply")
    assert code == 0 and f"applied  {ep.id} is now corrected" in out
    assert stored(EPISODE)[0]["status"] == "corrected"
    assert "## Corrections" in stored(EPISODE)[0]["show_notes_md"]
    assert trustlog.read("columbia-daily")[-1]["event"] == "correction"


def test_python_dash_m_earlobe_runs(tmp_path):
    env = {k: v for k, v in os.environ.items() if k not in [*LIVE_ENV, killswitch.ENV_VAR]}
    env["EARLOBE_DATA_DIR"] = str(tmp_path / "d")
    listed = subprocess.run([sys.executable, "-m", "earlobe", "list-shows"], cwd=ROOT, env=env,
                            capture_output=True, text=True, timeout=60, check=False)
    assert listed.returncode == 0 and "columbia-daily" in listed.stdout
    ran = subprocess.run([sys.executable, "-m", "earlobe", "run", "--show", "columbia-daily", "--dry-run"],
                         cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False)
    assert ran.returncode == 0, ran.stderr
    assert "published  columbia-daily" in ran.stdout and (tmp_path / "d" / "public" / "feeds").is_dir()
    bad = subprocess.run([sys.executable, "-m", "earlobe", "run", "--show", "nope", "--dry-run"], cwd=ROOT,
                         env=env, capture_output=True, text=True, timeout=60, check=False)
    assert bad.returncode == 2 and "unknown show" in bad.stderr


def _commands(text: str) -> list[list[str]]:
    """Every `python -m earlobe ...` line in a text, as an argv list ($show and ${...} become a real show id)."""
    found = []
    for line in text.splitlines():
        if "python -m earlobe" in line and not line.lstrip().startswith("#"):
            tail = line.split("python -m earlobe", 1)[1].split("#")[0].split("||")[0].replace('"$show"', "columbia-daily")
            found.append(shlex.split(tail))
    return found


def test_every_documented_command_parses():
    parser = cli.build_parser()
    commands = _commands((ROOT / "earlobe" / "README.md").read_text(encoding="utf-8"))
    commands += _commands((ROOT / "README.md").read_text(encoding="utf-8"))
    if WORKFLOWS.is_dir():
        for name in ("earlobe-daily-briefs", "earlobe-evergreen", "earlobe-breaking"):
            commands += _commands((WORKFLOWS / f"{name}.yml").read_text(encoding="utf-8"))
    assert len(commands) >= 6
    for argv in commands:
        parser.parse_args(argv)          # a SystemExit here means the docs or a workflow name a command that does not exist


# ================================================================== hygiene
MODEL_ID = re.compile("clau" + r"de-(?:opus|sonnet|haiku|[0-9])|(?:opus|sonnet|haiku)-[0-9]", re.IGNORECASE)
MY_FILES = [ROOT / "earlobe" / "pipeline.py", ROOT / "earlobe" / "cli.py", ROOT / "earlobe" / "__main__.py",
            ROOT / "config" / "evergreen" / "history-of-hollywood.yaml",
            ROOT / "config" / "evergreen" / "cold-case-files.yaml", pathlib.Path(__file__)]


@pytest.mark.parametrize("path", MY_FILES, ids=lambda p: p.name)
def test_no_model_ids_or_secrets(path):
    text = path.read_text(encoding="utf-8")
    assert not MODEL_ID.search(text)
    assert not re.search(r"sk-[A-Za-z0-9_-]{16,}|api[_-]?key\s*=\s*[\"'][^\"']+[\"']", text)


def test_pipeline_output_validates_against_the_contracts(data):
    pack = fixtures.fake("ArchivePack", show_id="cold-case-files", topic={"id": "x", "title": "y"})
    assert validate("ArchivePack", pack) == []
    ep = pipeline.run_show("la-daily", dry_run=True)
    assert validate("Copy", stored(pipeline.COPY, "la-daily")[0]) == []
    assert Episode.from_dict(stored(EPISODE, "la-daily")[0]) == ep
