-- Earlobe core schema (Supabase / Postgres).
--
-- One table per kind of thing the engine stores. Each row is the engine's own JSON (the
-- dataclasses in earlobe/schemas.py, via .to_dict()) in `payload`, plus a few promoted columns
-- so the common questions (this show, this day, this script) are plain indexed queries.
--
--   engine kind (earlobe/store.py)                  table
--   signal                                          signals
--   story                                           stories
--   script                                          scripts
--   verifier_report, factcheck_report, bias_report,
--     legal_report, recheck_report                  checker_reports   (column `checker`)
--   gate_decision                                   gate_decisions
--   episode                                         episodes
--   correction                                      corrections
--   agent_run                                       agent_runs        (budget: sum usd by show and day)
--
-- Conventions
--   * ids are the text ids the engine mints (sty_..., scr_..., ep_..., cor_..., run_...).
--     There are no foreign keys on purpose: this is an append-mostly audit log, and a partial
--     write must never block the log from recording what happened.
--   * show_id is '' when a row belongs to no single show (signals, unassigned stories).
--   * the closed vocabularies below mirror earlobe/schemas.py (DECISIONS, EPISODE_STATUS and the
--     Correction fields). Change them there and here together.
--
-- ROW LEVEL SECURITY: enabled on every table, with NO policies. That is deliberate.
--   With RLS on and no policy, the anon and authenticated roles (the keys that can ship in a
--   browser or app) can read and write nothing. Only the service_role key, which bypasses RLS,
--   can touch these tables, and it lives only in server-side secrets (GitHub Actions, the
--   engine host). Nobody reads this database from the public side: what the public sees is the
--   static output of the engine (RSS feeds, audio, the public trust log, the corrections page).
--   Script drafts, unpublished stories and the checkers' working reports must never leak, so we
--   also revoke the default grants as a second lock. If a table ever has to be read from a
--   browser, add one narrow SELECT policy for that table in a new migration. Never a blanket one.

-- ---------------------------------------------------------------- signals
create table if not exists public.signals (
  id          text primary key,
  show_id     text not null default '',
  market      text not null default '',
  beat        text not null default '',
  payload     jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- ---------------------------------------------------------------- stories
create table if not exists public.stories (
  id          text primary key,
  show_id     text not null default '',
  market      text not null default '',
  beat        text not null default '',
  payload     jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- ---------------------------------------------------------------- scripts
create table if not exists public.scripts (
  id            text primary key,
  show_id       text not null default '',
  episode_date  text not null default '',
  lane_policy   text not null default 'standard',
  revision      integer not null default 0,
  payload       jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ---------------------------------------------------------------- checker_reports
-- One row per report from an independent checker. `checker` is free text on purpose so a new
-- checker needs no migration: verifier | factcheck | bias | legal | recheck today.
create table if not exists public.checker_reports (
  id          text primary key,
  show_id     text not null default '',
  script_id   text not null,
  checker     text not null,
  revision    integer not null default 0,
  payload     jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- ---------------------------------------------------------------- gate_decisions
create table if not exists public.gate_decisions (
  id           text primary key,
  show_id      text not null default '',
  script_id    text not null,
  decision     text not null check (decision in ('PUBLISH', 'REWRITE', 'HOLD', 'KILL')),
  lane_policy  text not null default 'standard',
  revision     integer not null default 0,
  payload      jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

-- ---------------------------------------------------------------- episodes
create table if not exists public.episodes (
  id            text primary key,
  show_id       text not null default '',
  script_id     text not null default '',
  status        text not null default 'draft'
                check (status in ('draft', 'gated', 'rendered', 'published', 'corrected',
                                  'retracted', 'killed')),
  published_at  timestamptz,
  payload       jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ---------------------------------------------------------------- corrections
create table if not exists public.corrections (
  id           text primary key,
  show_id      text not null default '',
  episode_id   text not null,
  claim_id     text not null default '',
  reported_by  text not null default '',
  status       text not null default 'open' check (status in ('open', 'applied', 'rejected')),
  action       text not null default 'note' check (action in ('note', 'reissue', 'retract')),
  payload      jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

-- ---------------------------------------------------------------- agent_runs
-- id is AgentRun.run_id. The budget guard sums usd_estimate per show per UTC day of started_at.
create table if not exists public.agent_runs (
  id            text primary key,
  show_id       text not null default '',
  agent_id      text not null,
  model_tier    text not null default '',
  started_at    timestamptz not null default now(),
  usd_estimate  numeric(12, 6) not null default 0,
  ok            boolean not null default true,
  payload       jsonb not null check (jsonb_typeof(payload) = 'object'),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ---------------------------------------------------------------- indexes
create index if not exists signals_show_created_idx          on public.signals (show_id, created_at desc);
create index if not exists signals_market_created_idx        on public.signals (market, created_at desc);
create index if not exists stories_show_created_idx          on public.stories (show_id, created_at desc);
create index if not exists stories_market_created_idx        on public.stories (market, created_at desc);
create index if not exists scripts_show_created_idx          on public.scripts (show_id, created_at desc);
create index if not exists checker_reports_show_created_idx  on public.checker_reports (show_id, created_at desc);
create index if not exists checker_reports_script_idx        on public.checker_reports (script_id, checker);
create index if not exists gate_decisions_show_created_idx   on public.gate_decisions (show_id, created_at desc);
create index if not exists gate_decisions_script_idx         on public.gate_decisions (script_id);
create index if not exists episodes_show_created_idx         on public.episodes (show_id, created_at desc);
create index if not exists episodes_show_published_idx       on public.episodes (show_id, published_at desc);
create index if not exists episodes_status_idx               on public.episodes (status);
create index if not exists corrections_show_created_idx      on public.corrections (show_id, created_at desc);
create index if not exists corrections_episode_idx           on public.corrections (episode_id);
create index if not exists corrections_open_idx              on public.corrections (created_at desc) where status = 'open';
create index if not exists agent_runs_show_created_idx       on public.agent_runs (show_id, created_at desc);
create index if not exists agent_runs_show_started_idx       on public.agent_runs (show_id, started_at);

-- ---------------------------------------------------------------- updated_at
create or replace function public.earlobe_touch_updated_at()
returns trigger
language plpgsql
set search_path = ''
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

revoke all on function public.earlobe_touch_updated_at() from public, anon, authenticated;

do $$
declare
  t text;
begin
  foreach t in array array['signals', 'stories', 'scripts', 'checker_reports', 'gate_decisions',
                           'episodes', 'corrections', 'agent_runs']
  loop
    execute format('drop trigger if exists %I on public.%I', t || '_touch_updated_at', t);
    execute format('create trigger %I before update on public.%I '
                   'for each row execute function public.earlobe_touch_updated_at()',
                   t || '_touch_updated_at', t);
  end loop;
end;
$$;

-- ---------------------------------------------------------------- row level security (no policies)
alter table public.signals          enable row level security;
alter table public.stories          enable row level security;
alter table public.scripts          enable row level security;
alter table public.checker_reports  enable row level security;
alter table public.gate_decisions   enable row level security;
alter table public.episodes         enable row level security;
alter table public.corrections      enable row level security;
alter table public.agent_runs       enable row level security;

revoke all on table public.signals, public.stories, public.scripts, public.checker_reports,
                    public.gate_decisions, public.episodes, public.corrections, public.agent_runs
  from anon, authenticated;
