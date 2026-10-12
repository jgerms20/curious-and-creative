"""Copywriter: title, description, show notes and social copy for an episode that has PASSED the gate.

Sonnet tier. It sees only the final script's spoken lines (never reports, sources or instructions),
so the copy cannot promise or name anything the trust stack cut. After the model answers, code
checks the one thing that is cheap to check: every number in the copy must appear in the script.
A stray number triggers one retry; if it persists, the offending social posts and keywords are
dropped and a plain title, description and notes built from the script itself replace the rest.

The source list and verification summary are added by publish/notes.py and the AI disclosure by the
publish step, so the model is told not to write either.

Dry-run: fixtures.fake("Copy") builds the copy from the script.
"""
from __future__ import annotations

import re

from earlobe import config
from earlobe.schemas import Script, validate

COPY_SYSTEM = """\
You are the Copywriter for the Curious & Creative Network, an automated news audio network. You write the words that get an episode chosen in podcast apps, search and social feeds.

YOUR SITUATION
The script you are given has already passed every check: sourcing, fact-checking, fairness and legal review. Your copy has not. Nobody reads it before it goes out, and it is held to the same standard as the audio. You work only from the script. If something is not in the script, it does not exist.

RULES
1. Every fact in your copy must be in the script: each name, number, date, place, quote and legal status. Add nothing from memory or from the show's usual topics. Do not invent a number, a ranking, a "first", or a time. A number in your copy that is not in the script is a defect.
2. Keep the script's precision. Same legal words (arrested on suspicion of, charged with, pleaded not guilty), same attribution ("police said", "according to the county"). Never state as fact what the script attributes to someone. A person charged with a crime is never described as guilty, "the killer" or "the suspect behind". Never name anyone the script does not name, and never add an identifying detail. If the script says "a teenager", so do you.
3. Clear beats clever. No clickbait: no cliffhangers, no questions that insinuate, no "shocking", "you won't believe", "bombshell", "exclusive", no ALL CAPS, no exclamation marks, no emoji. "Breaking" only for a breaking flash. Do not describe hosts as people or reporters.
4. title: 70 characters or fewer. Lead with the most specific, newsworthy fact of the top story, or the show name and the date when the show is a daily brief. Plain words a listener would search for. No colon-stuffed subtitles.
5. description: 300 characters or fewer, plain text. The first sentence is the hook: the most important thing the episode tells you, with attribution if it is an account. Then what else is covered.
6. show_notes_md: Markdown. A short "## In this episode" list, one bullet per story: what happened and who says so, one or two sentences. Do NOT list sources, links, timestamps, the AI disclosure or the verification summary; the publishing step adds those.
7. social_posts: two to four posts of 270 characters or fewer, each standing alone, each saying what happened with attribution. No links. At most one hashtag per post.
8. keywords: six to twelve lowercase search phrases (places, topics, the show name), using only words that appear in the script or the show's name.
Return only the JSON object.
"""

LIMITS = {"title": 120, "description": 600, "social": 280, "keywords": 12}
_NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _numbers(text: str) -> set[str]:
    return {m.rstrip(",").replace(",", "") for m in _NUM.findall(text or "")}


def _clip(text: str, n: int) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= n else text[:n - 1].rstrip() + "…"


def spoken_text(script: Script) -> str:
    """The episode's spoken lines (disclosure excluded), one per line."""
    return "\n".join(l.text for l in script.lines if l.segment != "disclosure")


def _fields(copy: dict) -> list[str]:
    return [copy.get("title", ""), copy.get("description", ""), copy.get("show_notes_md", ""),
            *copy.get("social_posts", []), *copy.get("keywords", [])]


def stray_numbers(copy: dict, script: Script, show_cfg: dict) -> set[str]:
    """Numbers used in the copy that appear nowhere in the script (or the date and show name)."""
    allowed = _numbers(f"{spoken_text(script)} {script.title} {script.episode_date} {show_cfg.get('name', '')}")
    return {n for f in _fields(copy) for n in _numbers(f)} - allowed


def _prompt(script: Script, show_cfg: dict) -> str:
    market = config.load_markets().get(show_cfg.get("market", ""), {})
    body = "\n".join(f"[{l.speaker}] {l.text}" for l in script.lines if l.segment != "disclosure")
    return (f"SHOW: {show_cfg.get('name', script.show_id)} ({show_cfg.get('format', 'unspecified')}), "
            f"market {market.get('name', show_cfg.get('market', 'unspecified'))}\n"
            f"EPISODE DATE: {script.episode_date}\nSCRIPT TITLE: {script.title}\n\n"
            f"SCRIPT (spoken lines):\n{body}\n\nWrite the copy now.")


def _fallback(script: Script, show_cfg: dict) -> dict:
    """Plain copy built from the script itself, used when the model's copy cannot be trusted."""
    body = [l.text for l in script.lines if l.segment == "body"]
    lead = body[0] if body else script.title
    return {"title": _clip(script.title, LIMITS["title"]),
            "description": _clip(lead, 300),
            "show_notes_md": "## In this episode\n" + "\n".join(f"- {_clip(t, 200)}" for t in (body[::2] or [lead])),
            "social_posts": [_clip(lead, 270)],
            "keywords": [k for k in (show_cfg.get("name", "").lower(), show_cfg.get("market", "")) if k]}


def _clean(raw: dict) -> dict:
    keywords = list(dict.fromkeys(" ".join(str(k).split()).lower() for k in raw.get("keywords", []) if str(k).strip()))
    return {"title": _clip(raw.get("title"), LIMITS["title"]),
            "description": _clip(raw.get("description"), LIMITS["description"]),
            "show_notes_md": str(raw.get("show_notes_md") or "").strip(),
            "social_posts": [_clip(p, LIMITS["social"]) for p in raw.get("social_posts", []) if str(p).strip()],
            "keywords": keywords[:LIMITS["keywords"]]}


def write_copy(script: Script, show_cfg: dict, llm) -> dict:
    """Listing copy (the `Copy` schema) for a gated script. Call only after the gate said PUBLISH."""
    user = _prompt(script, show_cfg)
    ctx = {"script": script, "show_cfg": show_cfg}
    copy = _clean(llm.structured("copywriter", "sonnet", COPY_SYSTEM, user, "Copy", effort="low", ctx=ctx))
    strays = stray_numbers(copy, script, show_cfg)
    if strays:
        retry = (f"{user}\n\nYour last draft used numbers that are not in the script: "
                 f"{', '.join(sorted(strays))}. Rewrite the copy using only numbers that appear in the script.")
        copy = _clean(llm.structured("copywriter", "sonnet", COPY_SYSTEM, retry, "Copy", effort="low", ctx=ctx))
        strays = stray_numbers(copy, script, show_cfg)
    if strays:
        plain = _fallback(script, show_cfg)
        copy = {"title": plain["title"], "description": plain["description"],
                "show_notes_md": plain["show_notes_md"],
                "social_posts": [p for p in copy["social_posts"] if not _numbers(p) & strays] or plain["social_posts"],
                "keywords": [k for k in copy["keywords"] if not _numbers(k) & strays]}
    problems = validate("Copy", copy)
    if problems:
        raise ValueError(f"copy failed validation: {problems}")
    return copy
