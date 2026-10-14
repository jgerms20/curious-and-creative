"""Studio and publishing: TTS, mixing, show notes, RSS feed, hosts, trust log.

No keys and no network: HTTP is replaced by fakes, audio is silent or a test tone, and
everything lands in a temp data dir. Tests that need ffmpeg skip when it is missing.
"""
import email.utils
import io
import json
import shutil
import urllib.error
import urllib.parse
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from earlobe import config, fixtures
from earlobe.publish import disclosure_text, feed, hosts, notes, trustlog
from earlobe.schemas import (
    Correction,
    Episode,
    GateDecision,
    GateReason,
    Script,
    ScriptLine,
    Source,
)
from earlobe.studio import AudioError, est_seconds, ffmpeg, mix, operator, run_tool, tts

SHOW_ID = "columbia-daily"
NS = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
      "podcast": "https://podcastindex.org/namespace/1.0",
      "content": "http://purl.org/rss/1.0/modules/content/",
      "atom": "http://www.w3.org/2005/Atom"}
needs_ffmpeg = pytest.mark.skipif(shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
                                  reason="ffmpeg/ffprobe not installed")


# ---------------------------------------------------------------- builders
@pytest.fixture
def data_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.delenv("EARLOBE_PUBLIC_BASE_URL", raising=False)
    return tmp_path


def make_script() -> Script:
    """A fixture-built Script with sources, a disclosure line and claims that cite those sources."""
    sources = [Source(id=s.id, url=s.url, outlet=s.outlet, title=s.title, tier=s.tier, kind=s.kind)
               for s in fixtures.sample_signals("columbia-sc")]
    d = fixtures.fake("Script", show_id=SHOW_ID, episode_date="2026-10-13")
    script = Script.from_dict({"id": "scr_test", "show_id": SHOW_ID, "episode_date": "2026-10-13",
                               "sources": [s.to_dict() for s in sources], **d})
    script.lines.append(ScriptLine(id="ln_disc", speaker="ava", segment="disclosure",
                                   text="This episode was written and voiced using AI."))
    return script


def short_script() -> Script:
    """Three short lines: fast to render."""
    return Script(id="scr_short", show_id=SHOW_ID, episode_date="2026-10-13", title="Short test",
                  lines=[ScriptLine("ln_1", "mara", "Good morning and welcome to the test.", segment="intro"),
                         ScriptLine("ln_2", "theo", "Today there is one small story to tell you about.", segment="body"),
                         ScriptLine("ln_3", "ava", "This episode was written and voiced using AI.", segment="disclosure")])


def make_decision(revision: int = 0, decision: str = "PUBLISH") -> GateDecision:
    return GateDecision(script_id="scr_test", decision=decision, lane_policy="standard", revision=revision,
                        scores={"corroboration_rate": 1.0, "accuracy_rate": 0.92, "balance_score": 88, "claims": 6})


def make_episode(**kw) -> Episode:
    base = {"id": "ep_test1", "show_id": SHOW_ID, "script_id": "scr_test", "title": "Test episode & more",
            "description": "What happened today.",
            "show_notes_md": "## Sources\n\n1. Outlet: [Story](https://x.invalid/a)",
            "audio_url": "https://cdn.example.invalid/audio/ep_test1.mp3", "duration_sec": 60,
            "published_at": "2026-10-13T10:00:00Z", "guid": "ep_test1", "status": "published",
            "gate": make_decision().to_dict(), "source_count": 3}
    base.update(kw)
    return Episode(**base)


class SineTTS(tts.TTS):
    """Test double: a 440 Hz tone as long as the text would take to say (needs ffmpeg)."""

    dry_run = True

    def synthesize(self, text, voice_id=""):
        return ffmpeg("-f", "lavfi", "-i", f"sine=f=440:d={max(0.5, est_seconds(text)):.2f}",
                      "-c:a", "libmp3lame", "-b:a", "128k", "-f", "mp3", "pipe:1").stdout


def loudness(path) -> dict:
    out = run_tool(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
                    "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    return mix._measure(out.stderr.decode())


def stream_info(path) -> dict:
    out = run_tool(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate,channels,codec_name",
                    "-of", "json", path]).stdout
    return json.loads(out)["streams"][0]


