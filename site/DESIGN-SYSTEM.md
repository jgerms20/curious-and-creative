# Curious & Creative — Design System

Playful. Bubbly. Sticker-bright. The hub of Joshua German & Janel Moore.
Vibe: Cosmo & Wanda / Fairly OddParents energy — magical and fun, but not silly.
Inspired by the C&C logo (green "Curious", pink "Creative", gold accents, sparkles).

## Palette
| Token         | Hex       | Use                                  |
|---------------|-----------|--------------------------------------|
| `--cream`     | `#FFFCF5` | Page background                      |
| `--mint`      | `#E9F8E6` | Green-tint section                   |
| `--blush`     | `#FFEAF4` | Pink-tint section                    |
| `--sky`       | `#E7F6FB` | Blue-tint section                    |
| `--green`     | `#57B84A` | Primary (Curious) — buttons, footer  |
| `--green-deep`| `#2F9039` | Green text / brand                   |
| `--pink`      | `#EC3F8E` | Primary accent (Creative) — CTAs     |
| `--pink-deep` | `#D11F77` | Pink text / links                    |
| `--gold`      | `#FFC93C` | Ampersand, sparkles, highlights      |
| `--grape`     | `#8E6FE0` | Sparkle accent                       |
| `--sky-blue`  | `#46C7E8` | Sparkle accent                       |
| `--ink`       | `#3A2B3F` | Body text (warm near-black)          |
| `--outline`   | `#2A2030` | Sticker outlines (2.5–3px)           |

## Type
- Display: **Fredoka** (rounded, chunky, friendly) — headings, nav, buttons, chips
- Body: **Nunito** (rounded sans, very readable) — paragraphs, weight 500–800
- Loaded via Google Fonts.

## Signature look
- **Sticker style**: thick `--outline` borders + hard offset shadow (`--sticker: 4px 4px 0`).
- **Big round radii**: cards 28px, buttons pill.
- **Sparkles**: 4-point star SVGs floating in the hero (gold/pink/green/grape/sky).
- **Tilted gold marquee** of disciplines.
- **Bouncy motion**: spring/bounce easing; reveals scale + rise; buttons press in on click; ampersand wobbles.
- **Colored wordmark**: green "Curious" + gold "&" + pink "Creative".
- **Green footer** with gold headings.

## Pages (7)
1. `index.html` — Home: kinetic hero, marquee, 4-up Umbrella (Studio/Shows/Inventions/Art), shows preview, CTA
2. `pages/about.html` — story + mission + the duo (Joshua & Janel, photo slots) + SC origin + what we do
3. `pages/studio.html` — services arm (Strategy & Story · Brand Building · Production · Creative Consulting) + engagement shapes + founder cred
4. `pages/shows.html` — compact Spotify embeds (Aspiring Abolitionist, Eclectic Polymath, Dominate the Decade) + Approachable AI illustrated card + C&C podcast logo slot at bottom
5. `pages/inventions.html` — uniform card grid (Kindling + 3 coming-soon), no lead card
6. `pages/art.html` — gallery framework (6 placeholder tiles) + first-dibs email capture
7. `pages/contact.html` — playful form + reach-us rail

## Theme
Light is default. Dark mode toggled via nav button (saved as `localStorage['cc-theme']`) and respects `prefers-color-scheme` on first visit. Inline `<head>` script sets `data-theme` before paint to avoid FOUC.
Dark palette: warm purple backgrounds (#161020 → #241B2E), cream text + outline (#FFEEDC), brand greens/pinks lightened for AA contrast.

## Reusable classes (see css/components.css)
nav · hero · sparkle · marquee · section-head(.center) · card · card-cover · chip(.chip-status .live/.dev/.soon) · founder(.founder-portrait/.initials/.photo-hint) · logo-slot · manifesto · cta-block(.pink/.mint/.gold) · footer · form · page-head · reveal(.delay-1..4) · umbrella · split · principles

## Founder photos
Drop `assets/joshua.jpg` and `assets/janel.jpg` (square). Until then, the `<img onerror="this.remove()">` falls back to playful initials (JG / JM).

## Show links (verified with founders)
- Aspiring Abolitionist — Spotify `7natfWFnBgakjLLZcEDZaw`
- Eclectic Polymath — Spotify `3dlagzJ0jiWLTB9mF3y069`
- Approachable AI — YouTube `@Approachable.A.I`
- Dominate the Decade (Janel guest) — Spotify `3IiC15tFfb1rHoDm9R6Zxp` (TODO: exact episode link)
