"""earlobe.sensors with no network and no keys.

Every feed, JSON reply and HTTP response here is an inline sample. base.fetch (or urlopen, for
the fetch tests) is replaced, so a stray real request would fail loudly instead of going out.
"""
import io
import json
import urllib.error
import urllib.parse
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import pytest

from earlobe import sensors
from earlobe.schemas import Signal, make_id
from earlobe.sensors import base, courtlistener, gdelt, gnews, press, rss

NOW = datetime(2026, 10, 11, 13, 0, tzinfo=timezone.utc)

RSS_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:dc="http://purl.org/dc/elements/1.1/"
     xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel><title>Sample Gazette</title><link>https://gazette.example</link>
<item>
  <title>Council approves park budget</title>
  <link>https://gazette.example/news/park?id=7&amp;utm_source=rss&amp;utm_medium=feed#comments</link>
  <pubDate>Sun, 11 Oct 2026 12:30:00 GMT</pubDate>
  <description>&lt;p&gt;The council voted &lt;b&gt;5-2&lt;/b&gt; on Tuesday &amp;amp; adjourned.&lt;/p&gt;</description>
  <content:encoded>FULL ARTICLE TEXT THAT MUST NOT BE COPIED</content:encoded>
  <guid isPermaLink="false">gazette-123</guid>
  <dc:creator>A. Reporter</dc:creator>
</item>
<item><title>Entry with no link at all</title><guid>not-a-url</guid></item>
<item>
  <title>Guid doubles as the URL</title>
  <guid isPermaLink="true">https://gazette.example/g/1</guid>
  <dc:date>2026-10-11T12:00:00Z</dc:date>
</item>
</channel></rss>"""

ATOM_SAMPLE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>County Newsroom</title>
  <link rel="self" href="https://county.example/feed.atom"/>
  <entry>
    <title type="html">Boil-water notice lifted</title>
    <link rel="self" href="https://county.example/entry/1.atom"/>
    <link rel="alternate" type="text/html" href="https://county.example/news/boil-water"/>
    <id>urn:uuid:1</id>
    <published>2026-10-11T08:15:00-04:00</published>
    <updated>2026-10-11T09:00:00-04:00</updated>
    <summary>Residents may resume normal use.</summary>
    <author><name>County PIO</name></author>
  </entry>
  <entry>
    <title>Updated only</title>
    <link href="https://county.example/news/updated-only"/>
    <updated>2026-10-10T23:59:59Z</updated>
    <content type="html">&lt;p&gt;Body text&lt;/p&gt;</content>
  </entry>
</feed>"""

GNEWS_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>"city council" - Google News</title>
<item>
  <title>Council votes on stadium deal - The State</title>
  <link>https://news.google.com/rss/articles/CBMiAAA?oc=5</link>
  <guid isPermaLink="false">CBMiAAA</guid>
  <pubDate>Sun, 11 Oct 2026 12:00:00 GMT</pubDate>
  <description>&lt;a href="https://news.google.com/rss/articles/CBMiAAA?oc=5"&gt;Council votes on stadium deal&lt;/a&gt;&amp;nbsp;&amp;nbsp;&lt;font color="#6f6f6f"&gt;The State&lt;/font&gt;</description>
  <source url="https://www.thestate.com">The State</source>
</item>
<item>
  <title>Stadium deal heads to a vote - WIS News 10</title>
  <link>https://news.google.com/rss/articles/CBMiBBB?oc=5</link>
  <pubDate>Sun, 11 Oct 2026 11:00:00 GMT</pubDate>
  <description>&lt;a href="x"&gt;Stadium deal heads to a vote&lt;/a&gt;</description>
  <source url="https://www.wistv.com">WIS News 10</source>
</item>
<item>
  <title>Same story, duplicate link - The State</title>
  <link>https://news.google.com/rss/articles/CBMiAAA?oc=5</link>
  <source url="https://www.thestate.com">The State</source>