# ---------------------------------------------------------------- tts: chunking and ElevenLabs
def test_chunk_text_splits_at_sentence_boundaries():
    text = " ".join(f"This is sentence number {i} of the test." for i in range(200))
    chunks = tts.chunk_text(text, limit=300)
    assert len(chunks) > 1
    assert all(len(c) <= 300 for c in chunks)
    assert all(c.endswith(".") for c in chunks)              # never cut mid-sentence
    assert " ".join(chunks) == text


def test_chunk_text_edge_cases():
    assert tts.chunk_text("") == []
    assert tts.chunk_text("Short line.") == ["Short line."]
    monster = ("word " * 200).strip()                         # one 999-character "sentence"
    pieces = tts.chunk_text(monster, limit=100)
    assert all(len(p) <= 100 for p in pieces)
    assert " ".join(pieces) == monster


def test_elevenlabs_request_shape(monkeypatch):
    calls = []

    def fake_post(url, headers, payload, timeout=120):
        calls.append((url, headers, payload))
        return b"MP3" + bytes([len(calls)])

    monkeypatch.setattr(tts, "_post", fake_post)
    engine = tts.ElevenLabsTTS(api_key="test-key", model_id="test-model", max_chars=120)
    audio = engine.synthesize("First sentence is here. " * 10, "voice/abc")
    assert len(calls) > 1 and audio == b"".join(b"MP3" + bytes([i]) for i in range(1, len(calls) + 1))
    url, headers, payload = calls[0]
    assert url == f"{tts.API_ROOT}/text-to-speech/voice%2Fabc?output_format=mp3_44100_128"
    assert headers["xi-api-key"] == "test-key"
    assert set(payload) == {"text", "model_id"} and payload["model_id"] == "test-model"
    assert all(len(c[2]["text"]) <= 120 for c in calls)


