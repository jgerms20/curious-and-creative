"""Monitoring and operations: kill switch, budgets, corrections, re-checks, CI and SQL files.

No keys, no network: LLM calls use the dry-run LLM, config is a temp copy, and every store and
data folder is a temp dir.

Sections
  helpers        temp config / data / store, a published episode with its script, a verifier that disagrees
  kill switch    env and file, OR semantics, fail-safe on a broken file
  budget         caps, defaults when the file is missing, network cap and the breaking lane
  corrections    open, apply (status, notes, feed, trust log), retract, idempotence
  re-check       dry run, contradicted claims, window, statuses, budget, cost logging
  workflows      the GitHub Actions files, including the cron <-> shows.yaml link
  sql            the Supabase migration
  hygiene        no model ids or secrets in what this module owns
"""
import contextlib
import io
import itertools
import pathlib
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone

import pytest
import yaml

from earlobe import config, fixtures
from earlobe.llm import LLM
from earlobe.monitor import CORRECTION, EPISODE, RECHECK_REPORT, SCRIPT, budget, corrections, killswitch
from earlobe.monitor.recheck import recheck
from earlobe.publish import notes, public_dir, trustlog
from earlobe.schemas import AgentRun, Episode, GateDecision, Script, make_id
from earlobe.store import Store
from earlobe.trust.gate import NEEDS_CORROBORATION

ROOT = pathlib.Path(__file__).resolve().parent.parent
WORKFLOWS = ROOT.parent / ".github" / "workflows"
SQL = ROOT / "supabase" / "migrations" / "0001_earlobe_core.sql"
SHOW = "columbia-daily"
NOW = datetime(2026, 10, 12, 12, 0, tzinfo=timezone.utc)
DAY = "2026-10-12"


# ================================================================== helpers
@pytest.fixture
def conf(tmp_path, monkeypatch):
    """A temp copy of config/ that tests may edit; no kill switch in the environment."""
    target = tmp_path / "config"
    shutil.copytree(config.CONFIG_DIR, target)
    monkeypatch.setattr(config, "CONFIG_DIR", target)
    monkeypatch.delenv(killswitch.ENV_VAR, raising=False)
    return target


@pytest.fixture
def data(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path / "data")
    monkeypatch.delenv("EARLOBE_PUBLIC_BASE_URL", raising=False)
    return tmp_path / "data"


@pytest.fixture
def store(tmp_path):
    with Store(tmp_path / "test.db") as s:
        yield s


_run_numbers = itertools.count(1)


def spend(store, show_id, usd, started="2026-10-12T09:00:00Z"):
    """Log one agent run that cost `usd`, attributed to the show."""
    store.log_run(AgentRun(agent_id="verifier", run_id=f"run_{next(_run_numbers)}", model_tier="opus",
                           started_at=started, usd_estimate=usd), show_id)


def make_script(tag="a", show_id=SHOW) -> Script:
    d = fixtures.fake("Script", show_id=show_id, episode_date=DAY)
    return Script.from_dict({"id": f"scr_{tag}", "show_id": show_id, "episode_date": DAY, **d})


def publish(store, tag="a", *, show_id=SHOW, status="published", published_at="2026-10-12T10:00:00Z",
            with_script=True) -> tuple[Script, Episode]:
    """Put a script and the episode made from it in the store, the way the pipeline would."""
    script = make_script(tag, show_id)
    decision = GateDecision(script_id=script.id, decision="PUBLISH", lane_policy="standard", revision=0,
                            scores={"corroboration_rate": 1.0, "accuracy_rate": 1.0, "balance_score": 85,
                                    "claims": len(script.claims)})
    ep = Episode(id=make_id("ep", tag), show_id=show_id, script_id=script.id, title=script.title,
                 description="[SAMPLE] test episode", show_notes_md=notes.show_notes(script, decision),
                 audio_url=f"https://earlobe.invalid/audio/{tag}.mp3", duration_sec=420,
                 published_at=published_at, guid=f"guid-{tag}", status=status, gate=decision.to_dict())
    if with_script:
        store.put(SCRIPT, script.id, script, show_id)
    store.put(EPISODE, ep.id, ep, show_id)
    return script, ep


