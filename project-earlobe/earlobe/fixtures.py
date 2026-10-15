"""Deterministic dry-run data: fake agent outputs and sample sensor signals.

Dry runs swap every network / LLM / TTS call for this module, so a full episode
can be produced with no keys and no network.

  fake(kind, **ctx)         schema-valid dict for any kind in schemas.JSON_SCHEMAS
  sample_signals(market)    ~13 clearly fictional Signals per market

fake() derives its output from ctx (script, claims, stories, show_cfg, ...) so
the pieces line up: the verifier report covers the claim ids of the script it is
given, and so on. Every fake passes the deterministic gate (after the
disclosure step), so a dry run ends in PUBLISH. Same ctx in, same dict out; no
clocks and no randomness (choices come from a hash of the ids).

Everything made here is labelled "[SAMPLE]" and uses sample.invalid URLs, which
can never resolve. Outlet names are real only so the owner-group and
independence logic has something to chew on; the headlines are invented.
"""
from __future__ import annotations

import hashlib
import re
from datetime import datetime, timedelta, timezone

from earlobe import config
from earlobe.schemas import JSON_SCHEMAS, RISK_FLAGS, Signal, make_id

_SENSITIVE_TYPES = {"allegation", "legal_status"}
_SENSITIVE_FLAGS = {"crime", "legal_proceeding", "named_private_person", "minor", "victim", "death"}
_CLAIM_ID = re.compile(r"\bclm_\w+")


# ---------------------------------------------------------------- small helpers
def _g(obj, key, default=None):
    """Field from a dataclass or a dict."""
    value = obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)
    return default if value is None else value


def _dict(obj) -> dict:
    return obj.to_dict() if hasattr(obj, "to_dict") else obj


def _n(seed: str, mod: int) -> int:
    """Stable pseudo-random int in [0, mod) from a string."""
    return int(hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8], 16) % mod


def _slug(text: str, limit: int = 60) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:limit]


def _clip(text: str, n: int) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def _sentence(text: str) -> str:
    text = " ".join(str(text).split())
    return text if not text or text[-1] in ".!?" else text + "."


def _props(kind: str, *path: str) -> set:
    """Property names of a (nested) JSON schema object, so echoed data matches it exactly."""
    node = JSON_SCHEMAS[kind]
    for p in path:
        node = node["properties"][p]["items"]
    return set(node["properties"])


# ---------------------------------------------------------------- ctx readers
def _claims(ctx: dict) -> list[dict]:
    """Claims a checker is asked about. Unknown details (id-only) are flagged known=False."""
    if ctx.get("script") is not None:
        raw = _g(ctx["script"], "claims", [])
    elif ctx.get("claims") is not None:
        raw = ctx["claims"]
    elif ctx.get("claim_ids"):
        raw = list(ctx["claim_ids"])
    else:   # last resort: pull claim ids out of any prompt text passed along
        text = " ".join(v for v in ctx.values() if isinstance(v, str))
        raw = list(dict.fromkeys(_CLAIM_ID.findall(text)))
    out = []
    for c in raw:
        if isinstance(c, str):
            out.append({"id": c, "type": "fact", "risk_flags": [], "attributed": False, "known": False})
        else:
            out.append({"id": _g(c, "id"), "type": _g(c, "type", "fact"),
                        "risk_flags": list(_g(c, "risk_flags", [])),
                        "attributed": bool(_g(c, "attributed", False)), "known": True})
    return out


def _lane(ctx: dict) -> str | None:
    return (ctx.get("lane_policy") or _g(ctx.get("script") or {}, "lane_policy", None)
            or _g(ctx.get("show_cfg") or {}, "lane", None))


def _sensitive(c: dict) -> bool:
    return (not c["known"] or c["type"] in _SENSITIVE_TYPES
            or bool(_SENSITIVE_FLAGS & set(c["risk_flags"])))


