# Kindling — Manufacturing & Fulfillment Plan

A step-by-step from "we have a deck design" to "boxes are shipping."

> **Trademark risk to check first.** "Kindling" is a common English word, and
> Amazon holds many KINDLE registrations. Before spending on packaging, have a
> trademark attorney run a clearance search for KINDLING in Class 28 (games).
> Check for existing games with the name and for likelihood-of-confusion risk
> with KINDLE. Have a backup name ready. A stylized wordmark plus the flame mark
> is more defensible than the plain word.

---

## Fast track: first boxes in about 30 days

The deck is written, edited, and laid out. Print-ready files are in
`Production/Kindling/print/` (see `Production/Kindling/README.md`). The fastest
path to real boxes in real hands:

| Week | Do this | Cost |
|---|---|---|
| 1 | **Print a home prototype tonight.** Print the `kindling-prototype-*-letter.pdf` files duplex on 110 lb cardstock (flip on the long edge), cut on the crop marks, and play it with 3–4 friend groups. Note every card that stalls. | ~$20 |
| 1 | **Order a real proof.** Upload the press PDFs to MakePlayingCards (or The Game Crafter, which also sells and ships for you) as a poker-size deck with a tuck box. | $25–60 per deck |
| 1 | **Start the trademark clearance** (see the note above) and file once it's clear. | $350–1,500 |
| 2 | **Turn on pre-orders.** The shop at `/kindling/shop.html` already takes reservations. Paste a Formspree endpoint into `site/data/kindling-shop.json` so they land in your inbox (`Strategy/Kindling/shop-setup.md`). | $0 |
| 2–3 | **Get 3 manufacturer quotes** for 1,000 core decks + 500 of each expansion (Step 3 below). Send them `kindling-cards.csv` and the press PDFs. | $0 |
| 3 | **Seed 20 proof decks** to therapists, creators, and podcasts (`marketing-plan.md`). | ~$800 |
| 4 | **Pay the deposit** on the first run, or, if pre-orders are thin, sell print-on-demand through The Game Crafter while you build demand. | 30–50% of run |

Edits are cheap: change a card in `Production/Kindling/deck/*.json`, then run
`python3 scripts/build_kindling.py && node scripts/kindling_print.mjs`. The
website, the free game, and every PDF update together.

---

## Step 0 — Trademark & legal (parallel track)

- File a USPTO trademark for **KINDLING** in Class 28 (games & playthings)
  and Class 41 (entertainment). Use a flat-fee filing service
  (LegalZoom / Trademark Engine / a TM-focused attorney — ~$350–$1,500).
- Search the USPTO's Trademark Search system first (it replaced TESS in 2023) — "Kindling" is a common word; we will likely
  need a stylized mark + tagline ("Kindling: a game for pairings") for a
  defensible filing.
- Register **Curious & Creative LLC** as the owning entity on the
  application. Confirm the LLC is in good standing.
- File a copyright on the **card text + rules booklet** as a collective
  work. ($65 online, single application.)
- Add an "intended for adults" notice to the **After Dark** (18+) packaging and
  to its product page. Confirm compliance with Stripe/Shopify adult-product
  rules if you accept payments directly.

---

## Step 1 — Finalize the deck

- ✅ Card counts locked: Embers 150 + 4 rules, Wildfire 60, Slow Burn 60,
  After Dark 60. Full text in `Production/Kindling/kindling-cards.csv`.
- Run an internal playtest with 4–6 friend-pairings across orientations.
  Pay them in pizza. Capture which cards stalled.
- Edit pass on every card for: gender neutrality, clarity in 2 seconds,
  no inside-jokes that don't land.
- Sensitivity / inclusivity read: hire a queer sex educator for a 1-hour
  paid read of After Dark and Embers. (~$200–$500.)

---

## Step 2 — Design files

- Card size: **63mm × 88mm** (poker, the standard for printed card games).
  Box opens to a tuck-flap or a magnetic two-piece box.
- Bleed: 3mm on all sides. Safe area: 5mm inside the trim.
- Color: CMYK only, no spot colors for v1 to keep cost down.
- File deliverables to the manufacturer:
  - One PDF per card (front + back) OR a single multi-page PDF with bleed.
  - Box dieline (the manufacturer supplies this).
  - Rules booklet PDF (A6, 16 pages including consent insert).
  - Outer-wrap art if doing shrinkwrap with a belly-band.

