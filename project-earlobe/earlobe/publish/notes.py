"""Show notes: what listeners can check.

show_notes(script, decision, copy) returns markdown with, in order:
  the episode summary, chapters (times estimated from the script), numbered Sources
  (outlet + link, every source the script used), "How we checked this" (the gate's scores in
  plain language), corrections, and the AI disclosure line.

The sources, verification summary, corrections and disclosure are built here from the
Script and the GateDecision, never taken from the copywriter's text, so they cannot drift.
notes_html() turns the markdown into simple, safe HTML for the feed's content:encoded.
"""
from __future__ import annotations

import html
import re

from earlobe import config
from earlobe.publish import coerce, disclosure_text
from earlobe.publish import corrections_url as default_corrections_url
from earlobe.schemas import Correction, Script, Source
from earlobe.studio import est_seconds

SEGMENT_LABELS = {"cold_open": "Cold open", "intro": "Intro", "kicker": "One more thing",
                  "disclosure": "AI disclosure", "outro": "Outro"}


def _g(obj, key, default=None):
    """Field from a dataclass or a dict."""
    value = obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)
    return default if value is None else value


def _md_text(text: str) -> str:
    return str(text).replace("[", "(").replace("]", ")")


def _md_link(text: str, url: str) -> str:
    safe = url.strip().replace(" ", "%20").replace("(", "%28").replace(")", "%29")
    return f"[{_md_text(text)}]({safe})"


def _clock(seconds: float) -> str:
    s = int(seconds)
    h, rem = divmod(s, 3600)
    m, sec = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"


# ---------------------------------------------------------------- sources
def sources_used(script: Script) -> list[Source]:
    """Every source of the script, deduped by URL: cited ones first (in order of first use), then the rest."""
    sources = [coerce(Source, s) for s in script.sources]
    by_id = {s.id: s for s in sources}
    ordered: list[Source] = []
    seen: set[str] = set()

    def add(s: Source) -> None:
        key = s.url or s.id
        if key not in seen:
            seen.add(key)
            ordered.append(s)

    for claim in script.claims:
        for sid in claim.source_ids:
            if sid in by_id:
                add(by_id[sid])
    for s in sources:
        add(s)
    return ordered


def _source_line(n: int, s: Source) -> str:
    label = s.title or s.url
    tag = " (primary record)" if s.tier == 1 else ""
    return f"{n}. {_md_text(s.outlet or 'Unknown outlet')}{tag}: {_md_link(label, s.url)}"


def independent_sources(sources: list[Source]) -> int:
    """Distinct owner groups among tier 1-3 sources, syndicated copies collapsed (the gate's definition)."""
    return len({s.owner_group or s.outlet for s in sources if s.tier <= 3 and not s.syndicated_from})


