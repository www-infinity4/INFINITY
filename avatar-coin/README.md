# Infinity Avatar Coin Service

Avatar Coin is one account-wide creation, attribution and project-routing service. Individual websites may expose a small Avatar Coin marker, but they do not own separate chains or balances.

## Canonical flow

1. A user opens an intentional Avatar Coin edit anchor.
2. The edit, design, generated content or project contribution is written as an Avatar Creation Event.
3. The central ledger assigns a stable `avatar_coin_id`, parent/lineage IDs, creator account, source repository/page/anchor and content hash.
4. The first 10 qualifying Avatar Coins created by an account on an account-day may be allocated into that creator's wallet.
5. Additional qualifying creations remain attributed to the creator but are not forced into the creator's wallet. They enter `PROJECT_MATCH_POOL` and are rendered into project feeds for accounts whose profile, skills, interests and token graph indicate likely usefulness.
6. If an overflow Avatar Coin is purchased or otherwise transferred under an authorized transaction, its holder allocation changes while creator attribution and lineage remain intact.
7. Project-feed recipients can open, research, import, engineer, assimilate, route or decide on the coin through the standard Infinity color-action system. Their work produces descendant Avatar Creation Events rather than overwriting the original.

## Ownership is not authorship

`creator_account_id` never changes. `holder_account_id` may change. Feed placement is not ownership. An overflow coin can appear in another user's project feed without being transferred to them. A purchase/authorized transfer is what changes holder state.

## Daily creator allocation

`AVATAR_COIN_CREATE` uses the shared Infinity entitlement authority. The creator-wallet allocation cap is 10 per account-day. The system may continue accepting and ledgering additional Avatar Creation Events after the cap. Those overflow records route to `PROJECT_MATCH_POOL`.

This is separate from the user's other source-specific daily entitlements unless an explicit economy rule combines them.

## Trademark/editor marker placement

The marker is a portal affordance, not page decoration. Default placement rules:

- one brand/title anchor;
- major authored section headings where editing is useful;
- explicit `[data-avatar-anchor]` elements;
- selected generated-content cards/results;
- never every paragraph, form label, footer line or chat bubble;
- no duplicate markers inside one visual component;
- mobile hit target must not cover or displace primary controls.

Repositories should use an `avatar-coin.manifest.json` declaring their allowed anchors. A future central client should fetch/render the marker from this service rather than copying independent editor implementations.

## Feed rendering

Canonical coin facts are shared. Feed presentation is late-bound per viewer. The matcher can use permitted profile data, explicit interests/skills, prior color actions, current projects, related token symbols and accepted/rejected suggestions. It emits a scored feed placement with a reason such as `needs_component`, `related_research`, `skill_match`, `continuation`, or `serendipity`.

The renderer must keep these states distinct:

- `CREATED_ATTRIBUTED`
- `CREATOR_WALLET` (first 10/day)
- `PROJECT_MATCH_POOL`
- `FEED_RENDERED` (not ownership)
- `PURCHASED_TRANSFERRED`
- `BUILT_DESCENDANT`

## Color actions

Green = ENGINEER, Blue = IMPORT, Yellow = RESEARCH/EXTRACT, Orange = DECIDE, Red = ROUTE/FORK, Purple = ASSIMILATE. A feed may choose different anchor words, rankings and colors for different viewers without changing the Avatar Coin ID, creator, content hash or lineage.
