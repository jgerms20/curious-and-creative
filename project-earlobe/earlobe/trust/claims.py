"""Claim Extractor: an independent second pass over what the script actually asserts.

The writer logs its own claims, and a writer can miss a sentence or call a hard fact
"context". This pass reads only the spoken lines, never the writer's claim list or
sources, and lists every checkable assertion again. The two lists are then merged
conservatively:

  matched claims   keep the writer's id and source_ids; take the stricter type, the
                   union of risk flags, and `attributed` only if BOTH passes agree
  missed claims    added (source_ids stay empty, so the verifier must find sources)
  writer-only      kept; extra checking is harmless

Nothing here decides whether a claim is true. Dry-run: fixtures hand the script back
as-is, so the merge is a no-op.
"""
from __future__ import annotations

import dataclasses
import difflib
import re

from earlobe.schemas import CLAIM_TYPES, RISK_FLAGS, Claim, Script, make_id

CLAIMS_SYSTEM = """\
You are the Claim Extractor for the Curious & Creative Network's automated news audio shows.

A writer has produced a script that synthetic AI hosts will read aloud. No person reads it before it airs. Independent checkers will verify every claim you list, so your one job is to make sure NOTHING checkable slips through unlabelled. You are a separate pass from the writer. You are deliberately NOT shown the writer's own claim list or sources, so you cannot inherit its blind spots. Read the lines the way a listener would hear them, and list everything a listener could take away as a statement about the world.

WHAT YOU RETURN
One JSON object: the script title, every line, and your claims.
- lines: return every input line unchanged (same id, speaker, text, segment). Only fill claim_ids with the ids of the claims that line contains. Lines in the "disclosure" segment describe how the show is made, not the world: give them an empty claim_ids list and extract nothing from them.
- claims: one object per claim, ids "clm_1", "clm_2", ... in script order.
    text         the claim as one self-contained sentence (rules below)
    type         one of: fact, number, quote, attribution, allegation, legal_status, prediction, context
    line_ids     every line that carries it (usually one)
    source_ids   ALWAYS [] . You have not been shown sources and must never invent any.
    risk_flags   zero or more of: crime, legal_proceeding, named_private_person, minor, victim, health, election, death, breaking, financial
    attributed   true or false (rules below)

HOW TO WRITE A CLAIM
1. One checkable proposition per claim. Split a sentence when its parts could be separately true or false AND differ in type, attribution, risk, or the evidence needed. Do not split into grammatical fragments, and keep a figure with the event it measures when one source would settle both ("the council approved the budget amendment in a 5-2 vote" is one claim).
2. Make it stand alone. Replace pronouns and "the suspect / the company / the bill" with the names and descriptions used elsewhere in the script, so a researcher with no script can check it.
3. Keep the writer's wording. Same numbers, same verbs, same hedges, same attribution. Never strengthen ("approved" must not become "unanimously approved"), weaken, or correct a sentence. If it is wrong, that is the checkers' job to catch, and they can only catch what you faithfully record.
4. Keep the attribution inside the claim. "Police said the man was arrested on suspicion of burglary" is a claim about what police said; record it that way and mark attributed true. Do not strip "police said" and leave a bare accusation.
5. Include time words exactly as spoken ("on Tuesday", "this morning", "last year"). They are checkable.

TYPES (pick one per claim; when a sentence mixes types, pick the first that applies in this order of care: allegation, legal_status, quote, number, attribution, fact)
- allegation    an accusation of wrongdoing that is not proven: "prosecutors allege", "the lawsuit says", "accused of".
- legal_status  where a person or matter stands in the legal process: arrested, booked, charged, indicted, pleaded, convicted, acquitted, sentenced, sued, settled, dismissed, hearing set, injunction granted.
- quote         words presented as someone's exact words. Put the exact quoted words and the speaker in the claim.
- number        the claim's main content is a figure: a count, amount, percentage, age, date, measurement, ranking, vote tally.
- attribution   what a named person, agency, document or outlet said, announced, reported, believes or found, when that is not a quote, allegation or legal status.
- fact          any other statement about events, people, places, organizations, decisions or conditions, including background ("the bridge opened in 1952") and consequences ("the closure affects 12 bus routes").
- prediction    anything about the future or an uncertain outcome: forecasts, projections, "is expected to", "will".
- context       ONLY pure framing with no checkable content. A sentence that could be proven right or wrong is NEVER context, and background facts are facts. Do not make claims out of signposting ("Next up", "Here is what we know", greetings, sign-offs, rhetorical questions). One sanctioned exception: "We did not find a public response from X" describes our own search, not the world, so list it as context (the fact checker tests it).

RISK FLAGS (flag generously: a flag only makes the checkers stricter, never looser)
- crime                an alleged or actual crime, an arrest, police activity, an investigation of wrongdoing
- legal_proceeding     a court case, hearing, filing, lawsuit, or other legal process
- named_private_person a private individual (not an official or public figure acting in that public role) is named or identifiable
- minor                anyone under 18 is mentioned or identifiable, even if no age is given (a student, a child, a teen, a juvenile)
- victim               a victim of a crime, accident or abuse is named or identifiable; always flag sexual assault, abuse and trafficking
- health               a medical condition, diagnosis, treatment, outbreak or mental-health detail
- election             candidates, ballots, campaigns, voting
- death                a death, a death toll, a cause of death, or the identity of someone who died
- breaking             an unfolding event whose facts are still changing
- financial            prices, investments, fraud, or a company's or person's finances, where an error could cost someone money

ATTRIBUTED
true ONLY when this sentence, or the one right before it, names who is making the claim: a person, an agency, a document, or an outlet ("police said", "according to the county budget", "The State reported"). "Reportedly", "sources say", "it is believed", and "allegedly" with no named accuser do NOT count. Anything the host states in their own voice as fact is false.

BEFORE YOU ANSWER
Reread every non-disclosure line. Any sentence containing a name, number, date, place, quote, attribution, legal word, cause, effect, comparison ("largest", "first", "more than last year"), or "why it matters" statement must be covered by at least one claim. Do not add claims for things the script does not say. Do not judge whether anything is true. Do not use outside knowledge.
"""

