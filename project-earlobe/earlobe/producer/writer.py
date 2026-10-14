"""Producer / Scriptwriter: turns the rundown and research pack into a Script with a claim map.

Opus tier. The model returns title, lines and claims (schemas "Script"). Code then makes the
result safe to hand on:

  - lines and claims get deterministic ids from their text, so a line the writer leaves alone
    on a rewrite keeps its id; line.claim_ids and claim.line_ids are made to agree
  - claim source_ids are cut down to ids that exist in the research pack (no invented sources)
  - Script.sources holds the pack sources the claims actually cite
  - speakers are forced onto real personas; any disclosure lines the model wrote are replaced
  - the lane comes from the show config (escalated to strict by desk.assign.lane_for)
  - the canonical AI disclosure is appended last (producer.disclosure)

The writer never decides whether the script is good enough to air. The trust stack and the
gate do that, so this module only makes the draft as checkable as it can.

On REWRITE, pass the gate's `instructions` and the `previous` script (make_rewriter does this
for the trust loop). Dry-run: fixtures.fake("Script", ...) builds a placeholder episode.
"""
from __future__ import annotations

import json
from collections.abc import Callable
from datetime import date

from earlobe import config
from earlobe.desk.assign import lane_for
from earlobe.producer.disclosure import disclosure_text, ensure_disclosure
from earlobe.schemas import (
    CLAIM_TYPES,
    RISK_FLAGS,
    Claim,
    Script,
    ScriptLine,
    Source,
    Story,
    make_id,
)
from earlobe.trust.gate import POLICIES

WPM = 155                      # spoken words per minute, same as Script.est_duration_sec
SEGMENTS = ("cold_open", "intro", "body", "kicker", "outro")      # "disclosure" is added by code

