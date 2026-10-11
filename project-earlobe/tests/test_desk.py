"""Story Desk: independence, clustering, scoring, breaking detection, assignment.

Everything here is synthetic Signals plus the fictional fixtures; no keys, no network, no clock
(every time-sensitive call is given `now`).
"""
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from earlobe import config, fixtures
from earlobe.desk import assign as assign_mod
from earlobe.desk import breaking, cluster as cluster_mod, independence, score as score_mod
from earlobe.desk.assign import assign, lane_for, lane_hint
from earlobe.desk.breaking import BREAKING_BEATS, classify, detect
from earlobe.desk.cluster import cluster, parse_time, risk_flags
from earlobe.desk.independence import independent_count, owner_group
from earlobe.desk.score import score, triage
from earlobe.schemas import EvidenceSource, Signal, Source, Story, make_id

NOW = datetime(2026, 10, 11, 13, 0, tzinfo=timezone.utc)

OWNERS = {
    "wires": ["Associated Press", "Reuters", "AFP", "Bloomberg"],
    "groups": {
        "McClatchy": ["The State", "thestate.com"],
        "Gray Media": ["WIS", "WIS News 10", "wistv.com"],
        "TEGNA": ["WLTX", "WLTX 19", "wltx.com"],
        "Nexstar": ["KTLA", "ktla.com", "The Hill"],
        "Disney": ["ABC7 Los Angeles", "ABC News"],
        "Comcast NBCUniversal": ["NBC News", "NBC Los Angeles"],
    },
}


