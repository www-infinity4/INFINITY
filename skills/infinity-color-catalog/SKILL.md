---
name: infinity-color-catalog
description: Classify conversation and project work into Kris's seven-color operational catalog, surface attention needs, and propose evidence-backed next routes. Use when indexing threads, determining current work state, prioritizing unresolved blocks, or preparing color metadata for a catalog or repository.
---

# Infinity Color Catalog

Treat colors as operations on distinct work blocks, not decorative thread labels. A conversation may contain multiple blocks with different colors.

## Classify

1. Split the supplied material into independently actionable blocks.
2. Resolve each block to a canonical project when the evidence permits.
3. Assign one current color using [the registry](references/color-registry.md).
4. Cite the facts supporting the classification and state confidence.
5. Record a proposed next color and its entry condition.
6. Surface Orange decisions, Pink unknowns, blocked work, and stale verification before completed work.

When access to prior conversations or repositories is unavailable, classify only the supplied evidence and say what remains unscanned. Never imply access to an entire catalog without a successful retrieval.

## Preserve Yellow

Yellow is exact extraction only. Preserve selected source text word for word without correction, summarization, coding, gap filling, or interpretation. Keep commentary in a separate block that points to the Yellow source. Do not publish private Yellow text to a public repository unless the user deliberately approves it.

## Require evidence

- Blue requires a named destination and an import receipt, file, pull request, or commit.
- Green requires an implementation plus relevant verification.
- Red requires a known destination; otherwise use Pink.
- Orange requires a recorded human decision before an authority-sensitive action.
- Purple identifies the inputs being assimilated and records gaps or corrections.
- Pink records the unknown, sources checked, and evidence needed to exit.

Do not downgrade contradictory evidence merely to obtain a cleaner color sequence. The system is fluid and does not require every block to pass through every color.

## Output

For ordinary requests, return a compact inventory containing block, project, current color, evidence, status, confidence, attention reason, and next condition. For machine output, use the schema supplied by the destination project when available; otherwise use stable lowercase IDs and ISO-8601 timestamps.

Proposed classifications do not authorize external writes, conversation moves, publication, deletion, or account changes. Obtain the authority required by the active tool immediately before such an action.
