# `earlobe/`: the engine

Python 3.10+. Third-party dependencies are limited to `anthropic`, `pyyaml` and `jsonschema`. Everything else is standard library, plus `ffmpeg` on PATH for audio.

Run everything from `project-earlobe/`.

```
python -m earlobe list-shows
python -m earlobe run --show columbia-daily --dry-run      # full episode, no API keys needed
python -m earlobe breaking-scan --dry-run
python -m earlobe recheck --days 7 --dry-run
python -m earlobe feeds                                    # rebuild RSS feeds from the store
python -m pytest
```

**Dry-run** swaps the network, Claude, ElevenLabs and host calls for deterministic fixtures in `earlobe/fixtures.py`. A dry run still produces every artifact: script JSON, checker reports, gate decision, show notes, a silent MP3 if ffmpeg is present, an RSS item and a trust-log line. All output lands in `data/` (gitignored).

## Module map: public interfaces

These are the agreed interfaces. Each module owns its file(s), and modules talk to each other only through the contracts in `schemas.py`.

| Module | Public functions / classes | Notes |
|---|---|---|
| `schemas.py` | dataclasses + `JSON_SCHEMAS` + `validate(kind, data)` + `make_id(prefix, *parts)` | Single source of truth |
| `config.py` | `ROOT`, `DATA_DIR`, `load_shows()`, `load_markets()`, `load_voices()`, `load_owners()`, `load_sources(market)`, `model_for(tier)`, `PRICES` | Model IDs only from env `EARLOBE_MODEL_{OPUS,SONNET,HAIKU}`; returns `None` if unset |
| `llm.py` | `LLM(dry_run=False)`; `.structured(agent_id, tier, system, user, kind, effort="medium") -> dict`; `.research(agent_id, tier, system, user, kind, max_searches=10) -> dict`; `.runs: list[AgentRun]` | Anthropic SDK; `structured` uses `output_config.format`; `research` uses the web search server tool and parses JSON from the final text, with a `structured` repair pass on failure; dry-run returns `fixtures.fake(kind, ...)` |
| `store.py` | `Store(path=DATA_DIR/"earlobe.db")`; `.put(kind, id, obj_dict, show_id="")`, `.get(kind, id)`, `.list(kind, show_id=None, since=None)`, `.log_run(AgentRun)` | sqlite3, JSON blobs |
| `sensors/base.py` | `fetch(url, timeout=20) -> str`, `parse_feed(xml, *, sensor, market, beat, outlet, tier) -> list[Signal]` | stdlib urllib + ElementTree; RSS 2.0 + Atom |
| `sensors/rss.py` | `poll_market(market, since_hours=24, dry_run=False) -> list[Signal]` | Uses `config/sources/<market>.yaml` |
| `sensors/gnews.py` | `search(query, market, hours=24) -> list[Signal]` | Google News RSS search |
| `sensors/gdelt.py` | `articles(query, timespan="1h") -> list[Signal]`, `velocity(query, timespan="1h") -> float` | GDELT DOC 2.0 |
| `sensors/courtlistener.py` | `recent_dockets(courts, since_hours=24, token=None) -> list[Signal]` | v4 API, token from env `COURTLISTENER_TOKEN` |
| `sensors/__init__.py` | `run_sensors(market, beats, since_hours=24, dry_run=False) -> list[Signal]` | Dedupes by URL |
| `desk/cluster.py` | `cluster(signals, owners) -> list[Story]` | Title shingles + time window; computes `independent_outlets` |
| `desk/independence.py` | `owner_group(outlet, owners) -> str`, `independent_count(evidence_or_sources, owners) -> int` | Wires collapse syndicated copies |
| `desk/score.py` | `score(story, show_cfg) -> int`, `triage(stories, llm, show_cfg) -> list[Story]` | Heuristic score; Haiku-tier triage optional |
| `desk/breaking.py` | `detect(stories, window_minutes=60) -> list[Story]` | Velocity + independent tier ≤2 outlets + official confirmation + event class |
| `desk/assign.py` | `assign(stories, shows) -> dict[show_id, list[Story]]` | Market/beat match, `max_stories`, risk → lane |
| `producer/research_pack.py` | `build_pack(stories, sources) -> dict` | |
| `producer/writer.py` | `write_script(show_id, show_cfg, stories, pack, llm, *, revision=0, instructions=None, episode_date) -> Script` | Opus tier; every body line carries `claim_ids` |
| `producer/disclosure.py` | `disclosure_lines(show_cfg, voices) -> list[ScriptLine]`, `ensure_disclosure(script, show_cfg, voices) -> Script` | End-of-episode AI disclosure |
| `producer/copywriter.py` | `write_copy(script, show_cfg, llm) -> dict` | `Copy` schema; Sonnet tier |
| `trust/claims.py` | `extract_claims(script, llm) -> Script` | Independent claim pass; adds missed claims |
| `trust/verifier.py` | `verify(script, llm, owners, max_searches=20) -> VerifierReport` | **Blind** re-sourcing: never shown the writer's sources; recomputes `independent_count` in code |
| `trust/factcheck.py` | `fact_check(script, verifier_report, llm) -> FactCheckReport` | |
| `trust/bias.py` | `bias_check(script, llm) -> BiasReport` | |
| `trust/legal.py` | `legal_screen(script, llm) -> LegalReport` | Names, minors, victims, allegations |
| `trust/gate.py` | `decide(script, verifier, factcheck, bias, legal=None, policy=None, holds_used=0) -> GateDecision`, `POLICIES` | Deterministic (done) |
| `trust/loop.py` | `run_trust_loop(script, rewrite_fn, llm, owners) -> tuple[Script, GateDecision, dict]` | Runs the checkers in isolation, then the gate; REWRITE loops back through `rewrite_fn` |
| `studio/tts.py` | `ElevenLabsTTS(api_key, model_id).synthesize(text, voice_id) -> bytes`, `DryRunTTS()` | REST via urllib |
| `studio/mix.py` | `render(script, voices, tts, out_path, music_bed=None) -> tuple[str, int]` | ffmpeg concat + loudnorm (-16 LUFS) |
| `studio/operator.py` | `StudioOperator` interface for computer-use engines (NotebookLM, Meta Muse) | Stub, documented |
| `publish/notes.py` | `show_notes(script, decision, copy) -> str` | Sources plus a verification summary |
| `publish/feed.py` | `build_feed(show_id, show_cfg, episodes, base_url) -> str`, `write_feed(...) -> path` | iTunes + podcast namespace tags; AI disclosure in metadata |
| `publish/hosts.py` | `HostAdapter`, `LocalHost(out_dir)`, `TransistorHost(api_key, show_id)` | Transistor adapter marked "verify vs docs" |
| `publish/trustlog.py` | `append(show_id, episode, decision)` | Public JSONL trust log |
| `monitor/corrections.py` | `open_correction(...)`, `apply_correction(store, correction)` | Reissues notes and feed |
| `monitor/recheck.py` | `recheck(store, llm, days=7) -> list[Correction]` | Re-verifies published claims |
| `monitor/killswitch.py` | `killed(show_id=None) -> bool` | Env `EARLOBE_KILL=all\|show1,show2` or `config/killswitch.yaml` |
| `monitor/budget.py` | `within_budget(store, show_id, day) -> bool` | Daily USD cap per show from `config/budgets.yaml` |
| `pipeline.py` | `run_show(show_id, *, dry_run=False, now=None) -> Episode \| None`, `run_breaking(dry_run=False)`, `run_evergreen(show_id, dry_run=False)` | Wires it all together |
| `cli.py` / `__main__.py` | argparse subcommands above | |
| `fixtures.py` | `fake(kind, **ctx) -> dict`, `sample_signals(market)` | Deterministic dry-run data |
