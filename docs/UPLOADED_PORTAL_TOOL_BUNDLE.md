# Uploaded Infinity Portal and Tool Bundle

## Files reviewed

### `InfinityPortal_index_Version2.html`

- Mobile-width portal shell
- Large hub buttons
- Sidebar navigation
- floating chat dock
- Google Identity Services script
- Google-hosted Inter font
- theme color and phone viewport support

SHA-256 prefix: `c6aa6d61d74f8d6a`

**Use:** preserve as a historical portal prototype. Its fixed set of hub buttons should be reconciled with the current five-choice Infinity Index: Music, TV, Build, Shop, More.

**Do not deploy unchanged:** Google login requires configured client identity, consent handling, origin restrictions, and a real session backend.

### `infinity-deployer.html`

- Three-column deployment dashboard
- PayPal/Infinity visual styling
- static buttons and panels
- no actual deployment API calls
- no credentials, localStorage, or fetch logic in the uploaded version

SHA-256 prefix: `88366df4bc1b5a79`

**Use:** visual foundation for a safe deployment review console.

**Required implementation:** deployments must be performed by a server-side service or GitHub workflow with least-privilege credentials. Never place GitHub, hosting, payment, or cloud secrets in browser JavaScript.

### `infinity-ai-terminal.html`

- Mongoose.OS-styled AI terminal
- search state indicators and responsive sidebar
- Wikipedia, Wikidata, DuckDuckGo, and AllOrigins requests
- localStorage state
- remote Google font

SHA-256 prefix: `7c1ce66a58ef34a3`

**Use:** terminal interface and research-result presentation.

**Replace:** public CORS proxy dependency, unsanitized remote content insertion, and assumptions that free public APIs are always available.

### `ignition-index.html`

- Infinity OS ignition/launch page
- animated orbital core and star canvas
- localStorage state
- `/shared-components.js` dependency
- external Google fonts
- direct repository link

SHA-256 prefix: `1d3a769fa10d9f0d`

**Use:** intermission/launch transition into Build tools, Mario Spin, or deployment console.

### `forknight-page.html`

- Project-gallery page linking several public GitHub game repositories
- includes a link to `pewpi-infinity/Forknight`
- no scripts or application state

SHA-256 prefix: `961a04452344c662`

**Use:** source-attribution/catalog page, not a game itself. Verify licenses before copying code from linked repositories.

## Recommended architecture

```text
Infinity Index
├── Music
├── TV
├── Build
│   ├── Ignition
│   ├── Infinity AI Terminal
│   └── Infinity Deployer
├── Shop
└── More
    ├── Forknight project catalog
    ├── Mario Spin
    └── Research laboratories
```

## Security corrections

1. No secret keys in HTML, localStorage, URL parameters, or generated pages.
2. Google sign-in only through an approved OAuth/OIDC backend with state, nonce, PKCE where applicable, and origin restrictions.
3. Deployments require authenticated server-side actions, branch protection, signed commits/releases, and environment approvals.
4. Remote search content must be escaped before display.
5. Replace AllOrigins with a controlled proxy that validates domains, methods, size, timeout, and content type.
6. Self-host fonts or use system fonts.
7. Use a strict Content Security Policy and explicit frame/connect allowlists.
8. Add audit logs for build/deploy actions without logging credentials or private prompts.
9. The Deployer should default to preview/dry-run and require explicit confirmation for production.
10. Payment styling must not imply PayPal affiliation or process payments without a compliant provider integration.

## Canonical product roles

- **Infinity Portal:** public navigation and identity entry.
- **Ignition:** visual transition and health/status check.
- **Infinity AI Terminal:** research, project search, and command drafting.
- **Infinity Deployer:** review, preview, approve, and deploy—not an in-browser secret holder.
- **Forknight Catalog:** attribution and project discovery.

## Import policy

Preserve original uploads under a future `prototypes/2026-08-05/` directory. Build cleaned production routes separately. Do not overwrite the current entry point until all links, identity flows, accessibility, and deployment actions have been tested.