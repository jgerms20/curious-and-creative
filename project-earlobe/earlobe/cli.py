"""Command line: `python -m earlobe <command>` (or the `earlobe` script after `pip install -e .`).

  list-shows                  every configured show: lane, format, market, schedule, enabled
  run --show ID               one episode of a show (evergreen shows are handed to their topic queue)
  breaking-scan               scan the national market and cut a flash for each new breaking story
  evergreen --show ID         the next queued episode of an archive or cold-case series
  recheck [--days N]          re-verify recent episodes and open corrections (--apply publishes them)
  feeds [--show ID]           rebuild the RSS feeds from the store
  cost-report [--days N]      estimated agent spend by show and agent

--dry-run (run, breaking-scan, evergreen, recheck) uses fixtures instead of the network, Claude,
ElevenLabs and the host, needs no keys, and still produces every artifact. --data-dir PATH (or the
environment variable EARLOBE_DATA_DIR) moves the store and everything under data/ elsewhere, which
keeps a dry run apart from real data.

Progress goes to stderr, results to stdout. Exit status: 0 done (including "the gate published
nothing"), 1 a run failed, 2 bad usage or missing configuration.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

from earlobe import config, pipeline
from earlobe.llm import LLM
from earlobe.monitor import corrections, recheck
from earlobe.pipeline import PipelineError
from earlobe.publish import public_dir, trustlog
from earlobe.schemas import Episode
from earlobe.store import Store


# ================================================================== logging
class _StderrHandler(logging.Handler):
    """Writes to whatever sys.stderr is at the moment of the record (so redirects and test capture work)."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            print(self.format(record), file=sys.stderr, flush=True)
        except Exception:  # noqa: BLE001
            self.handleError(record)


