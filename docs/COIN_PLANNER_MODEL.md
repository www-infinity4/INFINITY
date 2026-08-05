# Infinity Coin Planner Operating Model

## Mission

Coin Planner discovers businesses, verifies their real capacity, negotiates local and bulk offers, predicts destination demand, stages appropriate inventory, and assembles typed Store Claims into affordable vacation, housing, health, work, and product packages.

The intended outcome may be described as:

> Build a package with a $1,000 public retail-equivalent while charging the traveler 100 Infinity Units.

That is a target, not an automatic promise. It is valid only when the actual contracted cost and every funding source are documented.

```text
Public retail-equivalent benchmark
        ≠
Actual contracted package cost
        ≠
User contribution
```

The complete funding equation is:

```text
Actual contracted cost
=
User Infinity-unit settlement
+ sponsor or advertiser funding
+ government/nonprofit/benefit funding
+ merchant promotion
+ donations or grants
+ Infinity community/profit-pool funding
+ other disclosed funding
```

A package cannot become available while this equation has an unfunded gap.

## Global business coverage

No single source contains every active business in every country. Coin Planner combines multiple permitted sources and stores provenance for each field.

### Discovery sources

- official national and regional business registers;
- official tourism and destination directories;
- licensed place and business APIs;
- OpenStreetMap and other permitted open geographic data;
- hotel, transport, event, wholesale, shipping, and travel feeds;
- chambers, professional directories, and industry organizations;
- merchant-direct applications and signed data feeds;
- verified community and field contributions.

Useful standards and technical sources include:

- ISO 3166 country and subdivision codes: https://www.iso.org/iso-3166-country-codes.html
- Schema.org `LocalBusiness`, `Offer`, `Service`, `Product`, and `OfferCatalog`: https://schema.org/LocalBusiness
- OpenStreetMap Overpass API: https://wiki.openstreetmap.org/wiki/Overpass_API
- Google Places API: https://developers.google.com/maps/documentation/places/web-service/overview

The system must comply with every source's license, attribution, storage, caching, display, and downstream-use terms.

## Business record

Each business receives a canonical Infinity Business ID and may contain:

- legal and public names;
- registration identifiers;
- country and subdivision codes;
- address and service area;
- geographic coordinates;
- languages and currencies;
- categories;
- contact channels;
- website and storefront;
- hours and seasonality;
- accessibility details;
- licenses and insurance where applicable;
- ownership-control verification;
- payout-destination verification;
- products, services, and capacity;
- public prices;
- direct contract prices;
- volume and date rules;
- taxes and fees;
- cancellation and refund terms;
- shipping, pickup, or service radius;
- Store Card and Infinity acceptance;
- complaints, corrections, and fulfillment history;
- source and retrieval history;
- allowed data use and expiration.

## Discovery is not enrollment

Finding a business in a public or licensed data source does not enroll it in Infinity.

Before a business can receive payment or issue a Store Claim, Coin Planner must verify that an authorized representative controls:

- the business identity;
- the offer;
- the live capacity;
- the payout account;
- relevant licenses or authority;
- fulfillment and refund obligations.

## Pipeline

### 1. Discover

Search permitted sources for businesses, products, services, and destinations.

### 2. Normalize

Convert records into shared country, currency, language, address, category, product, service, and offer schemas.

### 3. Deduplicate

Resolve:

- alternate names;
- chains and branches;
- copied listings;
- moved or closed businesses;
- franchise relationships;
- multiple source identifiers;
- duplicate payout applications.

### 4. Verify

Confirm identity, authority, licenses, insurance, capacity, accessibility, pricing, contract, payout, and performance evidence.

### 5. Source locally first

For a destination package, search the destination and surrounding service area before importing products or providers.

Local-first sourcing can reduce:

- shipping;
- storage;
- transport;
- breakage;
- spoilage;
- customs complexity;
- environmental cost;
- money leaving the destination community.

It does not mean choosing a local provider when quality, safety, accessibility, price, or capacity is inadequate.

### 6. Negotiate bulk capacity

The planner may request bids or direct offers for:

- room blocks;
- extended stays;
- off-peak nights;
- meals and grocery packages;
- accessible rides;
- attractions and experiences;
- support hours;
- equipment rentals;
- durable products;
- moving and housing services.

Every bulk offer states:

- exact dates or inventory;
- minimum and maximum volume;
- price and currency;
- taxes and fees;
- included and excluded items;
- accessibility;
- cancellation and attrition rules;
- substitutions;
- refund rights;
- settlement timing;
- expiration;
- responsible party.

### 7. Forecast demand

Coin Planner estimates likely use by destination, date, trip length, package type, accessibility requirement, product type, and cancellation probability.

Personal identities and sensitive health data are not exposed to merchants merely for forecasting.

### 8. Stage inventory

Coin Planner can reserve service capacity and move suitable durable products near likely destinations.

Good staging candidates may include:

- accessible equipment;
- luggage and shipping supplies;
- mobility accessories;
- basic clothing or weather gear;
- repair parts;
- reusable recreation equipment;
- package materials.

Items that should generally remain close to actual use or personal approval include:

- food and perishables;
- medicine;
- fitted medical equipment;
- sensitive personal goods;
- high-value items without confirmed custody;
- products subject to customs or local restrictions.

Every staging plan includes reverse logistics for unused goods, returns, repairs, resale, donation, redistribution, recycling, and warranty claims.

### 9. Assemble package

The planner combines separate typed claims into one user-facing package.

Example:

```text
7 hotel-night claims
+ 14 meal claims
+ 4 accessible-ride claims
+ 2 experience claims
+ 1 accessibility-coordination claim
+ destination product claims
+ NFC and in-person discounts
=
One seven-day vacation package
```

