# Curious & Creative — Design System

Bespoke. Editorial-cinematic. Built for the hub of Joshua German & Janel Moore.

## Tone of voice
Confident, warm, culturally fluent. Magazine-grade type, dark canvas, ember accent.
Reference caliber: Proximity Media · Monkeypaw · HOORAE · Sixthirtysix.

## Palette
| Token            | Hex       | Use                                   |
|------------------|-----------|---------------------------------------|
| `--ink`          | `#0A0908` | Page background                       |
| `--ink-2`        | `#13110F` | Surface                               |
| `--ink-3`        | `#1A1612` | Elevated surface                      |
| `--eggshell`     | `#F2E8D5` | Primary text                          |
| `--mist`         | `#8B8378` | Muted text                            |
| `--ember`        | `#E94F37` | Primary accent (CTAs, signature mark) |
| `--ember-soft`   | `#FFB099` | Hover / glow tint                     |
| `--cobalt`       | `#3D5AFE` | Secondary punctuation accent          |
| `--hairline`     | `rgba(242, 232, 213, 0.08)` | Borders         |

## Type
- Display: **Fraunces** (variable, opsz + soft axes) — editorial, characterful
- Body: **Inter Tight** — modern, slightly condensed
- Mono: **JetBrains Mono** — metadata, eyebrows

Loaded via Google Fonts.

### Ramp
| Role     | Size                            | Family / Weight       |
|----------|---------------------------------|-----------------------|
| Hero     | `clamp(4rem, 11vw, 10rem)`      | Fraunces 600, lh 0.92 |
| H1       | `clamp(2.5rem, 5vw, 4.5rem)`    | Fraunces 600, lh 1.05 |
| H2       | `clamp(1.75rem, 3vw, 2.75rem)`  | Fraunces 600, lh 1.1  |
| H3       | `1.375rem`                      | Inter Tight 600       |
| Body     | `1.0625rem`                     | Inter Tight 400, lh 1.6 |
| Small    | `0.875rem`                      | Inter Tight 400       |
| Eyebrow  | `0.75rem`                       | JetBrains Mono 500, ucase, tracking 0.18em |

## Space scale (rem)
`0.25 · 0.5 · 0.75 · 1 · 1.5 · 2 · 3 · 4 · 6 · 8 · 12 · 16`

## Radii
`xs 4px · sm 8px · md 12px · lg 20px · pill 999px`

## Shadows
- `--shadow-soft`: `0 20px 60px -20px rgba(0, 0, 0, 0.6)`
- `--shadow-ember`: `0 0 0 1px rgba(233, 79, 55, 0.35), 0 20px 60px -10px rgba(233, 79, 55, 0.25)`

## Motion
- Fast `180ms`, Base `320ms`, Slow `600ms`, Story `900ms`
- Standard ease: `cubic-bezier(0.2, 0.7, 0.2, 1)`
- Spring: `cubic-bezier(0.34, 1.56, 0.64, 1)`

### Reveal vocabulary
- **Fade-rise**: opacity 0 → 1, translateY 24px → 0, 600ms
- **Letter cascade**: hero words stagger in (40ms between words)
- **Marquee**: disciplines strip, 40s linear infinite
- **Hover-tilt**: cards lift 4px + subtle 1.5deg rotation
- **Ampersand pulse**: signature `&` mark rotates / pulses on view
- `prefers-reduced-motion` disables all of the above except instant opacity transitions

## Components
- **Nav** — fixed top, blur-glass backdrop, ampersand mark on left, 6 links on right, mobile hamburger
- **Hero** — full-bleed, kinetic display type, eyebrow eyebrow, scroll cue
- **Section header** — eyebrow + display H2 + lede
- **Card (show)** — cover slot, eyebrow (Podcast / YouTube), title, host line, platform chips, link arrow
- **Card (venture)** — title, status chip (Live / In Dev / Coming Soon), one-liner, link arrow
- **Card (founder)** — portrait slot, name in display, role line, bio paragraph, link rail (LinkedIn / Site / Socials)
- **Marquee** — full-bleed scrolling disciplines (Direction · Production · Strategy · Story · Sound · Brand · Policy · AI)
- **Footer** — wordmark + ampersand mark + 3 columns + copyright line
- **Chips** — pill, mono caps, status variants (live / dev / soon)
- **Buttons** — primary (ember), ghost (hairline border), arrow link (text + animated arrow)
- **Form** — labeled inputs, ember focus ring, hairline border

## Page layouts (brief)
- **Home**: kinetic hero → marquee → Under the Umbrella (3-up: Shows / Ventures / Founders) → manifesto pull-quote → CTA → footer
- **About**: hero ("Two curious minds. One canvas.") → mission → USC origin → what C&C does → manifesto principles
- **Founders**: side-by-side bio for Joshua + Janel with portrait slots, real employers, real links
- **Shows**: grid — Aspiring Abolitionist · Eclectic Polymath · Approachable AI · Dominate the Decade (Janel featured) · C&C Podcast (Coming Soon w/ logo slot)
- **Ventures**: Kindling (lead, ember accent) + 2 Coming Soon cards
- **Contact**: split — left form, right "Other ways to reach us" (emails, socials, location)

## Signature mark
The ampersand `&` set in Fraunces 600 italic is the brand mark. Used as nav-left logo, footer mark, favicon, and section dividers. Pulses on view (scale 1 → 1.06 → 1, 1.8s ease-in-out).
