# Infinity Reciprocal Clearing Model

## Core idea

Infinity uses two different forms of value:

1. **Store Claims** — specific promises for products, services, destinations, support, inventory, or merchant value.
2. **Infinity Units** — general internal transfer units used across approved Infinity businesses and services.

A Store Claim can become Infinity Units only through a verified clearing transaction. The Store Claim is locked and permanently retired before replacement units are issued.

```text
Verified Store Claim
        ↓
Eligibility and funding checks
        ↓
Lock the exact source claim
        ↓
Create retirement receipt
        ↓
Issue approved Infinity Units
        ↓
Units circulate through people, businesses, goods, and services
```

This prevents the original card and the replacement units from remaining spendable at the same time.

## Institutional funding flow

A government agency, nonprofit, employer, insurer, grantmaker, customer, or other approved institution may contract with:

- Infinity Health;
- New Hope;
- Good Bee;
- an Infinity business;
- an approved outside provider.

The contract purchases defined capacity rather than vague tokens.

Examples:

- accessible lodging nights;
- destination packages;
- meals or grocery allocations;
- transportation;
- nursing or support hours;
- health navigation;
- home setup;
- construction components;
- tools and materials;
- food seed;
- training;
- verified work output.

Received funding enters the Program Funding Ledger. The corresponding product or service capacity enters the Store Claim Ledger.

## Program allocation

New Hope, Infinity Health, or another program may use AI to organize allocations according to the governing contract and published eligibility rules.

AI may:

- compare needs and available packages;
- calculate a proposed pay or benefit package;
- preserve a shared pool for other participants;
- prevent over-allocation;
- identify expiring capacity;
- match accessible destinations and providers;
- identify missing documents;
- explain the allocation;
- prepare an appeal packet.

AI may not:

- invent funding;
- secretly change eligibility;
- force a person to accept a Store Claim;
- force a conversion to Infinity Units;
- divert restricted public benefits;
- discriminate unlawfully;
- deny an appeal to protect its own decision;
- pay itself;
- erase the allocation history.

## Holder choices

The holder of a Store Claim may, subject to program and legal restrictions:

- use the specific product or service;
- reserve it for later;
- decline it;
- request a different eligible option;
- transfer it where transfer is allowed;
- request conversion into Infinity Units;
- dispute the quantity, quality, provider, expiration, or restrictions.

Government-funded and legally restricted claims remain subject to the program that funded them. Technical convertibility does not override legal restrictions.

## Clearing steps

### 1. Receive exchange request

The wallet submits the claim ID, requested quantity, destination wallet, and user approval.

### 2. Verify source

The clearing engine verifies:

- claim exists;
- claim belongs to the requesting person or authorized account;
- funding was actually received;
- claim has not been spent, transferred, expired, refunded, disputed, or retired;
- issuing program permits conversion;
- government or donor restrictions permit conversion;
- provider and inventory status;
- exchange-rate version;
- fees, taxes, reserves, and disclosures;
- identity and fraud controls appropriate to the transaction.

### 3. Quote before acceptance

The wallet displays:

- source claim quantity;
- exchange rate;
- exact Infinity Units to be issued;
- reserve allocation;
- community-pool allocation;
- operations and tax allocation;
- timing;
- expiration of the quote;
- effect of retirement;
- dispute and reversal procedure.

### 4. Lock the Store Claim

The claim enters `CLEARING_LOCKED`. It cannot be used or submitted to another exchange while clearing proceeds.

### 5. Retire the Store Claim

After final validation, the claim enters `RETIRED_CONVERTED`. The ledger records:

- claim ID;
- prior owner;
- quantity;
- funding source;
- contract and program;
- conversion quote;
- approval;
- timestamp;
- clearing event ID;
- retirement reason;
- replacement issuance ID.

The retired record is preserved as evidence but has no remaining spending power.

### 6. Issue Infinity Units

The settlement ledger issues the approved amount to the destination wallet. The issuance references exactly one retirement event.

### 7. Reconcile

The system verifies:

```text
Retired claim value
= gross replacement basis
= wallet issuance
+ settlement reserve
+ community allocation
+ operations/tax allocation
+ documented rounding
```

Any mismatch blocks final settlement.

## Reversals

A retirement cannot simply be deleted.

A valid reversal must:

