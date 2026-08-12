-- Rich, additive package around an immutable Infinity Commit Token.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS token_packages (
    token_id TEXT PRIMARY KEY,
    package_schema TEXT NOT NULL DEFAULT 'infinity/token-package/v1',
    status TEXT NOT NULL DEFAULT 'BUILDING' CHECK(status IN ('BUILDING','READY','REVIEW_REQUIRED')),
    project_research_entry_id INTEGER,
    discovery_research_entry_id INTEGER,
    utility_target_microunits INTEGER NOT NULL DEFAULT 1000000,
    utility_unit TEXT NOT NULL DEFAULT 'INFINITY',
    utility_reference_microunits INTEGER NOT NULL DEFAULT 0,
    market_value_microunits INTEGER,
    valuation_evidence_level TEXT NOT NULL DEFAULT 'USER_DEFINED',
    manifest_json TEXT,
    manifest_sha256 TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(project_research_entry_id) REFERENCES research_stream_entries(entry_id),
    FOREIGN KEY(discovery_research_entry_id) REFERENCES research_stream_entries(entry_id)
);

CREATE TABLE IF NOT EXISTS token_pr_context (
    token_id TEXT NOT NULL,
    repository TEXT NOT NULL,
    pr_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT,
    html_url TEXT NOT NULL,
    state TEXT,
    base_ref TEXT,
    head_ref TEXT,
    merge_commit_sha TEXT,
    changed_files INTEGER,
    additions INTEGER,
    deletions INTEGER,
    review_summary_json TEXT,
    check_summary_json TEXT,
    evidence_level TEXT NOT NULL DEFAULT 'OBSERVED',
    retrieved_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(token_id, repository, pr_number)
);

CREATE TABLE IF NOT EXISTS token_keywords (
    keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    keyword TEXT NOT NULL,
    normalized_keyword TEXT NOT NULL,
    source_type TEXT NOT NULL CHECK(source_type IN (
        'USER','COMMIT','PR','HISTORY','CROSS_INPUT','AI_SUGGESTED'
    )),
    source_ref TEXT,
    confidence REAL NOT NULL DEFAULT 1.0,
    accepted INTEGER NOT NULL DEFAULT 1,
    evidence_level TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(token_id, normalized_keyword, source_type, source_ref)
);

CREATE INDEX IF NOT EXISTS idx_token_keywords_lookup
ON token_keywords(token_id, accepted, confidence DESC);

CREATE TABLE IF NOT EXISTS token_media_candidates (
    media_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    provider_identifier TEXT NOT NULL,
    media_type TEXT NOT NULL CHECK(media_type IN ('MOVIE','SONG','AUDIO','VIDEO','IMAGE','TEXT','SOFTWARE')),
    title TEXT NOT NULL,
    details_url TEXT NOT NULL,
    playable_url TEXT,
    license_url TEXT,
    rights_statement TEXT,
    rights_status TEXT NOT NULL CHECK(rights_status IN ('VERIFIED_REUSE','REVIEW_REQUIRED','BLOCKED')),
    availability_status TEXT NOT NULL DEFAULT 'METADATA_ONLY',
    source_metadata_json TEXT NOT NULL,
    source_metadata_sha256 TEXT NOT NULL,
    retrieved_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(token_id, provider, provider_identifier, media_type)
);

CREATE TABLE IF NOT EXISTS token_utility_components (
    component_id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_id TEXT NOT NULL,
    component_type TEXT NOT NULL CHECK(component_type IN (
        'COMMIT_CONTEXT','PR_CONTEXT','PROJECT_RESEARCH','DISCOVERY_RESEARCH',
        'MOVIE_ACCESS','SONG_ACCESS','CREATIVE_ATTACHMENT'
    )),
    component_ref TEXT NOT NULL,
    reference_microunits INTEGER NOT NULL,
    utility_unit TEXT NOT NULL DEFAULT 'INFINITY',
    basis TEXT NOT NULL DEFAULT 'USER_DEFINED_REFERENCE',
    evidence_level TEXT NOT NULL DEFAULT 'USER_DEFINED',
    usable INTEGER NOT NULL DEFAULT 1,
    note TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(token_id, component_type, component_ref)
);

CREATE INDEX IF NOT EXISTS idx_token_utility_total
ON token_utility_components(token_id, usable);
