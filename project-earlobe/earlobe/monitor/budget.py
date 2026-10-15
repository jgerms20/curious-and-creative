"""Daily spend caps: stop a show before a runaway loop gets expensive.

within_budget(store, show_id, day) is True while BOTH hold for the UTC day:
  * the show's estimated spend (sum of AgentRun.usd_estimate logged for it) is under its cap
  * the network's total is under network_daily_usd, unless the show is on the breaking lane,
    which may keep running until its own cap (config/budgets.yaml says so)

Caps come from config/budgets.yaml. If that file is missing or unreadable the built-in DEFAULTS
below apply, so a bad checkout never means "no limit". Costs are estimates (config.PRICES); an
agent run only counts once it has been logged with store.log_run(run, show_id).
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timezone

import yaml

from earlobe import config

log = logging.getLogger(__name__)

DEFAULTS = {
    "network_daily_usd": 60.0,
    "default_daily_usd": 5.0,
    "warn_fraction": 0.8,
    "shows": {"columbia-daily": 5.0, "la-daily": 6.0, "breaking-desk": 10.0, "la-courts": 6.0,
              "case-tracker": 8.0, "cold-case-files": 8.0, "history-of-hollywood": 6.0,
              "nyc-daily": 5.0, "chicago-daily": 5.0},
}


def load() -> dict:
    """budgets.yaml with every key filled in (DEFAULTS when the file is missing or broken)."""
    try:
        data = config.load_budgets()
    except FileNotFoundError:
        data = None
    except (yaml.YAMLError, OSError) as e:
        log.error("config/budgets.yaml unreadable (%s); using built-in caps", e)
        data = None
    if not isinstance(data, dict):
        return {**DEFAULTS, "shows": dict(DEFAULTS["shows"])}
    out = {key: float(data.get(key, DEFAULTS[key]))
           for key in ("network_daily_usd", "default_daily_usd", "warn_fraction")}
    out["shows"] = {str(k): float(v) for k, v in (data.get("shows") or {}).items()}
    return out


def cap_for(show_id: str, budgets: dict | None = None) -> float:
    """The show's daily cap in USD (default_daily_usd for a show with no entry)."""
    budgets = budgets or load()
    return float(budgets["shows"].get(show_id, budgets["default_daily_usd"]))


def day_key(day: date | datetime | str | None = None) -> str:
    """'YYYY-MM-DD' in UTC for a date, datetime, ISO string, or None (today)."""
    if day is None:
        day = datetime.now(timezone.utc)
    if isinstance(day, datetime):
        day = day.astimezone(timezone.utc) if day.tzinfo else day
    return day[:10] if isinstance(day, str) else day.strftime("%Y-%m-%d")


def _is_breaking(show_id: str) -> bool:
    try:
        return config.load_shows().get(show_id, {}).get("lane") == "breaking"
    except (FileNotFoundError, yaml.YAMLError, OSError):
        return False


def status(store, show_id: str, day: date | datetime | str | None = None) -> dict:
    """Spend against caps for one show and day: spent, cap, network_spent, network_cap, warn, within."""
    budgets, key = load(), day_key(day)
    spent, total = store.spend(show_id, key), store.spend(None, key)
    cap, network_cap = cap_for(show_id, budgets), budgets["network_daily_usd"]
    network_ok = total < network_cap or _is_breaking(show_id)
    return {"show_id": show_id, "day": key, "spent": spent, "cap": cap,
            "network_spent": total, "network_cap": network_cap,
            "warn": spent >= cap * budgets["warn_fraction"],
            "within": spent < cap and network_ok}


def within_budget(store, show_id: str, day: date | datetime | str | None = None) -> bool:
    """True if the show may spend more today. Logs a warning near the cap and an error over it."""
    s = status(store, show_id, day)
    if not s["within"]:
        log.error("%s is over budget for %s: $%.2f of $%.2f (network $%.2f of $%.2f)", show_id,
                  s["day"], s["spent"], s["cap"], s["network_spent"], s["network_cap"])
    elif s["warn"]:
        log.warning("%s is near its budget for %s: $%.2f of $%.2f", show_id, s["day"], s["spent"],
                    s["cap"])
    return s["within"]
