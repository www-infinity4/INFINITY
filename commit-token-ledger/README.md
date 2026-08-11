# Infinity Commit Token Ledger

## Purpose

The Infinity Commit Token Ledger treats a Git commit as an immutable source event from which a durable token record can be derived.

A token in this repository is a **database record**, not a claim that the Git commit itself is cryptocurrency, legal tender, equity, or a token issued by any outside company.

The internal class name `SPACEX` / `SPACE_X` is an Infinity taxonomy label. It does **not** imply affiliation with, ownership of, endorsement by, or issuance from SpaceX or any other company.

## Core Theory

A repository can be understood as an occupied information-space with a recoverable history. Editing a README does not erase the earlier state: Git preserves earlier commits, and each commit SHA identifies a particular recorded state/change in that history.

The ledger turns that property into a catalog:

1. A watcher discovers a commit.
2. The commit becomes a source event.
3. A deterministic token ID is derived from repository identity + full commit SHA.
4. The token begins with a neutral class: `NON_SPACEX`.
5. The classifier records evidence about the repository and commit.
6. If configured classification rules are satisfied later, the same token transitions to `SPACE_X` rather than creating a duplicate token.
7. Every classification transition is retained in an append-only event history.

This makes the token represent **continuity through version history**. The token ID stays fixed even if its classification changes.

## Token Identity

Canonical source key:

```text
<owner>/<repository>@<40-character-git-sha>
```

Deterministic token ID:

```text
ICT-<SHA256(canonical-source-key)[0:32]>
```

The full source SHA is always preserved in the database, so the shortened token ID is only a convenient public identifier.

## State Model

```text
DISCOVERED
    |
    v
NON_SPACEX
    |
    | classification evidence reaches configured threshold
    v
SPACE_X
```

A token is not destroyed when it changes state. The `tokens` table stores its current classification and the `token_events` table preserves the complete transition history.

## Why a Separate Ledger Database Is Necessary

A naive design would append a token to a file, commit that file, then tokenize the new commit. That creates an endless recursive minting loop:

```text
commit -> token-db commit -> token -> token-db commit -> ...
```

The watcher therefore writes its operational state to `data/commit_tokens.sqlite3`, which is ignored by Git. Export snapshots may be committed deliberately, but watcher-generated administrative commits can be marked `ADMINISTRATIVE` and excluded from automatic minting unless explicitly imported later.

This keeps repository events and ledger bookkeeping separate.

## Files

```text
commit-token-ledger/
├── README.md                  # system theory and operating model
├── watcher.py                 # zero-dependency GitHub commit watcher
├── classify.py                # reusable classification logic
├── config.json                # repositories and SPACE_X classification rules
├── schema.sql                 # SQLite schema
├── .gitignore                 # excludes live ledger database/runtime state
├── docs/
│   ├── TOKEN-SPEC.md          # canonical token/event fields
│   └── WATCHER-OPERATIONS.md  # running, backfill, export and failure behavior
└── data/
    └── .gitkeep
```

## What the Watcher Actually Watches

The watcher queries the GitHub API for repositories owned by the configured account and then requests commits from those repositories. It stores:

- repository full name
- commit SHA
- parent SHAs
- author and committer metadata
- commit message
- commit timestamp
- canonical GitHub URL
- discovery timestamp
- initial classification
- current classification
- classification score and evidence

Because polling can miss events if a machine is offline, the program does not rely only on "new since last second" behavior. It remembers SHAs and can repeatedly scan recent history. `--backfill` can deliberately walk deeper history.

## Classification

`NON_SPACEX` means "captured but not classified into the SPACE_X branch of the Infinity taxonomy."

`SPACE_X` means "the configured Infinity classifier has determined that this commit/repository belongs to the project's space/aerospace subsystem."

Classification is evidence-based and configurable. The default implementation scores repository names, commit messages and README text against explicit terms such as `space`, `spacecraft`, `aerospace`, `propulsion`, `orbital`, `rocket`, `plasma shield`, and configured manual repository overrides.

A manual override is stronger than keyword inference and is recorded as evidence rather than silently changing a record.

## Reclassification Instead of Reminting

Suppose commit `abc...` is first seen in a general research repository:

```text
ICT-... -> NON_SPACEX
```

Later the repository is explicitly mapped into the Infinity space subsystem:

```text
ICT-... -> SPACE_X
```

The token ID remains identical. A new `CLASSIFICATION_CHANGED` event records the transition, timestamp, reason, score and evidence.

That makes the ledger useful for studying how concepts migrate between parts of the larger system.

## Running

Python 3 standard library only:

```bash
cd commit-token-ledger
python3 watcher.py --once
```

Continuous polling:

```bash
python3 watcher.py --interval 300
```

Backfill recent history:

```bash
python3 watcher.py --backfill 100
```

Optional authentication increases GitHub API limits:

```bash
export GITHUB_TOKEN='your-token'
python3 watcher.py --once
```

Do not commit a personal access token.

## Evidence Levels

The wider Infinity documentation convention applies here too:

- **Observed** — a GitHub commit/repository/API fact captured by the watcher.
- **Inferred** — a classifier result based on configured rules.
- **Confirmed** — an explicit manual classification or externally verified fact.

The database stores enough evidence to distinguish those states.

## Safety and Integrity

The watcher is read-only toward watched repositories. It does not rewrite history, force-push, delete branches, execute repository code, or automatically merge anything.

Its job is narrower: **observe commits, derive stable records, preserve provenance, classify them, and retain every transition.**