# ---------------------------------------------------------------- Script
def _story(s) -> dict:
    s = _dict(s)
    return {"id": s.get("id") or make_id("sty", s.get("headline", "")),
            "headline": s.get("headline", "[SAMPLE] Untitled story"),
            "summary": s.get("summary", ""), "beat": s.get("beat", ""),
            "outlets": list(s.get("outlets") or []), "source_ids": list(s.get("source_ids") or []),
            "risk_flags": [f for f in (s.get("risk_flags") or []) if f in RISK_FLAGS],
            "entities": list(s.get("entities") or []), "signal_ids": list(s.get("signal_ids") or []),
            "newsworthiness": int(s.get("newsworthiness") or 0)}


def _default_stories(market: str, limit: int = 3) -> list[dict]:
    """Stories built from the first few sample events, used when ctx carries none."""
    stories, seen = [], set()
    for sig in sample_signals(market):
        event = sig.raw["event"]
        if event not in seen:
            seen.add(event)
            stories.append({"id": make_id("sty", event), "headline": sig.title, "summary": sig.summary,
                            "beat": sig.beat, "outlets": [sig.outlet], "source_ids": [sig.id]})
        if len(stories) == limit:
            break
    return stories


def _script(ctx: dict) -> dict:
    if ctx.get("script") is not None:        # claim-extraction pass etc.: hand the script back as-is
        d = _dict(ctx["script"])
        lines, claims = _props("Script", "lines"), _props("Script", "claims")
        return {"title": d["title"],
                "lines": [{k: v for k, v in _dict(x).items() if k in lines} for x in d["lines"]],
                "claims": [{k: v for k, v in _dict(x).items() if k in claims} for x in d["claims"]]}

    show_id = ctx.get("show_id") or "sample-show"
    show = ctx.get("show_cfg") or config.load_shows().get(show_id, {})
    name, date = show.get("name") or "Sample Show", ctx.get("episode_date") or "2026-01-01"
    hosts = show.get("hosts") or ["mara", "theo"]
    stories = [_story(s) for s in (ctx.get("stories") or _default_stories(show.get("market") or "national"))]
    stories = stories[: show.get("max_stories") or len(stories)]

    lines, claims = [], []

    def add_line(text: str, segment: str, claim_ids: list) -> str:
        lid = make_id("ln", show_id, date, len(lines))
        lines.append({"id": lid, "speaker": hosts[len(lines) % len(hosts)], "text": text,
                      "claim_ids": claim_ids, "segment": segment})
        return lid

    add_line(f"This is {name} for {date}. Here is what we are tracking. "
             "Everything in this sample episode is placeholder content.", "intro", [])
    for st in stories:
        outlet = (st["outlets"] or ["local reporting"])[0]
        for part, (ctype, text, attributed) in enumerate([
                ("fact", _sentence(st["summary"] or st["headline"]), False),
                ("attribution", f"According to {outlet}, officials are expected to share "
                                f"more details soon.", True)]):
            cid = make_id("clm", show_id, date, st["id"], part)
            body = f"{_sentence(st['headline'])} {text}" if part == 0 else text
            lid = add_line(body, "body", [cid])
            claims.append({"id": cid, "text": _clip(text, 240), "type": ctype, "line_ids": [lid],
                           "source_ids": st["source_ids"], "risk_flags": st["risk_flags"],
                           "attributed": attributed})
    add_line(f"That is {name} for {date}. Sample data only.", "kicker", [])
    return {"title": f"[SAMPLE] {name} for {date}", "lines": lines, "claims": claims}


# ---------------------------------------------------------------- trust-stack reports
_MEDIA = [("[SAMPLE] Metro Gazette", 2, "Sample Media Group A"),
          ("[SAMPLE] Channel 9 News", 2, "Sample Media Group B"),
          ("[SAMPLE] Public Radio Network", 2, "Sample Media Group C")]
_OFFICIAL = ("[SAMPLE] Office of Public Information", 1, "Sample Government")


def _evidence(claim_id: str, count: int, official: bool) -> list[dict]:
    """`count` supporting sources, each its own owner group, so a recount agrees with `count`."""
    picks = ([_OFFICIAL] if official else []) + _MEDIA[: count - int(official)]
    return [{"url": f"https://sample.invalid/evidence/{claim_id}/{_slug(outlet)}", "outlet": outlet,
             "tier": tier, "owner_group": group, "supports": True,
             "note": "Sample evidence for dry run."} for outlet, tier, group in picks[:count]]