# ---------------------------------------------------------------- chapters
def _chapter_title(text: str, limit: int = 70) -> str:
    """First real sentence of the line, cut at a word boundary."""
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", " ".join(text.split())) if len(s.split()) >= 4]
    title = sentences[0] if sentences else " ".join(text.split())
    if len(title) <= limit:
        return title.rstrip(".")
    return title[:limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


def chapters(script: Script, duration_sec: int | None = None) -> list[tuple[int, str]]:
    """[(start_seconds, title)]. Non-body segments get fixed labels; body lines are grouped by shared sources.

    Times come from the script's word count; pass duration_sec (the rendered length) to scale
    them to the real audio.
    """
    claims = {c.id: c for c in script.claims}
    found: list[list] = []
    clock = 0.0
    last_segment = None
    group: set = set()
    for line in script.lines:
        start = clock
        clock += est_seconds(line.text)
        if line.segment != "body":
            if line.segment != last_segment:
                found.append([start, SEGMENT_LABELS.get(line.segment, line.segment.replace("_", " ").title())])
            group = set()
        else:
            ids = {sid for cid in line.claim_ids if cid in claims for sid in claims[cid].source_ids}
            if last_segment != "body" or (group and ids and not ids & group):
                found.append([start, _chapter_title(line.text)])
                group = set(ids)
            else:
                group |= ids
        last_segment = line.segment
    scale = duration_sec / clock if duration_sec and clock else 1.0
    return [(int(start * scale), title) for start, title in found]


# ---------------------------------------------------------------- verification summary
def _pct(value) -> str:
    return f"{round(float(value) * 100)}%" if isinstance(value, (int, float)) else "not measured"


def verification_lines(script: Script, decision, sources: list[Source]) -> list[str]:
    scores = _g(decision, "scores", {}) or {}
    lane = _g(decision, "lane_policy", "") or script.lane_policy
    revision = int(_g(decision, "revision", script.revision) or 0)
    claims = scores.get("claims", len(script.claims))
    independent = scores.get("independent_sources", independent_sources(sources))
    rewrites = ("None. The first draft passed." if revision == 0 else
                f"{revision} (the script was rewritten {revision} time{'s' if revision != 1 else ''} "
                "and every check was re-run from scratch)")
    return [
        (f"- **Corroboration rate:** {_pct(scores.get('corroboration_rate'))} of the claims that need sources "
         f"({claims} claims in all) were backed by enough independent sources under the \"{lane}\" policy."),
        (f"- **Independent sources:** {independent} (outlets with different owners; syndicated copies "
         "of the same story count once)."),
        (f"- **Accuracy:** {_pct(scores.get('accuracy_rate'))} of the rated claims came back accurate "
         "or with only a minor issue."),
        f"- **Balance score:** {scores.get('balance_score', 'not measured')} out of 100.",
        f"- **Rewrites:** {rewrites}",
        f"- **Gate decision:** {_g(decision, 'decision', 'unknown')}.",
    ]


# ---------------------------------------------------------------- the notes
def show_notes(script: Script, decision, copy: dict | None = None, *, duration_sec: int | None = None,
               corrections: list | None = None, disclosure: str | None = None,
               corrections_link: str | None = None) -> str:
    """Markdown show notes for one episode.

    decision: the GateDecision (or its dict). copy: the Copy dict from the copywriter (optional).
    corrections: Correction records already applied to this episode, listed with their dates.
    """
    script = coerce(Script, script)
    copy = copy or {}
    sources = sources_used(script)
    link = corrections_link or default_corrections_url(script.show_id)

    summary = copy.get("description") or script.title
    parts = [str(summary).strip()]

    extra = (copy.get("show_notes_md") or "").strip()
    if extra:
        parts.append(extra if extra.startswith("#") else "## In this episode\n\n" + extra)

    chapter_list = chapters(script, duration_sec)
    if chapter_list:
        parts.append("## Chapters\n\n" + "\n".join(f"- {_clock(t)} {_md_text(title)}" for t, title in chapter_list))

    parts.append("## Sources\n\n" + ("\n".join(_source_line(i, s) for i, s in enumerate(sources, 1))
                                     if sources else "No outside sources were used for this episode."))

    parts.append("## How we checked this\n\nBefore this episode was published, automated systems compared "
                 "its claims against independent sources and applied our written standards. The result:\n\n"
                 + "\n".join(verification_lines(script, decision, sources)))

    fixes = [coerce(Correction, c) for c in (corrections or [])]
    corr = ["## Corrections", "",
            f"We fix mistakes in the open. See {_md_link('corrections and how to report an error', link)}."]
    if fixes:
        corr += [""] + [f"- {(c.created_at or '')[:10] or 'undated'} ({c.action}): {_md_text(c.description)}"
                         for c in fixes]
    parts.append("\n".join(corr))

    disclosure = disclosure or disclosure_text(config.load_shows().get(script.show_id))
    parts.append("---\n\n**AI disclosure:** " + disclosure)
    return "\n\n".join(parts) + "\n"


# ---------------------------------------------------------------- markdown -> HTML (small, safe)
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_SAFE_HREF = re.compile(r"^(https?://|mailto:|/)")


def _inline(text: str) -> str:
    text = html.escape(text, quote=True)
    text = _LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>'
                     if _SAFE_HREF.match(html.unescape(m.group(2))) else m.group(1), text)
    return _BOLD.sub(r"<strong>\1</strong>", text)


def notes_html(md: str) -> str:
    """Headings, paragraphs, bullet and numbered lists, rules, links and bold. Everything is HTML-escaped."""
    out: list[str] = []
    para: list[str] = []
    open_list = ""

    def close() -> None:
        nonlocal open_list
        if para:
            out.append("<p>" + " ".join(para) + "</p>")
            para.clear()
        if open_list:
            out.append(f"</{open_list}>")
            open_list = ""

    for raw in md.splitlines():
        line = raw.strip()
        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        bullet = re.match(r"^[-*]\s+(.*)$", line)
        number = re.match(r"^\d+\.\s+(.*)$", line)
        if heading:
            close()
            level = min(len(heading.group(1)) + 1, 6)
            out.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
        elif bullet or number:
            kind = "ul" if bullet else "ol"
            if open_list != kind:
                close()
                out.append(f"<{kind}>")
                open_list = kind
            out.append(f"<li>{_inline((bullet or number).group(1))}</li>")
        elif line == "---":
            close()
            out.append("<hr/>")
        elif not line:
            close()
        else:
            if open_list:
                close()
            para.append(_inline(line))
    close()
    return "\n".join(out)