class DisagreeingLLM(LLM):
    """Dry-run LLM whose blind verifier now finds evidence against the claims in `bad`."""

    def __init__(self, bad=()):
        super().__init__(dry_run=True)
        self.bad, self.calls = set(bad), 0

    def research(self, agent_id, tier, system, user, kind, max_searches=10, *, effort="medium", ctx=None):
        self.calls += 1
        report = super().research(agent_id, tier, system, user, kind, max_searches, effort=effort, ctx=ctx)
        for f in report["findings"]:
            if f["claim_id"] in self.bad:
                f.update(status="contradicted", note="A court filing says the opposite.")
        return report


def checkable(script: Script):
    return next(c for c in script.claims if c.type in NEEDS_CORROBORATION)


def feed_items(show_id=SHOW) -> list:
    return ET.parse(public_dir("feeds") / f"{show_id}.xml").getroot().findall(".//item")


# ================================================================== kill switch
def test_not_killed_by_default(conf):
    assert not killswitch.killed()
    assert not killswitch.killed(SHOW)
    assert killswitch.kill_reason(SHOW) is None


def test_env_all_halts_everything(conf, monkeypatch):
    monkeypatch.setenv(killswitch.ENV_VAR, "all")
    assert killswitch.killed() and killswitch.killed(SHOW) and killswitch.killed("anything")
    assert killswitch.kill_reason() == "EARLOBE_KILL=all"


def test_env_list_halts_only_the_listed_shows(conf, monkeypatch):
    monkeypatch.setenv(killswitch.ENV_VAR, " LA-Courts , cold-case-files ")
    assert killswitch.killed("la-courts") and killswitch.killed("cold-case-files")
    assert not killswitch.killed(SHOW)
    assert not killswitch.killed()          # a partial list is not a network-wide halt


def test_file_all_with_reason(conf):
    (conf / "killswitch.yaml").write_text("all: true\nshows: []\nreason: legal hold\n")
    assert killswitch.killed() and killswitch.killed(SHOW)
    assert killswitch.kill_reason(SHOW) == "legal hold"


def test_file_show_list(conf):
    (conf / "killswitch.yaml").write_text("all: false\nshows: [la-courts]\nreason: ''\n")
    assert killswitch.killed("la-courts") and not killswitch.killed(SHOW) and not killswitch.killed()
    assert "la-courts" in killswitch.kill_reason("la-courts")


def test_a_quoted_false_does_not_kill(conf):
    (conf / "killswitch.yaml").write_text("all: 'false'\nshows: []\n")
    assert not killswitch.killed()


def test_env_cannot_unkill_what_the_file_kills(conf, monkeypatch):
    (conf / "killswitch.yaml").write_text("all: true\n")
    monkeypatch.setenv(killswitch.ENV_VAR, "none")
    assert killswitch.killed(SHOW)


def test_env_kills_even_when_the_file_does_not(conf, monkeypatch):
    (conf / "killswitch.yaml").write_text("all: false\nshows: []\n")
    monkeypatch.setenv(killswitch.ENV_VAR, SHOW)
    assert killswitch.killed(SHOW) and not killswitch.killed("la-daily")


def test_missing_file_means_running(conf):
    (conf / "killswitch.yaml").unlink()
    assert not killswitch.killed(SHOW)


@pytest.mark.parametrize("text", ["all: [unclosed\n", "- just\n- a list\n", "just a string\n"])
def test_unreadable_file_halts_everything(conf, text):
    (conf / "killswitch.yaml").write_text(text)
    assert killswitch.killed() and killswitch.killed(SHOW)
    assert "unreadable" in killswitch.kill_reason(SHOW)


# ================================================================== budget
def test_caps_come_from_budgets_yaml(conf):
    assert budget.cap_for("breaking-desk") == 10.0
    assert budget.cap_for("la-daily") == 6.0
    assert budget.cap_for("some-new-show") == 5.0           # default_daily_usd


def test_missing_budgets_file_falls_back_to_built_in_caps(conf):
    (conf / "budgets.yaml").unlink()
    b = budget.load()
    assert b["network_daily_usd"] == 60.0 and b["shows"]["la-courts"] == 6.0
    assert budget.cap_for("case-tracker") == 8.0
    assert budget.cap_for("unknown") == 5.0


def test_unreadable_budgets_file_falls_back_to_built_in_caps(conf):
    (conf / "budgets.yaml").write_text("shows: [unclosed\n")
    assert budget.cap_for("breaking-desk") == 10.0


