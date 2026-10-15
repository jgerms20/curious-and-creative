"""Breaking-news detection.

A story is flagged breaking when BOTH hold:
  speed   at least 3 independent tier 1-2 outlets inside the window, OR official confirmation
          plus at least 2 independent tier 1-2 outlets (the official source counts as one)
  class   its headline/summary reads as one of the breaking-desk event classes (keyword rules)

"Inside the window" means published in the last `window_minutes` before `now`. Pass the
`signals` the stories were clustered from for the exact, tier-aware count. Without them
detect() falls back to Story fields only (the first-hour velocity from cluster()) and has to
assume every counted outlet is tier 1-2.

Flagged stories get story.breaking = True, story.beat = the event class (so the breaking
show's beat list matches) and a "breaking" risk flag. The keyword classifier favors precision:
a missed breaking story is recovered on the next scan, a false one costs a gated episode.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from earlobe.desk.cluster import VELOCITY_MINUTES, parse_time
from earlobe.desk.independence import independent_count
from earlobe.schemas import Signal, Story

BREAKING_BEATS = ("major_death", "attack_or_attempt", "disaster", "scotus", "federal_government",
                  "space", "sports_mega", "business_mega", "world")   # = breaking-desk beats in shows.yaml
MIN_OUTLETS = 3              # independent tier 1-2 outlets inside the window
MIN_OUTLETS_WITH_OFFICIAL = 2
MAX_TIER = 2

_DEATH = r"dies|died|dead|death of|passes away|passed away|dead at|found dead"
_PROMINENT = (r"president|prime minister|chancellor|senator|congress(?:man|woman)|justice|governor|pope|king"
              r"|queen|prince|princess|emperor|legend|icon|laureate|astronaut|olympian|actor|actress"
              r"|singer|rapper|musician|billionaire")

# class -> rules. A rule is a regex, or a tuple of regexes that must ALL match. The class with
# the most matching rules wins (ties: BREAKING_BEATS order). Every regex matches whole words.
_RULES: dict[str, list] = {
    "major_death": [(_DEATH, _PROMINENT)],   # a death alone is not "major"; it needs a prominent figure
    "attack_or_attempt": [r"assassinat\w*", r"gunmen|gunman", r"mass shooting", r"shooting", r"stabbing",
                          r"terror\w*", r"bomb(?:ing|er|ings)?\b", r"hostages?", r"(?<!heart )attacks?\b",
                          r"attempt(?:ed)? (?:on|to kill|to assassinate)"],
    "disaster": [r"hurricane|typhoon|cyclone|tornado", r"earthquake|tsunami|volcan\w*|eruption",
                 r"wildfires?", r"landfall", r"death toll", r"state of emergency", r"plane crash|air crash",
                 r"derail\w*", r"(?:bridge|building|dam) collapse\w*", r"mass casualt\w*", r"magnitude \d"],
    "scotus": [r"supreme court", r"scotus", r"justices"],
    "federal_government": [r"white house", r"congress(?:ional)?\b", r"u\.s\. senate|senate (?:passes|votes|confirms)",
                           r"house (?:passes|votes)", r"executive order", r"pentagon",
                           r"government shutdown|shutdown", r"impeach\w*", r"national guard",
                           r"president(?:ial)? (?:signs|vetoes|orders|announces|fires|pardons|address)"],
    "space": [r"nasa", r"spacex", r"rockets?\b", r"spacecraft", r"astronauts?", r"space station",
              r"lunar|moon landing", r"\bmars\b", r"satellites?", r"launch window"],
    "sports_mega": [r"super bowl", r"world series", r"world cup", r"olympic\w*", r"nba finals",
                    r"stanley cup", r"march madness|final four", r"wimbledon", r"champions league",
                    r"ryder cup"],
    "business_mega": [r"acquisitions?|acquires|merger|merges", r"bankruptcy|chapter 11", r"\bipo\b",
                      r"market crash|stocks? (?:plunge|tumble|crash)", r"federal reserve",
                      r"rate (?:cut|hike)", r"\$\s?\d[\d.,]*\s?(?:billion|trillion)"],
    "world": [r"invasion|invades", r"\bcoup\b", r"declares war|\bwar\b", r"cease-?fire", r"missiles?\b",
              r"air ?strikes?", r"nuclear", r"peace (?:deal|talks)", r"\bsummit\b", r"sanctions",
              r"prime minister", r"\bnato\b", r"security council"],
}


def _compile(rule) -> list[re.Pattern]:
    parts = (rule,) if isinstance(rule, str) else rule
    return [re.compile(rf"(?<!\w)(?:{p})(?!\w)", re.IGNORECASE) for p in parts]


_COMPILED = {beat: [_compile(r) for r in rules] for beat, rules in _RULES.items()}


def classify(text: str) -> str | None:
    """Breaking event class for a headline/summary, or None if no class fits."""
    best, best_hits = None, 0
    for beat in BREAKING_BEATS:
        hits = sum(all(p.search(text or "") for p in rule) for rule in _COMPILED[beat])
        if hits > best_hits:
            best, best_hits = beat, hits
    return best


def _recent_outlets(story: Story, signals: dict[str, Signal], owners: dict,
                    window_minutes: int, now: datetime) -> int:
    """Independent tier 1-2 outlets for this story inside the window."""
    members = [signals[i] for i in story.signal_ids if i in signals]
    if members:
        start = now - timedelta(minutes=window_minutes)
        recent = [s for s in members if (t := parse_time(s.published_at)) and t >= start]
        return independent_count(recent, owners, max_tier=MAX_TIER)
    # No signals to inspect: first-hour velocity stands in, but only while that hour still
    # overlaps the window; tiers are unknown, so every counted outlet is assumed tier 1-2.
    first = parse_time(story.first_seen)
    if first is None or now - first > timedelta(minutes=VELOCITY_MINUTES + window_minutes):
        return 0
    count = story.velocity * window_minutes / VELOCITY_MINUTES
    return min(story.independent_outlets, int(count + 0.5))


def detect(stories: list[Story], window_minutes: int = 60, *, signals: list[Signal] | None = None,
           owners: dict | None = None, now: datetime | None = None) -> list[Story]:
    """Flag breaking stories in place and return just those, in input order."""
    if owners is None:
        from earlobe import config
        owners = config.load_owners()
    now = now or datetime.now(timezone.utc)
    by_id = {s.id: s for s in signals or []}
    flagged = []
    for story in stories:
        beat = classify(f"{story.headline}. {story.summary}")
        if beat is None:
            continue
        outlets = _recent_outlets(story, by_id, owners, window_minutes, now)
        if outlets >= MIN_OUTLETS or (story.official_confirmation and outlets >= MIN_OUTLETS_WITH_OFFICIAL):
            story.breaking = True
            story.beat = beat
            if "breaking" not in story.risk_flags:
                story.risk_flags = story.risk_flags + ["breaking"]
            flagged.append(story)
    return flagged