---

## Step 3 — Manufacturer selection

Get quotes from three. We want a real game manufacturer, not a
print-on-demand site (POD card stock feels bad in the hand).

Quote-worthy vendors:
- **Delano (US)** — Texas, family-run, used by many indie game makers,
  reasonable MOQs (500–1,000 units).
- **Whitebox / WhitsEnd Publishing** — handles small runs, transparent
  pricing.
- **Ningbo BeiYa / Longpack (China)** — cheaper per-unit at 2,000+ units,
  4–6 week sea freight.
- **MakePlayingCards / MPC** — fine for prototyping a handful of decks at
  v0 quality; not the final-run vendor.

What to ask each quote:
- Per-unit cost at MOQ, 1k, 2k, 5k.
- Card stock options (we want **310gsm linen-finish black-core**).
- Box options (tuck box vs. two-piece rigid).
- Booklet binding (saddle-stitch vs. folded).
- Lead time from final files → delivered pallet.
- Sample / pre-production proof cost.

Target: **landed cost ≤ 25%** of retail. If retail is $39 for the base
deck, landed cost target is ≤ $9.75.

---

## Step 4 — Prototype run

- Order a **proof copy** from the chosen manufacturer (typically $50–$200
  for one set of decks). Hold it. Shuffle it. Spill on it.
- Run a second playtest with the *physical* proof. People play
  differently with a real deck than with a Figma PDF.

---

## Step 5 — Production run

- Recommended first run: **1,000 units of Embers (the core deck)**, **500 of each
  add-on**. Enough to test demand, small enough to absorb if a card
  needs an edit.
- Pay 30–50% deposit, balance on delivery.
- Lead time: 4–8 weeks domestic, 8–12 weeks overseas + freight.

---

## Step 6 — Fulfillment

Pick one of three models, in order of preference:

1. **3PL (recommended for >500 units).** ShipBob, ShipMonk, or a smaller
   shop like ShipHero. Pallets ship from manufacturer to 3PL. Shopify /
   web orders pick from the 3PL automatically.
2. **At-home fulfillment.** Works up to ~50 orders/week. Pallets in the
   garage. USPS/UPS pickup. Cheapest, most personal — handwritten note
   in every box is on-brand.
3. **Sell wholesale to specialty stores** (sex-positive shops, indie
   gift stores, queer bookstores). 50% margin to retailer is standard
   in this category.

---

## Step 7 — Storefront

- **Shopify** for v1 — fastest path to "I can take orders today." Use
  the *Sense* or *Studio* theme as a base.
- Set up Shopify on its **own subdomain** (`shop.curiousandcreative.com`)
  so the marketing microsite at `/kindling` on the main site can link
  out cleanly.
- Add age-gate on the After Dark product page (the site already confirms 18+ before adding it to the cart).
- Enable **pre-orders** during the manufacturing window so demand is
  visible before inventory lands.

---

## Step 8 — Launch checklist

- [ ] Trademark filed, copyright filed.
- [ ] Final deck files signed off.
- [ ] Manufacturer contract signed, 30% deposit paid.
- [ ] Proof copy in hand, signed off.
- [ ] Production run in motion.
- [ ] 3PL account opened, SKUs created.
- [ ] Shopify store live, products listed, age-gate tested.
- [ ] Marketing microsite (`/kindling`) live with waitlist form.
- [ ] Therapist / educator outreach list seeded with 30 names.
- [ ] First-25-orders handwritten-note plan in place.

---

## Rough budget (first run, all-in)

| Line item | Low | High |
|---|---|---|
| Trademark + copyright | $400 | $2,000 |
| Sensitivity reads | $200 | $500 |
| Design / illustration (if outsourced) | $0 | $5,000 |
| Manufacturing (1k base + 500 each add-on) | $8,000 | $15,000 |
| 3PL setup + initial shipping | $500 | $2,000 |
| Shopify + apps (year 1) | $400 | $1,000 |
| Launch marketing (gifting + ads seed) | $1,000 | $5,000 |
| **Total** | **~$10,500** | **~$30,500** |