def _verifier_finding(c: dict, lane: str | None) -> dict:
    sensitive = _sensitive(c)
    solo = (lane in ("standard", "archive") and c["known"] and c["attributed"] and not sensitive
            and _n(c["id"] + "solo", 4) == 0)             # the one 'mostly' in mostly corroborated
    if solo:
        status, count, official = "single_source", 1, False
    else:
        # breaking needs 3 independent sources; unknown lane gets the safe maximum
        status, count = "corroborated", 3 if lane in (None, "breaking") else 2 + _n(c["id"], 2)
        official = sensitive or c["type"] == "number" or _n(c["id"] + "off", 3) == 0
    return {"claim_id": c["id"], "status": status, "independent_count": count,
            "has_official": official, "traced_to_original": not solo,
            "evidence": _evidence(c["id"], count, official),
            "note": "Sample finding for dry run."}


def _verifier_report(ctx: dict) -> dict:
    lane = _lane(ctx)
    return {"findings": [_verifier_finding(c, lane) for c in _claims(ctx)]}


def _factcheck_report(ctx: dict) -> dict:
    return {"findings": [{"claim_id": c["id"], "rating": "accurate", "issue": "", "suggested_fix": ""}
                         for c in _claims(ctx)]}


def _bias_report(ctx: dict) -> dict:
    return {"balance_score": 85, "issues": [], "missing_perspectives": []}


def _legal_report(ctx: dict) -> dict:
    return {"issues": []}


# ---------------------------------------------------------------- triage and copy
def _triage(ctx: dict) -> dict:
    groups = []
    if ctx.get("stories"):
        for s in map(_story, ctx["stories"]):
            groups.append({"cluster_key": s["id"], "headline": s["headline"], "summary": s["summary"],
                           "beat": s["beat"], "risk_flags": s["risk_flags"], "entities": s["entities"],
                           "signal_ids": s["signal_ids"] or s["source_ids"],
                           "newsworthiness": s["newsworthiness"]})
    else:   # raw signals: group by sample event when present, otherwise one story per signal
        by_key: dict[str, list] = {}
        for sig in ctx.get("signals") or []:
            key = _g(_g(sig, "raw", {}), "event", None) or _g(sig, "id")
            by_key.setdefault(key, []).append(sig)
        for key, sigs in by_key.items():
            first = sigs[0]
            groups.append({"cluster_key": key, "headline": _g(first, "title"),
                           "summary": _g(first, "summary", ""), "beat": _g(first, "beat", ""),
                           "risk_flags": [], "entities": [], "signal_ids": [_g(s, "id") for s in sigs],
                           "newsworthiness": 55 + min(len(sigs) * 8, 30)})
    for g in groups:
        g["newsworthiness"] = g["newsworthiness"] or 55 + _n(g["cluster_key"], 40)
    return {"stories": groups}


def _copy(ctx: dict) -> dict:
    show = ctx.get("show_cfg") or {}
    script = _dict(ctx.get("script") or {})
    body = [l for l in script.get("lines", []) if l.get("segment") == "body"]
    title = script.get("title") or f"[SAMPLE] {show.get('name', 'Sample Show')}"
    lead = body[0]["text"] if body else "Sample episode for a dry run."
    notes = "## In this episode\n" + "\n".join(f"- {_clip(l['text'], 140)}" for l in body[::2]) \
        if body else "## In this episode\n- Sample episode for a dry run."
    return {"title": title,
            "description": _clip(f"{lead} Sample content for a dry run.", 300),
            "show_notes_md": notes,
            "social_posts": [_clip(f"New episode: {title}", 270),
                             _clip(f"{lead} #sample", 270)],
            "keywords": ["sample", "dry run", show.get("market", "news")]}


