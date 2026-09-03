# Python Standards (YepCode / Factorial Code)

Python is our primary language. Runtime: **3.12 on YepCode**, **3.13 on Factorial Code**. Write code compatible with the target platform declared in the project's build brief.

## 1. Project structure

```
project/
├── docs/                  # build brief (CLAUDE.md), design docs
├── modules/               # reusable logic — one folder per module
│   ├── <module_name>/<module_name>.py    (+ optional README.md, not deployed)
│   └── README.md          # catalog with dependency table
├── processes/             # entrypoints — one folder per process
│   ├── <process-slug>/main.py            (+ parametersSchema.json when it takes input)
│   └── README.md          # catalog
├── test/                  # offline suite (see testing-standards.md)
└── scripts/deploy.py      # YepCode projects only (Factorial Code uses fcode CLI)
```

Layering (dependencies only point downward):
**foundation** (config, log_utils, http_client) → **auth + API clients** → **state repositories** (over the datastore) → **domain logic** → **processes** (orchestrate only, no business logic).

## 2. Naming — platform-critical

- **Modules on YepCode**: underscored, valid Python identifiers (`link_table_repo`). Hyphens break the YepCode importer (verified in production).
- **Modules on Factorial Code**: kebab-case slugs are the platform convention (`shopify-client`) and what `base-app-py` uses; snake_case slugs work but release validation flags naming as a Warning. Migrated projects may keep snake_case — record the choice in the build brief. Entry file is always `modules/<slug>/<slug>.py`, never `main.py` (reserved for processes).
- **Processes**: hyphenated slugs (`sync-eligibility`). Entrypoints only, never imported.
- Never shadow the stdlib (`logging` → use `log_utils`).
- Datastore keys: only `[A-Za-z0-9_-]`. Encode anything else (e.g. base32 via a `make_key` helper).

## 3. Process entrypoint

All logic inside `main()`. No top-level `return` (platform wraps the script).

```python
# processes/<slug>/main.py
def main():
    params = fcode.context.parameters   # yepcode.context.parameters on YepCode
    orchestrator = fcode.import_module("sync_orchestrator")
    result = orchestrator.run(params)
    return {"status": 200, "body": result}
```

- **Factorial Code: never call `main()` yourself** — the platform invokes it; a self-invocation is a release-validation Blocker. The `fcode` global is injected (importable as `from fcode import fcode, logger`).
- **YepCode**: the `yepcode` global is injected; its runner also invokes `main()` — keep the file free of top-level side effects either way.

- Module imports use `yepcode.import_module("name")` / `fcode.import_module("name")` with **literal string arguments only** (static bundling requirement).
- Return `{"status", "body", "headers"}` to control webhook responses. Keep sensitive results out of persisted execution results: YepCode marks them `isTransient`; Factorial Code returns `{"transient": True, ...}`.

## 4. Dependencies

- Prefer the stdlib. Every third-party dependency must be justified in the build brief.
- **YepCode**: declare inline, pinned, single equals: `# @add-package pkg=x.y.z`.
- **Factorial Code**: pin in `dependencies/requirements.txt` (e.g. `argon2-cffi==25.1.0`); the `# @add-package` comment is needed only when the pip package name differs from the import name (`# @add-package argon2-cffi` above `import argon2`). Packages a parent workspace already provides (e.g. `factorial-api-client` from `base-app-py`) must **not** be redeclared — a child's specifier replaces the parent's.
- Dependencies are team-global by default — coordinate versions across processes.

## 5. HTTP and Factorial API

- All outbound HTTP to **external systems** goes through a shared `http_client` module: retries on 429/5xx with exponential backoff, honoring `RateLimit-*` / `Retry-After` headers; timeouts always set.
- **Factorial Code**: Factorial API calls go through the inherited `factorial-sdk` module — `sdk = fcode.import_module("factorial-sdk"); client = sdk.create_factorial_client()` (wraps the `factorial-api-client` SDK; `sdk.request_body({...})` for create/update bodies; `paginate()`/`all()` for cursor pagination, pages capped at 100). A hand-rolled Factorial HTTP client is a release-validation **Blocker**. Token arrives as `FACTORIAL_TOKEN` (auto-provisioned remotely; local runs take it from `variables.local.env`); never manage credentials in code. Higher-level helpers (company id, webhook subscriptions) live in the inherited `factorial-utils`.
- **YepCode**: thin `factorial_client` module over `http_client`; auth strategy (api_key / OAuth) via an `auth_factorial` module switched by env var. See `factorial-api-guide.md`.

## 6. Configuration and secrets

- All config through team variables (`fcode.env.X` / `os.environ`), catalogued in the build brief's environment-variable table with a Sensitive flag.
- Never log secrets or PII. Never commit `.env`.
- Mark sensitive form/schema inputs `isSensitive`; non-persistable data `isTransient`.

## 7. State

- `datastore` for cursors, checkpoints, link tables: strings/numbers only (JSON-stringify objects), small entries, key rules from §2.
- `storage` for files; local disk is ephemeral per-execution. Factorial Code: write temp files under `os.environ["TMP_DATA_DIR"]`; `fcode.storage.create_signed_url()` for download links; the inherited `datastore-inspector` process inspects/cleans/exports datastore state.
- Factorial Code runtime helpers: `fcode.variables.set/get/list/delete` (**sensitive by default** — pass `sensitive=False` for plain config; `delete` on an inherited key is a silent no-op) and `fcode.schedule.create/update/pause/resume/delete` for managing schedules from code. `fcode.env` is a snapshot taken at execution start.

## 8. Code style

- Type hints on all public functions. Docstring header per file: purpose, public API, contracts with other modules.
- Explicit domain errors (e.g. `FactorialAPIError` carrying status + truncated body); map platform/HTTP errors to domain errors at the client boundary.
- Logging: concise summaries, not per-record spam (platform caps log lines/size). Structured messages: `logger.info("flush complete: pushed=%d failed=%d", ok, ko)`.
- Factorial Code: log through the inherited `fcode-logs` module (`log = fcode.import_module("fcode-logs")`; `debug/info/warn/error`, gated by the `LOG_LEVEL` team variable, default `info`) — a project `log_utils` may wrap it for correlation ids, not replace it.
  - **Documented exception:** a project logger may *replace* `fcode-logs` when it keeps the
    same `LOG_LEVEL` gating **and** every level on a single stream. `fcode-logs` routes
    warn/error to stderr; interleaving stdout and stderr is not order-guaranteed, so a
    correlation-id trace through one ordered stream — the primary diagnostic for a
    multi-stage integration — breaks. Wrapping buys conformance and costs ordering, and
    `fcode-logs` offers no structure, correlation ids, redaction or chunking to gain in
    return. Taken by the Wellhub integration on 2026-09-03; record the same reasoning in
    `APP_VALIDATION_REPORT.md` (LOG-01) wherever it is used.
- Concurrency (`ThreadPoolExecutor`) only when measured need exists; keep worker counts configurable.

## 9. Webhooks

- Always validate: HMAC signature over the raw body, or at minimum basic auth + challenge check (`checkWebhookChallenge` on Factorial Code).
- Design for the 60s synchronous response timeout: acknowledge fast, process async (buffer-and-batch pattern), report status separately.
- Factorial webhook quirks are documented in `factorial-api-guide.md` §5 — read them before designing any webhook consumer.