</item>
</channel></rss>"""

GDELT_SAMPLE = json.dumps({"articles": [
    {"url": "https://www.alpha.example/a?utm_campaign=x", "title": "Quake rattles coast",
     "seendate": "20261011T123000Z", "domain": "alpha.example", "language": "English",
     "sourcecountry": "United States"},
    {"url": "https://beta.example/b", "title": "Earthquake hits coast", "seendate": "20261011T123500Z",
     "domain": "www.beta.example", "language": "English"},
    {"url": "https://beta.example/b2", "title": "Aftershocks expected", "seendate": "20261011T124000Z",
     "domain": "beta.example"},
    {"url": "https://gamma.example/g", "title": "Tremor felt downtown", "seendate": "20261011T124500Z",
     "domain": "gamma.example"},
    {"title": "no url, ignored"},
]})

CL_PAGE_1 = json.dumps({
    "count": 3,
    "next": "https://www.courtlistener.com/api/rest/v4/search/?cursor=abc&type=r",
    "results": [
        {"docket_id": 111, "caseName": "United States v. Doe", "docketNumber": "2:26-cr-00123",
         "court": "District Court, C.D. California", "court_id": "cacd", "dateFiled": "2026-10-10",
         "docket_absolute_url": "/docket/111/united-states-v-doe/", "cause": "18:1343 Wire Fraud"},
        {"docket_id": 112, "caseName": "Acme v. Widget Co.", "docketNumber": "2:26-cv-04567",
         "court": "District Court, C.D. California", "court_id": "cacd", "dateFiled": "2026-10-11",
         "docket_absolute_url": "/docket/112/acme-v-widget-co/", "nature_of_suit": "Patent"},
    ]})
CL_PAGE_2 = json.dumps({
    "count": 3, "next": "https://evil.example/steal-token",
    "results": [{"docket_id": 113, "caseName": "In re Sample", "court_id": "scotus",
                 "dateFiled": "2026-10-11"}]})


def sig(url, **kw):
    d = dict(id=make_id("sig", url), sensor="t", market="m", beat="government", title="T", url=url,
             outlet="O", published_at="2026-10-11T12:00:00Z")
    d.update(kw)
    return Signal(**d)


def parse(xml, **kw):
    args = dict(sensor="beat-test", market="columbia-sc", beat="government", outlet="Sample Gazette", tier=2)
    args.update(kw)
    return base.parse_feed(xml, **args)


@pytest.fixture
def net(monkeypatch):
    """Route base.fetch to canned bodies by URL substring; records every call."""
    class Net:
        routes: dict = {}
        calls: list = []

        def __call__(self, url, timeout=20, *, headers=None, retries=3):
            self.calls.append((url, headers))
            for key, body in self.routes.items():
                if key in url:
                    if isinstance(body, Exception):
                        raise body
                    return body
            raise AssertionError(f"unexpected fetch: {url}")

    n = Net()
    n.routes, n.calls = {}, []
    monkeypatch.setattr(base, "fetch", n)
    monkeypatch.setattr(gdelt, "MIN_INTERVAL", 0)
    monkeypatch.setattr(base.time, "sleep", lambda s: None)
    return n


# ---------------------------------------------------------------- parse_feed
def test_parse_rss_fields_and_id():
    sigs = parse(RSS_SAMPLE, kind="press_release")
    first = sigs[0]
    assert first.url == "https://gazette.example/news/park?id=7"      # tracking params + fragment gone
    assert first.id == make_id("sig", first.url)
    assert (first.title, first.outlet, first.tier, first.kind) == (
        "Council approves park budget", "Sample Gazette", 2, "press_release")
    assert (first.sensor, first.market, first.beat) == ("beat-test", "columbia-sc", "government")
    assert first.published_at == "2026-10-11T12:30:00Z"
    assert first.summary == "The council voted 5-2 on Tuesday & adjourned."
    assert "FULL ARTICLE" not in first.summary and first.raw["guid"] == "gazette-123"
    assert first.raw["author"] == "A. Reporter"


def test_rss_skips_items_without_url_and_accepts_guid_url():
    sigs = parse(RSS_SAMPLE)
    assert [s.title for s in sigs] == ["Council approves park budget", "Guid doubles as the URL"]
    assert sigs[1].url == "https://gazette.example/g/1" and sigs[1].published_at == "2026-10-11T12:00:00Z"


def test_parse_atom_prefers_alternate_link_and_published():
    sigs = parse(ATOM_SAMPLE, outlet="County", tier=1)
    assert [s.url for s in sigs] == ["https://county.example/news/boil-water",
                                     "https://county.example/news/updated-only"]
    a, b = sigs
    assert a.published_at == "2026-10-11T12:15:00Z"                    # -04:00 converted to UTC
    assert a.summary == "Residents may resume normal use." and a.outlet == "County" and a.tier == 1
    assert b.published_at == "2026-10-10T23:59:59Z" and b.summary == "Body text"


def test_atom_with_prefixed_namespace():
    xml = ('<a:feed xmlns:a="http://www.w3.org/2005/Atom"><a:entry><a:title>Hi</a:title>'
           '<a:link href="https://x.example/1"/><a:updated>2026-10-11T00:00:00Z</a:updated></a:entry></a:feed>')
    assert [s.url for s in parse(xml)] == ["https://x.example/1"]


def test_outlet_fallbacks_and_source_override():
    assert parse(RSS_SAMPLE, outlet="")[0].outlet == "Sample Gazette"      # channel title
    bare = "<rss><channel><item><title>x</title><link>https://www.host.example/p</link></item></channel></rss>"
    assert parse(bare, outlet="")[0].outlet == "host.example"             # host as last resort
    src = ('<rss><channel><title>Agg</title><item><title>x</title><link>https://a.example/1</link>'
           '<source url="https://real.example">Real Outlet</source></item></channel></rss>')
    s = parse(src, outlet="Default")[0]
    assert s.outlet == "Real Outlet" and s.raw["source_url"] == "https://real.example"


@pytest.mark.parametrize("bad", ["", "not xml at all", "<rss><channel><item></rss>"])
def test_malformed_feed_returns_empty(bad):
    assert parse(bad) == []


def test_parse_feed_takes_bytes_and_str_with_encoding_declaration():
    text = '<?xml version="1.0" encoding="UTF-8"?><rss><channel><item><title>Café opens</title><link>https://a.example/1</link></item></channel></rss>'
    assert parse(text)[0].title == parse(text.encode("utf-8"))[0].title == "Café opens"


def test_summary_is_capped_as_a_snippet():
    long = "word " * 500
    xml = f"<rss><channel><item><title>x</title><link>https://a.example/1</link><description>{long}</description></item></channel></rss>"
    summary = parse(xml)[0].summary
    assert len(summary) <= base.MAX_SUMMARY + 1 and summary.endswith("…")


# ---------------------------------------------------------------- helpers
def test_parse_date_formats():
    assert base.parse_date("Sun, 11 Oct 2026 12:30:00 GMT") == "2026-10-11T12:30:00Z"
    assert base.parse_date("Sun, 11 Oct 2026 08:30:00 -0400") == "2026-10-11T12:30:00Z"
    assert base.parse_date("2026-10-11T12:30:00Z") == "2026-10-11T12:30:00Z"
    assert base.parse_date("2026-10-11T12:30:00.250+00:00") == "2026-10-11T12:30:00Z"
    assert base.parse_date("20261011T123000Z") == "2026-10-11T12:30:00Z"
    assert base.parse_date("2026-10-10") == "2026-10-10T00:00:00Z"
    assert base.parse_date("yesterday-ish") is None and base.parse_date(None) is None


def test_clean_url_and_dedupe_keep_first():
    assert base.clean_url("HTTPS://News.Example/Path?a=1&utm_source=x&fbclid=y#frag") == \
        "https://news.example/Path?a=1"
    a, b, c = sig("https://x.example/1?utm_source=a"), sig("https://x.example/1/"), sig("https://x.example/2")
    assert base.dedupe([a, b, c]) == [a, c]


def test_classify_beat_and_queries():
    assert base.classify_beat("Mayor and city council clash over the budget", ["sports", "government"]) == "government"
    assert base.classify_beat("Deputies arrested a man after a crash", ["government", "public_safety"]) == "public_safety"
    assert base.classify_beat("Anything at all", ["weather"]) == "weather"          # single beat wins
    assert base.classify_beat("Local bakery opens", ["government", "sports"]) == "general"
    assert base.classify_beat("whatever", []) == "general"
    assert base.beat_query("scotus") == '"Supreme Court" OR justices OR SCOTUS'
    assert base.beat_query("some_new_beat") == '"some new beat"'          # unknown beat: its name


# ---------------------------------------------------------------- fetch
class FakeResp:
    def __init__(self, body=b"ok", charset=None):
        self._buf, self.headers = io.BytesIO(body), type("H", (), {"get_content_charset": lambda s: charset})()

    def read(self, n=-1):
        return self._buf.read(n)

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_fetch_sends_browser_ua_and_extra_headers(monkeypatch):
    seen = {}

    def fake_urlopen(req, timeout):
        seen.update(req.header_items()), seen.update(timeout=timeout)
        return FakeResp("café".encode("latin-1"), charset="latin-1")

    monkeypatch.setattr(base.urllib.request, "urlopen", fake_urlopen)
    assert base.fetch("https://a.example/f", timeout=7, headers={"Authorization": "Token t"}) == "café"
    assert seen["User-agent"] == base.UA and seen["Authorization"] == "Token t" and seen["timeout"] == 7


def test_fetch_retries_transient_errors_then_succeeds(monkeypatch):
    attempts, naps = [], []

    def flaky(req, timeout):
        attempts.append(1)
        if len(attempts) < 3:
            raise urllib.error.URLError("temporary")
        return FakeResp(b"<rss/>")

    monkeypatch.setattr(base.urllib.request, "urlopen", flaky)
    monkeypatch.setattr(base.time, "sleep", naps.append)
    assert base.fetch("https://a.example/f") == "<rss/>"
    assert len(attempts) == 3 and naps == [1.5, 3.0]


def test_fetch_does_not_retry_404_and_gives_up_after_retries(monkeypatch):
    calls = []

    def err(code):
        def fake(req, timeout):
            calls.append(code)
            raise urllib.error.HTTPError(req.full_url, code, "x", {}, None)
        return fake

    monkeypatch.setattr(base.time, "sleep", lambda s: None)
    monkeypatch.setattr(base.urllib.request, "urlopen", err(404))
    with pytest.raises(urllib.error.HTTPError):
        base.fetch("https://a.example/gone")
    assert calls == [404]
    calls.clear()
    monkeypatch.setattr(base.urllib.request, "urlopen", err(503))
    with pytest.raises(urllib.error.HTTPError):
        base.fetch("https://a.example/down")
    assert calls == [503, 503, 503]


def test_fetch_refuses_oversized_body(monkeypatch):
    monkeypatch.setattr(base, "MAX_BYTES", 10)
    monkeypatch.setattr(base.urllib.request, "urlopen", lambda req, timeout: FakeResp(b"x" * 100))
    monkeypatch.setattr(base.time, "sleep", lambda s: None)
    with pytest.raises(ValueError):
        base.fetch("https://a.example/big", retries=1)


# ---------------------------------------------------------------- rss + press
def _feed_xml(*items):
    body = "".join(f"<item><title>{t}</title><link>{u}</link><pubDate>{format_datetime(d, usegmt=True)}</pubDate></item>"
                   for t, u, d in items)
    return f"<rss><channel><title>Feed</title>{body}</channel></rss>"


@pytest.fixture
def feeds(net, monkeypatch):
    now = datetime.now(timezone.utc)
    cfg = [
        {"outlet": "The State", "url": "https://thestate.example/rss", "kind": "article", "tier": 2,
         "beats": ["government", "public_safety", "sports"]},
        {"outlet": "Dead Feed", "url": "https://dead.example/rss", "kind": "article", "tier": 3, "beats": ["sports"]},
        {"outlet": "City of Columbia", "url": "https://city.example/rss", "kind": "press_release", "tier": 1,
         "beats": ["government"]},
        {"outlet": "NWS", "url": "https://nws.example/atom", "kind": "official_data", "tier": 1, "beats": ["weather"]},
    ]
    monkeypatch.setattr(base, "market_feeds", lambda market: [dict(f, outlet=f["outlet"]) for f in cfg])
    net.routes = {
        "thestate.example": _feed_xml(
            ("Deputies arrested suspect after crash", "https://thestate.example/a", now - timedelta(hours=2)),
            ("Old story from last week", "https://thestate.example/old", now - timedelta(days=7)),
            ("Bakery opens downtown", "https://thestate.example/b", now - timedelta(hours=1))),
        "dead.example": urllib.error.URLError("dns failure"),
        "city.example": _feed_xml(("Mayor announces budget", "https://city.example/n1", now - timedelta(hours=3))),
        "nws.example": "<feed xmlns='http://www.w3.org/2005/Atom'><entry><title>Flood Warning</title>"
                       "<link href='https://nws.example/w1'/><updated>%s</updated></entry></feed>"
                       % base.iso(now - timedelta(minutes=20)),
    }
    return net


def test_poll_market_tags_beats_drops_stale_and_survives_dead_feed(feeds):
    sigs = rss.poll_market("columbia-sc", since_hours=24)
    by_url = {s.url: s for s in sigs}
    assert "https://thestate.example/old" not in by_url                       # older than 24h
    assert by_url["https://thestate.example/a"].beat == "public_safety"      # keyword match
    assert by_url["https://thestate.example/b"].beat == "general"            # multi-beat feed, no match
    assert by_url["https://city.example/n1"].beat == "government"            # single-beat feed
    assert by_url["https://city.example/n1"].kind == "press_release" and by_url["https://city.example/n1"].tier == 1
    assert by_url["https://nws.example/w1"].kind == "official_data"
    assert {s.sensor for s in sigs} == {"beat-columbia-sc"}
    assert by_url["https://thestate.example/a"].raw["feed_url"] == "https://thestate.example/rss"
    assert len(sigs) == 4                                                      # dead feed contributed nothing


def test_poll_market_kinds_filter_and_wider_window(feeds):
    assert {s.outlet for s in rss.poll_market("columbia-sc", kinds=("article",))} == {"The State"}
    assert "https://thestate.example/old" in {s.url for s in rss.poll_market("columbia-sc", since_hours=24 * 30)}


def test_poll_press_only_official_feeds(feeds):
    sigs = press.poll_press("columbia-sc", since_hours=24)
    assert {s.url for s in sigs} == {"https://city.example/n1", "https://nws.example/w1"}
    assert {s.sensor for s in sigs} == {"press-columbia-sc"} and all(s.tier == 1 for s in sigs)
    assert not any("thestate" in c[0] for c in feeds.calls)


def test_check_feeds_reports_each_feed(feeds):
    rows = {r["outlet"]: r for r in rss.check_feeds("columbia-sc")}
    assert rows["The State"]["ok"] and rows["The State"]["items"] == 3 and rows["The State"]["newest"]
    assert not rows["Dead Feed"]["ok"] and "URLError" in rows["Dead Feed"]["error"]


def test_market_feeds_normalises_config(monkeypatch):
    from earlobe import config
    monkeypatch.setattr(config, "load_sources", lambda m: [
        {"outlet": "A", "url": "https://a.example/rss", "kind": "press_release", "tier": 1, "beats": ["government"]},
        {"url": "https://b.example/rss", "beat": "sports"}, "https://c.example/rss", {"outlet": "no url"}])
    a, b, c = base.market_feeds("x")
    assert (a["kind"], a["tier"], a["beats"]) == ("press_release", 1, ["government"])
    assert (b["kind"], b["tier"], b["beats"], b["outlet"]) == ("article", 3, ["sports"], "")
    assert c["url"] == "https://c.example/rss" and c["beats"] == []
    monkeypatch.setattr(config, "load_sources", lambda m: (_ for _ in ()).throw(OSError("boom")))
    assert base.market_feeds("x") == []


def test_dry_run_paths_need_no_network_or_config(net, monkeypatch):
    monkeypatch.setattr(base, "market_feeds", lambda m: pytest.fail("dry run must not read config"))
    sample = rss.poll_market("columbia-sc", dry_run=True)
    assert sample and all(isinstance(s, Signal) and s.market == "columbia-sc" for s in sample)
    assert all(s.kind in rss.OFFICIAL_KINDS for s in press.poll_press("columbia-sc", dry_run=True))
    assert net.calls == []


# ---------------------------------------------------------------- gnews
def test_gnews_search_url():
    url = gnews.search_url('"city council" Columbia', 6)
    assert url == ("https://news.google.com/rss/search?q=%22city+council%22+Columbia+when:6h"
                   "&hl=en-US&gl=US&ceid=US:en")


def test_gnews_parses_outlet_from_source_and_tidies_titles(net):
    net.routes = {"news.google.com": GNEWS_SAMPLE}
    sigs = gnews.search("stadium", "columbia-sc", hours=12, beat="government")
    assert "when:12h" in net.calls[0][0]
    assert [(s.outlet, s.title) for s in sigs] == [
        ("The State", "Council votes on stadium deal"), ("WIS News 10", "Stadium deal heads to a vote")]
    first = sigs[0]
    assert first.summary == "" and first.sensor == "gnews" and first.beat == "government"
    assert first.market == "columbia-sc" and first.tier == 3
    assert first.raw["source_url"] == "https://www.thestate.com" and first.raw["query"] == "stadium"
    assert first.published_at == "2026-10-11T12:00:00Z"


def test_gnews_failure_returns_empty(net):
    net.routes = {"news.google.com": urllib.error.URLError("offline")}
    assert gnews.search("anything", "columbia-sc") == []


# ---------------------------------------------------------------- gdelt
def test_gdelt_doc_url_matches_spec():
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(gdelt.doc_url("earthquake", "1h", 75)).query)
    assert q == {"query": ["earthquake"], "mode": ["ArtList"], "format": ["json"],
                 "timespan": ["1h"], "maxrecords": ["75"]}
    assert gdelt.doc_url("x", "1h", 75).startswith("https://api.gdeltproject.org/api/v2/doc/doc?")


def test_gdelt_articles_become_tier4_signals(net):
    net.routes = {"gdeltproject.org": GDELT_SAMPLE}
    sigs = gdelt.articles("earthquake", "1h", market="national", beat="disaster")
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(net.calls[0][0]).query)
    assert q["query"] == ["earthquake sourcelang:english"] and q["maxrecords"] == ["75"]
    assert [s.outlet for s in sigs] == ["alpha.example", "beta.example", "beta.example", "gamma.example"]
    a = sigs[0]
    assert (a.sensor, a.tier, a.kind, a.market, a.beat) == ("gdelt", 4, "article", "national", "disaster")
    assert a.url == "https://www.alpha.example/a" and a.published_at == "2026-10-11T12:30:00Z"
    assert a.raw["sourcecountry"] == "United States"


def test_gdelt_wraps_or_terms_and_can_skip_language(net):
    net.routes = {"gdeltproject.org": "{}"}
    gdelt.articles('"Supreme Court" OR justices', lang=None)
    gdelt.articles("(a OR b)", lang="spanish")
    qs = [urllib.parse.parse_qs(urllib.parse.urlsplit(u).query)["query"][0] for u, _ in net.calls]
    assert qs == ['("Supreme Court" OR justices)', "(a OR b) sourcelang:spanish"]


def test_gdelt_velocity_counts_distinct_domains_per_hour(net):
    net.routes = {"gdeltproject.org": GDELT_SAMPLE}
    assert gdelt.velocity("earthquake", "1h") == 3.0           # alpha, beta, gamma (www. folded)
    assert gdelt.velocity("earthquake", "2h") == 1.5
    assert gdelt.velocity("earthquake", "30min") == 6.0
    assert "maxrecords=250" in net.calls[0][0]


@pytest.mark.parametrize("reply", ["", "Your query was too short or too long.", "[]", '{"articles": null}'])
def test_gdelt_bad_replies_give_nothing(net, reply):
    net.routes = {"gdeltproject.org": reply}
    assert gdelt.articles("x") == [] and gdelt.velocity("x") == 0.0


def test_gdelt_bad_timespan_and_network_error(net):
    assert gdelt.velocity("x", "soon") == 0.0 and net.calls == []
    net.routes = {"gdeltproject.org": urllib.error.URLError("offline")}
    assert gdelt.articles("x") == [] and gdelt.velocity("x") == 0.0
    assert gdelt.timespan_hours("1d") == 24 and gdelt.timespan_hours("15min") == 0.25


# ---------------------------------------------------------------- courtlistener
def test_courtlistener_without_token_returns_empty_and_never_fetches(net, monkeypatch, caplog):
    monkeypatch.delenv("COURTLISTENER_TOKEN", raising=False)
    with caplog.at_level("WARNING"):
        assert courtlistener.recent_dockets(["cacd"]) == []
    assert net.calls == [] and "COURTLISTENER_TOKEN" in caplog.text


def test_courtlistener_request_shape(net, monkeypatch):
    monkeypatch.setenv("COURTLISTENER_TOKEN", "from-env")
    net.routes = {"courtlistener.com": json.dumps({"results": [], "next": None})}
    courtlistener.recent_dockets(["cacd", "nysd"], since_hours=24, now=NOW)
    url, headers = net.calls[0]
    q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
    assert url.startswith("https://www.courtlistener.com/api/rest/v4/search/?")
    assert q["type"] == ["r"] and q["court"] == ["cacd nysd"] and q["filed_after"] == ["10/10/2026"]
    assert headers == {"Authorization": "Token from-env"}


def test_courtlistener_explicit_token_beats_env_and_aliases_apply(net, monkeypatch):
    monkeypatch.setenv("COURTLISTENER_TOKEN", "from-env")
    net.routes = {"courtlistener.com": "{}"}
    courtlistener.recent_dockets("dsc, cacd", token="explicit", now=NOW)
    assert net.calls[0][1] == {"Authorization": "Token explicit"}
    assert urllib.parse.parse_qs(urllib.parse.urlsplit(net.calls[0][0]).query)["court"] == ["scd cacd"]
    assert courtlistener.court_ids(["CACD", "cacd", " ", None]) == ["cacd"]


def test_courtlistener_signals_and_pagination_stays_on_site(net):
    net.routes = {"cursor=abc": CL_PAGE_2, "search/?type=r": CL_PAGE_1}
    sigs = courtlistener.recent_dockets(["cacd", "scotus"], token="t", market="los-angeles", now=NOW)
    assert len(net.calls) == 2                                     # followed the site's own next link only
    assert all("evil.example" not in c[0] for c in net.calls)
    first, second, third = sigs
    assert first.url == "https://www.courtlistener.com/docket/111/united-states-v-doe/"
    assert first.title == "United States v. Doe (2:26-cr-00123)" and first.summary == "18:1343 Wire Fraud"
    assert (first.sensor, first.kind, first.tier, first.market, first.beat) == (
        "courtlistener", "court_record", 1, "los-angeles", "federal_court")
    assert first.outlet == "District Court, C.D. California" and first.published_at == "2026-10-10T00:00:00Z"
    assert first.raw["docket_id"] == 111 and first.id == make_id("sig", first.url)
    assert second.summary == "Patent"
    assert third.beat == "scotus" and third.url.endswith("/docket/113/") and third.title == "In re Sample"


def test_courtlistener_errors_return_what_we_have(net):
    net.routes = {"courtlistener.com": urllib.error.URLError("offline")}
    assert courtlistener.recent_dockets(["cacd"], token="t", now=NOW) == []
    net.routes = {"courtlistener.com": "[1, 2]"}
    assert courtlistener.recent_dockets(["cacd"], token="t", now=NOW) == []
    assert courtlistener.recent_dockets([], token="t") == []


# ---------------------------------------------------------------- run_sensors
def test_run_sensors_dry_run_returns_fixture_signals_without_io(net, monkeypatch):
    from earlobe import fixtures
    monkeypatch.setattr(base, "market_feeds", lambda m: pytest.fail("no config in dry run"))
    monkeypatch.setattr(sensors, "_market_cfg", lambda m: pytest.fail("no config in dry run"))
    for market in ("columbia-sc", "national"):
        out = sensors.run_sensors(market, ["government"], dry_run=True)
        assert out and all(isinstance(s, Signal) for s in out)
        assert [s.id for s in out] == [s.id for s in fixtures.sample_signals(market)]
    assert net.calls == []


@pytest.fixture
def stubbed(monkeypatch):
    """Replace every sensor with a recorder; returns the call log."""
    calls = []
    monkeypatch.setattr(sensors, "_market_cfg", lambda m: {"name": "Columbia, SC",
                                                           "courts": {"federal": "dsc"}} if m != "national"
                        else {"name": "National / Global", "courts": {"federal": ["scotus"]}})
    monkeypatch.setattr(rss, "poll_market", lambda m, h, dry_run=False, kinds=None: calls.append(("rss", kinds)) or [
        sig("https://a.example/1", published_at="2026-10-11T10:00:00Z"),
        sig("https://a.example/2", published_at="2026-10-11T12:00:00Z")])
    monkeypatch.setattr(press, "poll_press", lambda m, h, dry_run=False: calls.append(("press",)) or [
        sig("https://a.example/1?utm_source=dupe", sensor="press"), sig("https://c.example/3", published_at=None)])
    monkeypatch.setattr(gnews, "search", lambda q, m, hours=24, beat="", tier=3: calls.append(("gnews", q, beat)) or [
        sig(f"https://g.example/{beat}", beat=beat, published_at="2026-10-11T11:00:00Z")])
    monkeypatch.setattr(courtlistener, "recent_dockets", lambda courts, h=24, token=None, **kw: calls.append(
        ("cl", courts)) or [sig("https://cl.example/1", kind="court_record")])
    monkeypatch.setattr(gdelt, "articles", lambda q, ts="1h", **kw: calls.append(("gdelt", q, ts, kw["beat"])) or [
        sig(f"https://d.example/{kw['beat']}", beat=kw["beat"])])
    return calls


def test_run_sensors_dedupes_by_url_and_sorts_newest_first(stubbed):
    out = sensors.run_sensors("columbia-sc", ["government", "weather"], since_hours=24)
    urls = [s.url for s in out]
    assert len(urls) == len(set(urls))
    assert urls.count("https://a.example/1") == 1 and out[[s.url for s in out].index("https://a.example/1")].sensor == "t"
    assert urls[0] == "https://a.example/2" and urls[-1] == "https://c.example/3"      # undated sorts last
    assert ("rss", ("article",)) in stubbed and ("press",) in stubbed          # no double polling of official feeds
    queries = {c[2]: c[1] for c in stubbed if c[0] == "gnews"}
    assert set(queries) == {"government", "weather"}
    assert queries["government"].startswith('"Columbia, SC" ("city council" OR')
    assert not any(c[0] in ("cl", "gdelt") for c in stubbed)    # no court beat, not the national market


def test_run_sensors_court_beats_trigger_dockets_and_national_adds_gdelt(stubbed):
    sensors.run_sensors("los-angeles", ["federal_court"], 24)
    assert ("cl", "dsc") in stubbed
    stubbed.clear()
    out = sensors.run_sensors("national", ["scotus", "disaster"], since_hours=6)
    assert ("cl", ["scotus"]) in stubbed
    gd = [c for c in stubbed if c[0] == "gdelt"]
    assert [(c[2], c[3]) for c in gd] == [("6h", "scotus"), ("6h", "disaster")]
    assert not any('"National' in c[1] for c in stubbed if c[0] == "gnews")    # no place term nationally
    assert {"https://d.example/scotus", "https://d.example/disaster"} <= {s.url for s in out}


def test_one_failing_sensor_does_not_stop_the_rest(stubbed, monkeypatch, caplog):
    def boom(*a, **k):
        raise RuntimeError("feed exploded")

    monkeypatch.setattr(rss, "poll_market", boom)
    monkeypatch.setattr(gnews, "search", boom)
    with caplog.at_level("WARNING"):
        out = sensors.run_sensors("columbia-sc", ["government"], 24)
    assert {s.url for s in out} == {"https://a.example/1?utm_source=dupe", "https://c.example/3"}   # press survived
    assert "feed exploded" in caplog.text


def test_run_sensors_never_raises(monkeypatch):
    monkeypatch.setattr(sensors, "_live", lambda *a: (_ for _ in ()).throw(RuntimeError("catastrophe")))
    assert sensors.run_sensors("columbia-sc", ["government"]) == []
    from earlobe import fixtures
    monkeypatch.setattr(fixtures, "sample_signals", lambda m: (_ for _ in ()).throw(ValueError("no market")))
    assert sensors.run_sensors("atlantis", [], dry_run=True) == []


def test_run_sensors_end_to_end_through_real_config(net, monkeypatch):
    """Real config.load_sources / load_markets; every HTTP call answered from inline samples."""
    def route(url, timeout=20, *, headers=None, retries=3):
        net.calls.append((url, headers))
        if "news.google.com" in url:
            return GNEWS_SAMPLE
        if "courtlistener.com" in url:
            return "{}"
        return RSS_SAMPLE                                       # every configured feed

    monkeypatch.setattr(base, "fetch", route)
    out = sensors.run_sensors("columbia-sc", ["government", "weather"], since_hours=24 * 365 * 5)
    assert {"https://gazette.example/news/park?id=7", "https://gazette.example/g/1"} <= {s.url for s in out}
    assert {"gnews", "beat-columbia-sc"} <= {s.sensor for s in out}
    assert len({s.url for s in out}) == len(out)
    assert not any("courtlistener" in u for u, _ in net.calls)    # no court beat requested