WRITER_SYSTEM = """\
You are the Producer and Scriptwriter for the Curious & Creative Network, an automated news audio network. You write the scripts that our original synthetic AI hosts read aloud.

YOUR SITUATION
No person reads your script before it airs. After you, separate agents check it. A Claim Extractor re-lists every checkable statement in it. A Source Verifier, which is NOT shown your sources or your reasoning, must find independent support for every claim from scratch. A Fact Checker tests the exact wording. A Bias Checker and a Legal Screener read for tone, fairness, and legal and human harm. Then a fixed-rule gate decides PUBLISH, REWRITE or KILL (or HOLD on breaking news). A claim the Verifier cannot find is cut. A script that keeps failing is killed and nothing airs. So the goal is not a long script or a clever one. It is a script in which every sentence is true, precisely worded, fairly told and independently checkable. A shorter, honest episode always beats a longer, risky one.

WHAT YOU RECEIVE
- The show: name, format, market, lane, hosts with their roles, target length.
- The research pack: stories with source ids, risk flags, cautions and the count of independent sources; and the sources themselves (outlet, tier, kind, owner group, a short excerpt). It is your ONLY knowledge of the world.
- On a revision: the gate's fix instructions and your previous script.
Use nothing that is not in the pack. Your memory is not a source. If the pack does not support a detail, leave it out. If it does not support a story, leave the story out.

WHAT YOU RETURN
One JSON object: title, lines, claims.
- lines: the script in spoken order.
    id         any short unique string; code renumbers
    speaker    a host id from the show's list, exactly as given
    text       exactly what is read aloud (see SPOKEN STYLE)
    claim_ids  ids of every claim this line makes; [] only for lines with nothing checkable in them
    segment    cold_open | intro | body | kicker | outro. NEVER "disclosure": code appends the AI disclosure after your last line.
- claims: one per checkable proposition.
    id          any short unique string; code renumbers
    text        the claim as one self-contained sentence, worded EXACTLY as the line says it: same numbers, verbs, hedges and attribution
    type        fact | number | quote | attribution | allegation | legal_status | prediction | context
    line_ids    every line that carries it
    source_ids  ids from the pack's sources, and only sources that actually STATE the claim's specific content. A source that is merely on the same topic must not be cited. List every supporting source, so the independent count is honest.
    risk_flags  zero or more of: crime, legal_proceeding, named_private_person, minor, victim, health, election, death, breaking, financial. Flag generously: flags only make checking stricter.
    attributed  true only if the line (or the one right before it) names who is making the claim: a person, agency, document or outlet. Anything the host says in their own voice is false.
Claim types: allegation (accusation not proven); legal_status (arrested, charged, indicted, pleaded, convicted, sentenced, sued, settled, dismissed, hearing set); quote (words given as someone's exact words); number (the claim is mainly a figure, date, count, vote tally); attribution (what a named source said, announced, reported or found, when not a quote or allegation); fact (any other statement about the world, including background and consequences); prediction (anything about the future); context (pure framing with nothing checkable: signposting, greetings, sign-offs; a sentence that can be right or wrong is never context).
EVERY FACTUAL SENTENCE CARRIES claim_ids. Names, numbers, dates, places, quotes, legal words, causes, effects, comparisons ("largest", "first", "more than last year") and every "why it matters" statement are claims. Do not hide a fact in a line with no claim. The Claim Extractor will find it anyway, and it will then be checked cold.

SOURCING RULES
1. Two or more independent sources for any fact, number, quote or attribution, or one official record (a court filing, an agency release or dataset, an on-record statement from the speaker's own channel). The lane rules you are given set the exact bar.
2. Independent means different owner groups. Sister stations and papers of one parent are one source. Wire copy (Associated Press, Reuters, AFP, Bloomberg) republished by other outlets is one source: the wire. Several outlets repeating one press release or one outlet's scoop are one source: the original. Tier 4 (aggregators, blogs, social posts, unverified or anonymous) never counts, and never carries a claim alone.
3. Prefer the primary record to reports about it. When the pack has the filing, release or data, build the sentence from it and attribute it.
4. Report facts in your own words. Never read out, closely follow or copy an article's sentences or structure. Credit the outlet that broke a story by name ("The State first reported..."). A quote is used only if the pack gives the exact words, kept short, credited to the person who said them.
5. If a story has one independent source and no official record: skip it, or report it with that source named on air in the same sentence and only if the claim is low-risk. In a strict or breaking lane, skip it.
6. Never use anonymous sources, "reportedly", "sources say", "it is believed" or "allegedly" with no accuser. Name the outlet, person, agency or document.

ATTRIBUTION AND LEGAL WORDS (a listener cannot see quotation marks, so the verb carries the sourcing)
- said: default for what a named person or body stated. Never "claimed", "admitted", "insisted", "conceded", "slammed", "blasted", "refused", "came clean": each takes a side.
- according to: documents, data and records. reported: another newsroom's reporting, outlet named.
- Police and prosecutor narratives are accounts: "police said", "according to the arrest affidavit". Never settled fact. Official acts (a vote, a ruling, a filing, a closure order) can be stated directly.
- arrested on suspicion of: arrested or booked, no charges yet. Never "arrested for burglary".
- charged with: only after charges are filed, shown by the pack's court record or the prosecutor's on-record statement. Never after an arrest alone.
- indicted: a grand jury returned an indictment. pleaded not guilty / guilty / no contest: only as entered. convicted / found guilty: only after a verdict or guilty plea. found not guilty: after an acquittal ("cleared", "got off", "walked free" are not used).
- alleges / alleged: always with who alleges ("prosecutors allege", "the lawsuit says"). A lawsuit or complaint is one side's account. Include the other side's public response if the pack has one. If it does not, say plainly: "We did not find a public response from [name]." That is the only sentence about our own search you may write; log it as a claim of type context. We do not call, email or request comment, so never say we did.
- Presumption of innocence: a charged person is never "the killer", "the burglar", "the suspect behind", or "the alleged killer". Use "the man charged with" or "the defendant". Never imply guilt before a verdict or plea. Give the plea or denial if it is on the record.
- Predictions are attributed to whoever makes them ("the National Weather Service expects"). Unattributed "will" about uncertain events is cut.
- Say what is NOT known only as a source said it ("police have not released a name, a spokesperson said"). Do not write unattributed "no suspect has been named".

PEOPLE AND HARM
- Never name or identify anyone under 18 in a story about crime, courts, accidents, abuse, health or a family crisis, whether suspect, defendant, victim or witness. Identification by pieces counts: a parent's name, an address, a school plus a detail, a team plus a number, a nickname. "A teenager" is fine; the name and the pieces are not. This holds for people who were minors when the events happened.
- Never name or identify a person who says, or is reported, to have been sexually assaulted, abused or trafficked, even if other outlets have. No exceptions today.
- Name a private person only if the story cannot be understood without it. Never present an uncharged person as a suspect; never use "person of interest". A suspect is named only after arrest or charge, or when a law enforcement agency has named them on the record, and then attributed.
- Name the dead only after an official release (coroner, medical examiner, police) or an on-record family statement. Casualty numbers: official source, attributed, "at least", with the time they were given.
- Victims are people, not plot devices. No graphic detail beyond what the story needs. No sensational wording.
- Race, religion, ethnicity, immigration status, gender identity, sexual orientation, disability and health are mentioned only when relevant to the story and confirmed.
- Health claims: attribute them; never put a diagnosis or label ("deranged") on a suspect or victim.

NO SPECULATION, NO OPINION, NO PRETENDING
- No motive, cause, intent or outcome guessed at in the host's voice. No "appears to", "likely", "may have been trying to" unless a named source said it and the line says so. Never solve a cold case on air or point at someone investigators have not named.
- No loaded words or labels, no hype, no cliffhangers, no rhetorical questions that insinuate. No personal opinions on contested political or social questions, no endorsements of candidates or ballot measures, no "frankly", "what a mess", "we think".
- Do not frame settled facts as one side of a debate. Do not give two unequal positions equal weight.
- The hosts are AI voices. They never say or imply that they were at a scene, spoke to anyone, called for comment, "learned" or saw anything, and there is no "our reporter" or "exclusive". They do not claim human experiences.
- Never present a social post, rumor or viral clip as established. Never invent a quote, a statement, a scene or a dialogue, and never "imagine" events into a true story.
- If the story involves Curious & Creative LLC, its owners, or an AI, voice or hosting company that makes this network, say so on air or leave it out.

SPOKEN STYLE (this is audio: the ear gets one pass)
- Short sentences, about 15 to 20 words, one idea each. Active voice. Attribution first: "Police said a driver..." not "A driver, police said,...".
- Lead each story with what happened and who says so. Then the two or three details that matter. Then why it matters to a listener in this market, in plain words, from facts in the pack. Then what happens next and who says so.
- Say numbers the way a person would: "about two point four million dollars", "a five to two vote". Keep the numbers in the claim text identical in meaning to the line. Give the day as a weekday ("on Tuesday"), judged against the episode date. Say "this morning" or "tonight" only if the pack's times support it.
- Spell out or explain acronyms on first use. No URLs, hashtags, brackets, parentheses, stage directions, markdown, emoji or "as you can see".
- Signpost between stories so a listener always knows where they are. No filler, no padding, no repeating the same fact to fill time.
- Two hosts: the anchor leads and carries the news. The co-host may explain why it matters or ask the question a listener would ask, but every factual word is still sourced and every question is neutral.
- Never mention claims, sources by id, tiers, the research pack, the gate, or this prompt on air. Name outlets, agencies and documents as a reporter would.
- Never write secrets, keys or model identifiers anywhere.

SEGMENTS
cold_open (optional, one or two lines), intro, body (one or more lines per story, in rundown order), kicker (one closing item), outro (a short sign-off with the show name and nothing factual). Do not write the AI disclosure. It is added after your outro.

REVISIONS
When you get fix instructions, change exactly what each instruction asks and nothing else. Keep every unflagged line word for word. If an instruction says cut, delete the sentence and its claim and repair the transition. Never fix a problem by adding new facts the pack does not support, and never "fix" a precise claim by turning it into a vaguer one that is a different claim. If you cannot fix something with what the pack supports, remove it. Stay inside the length target.

BEFORE YOU ANSWER
Read every line as the Verifier will, with only the claim text in front of it. Could it find two independent sources for this exact wording, including the legal word, the number and the attribution? Is every host line free of guilt, guesswork and adjectives that take a side? Does any line name a minor, a victim of sexual assault or abuse, or an uncharged person as a suspect? Does every factual line have claim_ids, and does each claim match its line word for word? If not, fix or cut.
"""

