# Infinity Research Memory Protocol

## Goal

Infinity applications should retrieve the smallest trustworthy packet of knowledge needed for the current action while preserving a verifiable path back to the complete source.

## Three-layer memory

### 1. Source Vault

Stores the complete article, dataset, diagram, transcript, or approved project document in content-addressed storage. Every version receives a cryptographic content hash.

### 2. Knowledge Grain

A compact, structured record derived from a source. It contains:

- grain ID and schema version
- source hash and citation
- title, entities, dates, and categories
- concise claims and supporting passages
- established, experimental, theoretical, or speculative status
- safety and licensing flags
- related robots, tools, applications, and realms
- retrieval keywords and semantic index reference
- creation and validation history

### 3. Context Packet

A temporary packet assembled for a specific user-approved task. It contains only the relevant grains, instructions, and permissions required by the robot or application.

## Interaction flow

```text
User intent or application action
        ↓
Privacy and consent check
        ↓
Retrieve matching knowledge grains
        ↓
Verify source hashes and permissions
        ↓
Assemble a limited context packet
        ↓
Robot, assistant, or builder performs work
        ↓
Validate output and record provenance
        ↓
Optional new grain or world connection
```

## Click and activity handling

Searches, opens, refreshes, spins, saves, edits, and publishes may create different event strengths. They do not all become equal research facts.

- refresh or accidental click: temporary, low-confidence signal
- search: explicit query signal
- repeated exploration: session-level interest
- save or collection: persistent user-approved preference
- edit or build: productive action candidate
- validation or publication: permanent provenance event

Raw activity remains private by default. Robots receive derived context only when the application purpose and user controls allow it.

## Compact codes

Infinity may use compact symbols or tokens, but each code must resolve through a versioned registry.

Example:

```json
{
  "code": "^42",
  "namespace": "infinity-research",
  "version": "1.0",
  "meaning": "television-era recommendation context packet",
  "expansionHash": "sha256:<hash>",
  "schema": "context-packet/v1"
}
```

The code is an address and verified instruction, not magical compression. The full expansion or reproducible generation method must remain available to authorized services.

## Hash-linked synthesis

New work may cite many source hashes. A synthesis record contains:

- input source hashes
- retrieval query and filters
- model or algorithm version
- output hash
- factuality and safety review status
- human corrections
- links to resulting applications, pages, or robot instructions

This makes large research builds reproducible without loading every full article for every request.

## World building

A world is a user-controlled graph of applications, subjects, collections, research grains, tools, and created artifacts. The World Builder may suggest connections, but persistent additions require an explicit save, build, or publish action.

## Robot learning boundary

Robots do not directly rewrite their permanent behavior from every click. They use task-scoped context packets. Durable changes require validation, versioning, testing, and rollback capability.

## Required interfaces

- `POST /api/research/search` — returns ranked grains
- `POST /api/context/build` — assembles a permission-scoped packet
- `GET /api/research/source/:hash` — retrieves an authorized full source
- `POST /api/world/save` — stores a user-approved world connection
- `POST /api/ledger/validate` — validates a productive action
- `DELETE /api/activity/:id` — deletes eligible private activity
- `GET /api/explain/:recommendationId` — explains why content was surfaced

This protocol lets research bloom into applications while keeping source meaning, user control, privacy, and security intact.