# ---------------------------------------------------------------- archive pack (evergreen research)
_ARCHIVE_SOURCES = [
    ("[SAMPLE] National Archives Catalog", 1, "archive", "Sample record group, finding aid and dated documents."),
    ("[SAMPLE] Library of Congress Digital Collections", 1, "archive", "Sample digitized newspaper page and caption."),
    ("[SAMPLE] State Historical Society", 2, "archive", "Sample oral-history summary and a dated timeline."),
    ("[SAMPLE] University Special Collections", 3, "archive", "Sample finding aid for a donated collection."),
]
_CASE_SOURCES = [
    ("[SAMPLE] County Sheriff's Office", 1, "press_release", "Sample public appeal for tips with the agency tip line."),
    ("[SAMPLE] State Bureau of Investigation", 1, "official_data", "Sample listing in a state cold-case unit page."),
    ("[SAMPLE] Regional Daily Newspaper", 2, "article", "Sample anniversary report summarizing the public record."),
    ("[SAMPLE] Public Radio Archive", 2, "broadcast", "Sample broadcast summary of the agency's renewed appeal."),
]


def _archive_pack(ctx: dict) -> dict:
    show = ctx.get("show_cfg") or config.load_shows().get(ctx.get("show_id") or "", {})
    topic = _dict(ctx.get("topic") or {})
    cold = show.get("lane") == "strict"
    title = topic.get("title") or ("Sample cold case" if cold else "Sample history topic")
    sources = _CASE_SOURCES if cold else _ARCHIVE_SOURCES
    key = _slug(f"{show.get('id') or ctx.get('show_id') or 'show'}-{topic.get('id') or title}")
    return {"subject": f"[SAMPLE] {_clip(title, 120)}",
            "summary": _sentence(f"[SAMPLE] Placeholder summary of the record on: {_clip(title, 160)} "
                                 "This is dry-run content, not research"),
            "risk_flags": ["crime"] if cold else [],
            "sources": [{"url": f"https://sample.invalid/archive/{key}/{_slug(outlet)}", "outlet": outlet,
                         "title": f"[SAMPLE] {_clip(title, 80)}", "published_at": "", "tier": tier,
                         "kind": kind, "excerpt": excerpt} for outlet, tier, kind, excerpt in sources],
            "uncertain": ["Dry-run sample: nothing here was researched."]}


_BUILDERS = {"Script": _script, "VerifierReport": _verifier_report, "FactCheckReport": _factcheck_report,
             "BiasReport": _bias_report, "LegalReport": _legal_report, "StoryTriage": _triage,
             "Copy": _copy, "ArchivePack": _archive_pack}


def fake(kind: str, **ctx) -> dict:
    """A schema-valid dict for `kind`, derived from ctx (script, claims, stories, show_cfg, ...)."""
    try:
        build = _BUILDERS[kind]
    except KeyError:
        raise ValueError(f"no fixture for kind {kind!r}; known kinds: {sorted(_BUILDERS)}") from None
    return build(ctx)


# ---------------------------------------------------------------- sample signals
# outlet -> (tier, kind). Anything not listed is an established newsroom: (2, "article").
_OUTLETS = {
    "City of Columbia": (1, "press_release"), "City of Los Angeles": (1, "press_release"),
    "City of New York": (1, "press_release"), "City of Chicago": (1, "press_release"),
    "LA Metro": (1, "press_release"), "MTA": (1, "press_release"), "CTA": (1, "press_release"),
    "FEMA": (1, "press_release"), "NASA": (1, "press_release"),
    "National Weather Service": (1, "official_data"), "National Hurricane Center": (1, "official_data"),
    "CourtListener": (1, "court_record"), "U.S. Supreme Court": (1, "court_record"),
    "SC Daily Gazette": (3, "article"), "Block Club Chicago": (3, "article"),
    "amNY": (3, "article"), "THE CITY": (3, "article"),
}