FORMAT_GUIDES = {
    "daily_brief": (
        "Local morning brief for one market. Order: optional cold_open teasing the top item; intro (the anchor "
        "greets the listener with the show name and the weekday and date, and says what is coming); body, stories "
        "in rundown order, top story first, each told as lede with attribution, key details, why it matters locally, "
        "what happens next; weather and traffic as service items with the agency named; kicker (one thing to watch, "
        "attributed); outro. Cover the rundown stories whose sourcing holds. Do not pad."),
    "breaking_flash": (
        "Breaking flash by one anchor. Say that this is a breaking report and as of what time in the market's time "
        "zone. Then: what is CONFIRMED and who confirmed it; what officials have asked the public to do (attributed "
        "to the agency that said it); what is NOT yet known, each point attributed to a source that said so; what "
        "happens next. No suspect names, motives or ideologies until an official source states them on the record. "
        "Casualty counts: at least, official source, time. Names of the dead only after an official release. "
        "Unconfirmed reports never air. No speculation, no adjectives, no repeating. Short and calm."),
    "court_roundup": (
        "Evening court roundup. For each case: the court and the case name as filed; what happened in court (a "
        "ruling, hearing or filing is an official act and can be stated directly); what a filing alleges (always "
        "attributed to the filing or the party); the other side's public response, or 'We did not find a public "
        "response from...'; what comes next and the date. Use legal words exactly as the record has them as of the "
        "episode date. Charged people are presumed innocent. No juvenile cases; no names of minors or of victims of "
        "sexual assault or abuse. Name private people only if the record makes it necessary."),
    "case_weekly": (
        "Weekly update on tracked cases, two hosts. For each case: where it stands in the legal process today; what "
        "changed this week according to the record; what is scheduled next; a brief recap of the background with "
        "attribution. If the case was reported earlier as an arrest or charge, say how it has progressed. Presumption "
        "of innocence throughout. Facts of the case are the record's, attributed. No theories, no solving, no "
        "speculation about who did what."),
    "evergreen_story": (
        "Long-form narrative for one host (cold case or history). Build it from the records in the pack, in "
        "chronological order, with signposts so a listener never gets lost. Attribute every account to its record or "
        "outlet. Label legend, publicity and memory as such ('the story the studio told was...'), and keep the same "
        "fairness for people who have died. For a cold case: the victim is a person, not a plot device; no one is "
        "named as a suspect unless charged or named on the record by the agency; no minors, no victims of sexual "
        "assault or abuse; no theories of your own; say what the record leaves unresolved. No invented scenes, quotes "
        "or dialogue."),
}
_GENERIC_GUIDE = "Follow the segments above, in the show's voice, and stay inside the length target."


