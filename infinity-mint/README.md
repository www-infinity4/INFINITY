# Infinity Mint — Living Infinity Capital Notes

Infinity Mint is the wallet-facing mint and token-entry surface for the Infinity system. It turns one individually minted $1 Infinity Capital Note into a visual gateway for a Living Token.

> **Status:** prototype architecture. Infinity Capital Notes are internal digital/collectible instruments in the Infinity ecosystem and are **not U.S. legal tender or Federal Reserve notes**.

## Core rule

A user receives up to **10 individual $1 Infinity Capital Note mint opportunities per local calendar day**. The user must mint them one at a time. There is no `Mint $10` batch button.

Each note has:

- a stable note ID;
- a browser-generated provisional SHA-256 token fingerprint;
- a later ledger/Git commit binding when the backend checkpoint is written;
- a rendered serial field designed to change without changing the master note artwork;
- optional phone-drawn signature;
- optional image, audio/song, video, poem/text, card/project, research, tree-coupon, Alien Coin, or other token attachments;
- optional AI/profile curation when the user leaves the personalization area blank;
- links into Project Research and Infinity Discovery Research;
- profile-conditioned color actions and jump words;
- Living Token lineage as users continue, import, research, decide, route, and assimilate.

## Identity layers

Do not confuse these identifiers:

1. **Note ID** — local/user-facing identity created when minting starts.
2. **Provisional token fingerprint** — SHA-256 of the canonical note payload created in the browser. This makes the draft content tamper-evident.
3. **Commit Token** — the actual `owner/repository@full-git-SHA` identity created only after the finished note/checkpoint is committed by the ledger service.
4. **Action Tokens** — high-volume click/route events accumulated during use and summarized in hourly scoring checkpoints.

A note can render the shortened provisional fingerprint while pending. After commit binding, the renderer must prefer the shortened Git commit SHA and retain the provisional fingerprint in provenance.

## Mint flow

```text
Wallet
  ↓
Mint one $1 note
  ↓
Personalize
  ├─ draw signature on phone
  ├─ image / art
  ├─ song / audio
  ├─ video
  ├─ poem / story
  ├─ card / project
  ├─ research
  ├─ Alien Coin data
  ├─ tree coupons
  └─ leave blank → profile-conditioned AI curation
  ↓
Generate note payload + provisional SHA-256
  ↓
Save to wallet
  ↓
Hourly/backend checkpoint binds the finished record to Git
  ↓
Commit Token
  ↓
Open note → Living Token workspace
```

## Color grammar

Color is an operation selected at render time for a particular user, not a permanent universal label on the canonical commit.

| Lane | Meaning | A → B operation |
|---|---|---|
| Green | Engineering | use B to build/advance A |
| Blue | Import | bring a missing form/component/data from B into A |
| Yellow | Research / extract | extract useful evidence/information from B for A |
| Orange | Decision | present an evidence-informed decision about A, often informed by Yellow research |
| Red | Route / fork | expose two or more legitimate paths away from the current point |
| Purple | Assimilation | combine imports and alternate routes into a broader architecture |

The renderer chooses anchor words/phrases and target tokens using the current user profile, research corpus, token graph, and action history.

## User profile

The profile is continuously refined from explicit information and consented activity. Useful features include:

- interests;
- skills;
- education/training;
- active projects;
- tools and technologies used;
- tokens opened/saved/continued;
- lane selections;
- suggestions accepted/rejected;
- search history inside Infinity;
- user-entered profile facts.

Canonical token history is the same for everyone. Token title, emphasis, color ranking, jump links, suggested related tokens, and AI build prompt may differ per viewer.

## Files

- `index.html` — zero-dependency mobile-first mint + wallet prototype.
- `mint_schema.sql` — durable server-side note/asset/commit-binding model.
- `API-CONTRACT.md` — production integration between browser, profile brain, ledger, research, and Git checkpoint writer.

## Privacy / safety model

- User-uploaded media stays local in this prototype via IndexedDB.
- A production backend must require explicit consent before uploading private media.
- Do not put GitHub credentials or private API keys in the browser.
- Sensitive personal traits must not be silently inferred for ranking.
- AI-generated research must preserve `OBSERVED`, `INFERRED`, `EXTERNALLY_VERIFIED`, and `USER_DEFINED` evidence states.

## Acceptance criteria

The mint is considered complete only when the production system can demonstrate:

1. exactly one note is minted per deliberate mint action;
2. daily allowance cannot exceed 10 notes for the account/day;
3. each note renders its own serial/token reference;
4. touch signature works on mobile;
5. assets can be attached and previewed;
6. blank personalization can request profile-conditioned curation;
7. wallet lists all minted notes and can reopen each note;
8. finished notes can be bound to an actual Git commit without exposing credentials client-side;
9. opening a bound note enters its Living Token page;
10. color actions create Action Tokens and pending operations rather than silently rewriting canonical history;
11. accepted project changes create new Git commits and descendant Commit Tokens;
12. the two research streams continually enrich the token without fabricating external verification.
