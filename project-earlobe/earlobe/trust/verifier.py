"""Source Verifier: blind re-sourcing of every claim that needs corroboration.

Blindness is the point. The model is shown ONLY each claim's id and text, plus
the show's market and the episode date. It never sees the writer's sources, notes or
reasoning, so it cannot rubber-stamp them; it has to find sources itself with web
search and trace wire copy and echoes back to the original.

What the model reports is then treated as testimony, not as the answer:

  1. evidence is cleaned (real URLs only, duplicates dropped, tier clamped to 1-4)
  2. owner groups come from config/owners.yaml (the model's label is kept only for
     outlets the table doesn't know)
  3. independent_count and has_official are recomputed in code with
     desk.independence, and the status can only be downgraded, never upgraded
  4. only AFTER all that is the writer's source list compared with what the verifier
     found, so ghost sources show up in the notes without ever influencing the count

Dry-run: fixtures.fake("VerifierReport") supplies the evidence.
"""
from __future__ import annotations

from urllib.parse import urlsplit

from earlobe import config
from earlobe.desk.independence import independent_count, owner_group
from earlobe.schemas import (
    Claim,
    EvidenceSource,
    Script,
    VerifierFinding,
    VerifierReport,
)
from earlobe.trust.gate import NEEDS_CORROBORATION

VERIFIER_SYSTEM = """\
You are the Source Verifier for the Curious & Creative Network's automated news audio shows.

YOUR SITUATION
An automated writer produced a script that synthetic AI hosts will read aloud. No person reads it before it airs. You are given only the list of claims from that script, plus the show's market and the episode date. You have NOT been shown the writer's sources or reasoning, and you must not guess at them: that is by design. Your job is to find out for yourself, with web search, whether each claim is true and how well it is sourced. Afterwards, code (not you) recounts independent sources from your evidence using an ownership table, and a fixed-rule gate decides whether each claim may air. Inflated evidence gets caught; missing evidence gets claims cut. Report exactly what you found.

PROCEDURE FOR EACH CLAIM
1. Search for the claim's checkable content: names, numbers, dates, places, the exact legal words. Search more than once, with different wording.
2. Look for the primary source first. Court matter: the docket or filing. Government action: the agency's or body's own release, agenda, minutes, vote record or data. Statistic: the dataset or report. Quote: the transcript, statement, filing or recording. Press release: the release itself, which shows what its author asserts. When a news report cites a document, look for the document and prefer it.
3. Trace to the original. Many outlets run the same wire story or repeat one outlet's scoop. Those are ONE source.
   - Wire copy: if a page is Associated Press, Reuters, AFP or Bloomberg copy republished by another outlet (a wire credit line or byline, "AP", "(Reuters)", text identical to another outlet's), list the WIRE as the evidence, not the republisher. Use the wire's own URL if you can find it, and set outlet and owner_group to the wire's name.
   - Echoes: if several outlets repeat one press release, one outlet's exclusive, or one official's statement, list only the origin and set traced_to_original true if you reached it. Say in the note how many outlets echoed it.
   - Sister outlets: stations, papers and sites with the same parent company are one source. Set owner_group to the PARENT COMPANY whenever you know it, not the outlet's own name.
   - In an evidence note, mention a wire service only when that item IS a republished copy of the wire's story: code reads such a note as syndication and counts the item as the wire.
4. Grade every source you rely on:
   tier 1  primary/official record: a court filing or docket, a government or agency release or dataset, a company filing, an on-record statement published by the speaker's own official channel.
   tier 2  wire service or established newsroom with editorial standards and a corrections policy.
   tier 3  local or specialist outlet, trade press, a verified expert.
   tier 4  aggregators, blogs, forums, social posts, content farms, unverified sites, auto-generated summaries. A social post is tier 1 ONLY when it comes from the official account of the person or agency speaking and you can confirm that account is official (for example, linked from the agency's own site); otherwise tier 4. Anything that rests only on unnamed sources is tier 4: say so in the note. Tier 4 never counts.
5. supports = true only if the source itself states or documents the claim's specific content (the name, number, legal status, date, quote). A page that is merely on the same topic does not support it. supports = false ONLY for a source that contradicts or materially conflicts with the claim as worded (different number, different legal status, a denial, a later reversal). Do not list sources that merely fail to mention the claim.

A CLAIM IS SUPPORTED ONLY TO THE PRECISION OF ITS WORDING
- Legal words: arrested is not charged, charged is not indicted, indicted is not convicted. "Charged" needs a charging document or the prosecutor's on-record statement; an arrest report does not support it. "Pleaded not guilty" needs the plea on the record.
- Numbers: the figure, the unit, the period and the direction words ("more than", "nearly", "at least") must all hold. A figure for a different year, place or measure does not support the claim.
- Quotes: the exact words, by the credited person. A paraphrase, or different wording, does not verify a quote. A quote relayed by a second outlet needs the original statement or an outlet that heard it first-hand.
- Attribution ("X said Y"): verify that X said Y. That is separate from whether Y is true. For allegations, verify that the named accuser made the accusation; do not treat the accusation as proven.
- Names, titles, ages, places and spellings must match.
- Time: judge the claim as of the episode date. If a later source shows the situation changed (charges dropped, a vote reversed, a closure lifted), the claim as worded about the present is contradicted.

STATUS (per claim)
- corroborated  at least two supporting sources with different owners, or a primary record that fully supports the claim.
- single_source exactly one independent supporting source and no primary record.
- unsupported   nothing found that supports it. That includes finding only tier 4, only unnamed sources, or only pages on the topic that never state the specific content.
- contradicted  credible evidence conflicts with the claim as worded. Put what the evidence says in the note.

HONESTY RULES
- You can only count what you actually read in search results. A headline or snippet that lacks the detail does not support the detail. Never get around a paywall or login.
- Never invent a URL, outlet, date or fact. Every evidence URL must be one your searches returned. If you find nothing, say unsupported with an empty evidence list.
- Your own memory is not evidence. For anything recent or local, only what you find counts.
- Do not copy article text. Notes are your own words, two sentences at most.
- Cover EVERY claim: exactly one finding per claim id, using the ids you were given.
- independent_count is the number of different owners among your supporting tier 1-3 evidence; has_official is true if any supporting evidence is tier 1. These are your best estimates; the code recomputes both.
- You have a limited search budget. Spend it where doubt is greatest: allegations, legal status, deaths, named private people, minors, and numbers first. Claims backed by an official record need fewer searches.
"""

