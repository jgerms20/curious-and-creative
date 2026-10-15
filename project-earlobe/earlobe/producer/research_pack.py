"""Research pack: the writer's one input about the world.

build_pack() turns the assigned Stories and the Sources behind them into a plain dict:
every story with its source ids, every source with tier, kind and owner group, how many
INDEPENDENT sources each story has (owner groups, wire copy and syndication collapsed, tier 4
ignored), and short cautions that follow from the story's risk flags. The writer may use
nothing outside the pack, and may cite only source ids that appear in it.

Excerpts are summaries in our own words, never article text (CONVENTIONS rule 7), and are
cut to EXCERPT_MAX characters. No network, no clock: same inputs give the same pack.
"""
from __future__ import annotations

from earlobe import config
from earlobe.desk.independence import independent_count, owner_group
from earlobe.schemas import Source, Story, make_id

EXCERPT_MAX = 400
MAX_SOURCES_PER_STORY = 12

CAUTIONS = {
    "minor": "A person under 18 may be involved. Never name or identify them (no parent, address, school detail or nickname).",
    "victim": "A victim may be involved. Never name or identify a victim of sexual assault, abuse or trafficking; keep detail to what the story needs.",
    "crime": "Crime story. Say arrested on suspicion of, charged with, indicted, pleaded or convicted only as the record states, attribute police and prosecutor accounts, and presume innocence.",
    "legal_proceeding": "Court matter. Official acts (a ruling, a vote, a filing) can be stated directly; a filing's contents are one side's claims and must be attributed to it.",
    "named_private_person": "A private person may be named in the sources. Name them only if the story cannot be understood without it.",
    "death": "A death is involved. Name the dead only after an official release or on-record family statement. Casualty counts: at least, official source, time given.",
    "health": "Health information. Attribute it to the source; apply no diagnosis or label to a person.",
    "election": "Election material. Stay neutral, no endorsements, attribute every claim about a candidate or measure.",
    "financial": "Money is involved. Figures need their source, period and unit; no advice.",
    "breaking": "Unfolding story. State only what is confirmed, who confirmed it and as of when, and what is still unknown.",
}


def _source(x) -> tuple[Source, str]:
    """(Source, alias id) from a Source, a Signal or a dict of either. The alias is the signal id, if any."""
    if isinstance(x, Source):
        return x, ""
    d = x.to_dict() if hasattr(x, "to_dict") else dict(x)
    url = d.get("url", "")
    sid = d.get("id", "")
    alias = sid if sid and not str(sid).startswith("src_") else ""
    raw = d.get("raw") or {}
    return Source(
        id=sid if str(sid).startswith("src_") else make_id("src", url), url=url,
        outlet=d.get("outlet", ""), title=d.get("title", ""), published_at=d.get("published_at"),
        retrieved_at=d.get("retrieved_at"), tier=int(d.get("tier") or 3), kind=d.get("kind") or "article",
        owner_group=d.get("owner_group", ""),
        syndicated_from=d.get("syndicated_from") or raw.get("syndicated_from", ""),
        excerpt=d.get("excerpt") or d.get("summary", ""), market=d.get("market", "")), alias


def _excerpt(text: str) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= EXCERPT_MAX else text[:EXCERPT_MAX - 1].rstrip() + "…"


def _entry(s: Source, owners: dict) -> dict:
    return {"id": s.id, "url": s.url, "outlet": s.outlet, "title": s.title, "published_at": s.published_at,
            "tier": s.tier, "kind": s.kind,
            "owner_group": s.owner_group or owner_group(s.outlet or s.url, owners),
            "syndicated_from": s.syndicated_from, "excerpt": _excerpt(s.excerpt)}


def _cautions(story: Story, srcs: list[Source], independent: int, official: bool) -> list[str]:
    out = []
    if not any(s.tier <= 3 for s in srcs):
        out.append("No tier 1-3 source on file. Do not report this story.")
    elif independent < 2 and not official:
        out.append("Only one independent source. Skip it, or attribute it to that source by name on air "
                   "and keep it low-risk. Strict and breaking shows cannot air it.")
    flags = list(story.risk_flags) + (["breaking"] if story.breaking and "breaking" not in story.risk_flags else [])
    out += [CAUTIONS[f] for f in flags if f in CAUTIONS]
    return out


def build_pack(stories: list, sources: list, owners: dict | None = None) -> dict:
    """Pack for the writer: {stories, sources, warnings}. Stories and sources may be objects or dicts.

    `sources` can be Sources or Signals (a Signal becomes a Source keyed by its URL, the same way
    Story.source_ids are made). `owners` defaults to config/owners.yaml.
    """
    owners = config.load_owners() if owners is None else owners
    stories = [s if isinstance(s, Story) else Story.from_dict(s) for s in stories or []]
    by_id: dict[str, Source] = {}
    alias: dict[str, str] = {}
    for x in sources or []:
        src, sig_id = _source(x)
        by_id.setdefault(src.id, src)
        if sig_id:
            alias[sig_id] = src.id

    warnings, used, entries = [], [], []
    for st in stories:
        wanted = list(dict.fromkeys(list(st.source_ids) + [alias[i] for i in st.signal_ids if i in alias]))
        srcs = [by_id[i] for i in wanted if i in by_id]
        if len(srcs) < len(wanted):
            warnings.append(f"{st.id}: {len(wanted) - len(srcs)} listed source(s) were not supplied")
        srcs = sorted(srcs, key=lambda s: s.tier)[:MAX_SOURCES_PER_STORY]
        independent = independent_count(srcs, owners)
        official = any(s.tier == 1 for s in srcs)
        used += [s.id for s in srcs]
        entries.append({"story_id": st.id, "headline": st.headline, "summary": st.summary, "beat": st.beat,
                        "market": st.market, "first_seen": st.first_seen, "breaking": st.breaking,
                        "risk_flags": list(st.risk_flags), "entities": list(st.entities),
                        "official_confirmation": official or st.official_confirmation,
                        "independent_sources": independent, "source_ids": [s.id for s in srcs],
                        "cautions": _cautions(st, srcs, independent, official)})
    unused = [i for i in by_id if i not in set(used)]
    if unused:
        warnings.append(f"{len(unused)} supplied source(s) matched no story and were left out")
    return {"stories": entries,
            "sources": [_entry(by_id[i], owners) for i in dict.fromkeys(used)],
            "warnings": warnings}
