# Infinity — August 12, 2026 Build Plan

## Objective

Stop expanding disconnected prototypes for one work session and make the existing system reliably talk through shared infrastructure.

## P0 — StarQuest share / StarCoin regression

1. Verify the independent Share safety-net on Android/mobile browser.
2. Test Share on at least:
   - one direct Archive MP4 episode;
   - one Archive item resolved at playback time;
   - one movie;
   - one YouTube-backed item if available.
3. Confirm the visible Share button is never disabled after playback opens.
4. Confirm the normal share sheet opens when `app.js` is healthy.
5. Intentionally simulate an `app.js` failure and confirm the safety-net opens the share sheet instead.
6. Verify native phone share, SMS, email, and exact-link copy.
7. Confirm a canceled share creates no StarCoin progress.
8. Confirm copied/unverified links remain auditable but do not falsely count as verified delivery.
9. Confirm a qualifying completed-watch + verified native share reaches the existing StarCoin ledger.
10. Check the wallet counter refreshes after a credited event.

Exit criterion: Share works independently of unrelated catalog/player errors and StarCoin accounting is neither blocked nor double-counted.

## P1 — Local Gemma runtime

1. Choose the first actual local execution framework for the development machine/device.
2. Download/accept the appropriate Gemma model weights through the chosen official/supported distribution path.
3. Bring up the local loopback runtime at the configured base URL.
4. Implement `/v1/health`.
5. Connect a general Gemma role for reasoning/synthesis.
6. Connect FunctionGemma for structured tool proposals.
7. Connect ShieldGemma 2 for image publication moderation.
8. Connect ShieldGemma text moderation for public text/ads/captions.
9. Add embeddings after the first four roles are stable.
10. Keep hosted providers disabled by default; only add a key if a deliberately chosen hosted fallback requires one.

Exit criterion: the central runtime responds locally to health, reason, tool, image-safety, and text-safety requests without any paid API being required for the normal local path.

## P2 — Infinity Mint moderation and creation toolkit

1. Replace any purely client-side `AI filtered` claim with a call to the shared `IMAGE_SAFETY` / `TEXT_SAFETY` roles.
2. Keep uploads in `LOCAL_DRAFT` until approved.
3. Add Art Pad.
4. Add direct microphone/audio recording.
5. Add Writing Studio.
6. Add Product/Ad Builder.
7. Add package-level moderation after individual asset moderation.
8. Preserve provenance: user-supplied vs AI-suggested vs AI-generated.
9. Confirm blocked/review-required content cannot enter transferable/public token manifests.

Exit criterion: a minter can create a rich note package and unsafe material cannot become publicly transferable through the normal UI.

## P3 — Research brain consolidation

1. Put Bitcoin Crusher, Octave Research Portal, Alien Coin enrichment, and the two-stream research writer behind the same `REASONER` and `TOOL_ROUTER` interface.
2. Keep external search as a tool, not something the model pretends it performed.
3. Run novelty checks against query hashes, source-set hashes, article hashes, token lineage, and prior user paths.
4. Make each generated research record explicitly identify `PROJECT_RESEARCH` or `INFINITY_DISCOVERY_RESEARCH`.
5. Preserve `OBSERVED`, `INFERRED`, `EXTERNALLY_VERIFIED`, and `USER_DEFINED` states.

Exit criterion: one AI runtime can create new research assignments across projects without duplicating the same article or corrupting evidence provenance.

## P4 — Shared wallet/API bridge

Do not call the wallet cross-device synchronized until this exists.

1. Deploy one authenticated ledger service/database.
2. Connect Mint daily allocation.
3. Connect Avatar Coin 10/day allocation + overflow project pool.
4. Connect Bitcoin Crusher and Mario first-ten allocation + system overflow.
5. Connect Alien Radio one/hour and 10/day rules.
6. Add idempotency and account-scoped reconciliation tests.

Exit criterion: the same signed-in account sees the same authoritative wallet state from two different apps/devices.

## P5 — TV catalog cleanup after Share

Only after P0 works:

- recheck Reading Rainbow;
- Price Is Right buffering/presence;
- M*A*S*H;
- Seinfeld;
- Twilight Zone;
- Alfred Hitchcock;
- For You genre diversity;
- exact Archive source health;
- player mobile regression;
- Avatar Coin marker placement.

Do not mix these fixes into the Share branch unless they directly break sharing.