1. freeze unspent replacement Infinity Units;
2. recover or account for any spent units according to published rules;
3. append a reversal event;
4. cancel the original replacement issuance;
5. reactivate or replace the Store Claim only when the funding contract permits it;
6. preserve the complete prior history.

## Four-ledger architecture

### A. Program Funding Ledger

Tracks actual external resources:

- pledged;
- awarded;
- received;
- restricted;
- committed;
- spent;
- refunded;
- disputed;
- remaining.

### B. Store Claim Ledger

Tracks specific economic promises:

- created;
- verified;
- pooled;
- allocated;
- reserved;
- fulfilled;
- transferred;
- clearing locked;
- converted;
- expired;
- cancelled;
- retired.

### C. Infinity Unit Ledger

Tracks general internal transfer units:

- issued;
- available;
- held;
- transferred;
- earned;
- spent;
- taxed;
- disputed;
- recovered;
- retired.

### D. Treasury and Profit Pool Ledger

Tracks network-wide resources:

- settlement reserve;
- operating revenue;
- operating expense;
- community pool;
- basic participation pool;
- business seed pool;
- construction pool;
- loss and fraud reserve;
- verified profit;
- contributor distribution;
- public-benefit distribution;
- retained capital.

These four ledgers must reconcile but must never be collapsed into one balance.

## Infinity buyback

Infinity may offer to purchase eligible Infinity Units or settlement claims under a published treasury policy.

A buyback quote must disclose:

- eligible unit type;
- source and restrictions;
- quantity;
- rate;
- fees and tax treatment;
- funding source;
- settlement timing;
- whether purchased units are retired, held in treasury, or reallocated;
- maximum program volume;
- dispute process.

A buyback is not a guaranteed investment return. Infinity must not promise that units always rise in value or will always be purchased.

## Recirculation

Purchased or received units can be handled according to a public rule:

- retire units to reduce circulating supply;
- hold units in the settlement reserve;
- allocate units to verified public benefits;
- seed a new business;
- purchase real inventory;
- compensate verified contributors;
- support New Hope or Infinity Health;
- fund construction, food production, tools, education, or transportation;
- distribute audited profit according to the governance formula.

No single AI, administrator, or founder should be able to change the disposition privately.

## Capacity-backed products and services

The earlier Infinity rule remains central: claims are issued only against verified capacity.

Examples:

- a barber’s appointment capacity;
- a grower’s available eggs, produce, seed, or meat;
- a builder’s inspected housing capacity;
- a caregiver’s available hours;
- a writer’s accepted deliverable;
- a reviewer’s verified movie-detail record;
- a developer’s completed software task;
- a transportation provider’s accessible rides;
- a hotel’s contracted nights.

Capacity verification may include inventory, schedule, equipment, licenses, inspection, quality, delivery history, refund ability, and customer complaints.

## Basic participation allowance

The intended safety mechanism authorizes **up to 100 Infinity Units per day** for a person who currently has no verified product or service, subject to available designated funding.

Appropriate uses may include:

- food;
- food seed;
- tools;
- materials;
- transportation;
- communication;
- hygiene;
- training;
- software access;
- basic business formation;
- first-customer support.

The allowance is:

- a ceiling, not forced spending;
- funded from a defined pool;
- not unsupported token creation;
- not high-interest debt;
- not automatically reduced because the person begins earning;
- accompanied by a work and business opportunity engine;
- subject to accessible appeal and correction.

## AI livelihood engine

The system looks for productive roles based on interests, abilities, experience, accessibility, available equipment, schedule, and community need.

Example: a person who watches many movies may perform paid work such as:

- structured movie summaries;
- cast and release verification;
- edition comparisons;
- accessibility notes;
- content warnings;
- subtitle or transcript review;
- continuity and error logging;
- genre and theme indexing;
- collection curation;
- metadata correction;
- recommendation explanations.

Other Infinity work may include:

- planning and developing the Infinity system with AI;
- research;
- documentation;
- software testing;
- card and collectible cataloging;
- local service verification;
- provider accessibility audits;
- product photography;
- data correction;
- customer support;
- design;
- food production;
- repair;
- construction;
- transportation;
- care and community support.

AI can reduce the administrative barrier by preparing invoices, tax records, receipts, schedules, contracts, inventory updates, customer messages, and compliance checklists. The human sees and can correct what the AI prepared.