# ---------------------------------------------------------------- builders
def ts(minutes_ago: float) -> str:
    return (NOW - timedelta(minutes=minutes_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")


def sig(outlet, title, ago=10, *, market="columbia-sc", beat="government", tier=2, summary="",
        raw=None, kind="article", url=None):
    """Signal published `ago` minutes before NOW (ago=None: no timestamp)."""
    url = url or f"https://news.invalid/{outlet.replace(' ', '-')}/{title.replace(' ', '-')}"
    return Signal(id=make_id("sig", url, market), sensor="test", market=market, beat=beat, title=title,
                  url=url, outlet=outlet, published_at=None if ago is None else ts(ago),
                  summary=summary, kind=kind, tier=tier, raw=raw or {})


_counter = iter(range(10_000))


def story(**kw) -> Story:
    base = dict(id=f"sty_t{next(_counter)}", market="columbia-sc", beat="government",
                headline="Headline", summary="", first_seen=ts(30), independent_outlets=2)
    base.update(kw)
    return Story(**base)


# ================================================================ independence
class TestOwnerGroup:
    def test_outlet_maps_to_owner(self):
        assert owner_group("The State", OWNERS) == "McClatchy"
        assert owner_group("WIS News 10", OWNERS) == "Gray Media"

    def test_case_insensitive(self):
        assert owner_group("the STATE", OWNERS) == "McClatchy"
        assert owner_group("wlTX", OWNERS) == "TEGNA"

    def test_domains_and_urls(self):
        assert owner_group("thestate.com", OWNERS) == "McClatchy"
        assert owner_group("www.TheState.com", OWNERS) == "McClatchy"
        assert owner_group("https://www.thestate.com/news/local/article1.html", OWNERS) == "McClatchy"
        assert owner_group("news.thestate.com", OWNERS) == "McClatchy"      # subdomain -> parent domain

    def test_owner_name_maps_to_itself(self):
        assert owner_group("McClatchy", OWNERS) == "McClatchy"

    def test_wire_maps_to_the_wire_itself(self):
        assert owner_group("Associated Press", OWNERS) == "Associated Press"
        assert owner_group("reuters", OWNERS) == "Reuters"
        assert owner_group("AP", OWNERS) == "Associated Press"
        assert owner_group("apnews.com", OWNERS) == "Associated Press"
        assert owner_group("https://www.reuters.com/world/x", OWNERS) == "Reuters"

    def test_unknown_outlet_is_its_own_group(self):
        assert owner_group("Smalltown Gazette", OWNERS) == "Smalltown Gazette"
        assert owner_group("  Smalltown Gazette ", OWNERS) == "Smalltown Gazette"
        assert owner_group("blog.example.org", OWNERS) == "blog.example.org"

    def test_empty_owners_and_blank_outlet(self):
        assert owner_group("The State", {}) == "The State"
        assert owner_group("The State", None) == "The State"
        assert owner_group("", OWNERS) == ""

    def test_real_owners_file(self):
        owners = config.load_owners()
        assert owner_group("thestate.com", owners) == owner_group("The State", owners)
        assert owner_group("AP", owners) == "Associated Press"
        assert owner_group("KTLA 5", owners) == owner_group("The Hill", owners)    # both Nexstar


def src(outlet, tier=2, **kw):
    return Source(id=make_id("src", outlet, kw.get("syndicated_from", "")), url=f"https://x.invalid/{outlet}",
                  outlet=outlet, tier=tier, **kw)


def ev(outlet, tier=2, **kw):
    return EvidenceSource(url=f"https://x.invalid/{outlet}", outlet=outlet, tier=tier, **kw)


class TestIndependentCount:
    def test_empty(self):
        assert independent_count([], OWNERS) == 0
        assert independent_count(None, OWNERS) == 0

    def test_distinct_groups_each_count(self):
        assert independent_count([src("The State"), src("WIS"), src("WLTX")], OWNERS) == 3

    def test_same_owner_group_counts_once(self):
        items = [src("The State"), src("thestate.com"), src("WIS"), src("WIS News 10")]
        assert independent_count(items, OWNERS) == 2

    def test_same_unknown_outlet_counts_once_regardless_of_case(self):
        assert independent_count([src("Smalltown Gazette"), src("smalltown gazette")], OWNERS) == 1

    def test_different_unknown_outlets_are_independent(self):
        assert independent_count([src("Smalltown Gazette"), src("Riverside Courier")], OWNERS) == 2

    def test_tier_4_ignored(self):
        assert independent_count([src("The State"), src("Some Aggregator", tier=4),
                                  src("Random Blog", tier=4)], OWNERS) == 1

    def test_tier_4_alone_is_zero(self):
        assert independent_count([src("Some Aggregator", tier=4)], OWNERS) == 0

    def test_max_tier_parameter(self):
        items = [src("The State", tier=2), src("WIS", tier=3), src("FEMA", tier=1)]
        assert independent_count(items, OWNERS) == 3
        assert independent_count(items, OWNERS, max_tier=2) == 2
        assert independent_count(items, OWNERS, max_tier=1) == 1

    def test_unreadable_tier_not_counted(self):
        assert independent_count([{"outlet": "WIS", "tier": "high"}, {"outlet": "WLTX", "tier": 2}], OWNERS) == 1

    def test_wire_counts_once(self):
        assert independent_count([src("Associated Press"), src("AP")], OWNERS) == 1

    def test_syndicated_copy_collapses_into_the_wire(self):
        items = [src("Associated Press"), src("The State", syndicated_from="Associated Press"),
                 src("WLTX", syndicated_from="Associated Press")]
        assert independent_count(items, OWNERS) == 1

    def test_syndicated_copy_plus_one_real_outlet(self):
        items = [src("The State", syndicated_from="Associated Press"), src("WIS")]
        assert independent_count(items, OWNERS) == 2

    def test_syndicated_from_a_url_or_alias(self):
        items = [src("Associated Press"),
                 src("The State", syndicated_from="https://apnews.com/article/abc"),
                 src("WLTX", syndicated_from="AP")]
        assert independent_count(items, OWNERS) == 1

    def test_syndicated_from_a_non_wire_outlet_collapses_to_that_outlet(self):
        items = [src("The State"), src("Smalltown Gazette", syndicated_from="The State")]
        assert independent_count(items, OWNERS) == 1

    def test_evidence_note_naming_a_wire_collapses(self):
        items = [ev("Associated Press"), ev("Smalltown Gazette", note="Syndicated AP copy"),
                 ev("Riverside Courier", note="Reprint of Reuters story"), ev("Reuters")]
        assert independent_count(items, OWNERS) == 2          # AP and Reuters

    def test_evidence_note_ap_must_be_the_word(self):
        items = [ev("WIS", note="Map shows the closure"), ev("WLTX", note="capital project")]
        assert independent_count(items, OWNERS) == 2

    def test_evidence_without_note_counts_normally(self):
        assert independent_count([ev("WIS"), ev("WLTX", note="independent reporting at the scene")], OWNERS) == 2

    def test_evidence_that_does_not_support_is_ignored(self):
        assert independent_count([ev("WIS"), ev("WLTX", supports=False)], OWNERS) == 1

    def test_item_owner_group_label_used_for_unknown_outlets_only(self):
        items = [ev("Smalltown Gazette", owner_group="Local Media Co"),
                 ev("Riverside Courier", owner_group="Local Media Co")]
        assert independent_count(items, OWNERS) == 1
        known = [ev("The State", owner_group="Whatever LLC"), ev("thestate.com", owner_group="Other")]
        assert independent_count(known, OWNERS) == 1          # config wins over the item's own label

    def test_signals_use_raw_syndicated_from(self):
        a = sig("Associated Press", "Bridge closed")
        b = sig("The State", "Bridge closed", raw={"syndicated_from": "Associated Press"})
        c = sig("WLTX", "Bridge shut")
        assert independent_count([a, b, c], OWNERS) == 2

    def test_accepts_dicts(self):
        items = [{"outlet": "The State", "tier": 2}, {"outlet": "thestate.com", "tier": 2},
                 {"outlet": "WIS", "tier": 2, "syndicated_from": "Reuters"}]
        assert independent_count(items, OWNERS) == 2

    def test_missing_outlet_falls_back_to_url_host(self):
        items = [{"url": "https://www.thestate.com/a", "tier": 2}, {"url": "https://wltx.com/b", "tier": 2}]
        assert independent_count(items, OWNERS) == 2
        assert independent_count([{"url": "https://www.thestate.com/a"}, {"url": "https://thestate.com/b"}],
                                 OWNERS) == 1

    def test_items_naming_nobody_are_skipped(self):
        assert independent_count([{"tier": 2}], OWNERS) == 0


# ================================================================ clustering
class TestParseTime:
    def test_formats(self):
        assert parse_time("2026-10-11T13:00:00Z") == NOW
        assert parse_time("2026-10-11T09:00:00-04:00") == NOW
        assert parse_time("2026-10-11T13:00:00") == NOW          # naive -> UTC
        assert parse_time("2026-10-11T13:00:00+00:00") == NOW

    def test_bad_input(self):
        assert parse_time(None) is None
        assert parse_time("") is None
        assert parse_time("yesterday") is None


class TestClusterGrouping:
    def test_empty(self):
        assert cluster([], OWNERS) == []

    def test_rephrased_headlines_join_one_story(self):
        stories = cluster([
            sig("WIS", "City Council approves Riverbend Park budget amendment in 5-2 vote", 120),
            sig("The State", "Council approves $2.4 million Riverbend Park budget amendment", 100),
            sig("SC Daily Gazette", "Columbia council splits 5-2 on Riverbend Park budget amendment", 60, tier=3),
        ], OWNERS)
        assert len(stories) == 1
        assert len(stories[0].signal_ids) == 3

    def test_different_events_stay_separate(self):
        stories = cluster([
            sig("WIS", "Council approves Riverbend Park budget amendment", 60),
            sig("WLTX", "Elm Street Bridge closed after inspectors find structural crack", 50),
            sig("The State", "Flood watch issued for the Midlands through Sunday", 40),
        ], OWNERS)
        assert len(stories) == 3

    def test_single_shared_word_never_merges(self):
        stories = cluster([sig("WIS", "Fire downtown", 30), sig("WLTX", "Downtown parking garage opens", 20)], OWNERS)
        assert len(stories) == 2

    def test_one_word_overlap_on_tiny_titles_never_merges(self):
        # Jaccard would be 0.5 here, but one shared word is not evidence of the same event
        stories = cluster([sig("WIS", "Fire", 30), sig("WLTX", "Downtown fire", 20)], OWNERS)
        assert len(stories) == 2
        assert len(cluster([sig("WIS", "Flood watch", 30), sig("WLTX", "Flood watch issued", 20)], OWNERS)) == 1

    def test_never_merges_across_markets(self):
        title = "Council approves park budget amendment in 5-2 vote"
        stories = cluster([sig("WIS", title, 30, market="columbia-sc"),
                           sig("KTLA", title, 20, market="los-angeles")], OWNERS)
        assert sorted(s.market for s in stories) == ["columbia-sc", "los-angeles"]

    def test_duplicate_signal_ids_collapse(self):
        s = sig("WIS", "Council approves park budget amendment", 30)
        stories = cluster([s, s], OWNERS)
        assert len(stories) == 1 and stories[0].signal_ids == [s.id]

    def test_time_window_36h(self):
        title = "Council approves Riverbend Park budget amendment"
        near = cluster([sig("WIS", title, 35 * 60), sig("WLTX", title, 0)], OWNERS)
        far = cluster([sig("WIS", title, 37 * 60), sig("WLTX", title, 0)], OWNERS)
        assert len(near) == 1
        assert len(far) == 2

    def test_window_is_measured_from_the_first_signal(self):
        title = "Council approves Riverbend Park budget amendment"
        stories = cluster([sig("WIS", title, 40 * 60), sig("WLTX", title, 20 * 60),
                           sig("The State", title, 0)], OWNERS)
        assert len(stories) == 2        # the third is 40h after the first

    def test_google_news_outlet_suffix_is_ignored_for_matching_and_headline(self):
        stories = cluster([sig("WIS", "Council approves Riverbend Park budget amendment - WIS", 30),
                           sig("The State", "Council approves Riverbend Park budget amendment | The State", 20)],
                          OWNERS)
        assert len(stories) == 1
        assert stories[0].headline == "Council approves Riverbend Park budget amendment"

    def test_input_order_does_not_matter(self):
        sigs = [sig("WIS", "Council approves Riverbend Park budget amendment", 90),
                sig("The State", "Council approves $2.4 million Riverbend Park budget amendment", 70),
                sig("WLTX", "Elm Street Bridge closed after structural crack found", 50),
                sig("WIS", "Bridge on Elm Street closed after structural crack found", 40)]
        a = cluster(sigs, OWNERS)
        b = cluster(list(reversed(sigs)), OWNERS)
        assert [s.to_dict() for s in a] == [s.to_dict() for s in b]

    def test_stories_come_back_oldest_first(self):
        stories = cluster([sig("WIS", "Flood watch issued for the Midlands", 10),
                           sig("WLTX", "Council approves Riverbend Park budget amendment", 90)], OWNERS)
        assert [s.first_seen for s in stories] == sorted(s.first_seen for s in stories)

    def test_untimed_signals_still_cluster(self):
        stories = cluster([sig("WIS", "Council approves Riverbend Park budget amendment", None),
                           sig("The State", "Council approves Riverbend Park budget amendment vote", None)], OWNERS)
        assert len(stories) == 1
        assert stories[0].first_seen == "" and stories[0].velocity == 0.0
        assert stories[0].independent_outlets == 2

    def test_untimed_signal_joins_a_timed_cluster(self):
        stories = cluster([sig("WIS", "Council approves Riverbend Park budget amendment", 30),
                           sig("The State", "Council approves Riverbend Park budget amendment", None)], OWNERS)
        assert len(stories) == 1


class TestStoryFields:
    def setup_method(self):
        self.title = "Council approves Riverbend Park budget amendment"

    def test_ids_are_stable_across_reruns_and_new_arrivals(self):
        first = [sig("WIS", self.title, 90), sig("The State", self.title, 80)]
        later = first + [sig("WLTX", self.title, 10)]
        assert cluster(first, OWNERS)[0].id == cluster(later, OWNERS)[0].id
        assert cluster(first, OWNERS)[0].id.startswith("sty_")

    def test_headline_is_most_common_title(self):
        stories = cluster([sig("WIS", "Council approves Riverbend Park budget amendment", 90),
                           sig("WLTX", "Council approves Riverbend Park budget amendment quickly", 80),
                           sig("The State", "Council approves Riverbend Park budget amendment quickly", 70)], OWNERS)
        assert stories[0].headline == "Council approves Riverbend Park budget amendment quickly"

    def test_headline_tie_goes_to_earliest(self):
        stories = cluster([sig("WLTX", "Riverbend Park budget amendment gets council approval", 50),
                           sig("WIS", "Council approves Riverbend Park budget amendment", 90)], OWNERS)
        assert stories[0].headline == "Council approves Riverbend Park budget amendment"

    def test_beat_is_most_common_then_earliest(self):
        stories = cluster([sig("WIS", self.title, 90, beat="government"),
                           sig("WLTX", self.title, 80, beat="business"),
                           sig("The State", self.title, 70, beat="business")], OWNERS)
        assert stories[0].beat == "business"
        tie = cluster([sig("WIS", self.title, 90, beat="government"),
                       sig("WLTX", self.title, 80, beat="business")], OWNERS)
        assert tie[0].beat == "government"

    def test_summary_prefers_the_most_authoritative_signal(self):
        stories = cluster([sig("WIS", self.title, 90, tier=2, summary="TV summary."),
                           sig("City of Columbia", self.title, 80, tier=1, summary="Official summary."),
                           sig("WLTX", self.title, 70, tier=2, summary="")], OWNERS)
        assert stories[0].summary == "Official summary."

    def test_outlets_unique_in_order_and_include_every_tier(self):
        stories = cluster([sig("WIS", self.title, 90), sig("WLTX", self.title, 80),
                           sig("WIS", self.title + " today", 70), sig("Random Blog", self.title, 60, tier=4)],
                          OWNERS)
        assert stories[0].outlets == ["WIS", "WLTX", "Random Blog"]

    def test_independent_outlets_collapse_owner_groups_syndication_and_tier_4(self):
        stories = cluster([
            sig("Associated Press", self.title, 90),
            sig("The State", self.title, 85, raw={"syndicated_from": "Associated Press"}),
            sig("WIS", self.title, 80),
            sig("WIS News 10", self.title, 75),
            sig("Random Blog", self.title, 70, tier=4),
        ], OWNERS)
        assert stories[0].independent_outlets == 2          # AP (+ its copy) and Gray Media

    def test_source_ids_follow_urls(self):
        s = sig("WIS", self.title, 30)
        assert cluster([s], OWNERS)[0].source_ids == [make_id("src", s.url)]

    def test_official_confirmation_means_any_tier_1(self):
        without = cluster([sig("WIS", self.title, 90), sig("WLTX", self.title, 80, tier=3)], OWNERS)
        with_official = cluster([sig("WIS", self.title, 90),
                                 sig("City of Columbia", self.title, 80, tier=1, kind="press_release")], OWNERS)
        assert without[0].official_confirmation is False
        assert with_official[0].official_confirmation is True

    def test_velocity_counts_independent_outlets_in_first_hour(self):
        stories = cluster([sig("WIS", self.title, 200),            # +0
                           sig("WLTX", self.title, 180),           # +20
                           sig("WIS News 10", self.title, 170),    # +30, same group as WIS
                           sig("The State", self.title, 140),      # +60, boundary is inclusive
                           sig("KTLA", self.title, 139)], OWNERS)  # +61, outside the first hour
        s = stories[0]
        assert s.velocity == 3.0
        assert s.independent_outlets == 4

    def test_velocity_ignores_tier_4(self):
        stories = cluster([sig("WIS", self.title, 60), sig("Random Blog", self.title, 55, tier=4)], OWNERS)
        assert stories[0].velocity == 1.0

    def test_market_and_first_seen(self):
        stories = cluster([sig("WIS", self.title, 90, market="columbia-sc"),
                           sig("WLTX", self.title, 30, market="columbia-sc")], OWNERS)
        assert stories[0].market == "columbia-sc"
        assert stories[0].first_seen == ts(90)


class TestRiskFlags:
    @pytest.mark.parametrize("text,expected", [
        ("Man arrested after downtown robbery", {"crime"}),
        ("Police say suspect fled the scene", {"crime"}),
        ("Judge dismisses lawsuit against the city", {"legal_proceeding"}),
        ("Sample v. Example Studios: motion to dismiss granted", {"legal_proceeding"}),
        ("Jury returns verdict in embezzlement trial", {"legal_proceeding"}),
        ("16-year-old charged in school threat", {"minor", "crime"}),
        ("Juvenile detained after chase", {"minor"}),
        ("Victim identified in Tuesday crash", {"victim"}),
        ("Driver dies after crash on Elm Street", {"death"}),
        ("Killed in shooting, family says", {"victim", "death", "crime"}),
        ("Candidates debate ahead of the election", {"election"}),
        ("Early voting begins Monday", {"election"}),
        ("Council approves Riverbend Park budget amendment", set()),
        ("Metro announces weekend closure of Verdant Line", set()),
        ("Starlight Pictures announces studio lot expansion", set()),
    ])
    def test_keyword_rules(self, text, expected):
        assert set(risk_flags(text)) == expected

    def test_age_18_and_over_is_not_minor(self):
        assert "minor" not in risk_flags("18-year-old wins scholarship")
        assert "minor" in risk_flags("17-year-old wins scholarship")

    def test_whole_words_only(self):
        assert risk_flags("Nineteen deadlines loom for the courtesy committee") == []

    def test_flags_use_schema_vocabulary_and_fixed_order(self):
        from earlobe.schemas import RISK_FLAGS
        flags = risk_flags("Teen killed in shooting; judge sets trial; candidates react to election")
        assert all(f in RISK_FLAGS for f in flags)
        assert flags == [f for f in RISK_FLAGS if f in flags]

    def test_story_gets_flags_from_all_titles_and_summary(self):
        stories = cluster([sig("WIS", "Man arrested in downtown robbery", 90, summary=""),
                           sig("WLTX", "Downtown robbery suspect arrested", 80, summary="A judge set bond Tuesday.")],
                          OWNERS)
        assert {"crime", "legal_proceeding"} <= set(stories[0].risk_flags)


class TestClusterOnFixtures:
    @pytest.mark.parametrize("market", ["columbia-sc", "los-angeles", "new-york", "chicago", "national"])
    def test_every_sample_event_becomes_exactly_one_story(self, market):
        sigs = fixtures.sample_signals(market, now=NOW)
        by_id = {s.id: s for s in sigs}
        stories = cluster(sigs, config.load_owners())
        events_per_story = [{by_id[i].raw["event"] for i in s.signal_ids} for s in stories]
        assert all(len(e) == 1 for e in events_per_story), "a story mixes events"
        assert len(stories) == len({s.raw["event"] for s in sigs}), "an event was split"

    def test_wire_copies_collapse_in_the_sample_data(self):
        sigs = fixtures.sample_signals("columbia-sc", now=NOW)
        bridge = next(s for s in cluster(sigs, config.load_owners()) if "Elm Street Bridge" in s.headline)
        assert len(bridge.signal_ids) == 3                  # AP, The State (AP copy), WLTX
        assert bridge.independent_outlets == 2

    def test_sample_story_fields_are_valid(self):
        for market in ("columbia-sc", "national"):
            for s in cluster(fixtures.sample_signals(market, now=NOW), config.load_owners()):
                assert s.market == market and s.beat and s.headline and s.first_seen
                assert s.independent_outlets >= 1 and s.independent_outlets <= len(s.outlets)
                assert Story.from_dict(s.to_dict()) == s


# ================================================================ scoring
class TestScore:
    BEATS = {"beats": ["government", "public_safety", "weather", "sports"]}

    def test_exact_breakdown(self):
        s = story(independent_outlets=2, first_seen=ts(18 * 60), beat="government", velocity=2.0)
        # coverage 20 + official 0 + recency 10 (half the 36h window) + beat 20 (first of 4) + velocity 6
        assert score(s, self.BEATS, now=NOW) == 56

    def test_always_an_int_in_range(self):
        top = story(independent_outlets=9, official_confirmation=True, first_seen=ts(0),
                    velocity=9.0, breaking=True)
        assert score(top, self.BEATS, now=NOW) == 100
        bottom = story(independent_outlets=0, first_seen="", beat="nonsense", risk_flags=["crime"])
        assert score(bottom, self.BEATS, now=NOW) == 0
        assert isinstance(score(top, self.BEATS, now=NOW), int)

    def test_more_independent_outlets_score_higher(self):
        scores = [score(story(independent_outlets=n), self.BEATS, now=NOW) for n in range(5)]
        assert scores == sorted(scores) and scores[0] < scores[3]
        assert scores[3] == scores[4]                       # coverage is capped

    def test_official_confirmation_adds_points(self):
        base = score(story(), self.BEATS, now=NOW)
        assert score(story(official_confirmation=True), self.BEATS, now=NOW) == base + 15

    def test_recency_decays_over_the_window(self):
        fresh = score(story(first_seen=ts(0)), self.BEATS, now=NOW)
        day = score(story(first_seen=ts(18 * 60)), self.BEATS, now=NOW)
        old = score(story(first_seen=ts(36 * 60)), self.BEATS, now=NOW)
        ancient = score(story(first_seen=ts(90 * 60)), self.BEATS, now=NOW)
        assert fresh > day > old
        assert old == ancient
        assert fresh - old == 20

    def test_future_or_missing_first_seen(self):
        assert score(story(first_seen=ts(-30)), self.BEATS, now=NOW) == score(story(first_seen=ts(0)), self.BEATS, now=NOW)
        assert score(story(first_seen=""), self.BEATS, now=NOW) == score(story(first_seen=ts(36 * 60)), self.BEATS, now=NOW)

    def test_beat_priority_follows_the_show_list(self):
        s = [score(story(beat=b), self.BEATS, now=NOW) for b in ("government", "public_safety", "weather", "sports")]
        assert s == sorted(s, reverse=True) and len(set(s)) == 4

    def test_beat_priority_is_per_show(self):
        a = {"beats": ["weather", "government"]}
        b = {"beats": ["government", "weather"]}
        st = story(beat="weather")
        assert score(st, a, now=NOW) > score(st, b, now=NOW)

    def test_beat_outside_the_show_gets_nothing_but_not_below_zero(self):
        inside = score(story(beat="sports"), self.BEATS, now=NOW)
        outside = score(story(beat="entertainment_business"), self.BEATS, now=NOW)
        assert outside < inside

    def test_no_show_config_gives_a_neutral_beat_score(self):
        assert score(story(), {}, now=NOW) == score(story(), None, now=NOW)
        assert score(story(beat="anything"), {}, now=NOW) == score(story(beat="other"), {}, now=NOW)

    def test_breaking_beats_velocity(self):
        assert score(story(breaking=True), self.BEATS, now=NOW) > score(story(velocity=4.0), self.BEATS, now=NOW)

    def test_velocity_bonus_is_capped(self):
        assert score(story(velocity=4.0), self.BEATS, now=NOW) == score(story(velocity=40.0), self.BEATS, now=NOW)

    def test_thin_sourcing_on_sensitive_story_is_penalised(self):
        plain = score(story(independent_outlets=1), self.BEATS, now=NOW)
        risky = score(story(independent_outlets=1, risk_flags=["crime"]), self.BEATS, now=NOW)
        assert risky == plain - 20

    @pytest.mark.parametrize("kw", [
        dict(independent_outlets=2),                         # two groups is not thin
        dict(independent_outlets=1, official_confirmation=True),
    ])
    def test_no_penalty_when_sourcing_is_adequate(self, kw):
        plain = score(story(**kw), self.BEATS, now=NOW)
        risky = score(story(risk_flags=["crime", "minor"], **kw), self.BEATS, now=NOW)
        assert risky == plain

    def test_non_sensitive_flags_do_not_penalise(self):
        plain = score(story(independent_outlets=1), self.BEATS, now=NOW)
        assert score(story(independent_outlets=1, risk_flags=["breaking"]), self.BEATS, now=NOW) == plain

    def test_default_clock_is_used_when_now_is_omitted(self):
        fresh = story(first_seen=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        assert 0 <= score(fresh, self.BEATS) <= 100


class _StubLLM:
    """Stands in for LLM: records calls, returns a canned StoryTriage dict (or raises)."""

    def __init__(self, response=None, error=None):
        self.response, self.error, self.calls = response, error, []

    def structured(self, agent_id, tier, system, user, kind, effort="medium", **kw):
        self.calls.append(dict(agent_id=agent_id, tier=tier, system=system, user=user, kind=kind, kw=kw))
        if self.error:
            raise self.error
        return self.response(user) if callable(self.response) else self.response


class TestTriage:
    BEATS = {"name": "Columbia Daily", "market": "columbia-sc", "beats": ["government", "weather"]}

    def three(self):
        return [story(id="sty_a", independent_outlets=1, beat="weather", headline="Flood watch issued"),
                story(id="sty_b", independent_outlets=4, official_confirmation=True, headline="Council votes"),
                story(id="sty_c", independent_outlets=2, headline="Taproom opens")]

    def test_without_llm_scores_and_sorts(self):
        stories = self.three()
        ranked = triage(stories, None, self.BEATS, now=NOW)
        assert [s.id for s in ranked][0] == "sty_b"
        assert [s.newsworthiness for s in ranked] == sorted((s.newsworthiness for s in ranked), reverse=True)
        for s in stories:
            assert s.newsworthiness == score(s, self.BEATS, now=NOW)

    def test_ties_break_by_outlets_then_id(self):
        a, b = story(id="sty_a", independent_outlets=2), story(id="sty_b", independent_outlets=2)
        assert [s.id for s in triage([b, a], None, {}, now=NOW)] == ["sty_a", "sty_b"]

    def test_empty_input_makes_no_llm_call(self):
        llm = _StubLLM(response={"stories": []})
        assert triage([], llm, self.BEATS, now=NOW) == []
        assert llm.calls == []

    def test_llm_call_uses_the_haiku_tier_and_no_model_id(self):
        llm = _StubLLM(response={"stories": []})
        triage(self.three(), llm, self.BEATS, now=NOW)
        call = llm.calls[0]
        assert (call["agent_id"], call["tier"], call["kind"]) == ("story-triage", "haiku", "StoryTriage")
        assert not MODEL_ID.search(call["system"] + call["user"])
        assert "sty_b" in call["user"]

    def test_llm_rating_is_blended_not_trusted_blindly(self):
        stories = self.three()
        base = {s.id: score(s, self.BEATS, now=NOW) for s in stories}
        llm = _StubLLM(response={"stories": [
            {"cluster_key": "sty_a", "headline": "X", "summary": "", "beat": "weather", "newsworthiness": 100,
             "risk_flags": [], "entities": [], "signal_ids": []}]})
        triage(stories, llm, self.BEATS, now=NOW)
        by_id = {s.id: s for s in stories}
        assert by_id["sty_a"].newsworthiness == round(0.6 * base["sty_a"] + 0.4 * 100)
        assert by_id["sty_b"].newsworthiness == base["sty_b"]          # not in the response: heuristic only

    def test_llm_cannot_rewrite_headlines_or_summaries(self):
        stories = [story(id="sty_a", headline="Original", summary="Original summary")]
        llm = _StubLLM(response={"stories": [{"cluster_key": "sty_a", "headline": "Hijacked", "summary": "Nope",
                                              "beat": "weather", "newsworthiness": 50, "risk_flags": [],
                                              "entities": ["Mayor Example"], "signal_ids": []}]})
        triage(stories, llm, self.BEATS, now=NOW)
        assert (stories[0].headline, stories[0].summary) == ("Original", "Original summary")
        assert stories[0].entities == ["Mayor Example"]

    def test_llm_flags_are_added_validated_and_counted_in_the_penalty(self):
        stories = [story(id="sty_a", independent_outlets=1, risk_flags=["minor"])]
        before = score(stories[0], self.BEATS, now=NOW)
        llm = _StubLLM(response={"stories": [{"cluster_key": "sty_a", "headline": "", "summary": "",
                                              "beat": "", "newsworthiness": before,
                                              "risk_flags": ["crime", "minor", "bogus"],
                                              "entities": [], "signal_ids": []}]})
        triage(stories, llm, self.BEATS, now=NOW)
        assert stories[0].risk_flags == ["minor", "crime"]

    def test_llm_never_removes_flags_and_unknown_keys_are_ignored(self):
        stories = [story(id="sty_a", risk_flags=["crime"])]
        llm = _StubLLM(response={"stories": [{"cluster_key": "someone-else", "headline": "", "summary": "",
                                              "beat": "", "newsworthiness": 0, "risk_flags": [],
                                              "entities": [], "signal_ids": []}]})
        triage(stories, llm, self.BEATS, now=NOW)
        assert stories[0].risk_flags == ["crime"]
        assert stories[0].newsworthiness == score(stories[0], self.BEATS, now=NOW)

    def test_out_of_range_llm_rating_is_clamped(self):
        stories = [story(id="sty_a")]
        llm = _StubLLM(response={"stories": [{"cluster_key": "sty_a", "headline": "", "summary": "", "beat": "",
                                              "newsworthiness": 900, "risk_flags": [], "entities": [],
                                              "signal_ids": []}]})
        triage(stories, llm, self.BEATS, now=NOW)
        assert 0 <= stories[0].newsworthiness <= 100

    def test_llm_failure_falls_back_to_the_heuristic(self):
        stories = self.three()
        ranked = triage(stories, _StubLLM(error=RuntimeError("model unavailable")), self.BEATS, now=NOW)
        assert len(ranked) == 3
        assert all(s.newsworthiness == score(s, self.BEATS, now=NOW) for s in stories)

    def test_malformed_llm_response_is_tolerated(self):
        stories = self.three()
        assert len(triage(stories, _StubLLM(response={}), self.BEATS, now=NOW)) == 3
        assert len(triage(stories, _StubLLM(response=None), self.BEATS, now=NOW)) == 3

    def test_dry_run_llm_end_to_end(self):
        from earlobe.llm import LLM
        llm = LLM(dry_run=True)
        stories = cluster(fixtures.sample_signals("columbia-sc", now=NOW), config.load_owners())
        headlines = [s.headline for s in stories]
        ranked = triage(stories, llm, config.load_shows()["columbia-daily"], now=NOW)
        assert len(ranked) == len(stories)
        assert all(0 <= s.newsworthiness <= 100 for s in ranked)
        assert [s.newsworthiness for s in ranked] == sorted((s.newsworthiness for s in ranked), reverse=True)
        assert sorted(s.headline for s in ranked) == sorted(headlines)
        assert [(r.agent_id, r.model_tier, r.ok) for r in llm.runs] == [("story-triage", "haiku", True)]


# ================================================================ breaking
@pytest.mark.parametrize("text,expected", [
    ("Hurricane Zeta makes landfall near Cape Marlow", "disaster"),
    ("Magnitude 7 earthquake strikes the coast", "disaster"),
    ("Death toll rises after building collapse", "disaster"),
    ("Former president dies at 91", "major_death"),
    ("Beloved actor passed away overnight, family says", "major_death"),
    ("Gunman opens fire at stadium in mass shooting", "attack_or_attempt"),
    ("Assassination attempt on prime minister", "attack_or_attempt"),
    ("Supreme Court strikes down state law", "scotus"),
    ("White House announces executive order on tariffs", "federal_government"),
    ("Government shutdown begins as Congress misses deadline", "federal_government"),
    ("NASA launches rocket toward Mars", "space"),
    ("Super Bowl halftime show lineup revealed", "sports_mega"),
    ("Company announces $12 billion acquisition of rival", "business_mega"),
    ("Ceasefire collapses as missiles strike capital", "world"),
    ("Local man dies after crash on Elm Street", None),             # a death alone is not "major"
    ("Council approves Riverbend Park budget amendment", None),
    ("Flood watch issued for the Midlands through Sunday", None),
    ("Brush fire near Sample Canyon prompts evacuation orders", None),
    ("Heart attack survivors meet at the rec center", None),
    ("Orbital Dynamics Corp. reports record quarterly revenue", None),
    ("", None),
])
def test_classify(text, expected):
    assert classify(text) == expected


def test_classify_prefers_the_class_with_more_evidence():
    assert classify("Hurricane landfall prompts state of emergency; White House responds") == "disaster"


def test_classify_tie_follows_breaking_beat_order():
    assert classify("Prime minister dies at 80") == "major_death"      # also a "world" match


def test_every_class_has_rules_and_matches_the_show_config():
    assert set(breaking._RULES) == set(BREAKING_BEATS)
    assert list(BREAKING_BEATS) == config.load_shows()["breaking-desk"]["beats"]


def hurricane(outlet_ago, *, title="Hurricane Zeta makes landfall near Cape Marlow as Category 4", **kw):
    """Signals for one event: [(outlet, minutes_ago, tier)] -> list[Signal]."""
    return [sig(o, title, ago, tier=tier, market="national", beat="disaster", **kw) for o, ago, tier in outlet_ago]


def run_detect(signals, window=60, now=NOW):
    stories = cluster(signals, OWNERS)
    flagged = detect(stories, window, signals=signals, owners=OWNERS, now=now)
    return stories, flagged


class TestDetectWithSignals:
    def test_three_independent_tier_2_outlets_in_window(self):
        stories, flagged = run_detect(hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2), ("WIS", 20, 2)]))
        assert flagged == stories and len(flagged) == 1
        s = flagged[0]
        assert s.breaking is True
        assert s.beat == "disaster"
        assert "breaking" in s.risk_flags

    def test_two_outlets_is_not_enough(self):
        _, flagged = run_detect(hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2)]))
        assert flagged == []

    def test_same_owner_group_does_not_count_twice(self):
        _, flagged = run_detect(hurricane([("WLTX", 30, 2), ("WLTX 19", 25, 2), ("Associated Press", 20, 2)]))
        assert flagged == []

    def test_syndicated_copies_do_not_count_twice(self):
        sigs = hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2)])
        sigs += hurricane([("The State", 20, 2)], raw={"syndicated_from": "Associated Press"})
        _, flagged = run_detect(sigs)
        assert flagged == []

    def test_tier_3_and_4_outlets_do_not_count(self):
        _, flagged = run_detect(hurricane([("Associated Press", 30, 2), ("WLTX", 25, 3),
                                           ("WIS", 20, 3), ("Random Blog", 15, 4)]))
        assert flagged == []

    def test_outside_the_window_does_not_count(self):
        sigs = hurricane([("Associated Press", 200, 2), ("WLTX", 190, 2), ("WIS", 180, 2)])
        assert run_detect(sigs, window=60)[1] == []
        assert len(run_detect(sigs, window=240)[1]) == 1

    def test_only_signals_inside_the_window_are_counted(self):
        sigs = hurricane([("Associated Press", 300, 2), ("WLTX", 25, 2), ("WIS", 20, 2)])
        assert run_detect(sigs)[1] == []                      # one old, two fresh

    def test_untimed_signals_are_not_counted(self):
        sigs = hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2), ("WIS", None, 2)])
        assert run_detect(sigs)[1] == []

    def test_official_confirmation_lowers_the_bar_to_two(self):
        sigs = hurricane([("FEMA", 30, 1), ("Associated Press", 25, 2)])
        stories, flagged = run_detect(sigs)
        assert stories[0].official_confirmation and len(flagged) == 1

    def test_official_alone_is_not_enough(self):
        assert run_detect(hurricane([("FEMA", 30, 1)]))[1] == []

    def test_official_confirmation_from_before_the_window_still_counts(self):
        sigs = hurricane([("FEMA", 400, 1), ("Associated Press", 25, 2), ("WLTX", 20, 2)])
        assert len(run_detect(sigs)[1]) == 1

    def test_two_outlets_without_official_is_not_enough(self):
        stories, flagged = run_detect(hurricane([("Associated Press", 30, 2), ("Reuters", 25, 2)]))
        assert not stories[0].official_confirmation and flagged == []

    def test_event_class_must_match(self):
        sigs = hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2), ("WIS", 20, 2)],
                         title="City Council approves Riverbend Park budget amendment")
        stories, flagged = run_detect(sigs)
        assert flagged == [] and stories[0].breaking is False and stories[0].beat == "disaster"   # untouched

    def test_beat_is_replaced_by_the_event_class(self):
        sigs = hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2), ("WIS", 20, 2)],
                         title="Supreme Court strikes down the state law")
        for s in sigs:
            s.beat = "public_safety"
        stories, flagged = run_detect(sigs)
        assert flagged[0].beat == "scotus"

    def test_returns_only_the_flagged_stories_in_input_order(self):
        breaking_sigs = hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2), ("WIS", 20, 2)])
        quiet = [sig("The State", "Taproom plans second location", 15, market="national")]
        stories, flagged = run_detect(quiet + breaking_sigs)
        assert len(stories) == 2 and len(flagged) == 1
        assert flagged[0].headline.startswith("Hurricane")
        assert [s.breaking for s in stories if s not in flagged] == [False]

    def test_idempotent(self):
        sigs = hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2), ("WIS", 20, 2)])
        stories, first = run_detect(sigs)
        again = detect(stories, 60, signals=sigs, owners=OWNERS, now=NOW)
        assert len(again) == 1
        assert stories[0].risk_flags.count("breaking") == 1

    def test_existing_risk_flags_are_kept(self):
        sigs = hurricane([("Associated Press", 30, 2), ("WLTX", 25, 2), ("WIS", 20, 2)],
                         title="Mass shooting at stadium, victims taken to hospital")
        stories, flagged = run_detect(sigs)
        assert flagged[0].beat == "attack_or_attempt"
        assert {"crime", "victim", "breaking"} <= set(flagged[0].risk_flags)

    def test_loads_owners_from_config_when_not_given(self):
        sigs = hurricane([("Associated Press", 30, 2), ("NBC News", 25, 2), ("CBS News", 20, 2)])
        stories = cluster(sigs, config.load_owners())
        assert len(detect(stories, 60, signals=sigs, now=NOW)) == 1

    def test_empty_inputs(self):
        assert detect([], owners=OWNERS, now=NOW) == []


