# Kindling — Game Design (First Edition, v1.0)

Kindling is a card game for kindling and rekindling intimacy. It has
the coffee-table energy of Cards Against Humanity and We're Not Really
Strangers, but it covers intimacy at large: emotional, playful,
sensual, sexual, and kinky.

It's built for couples, and it also works for new lovers, throuples,
polycules, and friends who want to get closer. These rules match the
digital game at `site/kindling/play.html` exactly.

- **Every card:** `Production/Kindling/deck/*.json` (edit there, then run `python3 scripts/build_kindling.py`)
- **Browse the deck:** `site/kindling/deck.html`
- **Spreadsheet:** `Production/Kindling/kindling-cards.csv`

---

## Design pillars

1. **Consent is the game, not the fine print.** Skipping is always free. The table plays at the lowest heat anyone picks. Anyone can say "cool it" or "ember out."
2. **Intimacy at large.** Talking, touching, play, dates, rituals, sex, and kink are all on the same heat scale.
3. **Queer by default.** No card assumes gender, anatomy, or monogamy. Group cards are written for groups, not adapted.
4. **Reward leaning in, never pushing.** Bolder cards score more, but nothing is ever scored *against* you.
5. **Everyone wins, someone wins a little more.** The prize is always something the whole table enjoys.

---

## What's in the box

| Deck | Cards | What it is | Sparks |
|---|---|---|---|
| **Embers** (core) | 150 + 4 rules | Ask, Tell, Notice, Touch, Tend, Play, Dare + 10 wild cards | heat × 1 |
| **Wildfire** | 60 | 44 challenges, 10 role reversals, 6 group challenges | heat × 2 |
| **Slow Burn** | 60 | 22 rituals, 24 dates, 14 slow sensual cards | heat × 2 |
| **After Dark** (18+) | 60 | 10 negotiation, 14 power, 14 sensation, 12 roleplay, 10 group; aftercare on every card | heat × 2 |

**Heat scale:** 1 Spark (sweet, friend-safe) · 2 Glow · 3 Flame · 4 Blaze · 5 Inferno.

Every Embers card is tagged **friend-safe** (heat 1–2, nothing sexual) or **partners**. Embers has 62 friend-safe cards, so Friends mode is a real game, not a sampler.

There are **21 Match cards** across the decks, and **27 group (3+) cards** spread through every deck.

### Card anatomy
Type (top left) · heat flames (top right) · prompt (center, serif) · time (bottom left) · deck mark (bottom center) · Sparks value (bottom right). Match cards carry a "Match" tab, and 3+ cards a "3+ players" tab. After Dark cards are dark, with an Aftercare line above the footer.

---

## How to play

### Setup
1. **Set the heat.** Each player privately picks a max heat, 1–5. The table plays at the **lowest** pick, and nobody has to say whose it was.
2. **Pick decks.** Embers plus any expansions. The game skips 3+ cards when only two people are playing.
3. **Pick a length.** Quick (first to 25 Sparks), Long night (50), or Endless.
4. **Wish lists (optional).** Each player writes up to three things they'd love to receive.
5. **The Pot (optional).** Everyone puts in the same amount (see below).

### A turn
Draw a card and read it aloud. Then choose one:

- **Do it.** Score the Sparks printed on the card.
- **Claim it.** The card goes face up in your **Woodpile**. It scores when you complete it, tonight or before next game night. Wildfire and Slow Burn cards are built for this.
- **Skip it.** Free. No reason, no penalty.

### Match cards
Everyone votes in secret (thumbs under the table, or pass the phone). If it's **unanimous**, everyone does it and everyone scores **double**. One no and the card disappears, and nobody learns who said no.

### Wild cards (10, in Embers)
| Card | Effect |
|---|---|
| Pass It On | Keep it. Later, hand any card you draw to someone else to play. |
| Double Down | The next card anyone completes scores double. |
| Cool It | Heat cap drops by one for three rounds. |
| Turn It Up | Heat cap rises by one for three rounds, only if everyone agrees out loud. |
| Steal the Woodpile | Take a claimed card from someone else's Woodpile, Sparks and all. |
| Reverse | On your next turn, the person to your right reads your card and does it to you. |
| Free Pass | Keep it. Skip any card later and still score 1 Spark. |
| Callback | Redo any card played tonight for full Sparks. |
| Your Rules | Invent a card. Whoever receives it picks its heat, and the heat is the score. |
| Truce | Everyone +3 Sparks, and everyone gets water. |

### Safety words
- **"Cool it."** Anyone, any time. The heat cap drops by one for the rest of the game.
- **"Ember out."** Anyone, any time. The game ends immediately. Water, snacks, hug.

---

## Scoring

`Sparks = heat × (1 for Embers, 2 for expansions)`. The value is printed on the card, so nobody does math at the table.

Why expansions pay double: they ask more of you (time, planning, nerve), and doubling them makes claiming a Wildfire card a real strategic move rather than a detour.

The design avoids two things on purpose:
- **No penalty for skipping.** If skipping cost points, the game would pressure people into cards they don't want.
- **No stealing points from a partner.** The only "steal" is taking on someone else's promise, which still has to be kept.

### Winning
First to the goal **catches fire**. The winner picks one item from **someone else's** wish list, and that person makes it happen. If nobody wrote wish lists, the winner asks for something small and lovely from last place.

---

## The Pot and Seasons (the money mechanic)

This is the "each of us puts in $100" idea, built into the game.

1. **Pay in.** At the start of a **Season** (we suggest one month), everyone puts the same amount into a jar, an envelope, or a shared account. Then you write a **shared wish list** of experiences together: a hotel night, a pole class, a dinner you've been eyeing.
2. **Play for a month.** Keep a running Sparks total across game nights. Woodpile cards completed between games count.
3. **Catch fire.** At the end, the Sparks leader picks one experience from the list and **the whole pot pays for it**.
4. **Last place plans it.** Bookings, reservations, the outfit reveal. Everyone goes.

Why it works: the money is real, so the stakes feel real. But it's spent on a shared experience, so nobody loses money to their partner. The loser's "punishment" is planning a date, which is a gift in itself. Two players at $100 each make a $200 pot, enough for a hotel night.

---

## Modes in the digital game
- **Partners:** every card up to table heat.
- **Friends:** friend-safe cards only (heat 1–2, non-sexual). After Dark is disabled.
- Saved per browser, so a game survives a refresh. Nothing is sent anywhere.

---

## Editorial standards (apply to every new card)
- Under ~8 seconds to read aloud (6–28 words).
- Gender-, anatomy-, and structure-neutral. "Them," "your partner," "someone," "everyone."
- Never coerces, never involves anyone who isn't playing, never "you must."
- Hard nos: breath play, blood, permanent marks, intoxication as consent, filming or photos that leave the couple's control, anything with outsiders watching.
- Spicy, not pornographic: describe the invitation, not anatomy.
- After Dark: every card has a specific, warm aftercare line, and power and roleplay cards name limits or the safeword.

## Future packs
*Queer & Found* · *Long Distance* (video and async friendly) · *Brand New* (first 90 days) · *Long Haul* (10+ years) · *Platonic* (a full friends deck).
