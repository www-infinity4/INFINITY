PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS avatar_coins (
  avatar_coin_id TEXT PRIMARY KEY,
  content_hash TEXT NOT NULL UNIQUE,
  creator_account_id TEXT NOT NULL,
  source_repo TEXT NOT NULL,
  source_page TEXT,
  source_anchor TEXT,
  parent_avatar_coin_id TEXT REFERENCES avatar_coins(avatar_coin_id),
  created_at TEXT NOT NULL,
  account_day TEXT NOT NULL,
  daily_creator_ordinal INTEGER NOT NULL,
  allocation_state TEXT NOT NULL CHECK(allocation_state IN ('CREATOR_WALLET','PROJECT_MATCH_POOL','PURCHASED_TRANSFERRED')),
  canonical_payload_json TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_avatar_daily_ordinal ON avatar_coins(creator_account_id, account_day, daily_creator_ordinal);

CREATE TABLE IF NOT EXISTS avatar_coin_events (
  event_id TEXT PRIMARY KEY,
  avatar_coin_id TEXT NOT NULL REFERENCES avatar_coins(avatar_coin_id),
  actor_account_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  event_hash TEXT NOT NULL UNIQUE,
  event_payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS avatar_coin_holdings (
  avatar_coin_id TEXT PRIMARY KEY REFERENCES avatar_coins(avatar_coin_id),
  holder_account_id TEXT,
  holder_state TEXT NOT NULL CHECK(holder_state IN ('CREATOR_WALLET','UNALLOCATED_POOL','PURCHASED','TRANSFERRED')),
  changed_at TEXT NOT NULL,
  transaction_ref TEXT
);

CREATE TABLE IF NOT EXISTS avatar_feed_candidates (
  candidate_id TEXT PRIMARY KEY,
  avatar_coin_id TEXT NOT NULL REFERENCES avatar_coins(avatar_coin_id),
  viewer_account_id TEXT NOT NULL,
  profile_version TEXT,
  score REAL NOT NULL,
  reason TEXT NOT NULL,
  suggested_lane TEXT CHECK(suggested_lane IN ('GREEN','BLUE','YELLOW','ORANGE','RED','PURPLE')),
  anchor_text TEXT,
  render_payload_json TEXT NOT NULL,
  state TEXT NOT NULL DEFAULT 'READY' CHECK(state IN ('READY','RENDERED','OPENED','DISMISSED','ACCEPTED')),
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_avatar_feed_viewer ON avatar_feed_candidates(viewer_account_id, state, score DESC);

CREATE TABLE IF NOT EXISTS avatar_transfers (
  transfer_id TEXT PRIMARY KEY,
  avatar_coin_id TEXT NOT NULL REFERENCES avatar_coins(avatar_coin_id),
  from_account_id TEXT,
  to_account_id TEXT NOT NULL,
  transfer_type TEXT NOT NULL CHECK(transfer_type IN ('PURCHASE','GIFT','ASSIGNMENT')),
  transaction_ref TEXT,
  created_at TEXT NOT NULL
);
