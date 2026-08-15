# Physical Asset Fourth Brick

## Purpose

The fourth brick is the bridge between Infinity knowledge/activity and a real-world physical asset path. It must not unlock merely because an AI predicts that a user likes an asset category. A physical symbol such as 💎 becomes active only after the ledger can point to a verified merchant/supplier record, a specific asset or reservable inventory class, pricing/valuation evidence, funding or entitlement logic, and fulfillment/custody state.

## Example progression

A user may unlock realms in sequence:

- ⭐ Star/project key — an unlocked Star-family or StarCraft-family relationship.
- 📷 Image/media key — images/content added to or promoted through the token/page.
- ♦️ Merchant key — a verified merchant or commerce path attached to the token.
- 💎 Physical gemstone key — a real gemstone asset entitlement or sourcing path.

The first three keys can be knowledge, media, and commerce relationships. The fourth key is special: when it represents a physical asset, it must resolve to a physical_asset_id and an auditable acquisition/fulfillment state.

## Research value versus physical value

Infinity can assign internal research value to authored, sourced, connected research. That is distinct from the price or ownership of a real physical object.

A physical asset claim requires its own ledger facts:

- merchant_id and verification state
- asset_id / SKU / certificate number when available
- asset type, material, weight, grade, treatment/origin disclosures where relevant
- asking price and currency
- independent appraisal/certificate data when available
- inventory/reservation state
- funding/entitlement source
- custody state
- fulfillment/shipping state
- owner/beneficiary account
- timestamps and evidence URLs/documents

No token should state that a user owns a diamond, gemstone, ticket, or other physical object until the entitlement/fulfillment layer supports that statement.

## Economic activity

Advertising, merchant activity, imports, clicks, purchases, commissions, and other supported economic events can be tallied as Action Tokens. The hourly scorer can determine whether an account has earned or funded a physical-asset entitlement under explicit program rules.

This is not the same as assuming every click has cash value. The economic rules must identify which events are compensable, their rate/source, and the resulting balance or entitlement.

## Personalized discovery

The profile algorithm can predict that a user is already seeking gemstones and can rank 💎 opportunities highly for that user. It may locate verified suppliers and prepare candidate assets. The recommendation is profile-conditioned; the supplier and asset facts are canonical.

Example:

```text
TOKEN
  ⭐ unlocked project relationship
  📷 unlocked media/content relationship
  ♦️ verified merchant relationship
  💎 physical asset candidate
       ↓
 verified merchant
       ↓
 inventory / certificate / quote
       ↓
 funding or entitlement condition satisfied
       ↓
 RESERVED
       ↓
 PURCHASED / FULFILLED
```

## Physical asset state machine

```text
DISCOVERED
→ MERCHANT_VERIFIED
→ ASSET_VERIFIED
→ ELIGIBLE
→ RESERVED
→ PURCHASED
→ IN_CUSTODY
→ SHIPPED
→ DELIVERED
```

A token may also enter `EXPIRED`, `CANCELLED`, `OUT_OF_STOCK`, `REFUNDED`, or `DISPUTED`.

## Symbol rule

A symbol has three levels:

1. **Realm visible** — 💎 means the gemstone realm is relevant.
2. **Asset candidate** — a verified supplier/item has been matched.
3. **Physical entitlement** — the fourth brick points to a concrete `physical_asset_id` and entitlement state.

The UI must visually distinguish these levels so a suggested gemstone is never confused with an owned gemstone.

## Evidence

Merchant identity, inventory, pricing, certification and fulfillment facts are `EXTERNALLY_VERIFIED` only when their sources are stored. User intent is `USER_DEFINED`. Algorithmic matching is `INFERRED`. Clicks and ledger events are `OBSERVED`.