def test_a_listed_show_missing_from_a_real_file_uses_the_default(conf):
    (conf / "budgets.yaml").write_text("default_daily_usd: 2.5\nnetwork_daily_usd: 20\nshows:\n  la-daily: 9\n")
    assert budget.cap_for("la-daily") == 9.0
    assert budget.cap_for("columbia-daily") == 2.5


def test_within_budget_under_at_and_over_the_cap(conf, store):
    assert budget.within_budget(store, SHOW, DAY)           # nothing spent
    spend(store, SHOW, 4.99)
    assert budget.within_budget(store, SHOW, DAY)
    spend(store, SHOW, 0.01)                                # exactly the 5.00 cap
    assert not budget.within_budget(store, SHOW, DAY)


def test_other_shows_and_other_days_do_not_count_against_a_show(conf, store):
    spend(store, "la-daily", 50.0)
    spend(store, SHOW, 4.0, started="2026-10-11T23:59:59Z")
    assert budget.within_budget(store, SHOW, DAY)
    assert budget.within_budget(store, SHOW, "2026-10-13")


@pytest.mark.parametrize("day", [date(2026, 10, 12), NOW, DAY, "2026-10-12T05:00:00Z"])
def test_day_can_be_a_date_datetime_or_string(conf, store, day):
    spend(store, SHOW, 6.0)
    assert not budget.within_budget(store, SHOW, day)


