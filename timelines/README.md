# Timelines — AI Search Realms for the Infinity Token Ledger

Timelines is a side project inside Infinity for asking fast questions across large histories of tokens, projects, commits, research, media, people, places, objects, and interactions. It is designed as a quick AI search realm: pick a timeline or symbol realm, ask a question, and get a compact answer backed by the token ledger and its research history.

Timelines does not replace the Living Token system. It is a lens over it.

## Core idea

A token may begin as a compact four-brick identity and unfold into a much richer symbolic ledger. The four-brick display stays fast and recognizable, while the expanded token can expose a vocabulary of roughly 100 high-level symbols. Each symbol represents a realm with potentially millions of underlying records.

Example compact token:

```text
Token ID   🧱 🧱 🧱 🧱
Value      🧱 🧱 🧱 🧱
Category   rendered by color/profile
Date       birth date + interaction account
```

Expanded symbolic ledger:

```text
⭐  Star / unlocked Star-family key
📷  Images / photography / visual assets
♦️  Merchant / commerce / business
💎  Gemstones / minerals / material assets
🌎  World / geography / location
😎  Cool / style / high-interest discovery
🔧  Tools / engineering tools / equipment
🎟️  Tickets / access / events / entitlement
✨  Multi-star / multi-project constellation
🎬  Movies / video / cinema
```

The symbol is not the record itself. It is an index key into the relevant realm.

## Symbols are keys, not decoration

A symbol can summarize an enormous data set. For example, `🎟️` can represent one ticket, an event series, access rights, venue history, ticket-linked research, or millions of ticket positions. `🎬` can point to a single movie token or an entire media catalog. `⭐` can represent the specific Star-related project, product, or unlocked connection relevant to the current token and user.

When a user activates a jump link, the associated symbol becomes visibly unlocked in that user's token view. The canonical token identity does not change. The viewer now has an observed relationship to that realm.

## Canonical meaning + personal meaning

Each symbol has a stable system-level definition, but its ranking, wording, visible connections, and suggested actions are personalized.

Example:

- Canonical `🔧` meaning: tools, equipment, engineering utilities, build aids.
- For a mechanic: torque tools, diagnostics, repair tokens.
- For a software engineer: compilers, scripts, APIs, debugging tools.
- For a plumber: cutters, pumps, valves, pressure tools.

The user's profile and interaction history determine which part of the realm is rendered first.

## Timelines as AI search realms

Users can ask questions such as:

- What happened to this project between its first and latest token?
- Show every Green engineering action that led to this build.
- What images were attached before this token became active?
- Show the merchant history for this product.
- Which gemstone/material tokens were imported into this design?
- Which movie tokens connect to this song or research thread?
- Show every Red route that was considered but not selected.
- What did the user research immediately before making this Orange decision?
- Which Star key unlocked this project?

The AI should search the smallest relevant realm first, then expand outward only when needed.

## Timeline types

Timelines can represent many kinds of history:

1. **Commit timeline** — source commits and descendant Commit Tokens.
2. **Interaction timeline** — jump links, views, saves, imports, research, decisions, routes, assimilation and engineering events.
3. **Research timeline** — Project Research and Infinity Discovery Research revisions.
4. **Project timeline** — creation, dormancy, revival, repurposing, build-ready and built states.
5. **Asset timeline** — images, songs, movies, documents, cards, signatures and other attached media.
6. **Value timeline** — canonical base value plus clearly separated calculated/display metrics.
7. **Symbol timeline** — when each realm/key was first unlocked and how it accumulated connections.
8. **People/account timeline** — only authorized/account-visible activity relevant to the token.
9. **Location/world timeline** — geography and location-linked token events.
10. **Decision timeline** — Yellow evidence → Orange decision → Red routes → chosen descendant work.

## Color + symbol interaction

Colors describe the user's current intent. Symbols describe the realm/object being acted on.

Examples:

```text
GREEN + 🔧 = engineer using a tool-related token
BLUE  + 🎬 = import movie/video material into the current token
YELLOW + 💎 = research/extract gemstone or material information
ORANGE + ♦️ = make a business/merchant decision using accumulated evidence
RED + 🌎 = inspect alternate geographic/world routes
PURPLE + ⭐ = assimilate multiple Star-family paths into a broader project
```

This creates a compact grammar without requiring huge menus.

## Unlock model

A symbol has viewer-specific states:

```text
HIDDEN → VISIBLE → UNLOCKED → ACTIVE → CONNECTED
```

- **HIDDEN** — no current reason to render it.
- **VISIBLE** — profile algorithm predicts relevance.
- **UNLOCKED** — user activated a qualifying jump/action.
- **ACTIVE** — research or interaction is accumulating in that realm.
- **CONNECTED** — the realm has supported a durable token-to-token relationship or project result.

Unlocking never changes the underlying token hash.

## Rough 100-symbol vocabulary

The registry should grow toward roughly 100 symbols, grouped into broad namespaces rather than being an arbitrary emoji list. Initial groups:

- media and creative
- engineering and fabrication
- commerce and value
- science and materials
- people and organizations
- geography and world
- access and events
- software and data
- research and evidence
- routes, decisions and lineage
- collections and rarity
- communication and social
- health/wellness only when explicitly user-controlled and appropriate
- education and skills
- environment and nature

Every symbol record should contain:

```json
{
  "symbol": "🔧",
  "key": "TOOL",
  "canonical_definition": "Tools, equipment and build utilities",
  "namespace": "ENGINEERING",
  "allowed_colors": ["GREEN", "BLUE", "YELLOW", "ORANGE", "RED", "PURPLE"],
  "unlock_events": ["JUMP_LINK", "TOKEN_OPENED", "ENGINEER", "IMPORT"],
  "viewer_specific": true,
  "version": 1
}
```

## AI learning

The AI may learn how a user interprets a symbol from explicit profile data and observed Infinity interactions. It should preserve the canonical definition underneath and store personalized interpretation separately.

Example:

```text
Canonical ⭐: Star-family / starred-key realm
Viewer A: StarCraft product work
Viewer B: astronomy research
Viewer C: favorite/starred projects
```

The UI should explain why a particular interpretation was selected and allow the user to correct it.

## Fast query architecture

Timelines should use indexed event tables instead of repeatedly rereading every README. Suggested query path:

```text
question
  ↓
identify token(s)
  ↓
identify symbol realm(s)
  ↓
identify color/intent
  ↓
query indexed timeline events
  ↓
retrieve linked research only where needed
  ↓
AI synthesis with evidence labels
```

This keeps common questions fast even when the ledger reaches millions of tokens and interactions.

## Evidence

All Timeline answers preserve the existing evidence states:

- `OBSERVED`
- `INFERRED`
- `EXTERNALLY_VERIFIED`
- `USER_DEFINED`

A personalized emoji interpretation is not automatically a factual claim about the outside world.

## Relationship to the four-hash token system

The four hashes are the compact cryptographic envelope. The symbol ledger is its expandable semantic interface.

```text
FOUR-HASH TOKEN
   ↓ unfold
SYMBOL LEDGER (~100 realm keys)
   ↓ user unlocks a key
TIMELINE + RESEARCH + ACTIONS
   ↓
NEW RELATIONSHIPS / PROJECT WORK
   ↓
real change → new Commit Token
```

This preserves bulk-token speed while allowing any token to become extremely deep only when somebody actually uses it.
