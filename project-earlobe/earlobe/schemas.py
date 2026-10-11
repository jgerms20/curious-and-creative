"""Earlobe data contracts.

Every agent in the network reads and writes these shapes. The dataclasses are
what the Python engine passes around; JSON_SCHEMAS holds the matching JSON
Schema for each agent's structured output (used for LLM structured outputs and
for validating anything that crosses a boundary: files, the database, the
public trust log). docs/blueprint/json-contracts.md documents the same shapes
for humans — keep the two in sync.

Conventions
  ids        short strings, prefixed by kind: src_, sty_, clm_, ln_, scr_, ep_, cor_
  times      ISO-8601 UTC strings ("2026-10-11T13:00:00Z")
  scores     0-100 integers unless noted
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------- vocabularies
SOURCE_TIERS = {
    1: "primary/official record (court filing, government release, original data, on-record statement)",
    2: "wire service or established newsroom with editorial standards",
    3: "local/specialist outlet, trade press, verified expert",
    4: "aggregator, blog, social post, unverified (never counts toward corroboration alone)",
}
SOURCE_KINDS = ["article", "press_release", "court_record", "official_data", "archive",
                "broadcast", "social", "other"]
CLAIM_TYPES = ["fact", "number", "quote", "attribution", "allegation", "legal_status",
               "prediction", "context"]
RISK_FLAGS = ["crime", "legal_proceeding", "named_private_person", "minor", "victim",
              "health", "election", "death", "breaking", "financial"]
VERIFY_STATUS = ["corroborated", "single_source", "unsupported", "contradicted"]
FACT_RATINGS = ["accurate", "minor_issue", "misleading", "inaccurate", "unverifiable"]
BIAS_TYPES = ["loaded_language", "one_sided", "missing_perspective", "framing", "speculation",
              "sensationalism", "stereotype", "false_balance"]
LEGAL_RISKS = ["naming_minor", "naming_victim", "unproven_allegation", "presumption_of_innocence",
               "privacy", "copyright", "medical", "other"]
SEVERITY = ["low", "medium", "high"]
DECISIONS = ["PUBLISH", "REWRITE", "HOLD", "KILL"]
LANE_POLICIES = ["standard", "strict", "breaking", "archive"]
EPISODE_STATUS = ["draft", "gated", "rendered", "published", "corrected", "retracted", "killed"]


def make_id(prefix: str, *parts: Any) -> str:
    """Deterministic id from content, so re-runs dedupe naturally."""
    h = hashlib.sha1("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:12]
    return f"{prefix}_{h}"


class Contract:
    """Mixin: dict round-tripping for dataclasses (nested lists of contracts included)."""

    def to_dict(self) -> dict:
        return dataclasses.asdict(self)

    def to_json(self, **kw) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, **kw)

    @classmethod
    def from_dict(cls, d: dict):
        hints = {f.name: f for f in dataclasses.fields(cls)}
        kwargs = {}
        for k, v in (d or {}).items():
            if k not in hints:
                continue
            sub = _NESTED.get((cls.__name__, k))
            if sub is not None and isinstance(v, list):
                v = [sub.from_dict(x) if isinstance(x, dict) else x for x in v]
            elif sub is not None and isinstance(v, dict):
                v = sub.from_dict(v)
            kwargs[k] = v
        return cls(**kwargs)


# ---------------------------------------------------------------- sensing
@dataclass
class Source(Contract):
    id: str
    url: str
    outlet: str
    title: str = ""
    published_at: str | None = None
    retrieved_at: str | None = None
    tier: int = 3
    kind: str = "article"
    owner_group: str = ""          # parent company / network; same group = not independent
    syndicated_from: str = ""      # outlet or url this copy was syndicated from (wire copy)
    excerpt: str = ""              # short excerpt or summary in our own words, never full text
    market: str = ""


@dataclass
class Signal(Contract):
    """One raw item a sensor picked up (feed entry, docket entry, press release, search hit)."""
    id: str
    sensor: str                    # agent id of the sensor
    market: str
    beat: str
    title: str
    url: str
    outlet: str
    published_at: str | None = None
    summary: str = ""
    kind: str = "article"
    tier: int = 3
    raw: dict = field(default_factory=dict)


@dataclass
class Story(Contract):
    """A clustered news event, after dedupe — the Story Desk's unit of work."""
    id: str
    market: str
    beat: str
    headline: str
    summary: str
    first_seen: str
    signal_ids: list = field(default_factory=list)
    source_ids: list = field(default_factory=list)
    outlets: list = field(default_factory=list)
    independent_outlets: int = 0
    official_confirmation: bool = False
    newsworthiness: int = 0        # 0-100
    velocity: float = 0.0          # independent outlets per hour over the detector window
    breaking: bool = False
    risk_flags: list = field(default_factory=list)
    entities: list = field(default_factory=list)
    assigned_shows: list = field(default_factory=list)