# Stricter types win when the two passes disagree. A fact typed "context" or
# "prediction" by the writer therefore gets re-typed (ACC-13).
_TYPE_RANK = {"allegation": 7, "legal_status": 6, "quote": 5, "number": 4,
              "attribution": 3, "fact": 2, "prediction": 1, "context": 0}
MATCH_MIN = 0.6            # text similarity needed to call two claims the same assertion
_WORD = re.compile(r"[a-z0-9]+")


# ---------------------------------------------------------------- shared rendering
def render_lines(script: Script, *, skip_disclosure: bool = False) -> str:
    """The spoken lines as `[id] speaker (segment): text`, one per line, for checker prompts."""
    return "\n".join(f"[{l.id}] {l.speaker} ({l.segment}): {l.text}" for l in script.lines
                     if not (skip_disclosure and l.segment == "disclosure"))


def render_claims(script: Script) -> str:
    """The claim list as `[id] type | flags | attributed | lines: text`, for checker prompts."""
    rows = []
    for c in script.claims:
        flags = ",".join(c.risk_flags) or "none"
        rows.append(f"[{c.id}] {c.type} | flags: {flags} | attributed: {str(bool(c.attributed)).lower()}"
                    f" | lines: {','.join(c.line_ids) or '-'}\n    {c.text}")
    return "\n".join(rows)