def test_day_defaults_to_today_utc(conf, store):
    spend(store, SHOW, 6.0, started=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    assert not budget.within_budget(store, SHOW)


def test_network_cap_stops_ordinary_shows_but_not_the_breaking_lane(conf, store):
    for show in ("la-daily", "la-courts", "case-tracker", "cold-case-files", "history-of-hollywood"):
        spend(store, show, 12.0)                            # 60.0 in all: the network cap
    assert not budget.within_budget(store, SHOW, DAY)       # nothing of its own spent, still stopped
    assert budget.within_budget(store, "breaking-desk", DAY)
    spend(store, "breaking-desk", 10.0)
    assert not budget.within_budget(store, "breaking-desk", DAY)    # its own cap still applies


def test_unattributed_runs_count_toward_the_network_only(conf, store):
    spend(store, "", 59.0)
    s = budget.status(store, SHOW, DAY)
    assert s["spent"] == 0 and s["network_spent"] == 59.0 and s["within"]


def test_status_warns_near_the_cap(conf, store):
    spend(store, SHOW, 4.0)                                 # 80% of 5.00
    s = budget.status(store, SHOW, DAY)
    assert s["warn"] and s["within"] and s["cap"] == 5.0
    assert not budget.status(store, "la-daily", DAY)["warn"]


# ================================================================== corrections
def test_open_correction_stores_an_open_record_and_dedupes(conf, data, store):
    publish(store)
    ep_id = make_id("ep", "a")
    c = corrections.open_correction(store, ep_id, "The vote was 4-3,   not 5-2.", reported_by="listener", now=NOW)
    assert (c.status, c.action, c.episode_id, c.created_at) == ("open", "note", ep_id, "2026-10-12T12:00:00Z")
    assert c.description == "The vote was 4-3, not 5-2."
    again = corrections.open_correction(store, ep_id, "The vote was 4-3, not 5-2.", reported_by="listener")
    assert again.id == c.id and len(store.list(CORRECTION)) == 1
    assert store.list(CORRECTION, show_id=SHOW)[0]["id"] == c.id        # attributed to the show


def test_open_correction_is_per_claim_whatever_the_wording(conf, data, store):
    publish(store)
    ep_id = make_id("ep", "a")
    a = corrections.open_correction(store, ep_id, "first wording", claim_id="clm_1", reported_by="monitor:recheck")
    b = corrections.open_correction(store, ep_id, "second wording", claim_id="clm_1", reported_by="monitor:recheck")
    other = corrections.open_correction(store, ep_id, "first wording", claim_id="clm_2", reported_by="monitor:recheck")
    assert a.id == b.id != other.id


def test_open_correction_for_an_unknown_episode_fails_loudly(conf, data, store):
    with pytest.raises(LookupError):
        corrections.open_correction(store, "ep_missing", "nope")


def test_apply_note_corrects_status_notes_feed_and_trust_log(conf, data, store):
    script, ep = publish(store)
    c = corrections.open_correction(store, ep.id, "The vote was 4-3, not 5-2.", now=NOW)
    out = corrections.apply_correction(store, c)

    assert out.status == "corrected"
    saved = Episode.from_dict(store.get(EPISODE, ep.id))
    assert saved.status == "corrected" and saved.show_notes_md == out.show_notes_md
    assert store.get(CORRECTION, c.id)["status"] == "applied"

    note = "- 2026-10-12 (note): The vote was 4-3, not 5-2."
    section = saved.show_notes_md.split("## Corrections")[1]
    assert note in section
    assert saved.show_notes_md.rstrip().endswith(notes.disclosure_text(config.load_shows()[SHOW]))
    assert saved.show_notes_md.index(note) < saved.show_notes_md.index("**AI disclosure:**")

    items = feed_items()
    assert len(items) == 1                                   # corrected episodes stay in the feed
    assert "The vote was 4-3, not 5-2." in ET.tostring(items[0], encoding="unicode")

    log = [l for l in trustlog.read(SHOW) if l["event"] == "correction"]
    assert len(log) == 1 and log[0]["episode_id"] == ep.id
    assert log[0]["corrections"][0]["id"] == c.id and log[0]["corrections"][0]["status"] == "applied"


def test_apply_retract_removes_the_episode_from_the_feed(conf, data, store):
    _, ep = publish(store, "a")
    publish(store, "b")
    c = corrections.open_correction(store, ep.id, "The story was a hoax.", action="retract", now=NOW)
    assert corrections.apply_correction(store, c).status == "retracted"
    guids = [i.findtext("guid") for i in feed_items()]
    assert guids == ["guid-b"]
    assert "- 2026-10-12 (retract): The story was a hoax." in store.get(EPISODE, ep.id)["show_notes_md"]
    assert [l["corrections"][0]["action"] for l in trustlog.read(SHOW)] == ["retract"]


def test_apply_is_idempotent(conf, data, store):
    _, ep = publish(store)
    c = corrections.open_correction(store, ep.id, "A fix.", now=NOW)
    first = corrections.apply_correction(store, c)
    feed_xml = (public_dir("feeds") / f"{SHOW}.xml").read_text()
    second = corrections.apply_correction(store, store.get(CORRECTION, c.id))
    assert second.show_notes_md == first.show_notes_md and second.show_notes_md.count("A fix.") == 1
    assert (public_dir("feeds") / f"{SHOW}.xml").read_text() == feed_xml
    assert len(trustlog.read(SHOW)) == 1


def test_a_retracted_episode_is_never_downgraded(conf, data, store):
    _, ep = publish(store)
    corrections.apply_correction(store, corrections.open_correction(store, ep.id, "Gone.", action="retract"))
    out = corrections.apply_correction(store, corrections.open_correction(store, ep.id, "Late typo.", now=NOW))
    assert out.status == "retracted"


@pytest.mark.parametrize("status", ["draft", "gated", "killed"])
def test_an_episode_that_was_never_live_is_not_promoted(conf, data, store, status):
    _, ep = publish(store, status=status)
    out = corrections.apply_correction(store, corrections.open_correction(store, ep.id, "A fix.", now=NOW))
    assert out.status == status
    assert feed_items_or_none() == []


def feed_items_or_none() -> list:
    path = public_dir("feeds") / f"{SHOW}.xml"
    return ET.parse(path).getroot().findall(".//item") if path.exists() else []


def test_apply_refuses_a_rejected_correction_and_a_missing_episode(conf, data, store):
    _, ep = publish(store)
    c = corrections.open_correction(store, ep.id, "Not a real problem.", now=NOW)
    c.status = "rejected"
    with pytest.raises(ValueError):
        corrections.apply_correction(store, c)
    c.status, c.episode_id = "open", "ep_missing"
    with pytest.raises(LookupError):
        corrections.apply_correction(store, c)


def test_apply_accepts_a_dict_and_leaves_other_episodes_alone(conf, data, store):
    _, ep = publish(store, "a")
    _, other = publish(store, "b")
    c = corrections.open_correction(store, ep.id, "A fix.", now=NOW)
    corrections.apply_correction(store, c.to_dict())
    assert store.get(EPISODE, other.id)["status"] == "published"


def test_apply_open_applies_only_open_corrections(conf, data, store):
    _, ep = publish(store)
    done = corrections.open_correction(store, ep.id, "Already done.", now=NOW)
    corrections.apply_correction(store, done)
    corrections.open_correction(store, ep.id, "Still open.", now=NOW)
    changed = corrections.apply_open(store)
    assert len(changed) == 1 and "Still open." in changed[0].show_notes_md
    assert corrections.apply_open(store) == []


def test_note_is_exactly_what_show_notes_writes_for_applied_corrections(conf, data, store):
    script, ep = publish(store)
    decision = GateDecision.from_dict(ep.gate)
    one = corrections.open_correction(store, ep.id, "First fix [sic].", claim_id="clm_1", now=NOW)
    two = corrections.open_correction(store, ep.id, "Second fix.", action="reissue", now=NOW)
    before = ep.show_notes_md
    assert "## Corrections" in before and "- 2026" not in before
    assert corrections.append_note(before, one) == notes.show_notes(script, decision, corrections=[one])
    both = corrections.append_note(corrections.append_note(before, one), two)
    assert both == notes.show_notes(script, decision, corrections=[one, two])
    assert corrections.append_note(both, one) == both        # same line twice changes nothing


def test_append_note_creates_the_section_when_notes_have_none(conf, data, store):
    _, ep = publish(store)
    c = corrections.open_correction(store, ep.id, "A fix.", now=NOW)
    assert corrections.append_note("", c) == "## Corrections\n\n- 2026-10-12 (note): A fix.\n"
    plain = "Summary.\n\n## Sources\n\n1. A: [x](https://e.invalid)\n"
    out = corrections.append_note(plain, c)
    assert out.endswith("## Corrections\n\n- 2026-10-12 (note): A fix.\n") and out.startswith(plain.rstrip())
    with_rule = "Summary.\n\n---\n\n**AI disclosure:** yes.\n"
    out = corrections.append_note(with_rule, c)
    assert out == ("Summary.\n\n## Corrections\n\n- 2026-10-12 (note): A fix.\n\n---\n\n**AI disclosure:** yes.\n")


# ================================================================== re-check
def test_dry_run_recheck_opens_nothing_and_logs_its_cost(conf, data, store):
    script, ep = publish(store)
    llm = LLM(dry_run=True)
    assert recheck(store, llm, days=7, now=NOW) == []
    assert llm.runs and all(r.agent_id.startswith("verifier") for r in llm.runs)
    logged = store.list("agent_run", show_id=SHOW)
    assert {r["run_id"] for r in logged} == {r.run_id for r in llm.runs}
    report = store.list(RECHECK_REPORT)[0]
    assert report["episode_id"] == ep.id and report["script_id"] == script.id
    assert {f["claim_id"] for f in report["findings"]} <= {c.id for c in script.claims}


def test_contradicted_claim_opens_exactly_one_correction(conf, data, store):
    script, ep = publish(store)
    claim = checkable(script)
    llm = DisagreeingLLM([claim.id])
    opened = recheck(store, llm, days=7, now=NOW)

    assert len(opened) == 1
    c = opened[0]
    assert (c.episode_id, c.claim_id, c.status, c.action, c.reported_by) == (
        ep.id, claim.id, "open", "note", "monitor:recheck")
    assert claim.text in c.description and "A court filing says the opposite." in c.description
    assert store.get(CORRECTION, c.id)["status"] == "open"
    assert store.get(EPISODE, ep.id)["status"] == "published"      # opening is not applying
    assert trustlog.read(SHOW) == []

    assert recheck(store, DisagreeingLLM([claim.id]), days=7, now=NOW + timedelta(hours=6)) == []
    assert len(store.list(CORRECTION)) == 1


def test_a_rejected_recheck_correction_is_not_reopened(conf, data, store):
    script, ep = publish(store)
    claim = checkable(script)
    c = recheck(store, DisagreeingLLM([claim.id]), now=NOW)[0]
    stored = store.get(CORRECTION, c.id)
    store.put(CORRECTION, c.id, {**stored, "status": "rejected"}, SHOW)
    assert recheck(store, DisagreeingLLM([claim.id]), now=NOW + timedelta(days=1)) == []
    assert store.get(CORRECTION, c.id)["status"] == "rejected"


def test_a_recheck_correction_can_then_be_applied(conf, data, store):
    script, ep = publish(store)
    recheck(store, DisagreeingLLM([checkable(script).id]), now=NOW)
    [out] = corrections.apply_open(store)
    assert out.status == "corrected" and "On re-check, independent sources contradict" in out.show_notes_md
    assert len(feed_items()) == 1


def test_only_episodes_inside_the_window_are_rechecked(conf, data, store):
    publish(store, "old", published_at="2026-10-01T10:00:00Z")
    publish(store, "edge", published_at="2026-10-05T12:00:00Z")
    llm = DisagreeingLLM()
    recheck(store, llm, days=7, now=NOW)
    assert {r["episode_id"] for r in store.list(RECHECK_REPORT)} == {make_id("ep", "edge")}
    llm = DisagreeingLLM()
    recheck(store, llm, days=30, now=NOW)
    assert len(store.list(RECHECK_REPORT)) == 2


@pytest.mark.parametrize("status", ["draft", "gated", "rendered", "retracted", "killed"])
def test_episodes_that_are_not_live_are_skipped(conf, data, store, status):
    publish(store, status=status)
    llm = DisagreeingLLM()
    assert recheck(store, llm, now=NOW) == [] and llm.calls == 0


def test_corrected_episodes_are_still_rechecked(conf, data, store):
    publish(store, status="corrected")
    llm = DisagreeingLLM()
    recheck(store, llm, now=NOW)
    assert llm.calls >= 1


def test_episodes_without_a_date_or_a_script_are_skipped(conf, data, store):
    publish(store, "nodate", published_at=None)
    publish(store, "noscript", with_script=False)
    llm = DisagreeingLLM()
    assert recheck(store, llm, now=NOW) == [] and llm.calls == 0


def test_a_show_over_budget_is_skipped_unless_told_otherwise(conf, data, store):
    publish(store)
    spend(store, SHOW, 99.0)
    llm = DisagreeingLLM()
    assert recheck(store, llm, now=NOW) == [] and llm.calls == 0
    recheck(store, llm, now=NOW, respect_budget=False)
    assert llm.calls >= 1


def test_the_kill_switch_does_not_stop_corrections(conf, data, store, monkeypatch):
    script, _ = publish(store)
    monkeypatch.setenv(killswitch.ENV_VAR, "all")
    assert len(recheck(store, DisagreeingLLM([checkable(script).id]), now=NOW)) == 1
    assert len(corrections.apply_open(store)) == 1


def test_each_show_is_rechecked_and_corrected_on_its_own(conf, data, store):
    a, _ = publish(store, "a", show_id=SHOW)
    b, _ = publish(store, "b", show_id="la-daily")
    opened = recheck(store, DisagreeingLLM([checkable(b).id]), now=NOW)
    assert [c.episode_id for c in opened] == [make_id("ep", "b")]
    corrections.apply_open(store)
    assert store.get(EPISODE, make_id("ep", "a"))["status"] == "published"
    assert store.list(CORRECTION, show_id="la-daily") and not store.list(CORRECTION, show_id=SHOW)


# ================================================================== workflows
needs_workflows = pytest.mark.skipif(not WORKFLOWS.is_dir(), reason="project is not inside the repo checkout")
WORKFLOW_FILES = ["earlobe-ci", "earlobe-daily-briefs", "earlobe-breaking", "earlobe-evergreen"]
SCHEDULED = ["earlobe-daily-briefs", "earlobe-evergreen"]
FIVE = ("ANTHROPIC_API_KEY", "ELEVENLABS_API_KEY", "EARLOBE_MODEL_OPUS", "EARLOBE_MODEL_SONNET",
        "EARLOBE_MODEL_HAIKU")


def load_workflow(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / f"{name}.yml").read_text(encoding="utf-8"))


