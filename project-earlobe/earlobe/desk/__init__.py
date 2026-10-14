"""Story Desk: turns raw Signals into ranked, routed Stories.

  independence  owner groups and independent-source counting (wires and syndication collapse)
  cluster       Signals -> Stories (title shingles, time window, risk flags, velocity)
  score         heuristic newsworthiness and optional Haiku-tier triage
  breaking      flags breaking stories (speed + event class)
  assign        routes stories to enabled shows (market + beat, max_stories, lane hints)

Typical flow (see earlobe/README.md):
  stories = cluster(signals, owners)
  detect(stories, signals=signals, owners=owners)
  triage(stories, llm, show_cfg)
  assign(stories, shows)
"""
