"""Paths, YAML config loaders, model-tier lookup and the price table.

Model IDs are never written in the repo. They come only from the environment
(EARLOBE_MODEL_OPUS / _SONNET / _HAIKU) through model_for(tier), which returns
None when a tier is unset (the LLM wrapper then refuses a live call and tells
you which variable to set; dry runs need no model at all).

A local .env (gitignored) is read once at import. It fills in variables that
are not already set, so real environment variables always win.
"""
from __future__ import annotations

import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent       # project-earlobe/
CONFIG_DIR = ROOT / "config"


def load_env(path: Path | None = None) -> None:
    """Fill os.environ from a KEY=VALUE file (default ROOT/.env). Never overrides, skips blanks."""
    path = path or ROOT / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.removeprefix("export ").partition("=")
        value = value.strip().strip("'\"")
        if key.strip() and value:
            os.environ.setdefault(key.strip(), value)


load_env()

DATA_DIR = Path(os.environ.get("EARLOBE_DATA_DIR") or ROOT / "data")   # gitignored; see data_dir()


def data_dir(*parts: str) -> Path:
    """DATA_DIR (or a subfolder of it), created on demand."""
    path = DATA_DIR.joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


# ---------------------------------------------------------------- models and prices
TIERS = ("opus", "sonnet", "haiku")


def model_for(tier: str) -> str | None:
    """Model ID for a tier from env EARLOBE_MODEL_<TIER>; None if unset."""
    if tier not in TIERS:
        raise ValueError(f"unknown model tier {tier!r}; expected one of {TIERS}")
    return os.environ.get(f"EARLOBE_MODEL_{tier.upper()}") or None


# USD per million tokens. list prices as of Oct 2026; verify
PRICES = {
    "opus":   {"in": 4.0, "out": 20.0},
    "sonnet": {"in": 2.0, "out": 10.0},
    "haiku":  {"in": 0.10, "out": 0.50},
}
WEB_SEARCH_USD_PER_1K = 10.0     # server-side web search, per 1,000 searches
CACHE_READ_MULT = 0.1            # cached input tokens cost this fraction of the input price
BATCH_DISCOUNT = 0.5             # batch API multiplier on token cost


def estimate_usd(tier: str, input_tokens: int, output_tokens: int, web_searches: int = 0,
                 cache_read_tokens: int = 0, batch: bool = False) -> float:
    """Rough USD cost of one call. input_tokens excludes cache reads (they are billed separately)."""
    p = PRICES[tier]
    tokens = (input_tokens * p["in"] + cache_read_tokens * p["in"] * CACHE_READ_MULT
              + output_tokens * p["out"]) / 1_000_000
    if batch:
        tokens *= BATCH_DISCOUNT
    return round(tokens + web_searches * WEB_SEARCH_USD_PER_1K / 1000, 6)


# ---------------------------------------------------------------- YAML loaders
def load_yaml(name: str) -> dict:
    """Read config/<name>.yaml (name may include a subfolder, e.g. 'sources/national')."""
    with (CONFIG_DIR / f"{name}.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _with_ids(mapping: dict) -> dict:
    return {key: {"id": key, **(cfg or {})} for key, cfg in (mapping or {}).items()}


def load_shows(enabled_only: bool = False) -> dict[str, dict]:
    """show_id -> config (each also carries its own 'id')."""
    shows = _with_ids(load_yaml("shows").get("shows"))
    return {k: v for k, v in shows.items() if v.get("enabled", True)} if enabled_only else shows


def load_markets() -> dict[str, dict]:
    """market_id -> config (each also carries its own 'id')."""
    return _with_ids(load_yaml("markets").get("markets"))


def load_voices() -> dict:
    """Whole voices.yaml: engine, default_tts_model_env, personas{}, disclosure_voice."""
    return load_yaml("voices")


def load_owners() -> dict:
    """Whole owners.yaml: wires[] and groups{owner: [outlet names/domains]}."""
    return load_yaml("owners")


def load_sources(market: str) -> list[dict]:
    """Feed entries for a market: [{outlet, url, kind, tier, beats, verified}, ...]. [] if no file."""
    path = CONFIG_DIR / "sources" / f"{Path(market).name}.yaml"
    if not path.is_file():
        return []
    with path.open(encoding="utf-8") as f:
        return list((yaml.safe_load(f) or {}).get("feeds") or [])


def load_evergreen(show_id: str) -> dict:
    """config/evergreen/<show>.yaml: the topic queue and research brief of an archive or cold-case show.

    Returns {agent, tier, max_searches, brief, topics: [{id, title, angle}]}. Raises FileNotFoundError
    (with the path) when the show has no queue.
    """
    path = CONFIG_DIR / "evergreen" / f"{Path(show_id).name}.yaml"
    if not path.is_file():
        raise FileNotFoundError(f"no evergreen topic queue for {show_id!r}: expected {path}")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_budgets() -> dict:
    """budgets.yaml: network_daily_usd, default_daily_usd, warn_fraction, shows{id: usd}."""
    return load_yaml("budgets")


def load_killswitch() -> dict:
    """killswitch.yaml: all (bool), shows[] (ids), reason."""
    return load_yaml("killswitch")


def voice_id(persona: str) -> str | None:
    """ElevenLabs voice ID for a persona, read from the env var named in voices.yaml."""
    cfg = load_voices().get("personas", {}).get(persona, {})
    return os.environ.get(cfg.get("voice_id_env", "")) or None
