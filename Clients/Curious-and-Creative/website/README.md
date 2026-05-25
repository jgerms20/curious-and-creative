# Curious & Creative — Website

The Next.js site for Curious & Creative, including the **Kindling** card-game
microsite at `/kindling`.

## Stack

- Next.js 15 (App Router) + TypeScript
- Tailwind CSS
- Google Fonts (Fraunces serif + Inter sans)
- Static-rendered

## Develop

```bash
npm install
npm run dev
```

Open <http://localhost:3000>.

## Routes

- `/` — Studio home
- `/about`, `/projects`, `/podcast`, `/journal`, `/contact`
- `/journal/[slug]` — long-form posts (seeded from `content/journal/posts.ts`)
- `/kindling` — microsite home
  - `/kindling/decks`
  - `/kindling/how-it-works`
  - `/kindling/manifesto`
  - `/kindling/order` — waitlist form

## Content

- Journal posts: `content/journal/posts.ts`
- Sample Kindling cards: `content/kindling/sample-cards.ts`
- Scoring logic (shared with the explainer UI): `lib/kindling-scoring.ts`

## Build

```bash
npm run build
npm run start
```
