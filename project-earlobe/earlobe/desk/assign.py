"""Assignment: which stories go to which show.

Routing rules, per enabled show:
  breaking lane   any market; only stories flagged breaking whose beat is in the show's beats
  other lanes     the story's market must equal the show's market, and its beat must be in the
                  show's beats. Standard-lane shows also take their market's breaking stories
                  (detect() replaces the beat with the event class, so the beat alone would miss them)
  lane hints      a crime/court story is also routed to the strict court shows of its market
                  (shows whose beats include court beats) when it carries the legal_proceeding flag
                  or its beat is one of the show's beats

Per show the stories are ranked (newsworthiness, else the show-specific heuristic score) and cut
to max_stories. story.assigned_shows is rewritten to the final routing.

lane_hint()/lane_for() expose the strictness a story calls for, so a show that is normally
standard can run an episode in the strict lane when it carries crime or court material.
"""
from __future__ import annotations

from datetime import datetime

from earlobe.desk.score import score
from earlobe.schemas import Story

DEFAULT_MAX_STORIES = 5
STRICT_FLAGS = frozenset({"crime", "legal_proceeding", "minor", "victim"})
COURT_BEATS = frozenset({"criminal_court", "civil_court", "federal_court", "da_press"})
STRICT_BEATS = COURT_BEATS | {"tracked_cases", "cold_case"}


def lane_hint(story: Story) -> str | None:
    """'breaking' for breaking stories, 'strict' for crime/court material, else None."""
    if story.breaking:
        return "breaking"
    if STRICT_FLAGS & set(story.risk_flags) or story.beat in STRICT_BEATS:
        return "strict"
    return None


def lane_for(show_cfg: dict, stories: list[Story]) -> str:
    """Lane an episode should run in: the show's own lane, escalated standard -> strict by hints."""
    lane = (show_cfg or {}).get("lane", "standard")
    if lane == "standard" and any(lane_hint(s) == "strict" for s in stories):
        return "strict"
    return lane


def _matches(story: Story, cfg: dict) -> bool:
    lane, beats = cfg.get("lane", "standard"), cfg.get("beats") or []
    if lane == "breaking":
        return story.breaking and story.beat in beats
    if story.market != cfg.get("market"):
        return False
    return story.beat in beats or (story.breaking and lane == "standard")


def _strict_court_match(story: Story, cfg: dict) -> bool:
    """Lane hint: crime/court story, same market, strict show that covers courts."""
    beats = cfg.get("beats") or []
    if cfg.get("lane") != "strict" or story.market != cfg.get("market") or not COURT_BEATS & set(beats):
        return False
    return lane_hint(story) == "strict" and (story.beat in beats or "legal_proceeding" in story.risk_flags)


def _items(shows) -> list[tuple[str, dict]]:
    pairs = shows.items() if isinstance(shows, dict) else [(c["id"], c) for c in shows]
    return [(sid, cfg or {}) for sid, cfg in pairs if (cfg or {}).get("enabled", True)]


def assign(stories: list[Story], shows: dict, *, now: datetime | None = None) -> dict[str, list[Story]]:
    """Route stories to enabled shows; returns {show_id: ranked stories} with every enabled show present."""
    routed: dict[str, list[Story]] = {}
    for show_id, cfg in _items(shows):
        picked = [s for s in stories if _matches(s, cfg) or _strict_court_match(s, cfg)]
        picked.sort(key=lambda s: (-(s.newsworthiness or score(s, cfg, now=now)), -s.independent_outlets, s.id))
        routed[show_id] = picked[: cfg.get("max_stories") or DEFAULT_MAX_STORIES]
    for s in stories:
        s.assigned_shows = [sid for sid, picked in routed.items() if any(p is s for p in picked)]
    return routed