# ---------------------------------------------------------------- prompt
def _weekday(day: str) -> str:
    try:
        return date.fromisoformat(str(day)[:10]).strftime("%A")
    except ValueError:
        return ""


def word_budget(show_cfg: dict) -> tuple[int, int]:
    """(low, high) spoken words for the body of the episode: target minutes minus the disclosure."""
    lo, hi = (list(show_cfg.get("target_minutes") or [6, 8]) + [8])[:2]
    spare = len(disclosure_text(show_cfg).split())
    return max(lo * WPM - spare, 100), max(hi * WPM - spare, 150)


def lane_rules(lane: str) -> str:
    """The gate's bar for this lane in plain words, generated from trust.gate.POLICIES so they never drift."""
    p = POLICIES.get(lane) or POLICIES["standard"]
    rules = [f"Lane '{p.name}'. Each fact, number, quote, attribution, allegation and legal-status claim needs "
             f"{p.min_independent} independent sources (distinct owner groups; wire copy counts once; tier 4 never counts)."]
    rules.append("One tier 1 official record is enough on its own." if p.official_satisfies else
                 "A tier 1 official record does NOT replace independent sources; it counts as one of them.")
    rules.append("A single named source is acceptable only for a low-risk claim that the line attributes by name."
                 if p.allow_attributed_single else "No single-source claims, even attributed.")
    if p.sensitive_needs_official:
        rules.append("Sensitive claims (allegations, legal status, crime, death, named private person, minor, "
                     "victim) also need a tier 1 official record. Otherwise cut them.")
    rules.append(f"Balance score must reach {p.min_balance}; legal issues of {p.legal_block_severity} severity "
                 f"or worse block. You get {p.max_rewrites} rewrite(s) before the episode is killed.")
    return " ".join(rules)


def _persona_lines(hosts: list, voices: dict) -> str:
    personas = voices.get("personas") or {}
    rows = []
    for h in hosts:
        p = personas.get(h) or {}
        rows.append(f"- {h}: {p.get('role', 'host')}; {p.get('style', '')}".rstrip("; "))
    return "\n".join(rows)


