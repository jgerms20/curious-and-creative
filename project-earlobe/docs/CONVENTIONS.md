# Project Earlobe — writing & build conventions

Every doc, agent file and module in this folder follows these rules.

1. **Numbers cite the facts sheet.** Any price, CPM, download count or market figure comes from
   [`docs/research/facts-and-figures.md`](research/facts-and-figures.md) and cites its ID (e.g. `F-TTS-03`).
   If a number isn't there, add it there first (with source + as-of date), then cite it.
2. **As of October 2026.** Vendor prices and policies change. Every cost or policy statement carries
   "as of Oct 2026 — verify before buying" once per section.
3. **Label inferences.** Anything we reasoned out rather than read from a source is marked *(inference)*.
   This matters most in the Jeanine Wright / Liquid Studios research.
4. **No model version strings.** Refer to Claude model tiers only as **Opus tier**, **Sonnet tier**,
   **Haiku tier**. Concrete model IDs live only in environment variables
   (`EARLOBE_MODEL_OPUS`, `EARLOBE_MODEL_SONNET`, `EARLOBE_MODEL_HAIKU`), never in the repo.
5. **No secrets.** API keys go in GitHub Actions secrets / local `.env` (gitignored). `.env.example` lists names only.
6. **Original voices, disclosed.** Host personas are original synthetic voices. Every episode ends with the
   AI disclosure outro and carries the disclosure in its metadata.
7. **Copyright.** We report facts in our own words and link sources. Never read or paste articles.
8. **Contracts are code.** The JSON shapes agents exchange are defined in [`earlobe/schemas.py`](../earlobe/schemas.py)
   and documented in [`docs/blueprint/json-contracts.md`](blueprint/json-contracts.md). Change both together.
9. **Status tags** for agents and features: `built` (code exists in v1), `next` (next build wave),
   `future` (designed, not scheduled).
10. **Plain language.** Write for Joshua and Janel first: short sentences, tables over walls of text,
    "what it does / why it matters / what it costs" up front.
