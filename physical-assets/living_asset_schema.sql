PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS asset_rights_bundles (
  rights_bundle_id TEXT PRIMARY KEY,
  token_id TEXT NOT NULL,
  entitlement_id TEXT,
  contract_reference TEXT,
  rights_json TEXT NOT NULL,
  transferable INTEGER NOT NULL DEFAULT 0,
  redeemable INTEGER NOT NULL DEFAULT 0,
  effective_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires_at TEXT,
  evidence_level TEXT NOT NULL DEFAULT 'OBSERVED',
  evidence_json TEXT
);

CREATE TABLE IF NOT EXISTS token_holders (
  token_id TEXT NOT NULL,
  account_id TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'HOLDER',
  acquired_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  released_at TEXT,
  acquisition_event_id TEXT,
  PRIMARY KEY (token_id, account_id, acquired_at)
);

CREATE TABLE IF NOT EXISTS asset_transfer_events (
  transfer_event_id TEXT PRIMARY KEY,
  token_id TEXT NOT NULL,
  entitlement_id TEXT,
  rights_bundle_id TEXT,
  from_account_id TEXT,
  to_account_id TEXT,
  transfer_type TEXT NOT NULL CHECK (transfer_type IN (
    'SALE','GIFT','ASSIGNMENT','INHERITANCE','CUSTODY_TRANSFER','OTHER'
  )),
  status TEXT NOT NULL CHECK (status IN (
    'PROPOSED','AUTHORIZED','SETTLED','REJECTED','CANCELLED'
  )),
  consideration_amount REAL,
  consideration_currency TEXT,
  contract_reference TEXT,
  occurred_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  evidence_level TEXT NOT NULL DEFAULT 'OBSERVED',
  evidence_json TEXT
);

CREATE TABLE IF NOT EXISTS asset_value_observations (
  value_observation_id TEXT PRIMARY KEY,
  token_id TEXT NOT NULL,
  physical_asset_id TEXT,
  value_type TEXT NOT NULL CHECK (value_type IN (
    'INFINITY_BASE','MERCHANT_QUOTE','RESERVATION_AMOUNT','PURCHASE_PRICE',
    'APPRAISAL','LISTING_PRICE','SALE_PRICE','INTERNAL_RESEARCH_SCORE'
  )),
  amount REAL,
  currency_or_unit TEXT,
  source_reference TEXT,
  observed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  evidence_level TEXT NOT NULL,
  evidence_json TEXT
);

CREATE TABLE IF NOT EXISTS asset_derivative_projects (
  derivative_id TEXT PRIMARY KEY,
  source_token_id TEXT NOT NULL,
  descendant_token_id TEXT,
  project_type TEXT NOT NULL,
  title TEXT,
  description TEXT,
  profile_render_context_json TEXT,
  created_by_account_id TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status TEXT NOT NULL DEFAULT 'PROPOSED',
  evidence_level TEXT NOT NULL DEFAULT 'USER_DEFINED'
);

CREATE TABLE IF NOT EXISTS asset_documents (
  document_id TEXT PRIMARY KEY,
  token_id TEXT NOT NULL,
  physical_asset_id TEXT,
  derivative_id TEXT,
  document_type TEXT NOT NULL,
  title TEXT,
  content_reference TEXT NOT NULL,
  content_hash TEXT,
  source_reference TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  evidence_level TEXT NOT NULL,
  evidence_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_asset_transfers_token ON asset_transfer_events(token_id, occurred_at);
CREATE INDEX IF NOT EXISTS idx_asset_values_token ON asset_value_observations(token_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_asset_derivatives_source ON asset_derivative_projects(source_token_id, created_at);
CREATE INDEX IF NOT EXISTS idx_asset_documents_token ON asset_documents(token_id, created_at);
