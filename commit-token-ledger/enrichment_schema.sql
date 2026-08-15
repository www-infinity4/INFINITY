-- Infinity Commit Token Ledger: enrichment extension
-- Safe to apply after schema.sql. Additive only.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS token_relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_token_id TEXT NOT NULL,
    target_token_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    evidence_level TEXT NOT NULL DEFAULT 'INFERRED',
    confidence REAL NOT NULL DEFAULT 0.5,
    reason TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_token_id, target_token_id, relationship_type),
    FOREIGN KEY(source_token_id) REFERENCES tokens(token_id),
    FOREIGN KEY(target_token_id) REFERENCES tokens(token_id)
);

CREATE INDEX IF NOT EXISTS idx_token_relationships_source ON token_relationships(source_token_id);
CREATE INDEX IF NOT EXISTS idx_token_relationships_target ON token_relationships(target_token_id);
CREATE INDEX IF NOT EXISTS idx_token_relationships_type ON token_relationships(relationship_type);

CREATE TABLE IF NOT EXISTS token_annotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    annotation_type TEXT NOT NULL,
    evidence_level TEXT NOT NULL,
    title TEXT,
    body TEXT NOT NULL,
    structured_json TEXT,
    author_type TEXT NOT NULL DEFAULT 'AI_RESEARCH_WRITER',
    author_id TEXT,
    model_or_engine TEXT,
    confidence REAL,
    source_refs_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    supersedes_annotation_id INTEGER,
    FOREIGN KEY(token_id) REFERENCES tokens(token_id),
    FOREIGN KEY(supersedes_annotation_id) REFERENCES token_annotations(id)
);

CREATE INDEX IF NOT EXISTS idx_token_annotations_token ON token_annotations(token_id);
CREATE INDEX IF NOT EXISTS idx_token_annotations_type ON token_annotations(annotation_type);

CREATE TABLE IF NOT EXISTS token_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT,
    evidence_level TEXT NOT NULL DEFAULT 'INFERRED',
    confidence REAL NOT NULL DEFAULT 0.5,
    reason TEXT,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(token_id) REFERENCES tokens(token_id)
);

CREATE INDEX IF NOT EXISTS idx_token_categories_token ON token_categories(token_id);
CREATE INDEX IF NOT EXISTS idx_token_categories_category ON token_categories(category);

CREATE TABLE IF NOT EXISTS research_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    job_type TEXT NOT NULL DEFAULT 'COMMIT_RESEARCH',
    priority INTEGER NOT NULL DEFAULT 50,
    status TEXT NOT NULL DEFAULT 'PENDING',
    attempts INTEGER NOT NULL DEFAULT 0,
    requested_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TEXT,
    completed_at TEXT,
    last_error TEXT,
    UNIQUE(token_id, job_type),
    FOREIGN KEY(token_id) REFERENCES tokens(token_id)
);

CREATE INDEX IF NOT EXISTS idx_research_queue_status_priority
ON research_queue(status, priority DESC, requested_at ASC);

CREATE TABLE IF NOT EXISTS recursive_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    caused_by_token_id TEXT,
    generator TEXT,
    operation TEXT,
    recursion_depth INTEGER NOT NULL DEFAULT 0,
    details_json TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(token_id) REFERENCES tokens(token_id),
    FOREIGN KEY(caused_by_token_id) REFERENCES tokens(token_id)
);

CREATE INDEX IF NOT EXISTS idx_recursive_events_token ON recursive_events(token_id);
CREATE INDEX IF NOT EXISTS idx_recursive_events_cause ON recursive_events(caused_by_token_id);

-- Backfill every token that already exists.
INSERT OR IGNORE INTO research_queue (token_id, job_type, priority)
SELECT token_id, 'COMMIT_RESEARCH', 50 FROM tokens;

-- Then guarantee that every future ledgered commit automatically becomes
-- research work. This is the account-wide token -> research handoff.
CREATE TRIGGER IF NOT EXISTS trg_token_enqueue_research
AFTER INSERT ON tokens
BEGIN
    INSERT OR IGNORE INTO research_queue (token_id, job_type, priority, status)
    VALUES (NEW.token_id, 'COMMIT_RESEARCH', 50, 'PENDING');
END;