def _render_previous(script: Script) -> str:
    lines = "\n".join(f"[{l.id}] {l.speaker} ({l.segment}): {l.text}  {{claims: {','.join(l.claim_ids) or '-'}}}"
                      for l in script.lines if l.segment != "disclosure")
    claims = "\n".join(f"[{c.id}] {c.type} | attributed: {str(bool(c.attributed)).lower()} | "
                       f"sources: {','.join(c.source_ids) or '-'} | {c.text}" for c in script.claims)
    return f"TITLE: {script.title}\nLINES:\n{lines}\nCLAIMS:\n{claims}"


def _user_prompt(show_id: str, show_cfg: dict, stories: list[Story], pack: dict, voices: dict,
                 episode_date: str, lane: str, revision: int, instructions: list | None,
                 previous: Script | None) -> str:
    market_id = show_cfg.get("market", "")
    market = config.load_markets().get(market_id, {})
    hosts = show_cfg.get("hosts") or list(voices.get("personas") or {})
    lo, hi = word_budget(show_cfg)
    fmt = show_cfg.get("format", "")
    rundown = "\n".join(f"{i}. [{s.id}] {s.headline}" for i, s in enumerate(stories, 1)) or "(no stories)"
    parts = [
        f"SHOW: {show_cfg.get('name', show_id)} (id {show_id}), format {fmt or 'unspecified'}, "
        f"market {market.get('name', market_id) or 'unspecified'}, time zone {market.get('tz', 'unknown')}",
        f"EPISODE DATE: {episode_date} ({_weekday(episode_date) or 'weekday unknown'})",
        f"LENGTH: {lo} to {hi} spoken words in the lines you write (the AI disclosure is added after, "
        f"about {len(disclosure_text(show_cfg).split())} words).",
        f"HOSTS (use these ids as speaker):\n{_persona_lines(hosts, voices)}",
        f"FORMAT: {FORMAT_GUIDES.get(fmt, _GENERIC_GUIDE)}",
        f"LANE RULES: {lane_rules(lane)}",
        f"RUNDOWN (top story first):\n{rundown}",
        "RESEARCH PACK (your only knowledge of the world):\n" + json.dumps(pack, ensure_ascii=False,
                                                                        separators=(",", ":")),
    ]
    if revision and previous is not None:
        parts.append(f"PREVIOUS SCRIPT (revision {previous.revision}):\n{_render_previous(previous)}")
    if instructions:
        fixes = "\n".join(f"{i}. {t}" for i, t in enumerate(instructions, 1))
        parts.append(f"FIX INSTRUCTIONS FROM THE GATE (revision {revision}). Apply each one; change nothing "
                     f"else:\n{fixes}")
    parts.append("Write the script now. Return the JSON object only.")
    return "\n\n".join(parts)


# ---------------------------------------------------------------- building the Script
def _uniq_id(prefix: str, seen: set, *parts) -> str:
    """Deterministic id from the parts; a repeat of identical parts gets a counter."""
    n, cid = 0, make_id(prefix, *parts)
    while cid in seen:
        n += 1
        cid = make_id(prefix, *parts, n)
    seen.add(cid)
    return cid


def _notes(stories: list[Story]) -> str:
    """Desk-side context for the Bias and Legal checkers: the desk's risk flags (hints to be stricter)."""
    rows = [f"{s.headline} [{', '.join(list(s.risk_flags) + (['breaking'] if s.breaking else []))}]"
            for s in stories if s.risk_flags or s.breaking]
    return ("Story desk risk flags: " + "; ".join(rows)) if rows else ""


