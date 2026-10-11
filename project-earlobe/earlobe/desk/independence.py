"""Source independence: which outlets count as separate voices.

An outlet's owner group comes from config/owners.yaml (see config.load_owners()).
Wire services (AP, Reuters, ...) are their own group, and a copy syndicated from a
wire (or from any other outlet) collapses into the origin's group. Tier 4 sources
(aggregators, social, unverified) never count toward corroboration.

Conservative by design: when in doubt, items collapse into one group, so the count
can only err low. The verifier and the Story Desk both use independent_count().
"""
from __future__ import annotations

import re
from urllib.parse import urlparse

# Extra spellings per wire (lowercase wire name -> aliases). "ap" only matches as the
# uppercase word AP inside a free-text note; everywhere else matching is case-insensitive.
WIRE_ALIASES = {
    "associated press": ["ap", "ap news", "apnews", "apnews.com"],
    "reuters": ["reuters.com"],
    "afp": ["afp.com", "agence france-presse"],
    "bloomberg": ["bloomberg.com", "bloomberg news"],
}


def get(obj, key: str, default=None):
    """Field from a dataclass or a dict (None counts as missing)."""
    value = obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)
    return default if value is None else value


def _key(name) -> str:
    """Lookup key: lowercase host for URLs and www. names, else the lowercase name."""
    s = str(name or "").strip()
    if "://" in s:
        s = urlparse(s).netloc or s
    s = s.lower()
    return s[4:] if s.startswith("www.") else s


class _Index:
    """Case-insensitive outlet/domain -> group lookup, plus patterns that spot a wire in a note."""

    def __init__(self, owners: dict | None):
        owners = owners or {}
        self.lookup: dict[str, str] = {}
        self.wire_patterns: list[tuple[re.Pattern, str]] = []
        for owner, members in (owners.get("groups") or {}).items():
            self.lookup[_key(owner)] = owner
            for m in members or []:
                self.lookup[_key(m)] = owner
        for wire in owners.get("wires") or []:
            names = [wire] + WIRE_ALIASES.get(wire.lower(), [])
            for n in names:
                self.lookup[_key(n)] = wire
                flags = 0 if n == "ap" else re.IGNORECASE
                text = "AP" if n == "ap" else n
                self.wire_patterns.append((re.compile(rf"(?<![\w.]){re.escape(text)}(?![\w])", flags), wire))

    def find(self, name) -> str | None:
        """Group for a known outlet name or domain (subdomains fall back to the parent), else None."""
        k = _key(name)
        while k:
            if k in self.lookup:
                return self.lookup[k]
            if "." not in k or " " in k:
                return None
            k = k.split(".", 1)[1]
        return None

    def wire_in(self, text: str) -> str | None:
        for pattern, wire in self.wire_patterns:
            if pattern.search(text or ""):
                return wire
        return None


def owner_group(outlet: str, owners: dict) -> str:
    """Owner group for an outlet name or domain (case-insensitive).

    Wires map to the wire itself; unknown outlets are their own group.
    """
    found = _Index(owners).find(outlet)
    if found:
        return found
    s = str(outlet or "").strip()
    return _key(s) if "://" in s else s


def _syndication_origin(item, index: _Index) -> str:
    """Who this copy came from: an explicit syndicated_from, or a wire named in the evidence note."""
    origin = get(item, "syndicated_from", "") or get(get(item, "raw", {}), "syndicated_from", "")
    if origin:
        return str(origin)
    return index.wire_in(str(get(item, "note", ""))) or ""


def _group_of(item, index: _Index) -> str:
    """Effective group of one item after syndication collapse ('' if it names nobody)."""
    origin = _syndication_origin(item, index)
    if origin:
        found = index.find(origin)
        return found or (_key(origin) if "://" in origin else origin.strip())
    outlet = str(get(item, "outlet", "") or "").strip() or _key(get(item, "url", ""))
    found = index.find(outlet)
    if found:
        return found
    return str(get(item, "owner_group", "") or "").strip() or outlet   # config doesn't know it: trust the item's own label


def _tier(item) -> int:
    try:
        return int(get(item, "tier", 3))
    except (TypeError, ValueError):
        return 4   # unreadable tier: do not count


def independent_count(evidence_or_sources, owners: dict, max_tier: int = 3) -> int:
    """Distinct owner groups among Sources, EvidenceSources or Signals (objects or dicts).

    - same owner group counts once; syndicated copies count as their origin
    - tier above max_tier (default: tier 4) is ignored
    - evidence with supports=False is ignored
    """
    index = _Index(owners)
    groups = set()
    for item in evidence_or_sources or []:
        if _tier(item) > max_tier or get(item, "supports", True) is False:
            continue
        g = _group_of(item, index)
        if g:
            groups.add(g.casefold())
    return len(groups)