# ---------------------------------------------------------------- production
@dataclass
class Claim(Contract):
    id: str
    text: str                      # one checkable assertion, as worded in the script
    type: str = "fact"
    line_ids: list = field(default_factory=list)
    source_ids: list = field(default_factory=list)   # writer's sources
    entities: list = field(default_factory=list)
    risk_flags: list = field(default_factory=list)
    attributed: bool = False       # script says who claims it ("police said", "according to")


@dataclass
class ScriptLine(Contract):
    id: str
    speaker: str                   # persona id from config/voices.yaml
    text: str
    claim_ids: list = field(default_factory=list)
    segment: str = "body"          # cold_open | intro | body | kicker | disclosure | outro


@dataclass
class Script(Contract):
    id: str
    show_id: str
    episode_date: str
    title: str
    lines: list = field(default_factory=list)        # [ScriptLine]
    claims: list = field(default_factory=list)       # [Claim]
    sources: list = field(default_factory=list)      # [Source]
    story_ids: list = field(default_factory=list)
    lane_policy: str = "standard"
    revision: int = 0
    notes_for_checkers: str = ""

    def word_count(self) -> int:
        return sum(len(l.text.split()) for l in self.lines)

    def char_count(self) -> int:
        return sum(len(l.text) for l in self.lines)

    def est_duration_sec(self, wpm: int = 155) -> int:
        return round(self.word_count() / wpm * 60)


# ---------------------------------------------------------------- trust stack
@dataclass
class EvidenceSource(Contract):
    url: str
    outlet: str
    tier: int = 3
    owner_group: str = ""
    supports: bool = True
    note: str = ""


@dataclass
class VerifierFinding(Contract):
    claim_id: str
    status: str                    # VERIFY_STATUS
    independent_count: int = 0     # distinct owner groups, syndication collapsed, tier<=3
    has_official: bool = False     # at least one tier-1 primary source supports it
    traced_to_original: bool = False
    evidence: list = field(default_factory=list)     # [EvidenceSource]
    note: str = ""


@dataclass
class VerifierReport(Contract):
    script_id: str
    findings: list = field(default_factory=list)     # [VerifierFinding]
    searches_used: int = 0


@dataclass
class FactCheckFinding(Contract):
    claim_id: str
    rating: str                    # FACT_RATINGS
    issue: str = ""
    suggested_fix: str = ""


@dataclass
class FactCheckReport(Contract):
    script_id: str
    findings: list = field(default_factory=list)     # [FactCheckFinding]


@dataclass
class BiasIssue(Contract):
    line_id: str
    type: str                      # BIAS_TYPES
    severity: str                  # SEVERITY
    explanation: str = ""
    suggestion: str = ""


@dataclass
class BiasReport(Contract):
    script_id: str
    balance_score: int = 100       # 0-100, higher = more balanced/neutral
    issues: list = field(default_factory=list)       # [BiasIssue]
    missing_perspectives: list = field(default_factory=list)


@dataclass
class LegalIssue(Contract):
    target_id: str                 # claim id or line id
    risk: str                      # LEGAL_RISKS
    severity: str                  # SEVERITY
    explanation: str = ""
    fix: str = ""


@dataclass
class LegalReport(Contract):
    script_id: str
    issues: list = field(default_factory=list)       # [LegalIssue]


@dataclass
class GateReason(Contract):
    rule_id: str
    detail: str
    target_id: str = ""
    blocking: bool = True


@dataclass
class GateDecision(Contract):
    script_id: str
    decision: str                  # DECISIONS
    lane_policy: str
    revision: int
    reasons: list = field(default_factory=list)      # [GateReason]
    rewrite_instructions: list = field(default_factory=list)
    scores: dict = field(default_factory=dict)       # corroboration_rate, accuracy_rate, balance_score
    recheck_after_minutes: int | None = None         # set when decision == HOLD


# ---------------------------------------------------------------- publishing
@dataclass
class Episode(Contract):
    id: str
    show_id: str
    script_id: str
    title: str
    description: str
    show_notes_md: str = ""
    audio_path: str = ""
    audio_url: str = ""
    duration_sec: int = 0
    published_at: str | None = None
    guid: str = ""
    status: str = "draft"
    disclosure_text: str = ""
    transcript_path: str = ""
    gate: dict = field(default_factory=dict)         # GateDecision.to_dict()
    source_count: int = 0