BATCH = 8                  # claims per research call, so one call never has to hold a whole episode
_STATUS_RANK = {"contradicted": 0, "unsupported": 1, "single_source": 2, "corroborated": 3}
_TRACKING = ("utm_", "fbclid", "gclid")


# ---------------------------------------------------------------- prompt
def _market_line(script: Script) -> str:
    market_id = config.load_shows().get(script.show_id, {}).get("market", "")
    market = config.load_markets().get(market_id, {})
    if not market_id:
        return "Show market: not specified"
    return f"Show market: {market.get('name', market_id)} ({market_id}); time zone {market.get('tz', 'unknown')}"


def _prompt(script: Script, claims: list[Claim], max_searches: int) -> str:
    rows = "\n".join(f"- id: {c.id}\n  claim: {c.text}" for c in claims)   # nothing else of the writer's
    return (f"{_market_line(script)}\nEpisode date: {script.episode_date} (judge every claim as of this "
            f"date; words like \"today\" refer to it)\n\nVerify these {len(claims)} claims. You have up to "
            f"{max_searches} web searches for them.\n\n{rows}")


# ---------------------------------------------------------------- recount
def _url_key(url: str) -> str:
    """Comparable form of a URL: no scheme, www, fragment, tracking params or trailing slash."""
    p = urlsplit((url or "").strip().lower())
    query = "&".join(sorted(q for q in p.query.split("&") if q and not q.startswith(_TRACKING)))
    return f"{p.netloc.removeprefix('www.')}{p.path.rstrip('/')}" + (f"?{query}" if query else "")


def _tier(value) -> int:
    try:
        return min(max(int(value), 1), 4)
    except (TypeError, ValueError):
        return 4


def _clean_evidence(evidence: list[EvidenceSource]) -> list[EvidenceSource]:
    """Real http(s) URLs only, one entry per page, tier clamped to 1-4."""
    seen, out = set(), []
    for e in evidence:
        e.url = (e.url or "").strip()
        key = _url_key(e.url)
        if not e.url.lower().startswith(("http://", "https://")) or key in seen:
            continue
        seen.add(key)
        e.tier = _tier(e.tier)
        out.append(e)
    return out


def _label(e: EvidenceSource, owners: dict) -> str:
    """Owner group per config/owners.yaml; the model's own label only for outlets the table lacks."""
    group = owner_group(e.outlet, owners)
    return e.owner_group if group == e.outlet and e.owner_group else group