def relink(lines: list, claims: list) -> tuple[list, list]:
    """Make line.claim_ids and claim.line_ids agree, dropping references to ids that don't exist."""
    line_ids = {l.id for l in lines}
    claim_ids = {c.id for c in claims}
    by_line: dict[str, list] = {l.id: [] for l in lines}
    for c in claims:
        c.line_ids = [i for i in dict.fromkeys(c.line_ids) if i in line_ids]
    for l in lines:
        for cid in l.claim_ids:
            if cid in claim_ids:
                by_line[l.id].append(cid)
    for c in claims:
        for lid in c.line_ids:
            by_line[lid].append(c.id)
    for l in lines:
        l.claim_ids = list(dict.fromkeys(by_line[l.id]))
    for c in claims:
        c.line_ids = [l.id for l in lines if c.id in l.claim_ids]
    return lines, claims


# ---------------------------------------------------------------- merge
def _norm(text: str) -> str:
    return " ".join(_WORD.findall((text or "").lower()))


def _similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def _flags(*groups) -> list[str]:
    return [f for f in RISK_FLAGS if any(f in g for g in groups)]


def _from_extractor(raw: dict, script: Script) -> list[Claim]:
    """Claims the extractor returned, cleaned: known lines only, no disclosure, no invented sources."""
    segment = {l.id: l.segment for l in script.lines}
    on_line: dict[str, list] = {}
    for l in raw.get("lines") or []:
        for cid in l.get("claim_ids") or []:
            on_line.setdefault(cid, []).append(l.get("id"))
    out = []
    for c in raw.get("claims") or []:
        text = " ".join(str(c.get("text") or "").split())
        line_ids = [i for i in dict.fromkeys((c.get("line_ids") or []) + on_line.get(c.get("id"), []))
                    if i in segment and segment[i] != "disclosure"]
        if not text or not line_ids:
            continue
        ctype = c.get("type") if c.get("type") in CLAIM_TYPES else "fact"
        out.append(Claim(id=str(c.get("id") or ""), text=text, type=ctype, line_ids=line_ids,
                         risk_flags=_flags(c.get("risk_flags") or []),
                         attributed=bool(c.get("attributed"))))
    return out


def _best_match(new: Claim, old: list[Claim], taken: set) -> Claim | None:
    best, best_score = None, MATCH_MIN
    for c in old:
        if c.id in taken or (c.line_ids and not set(c.line_ids) & set(new.line_ids)):
            continue
        score = _similar(c.text, new.text)
        if score >= best_score:
            best, best_score = c, score
    return best


def merge_claims(script: Script, found: list[Claim]) -> Script:
    """Merge independently extracted claims into the script (see module docstring). Pure."""
    claims = [dataclasses.replace(c, line_ids=list(c.line_ids), source_ids=list(c.source_ids),
                                  risk_flags=list(c.risk_flags)) for c in script.claims]
    lines = [dataclasses.replace(l, claim_ids=list(l.claim_ids)) for l in script.lines]
    taken: set = set()
    used = {c.id for c in claims}
    for new in found:
        old = _best_match(new, claims, taken)
        if old is not None:
            taken.add(old.id)
            if _TYPE_RANK[new.type] > _TYPE_RANK.get(old.type, 0):
                old.type = new.type
            old.risk_flags = _flags(old.risk_flags, new.risk_flags)
            old.attributed = bool(old.attributed and new.attributed)
            old.line_ids = list(dict.fromkeys(old.line_ids + new.line_ids))
            continue
        cid = make_id("clm", script.id, "x", new.text)
        if cid in used:
            cid = make_id("clm", script.id, "x", new.text, len(used))
        used.add(cid)
        new.id = cid
        claims.append(new)
    lines, claims = relink(lines, claims)
    return dataclasses.replace(script, lines=lines, claims=claims)


def extract_claims(script: Script, llm) -> Script:
    """Run the independent claim pass and merge it into `script`. Returns a new Script."""
    user = ("Extract every claim from this script. Return the lines unchanged, with claim_ids "
            "filled in, and the claims list.\n\nSCRIPT TITLE: "
            f"{script.title}\n\nLINES:\n{render_lines(script)}")
    raw = llm.structured("claim-extractor", "opus", CLAIMS_SYSTEM, user, "Script", effort="high",
                         ctx={"script": script})
    return merge_claims(script, _from_extractor(raw, script))
