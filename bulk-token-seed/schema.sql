PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS bulk_tokens (
  token_id TEXT PRIMARY KEY,
  namespace TEXT NOT NULL,
  source_key TEXT NOT NULL,
  source_type TEXT NOT NULL DEFAULT 'GENERIC',
  source_pointer TEXT,
  normalized_payload TEXT NOT NULL,
  identity_hash TEXT NOT NULL UNIQUE,
  identity_brick_1 TEXT NOT NULL,
  identity_brick_2 TEXT NOT NULL,
  identity_brick_3 TEXT NOT NULL,
  identity_brick_4 TEXT NOT NULL,
  base_value TEXT NOT NULL DEFAULT '1',
  value_policy_version TEXT NOT NULL DEFAULT 'v1',
  value_hash TEXT NOT NULL,
  provenance_hash TEXT NOT NULL,
  interaction_root_hash TEXT NOT NULL,
  birth_at TEXT NOT NULL,
  git_commit_sha TEXT,
  lifecycle_state TEXT NOT NULL DEFAULT 'BRICKED'
    CHECK(lifecycle_state IN ('BRICKED','SEEDED','OPENED','RESEARCHED','CONNECTED','BUILD_READY','BUILT')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(namespace, source_key)
);

CREATE INDEX IF NOT EXISTS idx_bulk_tokens_state ON bulk_tokens(lifecycle_state);
CREATE INDEX IF NOT EXISTS idx_bulk_tokens_birth ON bulk_tokens(birth_at);

CREATE TABLE IF NOT EXISTS bulk_enrichment_queue (
  token_id TEXT PRIMARY KEY REFERENCES bulk_tokens(token_id) ON DELETE CASCADE,
  reason TEXT NOT NULL DEFAULT 'NEW_SEED',
  priority REAL NOT NULL DEFAULT 0.0,
  status TEXT NOT NULL DEFAULT 'PENDING'
    CHECK(status IN ('PENDING','RUNNING','COMPLETED','RETRY','DEFERRED')),
  requested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  started_at TEXT,
  completed_at TEXT,
  attempts INTEGER NOT NULL DEFAULT 0,
  last_error TEXT
);

CREATE TABLE IF NOT EXISTS token_interactions (
  interaction_id TEXT PRIMARY KEY,
  token_id TEXT NOT NULL REFERENCES bulk_tokens(token_id) ON DELETE CASCADE,
  target_token_id TEXT REFERENCES bulk_tokens(token_id) ON DELETE SET NULL,
  account_id TEXT NOT NULL,
  session_id TEXT,
  lane TEXT NOT NULL CHECK(lane IN ('GREEN','BLUE','YELLOW','ORANGE','RED','PURPLE','OPEN','VIEW','SAVE','OTHER')),
  action_type TEXT NOT NULL,
  anchor_text TEXT,
  source_view TEXT,
  target_view TEXT,
  profile_version TEXT,
  occurred_at TEXT NOT NULL,
  previous_interaction_hash TEXT,
  interaction_hash TEXT NOT NULL UNIQUE,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  checkpoint_id TEXT
);

CREATE INDEX IF NOT EXISTS idx_interactions_token_time ON token_interactions(token_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_interactions_account_time ON token_interactions(account_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_interactions_checkpoint ON token_interactions(checkpoint_id);

CREATE TABLE IF NOT EXISTS viewer_token_render (
  account_id TEXT NOT NULL,
  token_id TEXT NOT NULL REFERENCES bulk_tokens(token_id) ON DELETE CASCADE,
  profile_version TEXT NOT NULL,
  display_title TEXT,
  primary_lane TEXT CHECK(primary_lane IN ('GREEN','BLUE','YELLOW','ORANGE','RED','PURPLE')),
  lane_scores_json TEXT NOT NULL DEFAULT '{}',
  unlocked_depth INTEGER NOT NULL DEFAULT 0,
  visible_bricks_json TEXT NOT NULL DEFAULT '[]',
  jump_links_json TEXT NOT NULL DEFAULT '[]',
  render_reason_json TEXT NOT NULL DEFAULT '{}',
  rendered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(account_id, token_id, profile_version)
);

CREATE TABLE IF NOT EXISTS hourly_token_checkpoints (
  checkpoint_id TEXT PRIMARY KEY,
  window_start TEXT NOT NULL,
  window_end TEXT NOT NULL,
  event_count INTEGER NOT NULL DEFAULT 0,
  affected_token_count INTEGER NOT NULL DEFAULT 0,
  affected_account_count INTEGER NOT NULL DEFAULT 0,
  event_merkle_root TEXT,
  summary_hash TEXT NOT NULL,
  summary_json TEXT NOT NULL,
  git_commit_sha TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