def _settle(f: VerifierFinding, owners: dict) -> VerifierFinding:
    """Recompute count, official flag and status in code (status is only ever downgraded)."""
    f.evidence = _clean_evidence(f.evidence)
    for e in f.evidence:
        e.owner_group = _label(e, owners)
    supporting = [e for e in f.evidence if e.supports]
    f.independent_count = independent_count(supporting, owners)
    f.has_official = any(e.tier == 1 for e in supporting)
    if not supporting:
        f.traced_to_original = False

    notes = []
    status = f.status if f.status in _STATUS_RANK else "unsupported"
    if status != "contradicted" and any(e.tier == 1 and not e.supports for e in f.evidence):
        status = "contradicted"
        notes.append("a tier-1 source conflicts with the claim")
    counted = "unsupported" if f.independent_count == 0 else \
        "single_source" if f.independent_count == 1 else "corroborated"
    if _STATUS_RANK[counted] < _STATUS_RANK[status] and status != "contradicted":
        notes.append(f"{f.independent_count} independent source(s) on recount, not enough for "
                     f"'{status}'")
        status = counted
    f.status = status
    if notes:
        f.note = " ".join([f.note.strip()] + [f"[recount: {'; '.join(notes)}]"]).strip()
    return f


def _merge_dupes(findings: list[VerifierFinding]) -> list[VerifierFinding]:
    """One finding per claim; if the model repeated one, the more cautious status wins."""
    by_id: dict[str, VerifierFinding] = {}
    for f in findings:
        old = by_id.get(f.claim_id)
        if old is None or _STATUS_RANK[f.status] < _STATUS_RANK[old.status]:
            by_id[f.claim_id] = f
    return list(by_id.values())


# ---------------------------------------------------------------- writer comparison (after the fact)
def compare_sources(script: Script, report: VerifierReport, owners: dict) -> list[dict]:
    """Per claim: the writer's cited sources against what the blind verifier found.

    Pure and run only after the verifier's count is final. It never changes a count; it
    exposes writer sources the verifier could not find (possible ghost sources) so they
    can be logged.
    """
    by_id = {s.id: s for s in script.sources}
    found = {f.claim_id: f for f in report.findings}
    rows = []
    for c in script.claims:
        f = found.get(c.id)
        if f is None:
            continue
        writer = [by_id[i] for i in c.source_ids if i in by_id]
        theirs = {_url_key(s.url) for s in writer}
        ours = {_url_key(e.url) for e in f.evidence if e.supports}
        rows.append({"claim_id": c.id, "writer_sources": len(writer),
                     "writer_independent": independent_count(writer, owners),
                     "verifier_independent": f.independent_count,
                     "shared_urls": sorted(theirs & ours), "writer_only_urls": sorted(theirs - ours),
                     "verifier_only_urls": sorted(ours - theirs)})
    return rows


def _note_gaps(rows: list[dict], report: VerifierReport) -> None:
    by_id = {f.claim_id: f for f in report.findings}
    for r in rows:
        if r["writer_independent"] > r["verifier_independent"]:
            f = by_id[r["claim_id"]]
            f.note = (f"{f.note.strip()} [writer cited {r['writer_independent']} independent "
                      f"source(s); blind verification found {r['verifier_independent']}]").strip()


# ---------------------------------------------------------------- public
def verify(script: Script, llm, owners: dict, max_searches: int = 20) -> VerifierReport:
    """Blindly verify every claim whose type needs corroboration.

    `max_searches` is the budget per research call; claims go in batches of BATCH, so a
    long script may use up to ceil(claims / BATCH) * max_searches searches in total.
    """
    claims = [c for c in script.claims if c.type in NEEDS_CORROBORATION]
    start, found = len(llm.runs), []
    for i in range(0, len(claims), BATCH):
        chunk = claims[i:i + BATCH]
        ids = {c.id for c in chunk}
        raw = llm.research("verifier", "opus", VERIFIER_SYSTEM, _prompt(script, chunk, max_searches),
                           "VerifierReport", max_searches=max_searches, effort="high",
                           ctx={"claims": [c.to_dict() for c in chunk], "lane_policy": script.lane_policy})
        found += [_settle(VerifierFinding.from_dict(f), owners)
                  for f in raw.get("findings", []) if f.get("claim_id") in ids]
    searches = sum(r.web_searches for r in llm.runs[start:] if r.agent_id.startswith("verifier"))
    report = VerifierReport(script_id=script.id, findings=_merge_dupes(found), searches_used=searches)
    _note_gaps(compare_sources(script, report, owners), report)    # only now: writer's list, for comparison
    return report
