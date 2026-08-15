# Infinity AI Runtime — Local Gemma First

## Goal

Infinity applications should have one AI runtime contract instead of each repository hard-wiring a different paid provider. The default path is local/open-weight Gemma-family models. Hosted providers are optional fallbacks, not architectural requirements.

## Roles

### 1. `REASONER`
Use a general Gemma model for synthesis, classification, research planning, token reframing, profile-conditioned rendering, and multi-step decisions.

Default role: `gemma-general-local`.

The runtime does not assume a cloud API key. A local inference service can expose a loopback HTTP endpoint or be embedded directly in the application runtime. A hosted Gemini/Gemma endpoint may be configured later when desired.

### 2. `TOOL_ROUTER`
Use FunctionGemma or another small function-calling Gemma model to translate user intent into approved structured actions.

Examples:

- `research.search`
- `research.expand_token`
- `wallet.get_balance`
- `token.open`
- `token.engineer`
- `token.import`
- `token.route`
- `avatar.create`
- `mint.prepare`
- `media.share`

The model proposes a function and arguments. The Infinity application validates permissions and executes the tool. The model never receives unrestricted shell execution.

### 3. `IMAGE_SAFETY`
Use ShieldGemma 2 as the image publication gate for Mint, Avatar Coin, profile media, ads, and transferable token assets.

Draft uploads remain private until the safety result is `APPROVED`. `BLOCKED` and `REVIEW_REQUIRED` assets never enter a public/transferable token package.

### 4. `TEXT_SAFETY`
Use ShieldGemma text safety models for public text, captions, ads, descriptions, links, and generated material before publication.

### 5. `EMBEDDINGS`
Use a local embedding model (EmbeddingGemma when practical) for fast semantic token search, Timelines, related-project discovery, novelty checks, and profile/feed matching.

## Runtime contract

All repos talk to one logical interface:

```text
Infinity application
      |
      v
InfinityAIRuntime.request(role, input, tools, context)
      |
      +--> local REASONER
      +--> local TOOL_ROUTER
      +--> local IMAGE_SAFETY
      +--> local TEXT_SAFETY
      +--> local EMBEDDINGS
      |
      `--> optional hosted fallback if explicitly configured
```

Applications must not contain model-specific business logic. They request a role and receive a typed result.

## Local endpoint convention

Default local base URL:

```text
http://127.0.0.1:11435
```

Suggested endpoints:

```text
POST /v1/reason
POST /v1/tools
POST /v1/moderate/image
POST /v1/moderate/text
POST /v1/embed
GET  /v1/health
```

The URL is configurable. No API key is required for the loopback/local runtime unless the operator intentionally enables local authentication.

## Hosted fallback

Hosted inference is optional. When enabled, credentials live outside repositories in environment/runtime secrets. The application must never require a hosted key when a compatible local model is healthy.

Provider selection order:

```text
LOCAL_READY
  -> use local model
LOCAL_UNAVAILABLE + HOSTED_CONFIGURED
  -> use configured hosted provider
NO_PROVIDER
  -> fail closed for publication/moderation
  -> degrade gracefully for non-safety suggestions
```

Safety moderation always fails closed. General suggestions/research planning may fall back to deterministic local rules when no model is available.

## Tool safety

Function calling is routing, not automatic execution. Each proposed call is validated against:

- allowed function name;
- authenticated account;
- repository/token permissions;
- rate/daily entitlement rules;
- expected argument schema;
- content-safety state;
- idempotency key;
- confirmation requirement for irreversible operations.

## Repository migration

Repositories should gradually replace direct provider calls with the shared client.

Priority order:

1. Mint-For-Infinity — image/text moderation + curation.
2. Bitcoin-Crusher — novelty research planning and tool routing.
3. Octave Research Portal — research synthesis and tool routing.
4. TV-Database — recommendations, catalog research, share diagnostics.
5. Alien-Coin — bundle research/enrichment.
6. Avatar Coin clients — safe content review and edit-point planning.
7. Timelines — embedding/search acceleration.

## Evidence rules

The runtime must preserve the existing evidence distinction:

- `OBSERVED`: direct system/Git/user event facts.
- `INFERRED`: model interpretation.
- `EXTERNALLY_VERIFIED`: supported by captured external sources.
- `USER_DEFINED`: user taxonomy/business rules.

A Gemma response by itself is never `EXTERNALLY_VERIFIED`.

## Working gateway

`server.py` now implements the role contract as a standard-library-only loopback service. It sits between Infinity applications and one or more OpenAI-compatible local inference processes such as the `llama-server` launcher already provided by `Gemma4-AI-`.

Start a local model first:

```sh
cd Gemma4-AI-
./start-gemma.sh
```

Then start the shared Infinity gateway:

```sh
cd INFINITY/ai-runtime
chmod +x start-runtime.sh
./start-runtime.sh
```

No pip installation or API key is required. Confirm the gateway and every configured role:

```sh
curl http://127.0.0.1:11435/v1/health
```

The health response is `READY` only when every role's configured local endpoint answers. If the general model is running but a ShieldGemma role is unavailable, health is `DEGRADED` and `publicationAllowed` remains false.

### Requests

Reasoning:

```sh
curl -X POST http://127.0.0.1:11435/v1/reason \
  -H 'Content-Type: application/json' \
  -d '{"input":"Plan a new Bitcoin Crusher research assignment."}'
```

Tool proposal:

```sh
curl -X POST http://127.0.0.1:11435/v1/tools \
  -H 'Content-Type: application/json' \
  -d '{"input":"Research hydrogen","tools":[{"name":"research.search","description":"Search captured sources"}]}'
```

The response contains `executed: false`. The calling application must still validate permissions, schemas, rate limits, confirmation requirements, and idempotency before running anything.

Text moderation:

```sh
curl -X POST http://127.0.0.1:11435/v1/moderate/text \
  -H 'Content-Type: application/json' \
  -d '{"input":"Public caption to review"}'
```

Image moderation accepts an image data URL or another reference that the configured local multimodal server can read. Embeddings use `POST /v1/embed`.

### Multiple local model processes

A single `llama-server` normally serves one loaded model. Run separate local processes for specialized roles, then set role-specific environment variables:

```sh
INFINITY_REASONER_BASE_URL=http://127.0.0.1:8080/v1 \
INFINITY_TOOL_ROUTER_BASE_URL=http://127.0.0.1:8081/v1 \
INFINITY_IMAGE_SAFETY_BASE_URL=http://127.0.0.1:8082/v1 \
INFINITY_TEXT_SAFETY_BASE_URL=http://127.0.0.1:8083/v1 \
INFINITY_EMBEDDINGS_BASE_URL=http://127.0.0.1:8084/v1 \
./start-runtime.sh
```

Hosted fallback remains disabled. The service refuses a non-loopback network bind unless the operator explicitly sets `INFINITY_AI_ALLOW_REMOTE=1`.

### Verification

```sh
python3 -m unittest -v test_server.py
```

The integration test starts a fake local inference process and verifies health, reasoning, tool allowlisting, text/image moderation, embeddings, and fail-closed publication behavior.

