PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS wallet_accounts (
  user_id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS source_policies (
  source_key TEXT PRIMARY KEY,
  user_daily_limit INTEGER NOT NULL,
  min_interval_seconds INTEGER NOT NULL DEFAULT 0,
  one_at_a_time INTEGER NOT NULL DEFAULT 0,
  overflow_owner TEXT NOT NULL DEFAULT 'NONE',
  policy_version INTEGER NOT NULL DEFAULT 1
);

INSERT OR REPLACE INTO source_policies
(source_key,user_daily_limit,min_interval_seconds,one_at_a_time,overflow_owner,policy_version)
VALUES
('INFINITY_MINT',10,0,1,'NONE',1),
('ALIEN_RADIO',10,3600,0,'NONE',1),
('BITCOIN_CRUSHER',10,0,0,'INFINITY_SYSTEM_POOL',1),
('MARIO_SPIN',10,0,0,'INFINITY_SYSTEM_POOL',1);

CREATE TABLE IF NOT EXISTS generation_events (
  event_id TEXT PRIMARY KEY,
  idempotency_key TEXT NOT NULL UNIQUE,
  user_id TEXT NOT NULL,
  source_key TEXT NOT NULL REFERENCES source_policies(source_key),
  action_key TEXT NOT NULL,
  source_token_id TEXT,
  optional_input TEXT,
  occurred_at TEXT NOT NULL,
  account_day TEXT NOT NULL,
  source_day_ordinal INTEGER NOT NULL,
  evidence_json TEXT NOT NULL DEFAULT '{}',
  event_hash TEXT NOT NULL UNIQUE
);

CREATE INDEX IF NOT EXISTS idx_generation_user_source_day
ON generation_events(user_id, source_key, account_day, source_day_ordinal);

CREATE TABLE IF NOT EXISTS economy_tokens (
  token_id TEXT PRIMARY KEY,
  generation_event_id TEXT NOT NULL UNIQUE REFERENCES generation_events(event_id),
  canonical_denomination INTEGER NOT NULL DEFAULT 1 CHECK(canonical_denomination = 1),
  denomination_unit TEXT NOT NULL DEFAULT 'INFINITY',
  canonical_hash TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS token_allocations (
  allocation_id TEXT PRIMARY KEY,
  token_id TEXT NOT NULL REFERENCES economy_tokens(token_id),
  owner_type TEXT NOT NULL CHECK(owner_type IN ('USER','INFINITY_SYSTEM_POOL')),
  owner_id TEXT NOT NULL,
  reason TEXT NOT NULL,
  allocated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_allocations_owner
ON token_allocations(owner_type, owner_id, allocated_at);

CREATE TABLE IF NOT EXISTS wallet_views (
  user_id TEXT NOT NULL,
  token_id TEXT NOT NULL REFERENCES economy_tokens(token_id),
  first_seen_at TEXT NOT NULL,
  last_seen_at TEXT NOT NULL,
  PRIMARY KEY(user_id, token_id)
);

CREATE TABLE IF NOT EXISTS token_analytics (
  token_id TEXT NOT NULL REFERENCES economy_tokens(token_id),
  metric_key TEXT NOT NULL,
  metric_value REAL,
  metric_text TEXT,
  evidence_level TEXT NOT NULL CHECK(evidence_level IN ('OBSERVED','INFERRED','EXTERNALLY_VERIFIED','USER_DEFINED')),
  calculated_at TEXT NOT NULL,
  PRIMARY KEY(token_id, metric_key, calculated_at)
);

CREATE TABLE IF NOT EXISTS source_sessions (
  session_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  source_key TEXT NOT NULL REFERENCES source_policies(source_key),
  started_at TEXT NOT NULL,
  ended_at TEXT,
  evidence_json TEXT NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS pool_movements (
  movement_id TEXT PRIMARY KEY,
  token_id TEXT NOT NULL REFERENCES economy_tokens(token_id),
  from_owner TEXT NOT NULL,
  to_owner TEXT NOT NULL,
  reason TEXT NOT NULL,
  occurred_at TEXT NOT NULL,
  movement_hash TEXT NOT NULL UNIQUE
);
