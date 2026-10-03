# Kindling — Shop setup

The shop at `/kindling/shop.html` is fully built: products, a cart that
persists in the browser, quantities, free-shipping progress, an 18+
confirmation for After Dark and the bundle, and a nudge when an expansion
is in the cart without the core deck.

**Checkout is a setting, not code.** Everything lives in
`site/data/kindling-shop.json`. Change it, push to `main`, and the site
redeploys.

---

## Mode 1 — Pre-order reservations (live now)

```json
"checkout": { "mode": "preorder", "preorder": { "formEndpoint": "", "email": "jgerms20@gmail.com" } }
```

Customers fill in their name, email, ZIP, and an optional note. Nothing is
charged.

- **With no `formEndpoint`** (the current setting), submitting opens the customer's email app with the order pre-filled, addressed to `email`. It works today, but some people won't hit send.
- **Recommended (10 minutes): add a Formspree endpoint.**
  1. Create a free form at formspree.io and verify `jgerms20@gmail.com`.
  2. Copy the endpoint, e.g. `https://formspree.io/f/abcdwxyz`.
  3. Paste it into `formEndpoint`. Reservations then post straight to your inbox and Formspree dashboard: name, email, ZIP, note, items, and total.
  4. Optional: connect Formspree to Google Sheets for a live pre-order list.

## Mode 2 — Shopify (when inventory is real)

```json
"checkout": {
  "mode": "shopify",
  "shopify": {
    "storeDomain": "kindling-game.myshopify.com",
    "variants": { "embers": "44001", "wildfire": "44002", "slowburn": "44003", "afterdark": "44004", "bundle": "44005" }
  }
}
```

1. Create the five products in Shopify with the same prices as `products` in the JSON.
2. For each product, copy its **variant ID**. In the admin, open the product, click the variant, and take the number at the end of the URL.
3. Paste them in. The cart sends customers to `https://<store>/cart/<variant>:<qty>,…`. That's Shopify's cart permalink, so the whole multi-item cart carries over and no API token is needed.
4. Shopify handles payment, tax, shipping rates, and receipts. If any variant ID is blank, the shop falls back to pre-order mode, so nothing breaks.

**Adult products on Shopify:** After Dark is card text only (no explicit
imagery), which is generally fine. Read Shopify's Acceptable Use Policy
anyway, and keep the product photos tasteful.

## Mode 3 — Stripe Payment Links (simplest paid option)

```json
"checkout": { "mode": "stripe", "stripe": { "paymentLinks": { "embers": "https://buy.stripe.com/…", "bundle": "https://buy.stripe.com/…" } } }
```

Create one Payment Link per product in Stripe and allow adjustable
quantity. Payment Links check out **one product at a time**, so a mixed
cart shows one button per product and suggests the bundle. This mode is
best if you mostly sell the bundle.

---

## Pricing (in `products`)

| Product | Price | Notes |
|---|---|---|
| Embers (core) | $39 | Required to play expansions |
| Wildfire | $24 | |
| Slow Burn | $24 | |
| After Dark | $28 | 18+, age confirmation before adding to cart |
| The Whole Fire (bundle) | $99 | Compare-at $115; 18+ because it includes After Dark |

Free shipping over $75 (`freeShippingOver`), otherwise $6 flat
(`flatShipping`). The banner under the page title is `status`.

## Before you take real money

- [ ] Trademark clearance (see `manufacturing-plan.md`).
- [ ] Sales tax: Shopify and Stripe Tax can both calculate it. Turn it on.
- [ ] Shipping: discreet, unbranded outer mailer (promised on the shop page).
- [ ] A refund policy and contact email on the shop's checkout.
- [ ] Decide what stays free. The digital game at `/kindling/play.html` currently deals **the full deck**, and the card text is public in `site/data/kindling-cards.json`. That's great for word of mouth. If you'd rather the free version be a sampler, trim what gets published to the site at launch.
