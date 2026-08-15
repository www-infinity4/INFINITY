# Infinity AI Token Studio Operating Model

## Purpose

The Infinity AI Token Studio turns an existing project, idea, business, product, service, component, station, work role, offer, chart, or system module into a structured token plan without collapsing every type of value into one coin.

The Studio provides:

- one universal conversion mark;
- a transparent product-need ranking;
- named and attributable creation versions;
- Product Token supply planning;
- Avatar Coin identity requirements;
- capacity-verification gates;
- connections to Store Cards, Coin Planner, AI Wallet, fulfillment, Reciprocal Clearing, and contribution records;
- charts and append-only local prototype events.

## Universal Star mark

The symbol is:

```text
⭐
```

It functions like a quiet creation trademark across the Infinity interface.

### Presentation standard

- exactly 15 × 15 pixels in the current website standard;
- upper-right corner of every convertible object;
- identical position, spacing, hover, focus, and accessibility label;
- partial opacity until the object is hovered, focused, or actively selected;
- no large floating duplicates when the small mark is sufficient.

### Meaning

Clicking the mark means:

- create;
- edit;
- version;
- convert;
- connect;
- inspect ancestry;
- inspect token and product requirements.

It does **not** mean:

- favorite;
- rating;
- endorsement;
- verified business;
- funded product;
- guaranteed value;
- ownership title.

## Token types

### 1. Star Blueprint

A Star Blueprint is the editable creation record.

It contains:

- creation or business name;
- selected source object;
- creator and contributors;
- parent version;
- version number;
- exact product definition;
- system need;
- planned units or identities;
- factor scores;
- Product Token supply;
- Avatar Coin requirement;
- status;
- timestamp;
- linked systems and evidence.

A change creates a child version. It does not silently overwrite its parent.

### 2. Product Token

A Product Token defines what the system actually needs produced.

It may represent:

- one hotel night;
- one accessible ride;
- a radio-station system;
- a housing component;
- a complete destination package;
- a Store Card offer;
- a business product;
- a work deliverable;
- a support hour;
- a creator or research product.

A Product Token is not automatically spendable. Before it can become a Store Claim, the responsible system verifies capacity, provider authority, funding, dates, restrictions, quality tests, fulfillment, refunds, rights, and disputes.

### 3. Avatar Coin

An Avatar Coin is an identity-activation record for a distinct operating identity.

Examples may include:

- a radio station;
- a verified business identity;
- a creator world;
- a qualified service identity;
- another operating entity that must remain distinct from its Product Tokens and Store Claims.

The current Alien Radio prototype uses this rule:

```text
Another verified user actively uses the creator's station design
for 24 continuous qualified hours
        ↓
One Avatar Coin is produced
        ↓
One Avatar Coin is locked to one active radio-station identity
```

Creator self-use, bots, hidden tabs, stopped playback, disconnected use, and unlabeled demonstration time do not qualify.

A demonstration control can advance test time, but demonstration Avatar Coins are marked nonproduction and cannot activate a production station.

### 4. Store Claim

A Store Claim is the specific funded promise that can be used or fulfilled.

It connects the Product Token to:

- verified provider;
- inventory or capacity;
- price or benefit units;
- funding source;
- holder;
- restrictions;
- dates and expiration;
- delivery or performance;
- receipt;
- return and dispute rights.

### 5. Infinity Unit

An Infinity Unit is the general settlement and transfer layer handled by Reciprocal Clearing and the treasury rules.

The Token Studio does not issue Infinity Units.

When conversion is permitted:

```text
Store Claim verified
→ conversion quoted
→ Store Claim locked
→ Store Claim retired
→ approved Infinity Units issued
```

## Product Need Engine

The current transparent weighted score is:

```text
Need Score
=
System Demand × 35%
+ Scarcity × 25%
+ Human Usefulness × 20%
+ Production Readiness × 10%
+ Local Capacity × 10%
```

Each factor is scored from 0 through 100.

### Priority bands

| Score | Planning band |
|---:|---|
| 80–100 | Critical product priority |
| 60–79.9 | High product priority |
| 40–59.9 | Build and verify |
| 0–39.9 | Research before production |

The score is a planning tool, not an investment rating or guarantee of demand.

The weakest factor becomes the next work recommendation. For example, a highly useful housing component with weak local capacity should trigger supplier, tooling, inspection, or partner work rather than unsupported issuance.

## Product Token supply

The current planning formula is:

