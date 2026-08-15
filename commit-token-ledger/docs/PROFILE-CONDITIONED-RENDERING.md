# Profile-Conditioned Living Token Rendering

## Core Rule

Infinity Commit Tokens have one canonical historical identity but are rendered late for each user. The commit SHA, repository, parent commits, observed diff, timestamps, evidence and canonical research are shared facts. The token name shown to a person, color lane, ranking, related-token links, AI prompt, suggested continuation and research emphasis are generated at view time from that person's evolving profile.

The model is intentionally similar to an electron cloud as a visualization metaphor: the canonical token is the stable underlying object, while the rendered arrangement is a probability/ranking field conditioned by the viewer. This does not require quantum-computing hardware.

## User Profile Is the Routing Key

A profile grows from two sources:

1. Explicit profile data supplied by the user: interests, skills, education/training, professions, tools, certifications, current projects, goals, preferred domains, topics to avoid, accessibility needs and preferred depth.
2. Consented behavioral signals: tokens opened, saved, dismissed, continued, connected, researched, searched, edited or built from; time spent in lanes; accepted/rejected AI suggestions; repo languages and project categories the user actively works with.

Do not silently infer sensitive traits. Profile fields are explainable, editable and removable. Behavioral signals should record their source and confidence.

## Late-Bound Token Naming

A token has a canonical ID and canonical project title. It may also receive a `viewer_title` generated when rendered.

Example:

- canonical: `ICT-www-infinity4-Oxide-Electron-Pump-<sha>`
- engineer view: `Oxide Charge Transfer Controller`
- fabrication view: `Pump Interface Fabrication Block`
- materials view: `Oxide Transport Research Node`

These names do not create new canonical tokens. They are user-specific aliases tied to the same provenance.

## Color Lanes

The initial navigation model uses stable lane colors while relevance within each lane is personalized.

- GREEN — Engineering / build / fabrication / implementation
- PURPLE — Assimilation / synthesis / cross-token connection / systems integration
- BLUE — Import / ingestion / external source / dependency / data brought into the user's working universe
- YELLOW — Research / analysis / evidence / questions
- ORANGE — Decision / review / unresolved choice / next action
- RED — Repair / reroute / conflict / security attention

Colors are routing semantics, not scientific claims. A token may qualify for several lanes. The user profile determines which lane is primary for that viewer and which jump-links appear inside it.

## Personalized Lane Query

When a person selects a lane, the renderer runs a profile-conditioned ranking over canonical tokens.

Conceptually:

`rank(token, user, lane) = domain_fit + skill_fit + active_project_fit + lineage_fit + interaction_fit + novelty + readiness - fatigue - mismatch`

The returned set is different for each viewer even when the source ledger is identical.

An engineer does not automatically receive plumbing projects just because they are tagged Engineering. A plumber, controls engineer and materials engineer can all select GREEN and receive different token clouds because their skill vectors, current projects and prior actions differ.

## Jump Links Grow With the User

Each token can display profile-conditioned jump links such as:

- Continue with
- Import from
- Assimilate with
- Research next
- Repair using
- Earlier version
- Descendant version
- Missing component
- Similar skill match
- Build-ready companion

The canonical relationship graph supplies possible links. The user model chooses which links to surface, their color, order and explanation. User actions can strengthen or weaken these edges for that person's future rendering without falsifying the canonical relationship graph.

## Daily Profile Growth

Every session can update the profile through explicit answers and consented actions. The profile is versioned rather than overwritten so the recommendation engine can explain why a token began appearing or stopped appearing.

Suggested profile event schema:

- `PROFILE_FIELD_ADDED`
- `PROFILE_FIELD_UPDATED`
- `TOKEN_OPENED`
- `TOKEN_SAVED`
- `TOKEN_DISMISSED`
- `TOKEN_CONTINUED`
- `TOKEN_CONNECTED`
- `SUGGESTION_ACCEPTED`
- `SUGGESTION_REJECTED`
- `SEARCH_PERFORMED`
- `LANE_SELECTED`

A periodic compactor converts events into weighted profile features while retaining provenance.

## Rendering Pipeline

1. Load canonical token record.
2. Load canonical research and lineage.
3. Load the viewer's current profile snapshot.
4. Compute lane scores.
5. Generate viewer-specific title/summary.
6. Rank related tokens and jump links.
7. Select color lane and secondary color accents.
8. Generate a concise AI build/query prompt explaining relevance.
9. Render `index.html`/wallet view.
10. Record only consented interaction events back to the profile.

## Canonical vs Personalized Data

Never put viewer-specific interpretations into the immutable commit facts.

Canonical:
- commit SHA
- repo and branch provenance
- observed diff
- source files
- canonical categories
- evidence-backed research
- token lineage

Personalized:
- viewer title
- lane score
- chosen primary color
- ranking
- recommended jump links
- AI prompt
- relevance explanation
- display density/depth

## AI Inside the Token

The token AI receives the canonical token context plus a scoped viewer profile. It acts as a project query/workspace assistant. It can answer what remains, what can be reused, which tokens connect, what research conflicts, and what next build is suitable for this user.

The AI should always distinguish:
- OBSERVED facts
- EXTERNALLY_VERIFIED research
- INFERRED relationships
- USER_DEFINED concepts
- PERSONALIZED recommendations

## Two-Commit Compatibility

This model preserves the bounded two-commit design:

- Commit A creates the source token.
- Hourly scoring/checkpoint work may create Commit B for the batch.
- Viewer-specific rankings and daily profile changes stay in the live data layer and do not create Git commits for every interaction.
- A new Git commit occurs when somebody actually changes a project or when a meaningful batched checkpoint is intentionally written.

This keeps personalization alive without creating recursive Git noise.