def triggers(doc: dict) -> dict:
    return doc.get("on") or doc.get(True)            # YAML 1.1 reads a bare `on` as True


def crons(doc: dict) -> list[str]:
    return [s["cron"] for s in triggers(doc).get("schedule", [])]


def run_picker(doc: dict, schedule: str = "", show: str = "", monkeypatch=None) -> list[str]:
    """Execute the workflow's own 'Pick the shows to run' script and return the shows it prints."""
    step = next(s for s in doc["jobs"]["run"]["steps"] if s.get("id") == "pick")
    body = step["run"].split("<<'PY' >> \"$GITHUB_OUTPUT\"\n", 1)[1].rsplit("\nPY", 1)[0]
    monkeypatch.setenv("SCHEDULE", schedule)
    monkeypatch.setenv("SHOW_INPUT", show)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(compile(body, "<pick step>", "exec"), {"__name__": "__main__"})
    line = out.getvalue().strip()
    assert line.startswith("shows=")
    return line[len("shows="):].split()


@needs_workflows
@pytest.mark.parametrize("name", WORKFLOW_FILES)
def test_workflow_files_are_valid_yaml_with_a_name_and_least_privilege(name):
    doc = load_workflow(name)
    assert doc["name"] and doc["jobs"]
    assert doc["permissions"] == {"contents": "read"}


