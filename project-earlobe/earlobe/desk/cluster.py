"""Story clustering: many Signals about one event become one Story.

Greedy and deterministic. Signals are taken oldest first; each joins the best-matching
open cluster of the same market (title-shingle Jaccard >= JACCARD_MIN against any member,
first signal no more than WINDOW_HOURS earlier) or starts a new one. Shingles are the
normalized title's content words (k=1): on the sample data, headlines of one event score
>= 0.38 and different events <= 0.23, whereas bigram shingles split rephrased headlines.
At least two shared words are required, so one-word overlaps never merge short titles.

Each Story then gets its outlets, independent-outlet count (owner groups, wires and
syndication collapsed), official confirmation (any tier 1 signal), velocity and risk flags.
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from earlobe.desk.independence import get, independent_count
from earlobe.schemas import RISK_FLAGS, Signal, Story, make_id

JACCARD_MIN = 0.35
MIN_SHARED = 2
SHINGLE_K = 1
WINDOW_HOURS = 36
VELOCITY_MINUTES = 60

_STOP = frozenset("""a an the and or of in on at to for from with by as is are was were be been it its
this that these those after over into amid says say said than about up out off will could would may
can has have had not no""".split())
_BRACKETS = re.compile(r"\[[^\]]*\]")
_POSSESSIVE = re.compile(r"['’]s\b")
_WORD = re.compile(r"[a-z0-9]+")


# ---------------------------------------------------------------- time
def parse_time(value) -> datetime | None:
    """ISO-8601 string -> aware UTC datetime (naive input is taken as UTC); None if missing or bad."""
    if not value:
        return None
    try:
        t = datetime.fromisoformat(str(value).strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    return t.replace(tzinfo=timezone.utc) if t.tzinfo is None else t.astimezone(timezone.utc)


def fmt_time(t: datetime | None) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ") if t else ""


# ---------------------------------------------------------------- title matching
def _stem(word: str) -> str:
    """Tiny suffix stripper so approve/approves/approved line up."""
    if word.isdigit() or len(word) <= 3:
        return word
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and not word.endswith("ss") and len(word) - len(suffix) >= 3:
            word = word[: -len(suffix)]
            break
    return word[:-1] if word.endswith("e") and len(word) > 3 else word


def tokens(title: str) -> list[str]:
    """Normalized content words of a title ([TAGS] and possessives dropped)."""
    text = _POSSESSIVE.sub("", _BRACKETS.sub(" ", title or "").lower().replace("’", "'"))
    words = [_stem(w) for w in _WORD.findall(text.replace("'", ""))]
    return [w for w in words if w not in _STOP and (len(w) > 1 or w.isdigit())]


def shingles(title: str, k: int = SHINGLE_K) -> frozenset:
    """Set of k-word shingles of the normalized title (k=1: the content words)."""
    toks = tokens(title)
    if k <= 1:
        return frozenset(toks)
    return frozenset(" ".join(toks[i:i + k]) for i in range(max(len(toks) - k + 1, 1)) if toks)


def jaccard(a: frozenset, b: frozenset) -> float:
    """Jaccard similarity; 0 when fewer than MIN_SHARED shingles overlap."""
    if len(a & b) < MIN_SHARED:
        return 0.0
    return len(a & b) / len(a | b)


def strip_outlet(title: str, outlet: str) -> str:
    """Drop a trailing ' - Outlet' / ' | Outlet' (Google News style) when it names this outlet."""
    for sep in (" - ", " | ", " – ", " — "):
        head, _, tail = title.rpartition(sep)
        if head and tail.strip().casefold() == (outlet or "").strip().casefold():
            return head.strip()
    return title.strip()


# ---------------------------------------------------------------- risk flags
_RISK_RULES = {
    "crime": r"arrest\w*|charged|charges|shooting|shot|stabb\w*|murder\w*|homicide|robber\w*|burglar\w*"
             r"|assault\w*|suspect\w*|indict\w*|kidnap\w*|carjack\w*|manslaughter|gunman|gunmen"
             r"|police say|sheriff'?s? (?:office|deputies)",
    "legal_proceeding": r"courts?|courthouse|judges?|lawsuits?|sues|sued|trial|verdict|sentenc\w*|indict\w*"
                        r"|arraign\w*|pleaded|pleads|plea deal|plea agreement|guilty|jury|juror\w*"
                        r"|motion to dismiss|docket|appealed|appellate|plaintiff\w*|defendant\w*"
                        r"|prosecut\w*|subpoena\w*|injunction|\bv\.|\bvs\.",
    "minor": r"juvenile\w*|minors?|teen\w*|child|children|kids?|boys?|girls?|toddler\w*|infant\w*"
             r"|(?:[0-9]|1[0-7])[- ]year[- ]olds?",
    "victim": r"victims?|survivors?|slain|wounded|injured|killed|fatal\w*|found dead|abuse\w*|assault\w*",
    "death": r"dies|died|dead|death\w*|killed|fatal\w*|obituar\w*|funeral|slain|murder\w*|homicide"
             r"|passed away|passes away",
    "election": r"elections?|ballots?|candidates?|runoff|early voting|voters?|polling"
                r"|primary (?:race|election|vote|results?)",
}
_RISK_RE = {flag: re.compile(rf"(?<!\w)(?:{rules})(?!\w)", re.IGNORECASE) for flag, rules in _RISK_RULES.items()}


def risk_flags(text: str) -> list[str]:
    """Risk flags whose keyword rules match the text (a conservative net: flags make handling stricter)."""
    return [f for f in RISK_FLAGS if f in _RISK_RE and _RISK_RE[f].search(text or "")]


# ---------------------------------------------------------------- clustering
def _mode(values: list):
    """Most common value; ties go to the earliest."""
    counts: dict = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return max(counts, key=lambda v: (counts[v], -values.index(v))) if counts else ""


def _order(sig: Signal):
    t = parse_time(sig.published_at)
    return (t is None, t or datetime.max.replace(tzinfo=timezone.utc), sig.id)


class _Cluster:
    def __init__(self, sig: Signal):
        self.market = sig.market or ""
        self.first = parse_time(sig.published_at)
        self.signals: list[Signal] = []
        self.shingles: list[frozenset] = []
        self.add(sig)

    def add(self, sig: Signal) -> None:
        self.signals.append(sig)
        self.shingles.append(shingles(strip_outlet(sig.title, sig.outlet)))
        if self.first is None:
            self.first = parse_time(sig.published_at)

    def similarity(self, sig: Signal, sh: frozenset) -> float:
        """Best Jaccard against any member, 0 if the market differs or the time gap is too big."""
        if (sig.market or "") != self.market:
            return 0.0
        t = parse_time(sig.published_at)
        if t and self.first and abs(t - self.first) > timedelta(hours=WINDOW_HOURS):
            return 0.0
        return max(jaccard(sh, m) for m in self.shingles)


def cluster(signals: list[Signal], owners: dict) -> list[Story]:
    """Group signals into Stories (oldest first). Never merges across markets."""
    seen, unique = set(), []
    for sig in sorted(signals or [], key=_order):
        if sig.id not in seen:
            seen.add(sig.id)
            unique.append(sig)

    clusters: list[_Cluster] = []
    for sig in unique:
        sh = shingles(strip_outlet(sig.title, sig.outlet))
        best, best_sim = None, 0.0
        for c in clusters:
            sim = c.similarity(sig, sh)
            if sim >= JACCARD_MIN and sim > best_sim:
                best, best_sim = c, sim
        if best is None:
            clusters.append(_Cluster(sig))
        else:
            best.add(sig)
    return [_story(c, owners) for c in clusters]


def _story(c: _Cluster, owners: dict) -> Story:
    sigs = c.signals                                   # already oldest first
    first = c.first
    titles = [strip_outlet(s.title, s.outlet) for s in sigs]
    norm = [" ".join(tokens(t)) for t in titles]
    headline = titles[norm.index(_mode(norm))]

    with_summary = [s for s in sigs if (s.summary or "").strip()]
    best = min(with_summary, key=lambda s: (s.tier, sigs.index(s)), default=None)
    summary = best.summary.strip() if best else ""

    outlets = list(dict.fromkeys(s.outlet for s in sigs if s.outlet))
    early_end = first + timedelta(minutes=VELOCITY_MINUTES) if first else None
    early = [s for s in sigs if first and (t := parse_time(s.published_at)) and first <= t <= early_end]

    return Story(
        id=make_id("sty", c.market, sigs[0].id),
        market=c.market,
        beat=_mode([s.beat for s in sigs if s.beat]),
        headline=headline,
        summary=summary,
        first_seen=fmt_time(first),
        signal_ids=[s.id for s in sigs],
        source_ids=list(dict.fromkeys(make_id("src", s.url) for s in sigs if s.url)),
        outlets=outlets,
        independent_outlets=independent_count(sigs, owners),
        official_confirmation=any(s.tier == 1 for s in sigs),
        velocity=float(independent_count(early, owners)) / (VELOCITY_MINUTES / 60),
        risk_flags=risk_flags(" . ".join(dict.fromkeys(titles)) + " . " + summary),
    )
