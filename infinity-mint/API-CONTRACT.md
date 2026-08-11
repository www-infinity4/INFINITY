# Infinity Mint Production API Contract

This contract connects the mobile Mint UI to authenticated user profiles, durable media storage, the Commit Token ledger, two-stream research brain, Action Token scorer, and Git checkpoint writer.

The browser must **never** hold a GitHub write credential.

## 1. Session / profile

`GET /api/profile`

Returns the authenticated user profile plus profile version used for late-bound rendering.

```json
{
  "user_id": "u_123",
  "profile_version": 81,
  "explicit_features": [],
  "behavioral_features": [],
  "consents": {
    "behavioral_personalization": true,
    "private_media_research": false
  }
}
```

## 2. Daily allowance

`GET /api/mint/allowance`

```json
{
  "local_day": "2026-08-10",
  "limit": 10,
  "minted": 4,
  "remaining": 6,
  "next_position": 5
}
```

The server, not the browser, is authoritative. The server must transactionally reject an eleventh note for the same account/day.

## 3. Start one note

`POST /api/mint/notes`

Creates exactly one draft and reserves one daily position.

```json
{
  "denomination": 1
}
```

Response:

```json
{
  "note_id": "note_...",
  "daily_position": 5,
  "state": "DRAFT"
}
```

## 4. Assets

`POST /api/mint/notes/{note_id}/assets`

Multipart upload. Supported conceptual types include:

- signature;
- image/art;
- audio/song;
- video/movie;
- poem/story;
- card;
- project;
- research;
- Alien Coin data;
- tree coupon;
- link;
- AI-curated content.

The response records a content hash. Private media is not exposed to research or another user unless the owner permits it.

## 5. Curate blank note

`POST /api/mint/notes/{note_id}/curate`

The profile/token brain returns several candidates rather than silently choosing content where user confirmation matters.

Candidates may come from:

1. the user's own token graph;
2. Project Research;
3. Infinity Discovery Research;
4. saved/created media;
5. user-authorized public material.

Every suggestion includes `why_this`, evidence/provenance, and the profile features responsible for its ranking.

## 6. Finalize

`POST /api/mint/notes/{note_id}/finalize`

The server constructs canonical JSON, hashes it, and returns the immutable provisional fingerprint.

The note is now frozen as a mint event. Later enrichment is appended rather than rewriting the original payload.

## 7. Commit binding

Finalized notes enter the next checkpoint queue.

The checkpoint worker writes a deterministic ledger artifact to Git. The resulting Git SHA creates the actual Commit Token:

```text
www-infinity4/<ledger-repository>@<full-git-sha>
```

The service then updates:

- `git_repository`;
- `git_commit_sha`;
- `commit_token_id`;
- `displayed_serial`.

The renderer swaps the pending serial for a shortened representation of the real commit SHA while preserving the provisional SHA-256 in provenance.

Multiple finalized notes may be included in one hourly checkpoint commit. Each note therefore also needs a stable record path/index within that checkpoint so several notes do not collapse into one identity. Recommended logical identity:

```text
<commit-token-id>#mint-note/<note-id>
```

The Git SHA anchors the batch; the note ID selects the immutable note record inside it.

## 8. Wallet

`GET /api/wallet/notes`

Returns rendered note manifests, not just database rows. A rendered manifest includes:

- canonical note facts;
- the user's current display title;
- current serial;
- asset thumbnails;
- research status;
- top color-action opportunities;
- descendant/parent counts;
- build readiness.

`GET /api/wallet/notes/{note_id}` opens the note as a Living Token.

## 9. Color action

`POST /api/tokens/{token_id}/actions`

```json
{
  "lane": "GREEN",
  "anchor_text": "sensor controller",
  "target_token_id": "...",
  "render_manifest_id": "..."
}
```

This creates an Action Token immediately. It does not create a Git commit.

Lane semantics:

- `GREEN`: ENGINEER(A,B)
- `BLUE`: IMPORT(A,B)
- `YELLOW`: RESEARCH_EXTRACT(A,B)
- `ORANGE`: DECIDE(A,B), normally evidence-informed by Yellow material
- `RED`: ROUTE(A,{B,C,...})
- `PURPLE`: ASSIMILATE(A,{imports,routes,...})

## 10. Pending operation → real project

Blue, Green, Orange, Red, and Purple may create a `pending_token_operation` containing:

- source token A;
- contributing token(s) B...N;
- exact proposed files/content;
- research/evidence used;
- user's intent/action path;
- tests/acceptance criteria;
- AI explanation;
- approval state.

A preview must be shown before any material project write where user approval is required.

When accepted work actually changes a repository:

1. create/change files on a project branch;
2. validate the changed output;
3. create the real Git commit;
4. ledger the commit as a new Commit Token;
5. record lineage (`ENGINEERED_FROM`, `IMPORTED_FROM`, `ROUTED_FROM`, `ASSIMILATES`, etc.);
6. start Project Research and Infinity Discovery Research for the new token;
7. render the descendant into relevant users' wallets according to their profiles.

This is the point where a color-coded jump can grow into a new website/project rather than being merely a link.

## 11. Hourly action checkpoint

The Action Token scorer groups the user's path during the hour:

```text
A --GREEN--> B --BLUE--> C --YELLOW--> D --RED--> {E,F} --ORANGE--> E
```

The research brain can infer a narrative from this path, but the click sequence remains `OBSERVED` and the interpretation remains `INFERRED` unless evidence confirms it.

The hourly report updates:

- profile weights;
- token-to-token relationship scores;
- Project Research;
- Infinity Discovery Research;
- candidate jump words;
- build/route/import suggestions;
- documentation reframing;
- checkpoint ledger data.

## 12. Two research streams

Every Commit Token receives both:

### Project Research

Research about the project itself: commit changes, purpose, dependencies, history, missing pieces, tests, later/earlier implementations, sources and factual external context.

### Infinity Discovery Research

Continuously explores a different token/project/topic. It begins as `EXPLORATORY_LINK`. The system investigates whether there is a useful connection and records why it was promoted or rejected.

Research is versioned and append-only enough to retain provenance. New synthesis may reframe the displayed documentation without rewriting the original commit.

## 13. Generated token page

Each Living Token has a generated web manifest from which an `index.html` can be rendered. It contains:

- note art / serial;
- source commit;
- attached assets;
- profile-conditioned title and summary;
- Project Research;
- Infinity Discovery Research;
- selected jump words and six color operations;
- related tokens;
- routes and decisions;
- AI query/workspace;
- history and descendants.

The generated page is a *view* over canonical data plus a user/profile context. Two people can receive different rendered pages without having different historical Git facts.

## 14. Testing gates

Before calling the Mint production-ready, automated/browser tests must cover:

- multi-touch signature behavior;
- media upload/storage and size limits;
- exact daily limit under concurrent requests;
- provisional hash stability;
- successful checkpoint and Git binding;
- wallet reopen after refresh/device login;
- private-media authorization;
- Action Token creation for every color lane;
- hourly path reconstruction;
- profile-version reproducibility;
- Project Research generation;
- Discovery Research generation;
- evidence-state preservation;
- accepted Green/Blue action producing a descendant commit/token;
- failed project write leaving the source token unchanged.
