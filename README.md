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
- **Good Bee · Infinity Living** public prototype for voluntary accessible travel, relocation, housing, support, and NFC benefit packages
- **Infinity Store Cards** public prototype connecting cards, stores, benefits, drops, auctions, physical collectibles, provenance, and scam-resistant fulfillment

## Featured module: Good Bee

Open [`good-bee/`](good-bee/) for the Good Bee website.

It includes:

- beach, mountain, sailing, vacation, trial-stay, permanent-move, and new-home planning;
- accessibility, transportation, companion, personal-assistance, meal, check-in, and nursing-coordination choices;
- four modular accessible housing models for the future Infinity robotic building network;
- a Good Bee Honey Coin NFC access-key model;
- goods-and-services benefit units rather than an unverified investment token;
- person-controlled consent, return, privacy, payment, complaint, and audit protections;
- no paid AI requirement for the current static prototype.

The prototype does not currently provide housing, healthcare, travel, nursing, money, benefits, or construction. All displayed packages, balances, destinations, and availability are planning examples.

## Featured module: Infinity Store Cards

Open [`good-bee/store-cards.html`](good-bee/store-cards.html) for the recovered and consolidated store-card system.

The website incorporates the earlier conversations around:

- Good Bee Honey Card and Honey Coin;
- Infinity Store Card;
- Arrowhead Coin and Luxury Click–Infinity Drop;
- Black Card Market property and collateral records;
- Infinity Relic Cards containing real coins, sapphires, minerals, memorabilia, or specimens;
- Infinity Wallet, Infinity Market, and Infinity Stage storefronts;
- Shop World / Mario Shop World grab, accept, reject, charge, bid, and demo-token mechanics;
- NFC/RFID authentication, provenance, transfer, fulfillment, receipts, returns, and disputes;
- Boron Vault separation of viewing from real signing authority;
- AI monitoring for payout changes, fake inventory, duplicate listings, bid manipulation, and failed fulfillment.

The Store Cards prototype is static HTML, CSS, JavaScript, and JSON. Its demo tokens, balances, auctions, collateral, store value, cards, and offers are not real financial products or guaranteed inventory.

See:

- [`good-bee/README.md`](good-bee/README.md)
- [`docs/GOOD_BEE_OPERATING_MODEL.md`](docs/GOOD_BEE_OPERATING_MODEL.md)
- [`docs/STORE_CARD_OPERATING_MODEL.md`](docs/STORE_CARD_OPERATING_MODEL.md)

## Run locally

```bash
python3 -m http.server 8080
```

Open the root portal:

```text
http://localhost:8080/
```

Open Good Bee:

```text
http://localhost:8080/good-bee/
```

Open Store Cards:

```text
http://localhost:8080/good-bee/store-cards.html
```

## Deployment

The static portal can use GitHub Pages or Cloudflare Pages. AI calls must be handled by a server-side worker or function so provider keys remain private.

Good Bee and Store Cards can remain mostly frontend for public catalogs, package demonstrations, card visualizations, public provenance, housing designs, search, Shop World demonstrations, and explanations. Real identities, health/accessibility details, ownership, itineraries, provider records, payments, bids, collateral, balances, complaints, signing, and construction records require protected backend services and qualified operational partners.

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
