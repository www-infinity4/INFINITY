# Living Physical Asset Tokens

## Purpose

A physical-asset token does not end when an asset becomes available. The token remains a living project/provenance object that can continue through sale, redemption, fabrication, gifting, insurance, events, media, resale, and future research.

The system must distinguish three things:

1. **Canonical token history** — immutable commit/hash provenance.
2. **Contractual rights** — what the current holder is actually entitled to receive, transfer, redeem, or sell.
3. **Living documentation** — pages, research, images, timelines, merchant material, life events, and descendant projects that can keep growing around the token.

A token must never imply legal title to a physical object unless the underlying merchant/custody/contract record supports that claim.

## Example lifecycle

A user unlocks a gemstone realm through a sequence such as:

`⭐ → 📷 → ♦️ → 💎`

The diamond realm may initially be a verified candidate. If a supplier reserves an identified stone and a contractual entitlement is created, the token can represent that right. The holder can then choose among routes such as:

- redeem the entitlement and receive the stone;
- keep the entitlement unredeemed;
- transfer or sell the entitlement if the contract permits;
- commission a ring and convert the token into jewelry provenance;
- gift the token/asset rights where permitted;
- attach appraisal, grading, insurance, custody, shipping, or resale documentation;
- create a wedding, anniversary, family-history, design, merchant, or collector page around the same lineage.

No route erases the earlier history.

## Transfer is a lineage event

Selling a token is not `DELETE(old owner)`. It creates an append-only transfer event:

```text
Token T
  ↓
Holder A
  ↓ TRANSFER / SALE
Holder B
  ↓
Token T continues
```

The immutable token ID remains the same. Holder/account state changes. If the transaction creates new documentation or project work, those commits receive descendant Commit Tokens while retaining links back to Token T.

## Rights bundle

A physical-asset token can carry a rights bundle with independently controlled capabilities:

- `VIEW_PROVENANCE`
- `TRANSFER_TOKEN`
- `TRANSFER_ENTITLEMENT`
- `REDEEM_ASSET`
- `REQUEST_FULFILLMENT`
- `COMMISSION_DERIVATIVE`
- `ADD_DOCUMENTATION`
- `ADD_MEDIA`
- `CREATE_DESCENDANT_PROJECT`
- `LIST_FOR_RESALE`

The rights available to a holder are determined by verified agreements and system permissions, not by the emoji alone.

## Living derivative example: wedding stone

A verified gemstone token may later be connected to:

- stone photographs;
- grading/certificate records;
- jeweler and merchant records;
- ring CAD/design files;
- fabrication records;
- proposal/wedding media;
- wedding-page profile image;
- vows, song, poem, invitations, tickets, venue, travel and timeline realms;
- appraisal and insurance records;
- maintenance/repair history;
- inheritance or resale history.

The gemstone story therefore becomes a long-lived knowledge and asset graph rather than a one-time checkout object.

## AI assembly

The AI may suggest useful connections from the holder's profile, prior actions, token history, and verified inventory. Suggestions remain suggestions until a user acts.

Examples:

- `GREEN + 💎` — engineer a ring or setting around the stone.
- `BLUE + 📷` — import approved photographs into the token page.
- `YELLOW + 💎` — research grading, origin, treatments, comparable stones, or care.
- `ORANGE + ♦️` — decide among verified merchants or fulfillment routes.
- `RED + 💎` — show redeem, hold, sell, gift, commission, or alternate-asset routes.
- `PURPLE + 💎 + 🎬 + 🎵` — assimilate the gemstone, wedding video, and song into a wedding project/page.

Profile-conditioned rendering can change which route is emphasized, but cannot change canonical provenance, verified asset identity, or contractual rights.

## Value

The system should show value as layered data rather than one unsupported number:

- canonical/base Infinity value;
- verified merchant quote;
- paid/reserved amount;
- appraisal value when documented;
- resale listing price;
- completed sale price;
- research/activity value under Infinity's internal scoring model.

Market and appraisal values must retain their source and timestamp.

## Non-termination rule

Redemption, transfer, delivery, or sale changes the token state; none of them terminates the token history. A token may continue indefinitely as provenance, media, research, project lineage, asset history, and user-created derivative work.