@needs_workflows
def test_ci_runs_the_tests_on_push_and_pull_request():
    doc = load_workflow("earlobe-ci")
    on = triggers(doc)
    assert "project-earlobe/**" in on["push"]["paths"] and "project-earlobe/**" in on["pull_request"]["paths"]
    job = doc["jobs"]["test"]
    assert job["defaults"]["run"]["working-directory"] == "project-earlobe"
    text = yaml.dump(job)
    assert "'3.12'" in text and "ffmpeg" in text and "pip install -e" in text and "pytest" in text
    assert "dev" in text
    assert not any(k in text for k in ("secrets.", "ANTHROPIC_API_KEY"))     # tests need no keys


@needs_workflows
@pytest.mark.parametrize("name", SCHEDULED + ["earlobe-breaking"])
def test_scheduled_workflows_skip_cleanly_when_unconfigured(name):
    doc = load_workflow(name)
    steps = doc["jobs"]["preflight"]["steps"]
    first = steps[0]
    assert first["id"] == "check" and "not configured — skipping" in first["run"]
    for var in FIVE:
        assert var in first["run"] and var in first["env"]
    assert "secrets.ANTHROPIC_API_KEY" in first["env"]["ANTHROPIC_API_KEY"]
    assert "vars.EARLOBE_MODEL_OPUS" in first["env"]["EARLOBE_MODEL_OPUS"]
    assert "exit 1" not in first["run"]
    work = next(j for k, j in doc["jobs"].items() if k != "preflight")
    assert work["needs"] == "preflight" and "ready == 'true'" in work["if"]
    assert doc["jobs"]["preflight"]["outputs"]["ready"]