def test_elevenlabs_needs_key_and_model(monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    monkeypatch.delenv("ELEVENLABS_TTS_MODEL", raising=False)
    with pytest.raises(ValueError, match="ELEVENLABS_API_KEY"):
        tts.ElevenLabsTTS()
    with pytest.raises(ValueError, match="ELEVENLABS_TTS_MODEL"):
        tts.ElevenLabsTTS(api_key="k")
    with pytest.raises(ValueError, match="voice_id"):
        tts.ElevenLabsTTS(api_key="k", model_id="m").synthesize("Hello there.", "")


def _http_error(code):
    return urllib.error.HTTPError("https://x.invalid", code, "err", None, io.BytesIO(b'{"detail": "nope"}'))


def test_elevenlabs_retries_rate_limits_but_not_auth_errors(monkeypatch):
    monkeypatch.setattr(tts.time, "sleep", lambda s: None)
    attempts = []

    def flaky(url, headers, payload, timeout=120):
        attempts.append(1)
        if len(attempts) < 3:
            raise _http_error(429)
        return b"OK"

    monkeypatch.setattr(tts, "_post", flaky)
    assert tts.ElevenLabsTTS(api_key="k", model_id="m").synthesize("Hello there.", "v") == b"OK"
    assert len(attempts) == 3

    attempts.clear()
    monkeypatch.setattr(tts, "_post", lambda *a, **k: attempts.append(1) or (_ for _ in ()).throw(_http_error(401)))
    with pytest.raises(tts.TTSError, match="401") as err:
        tts.ElevenLabsTTS(api_key="secret-key", model_id="m").synthesize("Hello there.", "v")
    assert len(attempts) == 1 and "secret-key" not in str(err.value)


def test_dry_run_tts_returns_audio_bytes():
    audio = tts.DryRunTTS().synthesize("A few words to say out loud.", "ignored")
    assert isinstance(audio, bytes) and len(audio) > 100


@needs_ffmpeg
def test_dry_run_tts_length_matches_the_estimate(tmp_path):
    text = " ".join(["word"] * 78)                             # 78 words at 155 wpm = 30.2 s
    path = tmp_path / "x.mp3"
    path.write_bytes(tts.DryRunTTS().synthesize(text))
    assert mix.probe_duration(path) == pytest.approx(est_seconds(text), abs=0.6)


def test_dry_run_tts_without_ffmpeg_gives_placeholder(monkeypatch):
    monkeypatch.setattr(tts, "have_ffmpeg", lambda: False)
    assert tts.DryRunTTS().synthesize("Anything at all.") == tts.PLACEHOLDER_MP3


# ---------------------------------------------------------------- mix
def test_voice_id_comes_from_the_env_var_named_in_voices_yaml(monkeypatch):
    voices = config.load_voices()
    monkeypatch.setenv("VOICE_MARA", "mara-voice-id")
    assert mix.voice_id_for(voices, "mara") == "mara-voice-id"
    monkeypatch.delenv("VOICE_THEO", raising=False)
    with pytest.raises(ValueError, match="VOICE_THEO"):
        mix.voice_id_for(voices, "theo")
    assert mix.voice_id_for(voices, "theo", strict=False) == ""
    with pytest.raises(ValueError, match="not a persona"):
        mix.voice_id_for(voices, "nobody")
    monkeypatch.setenv("VOICE_AVA", "ava-voice-id")           # unknown speaker on a disclosure line -> disclosure voice
    assert mix.voice_id_for(voices, "nobody", "disclosure") == "ava-voice-id"


def test_music_windows_cover_intro_and_outro_only():
    spans = [("intro", 2.0, 5.0), ("body", 5.4, 10.0), ("body", 10.4, 12.0), ("disclosure", 12.8, 16.0)]
    assert mix.music_windows(spans, total=19.0) == [(0.0, 5.0), (12.3, 19.0)]
    expr = mix._gain_expr([(0.0, 5.0), (12.3, 19.0)])
    assert expr.startswith(f"{mix.MUSIC_GAIN}*(") and "12.300" in expr


def test_render_rejects_a_script_with_nothing_to_say(data_dir):
    empty = Script(id="scr_e", show_id=SHOW_ID, episode_date="2026-10-13", title="Empty",
                   lines=[ScriptLine("ln_1", "mara", "   ")])
    with pytest.raises(ValueError, match="no speakable"):
        mix.render(empty, config.load_voices(), tts.DryRunTTS(), data_dir / "x.mp3")


def test_render_checks_voice_ids_before_spending_on_a_live_engine(data_dir, monkeypatch):
    class Live(tts.TTS):
        def synthesize(self, text, voice_id):
            raise AssertionError("must not be called")

    monkeypatch.setattr(mix, "have_ffmpeg", lambda: True)
    for var in ("VOICE_MARA", "VOICE_THEO", "VOICE_AVA"):
        monkeypatch.delenv(var, raising=False)
    with pytest.raises(ValueError, match="VOICE_MARA"):
        mix.render(short_script(), config.load_voices(), Live(), data_dir / "x.mp3")


def test_render_without_ffmpeg(data_dir, monkeypatch):
    monkeypatch.setattr(mix, "have_ffmpeg", lambda: False)
    monkeypatch.setattr(tts, "have_ffmpeg", lambda: False)
    script = short_script()
    path, duration = mix.render(script, config.load_voices(), tts.DryRunTTS(), data_dir / "out" / "ep.mp3")
    assert Path(path).read_bytes() == tts.PLACEHOLDER_MP3 * 3 and duration == script.est_duration_sec()

    class Live(tts.TTS):
        def synthesize(self, text, voice_id):
            return b"x"

    with pytest.raises(AudioError, match="ffmpeg is required"):
        mix.render(script, config.load_voices(), Live(), data_dir / "out" / "live.mp3")


@needs_ffmpeg
def test_dry_run_render_produces_a_mastered_mp3(data_dir):
    script = short_script()
    path, duration = mix.render(script, config.load_voices(), tts.DryRunTTS(), data_dir / "audio" / "ep.mp3")
    assert Path(path).is_file() and Path(path).stat().st_size > 1000
    assert not Path(path + ".part").exists()
    spoken = sum(est_seconds(l.text) for l in script.lines)
    pauses = 2 * mix.PAUSE_SEGMENT_CHANGE
    assert duration == pytest.approx(spoken + pauses, abs=3)
    info = stream_info(path)
    assert info["codec_name"] == "mp3" and int(info["sample_rate"]) == 44100 and info["channels"] == 2


@needs_ffmpeg
def test_render_masters_to_the_loudness_target(data_dir):
    path, _ = mix.render(short_script(), config.load_voices(), SineTTS(), data_dir / "tone.mp3")
    m = loudness(path)
    assert m is not None
    assert m["input_i"] == pytest.approx(mix.TARGET_I, abs=1.0)       # -16 LUFS integrated
    assert m["input_tp"] <= -1.0                                       # true peak held under the ceiling


@needs_ffmpeg
def test_render_with_a_music_bed_adds_lead_in_and_tail(data_dir):
    music = data_dir / "bed.mp3"
    ffmpeg("-f", "lavfi", "-i", "sine=f=220:d=4", "-c:a", "libmp3lame", "-f", "mp3", music)
    voices = config.load_voices()
    _, plain = mix.render(short_script(), voices, SineTTS(), data_dir / "plain.mp3")
    path, with_music = mix.render(short_script(), voices, SineTTS(), data_dir / "bed-out.mp3", music_bed=music)
    assert Path(path).is_file()
    assert with_music == pytest.approx(plain + mix.MUSIC_LEAD + mix.MUSIC_TAIL, abs=1.5)
    assert loudness(path)["input_i"] == pytest.approx(mix.TARGET_I, abs=1.5)
    with pytest.raises(FileNotFoundError):
        mix.render(short_script(), voices, SineTTS(), data_dir / "x.mp3", music_bed=data_dir / "missing.mp3")


# ---------------------------------------------------------------- operator
def test_operator_stubs_are_documented_and_not_implemented(data_dir):
    with pytest.raises(TypeError):
        operator.StudioOperator()                              # abstract
    for cls in (operator.NotebookLMOperator, operator.MetaMuseOperator):
        op = cls()
        assert isinstance(op, operator.StudioOperator) and op.tos_cleared is False
        assert "ToS" in cls.__doc__ or "terms" in cls.__doc__.lower()
        with pytest.raises(NotImplementedError):
            op.produce(short_script())


def test_dry_run_operator_writes_audio(data_dir):
    path = operator.DryRunOperator().produce(short_script())
    assert Path(path).is_file() and Path(path).stat().st_size > 0


# ---------------------------------------------------------------- show notes
def test_show_notes_include_every_source():
    script = make_script()
    md = notes.show_notes(script, make_decision(), fixtures.fake("Copy", script=script, show_cfg={}))
    numbered = [l for l in md.splitlines() if l[:3].rstrip(". ").isdigit() and ". " in l[:4]]
    assert len(numbered) == len(script.sources)
    for s in script.sources:
        assert s.url in md and s.outlet in md
    assert "1. City of Columbia" in md                         # cited sources come first


def test_show_notes_dedupes_sources_by_url():
    script = make_script()
    script.sources.append(Source(id="src_dup", url=script.sources[0].url, outlet="Duplicate Outlet"))
    md = notes.show_notes(script, make_decision())
    assert md.count(script.sources[0].url) == 1 and "Duplicate Outlet" not in md


def test_show_notes_sections_and_verification_summary():
    md = notes.show_notes(make_script(), make_decision(revision=2), {"description": "The day's news."})
    for heading in ("## Chapters", "## Sources", "## How we checked this", "## Corrections"):
        assert heading in md
    assert md.startswith("The day's news.")
    assert "**Corroboration rate:** 100%" in md
    assert "**Accuracy:** 92%" in md and "**Balance score:** 88 out of 100" in md
    assert "**Independent sources:** 8" in md
    assert "**Rewrites:** 2" in md and "**Gate decision:** PUBLISH" in md
    assert "(https://earlobe.invalid/corrections/columbia-daily)" in md
    assert "**AI disclosure:** This episode was written and voiced using AI." in md
    assert "Columbia Daily is published by Curious & Creative LLC" in md
    assert "None. The first draft passed." in notes.show_notes(make_script(), make_decision())


def test_show_notes_accept_dicts_and_list_corrections():
    fix = Correction(id="cor_1", episode_id="ep_1", description="Amount corrected to $2.1 million.",
                     created_at="2026-10-15T08:21:40Z", action="note")
    md = notes.show_notes(make_script().to_dict(), make_decision().to_dict(), None, corrections=[fix.to_dict()],
                          corrections_link="https://pod.example.invalid/c")
    assert "- 2026-10-15 (note): Amount corrected to $2.1 million." in md
    assert "(https://pod.example.invalid/c)" in md


def test_independent_sources_collapse_owners_and_syndication():
    srcs = [Source("a", "https://a.invalid/1", "Outlet A", owner_group="Group X"),
            Source("b", "https://b.invalid/1", "Outlet B", owner_group="Group X"),
            Source("c", "https://c.invalid/1", "Wire Copy", owner_group="Group Y", syndicated_from="Outlet A"),
            Source("d", "https://d.invalid/1", "Blog", tier=4),
            Source("e", "https://e.invalid/1", "Outlet E")]
    assert notes.independent_sources(srcs) == 2                # Group X once, Outlet E; copy and tier 4 ignored


def test_chapters_are_ordered_labelled_and_scaled():
    script = make_script()
    found = notes.chapters(script)
    assert found[0] == (0, "Intro") and found[-1][1] == "AI disclosure"
    assert [t for t, _ in found] == sorted(t for t, _ in found)
    assert len(found) == 1 + 3 + 1 + 1                         # intro, 3 stories, kicker, disclosure
    scaled = notes.chapters(script, duration_sec=script.est_duration_sec() * 2)
    assert scaled[-1][0] > found[-1][0]
    assert notes._clock(75) == "01:15" and notes._clock(3725) == "01:02:05"


def test_notes_html_is_escaped_and_safe():
    html = notes.notes_html("## Sources\n\n1. A: [Story](https://x.invalid/a?b=1&c=2)\n\n- <script>alert(1)</script> **bold**\n\n"
                            "[bad](javascript:alert(1))\n\n---")
    assert "<h3>Sources</h3>" in html and "<ol>" in html and "<ul>" in html and "<hr/>" in html
    assert '<a href="https://x.invalid/a?b=1&amp;c=2">Story</a>' in html
    assert "<script>" not in html and "&lt;script&gt;" in html
    assert "<strong>bold</strong>" in html
    assert "<a href=\"javascript" not in html


# ---------------------------------------------------------------- feed
def parse(xml: str) -> ET.Element:
    return ET.fromstring(xml)


def text(el: ET.Element, path: str) -> str:
    found = el.find(path, NS)
    assert found is not None, f"missing {path}"
    return found.text or ""


def test_feed_is_valid_rss_with_required_tags():
    cfg = config.load_shows()[SHOW_ID]
    xml = feed.build_feed(SHOW_ID, cfg, [make_episode()], "https://pod.example.invalid/")
    root = parse(xml)
    assert root.tag == "rss" and root.get("version") == "2.0"
    ch = root.find("channel")
    for tag in ("title", "link", "description", "language", "lastBuildDate"):
        assert text(ch, tag)
    assert text(ch, "title") == "Columbia Daily"
    assert text(ch, "itunes:explicit") == "false"
    assert text(ch, "podcast:locked") == "no"
    assert text(ch, "itunes:author")
    category = ch.find("itunes:category", NS)
    assert category.get("text") == "News" and not (category.text or "").strip()   # an attribute, not element text
    self_link = ch.find("atom:link", NS)
    assert self_link.get("rel") == "self" and self_link.get("href") == "https://pod.example.invalid/feeds/columbia-daily.xml"
    uuid.UUID(text(ch, "podcast:guid"))                        # parses as a UUID
    assert "written and voiced using AI" in text(ch, "description")


def test_feed_item_has_enclosure_disclosure_and_dates():
    cfg = config.load_shows()[SHOW_ID]
    root = parse(feed.build_feed(SHOW_ID, cfg, [make_episode()], "https://pod.example.invalid"))
    items = root.findall("channel/item")
    assert len(items) == 1
    item = items[0]
    assert text(item, "title") == "Test episode & more"
    assert "What happened today." in text(item, "description")
    assert "written and voiced using AI" in text(item, "description")      # disclosure in every item
    enc = item.find("enclosure")
    assert enc.get("url") == "https://cdn.example.invalid/audio/ep_test1.mp3"
    assert enc.get("type") == "audio/mpeg" and int(enc.get("length")) == 60 * feed.BYTES_PER_SECOND
    guid = item.find("guid")
    assert guid.text == "ep_test1" and guid.get("isPermaLink") == "false"
    assert email.utils.parsedate_to_datetime(text(item, "pubDate")).year == 2026
    assert text(item, "itunes:duration") == "00:01:00" and text(item, "itunes:explicit") == "false"
    assert "Sources" in text(item, "content:encoded") and "<ol>" in text(item, "content:encoded")
    assert item.find("podcast:transcript", NS) is None


def test_feed_enclosure_length_is_the_file_size_and_transcript_is_listed(tmp_path):
    audio = tmp_path / "ep.mp3"
    audio.write_bytes(b"x" * 1234)
    ep = make_episode(audio_path=str(audio), transcript_path="data/public/transcripts/ep_test1.vtt")
    root = parse(feed.build_feed(SHOW_ID, {"name": "Test Show"}, [ep], "https://pod.example.invalid"))
    item = root.find("channel/item")
    assert item.find("enclosure").get("length") == "1234"
    tr = item.find("podcast:transcript", NS)
    assert tr.get("url") == "https://pod.example.invalid/transcripts/ep_test1.vtt"
    assert tr.get("type") == "text/vtt"
    ep2 = make_episode(transcript_path="https://elsewhere.invalid/t.json")
    tr2 = parse(feed.build_feed(SHOW_ID, {}, [ep2])).find("channel/item/podcast:transcript", NS)
    assert tr2.get("url") == "https://elsewhere.invalid/t.json" and tr2.get("type") == "application/json"


def test_feed_leaves_out_retracted_unpublished_and_audioless_episodes():
    eps = [make_episode(id="ep_live", guid="ep_live"),
           make_episode(id="ep_fixed", guid="ep_fixed", status="corrected", published_at="2026-10-12T10:00:00Z"),
           make_episode(id="ep_retracted", guid="ep_retracted", status="retracted"),
           make_episode(id="ep_killed", guid="ep_killed", status="killed"),
           make_episode(id="ep_draft", guid="ep_draft", status="draft"),
           make_episode(id="ep_noaudio", guid="ep_noaudio", audio_url="")]
    items = parse(feed.build_feed(SHOW_ID, {}, [e.to_dict() for e in eps])).findall("channel/item")
    assert [i.find("guid").text for i in items] == ["ep_live", "ep_fixed"]    # newest first, dicts accepted


def test_feed_survives_markup_and_control_characters():
    ep = make_episode(title="Fish & Chips <b>today</b>\x08", description="Line one\x0b & two",
                      show_notes_md="<script>x</script> & more")
    root = parse(feed.build_feed(SHOW_ID, {"name": "A & B <Show>"}, [ep]))
    assert text(root.find("channel"), "title") == "A & B <Show>"
    assert text(root.find("channel/item"), "title") == "Fish & Chips <b>today</b>"
    assert "<script>" not in text(root.find("channel/item"), "content:encoded")


def test_podcast_guid_follows_the_spec():
    ns = uuid.UUID("ead4c236-bf58-58c6-a2d6-a6b28d128cb6")
    expected = str(uuid.uuid5(ns, "example.invalid/feeds/x.xml"))
    assert feed.podcast_guid("https://example.invalid/feeds/x.xml") == expected
    assert feed.podcast_guid("http://example.invalid/feeds/x.xml") == expected
    assert feed.podcast_guid("https://example.invalid/feeds/x.xml/") == expected


def test_feed_with_no_episodes_and_owner_email():
    cfg = {"name": "Empty Show", "owner_email": "owner@example.invalid"}
    root = parse(feed.build_feed("empty", cfg, []))
    ch = root.find("channel")
    assert ch.findall("item") == []
    assert text(ch, "itunes:owner/itunes:email") == "owner@example.invalid"
    assert ch.find("podcast:locked", NS).get("owner") == "owner@example.invalid"


def test_write_feed_writes_under_data_public_feeds(data_dir):
    path = feed.write_feed(SHOW_ID, config.load_shows()[SHOW_ID], [make_episode()])
    assert Path(path) == data_dir / "public" / "feeds" / "columbia-daily.xml"
    assert not Path(path + ".part").exists()
    assert parse(Path(path).read_text(encoding="utf-8")).tag == "rss"
    # rewriting after a retraction drops the item
    feed.write_feed(SHOW_ID, {}, [make_episode(status="retracted")])
    assert parse(Path(path).read_text(encoding="utf-8")).findall("channel/item") == []


# ---------------------------------------------------------------- hosts
def test_local_host_copies_audio_and_returns_the_public_url(data_dir, monkeypatch):
    src = data_dir / "render" / "ep.mp3"
    src.parent.mkdir()
    src.write_bytes(b"audio-bytes")
    url = hosts.LocalHost().publish(make_episode(), src)
    assert url == "https://earlobe.invalid/audio/ep_test1.mp3"
    assert (data_dir / "public" / "audio" / "ep_test1.mp3").read_bytes() == b"audio-bytes"
    monkeypatch.setenv("EARLOBE_PUBLIC_BASE_URL", "https://pod.example.invalid/")
    assert hosts.LocalHost().publish(make_episode().to_dict(), src) == "https://pod.example.invalid/audio/ep_test1.mp3"
    # publishing a file that is already in place is fine
    assert hosts.LocalHost().publish(make_episode(), data_dir / "public" / "audio" / "ep_test1.mp3")


def test_local_host_copies_the_transcript_too(tmp_path):
    audio, vtt = tmp_path / "a.mp3", tmp_path / "t.vtt"
    audio.write_bytes(b"a")
    vtt.write_text("WEBVTT\n")
    host = hosts.LocalHost(tmp_path / "site" / "audio", base_url="https://pod.example.invalid")
    host.publish(make_episode(transcript_path=str(vtt)), audio)
    assert (tmp_path / "site" / "transcripts" / "t.vtt").read_text() == "WEBVTT\n"


@pytest.mark.parametrize("gate", [{}, {"decision": "REWRITE"}, {"decision": "HOLD"}, {"decision": "KILL"}])
def test_hosts_refuse_anything_that_is_not_a_publish_decision(tmp_path, gate):
    audio = tmp_path / "a.mp3"
    audio.write_bytes(b"a")
    host = hosts.LocalHost(tmp_path / "out")
    with pytest.raises(hosts.PublishRefused):
        host.publish(make_episode(gate=gate), audio)
    with pytest.raises(hosts.PublishRefused):
        host.publish(make_episode(status="retracted"), audio)
    assert not (tmp_path / "out").exists() or not list((tmp_path / "out").iterdir())
    with pytest.raises(FileNotFoundError):
        host.publish(make_episode(), tmp_path / "missing.mp3")


def test_transistor_host_follows_authorize_put_create_publish(tmp_path, monkeypatch):
    audio = tmp_path / "ep.mp3"
    audio.write_bytes(b"audio-bytes")
    calls = []

    def fake_http(method, url, *, headers=None, data=None, timeout=120):
        calls.append((method, url, headers or {}, data))
        if "authorize_upload" in url:
            return 200, json.dumps({"data": {"attributes": {
                "upload_url": "https://upload.example.invalid/signed?sig=abc", "audio_url": "https://media.example.invalid/ep.mp3",
                "content_type": "audio/mpeg"}}}).encode()
        if method == "PUT":
            return 200, b""
        if method == "POST":
            return 201, json.dumps({"data": {"id": "123"}}).encode()
        return 200, json.dumps({"data": {"attributes": {"media_url": "https://media.example.invalid/e/123.mp3",
                                                        "share_url": "https://share.example.invalid/123"}}}).encode()

    monkeypatch.setattr(hosts, "_http", fake_http)
    url = hosts.TransistorHost(api_key="test-key", show_id="show-1").publish(make_episode(), audio)
    assert url == "https://media.example.invalid/e/123.mp3"
    assert [c[0] for c in calls] == ["GET", "PUT", "POST", "PATCH"]
    get, put, post, patch = calls
    assert get[1] == "https://api.transistor.fm/v1/episodes/authorize_upload?filename=ep.mp3"
    assert get[2]["x-api-key"] == "test-key"
    assert put[1].startswith("https://upload.example.invalid/signed") and put[3] == b"audio-bytes"
    assert "x-api-key" not in put[2] and put[2]["Content-Type"] == "audio/mpeg"      # the key never goes to storage
    form = urllib.parse.parse_qs(post[3].decode())
    assert form["episode[show_id]"] == ["show-1"] and form["episode[audio_url]"] == ["https://media.example.invalid/ep.mp3"]
    assert form["episode[title]"] == ["Test episode & more"]
    assert patch[1] == "https://api.transistor.fm/v1/episodes/123/publish"
    assert urllib.parse.parse_qs(patch[3].decode()) == {"episode[status]": ["published"]}


def test_transistor_host_errors_and_dry_run(tmp_path, monkeypatch):
    audio = tmp_path / "ep.mp3"
    audio.write_bytes(b"a")
    monkeypatch.delenv("TRANSISTOR_API_KEY", raising=False)
    with pytest.raises(ValueError, match="TRANSISTOR_API_KEY"):
        hosts.TransistorHost(show_id="s")
    with pytest.raises(ValueError, match="show_id"):
        hosts.TransistorHost(api_key="k")

    monkeypatch.setattr(hosts, "_http", lambda *a, **k: (200, b'{"unexpected": true}'))
    with pytest.raises(hosts.HostError, match="authorize_upload"):
        hosts.TransistorHost(api_key="k", show_id="s").publish(make_episode(), audio)

    def no_network(*a, **k):
        raise AssertionError("dry run must not touch the network")

    monkeypatch.setattr(hosts, "_http", no_network)
    url = hosts.TransistorHost(show_id="s", dry_run=True).publish(make_episode(), audio)
    assert url == "https://share.transistor.invalid/s/ep_test1"
    with pytest.raises(hosts.PublishRefused):
        hosts.TransistorHost(show_id="s", dry_run=True).publish(make_episode(gate={}), audio)


# ---------------------------------------------------------------- trust log
def test_trustlog_appends_one_json_line_per_decision(data_dir):
    path = trustlog.append(SHOW_ID, make_episode(), make_decision())
    assert Path(path) == data_dir / "public" / "trustlog" / "columbia-daily.jsonl"
    (line,) = trustlog.read(SHOW_ID)
    assert line["episode_id"] == "ep_test1" and line["date"] == "2026-10-13"
    assert line["decision"] == "PUBLISH" and line["lane"] == "standard" and line["revision"] == 0
    assert line["scores"]["corroboration_rate"] == 1.0 and line["scores"]["claims"] == 6
    assert line["source_count"] == 3 and line["corrections"] == [] and line["rules"] == []
    assert json.loads(Path(path).read_text(encoding="utf-8").splitlines()[0]) == line


def test_trustlog_is_idempotent_and_logs_corrections_and_kills(data_dir):
    ep, dec = make_episode(), make_decision()
    trustlog.append(SHOW_ID, ep, dec)
    trustlog.append(SHOW_ID, ep.to_dict(), dec.to_dict())                 # same record again: no new line
    assert len(trustlog.read(SHOW_ID)) == 1

    fix = Correction(id="cor_1", episode_id="ep_test1", description="Amount corrected.", claim_id="clm_2",
                     reported_by="monitor:recheck", action="reissue", status="applied")
    trustlog.append(SHOW_ID, ep, dec, corrections=[fix], event="correction")
    trustlog.append(SHOW_ID, ep, dec, corrections=[fix], event="correction")
    lines = trustlog.read(SHOW_ID)
    assert [l["event"] for l in lines] == ["gate", "correction"]
    assert lines[1]["corrections"][0] == {"id": "cor_1", "action": "reissue", "claim_id": "clm_2",
                                          "reported_by": "monitor:recheck", "status": "applied",
                                          "summary": "Amount corrected."}

    killed = GateDecision(script_id="scr_dead", decision="KILL", lane_policy="strict", revision=2,
                          reasons=[GateReason(rule_id="V3", detail="x"), GateReason(rule_id="L2", detail="y")])
    trustlog.append(SHOW_ID, None, killed)                                # no episode ever existed
    last = trustlog.read(SHOW_ID)[-1]
    assert last["decision"] == "KILL" and last["episode_id"] == "" and last["script_id"] == "scr_dead"
    assert last["rules"] == ["V3", "L2"]


# ---------------------------------------------------------------- everything together
def test_dry_run_publish_flow_end_to_end(data_dir):
    cfg = config.load_shows()[SHOW_ID]
    script, decision = make_script(), make_decision()
    audio, duration = mix.render(script, config.load_voices(), tts.DryRunTTS(), data_dir / "audio" / "ep.mp3")
    md = notes.show_notes(script, decision, fixtures.fake("Copy", script=script, show_cfg=cfg), duration_sec=duration)
    ep = make_episode(audio_path=audio, duration_sec=duration, show_notes_md=md, audio_url="",
                      disclosure_text=disclosure_text(cfg), source_count=len(script.sources), status="rendered")
    ep.audio_url = hosts.LocalHost().publish(ep, audio)
    ep.status = "published"
    feed_path = feed.write_feed(SHOW_ID, cfg, [ep])
    trustlog.append(SHOW_ID, ep, decision)

    item = parse(Path(feed_path).read_text(encoding="utf-8")).find("channel/item")
    assert item.find("enclosure").get("url") == "https://earlobe.invalid/audio/ep_test1.mp3"
    assert int(item.find("enclosure").get("length")) == Path(audio).stat().st_size
    assert all(s.url in md for s in script.sources)
    assert trustlog.read(SHOW_ID)[0]["source_count"] == len(script.sources)
