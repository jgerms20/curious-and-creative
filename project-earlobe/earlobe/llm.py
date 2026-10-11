"""Claude access for every Earlobe agent: structured outputs, web research, cost tracking.

Two calls, both returning a plain dict that matches schemas.JSON_SCHEMAS[kind]:

  structured()  one Messages call with output_config.format (JSON Schema) and adaptive
                thinking. Validated with schemas.validate; one retry with the errors appended.
  research()    Messages call with the web search server tool. Structured output cannot be
                combined with it here, so the model ends with one fenced json block, which we
                parse and validate; on failure a structured() pass repairs it (no new facts).

Every call appends one AgentRun to LLM.runs (tokens, web searches, usd estimate).

Dry-run (LLM(dry_run=True)) never imports the SDK, reads no keys and touches no network: it
returns fixtures.fake(kind, **ctx) and records a zero-cost AgentRun.

Models: only from config.model_for(tier), which reads EARLOBE_MODEL_{OPUS,SONNET,HAIKU}.
The tier's model must support adaptive thinking, output_config.effort and structured outputs.

Optional server-side refusal fallback (off by default): set EARLOBE_FALLBACKS=1 and
EARLOBE_MODEL_FALLBACK=<model id>. Calls then go through the SDK's beta namespace with the
fallbacks parameter. Cost is still estimated at the primary tier's price.
"""
from __future__ import annotations

import json
import os
import re
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any

from earlobe import config
from earlobe.schemas import JSON_SCHEMAS, AgentRun, validate

MAX_TOKENS = 16000
MAX_CONTINUATIONS = 5          # pause_turn re-sends before giving up
FALLBACK_BETA = "server-side-fallback-2026-06-01"
WEB_SEARCH_TOOL = "web_search_20260209"

_JSON_FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)

RESEARCH_SUFFIX = (
    "Research with the web search tool, then finish with ONE fenced ```json block containing a "
    "single JSON object that matches this JSON Schema exactly (no extra keys, nothing after the "
    "block):\n{schema}"
)
RETRY_PROMPT = ("Your JSON did not validate against the schema:\n{errors}\n"
                "Return the corrected JSON object only.")
REPAIR_PROMPT = (
    "The research notes below should end with one JSON object matching the schema, but it "
    "failed to parse or validate.\nProblems:\n{errors}\n\nRebuild the JSON object from the "
    "notes. Use only information present in them: do not add facts, sources or URLs.\n\n"
    "--- NOTES ---\n{text}"
)


class LLMError(RuntimeError):
    """A model call failed in a way the caller should handle (config, truncation, bad output)."""


class LLMRefusal(LLMError):
    """The model declined (stop_reason == "refusal")."""


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _text(resp: Any) -> str:
    """Concatenate the text blocks of a response (thinking / tool blocks are skipped)."""
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def _extract_json(text: str) -> Any:
    """Parse the last fenced json block; fall back to the outermost {...} in the text."""
    fences = _JSON_FENCE.findall(text)
    candidates = [fences[-1]] if fences else []
    if "{" in text and "}" in text:
        candidates.append(text[text.index("{"):text.rindex("}") + 1])
    err: Exception | None = None
    for c in candidates:
        try:
            return json.loads(c.strip())
        except ValueError as e:
            err = e
    raise ValueError(f"no parseable JSON object in model output ({err or 'no braces found'})")


def _parse_and_validate(kind: str, text: str) -> tuple[dict | None, list[str]]:
    """Return (data, []) when text holds valid JSON for kind, else (None-or-data, errors)."""
    try:
        data = _extract_json(text)
    except ValueError as e:
        return None, [str(e)]
    if not isinstance(data, dict):
        return None, [f"top-level JSON must be an object, got {type(data).__name__}"]
    return data, validate(kind, data)


def _usage_counts(usage: Any) -> tuple[int, int, int]:
    """(input_tokens incl. cache reads/writes, output_tokens, web_search_requests)."""
    def n(obj, name):
        return int(getattr(obj, name, 0) or 0)
    inp = n(usage, "input_tokens") + n(usage, "cache_creation_input_tokens") \
        + n(usage, "cache_read_input_tokens")
    searches = n(getattr(usage, "server_tool_use", None), "web_search_requests")
    return inp, n(usage, "output_tokens"), searches


