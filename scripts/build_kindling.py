#!/usr/bin/env python3
"""Compile the Kindling deck.

Source of truth: Production/Kindling/deck/*.json (edit cards there).
Writes:
  site/data/kindling-cards.json       — what the website, game, and print sheets read
  Production/Kindling/kindling-cards.csv — one row per card, for manufacturers and spreadsheets

Run from the repo root:  python3 scripts/build_kindling.py
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "Production" / "Kindling" / "deck"
OUT_JSON = ROOT / "site" / "data" / "kindling-cards.json"
OUT_CSV = ROOT / "Production" / "Kindling" / "kindling-cards.csv"

DECKS = [
    {
        "id": "embers", "code": "E", "name": "Embers", "kind": "The core deck",
        "files": ["embers-talk", "embers-action"], "multiplier": 1,
        "blurb": "Questions, confessions, touch, play, and dares. Everything you need for a first night, or a hundredth.",
    },
    {
        "id": "wildfire", "code": "W", "name": "Wildfire", "kind": "Challenges pack",
        "files": ["wildfire"], "multiplier": 2,
        "blurb": "Big, one-time, story-you'll-tell-later challenges. Role reversals, classes, hotel nights, naked Twister.",
    },
    {
        "id": "slowburn", "code": "S", "name": "Slow Burn", "kind": "Dates & rituals pack",
        "files": ["slowburn"], "multiplier": 2,
        "blurb": "Rituals, dates, and slow sensual evenings. Read to them in the bath. Wash their hair. Take your time.",
    },
    {
        "id": "afterdark", "code": "A", "name": "After Dark", "kind": "18+ exploration pack",
        "files": ["afterdark"], "multiplier": 2, "adult": True,
        "blurb": "Kink and power play for couples and groups, with negotiation and aftercare printed on every card.",
    },
]

TYPE_ORDER = ["ask", "tell", "notice", "touch", "tend", "play", "dare", "wild",
              "challenge", "reversal", "group", "ritual", "date", "sensual",
              "negotiate", "power", "sensation", "roleplay"]
TYPE_LABEL = {"wild": "Wild card", "group": "Group", "negotiate": "Negotiate"}


def main():
    cards = []
    for deck in DECKS:
        items = []
        for f in deck["files"]:
            items += json.loads((SRC / f"{f}.json").read_text())
        items.sort(key=lambda c: (TYPE_ORDER.index(c["type"]), c["heat"]))
        for n, c in enumerate(items, 1):
            card = {
                "id": f"{deck['code']}{n:03d}",
                "deck": deck["id"],
                "type": c["type"],
                "label": TYPE_LABEL.get(c["type"], c["type"].capitalize()),
                "heat": c["heat"],
                "sparks": 0 if c["type"] == "wild" else c["heat"] * deck["multiplier"],
                "text": c["text"].strip(),
                "time": c.get("time", ""),
                "pairing": c.get("pairing", "partners"),
                "players": c.get("players", "2+"),
            }
            for k in ("match", "aftercare", "effect"):
                if c.get(k):
                    card[k] = c[k]
            cards.append(card)
        deck["count"] = len(items)

    rules = []
    for n, r in enumerate(json.loads((SRC / "rules.json").read_text()), 1):
        rules.append({"id": f"R{n:02d}", "deck": "rules", "type": "rules", "label": "Rules",
                      "title": r["title"], "html": r["html"]})

    ids = [c["id"] for c in cards]
    assert len(ids) == len(set(ids))
    texts = [c["text"].lower() for c in cards]
    assert len(texts) == len(set(texts)), "duplicate card text"

    decks_out = [{k: v for k, v in d.items() if k not in ("files", "code")} for d in DECKS]
    OUT_JSON.write_text(json.dumps({"decks": decks_out, "rules": rules, "cards": cards},
                                   ensure_ascii=False, separators=(",", ":")))

    with OUT_CSV.open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "deck", "type", "heat", "sparks", "match", "players", "pairing", "time", "text", "aftercare"])
        for c in cards:
            w.writerow([c["id"], c["deck"], c["label"], c["heat"], c["sparks"], "yes" if c.get("match") else "",
                        c["players"], c["pairing"], c["time"], c["text"], c.get("aftercare", "")])
        for r in rules:
            w.writerow([r["id"], "rules", "Rules", "", "", "", "", "", "", re.sub(r"<[^>]+>", " ", r["html"]).replace("&amp;", "&").replace("&ldquo;", '"').replace("&rdquo;", '"'), ""])

    for d in DECKS:
        print(f"{d['name']:<11} {d['count']:>3} cards")
    print(f"{'Rules':<11} {len(rules):>3} cards")
    print(f"Total      {len(cards) + len(rules):>4} → {OUT_JSON.relative_to(ROOT)}, {OUT_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
