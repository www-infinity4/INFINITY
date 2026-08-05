# Infinity Root Portal

The `INFINITY` repository is the main entry point for the `www-infinity4` project network.

## Purpose

This root does not copy every repository into one oversized codebase. It provides a live directory, shared architecture, standards, and integration contracts while every project keeps its own source history and deployment.

## Current build

- Responsive blue-purple root website
- Live GitHub repository discovery
- Search and automatic project grouping
- Direct links to every repository
- Architecture and AI-gateway documentation
- No API secrets stored in browser code
- **Infinity Economy System Map** connecting every website, ledger, value type, input, output, and protection rule
- **Good Bee · Infinity Living** for voluntary accessible travel, relocation, housing, support, and NFC benefit packages
- **Infinity Store Cards** for cards, stores, benefits, drops, physical collectibles, provenance, and fulfillment
- **Infinity Reciprocal Clearing Loop** for retiring Store Claims before issuing general Infinity units
- **Infinity AI Wallet Orchestrator** for hotel nights, physical-metal access, NFC discounts, product claims, business coins, ads, work, and simple user decisions
- **Infinity Coin Planner** for global business discovery, local-first sourcing, bulk contracts, destination staging, transparent package funding, and fulfillment

## Master system map

Open [`good-bee/infinity-system.html`](good-bee/infinity-system.html) for the complete connected system.

It includes:

- a searchable directory of every module;
- each module’s inputs, outputs, purpose, and public website;
- separate value types for program funding, Store Claims, Infinity units, metal access, ownership, contributions, and sponsored engagement;
- the complete funding → sourcing → Store Card → wallet → approval → fulfillment/clearing → settlement → recirculation flow;
- the $1,000 retail-equivalent / 100-unit package explanation;
- the core anti-double-spend, full-funding, merchant-verification, privacy, capacity, and AI-governance rules.

See [`docs/INFINITY_SYSTEM_WEBSITE_MAP.md`](docs/INFINITY_SYSTEM_WEBSITE_MAP.md) for the permanent file and architecture map.

## Good Bee

Open [`good-bee/`](good-bee/) for housing, travel, accessibility, support, Honey Coin, and modular-home planning.

## Infinity Store Cards

Open [`good-bee/store-cards.html`](good-bee/store-cards.html) for:

- Good Bee Honey Card;
- Infinity Store Card;
- Arrowhead Coin and Luxury Click–Infinity Drop;
- Black Card Market records;
- Infinity Relic Cards;
- Infinity Wallet, Market, and Stage;
- Shop World demonstration mechanics;
- NFC/RFID identity, provenance, transfer, delivery, returns, and disputes;
- Boron Vault viewing/signing separation.

## Reciprocal Clearing

Open [`good-bee/reciprocal-clearing.html`](good-bee/reciprocal-clearing.html) for the anti-double-spend conversion system:

```text
Verify funded Store Claim
→ quote conversion
→ lock the source claim
→ permanently retire its spending power
→ issue approved Infinity units
→ preserve linked retirement and issuance receipts
```

## Infinity AI Wallet

Open [`good-bee/wallet-orchestrator.html`](good-bee/wallet-orchestrator.html) for the simplified user interface over the deeper graph of:

- general Infinity units;
- hotel-night claims;
- meals, rides, products, and vacation packages;
- limited physical silver and gold access;
- physical and digital NFC Store Cards;
- baseline and in-person discounts;
- business-plan coins;
- sponsored visits and advertising budgets;
- work and contribution records;
- rights, receipts, and approvals.

## Infinity Coin Planner

Open [`good-bee/coin-planner.html`](good-bee/coin-planner.html) for the global-local package engine.

Coin Planner:

- builds country, locality, destination, and business records from permitted official, licensed, open, merchant-direct, industry, and community sources;
- normalizes and deduplicates listings;
- verifies merchant control, payout, capacity, accessibility, contracts, and licenses;
- sources hotels, meals, transportation, products, activities, and support locally before importing;
- requests bulk and off-peak contracts;
- forecasts likely destination demand;
- stages appropriate durable inventory;
- combines separate Store Claims into one understandable package;
- separates public retail-equivalent benchmark from actual contracted cost;
- shows traveler, sponsor, program, and Infinity-pool funding separately;
- blocks package publication while an unfunded gap remains;
- settles each provider only after verified fulfillment.

The included demonstration shows how a $1,000 retail-equivalent benchmark could be offered for 100 Infinity units only when real contracts and disclosed funding cover the actual package cost. It is not a guaranteed price or active offer.

## Documentation

- [`docs/INFINITY_SYSTEM_WEBSITE_MAP.md`](docs/INFINITY_SYSTEM_WEBSITE_MAP.md)
- [`docs/GOOD_BEE_OPERATING_MODEL.md`](docs/GOOD_BEE_OPERATING_MODEL.md)
- [`docs/STORE_CARD_OPERATING_MODEL.md`](docs/STORE_CARD_OPERATING_MODEL.md)
- [`docs/RECIPROCAL_CLEARING_MODEL.md`](docs/RECIPROCAL_CLEARING_MODEL.md)
- [`docs/COIN_PLANNER_MODEL.md`](docs/COIN_PLANNER_MODEL.md)
- [`docs/SECURITY_AND_DATA_ARCHITECTURE.md`](docs/SECURITY_AND_DATA_ARCHITECTURE.md)
- [`docs/INTEGRATION_PLAN.md`](docs/INTEGRATION_PLAN.md)

## Run locally

```bash
python3 -m http.server 8080
```

Open:

```text
http://localhost:8080/
http://localhost:8080/good-bee/infinity-system.html
http://localhost:8080/good-bee/
http://localhost:8080/good-bee/store-cards.html
http://localhost:8080/good-bee/reciprocal-clearing.html
http://localhost:8080/good-bee/wallet-orchestrator.html
http://localhost:8080/good-bee/coin-planner.html
```

## Prototype boundary

The repository does not currently operate housing, healthcare, travel, payments, prepaid accounts, currency, metal sales, auctions, lending, government benefits, merchant settlement, or guaranteed packages. All displayed balances, prices, discounts, inventory, funding, cards, units, metals, businesses, and packages are demonstrations until verified contracts and qualified operational systems exist.

## Integration order

1. Inventory and classify repositories.
2. Establish this repository as the public root.
3. Add a machine-readable project registry and health checks.
4. Select canonical repositories where duplicates overlap.
5. Create shared UI, schema, authentication, and API packages.
6. Connect projects through documented URLs and APIs.
7. Add server-side AI routing with budget and rate limits.
8. Migrate projects in small tested batches rather than a destructive mass merge.

See [`docs/INTEGRATION_PLAN.md`](docs/INTEGRATION_PLAN.md) for the detailed plan.