# market -> [(beat, summary, [(outlet, minutes_ago, title[, syndicated_from]), ...]), ...]
_EVENTS = {
    "columbia-sc": [
        ("government", "Council moved funds into the Riverbend Park project on a 5-2 vote; a second reading is next month.", [
            ("City of Columbia", 190, "[SAMPLE] City Council approves Riverbend Park budget amendment, 5-2 vote"),
            ("WIS", 175, "[SAMPLE] Columbia council approves Riverbend Park budget amendment in 5-2 vote"),
            ("The State", 160, "[SAMPLE] Council approves $2.4 million Riverbend Park budget amendment"),
            ("SC Daily Gazette", 120, "[SAMPLE] Columbia council splits 5-2 on Riverbend Park budget amendment")]),
        ("public_safety", "Inspectors found a crack in a support beam of the Elm Street Bridge; it is closed while engineers assess repairs.", [
            ("Associated Press", 95, "[SAMPLE] Elm Street Bridge closed after inspectors find structural crack"),
            ("The State", 88, "[SAMPLE] Elm Street Bridge closed after inspectors find structural crack", "Associated Press"),
            ("WLTX", 80, "[SAMPLE] Elm Street Bridge shut down after inspectors find crack")]),
        ("education", "The Sample County school board put off a vote on later school start times.", [
            ("WLTX", 300, "[SAMPLE] Sample County school board delays vote on later start times"),
            ("The Post and Courier", 280, "[SAMPLE] Sample County school board postpones later start times vote")]),
        ("weather", "A flood watch covers the Midlands through Sunday evening as heavy rain moves in.", [
            ("National Weather Service", 50, "[SAMPLE] Flood watch issued for the Midlands through Sunday evening"),
            ("WIS", 40, "[SAMPLE] Flood watch for Midlands as heavy rain moves in through Sunday")]),
        ("business", "Sample Fork Brewing Co. is planning a second taproom.", [
            ("The Post and Courier", 400, "[SAMPLE] Sample Fork Brewing Co. plans second taproom near Main Street")]),
        ("sports", "Central Sample High clinched the region title with a 24-17 win.", [
            ("WLTX", 500, "[SAMPLE] Central Sample High football clinches region title with 24-17 win")]),
    ],
    "los-angeles": [
        ("housing", "A council committee moved a tenant-protection ordinance for Alder Street forward after debate.", [
            ("City of Los Angeles", 210, "[SAMPLE] Council advances Alder Street tenant-protection ordinance"),
            ("LAist", 195, "[SAMPLE] LA council advances Alder Street tenant protection ordinance"),
            ("Los Angeles Times", 180, "[SAMPLE] Los Angeles council advances Alder Street tenant-protection ordinance after debate")]),
        ("transit", "Metro will close a segment of the Verdant Line this weekend for track work; shuttle buses will run.", [
            ("LA Metro", 130, "[SAMPLE] Metro announces weekend closure of Verdant Line segment for track work"),
            ("LAist", 120, "[SAMPLE] Verdant Line segment to close this weekend for Metro track work"),
            ("KTLA", 110, "[SAMPLE] Metro to close Verdant Line segment this weekend for track work")]),
        ("public_safety", "A brush fire near Sample Canyon prompted evacuation orders for nearby streets.", [
            ("KTLA", 75, "[SAMPLE] Brush fire near Sample Canyon prompts evacuation orders"),
            ("ABC7 Los Angeles", 62, "[SAMPLE] Evacuation orders issued as brush fire burns near Sample Canyon"),
            ("NBC Los Angeles", 58, "[SAMPLE] Sample Canyon brush fire forces evacuation orders")]),
        ("entertainment_business", "Starlight Pictures says it will expand its studio lot.", [
            ("Los Angeles Times", 240, "[SAMPLE] Starlight Pictures announces studio lot expansion"),
            ("Associated Press", 225, "[SAMPLE] Starlight Pictures plans expansion of its studio lot"),
            ("Los Angeles Daily News", 215, "[SAMPLE] Starlight Pictures plans expansion of its studio lot", "Associated Press")]),
        ("federal_court", "A federal judge granted in part a motion to dismiss in a studio contract suit.", [
            ("CourtListener", 150, "[SAMPLE] Docket: Sample v. Example Studios, motion to dismiss granted in part")]),
        ("culture", "A neighborhood jazz festival added a second stage to this year's lineup.", [
            ("LAist", 400, "[SAMPLE] Neighborhood jazz festival adds second stage for this year's lineup")]),
        ("sports", "Sample Valley Prep won the city title game in overtime.", [
            ("Los Angeles Daily News", 480, "[SAMPLE] Sample Valley Prep wins city title game in overtime")]),
    ],
    "new-york": [
        ("transit", "Overnight service on the Meridian Line will change for a signal upgrade.", [
            ("MTA", 160, "[SAMPLE] MTA announces overnight service changes on Meridian Line for signal upgrade"),
            ("Gothamist", 145, "[SAMPLE] Overnight Meridian Line service changes planned for signal upgrade"),
            ("New York Daily News", 130, "[SAMPLE] Meridian Line overnight service to change during signal upgrade, MTA says"),
            ("amNY", 120, "[SAMPLE] Meridian Line signal upgrade means overnight service changes")]),
        ("government", "The mayor's office unveiled Harbor Green, a plan to add street trees across the city.", [
            ("City of New York", 200, "[SAMPLE] Mayor's office unveils Harbor Green street-tree initiative"),
            ("THE CITY", 185, "[SAMPLE] City unveils Harbor Green plan to plant street trees"),
            ("The New York Times", 170, "[SAMPLE] New York City announces Harbor Green initiative to add street trees")]),
        ("public_safety", "A water main break flooded a block of Sample Avenue and closed a subway entrance.", [
            ("Associated Press", 90, "[SAMPLE] Water main break floods Sample Avenue block, closes subway entrance"),
            ("New York Daily News", 80, "[SAMPLE] Water main break floods Sample Avenue, shutting subway entrance"),
            ("amNY", 75, "[SAMPLE] Water main break floods Sample Avenue block, closes subway entrance", "Associated Press")]),
        ("housing", "The rent board set a hearing date ahead of a preliminary stabilization vote.", [
            ("THE CITY", 300, "[SAMPLE] Rent board schedules hearing on preliminary stabilization vote"),
            ("Gothamist", 285, "[SAMPLE] Rent board sets hearing date ahead of preliminary stabilization vote")]),
        ("weather", "A wind advisory covers the coast through Saturday morning.", [
            ("National Weather Service", 45, "[SAMPLE] Wind advisory issued for the coast through Saturday morning")]),
        ("sports", "A Sample Borough Little League team advanced to the state final.", [
            ("amNY", 420, "[SAMPLE] Sample Borough Little League team advances to state final")]),
    ],
    "chicago": [
        ("transit", "Shuttle buses will replace Ember Line trains this weekend during track work.", [
            ("CTA", 150, "[SAMPLE] CTA announces weekend Ember Line shuttle buses during track work"),
            ("WBEZ", 140, "[SAMPLE] Ember Line riders to take shuttle buses this weekend for track work"),
            ("Chicago Tribune", 130, "[SAMPLE] Weekend Ember Line track work means shuttle buses, CTA says"),
            ("Block Club Chicago", 120, "[SAMPLE] Ember Line shuttle buses replace trains this weekend during CTA track work")]),
        ("government", "The mayor's office announced a lighting upgrade along the Lakefront Trail.", [
            ("City of Chicago", 210, "[SAMPLE] Mayor's office announces Lakefront Trail lighting upgrade"),
            ("Chicago Sun-Times", 190, "[SAMPLE] City to upgrade Lakefront Trail lighting, mayor's office says"),
            ("Chicago Tribune", 175, "[SAMPLE] Lakefront Trail lighting upgrade announced by mayor's office")]),
        ("public_safety", "A warehouse fire on Sample Street sent smoke across the South Side.", [
            ("Associated Press", 85, "[SAMPLE] Warehouse fire on Sample Street sends smoke across South Side"),
            ("WGN", 70, "[SAMPLE] Warehouse fire on Sample Street sends smoke over South Side"),
            ("Chicago Sun-Times", 66, "[SAMPLE] Warehouse fire on Sample Street sends smoke across South Side", "Associated Press")]),
        ("housing", "A zoning committee delayed its vote on the Maple Court apartment proposal.", [
            ("Block Club Chicago", 330, "[SAMPLE] Zoning committee delays vote on Maple Court apartment proposal"),
            ("WBEZ", 310, "[SAMPLE] Maple Court apartment proposal vote delayed by zoning committee")]),
        ("weather", "A dense fog advisory is in effect until mid-morning.", [
            ("National Weather Service", 40, "[SAMPLE] Dense fog advisory issued for Chicago area until mid-morning")]),
        ("sports", "Sample Park Prep won the city volleyball final.", [
            ("Chicago Sun-Times", 450, "[SAMPLE] Sample Park Prep volleyball team wins city final")]),
    ],
    "national": [
        # Breaking-style cluster: official confirmation plus many independent tier-1/2 outlets inside 40 minutes.
        ("disaster", "A Category 3 hurricane made landfall near Cape Marlow; forecasters and emergency officials are tracking winds and storm surge.", [
            ("National Hurricane Center", 38, "[SAMPLE] NHC advisory: Hurricane Sample makes landfall near Cape Marlow as Category 3"),
            ("Associated Press", 34, "[SAMPLE] Hurricane Sample makes landfall near Cape Marlow as Category 3 storm"),
            ("Reuters", 31, "[SAMPLE] Category 3 Hurricane Sample makes landfall near Cape Marlow"),
            ("NBC News", 27, "[SAMPLE] Hurricane Sample slams into Cape Marlow coast as Category 3"),
            ("CBS News", 24, "[SAMPLE] Hurricane Sample hits Cape Marlow with Category 3 winds"),
            ("ABC News", 20, "[SAMPLE] Hurricane Sample makes landfall at Cape Marlow, Category 3"),
            ("The New York Times", 16, "[SAMPLE] Hurricane Sample strikes near Cape Marlow as a Category 3 storm"),
            ("FEMA", 12, "[SAMPLE] FEMA activates emergency response as Hurricane Sample hits Cape Marlow")]),
        ("scotus", "The Supreme Court put the Sample v. Example dispute on its argument calendar.", [
            ("U.S. Supreme Court", 600, "[SAMPLE] Supreme Court schedules argument in Sample v. Example dispute"),
            ("Reuters", 580, "[SAMPLE] Supreme Court to hear Sample v. Example dispute next term")]),
        ("space", "A space agency set a launch window for the Meridian lunar probe.", [
            ("NASA", 700, "[SAMPLE] Agency sets launch window for Meridian lunar probe")]),
        ("business_mega", "Orbital Dynamics Corp. reported record quarterly revenue.", [
            ("Bloomberg", 520, "[SAMPLE] Orbital Dynamics Corp. reports record quarterly revenue")]),
        ("tracked_cases", "A pretrial hearing was set in State v. Sample for next month.", [
            ("CourtListener", 360, "[SAMPLE] Docket: State v. Sample, pretrial hearing set for next month")]),
        ("world", "Coalition leaders in Veldoria agreed on a budget deal.", [
            ("BBC News", 800, "[SAMPLE] Coalition leaders in Veldoria agree on budget deal")]),
    ],
}


