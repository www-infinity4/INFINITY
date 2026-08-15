# Infinity Repository Integration Plan

## Core rule

The main root must remain easy to understand and deploy. Repositories connect through a registry, links, shared packages, and APIs. They are not blindly pasted together.

## Phase 1 — Inventory

Create a generated registry containing repository name, category, purpose, language, deployment URL, health status, dependencies, and canonical/duplicate status. The root portal already begins this by reading the public GitHub API.

## Phase 2 — Canonical project map

Review overlapping families such as Gitpal/Gitpal-/Clone-of-Gitpal, inertia projects, radio projects, media tools, games, finance tools, and science documentation. Choose one canonical repository per working product while preserving the others as archives or research inputs.

## Phase 3 — Shared foundation

Create versioned shared modules for:

- design tokens and reusable components
- repository and project schemas
- navigation and search
- authentication adapters
- API request and error formats
- logging, health checks, and rate limiting
- security headers and content-security policy

Projects consume released versions rather than copying files manually.

## Phase 4 — AI gateway

Use a server-side endpoint with a provider-neutral contract. Recommended provider order:

1. Gemini API free allowance where available
2. OpenRouter models explicitly marked free
3. Cloudflare Workers AI included/free allocation where available
4. OpenAI API only when billing is intentionally enabled

Required controls: secrets in environment variables, allowlisted models, request size limits, per-user rate limits, daily budget ceilings, safety filtering, audit logs without sensitive prompt storage, and automatic fallback.

## Phase 5 — Deployment

Use GitHub Pages or Cloudflare Pages for static projects. Use Cloudflare Workers, Pages Functions, or another serverless backend for private API keys and dynamic services. Every deployed project gets a stable URL recorded in the root registry.

## Phase 6 — Migration batches

Connect five to ten repositories at a time. For each batch:

1. document purpose and entry point
2. run or inspect the project
3. remove exposed secrets and unsafe dependencies
4. add a health endpoint or build check
5. add root navigation metadata
6. deploy a preview
7. validate links, mobile layout, and accessibility
8. merge only after the batch works

## Initial project families

- Core platform: INFINITY, Infinity-Flow, Infinity-Synapses, Frameworks, Hosting-service, Hydrhost
- Science/research: Infinity-Quantum-Systems, Atomic-Transmutation, Atom-Weaver, Electromagnetism, Field-theory, Hydrogen-Radio, Quanta-Microphone
- Robotics: Humanoid-BioBots, R2D2, Dr4ne-Sm4ker
- Media: Infinity-Sound, Alien-Radio, Broadcast-Engine, Visual-Camera-Analyzer, Infinity-Graphics
- Finance: Mint-For-Infinity, Bitcoin-Tonight-Coin, Alien-Coin, Money-Stream, Money-Farm
- Cards/commerce: Goudey-Tradition-Trading-Card-Company-LLC, Sports-Card-Builder, Mckee-Coins-Inc
- Games: Emulation-Station, Zelda-NES, Tetris, Atari, Mario-spin, FantasyQuest

## Definition of connected

A repository is connected when it has a documented purpose, stable root link, working build or readable documentation, deployment status, security review status, owner, integration contract, and automated validation. A link alone is discovery; the later checks make it operationally connected.