class TestDetectWithoutSignals:
    """Story fields only: cluster()'s first-hour velocity stands in, tiers are assumed 1-2."""

    def test_fast_story_is_flagged(self):
        s = story(headline="Hurricane Zeta makes landfall", independent_outlets=4, velocity=4.0, first_seen=ts(30))
        assert detect([s], owners=OWNERS, now=NOW) == [s] and s.breaking

    def test_slow_story_is_not(self):
        s = story(headline="Hurricane Zeta makes landfall", independent_outlets=4, velocity=2.0, first_seen=ts(30))
        assert detect([s], owners=OWNERS, now=NOW) == []

    def test_stale_story_is_not(self):
        s = story(headline="Hurricane Zeta makes landfall", independent_outlets=6, velocity=6.0, first_seen=ts(5 * 60))
        assert detect([s], owners=OWNERS, now=NOW) == []

    def test_official_confirmation_needs_two(self):
        base = dict(headline="Hurricane Zeta makes landfall", first_seen=ts(30), official_confirmation=True)
        assert detect([story(independent_outlets=2, velocity=2.0, **base)], owners=OWNERS, now=NOW)
        assert not detect([story(independent_outlets=1, velocity=1.0, **base)], owners=OWNERS, now=NOW)

    def test_summary_is_classified_too(self):
        s = story(headline="Developing story near the capital", summary="Gunman reported at the plaza.",
                  independent_outlets=3, velocity=3.0, first_seen=ts(10))
        assert detect([s], owners=OWNERS, now=NOW) == [s] and s.beat == "attack_or_attempt"

    def test_window_scales_velocity(self):
        s = story(headline="Hurricane Zeta makes landfall", independent_outlets=6, velocity=6.0, first_seen=ts(20))
        assert detect([s], 30, owners=OWNERS, now=NOW)            # 6/h over 30 min = 3
        s2 = story(headline="Hurricane Zeta makes landfall", independent_outlets=6, velocity=4.0, first_seen=ts(20))
        assert not detect([s2], 30, owners=OWNERS, now=NOW)       # 4/h over 30 min = 2

    def test_unparseable_first_seen_is_not_flagged(self):
        s = story(headline="Hurricane Zeta makes landfall", independent_outlets=5, velocity=5.0, first_seen="")
        assert detect([s], owners=OWNERS, now=NOW) == []


