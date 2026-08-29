# Paragraph Gear and Swipe Router

## Purpose

The Paragraph Gear turns each conversation paragraph into an addressable work block. A person or authorized robot can continue beside it, create a focused conversation from it, or route a linked copy into a related conversation or project.

The source paragraph remains in its original conversation. Routing does not silently delete, rewrite, or detach it.

![Paragraph Gear and nested color routing](paragraph-gear-quantum-routing.svg)

## Paragraph card

Each paragraph card carries:

- a stable block identifier;
- immutable source text or a private source reference;
- source conversation and position;
- current project and color state;
- parent and child relationships;
- destination links;
- timestamps and routing receipts;
- permissions and publication boundary.

Raw private conversation text stays private by default. Public GitHub records normally contain an approved summary, hashes or private references, routing metadata, and non-sensitive evidence.

## Gear menu

| Action | Result | Starting color |
|---|---|---|
| Discuss here | Places the composer directly below the selected paragraph | Current block color |
| Start new conversation | Creates a child thread seeded by a linked copy | Red, then Blue |
| Add to conversation | Imports a linked copy into a selected existing thread | Red, then Blue |
| Add to project | Routes the block to a named repository, document, issue, or card | Red, then Blue |
| Fold section | Hides older discussion without deleting it | No state change |
| Inspect source | Shows ancestry, exact source, permissions, and receipts | Pink when evidence is incomplete |

Swipe may expose the same actions on touch devices. The visible Gear remains available so the feature does not depend on a hidden gesture.

## Micro-routing rule

```text
Select paragraph
→ preserve exact source (Yellow)
→ open Gear
→ choose a known destination (Red)
→ create linked instance and receipt (Blue)
→ combine with destination context when needed (Purple)
→ engineer and verify the result (Green)
```

Red is not permission to move information anywhere automatically. A valid Red action requires:

1. a known destination;
2. authority to read the source;
3. authority to write to the destination;
4. a privacy check;
5. a non-destructive source link;
6. a receipt describing what moved, where, when, and by whom.

If the destination is unknown, the block becomes Pink rather than Red.

## Robot utility behavior

Robots may propose routes using similarity, project identity, unresolved dependencies, recency, and explicit user decisions. They must:

- present low-confidence destinations for review;
- request attention for Orange decisions;
- preserve Yellow text exactly;
- distinguish a copied instance from the original;
- avoid exporting private text to public repositories;
- never claim a route succeeded without a destination receipt.

The utility makes the conversation catalog actionable: relevant work can move forward without losing its ancestry or scattering duplicate, untraceable text.

## Phone-first behavior

- Keep the Gear beside its paragraph without covering text.
- Give controls large touch targets.
- Let the composer move beneath the selected paragraph.
- Allow older branches to fold while remaining recoverable.
- Support swipe as an accelerator, not the only control.
- Keep the newest conclusion visible beside its source.
- Require visible confirmation before external publishing, messaging, permission changes, or destructive actions.

## Data contract

See [paragraph-action.schema.json](paragraph-action.schema.json) for the machine-readable action and receipt format.