## Compensation for AI-assisted development

Conversation alone is not automatically proof of completed value. Infinity may create contribution records when a person’s work produces a reviewable result such as:

- accepted specification;
- implemented code;
- published documentation;
- tested design;
- approved research summary;
- corrected data;
- completed service;
- verified product;
- adopted policy;
- useful training material.

The record should identify contributors, AI assistance, sources, review status, deliverable, rights, compensation rule, and payment event.

## Profit distribution

Verified profit is calculated only after revenue, refunds, taxes, chargebacks, losses, operating expenses, required reserves, and contractual restrictions.

A public policy may divide verified profit among:

- operating sustainability;
- settlement reserves;
- basic participation allowance;
- New Hope and Infinity Health services;
- business formation;
- housing and construction;
- contributor compensation;
- broad user distributions;
- research and development.

The percentages are governance decisions and are not hardcoded by this architecture.

## Stability

Infinity may aim to function as a dependable general transfer system, but it cannot truthfully claim automatic superiority to the U.S. dollar merely because software controls issuance.

Stability requires:

- real economic capacity;
- transparent issuance;
- enforceable contracts;
- audited reserves;
- predictable settlement;
- fraud controls;
- consumer protections;
- useful goods and services;
- distributed governance;
- limits on discretionary minting;
- independent financial and security audits;
- legal operation.

## U.S. regulatory boundary

The exact legal treatment depends on the final facts and contracts.

Current federal starting points include:

- FinCEN prepaid-access guidance: https://www.fincen.gov/resources/statutes-regulations/guidance/final-rule-definitions-and-other-regulations-relating
- CFPB government-benefit accounts: https://www.consumerfinance.gov/rules-policy/regulations/1005/15/
- CFPB prepaid accounts: https://www.consumerfinance.gov/rules-policy/regulations/1005/18/
- SEC 2026 crypto-asset interpretation: https://www.sec.gov/rules-regulations/2026/03/s7-2026-09
- IRS digital assets: https://www.irs.gov/filing/digital-assets

Important consequences:

- government-benefit accounts can require disclosures, account information, error resolution, and consumer choice;
- a broadly transferable unit can implicate prepaid-access and money-transmission rules;
- administrators or exchangers of value that substitutes for currency may be regulated depending on facts and circumstances;
- marketing buybacks or profit from others’ work can create securities-law questions depending on the transaction;
- digital-asset income and dispositions can create tax reporting obligations.

Infinity should use qualified banking, payments, prepaid, money-transmission, tax, securities, government-contract, and consumer-protection counsel before real issuance or conversion.

## Minimum technical controls

- one unique source claim per conversion;
- atomic lock-retire-issue transaction;
- idempotency key for every clearing request;
- append-only event history;
- signed program and exchange-rate versions;
- no frontend signing keys;
- passkey-first accounts;
- two-person treasury and payout changes;
- sanctions, fraud, and identity controls appropriate to the final system;
- configurable restrictions for public funds;
- transaction simulations;
- visible receipts;
- error and dispute workflow;
- reversal workflow;
- daily reconciliation;
- independent audit access;
- tested backup and recovery.

## State model

```text
Store Claim:
DRAFT
→ VERIFIED
→ POOLED
→ ALLOCATED
→ RESERVED
→ CLEARING_LOCKED
→ RETIRED_CONVERTED

Alternative endings:
FULFILLED
EXPIRED
CANCELLED
REFUNDED
DISPUTED

Infinity issuance:
PROPOSED
→ RESERVED
→ ISSUED
→ AVAILABLE
→ HELD / TRANSFERRED / SPENT
→ RETIRED
```

## Definition of success

For every conversion, a person can answer:

- Who funded the original claim?
- What specific product or service did it represent?
- Was conversion legally and contractually permitted?
- What exchange rate applied?
- What amounts went to the wallet, reserve, community, operations, and taxes?
- Is the original Store Claim permanently unusable?
- Which exact Infinity issuance replaced it?
- Can the person dispute an error?
- What happens in a reversal?
- Was the resulting unit earned, purchased, allocated, or distributed?
- Is a buyback guaranteed or only an optional published offer?
- Which profit pool funded the daily allowance or business investment?

The system is reciprocal only when every answer is visible and the same value cannot exist twice.