def test_detect_on_fixture_national_market():
    owners = config.load_owners()
    sigs = fixtures.sample_signals("national", now=NOW)
    stories = cluster(sigs, owners)
    flagged = detect(stories, 60, signals=sigs, owners=owners, now=NOW)
    assert [s.beat for s in flagged] == ["disaster"]
    assert "Hurricane" in flagged[0].headline and flagged[0].official_confirmation
    assert sum(s.breaking for s in stories) == 1             # the routine SCOTUS item is not breaking


@pytest.mark.parametrize("market", ["columbia-sc", "los-angeles", "new-york", "chicago"])
def test_local_fixture_news_is_not_breaking(market):
    owners = config.load_owners()
    sigs = fixtures.sample_signals(market, now=NOW)
    assert detect(cluster(sigs, owners), 60, signals=sigs, owners=owners, now=NOW) == []


# ================================================================ assignment
SHOWS = {
    "local-daily": {"id": "local-daily", "market": "columbia-sc", "lane": "standard",
                    "beats": ["government", "public_safety", "weather"], "max_stories": 2, "enabled": True},
    "la-daily": {"id": "la-daily", "market": "los-angeles", "lane": "standard",
                 "beats": ["government", "public_safety"], "max_stories": 3},
    "la-courts": {"id": "la-courts", "market": "los-angeles", "lane": "strict", "max_stories": 4,
                  "beats": ["criminal_court", "civil_court", "federal_court", "da_press"]},
    "breaking": {"id": "breaking", "market": "national", "lane": "breaking", "beats": list(BREAKING_BEATS)},
    "tracker": {"id": "tracker", "market": "national", "lane": "strict", "beats": ["tracked_cases"]},
    "cold-cases": {"id": "cold-cases", "market": "national", "lane": "strict", "beats": ["cold_case"]},
    "off": {"id": "off", "market": "columbia-sc", "lane": "standard", "beats": ["government"], "enabled": False},
}


