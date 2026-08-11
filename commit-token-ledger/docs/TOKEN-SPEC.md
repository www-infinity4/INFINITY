# Commit Token Specification

## Canonical identity

Each token is derived from one and only one Git commit source event.

```text
source_key = owner/repository@full_commit_sha
token_id   = ICT- + first_32_hex(SHA256(source_key))
```

The token ID never changes when classification changes.

## Required provenance

Every record preserves the repository, full commit SHA, commit URL, message, parent SHAs, author/committer metadata, authored/committed timestamps and watcher discovery time.

## Classification fields

- `initial_classification`: state assigned at first capture. Ordinary commits begin `NON_SPACEX`; watcher bookkeeping commits can be `ADMINISTRATIVE`.
- `current_classification`: current Infinity taxonomy state.
- `classification_score`: current rule score.
- `classification_evidence`: exact terms/overrides that produced the classification.
- `evidence_level`: `OBSERVED`, `INFERRED`, or `CONFIRMED`.

## SPACE_X taxonomy

`SPACE_X` is an internal Infinity project classification for commits/repositories associated with the project's space/aerospace branch. It is not a statement about the corporation SpaceX.

The default classifier uses explicit weighted terms and manual repository overrides from `config.json`. A project can therefore move into or out of the class without altering its immutable source identity.

## Event history

`token_events` is append-only at the application level.

Events currently include:

- `TOKEN_DISCOVERED`
- `CLASSIFICATION_CHANGED`

Future safe extensions can include `MANUAL_REVIEW`, `SOURCE_TAGGED`, `EXPORT_CREATED`, and `VERIFICATION_ADDED`.

## No monetary assertion

A commit-token record is a provenance/catalog object. Any future economic valuation, transfer system, redemption rule or blockchain representation must be implemented and documented separately. Git history alone does not establish monetary value, securities status, legal tender status, or ownership rights over third-party technology.
