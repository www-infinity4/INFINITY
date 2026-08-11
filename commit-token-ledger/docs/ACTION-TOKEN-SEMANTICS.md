# Infinity Action Tokens and Hourly Scoring

## Purpose

Infinity distinguishes between two token classes:

1. **Commit Tokens** — hard provenance records anchored to a Git commit SHA. They provide the immutable database identity for source/project history.
2. **Action Tokens** — high-volume interaction events generated when a user navigates, combines, imports, researches, decides, repairs, or engineers across Living Tokens.

Action Tokens do **not** create a Git commit one-for-one. They are recorded immediately in the live ledger, accumulated during the hour, and summarized into a single hourly scoring/checkpoint commit. This keeps the interaction graph detailed without creating hundreds or thousands of recursive Git commits.

## Action Path as Research

A user's path through tokens is itself useful structured evidence. If a user moves:

`A -> B -> C -> D`

the system retains:

- the source token for each step;
- the destination token;
- the selected color/action lane;
- timestamp and session;
- what capability, information, decision, repair, or engineering relationship was requested;
- profile state/version used when the destination was rendered;
- later project commits that resulted from the path.

The research writer can then analyze the whole path rather than isolated clicks. It may create a derived research record explaining how content from A and B was combined, what C contributed, and why the user continued to D. Interpretations must remain distinguishable from observed click facts.

## Color/Action Semantics

### Green — ENGINEER

`ENGINEER(A, B)` means the user is asking the system to use relevant content/capability from B to advance or construct A.

Expected output may include:

- a proposed integration;
- a new design or build plan;
- missing-component resolution;
- code/design changes;
- links to additional engineering tokens.

A later real project change creates a normal Git commit and therefore a new Commit Token. The green click itself remains an Action Token.

### Blue — IMPORT

`IMPORT(A, B)` means B contains a form, component, dependency, data structure, method, interface, or other capability that A lacks and appears to need.

The renderer should show what is proposed for import and why it fills a gap. It must not silently mutate A. A user or authorized agent accepts/edits the import, and any resulting source change is captured as a later Commit Token.

### Yellow — RESEARCH / EXTRACT

`RESEARCH(A, B)` means the user is following B to obtain information useful for understanding, validating, expanding, or questioning A.

The system extracts a research packet that can contain:

- observed project facts;
- external sources when available;
- claims/evidence status;
- questions opened or answered;
- reusable information returned to A.

### Orange — DECIDE

`DECIDE(A, B)` creates a decision point. B represents an option, constraint, business choice, tradeoff, review item, or action requiring user judgment.

Decision records should capture alternatives and rationale without treating a click alone as final approval unless the user explicitly confirms a choice.

### Purple — ASSIMILATE

`ASSIMILATE(A, B)` asks the system to synthesize A and B at a broader architectural/conceptual level. It is used when B is not merely a missing import but can become part of A's larger system or knowledge universe.

### Red — REPAIR

`REPAIR(A, B)` means B is relevant to correcting, reconciling, securing, debugging, or restoring A. The record should identify the detected problem separately from the proposed fix.

## Hourly Batch

During an hour, a user may create hundreds of Action Tokens. The hourly scorer groups them into a checkpoint containing:

- event count by lane;
- unique source/destination tokens;
- ordered paths and repeated paths;
- strongest newly observed relationships;
- profile features reinforced or weakened;
- research packets created;
- unresolved decision points;
- imports/engineering proposals awaiting acceptance;
- real Commit Tokens created during the same interval.

One hourly Git commit may persist the aggregate scoring/report for many users and many actions. The underlying Action Token events remain individually addressable in the live ledger.

## Canonical vs Personalized

A click records an observed relationship request. Its rendered meaning depends on the user's profile and the token view shown at that moment. Therefore every Action Token stores the profile/render version used for the click.

This makes personalization reproducible: two users may click the same canonical token ID and receive different names, lane rankings, jump links, and suggested relationships while the underlying Git provenance remains unchanged.

## Evidence Levels

- `OBSERVED`: click, lane, source token, destination token, time, profile/render version.
- `INFERRED`: why the user followed that path; why two projects may fit together.
- `USER_DEFINED`: user-entered skills, interests, meanings, classifications, or explicit intent.
- `EXTERNALLY_VERIFIED`: claims supported by external research sources.

The AI research writer must keep these categories separate.