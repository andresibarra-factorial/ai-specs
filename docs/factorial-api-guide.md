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

- **API key**: `x-api-key` header. Simplest; used by current YepCode projects. (The key is JWT-formatted but is still sent as `x-api-key`, not as a bearer token.)
- **OAuth2** (authorization code; scopes `read`/`write`): bearer token, refresh-before-expiry. On Factorial Code this is handled for you — `FACTORIAL_TOKEN` is provisioned per customer deployment and consumed through the inherited `factorial-sdk` module (`create_factorial_client()`, token wins over api key when both exist).

Convention (Wellhub pattern for YepCode): an `auth_factorial` module switched by `FACTORIAL_AUTH_STRATEGY` (`api_key` | `oauth_company_token` | `oauth_user_token`), so strategy changes don't touch the client.

## 4. Rate limits and pagination

- Retry 429/5xx with exponential backoff, honoring `RateLimit-*` / `Retry-After` headers. Centralize in `http_client`.
- Pagination (hand-rolled clients): isolate envelope parsing and page-cursor extraction in dedicated helpers (`_extract_records`, `_next_page_params`) and **verify them against the pinned OAS**, not against assumptions — response envelopes have historically been the main source of drift.
- Pagination (SDKs): list endpoints return `{data, meta: {end_cursor, has_next_page}}`; pages are **hard-capped at 100 items**, cursors are sequential. Use `paginate()` / `all()` (`collect_all()` in Python), filter server-side first, and cap with `max_items` so a bug can't become an unbounded crawl.

## 5. Known quirks (verified in live runs — Wellhub `BUILD_DECISIONS.md`)

- **Webhook deliveries carry the bare resource object at the top level** — no `{type, data}` envelope and no event-type field: the operation (create/update/terminate) must be inferred from the delivered state, or disambiguated by using a distinct target URL per subscription (e.g. a `?type=` hint).
- **`create_with_contract` webhooks can arrive with null emails** — enrichment requires a follow-up `GET employees/{id}` re-read.
- **Delivery retry policy** *(official, 2026-08-26)*: Factorial retries a failing delivery up to **20 times over 48h**, then disables the subscription and emails you — re-enable with `PUT {enabled: true}`. Design consumers for **duplicate deliveries** (idempotency), and monitor for disabled subscriptions.
- Webhook subscriptions are created via `POST api_public/webhook_subscriptions` — **one subscription per type and company** (a 422 "already been taken" means reuse and repoint the existing one; `factorial-utils.setup_webhook` does this on Factorial Code). The optional `challenge` is echoed back in the `x-factorial-wh-challenge` header of every delivery. Validate it: on Factorial Code declare it as platform webhook auth (`webhook.authMode: TEAM` + `team.json` `webhookAuth {headerName: x-factorial-wh-challenge, variableKey: FACTORIAL_CHALLENGE_TOKEN}` — the platform 401s invalid callers before your code runs); elsewhere check it in code per `python-standards.md` §9. Author headers `x-factorial-author-id` / `x-factorial-author-type` identify who triggered the event.
- Custom-field lookups go `custom_fields/fields?label=` → `custom_fields/values?field_id=&value=` (the alsina pattern for external-ID → employee resolution).

When a live run disproves an assumption, record it in the project's `BUILD_DECISIONS.md` and propose promoting it here if it generalizes.

## 6. Client rules

- Factorial Code: **the inherited `factorial-sdk` module only** — `sdk.create_factorial_client()` returns an authenticated `FactorialClient` from the official SDK (`factorial-api-client` on PyPI / `@factorialco/api-client` on npm; namespaced `client.<domain>.<resource>.<method>`, throws on non-2xx). Wrap plain-dict bodies with `sdk.request_body({...})`. A hand-rolled Factorial HTTP client is a release-validation **Blocker**; higher-level helpers (company id via `get_company_id`, webhook management) come from `factorial-utils`.
- YepCode: thin `factorial_client` module — no auth or retry logic of its own; transport through `http_client`, auth through `auth_factorial`.
- Wrap failures in a domain error (`FactorialAPIError`) carrying status + truncated response body. Never let raw HTTP errors cross the client boundary.
- SDK majors pin an API date version — a newer API version ships as a new SDK major; keep the SDK pin consistent with the project's pinned OAS.
