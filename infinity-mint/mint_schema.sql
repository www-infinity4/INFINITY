PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS mint_notes (
  note_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  local_day TEXT NOT NULL,
  daily_position INTEGER NOT NULL CHECK (daily_position BETWEEN 1 AND 10),
  denomination INTEGER NOT NULL DEFAULT 1 CHECK (denomination = 1),
  state TEXT NOT NULL DEFAULT 'DRAFT' CHECK (state IN ('DRAFT','FINALIZED','CHECKPOINTED','COMMIT_BOUND','ARCHIVED')),
  provisional_sha256 TEXT,
  git_repository TEXT,
  git_commit_sha TEXT,
  commit_token_id TEXT,
  displayed_serial TEXT,
  canonical_json TEXT NOT NULL,
  profile_version INTEGER,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finalized_at TEXT,
  commit_bound_at TEXT,
  UNIQUE(user_id, local_day, daily_position)
);

CREATE TABLE IF NOT EXISTS mint_assets (
  asset_id TEXT PRIMARY KEY,
  note_id TEXT NOT NULL REFERENCES mint_notes(note_id) ON DELETE CASCADE,
  asset_type TEXT NOT NULL CHECK (asset_type IN (
    'SIGNATURE','IMAGE','AUDIO','VIDEO','POEM','STORY','CARD','PROJECT','RESEARCH',
    'ALIEN_COIN','TREE_COUPON','LINK','OTHER','AI_CURATED'
  )),
  title TEXT,
  media_type TEXT,
  content_uri TEXT,
  content_hash TEXT,
  metadata_json TEXT NOT NULL DEFAULT '{}',
  privacy TEXT NOT NULL DEFAULT 'PRIVATE' CHECK (privacy IN ('PRIVATE','TOKEN_ONLY','PUBLIC')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mint_research_links (
  note_id TEXT NOT NULL REFERENCES mint_notes(note_id) ON DELETE CASCADE,
  research_entry_id TEXT NOT NULL,
  stream TEXT NOT NULL CHECK (stream IN ('PROJECT_RESEARCH','INFINITY_DISCOVERY_RESEARCH')),
  relationship_type TEXT NOT NULL DEFAULT 'ATTACHED',
  score REAL,
  PRIMARY KEY(note_id, research_entry_id, stream)
);

CREATE TABLE IF NOT EXISTS mint_render_actions (
  action_candidate_id TEXT PRIMARY KEY,
  note_id TEXT NOT NULL REFERENCES mint_notes(note_id) ON DELETE CASCADE,
  user_id TEXT NOT NULL,
  profile_version INTEGER NOT NULL,
  lane TEXT NOT NULL CHECK (lane IN ('GREEN','BLUE','YELLOW','ORANGE','RED','PURPLE')),
  source_token_id TEXT,
  target_token_id TEXT,
  anchor_text TEXT NOT NULL,
  display_text TEXT NOT NULL,
  plan_json TEXT NOT NULL DEFAULT '{}',
  score REAL NOT NULL DEFAULT 0,
  evidence_level TEXT NOT NULL CHECK (evidence_level IN ('OBSERVED','INFERRED','EXTERNALLY_VERIFIED','USER_DEFINED')),
  generated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mint_checkpoint_batches (
  batch_id TEXT PRIMARY KEY,
  window_start TEXT NOT NULL,
  window_end TEXT NOT NULL,
  note_count INTEGER NOT NULL DEFAULT 0,
  action_count INTEGER NOT NULL DEFAULT 0,
  report_json TEXT NOT NULL DEFAULT '{}',
  git_commit_sha TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_mint_notes_wallet ON mint_notes(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mint_notes_commit ON mint_notes(git_commit_sha);
CREATE INDEX IF NOT EXISTS idx_mint_assets_note ON mint_assets(note_id, asset_type);
CREATE INDEX IF NOT EXISTS idx_mint_actions_user_lane ON mint_render_actions(user_id, lane, score DESC);