def ids(stories):
    return [s.id for s in stories]


class TestAssignRouting:
    def test_routes_by_market_and_beat(self):
        a = story(id="sty_a", market="columbia-sc", beat="government")
        b = story(id="sty_b", market="los-angeles", beat="government")
        c = story(id="sty_c", market="columbia-sc", beat="sports")        # no show covers sports
        out = assign([a, b, c], SHOWS, now=NOW)
        assert ids(out["local-daily"]) == ["sty_a"]
        assert ids(out["la-daily"]) == ["sty_b"]
        assert all(sid not in ids(v) for v in out.values() for sid in ["sty_c"])

    def test_every_enabled_show_is_a_key_and_disabled_shows_are_absent(self):
        out = assign([], SHOWS, now=NOW)
        assert set(out) == set(SHOWS) - {"off"}
        assert all(v == [] for v in out.values())

    def test_disabled_show_gets_nothing(self):
        out = assign([story(market="columbia-sc", beat="government")], SHOWS, now=NOW)
        assert "off" not in out

    def test_shows_may_be_given_as_a_list(self):
        out = assign([story(id="sty_a")], list(SHOWS.values()), now=NOW)
        assert ids(out["local-daily"]) == ["sty_a"]

    def test_real_show_config_registry(self):
        shows = config.load_shows()
        out = assign([story(id="sty_a", market="los-angeles", beat="transit")], shows, now=NOW)
        assert ids(out["la-daily"]) == ["sty_a"]
        assert "nyc-daily" not in out and "chicago-daily" not in out        # wave 1, disabled

    def test_max_stories_caps_each_show_keeping_the_best(self):
        stories = [story(id=f"sty_{i}", market="columbia-sc", beat="government", newsworthiness=n)
                   for i, n in enumerate([40, 90, 70, 10])]
        out = assign(stories, SHOWS, now=NOW)["local-daily"]
        assert ids(out) == ["sty_1", "sty_2"]                                 # cap is 2

    def test_default_cap_when_show_has_none(self):
        stories = [story(id=f"sty_{i}", market="national", beat="tracked_cases", newsworthiness=50 + i)
                   for i in range(8)]
        out = assign(stories, SHOWS, now=NOW)["tracker"]
        assert len(out) == assign_mod.DEFAULT_MAX_STORIES
        assert ids(out)[0] == "sty_7"

    def test_ranks_by_heuristic_score_when_newsworthiness_is_unset(self):
        weak = story(id="sty_weak", independent_outlets=1)
        strong = story(id="sty_strong", independent_outlets=4, official_confirmation=True)
        assert ids(assign([weak, strong], SHOWS, now=NOW)["local-daily"]) == ["sty_strong", "sty_weak"]

    def test_ranking_is_deterministic_on_ties(self):
        a, b = story(id="sty_a", newsworthiness=50), story(id="sty_b", newsworthiness=50)
        assert ids(assign([b, a], SHOWS, now=NOW)["local-daily"]) == ["sty_a", "sty_b"]

    def test_assigned_shows_is_rewritten_to_the_final_routing(self):
        keep = story(id="sty_keep", newsworthiness=90, assigned_shows=["stale"])
        cut_a, cut_b = story(id="sty_x", newsworthiness=50), story(id="sty_y", newsworthiness=10, assigned_shows=["stale"])
        none = story(id="sty_none", beat="sports", assigned_shows=["stale"])
        assign([keep, cut_a, cut_b, none], SHOWS, now=NOW)
        assert keep.assigned_shows == ["local-daily"]
        assert cut_b.assigned_shows == []                                      # dropped by the cap
        assert none.assigned_shows == []


