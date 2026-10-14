"""Monitoring and operations: corrections, re-checks, the kill switch and budgets.

  killswitch.py   killed(show_id) -> bool            stop a show or the whole network, no code change
  budget.py       within_budget(store, show, day)    daily USD cap per show from config/budgets.yaml
  corrections.py  open_correction / apply_correction fix a published episode in the open
  recheck.py      recheck(store, llm, days)          re-verify recent episodes, open corrections

Store kinds these modules read and write (the names the pipeline is expected to use):
  "episode"         Episode dicts          "script"          Script dicts
  "correction"      Correction dicts       "recheck_report"  VerifierReport + episode_id + checked_at

Nothing here makes a network call by itself. recheck() calls the LLM it is handed, so a dry-run
LLM keeps it fully offline.
"""

EPISODE = "episode"
SCRIPT = "script"
CORRECTION = "correction"
RECHECK_REPORT = "recheck_report"