class _Format(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        text = record.getMessage()
        if record.levelno >= logging.WARNING:
            return f"{record.levelname.lower()}: {text}"
        return text if record.levelno >= logging.INFO else f"{record.name}: {text}"


def _install_logging(verbose: bool) -> tuple[logging.Logger, logging.Handler, int]:
    logger = logging.getLogger("earlobe")
    handler, previous = _StderrHandler(), logger.level
    handler.setFormatter(_Format())
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger, handler, previous


# ================================================================== output helpers
def _clock(seconds: int) -> str:
    return f"{int(seconds) // 60}:{int(seconds) % 60:02d}"


def _pct(value) -> str:
    return f"{round(float(value) * 100)}%" if isinstance(value, (int, float)) else "n/a"


def _table(rows: list[list[str]], right: tuple[int, ...] = ()) -> list[str]:
    """Plain aligned columns; the first row is the header."""
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    out = []
    for row in rows:
        cells = [str(c).rjust(widths[i]) if i in right else str(c).ljust(widths[i]) for i, c in enumerate(row)]
        out.append("  ".join(cells).rstrip())
    return out


def _print_episode(ep: Episode) -> None:
    gate, scores = ep.gate or {}, (ep.gate or {}).get("scores", {})
    with Store() as store:
        spent = store.spend(ep.show_id, (ep.published_at or "")[:10] or None)
    print(f"published  {ep.show_id}  {ep.id}")
    print(f"  title      {ep.title}")
    print(f"  gate       {gate.get('decision')}, lane {gate.get('lane_policy')}, "
          f"{gate.get('revision', 0)} rewrite(s), corroboration {_pct(scores.get('corroboration_rate'))}, "
          f"accuracy {_pct(scores.get('accuracy_rate'))}, balance {scores.get('balance_score', 'n/a')}")
    print(f"  length     {_clock(ep.duration_sec)}, {ep.source_count} sources")
    print(f"  audio      {ep.audio_path}")
    print(f"  audio url  {ep.audio_url}")
    print(f"  notes      {public_dir('notes') / (ep.id + '.md')}")
    print(f"  feed       {public_dir('feeds') / (ep.show_id + '.xml')}")
    print(f"  trust log  {trustlog.path_for(ep.show_id)}")
    print(f"  spend      ${spent:.4f} estimated today for this show")


def _print_nothing(show_id: str) -> None:
    print(f"no episode published for {show_id}: it was skipped, put on hold or stopped by the gate.")
    print(f"  see the log above; the decision is in {trustlog.path_for(show_id)} and the store")


# ================================================================== commands
def cmd_list_shows(args) -> int:
    shows = config.load_shows()
    if args.json:
        print(json.dumps(list(shows.values()), indent=2, ensure_ascii=False))
        return 0

    def schedule(cfg: dict) -> str:
        cad = cfg.get("cadence") or {}
        if cad.get("type") == "cron":
            local = f" ({cad['local_time']} {cad.get('tz', '')})".replace(" )", ")") if cad.get("local_time") else ""
            return f"{cad.get('cron')} UTC{local}"
        gap = f", {cad['min_gap_minutes']} min apart" if cad.get("min_gap_minutes") else ""
        return f"on {cad.get('trigger', 'event')}{gap}"

    rows = [["ID", "ON", "WAVE", "LANE", "FORMAT", "MARKET", "SCHEDULE"]]
    for sid, cfg in shows.items():
        rows.append([sid, "yes" if cfg.get("enabled", True) else "no", cfg.get("wave", ""), cfg.get("lane", ""),
                     cfg.get("format", ""), cfg.get("market", ""), schedule(cfg)])
    print("\n".join(_table(rows)))
    return 0


def cmd_run(args) -> int:
    episode = pipeline.run_show(args.show, dry_run=args.dry_run)
    if episode is None:
        _print_nothing(args.show)
    else:
        _print_episode(episode)
    return 0


def cmd_evergreen(args) -> int:
    episode = pipeline.run_evergreen(args.show, args.dry_run)
    if episode is None:
        _print_nothing(args.show)
    else:
        _print_episode(episode)
    return 0


def cmd_breaking_scan(args) -> int:
    episodes = pipeline.run_breaking(args.dry_run)
    for episode in episodes:
        _print_episode(episode)
    print(f"breaking scan done: {len(episodes)} flash(es) published")
    return 0


def cmd_recheck(args) -> int:
    with Store() as store:
        llm = LLM(dry_run=args.dry_run)
        opened = recheck.recheck(store, llm, days=args.days)      # logs its own AgentRuns
        for cor in opened:
            print(f"opened  {cor.id}  episode {cor.episode_id}: {cor.description}")
        print(f"recheck done: {len(opened)} correction(s) opened for episodes of the last {args.days} day(s)")
        if args.apply:
            applied = corrections.apply_open(store)
            for ep in applied:
                print(f"applied  {ep.id} is now {ep.status}")
            print(f"{len(applied)} episode(s) corrected; notes, feeds and trust logs updated")
        elif opened:
            print("run again with --apply to publish them (notes, feed and trust log), or review first")
    return 0


def cmd_feeds(args) -> int:
    with Store() as store:
        built = pipeline.rebuild_feeds(store, args.show)
    for row in built:
        print(f"{row['show_id']}  {row['items']} item(s)  {row['path']}")
    if not built:
        print("no episodes in the store yet; nothing to build")
    return 0


def cmd_cost_report(args) -> int:
    since = None
    if args.days:
        since = (datetime.now(timezone.utc) - timedelta(days=args.days)).strftime("%Y-%m-%dT%H:%M:%SZ")
    with Store() as store:
        rows = pipeline.cost_rows(store, since=since)
    by_show: dict[str, float] = {}
    for row in rows:
        by_show[row["show_id"]] = round(by_show.get(row["show_id"], 0.0) + row["usd"], 6)
    total = round(sum(by_show.values()), 6)
    if args.json:
        print(json.dumps({"since": since, "rows": rows, "by_show": by_show, "total_usd": total}, indent=2))
        return 0

    window = f"last {args.days} day(s)" if args.days else "all time"
    print(f"Estimated agent spend, {window} (list prices in config.PRICES; real invoices differ)")
    if not rows:
        print("no agent runs logged yet")
        return 0
    table = [["SHOW", "AGENT", "RUNS", "FAILED", "IN TOKENS", "OUT TOKENS", "SEARCHES", "USD"]]
    current = None
    for row in rows:
        if current is not None and row["show_id"] != current:
            table.append([f"{current or '(none)'} total", "", "", "", "", "", "", f"{by_show[current]:.4f}"])
        current = row["show_id"]
        table.append([row["show_id"] or "(none)", row["agent_id"], row["runs"], row["failed"],
                      row["input_tokens"], row["output_tokens"], row["web_searches"], f"{row['usd']:.4f}"])
    table.append([f"{current or '(none)'} total", "", "", "", "", "", "", f"{by_show[current]:.4f}"])
    table.append(["ALL SHOWS", "", sum(r["runs"] for r in rows), sum(r["failed"] for r in rows),
                  sum(r["input_tokens"] for r in rows), sum(r["output_tokens"] for r in rows),
                  sum(r["web_searches"] for r in rows), f"{total:.4f}"])
    print("\n".join(_table(table, right=(2, 3, 4, 5, 6, 7))))
    return 0


# ================================================================== parser and entry point
def build_parser() -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--data-dir", metavar="PATH", default=argparse.SUPPRESS,
                        help="where the store and data/ live (default: EARLOBE_DATA_DIR, else ./data)")
    common.add_argument("-v", "--verbose", action="store_true", default=argparse.SUPPRESS,
                        help="debug logging and full tracebacks")

    parser = argparse.ArgumentParser(prog="earlobe", parents=[common],
                                     description="Project Earlobe: an automated, verified AI podcast network.")
    parser.set_defaults(data_dir=None, verbose=False)
    sub = parser.add_subparsers(dest="command", metavar="command", required=True)

    def add(name: str, handler, help: str, *, dry_run: bool = False, show: str | None = None):
        p = sub.add_parser(name, parents=[common], help=help, description=help)
        p.set_defaults(handler=handler)
        if show:
            p.add_argument("--show", metavar="ID", required=show == "required",
                           help="show id from config/shows.yaml")
        if dry_run:
            p.add_argument("--dry-run", action="store_true",
                           help="use fixtures instead of the network, Claude, ElevenLabs and the host (no keys needed)")
        return p

    p = add("list-shows", cmd_list_shows, "list the configured shows")
    p.add_argument("--json", action="store_true", help="print the show configs as JSON")
    add("run", cmd_run, "produce one episode of a show", dry_run=True, show="required")
    add("breaking-scan", cmd_breaking_scan, "scan for breaking news and cut a flash for each new story",
        dry_run=True)
    add("evergreen", cmd_evergreen, "produce the next queued episode of an archive or cold-case series",
        dry_run=True, show="required")
    p = add("recheck", cmd_recheck, "re-verify recent episodes and open corrections", dry_run=True)
    p.add_argument("--days", type=int, default=7, metavar="N", help="how many days back to look (default 7)")
    p.add_argument("--apply", action="store_true", help="also apply every open correction (notes, feed, trust log)")
    add("feeds", cmd_feeds, "rebuild the RSS feeds from the store", show="optional")
    p = add("cost-report", cmd_cost_report, "sum estimated agent spend by show and agent")
    p.add_argument("--days", type=int, default=0, metavar="N", help="only the last N days (default: all time)")
    p.add_argument("--json", action="store_true", help="print JSON instead of a table")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logger, handler, level = _install_logging(args.verbose)
    previous_dir = config.DATA_DIR
    if args.data_dir:
        config.DATA_DIR = Path(args.data_dir).expanduser().resolve()
    try:
        return args.handler(args)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
    except PipelineError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001 - the CLI reports every failure the same way
        if args.verbose:
            traceback.print_exc()
        print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    finally:
        config.DATA_DIR = previous_dir
        logger.removeHandler(handler)
        logger.setLevel(level)


if __name__ == "__main__":
    sys.exit(main())
