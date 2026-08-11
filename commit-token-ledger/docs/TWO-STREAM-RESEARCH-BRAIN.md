# Infinity Two-Stream Research Brain

## Purpose

Every Infinity Commit Token carries two continuously extensible research streams. The streams are not just prompts describing what ought to be researched. They are durable knowledge records that can be rewritten into user-facing documentation while preserving provenance and evidence state.

The canonical Commit Token remains immutable. Research is append-only/versioned around it.

## Stream A — PROJECT_RESEARCH

This stream stays centered on the token/project itself.

It should accumulate:

- what the source commit changed;
- why the change was made when the commit/documentation states a reason;
- file and architecture summaries;
- parent/descendant token relationships;
- dependencies and reusable components;
- known facts and cited external sources;
- hypotheses and user-defined interpretations clearly separated from verified facts;
- missing pieces;
- tests, experiments, validation status and failures;
- alternative routes;
- build-readiness assessment;
- suggested next work.

Research versions never overwrite the original commit record. A later research pass may correct an earlier annotation while retaining both versions and the reason for the correction.

## Stream B — INFINITY_DISCOVERY_RESEARCH

This stream intentionally explores the larger Infinity corpus instead of remaining confined to the source project.

The generator selects material from another token, subsystem, document, research record or externally verified subject. Selection combines controlled randomness, semantic novelty, the current user's interests and skills when available, under-connected areas of the token graph, evidence quality, and previous selections so the library does not simply repeat itself.

A random selection is never automatically asserted to be related. It begins as `EXPLORATORY_LINK`. Research then asks whether a defensible relationship exists. If supported, it can graduate into relationships such as `SUPPLIES_COMPONENT`, `IMPORTS_CAPABILITY`, `SHARES_METHOD`, `RESEARCH_SUPPORTS`, `ALTERNATIVE_ROUTE`, `ASSIMILATES_WITH`, or `ENGINEERS_WITH`.

The purpose is to continually build a cross-project research library and expose combinations a user or AI may not have searched for directly.

## The Brain

The two streams feed a token knowledge graph. The AI reasons over:

`commit facts + project research + discovery research + token lineage + action-token paths + user profile + evidence state`

This graph becomes working memory used when a token is rendered or queried.

The AI may have an intent such as `RESEARCH`, `ENGINEER`, `IMPORT`, `ASSIMILATE`, `DECIDE`, or `ROUTE`, but an intent is an operation request, not permission to falsify facts or silently modify a project.

## Reframed Documentation

The rendered README/article is a view, not the database of record. For each viewer the documentation engine may choose a viewer-specific title, reorder sections, surface different research, explain unfamiliar prerequisites, emphasize pieces matching the user's skills, add profile-specific jump links, and suggest a build plan appropriate for that person.

The renderer must preserve canonical token ID, source commit SHA, evidence labels, and source citations. Personalization cannot rewrite historical facts.

## Color Action Grammar

The renderer scans candidate concepts, sections and token relationships and assigns actions using the viewer profile.

### Green — ENGINEER

`ENGINEER(A, B)` — Use B to build, modify or advance A. A green jump opens a base plan showing what from B can be applied to A, files/components involved, assumptions, tests and the expected project change.

### Blue — IMPORT

`IMPORT(A, B)` — B contains a form, component, interface, dataset, method or capability A lacks. The blue jump explains the missing capability and proposes a mapping into A.

### Yellow — RESEARCH / EXTRACT

`RESEARCH(A, B)` — Extract information from B to understand, verify or enrich A. Yellow is the evidence/input layer and can feed later Orange decisions.

### Orange — DECIDE

`DECIDE(A, {B,C,...})` — A decision state produced from evidence, often including Yellow research. Orange presents alternatives, evidence, tradeoffs, unknowns and the next evaluation.

### Red — ROUTE / FORK

`ROUTE(A, {B,C,...})` — Expose two or more legitimate paths away from the current state. Red preserves all routes and can model legacy preservation, modernization, replacement, alternate architectures and predicted obsolescence. Claims of intentional planned obsolescence require evidence of intent.

### Purple — ASSIMILATE

`ASSIMILATE(A, {B,C,...})` — Higher-order synthesis. Purple commonly uses Blue import candidates plus Red alternate routes, allowing the user/AI to combine logic, material and projects into a broader architecture. It retains which pieces originate in which tokens.

## Profile-conditioned rendering

A canonical token is not permanently Green, Blue, Yellow, Orange, Red or Purple. Lane scores are calculated for the viewer at render time. The same token may be Green for a user whose skills make it buildable, Blue for a user whose project needs one of its components, Yellow for a user researching it, Orange for a business owner facing a choice, Red where it presents multiple replacement routes, or Purple where it can assimilate multiple active projects.

The profile can grow from explicit user-provided information and consented interaction events. Profile-derived labels must remain inspectable, editable and explainable.

## Hourly checkpointing

Research and Action Tokens can change rapidly without producing a Git commit for every update. During the hour, action clicks are ledgered, research records are appended/versioned, relationships are scored, profile evidence is updated and render candidates are recalculated.

The hourly checkpoint can summarize those changes into one durable Git commit/report. A real source-code/project modification still gets its own ordinary Git commit and therefore its own Commit Token.

## Evidence model

All generated content carries one of the existing evidence states:

- `OBSERVED` — direct Git/file/action facts;
- `INFERRED` — model interpretation supported by recorded inputs;
- `EXTERNALLY_VERIFIED` — factual outside research with recorded sources;
- `USER_DEFINED` — terminology, taxonomy, goals or project theory supplied by the user.

A research writer must never turn `INFERRED` or `USER_DEFINED` content into `EXTERNALLY_VERIFIED` merely by rewriting it.