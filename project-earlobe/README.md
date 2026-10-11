# Project Earlobe: the Curious & Creative Network

An automated audio network. Always-on agents find stories. Producers write the episodes. A **Trust Stack** checks every claim against independent sources. Original AI voices record each episode, and shows publish around the clock with no human gate. Each episode ends with an honest AI disclosure.

**Start here:** [`docs/00-START-HERE.md`](docs/00-START-HERE.md). It covers what's built, what's next, and what Joshua and Janel do first.

## Map

| Area | Where | What's inside |
|---|---|---|
| Blueprint ("the sauce") | [`docs/blueprint/`](docs/blueprint/) | Org chart, how the workflows actually run, trust gate, JSON contracts, full agent catalog |
| Agents | [`agents/`](agents/) | One instruction file per agent, grouped by desk |
| Standards | [`docs/standards/`](docs/standards/) | Sourcing, fact-check, bias, crime and courts, corrections, AI disclosure scripts, voices |
| Business | [`docs/business/`](docs/business/) | Business plan, products, advertising, go-to-market, legal, risks, founder to-do, timeline, Jeanine Wright meeting prep |
| Money | [`finance/`](finance/) | Cost-out workbook (`cost-model.xlsx`) plus the ROI report |
| Research | [`docs/research/`](docs/research/) | Facts and figures sheet, Jeanine Wright / Liquid Studios deep dive, market research, notes |
| Shows | [`docs/shows/`](docs/shows/) | Network lineup at scale, plus show bibles |
| Engine | [`earlobe/`](earlobe/) | Python pipeline: sensors → story desk → producer → trust stack → gate → studio → publish |
| Config | [`config/`](config/) | Shows, markets, voices, source feeds, outlet ownership |

## Run it (no keys needed)

```bash
cd project-earlobe
pip install -e .[dev]
python -m pytest
python -m earlobe run --show columbia-daily --dry-run
```

To run it live:

1. Copy `.env.example` to `.env`.
2. Fill in the keys: Anthropic, ElevenLabs, voice IDs, and the model tier variables.
3. Drop `--dry-run`.

For GitHub Actions, add the same names as repository secrets and variables. The scheduled workflows skip themselves cleanly until they're set.
