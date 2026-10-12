"""Kill switch: stop one show, or the whole network, without touching code.

killed(show_id) is True when EITHER source says so:

  env EARLOBE_KILL       "all", or comma-separated show ids ("la-courts,cold-case-files")
  config/killswitch.yaml all: true, or shows: [ids]; `reason` is free text for the trust log

It is OR, never "env overrides file": a kill switch must fail safe, so setting the env var to
something else cannot un-kill what the committed file kills. To resume, clear both.

killed() with no show id asks "is the whole network halted?". A partial list answers False
there; ask per show. A missing killswitch.yaml means "not killed". An unreadable one (bad YAML)
halts everything, because publishing wrongly costs more than pausing. Dry runs ignore the
switch; that is the pipeline's call, not this module's.
"""
from __future__ import annotations

import os

import yaml

from earlobe import config

ENV_VAR = "EARLOBE_KILL"
_TRUE = {"true", "yes", "on", "1", "all"}


def _truthy(value) -> bool:
    return value is True or str(value).strip().lower() in _TRUE


def _ids(value) -> set[str]:
    """Show ids from a YAML list or a comma-separated string, lower-cased."""
    if isinstance(value, str):
        value = value.split(",")
    return {str(v).strip().lower() for v in (value or []) if str(v).strip()}


def _file() -> dict:
    try:
        data = config.load_killswitch()
    except FileNotFoundError:
        return {}
    except (yaml.YAMLError, OSError):
        data = None
    if not isinstance(data, dict):
        return {"all": True, "reason": "config/killswitch.yaml is unreadable; halting to be safe"}
    return data


def kill_reason(show_id: str | None = None) -> str | None:
    """Why the show (or, with no id, the network) is halted; None when it may run."""
    env = _ids(os.environ.get(ENV_VAR, ""))
    sid = (show_id or "").strip().lower()
    if "all" in env:
        return f"{ENV_VAR}=all"
    if sid and sid in env:
        return f"{ENV_VAR} lists {show_id}"
    data = _file()
    why = str(data.get("reason") or "").strip()
    if _truthy(data.get("all")):
        return why or "config/killswitch.yaml: all"
    if sid and sid in _ids(data.get("shows")):
        return why or f"config/killswitch.yaml lists {show_id}"
    return None


def killed(show_id: str | None = None) -> bool:
    """True if the show (or, with no id, the whole network) is halted."""
    return kill_reason(show_id) is not None
