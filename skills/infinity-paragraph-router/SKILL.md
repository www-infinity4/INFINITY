---
name: infinity-paragraph-router
description: Create reviewable, non-destructive routes from a selected paragraph into a local discussion, new conversation, related conversation, project, document, issue, or card. Use for paragraph Gear actions, swipe routing, conversation branching, folding, and source-ancestry receipts.
---

# Infinity Paragraph Router

Treat each selected paragraph as an addressable block. Keep its original location and ancestry intact. A route creates a linked instance; it does not silently remove or rewrite the source.

## Choose the action

- **Discuss here:** position the reply or composer beside the source block when the interface supports it.
- **Start conversation:** create a child thread seeded by an approved linked instance.
- **Add to conversation:** route an approved linked instance into a named existing thread.
- **Add to project:** route it into a named repository, document, issue, or project card.
- **Fold section:** hide older discussion without deletion and keep it recoverable.
- **Inspect source:** show ancestry, permissions, integrity, destinations, and receipts.

If the host interface cannot perform a requested native UI action, produce the action record or implementation specification instead of claiming the UI changed.

## Route safely

1. Identify the exact source block and its privacy boundary.
2. Preserve exact text as Yellow or store a private immutable reference.
3. Require a named destination before entering Red.
4. Confirm authority to read the source and write to the destination.
5. Apply the minimum necessary transformation: exact approved text, private reference, or approved summary.
6. Import the linked instance as Blue.
7. Record a receipt with source, destination, created reference, actor, timestamp, and integrity result.

Read [the action contract](references/action-contract.md) when producing machine-readable routing records or implementing a Gear menu.

## Proposals and execution

Robots may rank destinations using project identity, semantic similarity, unresolved dependencies, explicit user decisions, and recency. Present low-confidence routes for review. Orange decisions and any external publication, message, permission change, or destructive action require visible human authority at execution time.

Never export unreviewed private conversation text to public GitHub. Never claim a route completed without a successful destination reference or receipt. If no destination is known, classify the block Pink and investigate rather than treating Red as a general permission.

## Interface invariants

- Keep the Gear beside its paragraph without covering text.
- Support large phone touch targets.
- Make swipe an accelerator, never the only control.
- Allow the composer to appear below the chosen paragraph.
- Fold older branches without erasing them.
- Keep the newest conclusion readable beside its source.
- Preserve native accessibility and confirmation behavior.
