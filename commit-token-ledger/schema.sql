PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS repositories (
    full_name TEXT PRIMARY KEY,
    html_url TEXT,
    default_branch TEXT,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tokens (
    token_id TEXT PRIMARY KEY,
    source_key TEXT NOT NULL UNIQUE,
    repository TEXT NOT NULL,
    commit_sha TEXT NOT NULL,
    commit_url TEXT,
    commit_message TEXT,
    authored_at TEXT,
    committed_at TEXT,
    author_name TEXT,
    author_email TEXT,
    committer_name TEXT,
    committer_email TEXT,
    parent_shas TEXT NOT NULL DEFAULT '[]',
    discovered_at TEXT NOT NULL,
    initial_classification TEXT NOT NULL DEFAULT 'NON_SPACEX',
    current_classification TEXT NOT NULL DEFAULT 'NON_SPACEX',
    classification_score INTEGER NOT NULL DEFAULT 0,
    classification_evidence TEXT NOT NULL DEFAULT '[]',
    evidence_level TEXT NOT NULL DEFAULT 'OBSERVED',
    administrative INTEGER NOT NULL DEFAULT 0,
    UNIQUE(repository, commit_sha),
    FOREIGN KEY(repository) REFERENCES repositories(full_name)
);

CREATE TABLE IF NOT EXISTS token_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    from_classification TEXT,
    to_classification TEXT,
    score INTEGER,
    evidence TEXT NOT NULL DEFAULT '[]',
    reason TEXT,
    evidence_level TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(token_id) REFERENCES tokens(token_id)
);

CREATE INDEX IF NOT EXISTS idx_tokens_repo ON tokens(repository);
CREATE INDEX IF NOT EXISTS idx_tokens_class ON tokens(current_classification);
CREATE INDEX IF NOT EXISTS idx_events_token ON token_events(token_id);