def estimate_usd(tier: str, input_tokens: int, output_tokens: int, searches: int = 0) -> float:
    """USD estimate from config.PRICES.

    Assumed shape: PRICES[tier] = {"input": usd_per_mtok, "output": usd_per_mtok} (aliases
    "in"/"out" accepted) and optional PRICES["web_search"] = usd per search request.
    Missing entries count as 0 rather than guessing.
    """
    prices = getattr(config, "PRICES", None) or {}
    t = prices.get(tier) or {}
    if isinstance(t, (tuple, list)) and len(t) >= 2:
        t = {"input": t[0], "output": t[1]}
    p_in = float(t.get("input", t.get("in", 0.0)))
    p_out = float(t.get("output", t.get("out", 0.0)))
    per_search = prices.get("web_search", 0.0)
    per_search = float(per_search) if isinstance(per_search, (int, float)) else 0.0
    return round((input_tokens * p_in + output_tokens * p_out) / 1_000_000 + searches * per_search, 6)


class LLM:
    """Thin, dry-runnable wrapper over the Anthropic Messages API. See module docstring."""

    def __init__(self, dry_run: bool = False, client: Any = None):
        self.dry_run = dry_run
        self.runs: list[AgentRun] = []
        self._client = client          # injectable for tests; built lazily otherwise

    # ------------------------------------------------------------ public API
    def structured(self, agent_id: str, tier: str, system: str, user: str, kind: str,
                   effort: str = "medium", *, ctx: dict | None = None) -> dict:
        """One structured-output call; validated against JSON_SCHEMAS[kind], one retry."""
        _check_kind(kind)
        with self._track(agent_id, tier) as run:
            if self.dry_run:
                return _fake(kind, ctx)
            model = self._model(tier)
            fmt = {"format": {"type": "json_schema", "schema": JSON_SCHEMAS[kind]},
                   "effort": effort}
            messages: list[dict] = [{"role": "user", "content": user}]
            errors: list[str] = []
            for attempt in range(2):
                resp = self._create(run, model, system=system, messages=messages,
                                    output_config=fmt)
                _check_stop(resp)
                text = _text(resp)
                data, errors = _parse_and_validate(kind, text)
                if data is not None and not errors:
                    return data
                messages = messages + [
                    {"role": "assistant", "content": text or "{}"},
                    {"role": "user", "content": RETRY_PROMPT.format(errors=_fmt_errors(errors))},
                ]
            raise LLMError(f"{agent_id}: output failed {kind} validation after retry: "
                           f"{_fmt_errors(errors)}")

    def research(self, agent_id: str, tier: str, system: str, user: str, kind: str,
                 max_searches: int = 10, *, effort: str = "medium",
                 ctx: dict | None = None) -> dict:
        """Web-search call whose final text ends in a json block for JSON_SCHEMAS[kind]."""
        _check_kind(kind)
        with self._track(agent_id, tier) as run:
            if self.dry_run:
                return _fake(kind, ctx)
            model = self._model(tier)
            tools = [{"type": WEB_SEARCH_TOOL, "name": "web_search", "max_uses": max_searches}]
            full_system = f"{system}\n\n" + RESEARCH_SUFFIX.format(
                schema=json.dumps(JSON_SCHEMAS[kind]))
            text = self._research_turn(run, model, full_system, user, tools, effort)
            data, errors = _parse_and_validate(kind, text)
            if data is not None and not errors:
                return data
        # Outside the research run so the repair is logged as its own AgentRun.
        return self.structured(
            f"{agent_id}.repair", tier, system,
            REPAIR_PROMPT.format(errors=_fmt_errors(errors), text=text), kind, effort="low")

    # ------------------------------------------------------------ internals
    def _research_turn(self, run: AgentRun, model: str, system: str, user: str,
                       tools: list, effort: str) -> str:
        """Run one research turn, re-sending on pause_turn. Returns all text of the turn."""
        first = [{"role": "user", "content": user}]
        messages, carried, texts = first, [], []
        for _ in range(MAX_CONTINUATIONS + 1):
            resp = self._create(run, model, system=system, messages=messages, tools=tools,
                                output_config={"effort": effort})
            _check_stop(resp)
            texts.append(_text(resp))
            if resp.stop_reason != "pause_turn":
                return "".join(texts)
            # The trailing server_tool_use block tells the API to resume; no extra user turn.
            carried = carried + list(resp.content)
            messages = first + [{"role": "assistant", "content": carried}]
        raise LLMError(f"still paused after {MAX_CONTINUATIONS} continuations")

    def _create(self, run: AgentRun, model: str, *, system: str, messages: list,
                output_config: dict, tools: list | None = None):
        kwargs: dict[str, Any] = dict(
            model=model, max_tokens=MAX_TOKENS, system=system, messages=messages,
            thinking={"type": "adaptive"}, output_config=output_config)
        if tools:
            kwargs["tools"] = tools
        fallback = _fallback_model()
        if fallback:
            resp = self.client.beta.messages.create(
                betas=[FALLBACK_BETA], fallbacks=[{"model": fallback}], **kwargs)
        else:
            resp = self.client.messages.create(**kwargs)
        inp, out, searches = _usage_counts(resp.usage)
        run.input_tokens += inp
        run.output_tokens += out
        run.web_searches += searches
        return resp

    @staticmethod
    def _model(tier: str) -> str:
        model = config.model_for(tier)
        if not model:
            raise LLMError(f"No model configured for the {tier} tier. Set the environment "
                           f"variable EARLOBE_MODEL_{tier.upper()} (or run with --dry-run).")
        return model

    @property
    def client(self):
        if self._client is None:
            import anthropic  # lazy: dry-run needs neither the SDK nor a key
            self._client = anthropic.Anthropic()
        return self._client

    @contextmanager
    def _track(self, agent_id: str, tier: str):
        """Yield an AgentRun; on exit stamp the finish time and cost, and record it."""
        run = AgentRun(agent_id=agent_id, run_id=f"run_{uuid.uuid4().hex[:12]}",
                       model_tier=tier, started_at=_now())
        try:
            yield run
        except Exception as e:
            run.ok, run.error = False, f"{type(e).__name__}: {e}"
            raise
        finally:
            run.finished_at = _now()
            run.usd_estimate = estimate_usd(tier, run.input_tokens, run.output_tokens,
                                            run.web_searches)
            self.runs.append(run)