@needs_workflows
@pytest.mark.parametrize("name", SCHEDULED + ["earlobe-breaking"])
def test_scheduled_workflows_explain_the_default_branch_rule_and_upload_public_output(name):
    text = (WORKFLOWS / f"{name}.yml").read_text(encoding="utf-8")
    assert "DEFAULT branch" in text and "workflow_dispatch" in text
    doc = load_workflow(name)
    work = next(j for k, j in doc["jobs"].items() if k != "preflight")
    upload = next(s for s in work["steps"] if str(s.get("uses", "")).startswith("actions/upload-artifact"))
    assert upload["with"]["path"] == "project-earlobe/data/public"
    assert doc["concurrency"]["cancel-in-progress"] is False


@needs_workflows
@pytest.mark.parametrize("name", SCHEDULED)
def test_dispatch_takes_a_show_and_schedules_run_it(name):
    doc = load_workflow(name)
    assert triggers(doc)["workflow_dispatch"]["inputs"]["show"]["required"] is True
    work = doc["jobs"]["run"]
    command = next(s for s in work["steps"] if s.get("name") == "Run the shows")["run"]
    assert 'python -m earlobe run --show "$show"' in command
    assert work["defaults"]["run"]["working-directory"] == "project-earlobe"


@needs_workflows
def test_breaking_runs_every_15_minutes_and_scans():
    doc = load_workflow("earlobe-breaking")
    assert crons(doc) == ["*/15 * * * *"]
    step = next(s for s in doc["jobs"]["scan"]["steps"] if s.get("name") == "Scan for breaking news")
    assert step["run"] == "python -m earlobe breaking-scan"


@needs_workflows
def test_secrets_stay_out_of_third_party_steps():
    for name in SCHEDULED + ["earlobe-breaking"]:
        doc = load_workflow(name)
        work = next(j for k, j in doc["jobs"].items() if k != "preflight")
        assert "env" not in work                                   # not exposed to every step
        for step in work["steps"]:
            if "uses" in step:
                assert "secrets." not in yaml.dump(step)


