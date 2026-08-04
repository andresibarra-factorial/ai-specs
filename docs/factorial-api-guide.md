# Factorial API Guide

How we consume Factorial's public API across all projects.

## 1. The OAS file — our reference contract

- Factorial publishes a dated OpenAPI snapshot roughly **every 3 months**. We keep it as `factorial-oas-YYYY-MM-DD.json`, where the date **is** the API version (e.g. `factorial-oas-2026-07-01.json` ↔ version `2026-07-01`).
- **Every new project starts by locating the latest OAS file and understanding it** — use the `factorial-oas` skill. Never design endpoints from memory.
- Each project **pins one API version** in its build brief and config. The `factorial-oas` skill flags drift between the pinned version and the newest available snapshot (e.g. Wellhub pins `2026-04-01` while `2026-07-01` exists).
- The spec is large (~380 paths, OpenAPI 3.1). Query it with `jq`/Python; don't read it whole. Real domain grouping is in the tags (`Domain > Resource`, e.g. `Attendance > Shift`, `Employees > Employee`, `Trainings > Session`).

## 2. URL pattern

```
{base_url}/api/{version}/resources/{domain}/{resource}[/{id}]
```

Servers: `https://api.factorialhr.com` (production), `https://api.eu2.demo.factorial.dev` (demo). The version segment must equal the pinned OAS version.

## 3. Authentication

Two schemes (from the OAS security schemes):

- **API key**: `x-api-key` header. Simplest; used by current YepCode projects.
- **OAuth2** (authorization code; scopes `read`/`write`): bearer token, refresh-before-expiry. On Factorial Code this is handled for you — `FACTORIAL_TOKEN` is provisioned per customer deployment and consumed by `FactorialClient`.

Convention (Wellhub pattern for YepCode): an `auth_factorial` module switched by `FACTORIAL_AUTH_STRATEGY` (`api_key` | `oauth_company_token` | `oauth_user_token`), so strategy changes don't touch the client.

## 4. Rate limits and pagination

- Retry 429/5xx with exponential backoff, honoring `RateLimit-*` / `Retry-After` headers. Centralize in `http_client`.
- Pagination: isolate envelope parsing and page-cursor extraction in dedicated helpers (`_extract_records`, `_next_page_params`) and **verify them against the pinned OAS**, not against assumptions — response envelopes have historically been the main source of drift.

## 5. Known quirks (verified in live runs — Wellhub `BUILD_DECISIONS.md`)

- **Webhooks carry no event-type payload field**: the operation (create/update/terminate) must be inferred from the delivered employee state and subscription type.
- **`create_with_contract` webhooks can arrive with null emails** — enrichment requires a follow-up `GET employees/{id}` re-read.
- Webhook subscriptions are created via `POST api_public/webhook_subscriptions`; validate deliveries (challenge check / signature) per `python-standards.md` §9. Factorial's subscription challenge arrives in the `x-factorial-wh-challenge` header (`checkWebhookChallenge` in `base-app` handles it on Factorial Code).
- Custom-field lookups go `custom_fields/fields?label=` → `custom_fields/values?field_id=&value=` (the alsina pattern for external-ID → employee resolution).

When a live run disproves an assumption, record it in the project's `BUILD_DECISIONS.md` and propose promoting it here if it generalizes.

## 6. Client rules

- Factorial Code: **`FactorialClient` only** (pagination, OAuth, error handling built in). SDKs: `@factorialco/api-client` (npm), `factorial-api-client` (PyPI).
- YepCode: thin `factorial_client` module — no auth or retry logic of its own; transport through `http_client`, auth through `auth_factorial`.
- Wrap failures in a domain error (`FactorialAPIError`) carrying status + truncated response body. Never let raw HTTP errors cross the client boundary.