# ---------------------------------------------------------------- helpers
def _check_kind(kind: str) -> None:
    if kind not in JSON_SCHEMAS:
        raise LLMError(f"unknown schema kind {kind!r}; known: {', '.join(sorted(JSON_SCHEMAS))}")


def _check_stop(resp: Any) -> None:
    """Fail loudly on refusal / truncation before anyone reads resp.content."""
    reason = getattr(resp, "stop_reason", None)
    if reason == "refusal":
        d = getattr(resp, "stop_details", None)
        detail = " ".join(str(x) for x in (getattr(d, "category", None),
                                           getattr(d, "explanation", None)) if x)
        raise LLMRefusal(f"model refused the request{': ' + detail if detail else ''}")
    if reason == "max_tokens":
        raise LLMError(f"output truncated at max_tokens={MAX_TOKENS}")


def _fmt_errors(errors: list[str]) -> str:
    return "\n".join(f"- {e}" for e in errors) or "- (none)"


def _fake(kind: str, ctx: dict | None) -> dict:
    from earlobe import fixtures  # lazy: owned by another module
    return fixtures.fake(kind, **(ctx or {}))


def _fallback_model() -> str | None:
    """Fallback model id when EARLOBE_FALLBACKS=1 (default off); the id comes from env only."""
    if os.environ.get("EARLOBE_FALLBACKS", "") != "1":
        return None
    model = os.environ.get("EARLOBE_MODEL_FALLBACK", "").strip()
    if not model:
        raise LLMError("EARLOBE_FALLBACKS=1 needs EARLOBE_MODEL_FALLBACK set to a model id.")
    return model