```text
Minimum Product Token Supply
=
Planned operating units
+ max(1, ceiling(Planned operating units × 20%))
```

The added amount is a version, replacement, testing, or contingency reserve. It is not general money supply.

For identity products:

```text
Avatar Coins required
=
Planned active identities × 1
```

Product supply and Avatar supply remain separate.

## Alien Radio wiring

Alien Radio is the first connected working example.

Existing working systems include:

- 12 live radio channels;
- Web Audio synthesizer fallback;
- spectrum visualization;
- station controls;
- user accounts and local prototype wallets;
- listening records;
- research generation;
- Signal Catch game;
- GP Suite AI modules.

The `agent/star-avatar-token-stage` branch adds:

- `stage.html` enhanced route;
- `star-stage.js` creation, charts, versions, usage, and station ledger;
- `star-stage.css` universal small Star marks and Stage interface;
- `token-manifest.json` machine-readable token rules;
- universal marks on Alien Radio, the active station, channels, AI modules, wallet, research, station identities, and blueprints;
- Product Need calculation;
- named Star Blueprint versions;
- Product Token supply calculation;
- 24-hour qualified-use tracking;
- Avatar Coin production and station locking;
- append-only local events.

## Connected Infinity systems

### Coin Planner

Finds and verifies businesses, capacity, prices, local sourcing, bulk contracts, funding, and packages.

### Store Cards

Turns a verified Product Token and provider offer into a specific physical or digital Store Claim with NFC, fulfillment, receipts, returns, ownership, and provenance where appropriate.

### Infinity AI Wallet

Organizes Star Blueprints, Product Tokens, Avatar Coins, Store Claims, Infinity Units, rights, work, receipts, packages, and approvals without representing them as the same balance.

### Reciprocal Clearing

Retires eligible Store Claims before issuing replacement Infinity Units.

### Contribution records

Identify human work, AI assistance, sources, accepted deliverables, rights, review status, and compensation.

## State model

```text
Idea or working system
→ STAR_DRAFT
→ STAR_VERSIONED
→ PRODUCT_DEFINED
→ CAPACITY_REVIEW
→ PRODUCT_VERIFIED
→ STORE_CLAIM_ELIGIBLE
→ OFFER_PUBLISHED
→ RESERVED
→ FULFILLED

Identity product branch:
QUALIFIED_USE_RUNNING
→ AVATAR_PRODUCED
→ AVATAR_LOCKED
→ IDENTITY_ACTIVE
```

Alternative states include:

- rejected;
- needs evidence;
- cancelled;
- expired;
- disputed;
- superseded by a child version;
- demonstration only.

## Production backend requirements

The current sites use local browser records for demonstration.

A real implementation requires protected services for:

- passkey-first accounts;
- verified creators and organizations;
- contribution and rights agreements;
- signed Star manifests;
- version and ancestry storage;
- provider and capacity verification;
- bot-resistant qualified-use evidence;
- privacy-preserving activity measurement;
- Avatar Coin issuance and locking;
- merchant contracts;
- payments and tax records where applicable;
- Store Claims and fulfillment;
- disputes, reversals, and corrections;
- append-only audit events;
- independent security, accessibility, financial, and legal review.

## AI authority limits

AI may:

- identify missing products;
- compare system demand and capacity;
- calculate transparent scores;
- suggest Product Token definitions;
- calculate planning supply;
- identify weak factors;
- connect related modules;
- detect duplicate or contradictory versions;
- prepare evidence and verification tasks;
- explain every recommendation.

AI may not independently:

- declare its own output verified;
- create general Infinity Units;
- fabricate use or capacity;
- count bots or creator self-use as qualified use;
- activate a production identity with a demonstration Avatar Coin;
- transfer money or rights;
- overwrite ancestry;
- hide a parent version;
- enroll a merchant;
- approve its own related business;
- promise investment return.

## Definition of success

For any small Star mark, the person can answer:

- What object did I select?
- What does conversion mean for this type?
- What exact product does the system need?
- Why is it needed?
- How was its priority calculated?
- What is missing before production?
- How many Product Tokens are needed?
- Does it require an Avatar Coin?
- What use produces that Avatar Coin?
- What version is this and what is its parent?
- Which systems consume the output?
- When can it become a Store Claim?
- Which actions still require my approval?

The Star system succeeds when one quiet symbol opens a complete, understandable, reversible creation path without cluttering the interface or pretending every record is money.