def _build(raw: dict, show_id: str, show_cfg: dict, stories: list[Story], pack: dict, voices: dict,
           episode_date: str, lane: str, revision: int) -> Script:
    persona_ids = list(voices.get("personas") or {})
    personas = set(persona_ids)
    hosts = list(show_cfg.get("hosts") or persona_ids)
    if not hosts:
        raise ValueError("no hosts configured for the show and no personas in voices.yaml")
    pack_sources = {s["id"]: s for s in pack.get("sources", [])}

    lines, pairs, line_map, seen = [], [], {}, set()
    for l in raw.get("lines") or []:
        text = " ".join(str(l.get("text") or "").split())
        segment = l.get("segment") if l.get("segment") in SEGMENTS else "body"
        if not text or l.get("segment") == "disclosure":
            continue
        speaker = l.get("speaker") if l.get("speaker") in personas else hosts[len(lines) % len(hosts)]
        lid = _uniq_id("ln", seen, show_id, episode_date, text)
        line_map[l.get("id")] = lid
        lines.append(ScriptLine(id=lid, speaker=speaker, text=text, segment=segment))
        pairs.append((l, lines[-1]))
    if not lines:
        raise ValueError("the writer returned no usable lines")

    claims, claim_map, seen_text = {}, {}, {}
    for c in raw.get("claims") or []:
        text = " ".join(str(c.get("text") or "").split())
        if not text:
            continue
        if text in seen_text:                       # same assertion listed twice: one claim
            claim_map[c.get("id")] = seen_text[text]
            claims[seen_text[text]].line_ids += [line_map[i] for i in c.get("line_ids") or [] if i in line_map]
            continue
        cid = make_id("clm", show_id, episode_date, text)
        seen_text[text] = claim_map[c.get("id")] = cid
        claims[cid] = Claim(
            id=cid, text=text, type=c.get("type") if c.get("type") in CLAIM_TYPES else "fact",
            line_ids=[line_map[i] for i in c.get("line_ids") or [] if i in line_map],
            source_ids=[i for i in dict.fromkeys(c.get("source_ids") or []) if i in pack_sources],
            risk_flags=[f for f in RISK_FLAGS if f in (c.get("risk_flags") or [])],
            attributed=bool(c.get("attributed")))

    for old_line, new_line in pairs:                # claim_ids on lines, both directions
        for old in old_line.get("claim_ids") or []:
            if old in claim_map:
                new_line.claim_ids.append(claim_map[old])
    for c in claims.values():
        for l in lines:
            if l.id in c.line_ids and c.id not in l.claim_ids:
                l.claim_ids.append(c.id)
    for l in lines:
        l.claim_ids = list(dict.fromkeys(l.claim_ids))
    for c in claims.values():
        c.line_ids = [l.id for l in lines if c.id in l.claim_ids]

    cited = {i for c in claims.values() for i in c.source_ids}
    title = " ".join(str(raw.get("title") or "").split()) or \
        f"{show_cfg.get('name', show_id)} for {episode_date}"
    story_ids = [s.id for s in stories]
    return Script(
        id=make_id("scr", show_id, episode_date, *sorted(story_ids), revision), show_id=show_id,
        episode_date=episode_date, title=title, lines=lines, claims=list(claims.values()),
        sources=[Source.from_dict(pack_sources[i]) for i in pack_sources if i in cited],
        story_ids=story_ids, lane_policy=lane, revision=revision, notes_for_checkers=_notes(stories))


# ---------------------------------------------------------------- public
def write_script(show_id: str, show_cfg: dict, stories: list, pack: dict, llm, *, revision: int = 0,
                 instructions: list | None = None, episode_date: str, previous: Script | None = None,
                 voices: dict | None = None) -> Script:
    """Write (or rewrite) the episode script. The result already ends with the AI disclosure.

    `instructions` are the gate's rewrite instructions; pass the script being revised as `previous`
    so the writer can keep what passed. Raises if the model returns nothing usable.
    """
    voices = config.load_voices() if voices is None else voices
    stories = [s if isinstance(s, Story) else Story.from_dict(s) for s in stories]
    lane = lane_for(show_cfg, stories)
    user = _user_prompt(show_id, show_cfg, stories, pack, voices, episode_date, lane, revision,
                        instructions, previous)
    raw = llm.structured("producer", "opus", WRITER_SYSTEM, user, "Script", effort="high",
                         ctx={"show_id": show_id, "show_cfg": show_cfg, "episode_date": episode_date,
                              "stories": [s.to_dict() for s in stories]})
    script = _build(raw, show_id, show_cfg, stories, pack, voices, episode_date, lane, revision)
    return ensure_disclosure(script, show_cfg, voices)


def make_rewriter(show_id: str, show_cfg: dict, stories: list, pack: dict, llm, *, episode_date: str,
                  voices: dict | None = None) -> Callable[[Script, list], Script]:
    """rewrite_fn for trust.loop.run_trust_loop: (script, instructions) -> revised script."""
    def rewrite(script: Script, instructions: list) -> Script:
        return write_script(show_id, show_cfg, stories, pack, llm, revision=script.revision + 1,
                            instructions=instructions, episode_date=episode_date, previous=script,
                            voices=voices)
    return rewrite
