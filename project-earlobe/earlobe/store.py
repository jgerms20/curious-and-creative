"""SQLite store: one generic table of JSON blobs, plus agent-run logging.

Everything the engine persists (stories, scripts, reports, episodes, corrections)
goes through put/get/list. Kinds are free-form strings ("script", "episode",
"verifier_report", ...). Agent runs are stored the same way under kind
"agent_run", so cost per show per day is a plain list() away; spend() sums it.

Timestamps are ISO-8601 UTC strings ("2026-10-11T13:00:00Z"), which sort as text.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path

from earlobe import config
from earlobe.schemas import AgentRun

_SCHEMA = """
CREATE TABLE IF NOT EXISTS objects (
    kind       TEXT NOT NULL,
    id         TEXT NOT NULL,
    show_id    TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    body       TEXT NOT NULL,
    PRIMARY KEY (kind, id)
);
CREATE INDEX IF NOT EXISTS objects_by_show ON objects (kind, show_id, created_at);
"""
AGENT_RUN = "agent_run"


def _iso(t: datetime | str | None = None) -> str:
    if isinstance(t, str):
        return t
    t = t or datetime.now(timezone.utc)
    return t.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Store:
    def __init__(self, path: str | Path | None = None):
        path = config.DATA_DIR / "earlobe.db" if path is None else path
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.path = str(path)
        self.db = sqlite3.connect(self.path)
        self.db.executescript(_SCHEMA)

    def close(self) -> None:
        self.db.close()

    def __enter__(self) -> "Store":
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    # ------------------------------------------------------------ objects
    def put(self, kind: str, id: str, obj: dict, show_id: str = "", *,
            created_at: datetime | str | None = None) -> None:
        """Insert or replace an object. Keeps the original created_at and any known show_id."""
        if hasattr(obj, "to_dict"):
            obj = obj.to_dict()
        show_id = show_id or str(obj.get("show_id") or "")
        now = _iso()
        self.db.execute(
            "INSERT INTO objects (kind, id, show_id, created_at, updated_at, body) "
            "VALUES (?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(kind, id) DO UPDATE SET "
            "show_id = COALESCE(NULLIF(excluded.show_id, ''), objects.show_id), "
            "updated_at = excluded.updated_at, body = excluded.body",
            (kind, id, show_id, _iso(created_at) if created_at else now, now,
             json.dumps(obj, ensure_ascii=False)))
        self.db.commit()

    def get(self, kind: str, id: str) -> dict | None:
        row = self.db.execute("SELECT body FROM objects WHERE kind = ? AND id = ?",
                              (kind, id)).fetchone()
        return json.loads(row[0]) if row else None

    def list(self, kind: str, show_id: str | None = None,
             since: datetime | str | None = None) -> list[dict]:
        """Objects of a kind, oldest first. since filters on created_at."""
        sql, args = "SELECT body FROM objects WHERE kind = ?", [kind]
        if show_id is not None:
            sql, args = sql + " AND show_id = ?", args + [show_id]
        if since is not None:
            sql, args = sql + " AND created_at >= ?", args + [_iso(since)]
        rows = self.db.execute(sql + " ORDER BY created_at, rowid", args).fetchall()
        return [json.loads(r[0]) for r in rows]

    # ------------------------------------------------------------ agent runs
    def log_run(self, run: AgentRun, show_id: str = "") -> None:
        """Record one agent call. show_id attributes the cost to a show for budgets."""
        self.put(AGENT_RUN, run.run_id, run.to_dict(), show_id,
                 created_at=run.started_at or None)

    def spend(self, show_id: str | None = None, day: date | str | None = None) -> float:
        """Estimated USD spent by logged runs, optionally for one show and one UTC day (YYYY-MM-DD)."""
        day = day.strftime("%Y-%m-%d") if isinstance(day, date) else day
        runs = self.list(AGENT_RUN, show_id=show_id, since=day)
        return round(sum(r.get("usd_estimate", 0.0) for r in runs
                         if day is None or str(r.get("started_at", "")).startswith(day)), 6)
