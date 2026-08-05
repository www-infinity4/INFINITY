# Good Bee · Infinity Living

Good Bee is a development prototype for voluntary accessible travel, trial stays, relocation, support coordination, modular housing, and physical NFC benefit credentials.

## Purpose

The platform is designed to help a person choose and coordinate:

- a beach, mountain, sailing, or other destination they prefer;
- a reversible vacation or trial stay before a permanent decision;
- an accessible home and transportation plan;
- personal assistance, nursing coordination, meals, companionship, and local services;
- a supported cross-country move with continuity of benefits and care;
- a Good Bee Honey Coin or card that opens a secure record of approved goods and services.

A new environment may improve quality of life for some people, but Good Bee does not present relocation as a medical cure and does not replace healthcare chosen by the person.

## Operating rules

1. Participation is voluntary.
2. The person chooses the destination and may reject any provider or package.
3. No destination is assigned by gender, disability, diagnosis, income, or another protected characteristic.
4. Trial stays include return transportation or another practical exit plan.
5. Permanent moves require housing verification, benefits continuity, care handoff, and follow-up.
6. A private home remains a home; support services do not create institutional control.
7. AI may organize options and detect missing steps but cannot force a move, withdraw support, or redirect money.
8. Health, identity, financial, and support records are never stored in a public GitHub repository.

## Current website

The static prototype includes:

- responsive blue, navy, purple, and honey visual design;
- a person-directed vacation, trial-stay, move, and housing package builder;
- beach, mountain, sailing, and supported relocation examples;
- disability-access and nursing-coordination choices;
- four modular accessible housing models;
- a Good Bee Honey Coin NFC operating explanation;
- example goods-and-services benefit units;
- consent, privacy, money-control, dispute, return, and audit protections.

## Run locally

From the repository root:

```bash
python3 -m http.server 8080
```

Open:

```text
http://localhost:8080/good-bee/
```

No package manager, API key, paid AI service, account, or database is required for the current prototype.

## Files

```text
good-bee/
├── index.html
├── styles.css
├── app.js
├── README.md
└── data/
    └── programs.json
```

## Good Bee Honey Coin

The physical coin or card is an NFC access credential—not a self-contained wallet.

```text
Tap NFC credential
        ↓
Resolve rotating credential with Infinity service
        ↓
Verify person, package, provider, limits, and consent
        ↓
Display the specific approved good or service
        ↓
Person confirms fulfillment
        ↓
Append receipt to the protected ledger
```

The tag must not store medical records, identity documents, private keys, bank credentials, or a readable monetary balance. A lost credential must be freezeable and replaceable. High-value actions require another authentication or human approval.

### Benefit-unit model

The prototype uses clearly defined units rather than pretending the coin is legal tender:

- one approved lodging night;
- one accessible ride;
- one meal or grocery allocation;
- one support hour;
- one listed experience;
- one defined move package;
- one home setup package.

Each unit requires scope, expiration, refund, substitution, provider, and dispute rules before launch.

If Good Bee later becomes a reloadable or broadly spendable prepaid product, banking, payments, consumer-protection, money-transmission, identity-verification, data-security, and state-law review will be required before public use.

## Housing system

The housing concept uses standardized, replaceable, robot-readable components while retaining licensed professional control.

Robots may assist with:

- material handling;
- cutting and drilling;
- panel placement;
- fastening with measured torque;
- scanning and dimensional verification;
- leak and continuity tests;
- component identification;
- inspection documentation;
- safe replacement instructions.

Robots do not replace required architects, engineers, inspectors, electricians, plumbers, accessibility specialists, fire officials, permits, or local code approval.

### Accessibility baseline

Every model begins with universal and adaptable design rather than treating access as a later upgrade. Features include zero-step routes, usable clearances, accessible kitchens and wet rooms, reachable controls, communication features, hands-free options, backup-power planning, safe evacuation, and configurable assistive technology.

Final construction must be reviewed against applicable federal, state, local, zoning, flood, wind, wildfire, energy, plumbing, electrical, mechanical, fire, accessibility, and coastal requirements for the actual site.

## Backend required for real operation

The public website may remain mostly static. Real operation requires protected services for:

- passkey-first accounts and recovery;
- consent and representative permissions;
- private accessibility and health information;
- provider verification;
- package inventory and reservations;
- payments and refunds through qualified partners;
- benefit-unit ledger and receipts;
- dispute and fraud handling;
- travel and care coordination;
- building permits, inspections, and warranty records;
- security monitoring, backups, and incident response.

No one AI, administrator, or NFC credential should possess enough authority to secretly change a payment destination, move a person, expose private records, or erase the audit trail.

## Launch status

This is software and service-architecture work, not an operating housing provider, travel agency, healthcare provider, bank, insurer, benefit program, licensed contractor, or token offering. All destinations, capacities, prices, funding, and benefit balances displayed by the prototype are examples only.

See [`../docs/GOOD_BEE_OPERATING_MODEL.md`](../docs/GOOD_BEE_OPERATING_MODEL.md) for the broader system plan.
