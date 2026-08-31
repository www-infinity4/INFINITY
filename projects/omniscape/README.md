# Omniscape

**A phone-first intelligent browser for exploring the web, the Infinity ecosystem, and your own connected knowledge.**

Omniscape is our modern counterpart to the early all-in-one browsers such as Netscape: a single doorway for browsing, searching, communicating, building, saving, and working with AI. It is not intended to be another skin placed over a search box. Omniscape treats every page, message, file, media item, application, and AI conversation as part of one navigable information landscape.

The name combines **omni**—many directions and connected spaces—with **scape**—a visible landscape that can be explored.

## Vision

Early browsers made the internet understandable by gathering navigation, documents, bookmarks, downloads, and communication into one application. Omniscape extends that idea for the AI era.

The browser should be able to:

- open ordinary websites;
- search the public web and the user's saved knowledge;
- converse with AI beside any page;
- collect related pages into visual workspaces;
- connect Infinity applications through one consistent launcher;
- continue essential work offline;
- explain unfamiliar content in clear language;
- preserve the user's history and projects without turning that history into an advertising product;
- run comfortably on an Android phone before requiring a desktop computer.

## Core experience

### One address and command field

The main field accepts a URL, search request, question, command, project name, or saved destination. Omniscape determines the intended action and shows it before carrying out anything sensitive.

Examples:

```text
starquest
open my machining game
https://example.com
find the explanation of hydrogen portals
compare these three pages
resume yesterday's research
```

### Landscapes instead of tab clutter

Tabs remain available, but related tabs can be collected into a **Landscape**. A Landscape is a resumable workspace containing pages, notes, conversations, media, files, and app states.

Example Landscapes might include:

- StarQuest development;
- Disney Academia cards;
- electronics simulators;
- machining education;
- hydrogen research;
- Infinity wallet and mint operations.

### AI beside the page

An optional assistant drawer can summarize, explain, compare, translate, extract structured information, or help operate the current page. The assistant must distinguish page content from trusted user instructions. A website can supply information, but it cannot silently instruct the browser's AI to expose data or perform unrelated actions.

### Foldable conversation

Notes and AI discussions can attach directly to the relevant paragraph, image, video time, form, or code section. Older discussion can fold away without being deleted, allowing the newest conclusion to remain readable beside its source.

### Phone-first controls

Omniscape is designed around one-handed Android use:

- large readable text and touch targets;
- bottom navigation within thumb reach;
- voice input;
- swipeable cards and tab groups;
- adjustable reading mode;
- picture-in-picture media;
- offline reading and queued actions;
- no essential hardware-keyboard commands.

## Main surfaces

| Surface | Purpose |
| --- | --- |
| Home | Launcher, prompt, recent Landscapes, and pinned Infinity apps |
| Browse | Normal web navigation with reading and accessibility controls |
| Search | Combined web, history, saved pages, files, and project search |
| Landscapes | Visual groups of connected tabs, media, notes, and tasks |
| Messages | AI conversations and later person-to-person communication |
| Library | Saved pages, downloads, cards, documents, and offline material |
| Builder | Page inspection, code assistance, app creation, and publishing tools |
| Settings | Privacy, permissions, storage, accessibility, accounts, and AI routing |

## Infinity ecosystem

Omniscape can serve as the front door to the wider Infinity system while keeping every application independently usable.

Planned connections include:

- StarQuest and Cosmo;
- Infinity Wallet and Mint;
- Infinity Builder;
- Idea Cloud;
- Infinity Market;
- Rogers Voice;
- Infinity Stage and Movie Hub;
- Infinity Times and Science Journal;
- Instrument Lab;
- Verse Engine;
- Infinity Clock;
- Mongoose.OS and approved agent tools.

Applications appear as signed capability cards. Each card states what it can read, what it can change, whether it requires network access, and whether the action leaves the device.

## Privacy and security

Omniscape follows a local-first and least-authority model.

