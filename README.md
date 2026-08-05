# Infinity Root Portal

The `INFINITY` repository is the main entry point for the `www-infinity4` project network.

## Purpose

This root does not copy every repository into one oversized codebase. It provides a live directory, shared architecture, standards, and integration contracts while every project keeps its own source history and deployment.

## Current build

- Responsive blue-purple root website
- Live GitHub repository discovery
- Search and automatic project grouping
- Direct links to every repository
- Architecture and AI-gateway documentation
- No API secrets stored in browser code

## Run locally

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080`.

## Deployment

The static portal can use GitHub Pages or Cloudflare Pages. AI calls must be handled by a server-side worker or function so provider keys remain private.

## Integration order

1. Inventory and classify repositories.
2. Establish this repository as the public root.
3. Add a machine-readable project registry and health checks.
4. Select canonical repositories where duplicates overlap.
5. Create shared UI, schema, authentication, and API packages.
6. Connect projects through documented URLs and APIs.
7. Add server-side AI routing with budget and rate limits.
8. Migrate projects in small tested batches rather than a destructive mass merge.

See [`docs/INTEGRATION_PLAN.md`](docs/INTEGRATION_PLAN.md) for the detailed plan.