class TestAssignBreaking:
    def test_breaking_lane_takes_flagged_stories_of_any_market(self):
        nat = story(id="sty_nat", market="national", beat="disaster", breaking=True)
        local = story(id="sty_loc", market="columbia-sc", beat="disaster", breaking=True)
        out = assign([nat, local], SHOWS, now=NOW)
        assert sorted(ids(out["breaking"])) == ["sty_loc", "sty_nat"]
        assert nat.assigned_shows == ["breaking"]

    def test_breaking_lane_ignores_unflagged_stories(self):
        calm = story(id="sty_calm", market="national", beat="world", breaking=False)
        assert assign([calm], SHOWS, now=NOW)["breaking"] == []

    def test_breaking_lane_needs_a_matching_beat(self):
        odd = story(id="sty_odd", market="national", beat="sports", breaking=True)
        assert assign([odd], SHOWS, now=NOW)["breaking"] == []

    def test_local_breaking_story_also_reaches_its_market_daily_despite_the_rewritten_beat(self):
        local = story(id="sty_loc", market="columbia-sc", beat="disaster", breaking=True)
        out = assign([local], SHOWS, now=NOW)
        assert ids(out["local-daily"]) == ["sty_loc"]
        assert out["la-daily"] == []
        assert local.assigned_shows == ["local-daily", "breaking"]

    def test_breaking_stories_do_not_bypass_strict_shows(self):
        la = story(id="sty_la", market="los-angeles", beat="disaster", breaking=True)
        out = assign([la], SHOWS, now=NOW)
        assert out["la-courts"] == []
        assert ids(out["la-daily"]) == ["sty_la"]

    def test_detect_then_assign_on_fixtures(self):
        owners, shows = config.load_owners(), config.load_shows()
        stories, signals = [], []
        for market in ("columbia-sc", "los-angeles", "national"):
            sigs = fixtures.sample_signals(market, now=NOW)
            signals += sigs
            stories += cluster(sigs, owners)
        detect(stories, 60, signals=signals, owners=owners, now=NOW)
        out = assign(stories, shows, now=NOW)
        assert [s.beat for s in out["breaking-desk"]] == ["disaster"]
        assert len(out["columbia-daily"]) == 6 and len(out["la-daily"]) <= 7
        assert all(s.market == "columbia-sc" for s in out["columbia-daily"])
        assert ids(out["la-courts"]) and all(s.market == "los-angeles" for s in out["la-courts"])
        assert [s.beat for s in out["case-tracker"]] == ["tracked_cases"]
        assert out["cold-case-files"] == [] and out["history-of-hollywood"] == []