- Browsing history, notes, and Landscape state remain on the device by default.
- Sync is optional, encrypted, and clearly separated from local storage.
- The browser never requests wallet seed phrases, recovery words, or private keys.
- Apps and AI tools receive only the capability required for the current action.
- Page content is treated as untrusted input, not as system instruction.
- External messages, purchases, publishing, account changes, and permission changes require visible confirmation.
- Private browsing creates no durable history after its session closes.
- Releases should be signed and accompanied by checksums.
- A restrictive content-security policy and dependency-light build reduce unnecessary attack surface.
- Physical-device controls are never exposed directly to public websites.

## Search and AI routing

Omniscape separates four jobs that ordinary browsers often mix together:

1. **Navigation** opens an exact address or known destination.
2. **Retrieval** finds public pages or local saved material.
3. **Reasoning** compares, explains, plans, or derives an answer.
4. **Action** changes an application or external service with user authority.

Local processing is preferred for history, organization, basic summaries, and private material. More capable remote models may be selected for difficult research or generation, but Omniscape displays which service will receive which information before transmission.

## Technical direction

### Prototype

The initial version can remain a dependency-light progressive web application:

- semantic HTML, CSS, and JavaScript;
- fragment-based routes for Home, Search, Landscapes, and Settings;
- IndexedDB for tabs, Landscapes, notes, history, and offline queues;
- service worker for an offline application shell and saved reading;
- web application manifest for Android installation;
- import/export using documented JSON schemas;
- no required cloud account for local use.

### Android application

The production Android build should use a maintained browser engine rather than inventing a new HTML renderer. A native shell can provide:

- secure web views and process isolation;
- Android share-target support;
- downloads and file handling;
- picture-in-picture;
- voice input;
- notifications;
- biometric protection for sensitive local areas;
- offline background queues;
- application links into Infinity projects.

### Core data model

```text
Landscape
  ├── Page references
  ├── Conversation threads
  ├── Notes and annotations
  ├── Media positions
  ├── Files and generated artifacts
  ├── Application states
  └── Permission receipts
```

Every saved object receives a stable local identifier, creation and update times, source information, integrity metadata, and optional encrypted sync state.

## Proposed repository structure

```text
omniscape/
├── README.md
├── SECURITY.md
├── LICENSE
├── docs/
│   ├── architecture.md
│   ├── privacy-model.md
│   ├── landscape-format.md
│   └── android-roadmap.md
├── web/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   ├── manifest.webmanifest
│   └── service-worker.js
├── android/
├── packages/
│   ├── landscape-core/
│   ├── search-router/
│   ├── permission-engine/
│   └── infinity-connectors/
└── tests/
```

## Development roadmap

### Phase 1 — Navigable prototype

- Home launcher and unified command field
- browser view and readable mobile controls
- tabs and persistent Landscapes
- local bookmarks, history, and downloads
- offline application shell
- installable Android PWA

### Phase 2 — Intelligent workspace

- AI drawer beside pages
- page summaries and comparisons
- attached and foldable conversations
- unified local search
- voice navigation
- structured import and export

### Phase 3 — Infinity browser

- signed Infinity application cards
- StarQuest, Wallet, Builder, and Idea Cloud launchers
- capability-based app permissions
- optional encrypted account sync
- user-controlled AI routing

### Phase 4 — Native Android release

- packaged Android application
- isolated browser processes
- share targets, picture-in-picture, downloads, and notifications
- accessibility and low-memory testing on inexpensive phones
- signed release artifacts and reproducible build documentation

## Definition of success

Omniscape succeeds when a person can open one application on an ordinary Android phone, reach the public web and their Infinity projects, understand what the AI is doing, keep important work organized, continue useful tasks offline, and remain in control of their history, permissions, and identity.

## Status

**Concept and architecture stage.** An earlier phone-first PWA starter established the offline shell, routes, local storage direction, manifest, and service-worker approach. This README is the product contract for the next implementation.

## Working principle

> The web should feel like a landscape you can understand, organize, and build upon—not an endless pile of disconnected pages.
