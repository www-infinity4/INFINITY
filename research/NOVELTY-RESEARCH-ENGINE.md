# Infinity Novelty Research Engine

## Goal

Every research-generating action should create a genuinely new research assignment while remaining grounded in real sources. "New" means the research seed, combination, framing, comparison, or unresolved question is not a duplicate of prior work for that user/token/source. It does **not** mean inventing evidence.

## Two research streams remain mandatory

1. **PROJECT_RESEARCH** — directly advances the token/project at hand.
2. **INFINITY_DISCOVERY_RESEARCH** — introduces a controlled cross-domain subject, older token, newer token, external field, material, method, historical comparison, or application that may reveal a useful connection.

Both streams are versioned and stored. They are inputs to the user profile, Living Token renderer, Timelines, color-action plans, and future research selection.

## Combinatorial "quantum logic"

The software model uses a superposition-like search metaphor: assemble many candidate combinations, score them, exclude previously exhausted states, and collapse the candidate set to one research plan for this action.

Candidate dimensions include:

- current token title, README terms and changed files;
- user's optional keywords/question;
- explicit profile skills/interests/projects;
- recently opened or connected tokens;
- prior Green/Blue/Yellow/Orange/Red/Purple paths;
- unresolved questions in Project Research;
- imported components and missing capabilities;
- random-but-controlled Infinity Discovery realm;
- a rotating external discipline/method/material/history term;
- time/date context;
- symbols unlocked in the token realm;
- prior search terms, titles, abstracts and article fingerprints.

A candidate seed can be represented as:

```text
seed = H(
  source_token
  + user_profile_version
  + action_event
  + chosen_terms
  + discovery_realm
  + novelty_nonce
)
```

The seed is reproducible for auditing but the selected term set changes because the history/exclusion set changes.

## Novelty requirements

Before research starts, compare the candidate against the research library.

Reject or mutate a candidate when:

- normalized query fingerprint already exists;
- title similarity is above the configured threshold;
- selected source-token pair has already used the same relationship framing;
- the same keyword tuple has already been researched;
- semantic summary is materially duplicative;
- discovery realm has appeared too frequently in the user's recent window.

Then rotate one or more dimensions and score again.

## Research fingerprint

Each job stores:

```json
{
  "query_terms": [],
  "normalized_terms": [],
  "source_token_ids": [],
  "relationship": "PROJECT|EXPLORATORY_LINK|IMPORT|ENGINEER|ROUTE|DECIDE|ASSIMILATE",
  "profile_version": 0,
  "discovery_realm": "",
  "query_hash": "sha256",
  "source_set_hash": "sha256",
  "article_hash": "sha256",
  "created_at": ""
}
```

`query_hash` stops identical assignments. `source_set_hash` catches the same evidence package. `article_hash` catches identical final output.

## Source integrity

Novelty is applied to the **question and synthesis**, never to facts.

- Retrieve real scholarly/public records from configured research providers.
- Deduplicate DOI/title/source records.
- Mark metadata-only, abstract-only and full-text evidence distinctly.
- Never invent authors, papers, DOIs, quotes, experiments or results.
- External claims only become `EXTERNALLY_VERIFIED` when sources support them.
- User theories stay `USER_DEFINED` or `INFERRED` as appropriate.

## Article pipeline

```text
ACTION/SPIN
   ↓
collect context
   ↓
generate 16-64 candidate term combinations
   ↓
novelty filter against full research history
   ↓
score candidates for relevance + distance + usefulness
   ↓
select one PROJECT_RESEARCH plan
   ↓
select one DISCOVERY_RESEARCH plan
   ↓
retrieve evidence
   ↓
synthesize new article/brief
   ↓
hash + compare final output
   ↓
if duplicate → reframe and regenerate
   ↓
store sources + article + token relationships
```

## Scoring sketch

```text
score =
  0.30 * profile_relevance
+ 0.25 * project_relevance
+ 0.15 * unresolved_need
+ 0.15 * cross_domain_distance
+ 0.10 * token_graph_opportunity
+ 0.05 * recency_bonus
- duplicate_penalty
- realm_saturation_penalty
```

High cross-domain distance is useful only when there remains a plausible bridge to the user's project. Pure randomness stays exploratory and should not be represented as established causation.

## Optional input rule

Research-producing games/apps must never require a user to type before the primary action works. Optional input increases steering weight:

```text
if optional_input:
    user_terms_weight += 0.35
else:
    infer seed from token + profile + history + discovery rotation
```

This is particularly important for Bitcoin Crusher: Spin remains one tap; `Add research direction` is optional.

## Color feedback

New research immediately feeds the color/action planner:

- **Yellow** extracts new evidence/knowledge.
- **Orange** consumes Yellow evidence to form a decision plan.
- **Blue** identifies a missing form/component/source to import.
- **Green** proposes engineering A with B.
- **Red** presents multiple routes/forks.
- **Purple** combines Blue imports with Red routes into a broader assimilation.

The clicked anchor phrase, user profile version, related token and research version are stored so the next research job can avoid repeating the same path and intentionally explore the next useful state.

## Daily pre-building

The same engine can run without active users to grow the dormant token library. Background jobs should use system profiles/real repository history and store results as BRICKED/SEEDED research until a user profile renders and unlocks them. User-facing recommendations remain profile-conditioned later.
