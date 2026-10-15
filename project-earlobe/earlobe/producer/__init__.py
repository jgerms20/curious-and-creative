"""Producer: from assigned stories to a script, its AI disclosure and its listing copy.

  research_pack  Stories + sources -> the one dict the writer is allowed to know about the world
  writer         the Opus-tier scriptwriter; every factual line carries claim_ids; rewrites on REWRITE
  disclosure     the spoken end-of-episode AI disclosure (deterministic text, no model)
  copywriter     title, description, show notes and social copy from the GATED script (Sonnet tier)

Typical flow (see earlobe/README.md):
  pack   = build_pack(stories, sources)
  script = write_script(show_id, show_cfg, stories, pack, llm, episode_date=day)   # ends with disclosure
  script, decision, reports = run_trust_loop(script, make_rewriter(...), llm, owners)
  copy   = write_copy(script, show_cfg, llm)                                       # only after PUBLISH
"""
