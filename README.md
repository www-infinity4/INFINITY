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

## Featured module: Good Bee

Open [`good-bee/`](good-bee/) for the first Good Bee website.

It includes:

- beach, mountain, sailing, vacation, trial-stay, permanent-move, and new-home planning;
- accessibility, transportation, companion, personal-assistance, meal, check-in, and nursing-coordination choices;
- four modular accessible housing models for the future Infinity robotic building network;
- a Good Bee Honey Coin NFC access-key model;
- goods-and-services benefit units rather than an unverified investment token;
- person-controlled consent, return, privacy, payment, complaint, and audit protections;
- no paid AI requirement for the current static prototype.

The prototype does not currently provide housing, healthcare, travel, nursing, money, benefits, or construction. All displayed packages, balances, destinations, and availability are planning examples.

See:

- [`good-bee/README.md`](good-bee/README.md)
- [`docs/GOOD_BEE_OPERATING_MODEL.md`](docs/GOOD_BEE_OPERATING_MODEL.md)

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

## Deployment

The static portal can use GitHub Pages or Cloudflare Pages. AI calls must be handled by a server-side worker or function so provider keys remain private.

Good Bee can remain mostly frontend for public catalogs, package demonstrations, housing designs, and explanations. Real identities, health/accessibility details, itineraries, provider records, payments, benefit balances, complaints, and construction records require protected backend services and qualified operational partners.

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
