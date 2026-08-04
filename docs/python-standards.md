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

- **Modules**: underscored, valid Python identifiers (`link_table_repo`). Hyphens break the platform importer.
- **Processes**: hyphenated slugs (`sync-eligibility`). Entrypoints only, never imported.
- Never shadow the stdlib (`logging` → use `log_utils`).
- Datastore keys: only `[A-Za-z0-9_-]`. Encode anything else (e.g. base32 via a `make_key` helper).

## 3. Process entrypoint

All logic inside `main()`. No top-level `return` (platform wraps the script). Required for `fcode setup-debug` and for testability.

```python
# processes/<slug>/main.py
from fcode import fcode, logger   # YepCode: the `yepcode` global is injected, no import

def main():
    params = fcode.context.parameters   # yepcode.context.parameters on YepCode
    orchestrator = fcode.import_module("sync_orchestrator")
    result = orchestrator.run(params)
    return {"status": 200, "body": result}

main()
```

- Module imports use `yepcode.import_module("name")` / `fcode.import_module("name")` with **literal string arguments only** (static bundling requirement).
- Return `{"status", "body", "headers"}` to control webhook responses; mark sensitive results `isTransient`.

## 4. Dependencies

- Prefer the stdlib. Every third-party dependency must be justified in the build brief.
- Declare inline, pinned, **single equals**: `# @add-package pkg=x.y.z` (e.g. `# @add-package openai=1.59.8`). Factorial Code also supports `dependencies/requirements.txt`.
- Dependencies are team-global by default — coordinate versions across processes.

## 5. HTTP and Factorial API

- All outbound HTTP goes through a shared `http_client` module: retries on 429/5xx with exponential backoff, honoring `RateLimit-*` / `Retry-After` headers; timeouts always set.
- **Factorial Code**: use `FactorialClient` (`fcode.import("FactorialClient")` from `base-app`) — never hand-roll Factorial calls. Token arrives as `FACTORIAL_TOKEN`; never manage credentials in code.
- **YepCode**: thin `factorial_client` module over `http_client`; auth strategy (api_key / OAuth) via an `auth_factorial` module switched by env var. See `factorial-api-guide.md`.

## 6. Configuration and secrets

- All config through team variables (`fcode.env.X` / `os.environ`), catalogued in the build brief's environment-variable table with a Sensitive flag.
- Never log secrets or PII. Never commit `.env`.
- Mark sensitive form/schema inputs `isSensitive`; non-persistable data `isTransient`.

## 7. State

- `datastore` for cursors, checkpoints, link tables: strings/numbers only (JSON-stringify objects), small entries, key rules from §2.
- `storage` for files; local disk is ephemeral per-execution.

## 8. Code style

- Type hints on all public functions. Docstring header per file: purpose, public API, contracts with other modules.
- Explicit domain errors (e.g. `FactorialAPIError` carrying status + truncated body); map platform/HTTP errors to domain errors at the client boundary.
- Logging: concise summaries, not per-record spam (platform caps log lines/size). Structured messages: `logger.info("flush complete: pushed=%d failed=%d", ok, ko)`.
- Concurrency (`ThreadPoolExecutor`) only when measured need exists; keep worker counts configurable.

## 9. Webhooks

- Always validate: HMAC signature over the raw body, or at minimum basic auth + challenge check (`checkWebhookChallenge` on Factorial Code).
- Design for the 60s synchronous response timeout: acknowledge fast, process async (buffer-and-batch pattern), report status separately.
- Factorial webhook quirks are documented in `factorial-api-guide.md` §5 — read them before designing any webhook consumer.
