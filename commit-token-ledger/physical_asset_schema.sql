PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS merchants (
  merchant_id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL,
  legal_name TEXT,
  website TEXT,
  location_text TEXT,
  verification_state TEXT NOT NULL DEFAULT 'UNVERIFIED',
  evidence_level TEXT NOT NULL DEFAULT 'INFERRED',
  evidence_json TEXT NOT NULL DEFAULT '[]',
  verified_at TEXT
);

CREATE TABLE IF NOT EXISTS physical_assets (
  physical_asset_id TEXT PRIMARY KEY,
  merchant_id TEXT NOT NULL REFERENCES merchants(merchant_id),
  asset_type TEXT NOT NULL,
  title TEXT NOT NULL,
  sku TEXT,
  certificate_number TEXT,
  attributes_json TEXT NOT NULL DEFAULT '{}',
  price_amount REAL,
  price_currency TEXT,
  inventory_state TEXT NOT NULL DEFAULT 'UNKNOWN',
  evidence_level TEXT NOT NULL DEFAULT 'INFERRED',
  evidence_json TEXT NOT NULL DEFAULT '[]',
  observed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS asset_entitlements (
  entitlement_id TEXT PRIMARY KEY,
  account_id TEXT NOT NULL,
  token_id TEXT NOT NULL,
  physical_asset_id TEXT NOT NULL REFERENCES physical_assets(physical_asset_id),
  symbol TEXT NOT NULL,
  state TEXT NOT NULL DEFAULT 'DISCOVERED',
  funding_rule_id TEXT,
  funded_amount REAL NOT NULL DEFAULT 0,
  funded_currency TEXT,
  reservation_reference TEXT,
  custody_reference TEXT,
  shipping_reference TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS asset_state_events (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  entitlement_id TEXT NOT NULL REFERENCES asset_entitlements(entitlement_id),
  from_state TEXT,
  to_state TEXT NOT NULL,
  evidence_level TEXT NOT NULL,
  reason TEXT,
  evidence_json TEXT NOT NULL DEFAULT '[]',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS economic_events (
  event_id TEXT PRIMARY KEY,
  account_id TEXT NOT NULL,
  token_id TEXT,
  action_token_id TEXT,
  event_type TEXT NOT NULL,
  gross_amount REAL,
  currency TEXT,
  compensable INTEGER NOT NULL DEFAULT 0,
  credited_amount REAL NOT NULL DEFAULT 0,
  rule_id TEXT,
  evidence_json TEXT NOT NULL DEFAULT '[]',
  occurred_at TEXT NOT NULL,
  recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_asset_entitlements_account ON asset_entitlements(account_id, state);
CREATE INDEX IF NOT EXISTS idx_physical_assets_merchant ON physical_assets(merchant_id, asset_type);
CREATE INDEX IF NOT EXISTS idx_economic_events_account ON economic_events(account_id, occurred_at);
