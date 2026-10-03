# Kindling — Logo Prompt for Claude Design

Paste the prompt below into Claude Design. Iterate on the **wordmark
direction** and the **icon direction** separately, then choose your
favorite combination.

> **Where things stand:** the site, cards, and box currently use a
> placeholder mark: two leaning flames (orange and gold) with a darker core
> where they meet, beside a lowercase Fraunces italic "kindling". It's drawn
> in `site/kindling/kindling.js` (`K.mark`). The brief below asks Claude Design
> to push past it. To swap in the final logo, replace the SVG paths in
> `K.mark` (one place), then rerun `node scripts/kindling_print.mjs`.

---

## The prompt

> Design a logo for **Kindling**, a modular intimacy card game for
> couples, throuples, and pairings of any kind. Kindling helps people
> deepen connection through prompts that range from conversation to
> shared experience to consensual physical intimacy. The brand is
> queer-friendly by default, consent-forward, warm, and grown-up — not
> coy, not clinical, not winking.
>
> **Brand mood:** the inside of a candlelit apartment in late autumn —
> warm, glowing, a little secret, a little ceremonial. Think *less*
> Hallmark, *more* The Atlantic + Aesop + Le Labo. It should look at
> home next to design objects, not gag gifts.
>
> **Inspiration to reference (do not copy):**
> - *We're Not Really Strangers* (typography confidence, minimal palette)
> - *Aesop* (restrained type, generous whitespace)
> - *Le Labo* (small caps, ledger-like serif energy)
> - *The Atlantic* magazine masthead (editorial gravitas)
>
> **Output requested:**
> 1. **Three wordmark directions** for "Kindling":
>    - A modern serif (Fraunces / GT Sectra / Tiempos energy) with high
>      contrast and a confident lowercase "g."
>    - A small-caps editorial wordmark with wide letterspacing.
>    - A custom hand-drawn wordmark that feels like a signature scrawled
>      on a matchbook.
> 2. **Three icon / mark directions** that pair with the wordmark:
>    - A single, abstracted flame, drawn in one continuous stroke.
>    - Two abstract shapes leaning toward each other to imply two people
>      / two sparks meeting (negative-space ember between them).
>    - A small ligature using the "K" and a flame as one form.
> 3. For each combination, show:
>    - The logo on **cream `#FBF0E2`** (the card face).
>    - The logo on **night `#170B0A`** (the box color) and on **flame `#FF6A2B`** (the Embers card back).
>    - The logo at small size (e.g. 24px tall) to confirm legibility.
>
> **Palette to stay inside (one warm-ember system):**
> - Night `#170B0A` (box and dark backgrounds)
> - Cream `#FBF0E2` (card faces)
> - Flame `#FF6A2B` (primary accent, Embers deck)
> - Gold `#FFC24B` (secondary accent)
> - Ember `#C2321F` (deep red)
> - Expansion colors: Wildfire `#E2363B`, Slow Burn `#E2728A`, After Dark `#B88CFF` on `#1A0F22`
>
> **Avoid:**
> - Hearts, lips, anatomy, flame emojis, anything literal.
> - Cursive script that reads as wedding-invitation.
> - "Sexy" coded styling — neon, latex, smoky type effects.
> - Anything that signals "couples only" or excludes queer pairings.
>
> The final logo will be debossed on a black-core card box and printed
> in single-color on the card backs. Prioritize a mark that holds up at
> small sizes and looks elegant in one ink.

---

## After you get options back

1. Pick your favorite **wordmark** and your favorite **mark** — they
   don't have to be from the same direction.
2. Ask Claude Design for a **lockup** combining them (mark left,
   wordmark right, with a baseline-aligned spec).
3. Ask for **monogram** variants ("K" + flame) for app icons and
   social avatars.
4. Export: SVG, PNG @1x/2x/3x, and a 300dpi CMYK PDF for print.
