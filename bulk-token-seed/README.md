# Infinity Bulk Four-Hash Token Seed

This subsystem restores the fast, cheap token-generation layer that existed before the Living Token system accumulated research, personalization, action-token, wallet, and hourly-scoring complexity.

The design goal is simple: **build the inventory first; enrich it later.** Infinity should be able to seed large numbers of dormant tokens in bulk so the future site has a deep library ready for users to encounter, unlock, research, combine, and revive.

## Canonical token skeleton

Every seeded token begins with a small public skeleton:

```text
Token ID       🧱 🧱 🧱 🧱
Value          🧱 🧱 🧱 🧱
Category       profile-rendered color lane
Date           immutable birth date + growing interaction account
```

The four bricks are four deterministic SHA-256-derived segments. They are not four separate currencies and are not four Git commits. Together they form a compact, independently verifiable identity envelope for the token.

### Canonical for every viewer

These facts do not change by viewer:

- `token_id`
- `identity_hash`
- four identity brick segments
- `base_value`
- `value_hash`
- source/provenance pointer
- birth timestamp
- Git commit SHA once one exists

The **Token ID and base Value are the same for everybody**. A profile must never rewrite these canonical fields.

### Late-bound for each viewer

These are calculated when the token is rendered:

- displayed title/name
- primary color/category
- secondary color lanes
- jump-link words and phrases
- related-token ranking
- project summary emphasis
- research emphasis
- AI next-action prompt
- visible unlocked portions of the token

That means Kris and another user can open the exact same token and receive different useful paths without having different token identities.

## Four-hash envelope

The restored seed format uses four related hashes/segments:

1. **Identity** — what token this is.
2. **Value** — immutable base-value record and valuation-policy version.
3. **Provenance** — where the token came from: source text/file/repository/commit/import batch.
4. **Interaction root** — starting root for the append-only interaction chain.

Each full SHA-256 is retained in the database. The wallet may display four short brick segments from the identity hash for compact rendering.

The interaction root does not change; later interaction events build an append-only chain/tree from that root.

## Dormant / bricked token

A newly bulk-generated token is intentionally cheap and incomplete. It can exist in `BRICKED` state with little more than its canonical skeleton and source pointer.

A bricked token is **not deleted, invalid, or worthless data**. It means the richer Living Token layers have not been opened yet.

A jump-to action can unlock a door:

- **Green — ENGINEER**: use token B to build or materially advance token A.
- **Blue — IMPORT**: bring a capability/form/data/component from B that A lacks.
- **Yellow — RESEARCH / EXTRACT**: extract information/evidence from B for A.
- **Orange — DECIDE**: use accumulated Yellow research/evidence to present a decision.
- **Red — ROUTE / FORK**: expose two or more legitimate paths away from the current route.
- **Purple — ASSIMILATE**: combine imports and alternate routes into a broader architecture.

Unlocking is progressive. The canonical token remains the same while research, relationships, render plans, and user-specific views accumulate around it.

## Bulk first, intelligence later

The bulk compiler performs only inexpensive deterministic work:

1. read newline JSON, CSV-like text, repository records, URLs, notes, or other source rows;
2. normalize a stable source key;
3. generate the four-hash envelope;
4. store the canonical token skeleton;
5. enqueue enrichment without blocking token creation.

It does **not** wait for web research, AI synthesis, color personalization, image generation, or Git commits.

This allows tens of thousands or more token skeletons to be prepared ahead of site adoption. Expensive work happens only when a token is scored highly, opened, clicked, or selected by the hourly research system.

## Interaction watcher

Every user interaction with a token is an Action Token/event, not automatically a Git commit.

An event records:

- user/account
- token A
- optional token B
- rendered lane/color at click time
- anchor phrase clicked
- source and destination view
- timestamp
- profile version used for rendering
- event hash
- previous event hash for that user/session where available

The sequence itself becomes research evidence. For example:

```text
A --GREEN--> B --BLUE--> C --YELLOW--> D --ORANGE--> E
```

can later be analyzed as a user engineering A with B, importing a missing part from C, extracting evidence from D, and reaching a decision at E. The clicks are OBSERVED; the meaning inferred from the path is INFERRED until supported.

## Hourly compaction

High-volume interaction data is written continuously to the event ledger but Git is checkpointed in batches. Once per hour the system can:

- tally events;
- rebuild paths;
- update profile features;
- score color-lane relationships;
- expand Project Research;
- expand Infinity Discovery Research;
- record unlock depth;
- generate one deterministic checkpoint payload;
- create at most the intended checkpoint commit instead of one commit per click.

This preserves the hard Git provenance layer without producing an unusable recursive commit storm.

## Relationship to Living Tokens

`BRICKED` -> `SEEDED` -> `OPENED` -> `RESEARCHED` -> `CONNECTED` -> `BUILD_READY` -> `BUILT`

These are lifecycle states, not replacements for the immutable token identity.

The token can become richer indefinitely while the original four-hash envelope stays stable.

## Value

`base_value` is canonical and viewer-independent. Any later scoring such as relevance, research depth, build readiness, rarity, activity, or usefulness must be stored as separate metrics rather than silently changing the canonical base value for different people.

This distinction allows a wallet to show one stable token/value record while still presenting very different personalized opportunities to different users.

## Termux / zero-dependency target

The compiler intentionally uses only Python's standard library plus SQLite. It is designed to work with a normal `python3` installation and does not require pip packages.

Example:

```bash
python3 bulk_seed.py --db ../commit-token-ledger/data/tokens.sqlite3 \
  --input seeds.jsonl --namespace infinity-library
```

The output is a compact report showing created, existing, and failed records. Research and rendering are separate passes.
