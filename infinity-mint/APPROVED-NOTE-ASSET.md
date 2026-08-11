# Approved Infinity Capital Note Front

## Status

The approved visual master is the front-only Infinity Capital / Bank of the NWO Reserve note selected in the August 10, 2026 design session.

The Mint must use **one master artwork file** and must never regenerate the artwork merely to change a token number. The expected production asset path is:

`infinity-mint/assets/infinity-capital-note-master.webp`

The generated image currently exists in the ChatGPT working session. The connected GitHub text writer cannot upload that binary asset, so this file records the exact integration target rather than silently replacing the approved art with a different design.

## Live serial rule

`note-template-v2.js` overlays the same display serial over both serial placeholders in the approved artwork. The serial is derived from the immutable full Commit Token hash.

Example:

`7ee49be7044b1a285ea363b55c1d65830fec05dd`

renders as:

`IC-7EE4-9BE7-044B-1A28`

The **full hash remains stored in the token ledger** and is exposed when the note is opened. The shortened serial is only the human-readable face identifier.

When a note is still local and has not yet been committed, the browser may generate a provisional SHA-256. As soon as the ledger binds the note to an actual Git commit, the face serial must be replaced by the Git-derived serial. A provisional hash must never be represented as a Git commit.

## Mint behavior

Every mint produces a separate note record. The note face must be rendered from:

1. the approved master image;
2. the live display serial;
3. the underlying full Commit Token hash;
4. the note owner's signature and attached assets in the surrounding Living Token interface; and
5. the note's research, action, symbol, and lineage records.

The image itself stays constant. The ledgered identity changes for every minted token.

## Wallet behavior

A wallet thumbnail must show the actual note face and its unique serial. Selecting the note opens the associated Living Token, where the user can inspect the full hash, media, research, symbols, colored actions, interactions, physical-asset rights where applicable, and descendant tokens.

This makes the visible sequence of notes auditable without requiring a unique banknote image file for every mint.