@needs_workflows
def test_every_enabled_cron_show_is_scheduled_by_exactly_one_workflow(monkeypatch):
    docs = {n: load_workflow(n) for n in SCHEDULED}
    for sid, cfg in config.load_shows(enabled_only=True).items():
        cadence = cfg.get("cadence") or {}
        if cadence.get("type") != "cron":
            continue
        owners = [n for n, d in docs.items() if sid in run_picker(d, cadence["cron"], "", monkeypatch)]
        assert len(owners) == 1, f"{sid} ({cadence['cron']}) is scheduled by {owners or 'no workflow'}"
        assert cadence["cron"] in crons(docs[owners[0]]), f"{owners[0]} lacks the cron for {sid}"


@needs_workflows
@pytest.mark.parametrize("name", SCHEDULED)
def test_every_scheduled_cron_runs_at_least_one_enabled_show(name, monkeypatch):
    doc = load_workflow(name)
    assert crons(doc)
    for cron in crons(doc):
        assert run_picker(doc, cron, "", monkeypatch), f"{name}: cron {cron!r} matches no enabled show"


@needs_workflows
def test_picker_honours_manual_runs_and_rejects_unknown_or_disabled_shows(monkeypatch):
    doc = load_workflow("earlobe-daily-briefs")
    assert run_picker(doc, "", SHOW, monkeypatch) == [SHOW]
    assert run_picker(doc, "0 0 1 1 *", "", monkeypatch) == []            # a cron nobody owns
    for bad in ("not-a-show", "nyc-daily"):                               # nyc-daily is disabled
        with pytest.raises(SystemExit):
            run_picker(doc, "", bad, monkeypatch)


# ================================================================== sql
TABLES = ["signals", "stories", "scripts", "checker_reports", "gate_decisions", "episodes",
          "corrections", "agent_runs"]


def sql_text() -> str:
    return SQL.read_text(encoding="utf-8")


def sql_code() -> str:
    return "\n".join(l.split("--")[0] for l in sql_text().splitlines())


@pytest.mark.parametrize("table", TABLES)
def test_each_table_has_jsonb_payload_rls_and_indexes(table):
    code = sql_code()
    body = re.search(rf"create table if not exists public\.{table} \((.*?)\n\);", code, re.S)
    assert body, table
    assert re.search(r"\bpayload\s+jsonb not null", body.group(1))
    assert "show_id" in body.group(1) and "created_at" in body.group(1)
    assert re.search(rf"alter table public\.{table}\s+enable row level security;", code)
    assert re.search(rf"create index if not exists \w+\s+on public\.{table} \(show_id, created_at desc\)", code)


def test_rls_is_on_with_no_public_policies_and_the_reason_is_written_down():
    code, text = sql_code().lower(), sql_text()
    assert "create policy" not in code and "grant select" not in code
    assert re.search(r"revoke all on table .*? from anon, authenticated", code, re.S)
    assert "NO policies" in text and "service_role" in text


def test_sql_vocabularies_match_schemas():
    from earlobe.schemas import DECISIONS, EPISODE_STATUS
    code = sql_code()
    for word in (*DECISIONS, *EPISODE_STATUS, "open", "applied", "rejected", "note", "reissue", "retract"):
        assert f"'{word}'" in code, word


# ================================================================== hygiene
MODEL_ID = re.compile("clau" + r"de-(?:opus|sonnet|haiku|[0-9])|(?:opus|sonnet|haiku)-[0-9]", re.IGNORECASE)
SECRET = re.compile(r"sk-[A-Za-z0-9_-]{16,}|api[_-]?key\s*=\s*[\"'][^\"']+[\"']", re.IGNORECASE)
OWNED = [*sorted((ROOT / "earlobe" / "monitor").glob("*.py")), pathlib.Path(__file__), SQL,
         *(WORKFLOWS / f"{n}.yml" for n in WORKFLOW_FILES if (WORKFLOWS / f"{n}.yml").exists())]


@pytest.mark.parametrize("path", OWNED, ids=lambda p: p.name)
def test_no_model_ids_or_secrets_in_owned_files(path):
    text = path.read_text(encoding="utf-8")
    assert not MODEL_ID.search(text)
    assert not SECRET.search(text)
