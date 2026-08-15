# Infinity Two-Commit Token Lifecycle

## Purpose

The commit-token system uses a bounded two-commit lifecycle so every source change can be permanently recorded without creating an uncontrolled chain of recursive bookkeeping commits.

A token is not a claim of external financial value. It is an Infinity project/provenance object anchored to Git history and enriched with research, lineage, scoring, and personalized rendering metadata.

## Commit A — Source / Birth Commit

Any normal Git commit in a watched `www-infinity4` repository is a source event.

The account watcher records:

- repository and branch
- full source SHA
- parent SHA(s)
- author and committer metadata available from Git
- commit timestamp
- commit message
- changed files and diff statistics when available
- subsystem classification
- lineage role
- internal `SPACE_X` / `NON_SPACEX` taxonomy
- evidence level

The deterministic token identity is derived from:

```text
owner/repository@full-source-sha
```

Commit A is immutable history. Later research never changes what Commit A actually contained.

## Hourly Score Window

The watcher scans the entire account on an hourly boundary. All source commits first observed during that window are accumulated into one scoring batch.

The scoring batch may calculate:

- project/subsystem categories
- lineage links to older tokens
- reuse/revival candidates
- build-readiness score
- research-completeness score
- dependency links
- risk/safety flags
- evidence confidence
- relevant-user matching features
- visual color/status metadata

A single hourly scoring commit records the batch. It does **not** create one bookkeeping commit per annotation.

## Commit B — Scored / Renderable Commit

Commit B is the hourly enrichment checkpoint. It can contain scoring manifests for many Commit-A tokens.

Each scored token becomes renderable as a project package. Its package can include:

```text
token/
├── index.html
├── token.json
├── source.json
├── lineage.json
├── scores.json
├── research/
│   ├── infinity-random-work.json
│   └── project-research.json
├── ai/
│   ├── workspace.json
│   ├── suggestions.json
│   └── query-context.json
└── render/
    ├── palette.json
    └── audience-rules.json
```

`index.html` is the presentation shell. The factual token record remains in the structured data.

## Why Two Commits

The source commit establishes the historical event.

The scoring commit establishes the first enriched/renderable state.

Further AI notes, user-specific views, query sessions, research packets, and tentative relationships can be stored in the ledger/database without generating Git commits on every change. A later Git commit is made only when there is a meaningful checkpoint, actual source change, or scheduled batch snapshot.

This prevents this failure mode:

```text
commit -> token -> ledger commit -> token -> ledger commit -> token -> ...
```

and replaces it with:

```text
SOURCE COMMITS DURING HOUR
            |
            v
      hourly watcher
            |
            v
ONE SCORING CHECKPOINT COMMIT
            |
            v
persistent token research + personalized rendering
```

The scoring checkpoint itself can still be ledgered. It receives lineage role `DERIVED_RECURSIVE`, but administrative/scoring commits do not trigger immediate scoring commits of their own. They wait for the next hourly batch and can be summarized into that batch if useful.

## Living Token / Revival

A token can become active again without rewriting its source commit.

Example:

```text
Token A — dormant sapphire project
   |
   | AI discovers compatible newer work
   v
personalized suggestion
   |
   | user chooses Continue / Revive
   v
new project commit
   |
   v
Token C
relationship: REVIVES_TOKEN -> Token A
```

The original token remains unchanged. The new token inherits selected research, dependencies, and lineage references through explicit relationships rather than history rewriting.

## Two Research Streams Per Token

Every scored token receives two distinct research streams.

### 1. Project Research

Research tied directly to the commit and project:

- what changed
- why the change appears to have been made
- related older and newer commits
- relevant technical background
- external references where appropriate
- missing components
- reusable components
- experiments/tests/results
- contradictions or uncertainty

Every statement should carry one of the evidence labels:

- `OBSERVED`
- `INFERRED`
- `EXTERNALLY_VERIFIED`
- `USER_DEFINED`

### 2. Infinity Random Work

One intentionally cross-domain Infinity work item is attached to the token. Its purpose is exploration, not factual proof of a connection.

The algorithm can select a distant token, concept, visual, dataset, UI component, material property, media project, or code pattern and ask whether the connection produces anything useful.

The random selection must be labeled `EXPLORATORY_LINK` unless a later analysis establishes a stronger relationship.

This supplies controlled serendipity without converting coincidence into evidence.

## AI Robot Workspace

Every token exposes a robot/AI query interface. The AI receives a structured context package instead of only the README:

- source commit
- project files/index
- project research
- random Infinity work
- lineage graph
- dependencies
- known tests/results
- related tokens
- user-visible build suggestions

The robot can answer questions and propose work inside the token's project universe. When it wants to incorporate another token, it records a proposed relationship first. Accepted work creates a normal source commit and therefore a new token.

## Personalized Rendering

The same source token can render differently for different users while retaining the same underlying facts.

A user profile may include only legitimately available, relevant signals such as:

- explicitly supplied interests
- explicitly supplied skills
- explicitly supplied education/training
- repositories/projects the user works on
- token categories the user opens or saves
- languages/tools they use
- explicit follows/subscriptions
- prior accepted build suggestions

Sensitive traits should not be inferred for targeting.

The personalization engine can alter:

- ordering
- highlighted research
- recommended next actions
- complexity/detail level
- examples
- related-token suggestions
- palette accents/status emphasis

It does **not** alter historical commit facts.

Thus Kris and Joe can receive different views of the same token because their project contexts differ. Someone whose explicit work is plumbing can receive plumbing-relevant build opportunities; someone working on electronics can receive electronics-relevant opportunities. The underlying token remains one provenance object.

## Color Model

Color conveys state at a glance. Store semantic values rather than hard-coding presentation:

- subsystem color
- lifecycle color/state
- evidence-confidence indicator
- activity/build-readiness indicator
- personalized highlight accent

The final renderer combines those layers. Two users may therefore see different accent emphasis while the token's canonical subsystem/status colors remain stable.

## AI Provocation

The preferred behavior is a useful invitation, not manipulation.

A recommendation should explain the concrete reason for showing the token:

```text
You already work on Oxide-Electron-Pump.
This older token contains an unfinished oxygen-interface model.
Two of its three dependencies now exist.
Suggested next step: connect the interface simulator.
```

Every suggestion should expose the evidence/reasoning inputs that led to the match and provide dismiss/save/continue controls.

## Core Rule

**One historical token, many evolving knowledge layers, many personalized views, and new immutable tokens whenever real project work creates new commits.**
