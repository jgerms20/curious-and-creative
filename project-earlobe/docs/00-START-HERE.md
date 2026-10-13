# Start here: Project Earlobe (Curious & Creative Network)

**For Joshua & Janel.** This page covers what got built, what's real versus stubbed, and what to do first.

## What this is

An automated audio network:

- **Always-on agents** find stories in every market.
- **Producers** write the episodes.
- **A Trust Stack** checks every claim against independent sources and decides whether to publish, rewrite, hold or kill.
- **Original AI voices** record each episode, and every episode ends with an AI disclosure.
- Nothing needs a human to publish. You set the rules, the budget and the kill switch.

## Read in this order (about 60 minutes)

1. [Business plan](business/business-plan.md): the whole thing on one page.
2. [Cost-out & ROI](../finance/cost-out-and-roi.md), plus the workbook [`cost-model.xlsx`](../finance/cost-model.xlsx): what it costs and when it pays.
3. [How it works](blueprint/how-it-works.md) and the [org chart](blueprint/org-chart.md): the 122-agent system.
4. [Jeanine Wright deep dive](research/jeanine-wright-deep-dive.md) and [meeting prep](business/meeting-jeanine-wright.md). The outreach email is waiting in your Gmail drafts.
5. [Founder to-do](business/founder-todo.md) and the [timeline](business/timeline.md).

## What got built

| Area | Status | Where |
|---|---|---|
| **Engine** (Python) | **Working in dry run.** A full Columbia Daily episode goes from sensors to script, 11 checked claims, a PUBLISH decision, a voiced MP3, show notes, an RSS feed and a trust-log line. 1,012 tests pass. CI runs on every PR | [`earlobe/`](../earlobe/README.md) |
| **Live mode** | Coded but **not yet run against real services.** It needs your API keys (Anthropic, ElevenLabs, CourtListener). Expect a tuning week in the dark run | `.env.example` |
| **Scheduled shows** | GitHub Actions workflows exist. They **skip cleanly** until secrets are set, and only run from `main` | `.github/workflows/earlobe-*.yml` |
| **Blueprint** | Agent catalog (122 agents, 10 desks), org chart, how-it-works loops, trust gate, JSON contracts | [`docs/blueprint/`](blueprint/) |
| **Agent instructions** | 122 files. The 10 core agents are hand-enriched; the rest were generated from the catalog and get deepened as each is built | [`agents/`](../agents/README.md) |
| **Standards** | Editorial, verification, fact-check, bias, crime & courts, corrections, AI disclosure scripts, voice personas | [`docs/standards/`](standards/README.md) |
| **Business** | Plan, products, advertising, go-to-market, competitive, legal, risks, to-do, timeline | [`docs/business/`](business/) |
| **Shows** | Lineup of 40+ shows across all layers, plus 7 launch show bibles | [`docs/shows/`](shows/network-lineup.md) |
| **Research** | Facts sheet (every number has an ID and a source), 10 research notes, market research, Freakonomics ep. 690 notes | [`docs/research/`](research/facts-and-figures.md) |
| **Money** | Cost-out workbook (542 formulas, recalculated clean) with 3 revenue cases and a network-only view | [`finance/`](../finance/) |

## Five things to know before you spend

1. **Startup cash:** about $7.3k one-time, then about $1.4k a month for the test markets. Plan **$25k of runway** to survive the conservative case.
2. **Ads alone don't pay for a local brief yet.** Sponsors, Studio Services and B2B carry the early months. The same thin spot pushed Inception Point toward selling infrastructure.
3. **Insurance is the real gate** for the courts and crime shows. Some insurers may decline automated crime coverage, so get quotes first.
4. **Don't flood feeds.** Platforms filtered Quiet Please as AI spam. Launch the 7 test shows over about 10 weeks, not in one day.
5. **Numbers marked *(inference)* are guesses** until real downloads arrive. Replace them monthly.

## Your first 10 actions

| # | Do | Cost |
|---|---|---|
| 1 | Anthropic API account + spend cap | about $300/mo at test |
| 2 | Set `EARLOBE_MODEL_OPUS`, `EARLOBE_MODEL_SONNET`, `EARLOBE_MODEL_HAIKU` (values from Claude in chat) | $0 |
| 3 | ElevenLabs plan, 6 original voices, Startup Grant application | $22–$299/mo |
| 4 | GitHub secrets for the workflows | $0 |
| 5 | E&O insurance quotes | about $500/mo placeholder |
| 6 | Book a media-lawyer review | about $2.5k–$7.5k |
| 7 | Business bank card | $0 |
| 8 | Send the Jeanine Wright email (it's in your Gmail drafts) | $0 |
| 9 | Domain + DBA + trademark clearance | about $1.2k |
| 10 | Start the 2–3 week dark run, and listen to 10 episodes | API + voice only |

## Run it yourself

```bash
cd project-earlobe
pip install -e .[dev]
python -m pytest                                   # 1,012 tests
python -m earlobe list-shows
python -m earlobe run --show columbia-daily --dry-run
```

## Known gaps (honest list)

- Live API paths are untested against real services: the Claude web-search verifier, ElevenLabs voices and the host upload.
- The Transistor host adapter is marked "verify against current docs".
- LA Superior Court has no confirmed bulk data access. Court Watch starts with press releases, news and CourtListener (federal).
- The Studio Operator (computer use for NotebookLM/Meta Muse) is a documented stub. Research found NotebookLM isn't a production engine, and Meta Muse is an assistant rather than a voice engine.
- 112 of the 122 agent files are generated from the catalog and get deepened as each agent is built.
- `docs/research/notes/engineering-apis.md` was never written; the usage limit hit mid-research.
- Everything lives on branch `claude/podcast-studio-ai-factcheck-1tfzno` (PR #14) in the **public** `curious-and-creative` repo. Move it to a private repo whenever you like: create an empty repo, give the Claude GitHub app access, and ask.