The claims remain separate underneath so each provider, restriction, expiration, receipt, refund, and failure can be handled correctly.

### 10. Close funding gap

The package is `PLANNING_ONLY` until verified funding is greater than or equal to contracted cost.

Funding sources are not interchangeable. Each keeps its own restrictions and accounting.

### 11. Fulfill and settle

The wallet reserves the claims. Providers verify fulfillment through appropriate evidence such as:

- NFC;
- QR;
- passkey;
- signed staff confirmation;
- check-in record;
- delivery receipt;
- customer acceptance;
- inspected completion.

Settlement follows the signed offer rather than a scraped public price.

### 12. Learn and recirculate

Coin Planner measures:

- actual use;
- cancellations;
- substitutions;
- refunds;
- satisfaction;
- accessibility outcomes;
- local spending share;
- provider performance;
- fraud;
- unused inventory;
- package cost and funding accuracy.

The next plan uses the evidence without silently changing past records.

## Retail-equivalent benchmark

A large retail comparison can be misleading unless documented.

Every benchmark includes:

- date collected;
- comparable provider or public offer;
- same destination and date range where possible;
- same room or product class;
- included taxes and fees;
- included meals, rides, products, and experiences;
- cancellation terms;
- availability status;
- source rights and evidence.

The page should use language such as **published retail-equivalent benchmark**, not claim that a person definitely would have paid that amount.

## $1,000 benchmark / 100-unit example

An illustrative package might have:

| Component | Retail benchmark | Contract cost |
|---|---:|---:|
| Seven hotel nights | $560 | $210 |
| Fourteen meals | $210 | $95 |
| Four rides | $120 | $55 |
| Two experiences | $110 | $40 |
| **Total** | **$1,000** | **$400** |

Possible disclosed funding:

| Funding source | Amount |
|---|---:|
| Traveler: 100 Infinity Units at $1 settlement value | $100 |
| Sponsor or advertiser | $100 |
| Government/nonprofit/benefit program | $100 |
| Infinity community/profit pool | $100 |
| **Total funding** | **$400** |

The traveler pays 100 units only because the negotiated cost and other funding sources cover the entire $400. The retail comparison does not fund anything.

## Local business fairness

Coin Planner must not create cheap packages by forcing losses onto small businesses or workers.

Controls include:

- merchants set or approve prices;
- workers' compensation is visible in the cost model;
- no hidden service requirements;
- no retroactive price reduction;
- prompt settlement terms;
- cancellation compensation where contracted;
- complaint and appeal paths;
- anti-retaliation rules;
- local economic-share reporting;
- no ranking penalty for rejecting an unsustainable offer.

## AI responsibilities

AI may:

- discover and normalize listings;
- match duplicate records;
- identify likely closed or moved businesses;
- compare prices and terms;
- request bulk bids;
- forecast demand;
- optimize packages;
- identify funding gaps;
- detect fake retail benchmarks;
- detect payout changes;
- flag inaccessible or contradictory listings;
- suggest substitutions;
- reconcile fulfillment and settlement;
- explain every recommendation.

AI may not independently:

- enroll a business based only on scraped data;
- sign a merchant contract;
- change payout details;
- promise a package with an unfunded gap;
- fabricate a retail benchmark;
- pressure a business below sustainable cost;
- hide a subsidy;
- expose personal travel or health data;
- settle its own related business;
- erase complaints or prior prices.

## Data and API design

### Core entities

- `Country`
- `Subdivision`
- `Locality`
- `Destination`
- `Business`
- `BusinessLocation`
- `MerchantAccount`
- `Product`
- `Service`
- `CapacityWindow`
- `Offer`
- `BulkContract`
- `StoreClaim`
- `Package`
- `FundingSource`
- `InventoryPosition`
- `Shipment`
- `Reservation`
- `FulfillmentEvent`
- `SettlementEvent`
- `CorrectionEvent`

### Package states

```text
DRAFT
→ SOURCING
→ QUOTED
→ CONTRACTED
→ FUNDING_PENDING
→ FULLY_FUNDED
→ PUBLISHED
→ RESERVED
→ IN_PROGRESS
→ FULFILLED

Alternative endings:
CANCELLED
EXPIRED
PARTIALLY_FULFILLED
REFUNDED
DISPUTED
FAILED
```

## Rollout

A realistic rollout does not begin with every business in every country.

### Phase 1

- one destination;
- several verified local hotels, restaurants, rides, and attractions;
- one package type;
- manual contract review;
- transparent optimizer.

### Phase 2

- several destinations;
- merchant self-enrollment;
- licensed discovery data;
- bulk bid requests;
- Store Card and NFC fulfillment.

### Phase 3

- country and region ingestion;
- destination forecasting;
- product staging;
- local contributor verification;
- automated reconciliation with human approvals.

### Phase 4

- multi-country packages;
- currency, tax, customs, language, and consumer-protection adapters;
- licensed travel and payment partners;
- independent audits.

### Phase 5

- broad global registry coverage;
- continuously scored data freshness;
- provider competition and cooperative purchasing;
- community and public-benefit package funding.

## Definition of success

For every package, a traveler and auditor can answer:

- Which businesses are included?
- How were they discovered and verified?
- Which businesses are local to the destination?
- What is the exact contracted cost?
- What does the retail-equivalent benchmark include?
- Who funds each part of the package?
- Is there any unfunded gap?
- What does the traveler pay?
- What does each provider receive?
- What claims are issued?
- What happens if a provider fails?
- How are refunds, substitutions, and returns handled?
- What inventory was moved and what happens if unused?
- How much spending remains in the local community?

The Coin Planner succeeds when a low user price is produced by transparent coordination and real funding—not by hiding cost or inventing value.