class TestLaneHints:
    def test_court_story_routes_to_the_strict_show_by_beat(self):
        s = story(id="sty_c", market="los-angeles", beat="federal_court", risk_flags=["legal_proceeding"])
        out = assign([s], SHOWS, now=NOW)
        assert ids(out["la-courts"]) == ["sty_c"] and out["la-daily"] == []

    def test_crime_story_with_legal_proceeding_goes_to_daily_and_courts(self):
        s = story(id="sty_c", market="los-angeles", beat="public_safety", risk_flags=["crime", "legal_proceeding"])
        out = assign([s], SHOWS, now=NOW)
        assert ids(out["la-daily"]) == ["sty_c"]
        assert ids(out["la-courts"]) == ["sty_c"]
        assert s.assigned_shows == ["la-daily", "la-courts"]

    def test_crime_without_court_activity_stays_with_the_daily(self):
        s = story(id="sty_c", market="los-angeles", beat="public_safety", risk_flags=["crime"])
        out = assign([s], SHOWS, now=NOW)
        assert ids(out["la-daily"]) == ["sty_c"] and out["la-courts"] == []

    def test_hints_do_not_cross_markets(self):
        s = story(id="sty_c", market="columbia-sc", beat="public_safety", risk_flags=["crime", "legal_proceeding"])
        assert assign([s], SHOWS, now=NOW)["la-courts"] == []

    def test_hints_do_not_feed_tracked_case_or_cold_case_shows(self):
        s = story(id="sty_s", market="national", beat="scotus", risk_flags=["legal_proceeding"])
        out = assign([s], SHOWS, now=NOW)
        assert out["tracker"] == [] and out["cold-cases"] == []

    def test_tracked_case_story_reaches_the_tracker_by_beat(self):
        s = story(id="sty_t", market="national", beat="tracked_cases")
        assert ids(assign([s], SHOWS, now=NOW)["tracker"]) == ["sty_t"]

    def test_lane_hint_values(self):
        assert lane_hint(story(risk_flags=["crime"])) == "strict"
        assert lane_hint(story(risk_flags=["legal_proceeding"])) == "strict"
        assert lane_hint(story(risk_flags=["minor"])) == "strict"
        assert lane_hint(story(beat="criminal_court")) == "strict"
        assert lane_hint(story(beat="tracked_cases")) == "strict"
        assert lane_hint(story(breaking=True, risk_flags=["crime"])) == "breaking"
        assert lane_hint(story(risk_flags=["election"])) is None
        assert lane_hint(story()) is None

    def test_lane_for_escalates_standard_shows_only(self):
        crime = story(risk_flags=["crime"])
        calm = story()
        assert lane_for(SHOWS["local-daily"], [calm]) == "standard"
        assert lane_for(SHOWS["local-daily"], [calm, crime]) == "strict"
        assert lane_for(SHOWS["breaking"], [crime]) == "breaking"
        assert lane_for(SHOWS["la-courts"], [calm]) == "strict"
        assert lane_for({"lane": "archive"}, [crime]) == "archive"
        assert lane_for({}, [calm]) == "standard"
        assert lane_for(SHOWS["local-daily"], []) == "standard"


# ================================================================ conventions
MODEL_ID = re.compile("clau" + r"de-[a-z0-9]", re.IGNORECASE)


@pytest.mark.parametrize("path", sorted(Path(independence.__file__).parent.glob("*.py")))
def test_no_model_ids_in_desk_sources(path):
    assert not MODEL_ID.search(path.read_text(encoding="utf-8")), f"hardcoded model id in {path.name}"


def test_triage_prompt_names_tiers_not_models():
    assert not MODEL_ID.search(score_mod.TRIAGE_SYSTEM)
