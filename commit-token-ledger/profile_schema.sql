-- Infinity user profile + personalized token rendering extension
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY,
    display_name TEXT,
    profile_version INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profile_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    feature_type TEXT NOT NULL,
    feature_key TEXT NOT NULL,
    feature_value TEXT,
    weight REAL NOT NULL DEFAULT 1.0,
    confidence REAL NOT NULL DEFAULT 1.0,
    source_type TEXT NOT NULL DEFAULT 'EXPLICIT',
    source_ref TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, feature_type, feature_key, source_type, source_ref),
    FOREIGN KEY(user_id) REFERENCES user_profiles(user_id)
);

CREATE TABLE IF NOT EXISTS profile_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    token_id TEXT,
    lane TEXT,
    details_json TEXT,
    consent_basis TEXT NOT NULL DEFAULT 'USER_ACTION',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user_profiles(user_id),
    FOREIGN KEY(token_id) REFERENCES tokens(token_id)
);

CREATE TABLE IF NOT EXISTS user_token_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    token_id TEXT NOT NULL,
    profile_version INTEGER NOT NULL,
    viewer_title TEXT,
    viewer_summary TEXT,
    primary_lane TEXT,
    primary_color TEXT,
    lane_scores_json TEXT NOT NULL,
    related_tokens_json TEXT,
    jump_links_json TEXT,
    ai_prompt TEXT,
    relevance_explanation TEXT,
    rendered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user_profiles(user_id),
    FOREIGN KEY(token_id) REFERENCES tokens(token_id)
);

CREATE INDEX IF NOT EXISTS idx_profile_features_user ON profile_features(user_id, active);
CREATE INDEX IF NOT EXISTS idx_profile_events_user_time ON profile_events(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_token_views_user_lane ON user_token_views(user_id, primary_lane, rendered_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_token_views_token ON user_token_views(token_id, rendered_at DESC);

-- Stable routing vocabulary. Personalized scoring chooses priority; these rows define semantics.
CREATE TABLE IF NOT EXISTS rendering_lanes (
    lane TEXT PRIMARY KEY,
    color_name TEXT NOT NULL,
    purpose TEXT NOT NULL
);

INSERT OR IGNORE INTO rendering_lanes(lane, color_name, purpose) VALUES
('ENGINEERING','GREEN','Build, fabrication, implementation and engineering work'),
('ASSIMILATION','PURPLE','Synthesis, integration and cross-token connection'),
('IMPORT','BLUE','External source, dependency, ingestion and imported work'),
('RESEARCH','YELLOW','Research, evidence, analysis and open questions'),
('DECISION','ORANGE','Review, choice, planning and next action'),
('REPAIR','RED','Repair, conflict, reroute, security or corrective attention');
