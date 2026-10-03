# Kindling — Production files

Everything needed to print Kindling, from a home prototype to a factory run.

## What's here

| Path | What it is | Use it for |
|---|---|---|
| `deck/*.json` | **Source of truth** for every card (text, type, heat, time, match, aftercare) and the 4 rules cards | Editing cards |
| `kindling-cards.csv` | All 334 cards, one row each | Manufacturer quotes, proofreading, sensitivity reads |
| `print/kindling-prototype-embers-letter.pdf` | Embers + rules on US Letter, 9 per sheet, fronts and backs alternating, crop marks | Home or office prototype |
| `print/kindling-prototype-wildfire-slowburn-letter.pdf` | Wildfire + Slow Burn, same layout | Home prototype |
| `print/kindling-prototype-afterdark-letter.pdf` | After Dark (18+), same layout | Home prototype |
| `print/kindling-press-<deck>-fronts.pdf` | One card per page, 69 × 94 mm (63 × 88 trim + 3 mm bleed), Embers file starts with the rules cards | Printer and manufacturer upload |
| `print/kindling-press-backs.pdf` | One back per deck (Embers, Wildfire, Slow Burn, After Dark, Rules), 69 × 94 mm | Printer and manufacturer upload |

## Specs

- **Card:** poker size, 63 × 88 mm trim, 3 mm bleed, about 3 mm corner radius (die-cut by the printer; the press files are square)
- **Safe area:** text stays ≥ 4.7 mm inside the trim
- **Stock:** 310 gsm black-core, linen finish (black core stops cards showing through)
- **Color:** RGB PDFs. Ask the printer to convert, or to send a hard proof. Deck colors: Embers `#FF6A2B`, Wildfire `#E2363B`, Slow Burn `#E2728A`, After Dark `#B88CFF` on `#1A0F22`, Rules `#FFC24B`
- **Type:** Fraunces (card prompts) and Archivo (labels), both SIL Open Font License, embedded in the PDFs
- **Counts:** Embers 150 + 4 rules = 154 · Wildfire 60 · Slow Burn 60 · After Dark 60

## Print a prototype tonight

1. Open a `print/kindling-prototype-*-letter.pdf`.
2. Print at **100% / actual size**, **double-sided, flip on long edge**, on 110 lb (300 gsm) white cardstock.
3. Cut on the crop marks with a paper trimmer, and round the corners with a 3 mm corner punch if you have one.
4. Odd pages are fronts and even pages are backs. Backs are mirrored so they line up after the flip.

## Order a professional proof

- **MakePlayingCards.com:** "Poker size, custom cards". They take images per card. Run `node scripts/kindling_print.mjs --png` for 300 dpi PNGs (written to `print/png/`, not committed).
- **The Game Crafter:** "Poker Deck" + "Poker Tuck Box". Upload PNGs per card. They can also sell and ship print-on-demand from their own storefront.
- **Factory runs (Delano, Longpack, etc.):** send `kindling-cards.csv` and the press PDFs with your quote request. They'll supply a box dieline, and the box art lives on the site (`site/kindling/kindling.js`, `K.boxHTML`) as a starting point.

## Change a card

```bash
# 1. edit Production/Kindling/deck/<deck>.json
python3 scripts/build_kindling.py          # rebuilds the site data + CSV, fails on duplicate text
node scripts/kindling_print.mjs --check    # confirms every card still fits at print size
node scripts/kindling_print.mjs            # regenerates every PDF
```

The website, the free digital game, the gallery, and the PDFs all read the
same compiled deck, so one edit updates everything.
