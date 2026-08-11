-- Infinity two-stream research library.
-- Additive schema: does not replace immutable commit token records.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS research_stream_entries (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    stream_type TEXT NOT NULL CHECK(stream_type IN (
        'PROJECT_RESEARCH',
        'INFINITY_DISCOVERY_RESEARCH'
    )),
    version INTEGER NOT NULL DEFAULT 1,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    structured_json TEXT,
    evidence_level TEXT NOT NULL CHECK(evidence_level IN (
        'OBSERVED','INFERRED','EXTERNALLY_VERIFIED','USER_DEFINED'
    )),
    source_token_id TEXT,
    source_urls_json TEXT,
    model_or_engine TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    supersedes_entry_id INTEGER,
    active INTEGER NOT NULL DEFAULT 1,
    UNIQUE(token_id, stream_type, version),
    FOREIGN KEY(supersedes_entry_id) REFERENCES research_stream_entries(entry_id)
);

CREATE INDEX IF NOT EXISTS idx_research_stream_token
ON research_stream_entries(token_id, stream_type, active, version);

CREATE TABLE IF NOT EXISTS research_sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    url TEXT,
    source_title TEXT,
    publisher TEXT,
    retrieved_at TEXT,
    excerpt_or_note TEXT,
    verification_status TEXT NOT NULL DEFAULT 'PENDING',
    FOREIGN KEY(entry_id) REFERENCES research_stream_entries(entry_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS discovery_links (
    discovery_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_token_id TEXT NOT NULL,
    candidate_token_id TEXT NOT NULL,
    research_entry_id INTEGER,
    status TEXT NOT NULL DEFAULT 'EXPLORATORY_LINK',
    relationship_type TEXT,
    confidence REAL NOT NULL DEFAULT 0.0,
    reason TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_token_id, candidate_token_id, research_entry_id),
    FOREIGN KEY(research_entry_id) REFERENCES research_stream_entries(entry_id)
);

CREATE TABLE IF NOT EXISTS render_action_candidates (
    candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    source_token_id TEXT NOT NULL,
    target_token_id TEXT,
    lane TEXT NOT NULL CHECK(lane IN (
        'GREEN_ENGINEER','BLUE_IMPORT','YELLOW_RESEARCH',
        'ORANGE_DECIDE','RED_ROUTE','PURPLE_ASSIMILATE'
    )),
    anchor_text TEXT NOT NULL,
    display_text TEXT NOT NULL,
    plan_json TEXT NOT NULL,
    evidence_level TEXT NOT NULL DEFAULT 'INFERRED',
    score REAL NOT NULL DEFAULT 0.0,
    profile_version INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TEXT,
    accepted_at TEXT,
    rejected_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_render_actions_user_lane
ON render_action_candidates(user_id, lane, score DESC);