@dataclass
class Correction(Contract):
    id: str
    episode_id: str
    description: str
    claim_id: str = ""
    reported_by: str = ""          # "monitor:recheck", "listener", "outlet"
    created_at: str = ""
    status: str = "open"           # open | applied | rejected
    action: str = "note"           # note | reissue | retract


@dataclass
class AgentRun(Contract):
    """Envelope every agent call is logged in (cost + provenance)."""
    agent_id: str
    run_id: str
    model_tier: str
    started_at: str
    finished_at: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    web_searches: int = 0
    usd_estimate: float = 0.0
    ok: bool = True
    error: str = ""


_NESTED = {
    ("Script", "lines"): ScriptLine,
    ("Script", "claims"): Claim,
    ("Script", "sources"): Source,
    ("VerifierFinding", "evidence"): EvidenceSource,
    ("VerifierReport", "findings"): VerifierFinding,
    ("FactCheckReport", "findings"): FactCheckFinding,
    ("BiasReport", "issues"): BiasIssue,
    ("LegalReport", "issues"): LegalIssue,
    ("GateDecision", "reasons"): GateReason,
}


# ---------------------------------------------------------------- JSON Schemas
def _obj(props: dict, required: list | None = None) -> dict:
    return {"type": "object", "properties": props,
            "required": required if required is not None else list(props),
            "additionalProperties": False}


_STR = {"type": "string"}
_INT = {"type": "integer"}
_BOOL = {"type": "boolean"}
_STRS = {"type": "array", "items": _STR}


def _enum(values):
    return {"type": "string", "enum": list(values)}


JSON_SCHEMAS: dict[str, dict] = {
    # Producer → script with claim map
    "Script": _obj({
        "title": _STR,
        "lines": {"type": "array", "items": _obj({
            "id": _STR, "speaker": _STR, "text": _STR, "claim_ids": _STRS,
            "segment": _enum(["cold_open", "intro", "body", "kicker", "disclosure", "outro"])})},
        "claims": {"type": "array", "items": _obj({
            "id": _STR, "text": _STR, "type": _enum(CLAIM_TYPES), "line_ids": _STRS,
            "source_ids": _STRS, "risk_flags": {"type": "array", "items": _enum(RISK_FLAGS)},
            "attributed": _BOOL})},
    }),
    "VerifierReport": _obj({
        "findings": {"type": "array", "items": _obj({
            "claim_id": _STR, "status": _enum(VERIFY_STATUS), "independent_count": _INT,
            "has_official": _BOOL, "traced_to_original": _BOOL,
            "evidence": {"type": "array", "items": _obj({
                "url": _STR, "outlet": _STR, "tier": _INT, "owner_group": _STR,
                "supports": _BOOL, "note": _STR})},
            "note": _STR})},
    }),
    "FactCheckReport": _obj({
        "findings": {"type": "array", "items": _obj({
            "claim_id": _STR, "rating": _enum(FACT_RATINGS), "issue": _STR,
            "suggested_fix": _STR})},
    }),
    "BiasReport": _obj({
        "balance_score": _INT,
        "issues": {"type": "array", "items": _obj({
            "line_id": _STR, "type": _enum(BIAS_TYPES), "severity": _enum(SEVERITY),
            "explanation": _STR, "suggestion": _STR})},
        "missing_perspectives": _STRS,
    }),
    "LegalReport": _obj({
        "issues": {"type": "array", "items": _obj({
            "target_id": _STR, "risk": _enum(LEGAL_RISKS), "severity": _enum(SEVERITY),
            "explanation": _STR, "fix": _STR})},
    }),
    "StoryTriage": _obj({
        "stories": {"type": "array", "items": _obj({
            "cluster_key": _STR, "headline": _STR, "summary": _STR, "beat": _STR,
            "newsworthiness": _INT, "risk_flags": {"type": "array", "items": _enum(RISK_FLAGS)},
            "entities": _STRS, "signal_ids": _STRS})},
    }),
    "Copy": _obj({
        "title": _STR, "description": _STR, "show_notes_md": _STR, "social_posts": _STRS,
        "keywords": _STRS,
    }),
}


def validate(kind: str, data: dict) -> list[str]:
    """Validate data against JSON_SCHEMAS[kind]. Returns a list of error strings ([] = valid).

    Uses the jsonschema package when installed; otherwise a minimal structural check.
    """
    schema = JSON_SCHEMAS[kind]
    try:
        import jsonschema  # type: ignore
    except ImportError:
        missing = [k for k in schema.get("required", []) if k not in (data or {})]
        return [f"missing field: {k}" for k in missing]
    v = jsonschema.Draft202012Validator(schema)
    return [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in v.iter_errors(data)]
