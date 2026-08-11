# Personalized Token Scoring and Wallet Feeds

## Principle

The canonical token describes the project. The personalized token view describes why that project is useful to a particular user.

Those are separate objects.

```text
canonical token + user relevance profile -> personalized render manifest
```

A personalized manifest may change frequently without changing the underlying commit token.

## Hourly Batch Scoring

Once per hour, the account watcher gathers all newly observed source commits plus meaningful changes to existing token research and lineage.

One scoring run creates or updates:

- canonical token scores
- semantic subsystem tags
- lifecycle state
- lineage relationships
- project research queue state
- one exploratory Infinity-work relationship
- user-match feature vectors

The run should produce **one Git checkpoint for the whole scoring batch**, not one commit per token and not one commit per user.

User-specific render manifests belong in the live data store/cache and do not require Git commits.

## Canonical Token Score

Suggested canonical fields:

```json
{
  "token_id": "ICT-...",
  "source_sha": "...",
  "subsystems": ["ATOMIC_MATERIALS"],
  "lifecycle": "DORMANT",
  "build_readiness": 74,
  "research_completeness": 61,
  "lineage_confidence": 0.88,
  "dependencies_ready": 0.67,
  "evidence_distribution": {
    "OBSERVED": 14,
    "INFERRED": 5,
    "EXTERNALLY_VERIFIED": 8,
    "USER_DEFINED": 3
  }
}
```

## User Relevance Profile

Use transparent, legitimate signals. Examples:

```json
{
  "user_id": "local-user-id",
  "explicit_interests": ["electronics", "materials"],
  "explicit_skills": ["web-development"],
  "explicit_training": [],
  "active_projects": ["Oxide-Electron-Pump"],
  "opened_categories": ["ATOMIC_MATERIALS", "FABRICATION"],
  "saved_tokens": [],
  "accepted_suggestions": []
}
```

Do not infer sensitive characteristics for targeting. Profiles should be inspectable and editable by the user.

## Relevance Formula

A starting scoring model can be transparent rather than mysterious:

```text
relevance =
  0.25 * active_project_overlap
+ 0.20 * explicit_interest_overlap
+ 0.15 * explicit_skill_overlap
+ 0.10 * tool_language_overlap
+ 0.10 * prior_token_engagement
+ 0.10 * dependency_opportunity
+ 0.10 * controlled_serendipity
```

Weights can later adapt, but the system should retain an explanation of why a token was surfaced.

## Different Users, Same Token

Example canonical project:

```text
Token X: old building-fluid-control project
```

For a user with explicitly stated plumbing experience:

- emphasize valves, fluid routing, pressure-control research, installation constraints
- recommend related fluid-system tokens
- show implementation-oriented next steps

For a user working primarily on electronics:

- emphasize sensors, controllers, power, telemetry, simulation interfaces
- recommend circuit and embedded-control tokens
- de-emphasize trade-specific installation work

The commit facts stay identical.

## Color Coding

Canonical colors communicate project facts:

- subsystem family
- lifecycle state
- confidence/evidence
- build readiness

Personalized accent communicates relevance to the current viewer.

Recommended semantic states:

```text
NEW            source commit recently observed
SCORED         first enrichment checkpoint complete
ACTIVE         current descendant work exists
DORMANT        no meaningful descendant activity recently
REVIVABLE      missing pieces now appear available
REVIVED        a newer token explicitly continues it
DERIVED        produced by research/ledger/tooling work
BLOCKED        important dependencies unresolved
```

The UI should not depend on color alone; always pair color with text/icons for accessibility.

## AI Prompting / Product Provocation

The AI should surface actionable opportunities, not generic engagement bait.

A suggestion consists of:

1. **Why you:** user-project/skill/interest match.
2. **Why now:** new dependency, related token, research result, or newly available component.
3. **What remains:** small explicit gap list.
4. **What happens next:** concrete safe action such as inspect, simulate, compare, draft, code, test, or connect.
5. **Evidence:** why the relationship was proposed.

Example:

```text
Why you:
You are already working on the controller used by this older token.

Why now:
Two previously missing dependencies have new implementations.

Remaining:
- adapter schema
- integration test

Suggested action:
Generate an adapter branch and run the compatibility test.
```

Users must be able to dismiss a suggestion and reduce future matching for that topic.

## Token Robot

Each token gets a query workspace whose system context is assembled from:

- immutable source commit
- scored metadata
- current project files
- two research streams
- lineage graph
- connected-token summaries
- user relevance profile (only fields allowed for recommendation)
- prior token workspace state for that user

The workspace can explore its own token universe, but proposed edits become real project changes only after going through the normal repository/commit workflow.

## Token-to-Token Incorporation

The algorithm can propose another token as a component using typed edges:

- `USES_COMPONENT`
- `REVIVES_TOKEN`
- `CONTINUES_TOKEN`
- `REPURPOSES_TOKEN`
- `RESEARCHES_TOKEN`
- `DOCUMENTS_TOKEN`
- `IMPLEMENTS_TOKEN`
- `ALTERNATIVE_TO`
- `EXPLORATORY_LINK`

A proposed relationship remains inferred until accepted or verified. Incorporation never deletes the history of either token.

## Rendering Contract

Each wallet render receives two payloads:

```json
{
  "canonical": { "...": "same for all users" },
  "view": { "...": "personalized for this user" }
}
```

This is how two users can receive entirely different useful presentations of one token while the ledger remains coherent.
