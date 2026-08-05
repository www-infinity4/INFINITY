# Infinity Application Security and Data Architecture

## Purpose

Infinity is an application platform, identity layer, research engine, activity system, and future value network. Public websites remain presentation surfaces; authenticated applications operate through protected services.

## Non-negotiable boundary

Git repositories store source code, schemas, public documentation, non-sensitive manifests, public research references, tests, and deployment configuration.

Git repositories must never store:

- passwords, passkeys, recovery codes, API keys, private signing keys, or seed phrases
- raw biometric images or templates
- personal viewing, searching, purchasing, auction, location, or messaging histories
- private user profiles or inferred interests
- unredacted support, housing, financial, or identity records
- production database exports

GitHub Secrets may inject deployment credentials into approved workflows, but application code must never copy those secrets into commits, logs, browser bundles, or generated pages.

## Application layers

1. **Infinity Shell** — shared navigation, accessibility, search, application launcher, session indicator, and privacy controls.
2. **Identity Service** — passkey-first authentication, optional verified-device step, session management, account recovery, and consent records.
3. **Infinity Vault** — encrypted private user data, preferences, saved worlds, and private activity history.
4. **Research Index** — public or licensed articles, structured summaries, citations, embeddings, hashes, and retrieval metadata.
5. **World Builder** — combines explicit user requests with approved context to assemble pages, tools, collections, and realms.
6. **Action Ledger** — append-only validated activity events used to measure system work and issue Infinity contribution units.
7. **Wallet Service** — balances and allocation rules. It is separate from identity and research data and is not a bank until legally and technically qualified.
8. **Application Registry** — manifests for TV-Database, Alien Radio, StarQuest, builders, commerce realms, robotics, and future apps.

## Login security

Use passkeys/WebAuthn as the preferred login method. Password login, when retained for recovery, requires modern password hashing, rate limits, breached-password checks, and multi-factor authentication.

Required controls:

- short-lived, HttpOnly, Secure, SameSite session cookies
- rotating refresh tokens stored server-side or as tightly scoped secure cookies
- CSRF protection for state-changing requests
- device and session list with remote sign-out
- risk-based step-up authentication for wallet, export, deletion, and identity changes
- recovery codes encrypted at rest and displayed once
- no authentication tokens in localStorage
- no secret-bearing query strings
- security event notifications without exposing private details

## Orb or coin verification

An Orb Coin may function as a possession-based security key or user-controlled authenticator. It must not silently scan a person or create an invisible biometric profile.

Safe design:

- explicit user action and visible consent
- prefer hardware-backed cryptographic proof over biometric storage
- if biometrics are ever used, match locally on the trusted device where possible
- never commit raw scans or templates to GitHub
- never use biometric identity as the sole recovery method
- provide a non-biometric login and recovery route
- document retention, deletion, false-match, and accessibility policies before release

## Private activity and personalization

Viewing fifteen movies, creating auction listings, searching, refreshing, or building a page can become contextual signals only under a clear privacy mode.

Every event must include:

- account or pseudonymous subject ID
- application and realm
- event type
- timestamp
- declared purpose
- consent scope
- retention class
- sensitivity class
- validation status

Raw activity is private by default. Derived recommendations must be explainable, correctable, exportable, and deletable. Accidental touches receive low weight. Publishing or token validation requires an explicit or clearly disclosed action.

## Action ledger and Infinity units

The ledger records validated work performed by the system. User collection limits and surplus allocation rules are applied by the wallet service, not by front-end JavaScript.

Each ledger event needs a unique ID, source application, validation method, policy version, allocation result, and tamper-evident signature or hash chain.

Platform units must not be represented as insured deposits, legal tender, investments, or guaranteed housing funds unless the required legal, financial, reserve, custody, and partner systems exist.

## Research storage

Full research remains in content-addressed storage when licensing permits. A cryptographic hash identifies the exact version. The retrieval layer stores compact structured records containing claims, sources, safety status, entities, keywords, and links to the full artifact.

A symbol such as `^` must never secretly stand for a 19,000-line program without a versioned dictionary. Safe compression requires:

- namespace and version, for example `infinity://research/v1/^42`
- deterministic expansion rules
- content hash of the expanded artifact
- human-readable description
- validation tests
- access-control classification

Compression saves transfer and retrieval cost; it does not remove the need to store and verify the source meaning.

## Encryption and key management

- TLS for all network traffic
- authenticated encryption for sensitive stored data
- keys in a managed key service, never in repositories
- separate keys by environment and data class
- key rotation and revocation procedures
- encrypted backups with tested restoration
- application logs scrubbed of credentials, biometrics, prompts, and private content

## Authorization

Use deny-by-default authorization. Every service checks subject, action, resource, realm, and consent scope. Administrative access must be separately authenticated, audited, time-limited where possible, and unavailable from public front-end code.

## Release gates

An Infinity project becomes an application only after it has:

- an application manifest and stable route
- authentication and authorization boundaries
- privacy and retention declarations
- security headers and content-security policy
- validated input and output handling
- dependency and secret scanning
- backup and recovery expectations
- accessible mobile and desktop behavior
- tests for critical flows
- a deployment and rollback plan

This document defines the minimum boundary for every connected Infinity application.