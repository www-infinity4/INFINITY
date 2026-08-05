# Good Bee · Infinity Living

Good Bee is a development prototype for voluntary accessible travel, trial stays, relocation, support coordination, modular housing, NFC benefit credentials, Store Cards, reciprocal clearing, AI wallet orchestration, and local-first package planning.

## Websites

### Good Bee Living

Open [`index.html`](index.html).

Includes:

- beach, mountain, sailing, vacation, trial-stay, permanent-move, and accessible-home planning;
- transportation, personal-assistance, nursing, meal, check-in, companion, and accessibility choices;
- modular robot-assisted housing concepts;
- Honey Coin NFC access;
- consent, return, complaint, privacy, and audit protections.

### Infinity Store Cards

Open [`store-cards.html`](store-cards.html).

Includes:

- Good Bee Honey Card;
- Infinity Store Card;
- Arrowhead Coin and Luxury Click–Infinity Drop;
- Black Card Market;
- Infinity Relic Cards;
- Infinity Wallet, Market, and Stage;
- Shop World demonstration mechanics;
- NFC/RFID identity, provenance, delivery, returns, and disputes.

### Reciprocal Clearing

Open [`reciprocal-clearing.html`](reciprocal-clearing.html).

Defines how an eligible Store Claim becomes general Infinity units without leaving duplicate spending power:

```text
Verify funding and ownership
→ quote exchange
→ lock Store Claim
→ permanently retire Store Claim
→ issue approved Infinity units
→ link retirement and issuance receipts
```

### Infinity AI Wallet Orchestrator

Open [`wallet-orchestrator.html`](wallet-orchestrator.html).

The wallet coordinates:

- hotel-night claims;
- physical silver and gold access limits;
- physical and digital NFC cards;
- baseline and in-person discounts;
- worldwide product claims;
- vacation-package assembly;
- business-plan digital coins;
- sponsored visits and advertising budgets;
- work, contribution, ownership, rights, and receipts;
- a simple “use, save, earn, exchange, travel, approve, or dispute” layer over the deeper graph.

### Infinity Coin Planner

Open [`coin-planner.html`](coin-planner.html).

Coin Planner:

- discovers businesses from permitted official, licensed, open, merchant-direct, industry, and community sources;
- organizes countries, localities, destinations, currencies, languages, and business categories;
- deduplicates and verifies listings before merchant enrollment;
- sources hotels, meals, rides, attractions, products, and services locally first;
- requests bulk, off-peak, and direct contracts;
- forecasts likely destination demand;
- stages suitable durable products near likely destinations;
- assembles separate Store Claims into one package;
- distinguishes public retail-equivalent benchmark from actual contracted cost;
- combines traveler, sponsor, government/nonprofit, merchant, and Infinity-pool funding;
- blocks publication while any funding gap remains;
- records fulfillment and settlement separately for every provider.

The demonstration tests how a $1,000 retail-equivalent vacation package could cost the traveler 100 Infinity units only when real discounts and disclosed funding cover the actual contract cost.

## Run locally

From the repository root:

```bash
python3 -m http.server 8080
```

Open:

```text
http://localhost:8080/good-bee/
http://localhost:8080/good-bee/store-cards.html
http://localhost:8080/good-bee/reciprocal-clearing.html
http://localhost:8080/good-bee/wallet-orchestrator.html
http://localhost:8080/good-bee/coin-planner.html
```

No package manager, API key, paid AI service, account, or database is required for the static prototypes.

## Files

```text
good-bee/
├── index.html
├── styles.css
├── app.js
├── store-cards.html
├── store-cards.css
├── store-cards.js
├── reciprocal-clearing.html
├── reciprocal-clearing.css
├── reciprocal-clearing.js
├── wallet-orchestrator.html
├── wallet-orchestrator.css
├── wallet-orchestrator.js
├── coin-planner.html
├── coin-planner.css
├── coin-planner.js
├── README.md
└── data/
    ├── programs.json
    ├── store-cards.json
    └── coin-planner.json
```

## Operating rules

1. Participation and destination choice are voluntary.
2. No destination is assigned by gender, disability, diagnosis, or income.
3. A Store Claim and replacement Infinity units cannot remain spendable at the same time.
4. A package cannot publish while its actual contracted cost has an unfunded gap.
5. A public or licensed discovery listing does not enroll a business; merchant authority and payout must be verified.
6. AI can discover, compare, plan, reconcile, and explain but cannot secretly redirect money, force a move, enroll a business, invent funding, or approve its own transaction.
7. Health, identity, ownership, financial, support, travel, and merchant payout information stays outside public GitHub repositories.
8. Every claim, package, discount, transfer, fulfillment, retirement, and correction receives a visible audit event.

## Backend required for real operation

Real operation requires protected services and qualified partners for:

- passkey accounts and recovery;
- consent and support-circle permissions;
- private accessibility and health information;
- merchant/provider verification;
- live inventory and reservations;
- contracts and signatures;
- payments, prepaid value, holds, settlement, refunds, and disputes;
- Store Claim and Infinity-unit ledgers;
- NFC issuance, freeze, and replacement;
- real bids, auctions, ownership, provenance, shipping, and custody;
- destination forecasting and inventory staging;
- hotel, travel, construction, healthcare, metals, tax, government-benefit, and consumer-protection compliance;
- security monitoring, backups, audits, and incident response.

## Launch status

This is software and service-architecture work, not an operating housing provider, travel agency, healthcare provider, bank, insurer, prepaid issuer, currency, metal dealer, marketplace, auction house, lender, licensed contractor, government-benefit administrator, or guaranteed vacation program. All businesses, prices, balances, inventory, discounts, metals, packages, and funding examples are demonstrations only.

See:

- [`../docs/GOOD_BEE_OPERATING_MODEL.md`](../docs/GOOD_BEE_OPERATING_MODEL.md)
- [`../docs/STORE_CARD_OPERATING_MODEL.md`](../docs/STORE_CARD_OPERATING_MODEL.md)
- [`../docs/RECIPROCAL_CLEARING_MODEL.md`](../docs/RECIPROCAL_CLEARING_MODEL.md)
- [`../docs/COIN_PLANNER_MODEL.md`](../docs/COIN_PLANNER_MODEL.md)