def sample_signals(market: str, now: datetime | None = None) -> list[Signal]:
    """~13 fictional Signals for a market; several outlets cover the same event so clustering has work to do.

    Events are labelled "[SAMPLE]", use sample.invalid URLs, and carry raw={"sample": True, "event": key}.
    Each local market has one wire copy (raw["syndicated_from"] = "Associated Press") that should
    collapse into the wire when counting independent outlets. The national set holds a
    breaking-style cluster. Ages are minutes before `now` (default: the current UTC minute) so
    time windows behave; pass `now` for fully reproducible timestamps.
    """
    if market not in _EVENTS:
        raise ValueError(f"no sample signals for market {market!r}; known: {sorted(_EVENTS)}")
    base = (now or datetime.now(timezone.utc)).replace(second=0, microsecond=0)
    signals = []
    for e, (beat, summary, items) in enumerate(_EVENTS[market]):
        event = f"{market}-{e}"
        for outlet, ago, title, *syndicated in items:
            tier, kind = _OUTLETS.get(outlet, (2, "article"))
            url = f"https://sample.invalid/{market}/{_slug(outlet)}/{_slug(title)}"
            raw = {"sample": True, "event": event}
            if syndicated:
                raw["syndicated_from"] = syndicated[0]
            signals.append(Signal(
                id=make_id("sig", url), sensor="courtlistener" if kind == "court_record" else f"beat-{market}",
                market=market, beat=beat, title=title, url=url, outlet=outlet,
                published_at=(base - timedelta(minutes=ago)).strftime("%Y-%m-%dT%H:%M:%SZ"),
                summary=f"{summary} [Sample data]", kind=kind, tier=tier, raw=raw))
    return signals
