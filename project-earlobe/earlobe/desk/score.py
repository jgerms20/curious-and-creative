"""Newsworthiness scoring for the Story Desk.

score() is a transparent 0-100 heuristic (no network, no LLM). triage() stores it on each
story and, when an LLM is supplied, blends in a cheap Haiku-tier read of the headlines.

  coverage   up to 30  independent outlets (10 each)
  official   15        any tier 1 signal
  recency    up to 20  linear decay over the clustering window (36h)
  beat       up to 20  position of the story's beat in the show's beat list (first = highest)
  momentum   up to 15  breaking flag, else 3 per independent outlet in the first hour (max 10)
  penalty    -20       sensitive risk flag with thin sourcing (<2 independent outlets, no official)
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from earlobe.desk.cluster import WINDOW_HOURS, parse_time
from earlobe.schemas import RISK_FLAGS, Story

log = logging.getLogger(__name__)

SENSITIVE_FLAGS = frozenset({"crime", "legal_proceeding", "named_private_person", "minor", "victim",
                             "death", "health", "election"})
COVERAGE_PER_OUTLET, COVERAGE_MAX = 10, 30
OFFICIAL_POINTS = 15
RECENCY_MAX = 20
BEAT_MAX, BEAT_NEUTRAL = 20, 10      # neutral when the show lists no beats at all
BREAKING_POINTS, VELOCITY_PER_OUTLET, VELOCITY_MAX = 15, 3, 10
THIN_SOURCING_PENALTY = 20
LLM_WEIGHT = 0.4


def _beat_points(story: Story, show_cfg: dict) -> int:
    beats = list((show_cfg or {}).get("beats") or [])
    if not beats:
        return BEAT_NEUTRAL
    if story.beat not in beats:
        return 0
    return round(BEAT_MAX * (len(beats) - beats.index(story.beat)) / len(beats))


def _recency_points(story: Story, now: datetime) -> int:
    first = parse_time(story.first_seen)
    if first is None:
        return 0
    age_h = max((now - first).total_seconds() / 3600, 0.0)
    return round(RECENCY_MAX * max(0.0, 1 - age_h / WINDOW_HOURS))


def score(story: Story, show_cfg: dict, *, now: datetime | None = None) -> int:
    """Heuristic newsworthiness 0-100 for this story on this show (see module docstring)."""
    now = now or datetime.now(timezone.utc)
    points = min(COVERAGE_MAX, COVERAGE_PER_OUTLET * story.independent_outlets)
    points += OFFICIAL_POINTS if story.official_confirmation else 0
    points += _recency_points(story, now)
    points += _beat_points(story, show_cfg)
    points += BREAKING_POINTS if story.breaking else min(VELOCITY_MAX, round(VELOCITY_PER_OUTLET * story.velocity))
    thin = story.independent_outlets < 2 and not story.official_confirmation
    if thin and SENSITIVE_FLAGS & set(story.risk_flags):
        points -= THIN_SOURCING_PENALTY
    return max(0, min(100, int(points)))


# ---------------------------------------------------------------- optional LLM triage
TRIAGE_SYSTEM = (
    "You are the triage editor of a news audio network's Story Desk. For each story, rate "
    "newsworthiness 0-100 for the given show (audience fit, public impact, timeliness) using only "
    "the headline and summary provided. Add a risk flag only when the text clearly warrants it, "
    "and only from the allowed list. Never invent facts. Return every story exactly once and "
    "copy its id into cluster_key."
)


def _triage_prompt(stories: list[Story], show_cfg: dict) -> str:
    show = {k: (show_cfg or {}).get(k) for k in ("name", "market", "lane", "beats")}
    items = [{"id": s.id, "beat": s.beat, "headline": s.headline, "summary": s.summary,
              "outlets": s.outlets, "independent_outlets": s.independent_outlets,
              "official_confirmation": s.official_confirmation, "risk_flags": s.risk_flags}
             for s in stories]
    return json.dumps({"show": show, "allowed_risk_flags": RISK_FLAGS, "stories": items},
                      ensure_ascii=False)


def _llm_read(stories: list[Story], llm, show_cfg: dict) -> dict[str, dict]:
    """cluster_key -> triage item from a Haiku-tier call; {} if the call fails (heuristic still stands)."""
    try:
        out = llm.structured("story-triage", "haiku", TRIAGE_SYSTEM, _triage_prompt(stories, show_cfg),
                             "StoryTriage", ctx={"stories": [s.to_dict() for s in stories],
                                                 "show_cfg": show_cfg})
    except Exception as e:   # triage is optional: never block the desk on it
        log.warning("story triage skipped: %s", e)
        return {}
    return {i.get("cluster_key"): i for i in (out or {}).get("stories", [])}


def triage(stories: list[Story], llm, show_cfg: dict, *, now: datetime | None = None) -> list[Story]:
    """Set newsworthiness on every story and return them best first.

    Heuristic score always; with an llm, 60% heuristic + 40% LLM rating. The LLM may also add
    risk flags and entities, never remove them, and never rewrites headlines or summaries.
    """
    reads = _llm_read(stories, llm, show_cfg) if llm is not None and stories else {}
    for s in stories:
        item = reads.get(s.id)
        if item:   # merge flags first so they count toward the thin-sourcing penalty
            s.risk_flags = s.risk_flags + [f for f in item.get("risk_flags", [])
                                           if f in RISK_FLAGS and f not in s.risk_flags]
            if not s.entities:
                s.entities = list(item.get("entities") or [])
        value = score(s, show_cfg, now=now)
        if item:
            rating = max(0, min(100, int(item.get("newsworthiness", value))))
            value = round((1 - LLM_WEIGHT) * value + LLM_WEIGHT * rating)
        s.newsworthiness = value
    return sorted(stories, key=lambda s: (-s.newsworthiness, -s.independent_outlets, s.id))
