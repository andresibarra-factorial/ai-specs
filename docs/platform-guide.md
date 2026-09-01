# Platform Guide — YepCode vs Factorial Code

Both platforms run the same engine (Factorial acquired YepCode; Factorial Code is its evolution integrated with Factorial). The platform is chosen **case by case per project**, declared in the build brief. Projects may start on YepCode and later migrate (see the `migrate-platform` skill).

Facts marked *(verified 2026-08-26)* come from a real `fcode clone` of a dev workspace and its official `fcode-*` skills — trust them over older doc readings.

## 1. Side-by-side

| Area | YepCode | Factorial Code |
|---|---|---|
| Docs | https://yepcode.io/docs/ | https://code.factorialhr.com/docs |
| Global SDK object | `yepcode.*` (injected) | `fcode.*` (injected; also `from fcode import fcode, logger`) |
| Python / Node | 3.12 / 20 | **3.13 / 22** |
| CLI | `@yepcode/cli` | `@factorialco/fcode-cli`: `clone/pull/add/run/push/status/http`, `team:*`, `variables:*`, `i18n:*`, `remote:add` |
| Unit of delivery | Team of processes | **App**: `dev-{id}` → release request (semver + notes, platform-validated) → read-only `prod-{appId}` (created on first release) with the **`stable` alias** → per-customer `deploy-{installationId}` workspaces created by marketplace install (variables only, no code) |
| Code reuse | Modules within the team | Modules + **workspace inheritance** via `team.json` `parentTeamSlugs` (≤5 direct parents, **non-transitive**, read-only where inherited). Python apps inherit **`base-app-py`** |
| Factorial API | Your own client + credentials (api key / OAuth) | **`factorial-sdk` module** (inherited): `create_factorial_client()` returns an authenticated `FactorialClient` from the `factorial-api-client` SDK; `FACTORIAL_TOKEN` auto-provisioned per deployment. Hand-rolled Factorial HTTP clients are a release **Blocker** |
| Process entry | `main.py`, define `main()`, **call `main()` at the end** | `main.py`, define `main()`, **NEVER call it yourself** (the platform invokes it — self-invocation is a release Blocker) |
| Module naming | Underscored valid Python identifiers (hyphens break the importer — verified in production) | **kebab-case slugs are the platform convention** (`shopify-client`); entry file `modules/<slug>/<slug>.py\|js`, never `main.py`/`index.js`. snake_case slugs work but validation flags naming as a Warning |
| Testing | Local `run` only → our offline harness | `fcode run` (local execution), `fcode http` (local webhook/forms server replicating cloud auth), `fcode-code-validation` (pre-release static gate) + our offline harness |
| Deploy | Git repo + GitHub Action → YepCode Management API (Wellhub pattern) | `fcode push` to the dev workspace (syncs **registered resources only** — never loose files; `fcode add` registers new ones). Release/promotion below |
| Email | Bring your own | `fcode.send_mail` built in (3/execution; From fixed; logged-not-sent locally) |
| Secrets locally | `credentials/*.json` + `variables.env` | 3-file model below; secrets pull as `********` placeholders |
| Multi-tenancy | One team per client (our convention) | Per-customer `deploy-{installationId}` workspace, inheriting the app workspace; carries only that customer's variables and `FACTORIAL_TOKEN` |

## 2. Shared engine facts (both platforms)

- Triggers: on-demand, cron/schedules, webhooks (per-process URL), embedded forms (JSON Schema / react-jsonschema-form), REST API, MCP.
- **Sync webhook timeout: 60s** (HTTP 408; execution continues). Prefer async acknowledgment. Form submissions have a ~1-minute request timeout too.
- No automatic retries at process level — code must be idempotent and re-runnable. On Factorial Code, wire the workspace error handler (`team.json` `errorHandlerConfig` → the inherited `workspace-error-handler` process, which emails `ERROR_NOTIFY_EMAIL`).
- Datastore: team-level KV, **strings/numbers only** (JSON-serialize objects). Storage: cloud files; local disk is ephemeral — on Factorial Code write temp files under `TMP_DATA_DIR` and use `fcode.storage` (upload/download/list/`create_signed_url`).
- Logs capped (lines and size) — log summaries.
- Dependency installs happen asynchronously after manifest changes; executions use the old set until done. Only a parent's *installed* dependencies inherit.
- Static egress IP for allowlisting (Factorial Code: `34.89.54.108`).

## 3. Factorial Code specifics *(verified 2026-08-26)*

**Workspace files** (all synced by the CLI; commit them except where noted):

| File | Holds |
|---|---|
| `settings.json` (was `team.json` before CLI v3; key `parentTeams`, was `parentTeamSlugs`) | `parentTeams`, `zoneId`, `errorHandlerConfig` (by process **slug**), `webhookAuth`, `primaryLocale`, `versions`/`aliases` (editing these releases on push — don't touch unless asked) |
| `processes/<slug>/metadata.json` | name, description, tags, `webhook` (`enabled`, `authMode: NONE\|TEAM\|CUSTOM`, `auth.variableKey` — stores the variable *name*, never a token), `form` (`enabled`, `authMode: FACTORIAL\|NONE`, marketplace `appRole: INSTALL\|SETTINGS\|USER_FACING_FORM\|UNINSTALL`) |
| `variables.env` | Variables this workspace owns (masked `********` for secrets) — committed |
| `variables.inherited.env` | From parents — pull-only, **gitignored** |
| `variables.local.env` | Local-only real secret values — never synced, never committed |
| `variables.meta.json` | Per-variable `isSensitive` (immutable once pushed) |
| `dependencies/requirements.txt` / `package.json` | Owned deps (pin here); `*.inherited.*` are pull-only |
| `.fcode/` | CLI sync state (content hashes, remotes) — local, gitignore it |
| `datastore.json`, `storage/` | Local emulation of the datastore and file storage for `fcode run` — gitignored (the CLI adds the entries) |
| `skills-lock.json`, `.agents/`, `.claude/skills/*` symlinks | Official skills installed by `fcode clone` — local tooling |

- **Variable resolution** (local runs and cloud): `variables.local.env` → `variables.env` → `variables.inherited.env`. Declaring a key *is* the override — don't copy parent variables into a child. Runtime helper `fcode.variables.set` creates variables **sensitive by default** (pass `sensitive=False` for plain config); `delete` on an inherited key is a silent no-op.
- **`base-app-py` provides** (inherited, read-only, gitignored via a CLI-managed `.gitignore` block): modules `factorial-sdk`, `factorial-utils` (company id, token validation, `setup_webhook`/list/delete — one subscription per type+company; on 422 "already taken" reuse and repoint), `fcode-logs` (`LOG_LEVEL`-gated), `fcode-utils`, `fcode-forms`, `mail-helper`, `error-handler`; processes `workspace-error-handler`, `datastore-inspector` (inspect/clean/export the datastore); variables **`FACTORIAL_BASE_URL` and `ERROR_NOTIFY_EMAIL` only**; dependency `factorial-api-client`.
- ⚠️ **`base-app-py` does *not* provide `FACTORIAL_TOKEN`, `FACTORIAL_CHALLENGE_TOKEN` or `LOG_LEVEL`** *(corrected 2026-09-01 — `fcode variables:status --showInherited` lists exactly two inherited keys)*. An earlier revision of this guide claimed it did; acting on that claim deleted a workspace-owned `FACTORIAL_CHALLENGE_TOKEN` in the belief a parent value would take over, and every webhook delivery 403'd until the value was restored by hand. **Verify what a parent actually provides with `--showInherited` before deleting any workspace-owned variable.**
- **Webhook auth is platform-level**: set `webhook.authMode: TEAM` on the process and `webhookAuth: { "headerName": "x-factorial-wh-challenge", "variableKey": "FACTORIAL_CHALLENGE_TOKEN" }` in `settings.json` — the platform **403s** invalid callers before the process runs (a correct challenge that still 403s means the workspace-side value is missing, not that the header is wrong); in-process token checking is flagged by validation. `webhookAuth` is **not inherited** — set it in every workspace addressed by a webhook URL, **and the variable it names must be owned by that same workspace**. Auth resolves against the workspace in the URL, so an inherited value is invisible to it: `variableKey` is the one Factorial variable that must *not* inherit. Webhook URL: `https://code.factorialhr.com/platform/api/<team-slug>/webhooks/<process-slug>?version_tag=stable` — **always pin `stable`**; an unknown tag silently runs the current version. `Fcode-*` headers are reserved (`Fcode-Async`, `Fcode-Version-Tag`, …).
- **Sensitive variables are opaque to the CLI — and `push` never carries their values.**
  `fcode push` / `variables:push` *creates* a sensitive variable in the cloud but uploads no value, so a freshly
  (re)created secret exists **empty** until someone types it into the Factorial Code UI. Nothing in the CLI will tell
  you: `variables:status` and `variables:diff` both report "up to date" whether or not a value exists (they compare
  only what they may read), and `contentHash` in `.fcode/remote.*.json` is `""` for **every** `isSensitive: true` key
  — redacted, not empty. Confirm a secret by exercising it (an authenticated call), never by reading CLI state.
  Corollary: **deleting a sensitive variable destroys its cloud value**, and only a human can restore it.
- **Webhook subscriptions store the challenge they were registered with.** The workspace variable and every live
  subscription must hold the *same* value — `GET /resources/api_public/webhook_subscriptions` returns `challenge`,
  so compare hashes to check. Rotating one side alone orphans the other: a freshly generated UI value does not fix a
  403, it breaks every existing subscription. Re-register them in the same pass or restore the original value.
- **OAuth scopes are baked into the issued token.** Granting a new scope on the app does **not** widen tokens already
  issued — they keep the grant they were minted with, and the endpoint keeps returning 403. Re-authorize /
  reinstall to mint a fresh token, then re-copy it into the workspace variable. A 403 (not 404) on a resource path
  means "exists, not granted"; 404 means the path itself is wrong — use the pair to tell a scope gap from a typo.
- **Schedules** can be managed from process code: `fcode.schedule.create/list/update/pause/resume/delete` (6-field cron, e.g. `0 0 6 * * SUN`, evaluated in the team's `zoneId`, or one-off `date_time`) — runtime state, **not** committed in `metadata.json`. Whether a child workspace (e.g. a `deploy-`) can schedule processes it *inherits* is unverified — the "never reschedule inherited resources" rule may apply; confirm before designing per-customer cadences around it.
- **Runtime surface** *(verified 2026-08-26)*: `fcode.team` is injected (`{baseUrl, slug}`; the inherited `fcode-utils.webhook_url(slug)` builds a process's public webhook URL from it — useful for links in task/alert bodies); `fcode.processes.run("slug")` runs another process; `fcode.execution.*` carries execution/process/schedule metadata; the inherited `error-handler` module exports `notify_failure` / `report_error` / `with_error_handler` (best-effort email via `mail-helper.branded_html` + `fcode.send_mail`).
- **i18n**: `i18n/<locale>.yaml` + `fcode.i18n("key")` (never alias the call). **MCP**: tag a process (e.g. `mcp-tool`) and it becomes an MCP tool automatically.
- **`# @add-package`** is needed only when the pip package name differs from the import name (`# @add-package argon2-cffi` above `import argon2`); pin versions in `dependencies/requirements.txt`.
- **CLI v3 team-repo layout**: one git repo per team (e.g. `factorialco/factorial-fde`) holding every app. Clone
  with `fcode team:clone`; each app is `<app>/` with a thin descriptor `settings.json` (id/name/description) and the
  **actual workspace one level down at `<app>/app/`** — that inner directory is what every `fcode` command expects
  as its cwd. `.claude/skills` inside an app is a **symlink to the team-level directory**: writing there edits every
  app's skills, so keep project-specific skills outside it.
- **Never read a CLI-managed local file as remote truth.** `variables.inherited.env`, `requirements.inherited.txt`,
  `.fcode/remote.*.json` and a freshly-cloned `parentTeams: []` all reflect the last successful *sync*, not the
  cloud. If a pull failed or a parent was detached, they will confidently describe a state that no longer exists.
  Diagnose from the cloud — an API call, an execution, `--showInherited` — before concluding anything.
- **git vs fcode are independent**: `fcode push` never uploads loose files (docs, templates, `.DS_Store`) — only registered resources. Conversely the CLI-managed `.gitignore` block covers inherited resources and local state but **not** `.DS_Store`/`__pycache__` — add those yourself, as `__pycache__/` (any depth; `*/__pycache__` matches one level only).

## 4. Choosing a platform

- Distributed to multiple Factorial customers, or reviewed/listed on the Marketplace? → **Factorial Code** (per-customer deploy workspaces, OAuth token provisioning; private apps are allow-listed and installed per company by an admin/FDE).
- Pushing payroll/ERP-supported capabilities (compensation, expenses, employee updates such as leaves) from Factorial to an external system? → Factorial Code **Integrations Framework** (`base-integration-app`'s `OutboundSync`: override `process()` and hooks, never `run()`; per-item success/invalid/failed statuses surfaced to users). Other shapes (forms, schedules, webhooks, non-supported data types) → standard app.
- Single-client, internal, or already living in an existing YepCode team? → **YepCode** is fine; keep the Wellhub deploy pattern.
- Undecided / might migrate later? → Start where delivery is fastest, follow `python-standards.md` strictly — migration is mostly mechanical (see `migrate-platform`).

## 5. Deployment workflow

**YepCode (Wellhub pattern):** git is the source of truth. `scripts/deploy.py` publishes process/module versions through the team-scoped Management API and repoints aliases; GitHub Action runs it on push (PRs = dry-run plan). Secrets: `YEPCODE_API_TOKEN`, `YEPCODE_TEAM`.

**Factorial Code** *(verified 2026-08-26)*:

1. **App creation** (console, auto-provisioned): name, purpose, **language** (selects the base workspaces, e.g. `base-app-py`), OAuth scopes (extendable later from the OAuth tab), Integrations-framework opt-in (only for supported capabilities).
2. **Build locally**: `fcode clone dev-{id}` (installs the official skills; `--skipSkillsSetup` to opt out) → edit → `fcode add` (**new** resources only) → `fcode run` / `fcode http` → `fcode push`. Pushing updates the *current* code only; consumers pinned to `stable` are untouched.
3. **Test installs** against **demo companies** in the **Dev Marketplace** (real OAuth flow; each install creates a `deploy-{installationId}` workspace; its `FACTORIAL_TOKEN` is copyable for local runs in that company's context).
4. **Validate** with the `fcode-code-validation` skill (Blocker/Warning/Suggestion → ✅/❌ `APP_VALIDATION_REPORT.md`); any Blocker blocks release.
5. **Release** from the App's Production tab: semver + notes; the platform validates (best practices, template reuse, secrets handling) and snapshots a pinned workspace version; first release creates `prod-{appId}` and flips the app to **published**.
6. **Promote** (Factorial team admin, or platform operators for partner teams — grant rides in the token, `fcode login` refreshes it): per the `fcode-release` skill — `fcode clone dev-{id}` → `remote:add prod-{id}` → `fcode pull` (mandatory) → `fcode add` → confirm → `fcode push`. Never `--force`.
7. **Rollout/rollback = moving `stable`** (web UI Versions tab or `team:aliases:set`) — never move it or publish versions unless explicitly asked.

**Org repo template caution** *(verified 2026-08-26)*: `factorialco/fde-factorialcode-template` is still the YepCode deploy harness (README, `scripts/deploy.py`, `.github/workflows/deploy.yml`, `YEPCODE_*` secrets). For a Factorial Code repo created from it, keep the `processes/`/`modules/` layout but strip the YepCode deploy wiring — the `fcode` CLI replaces it — and rewrite README/SETUP for the fcode flow.

Official skills installed by `fcode clone` (roster verified 2026-08-26; tracked in `skills-lock.json`): fcode-core-concepts, fcode-cli, fcode-python, fcode-javascript, fcode-json-schema, fcode-forms, fcode-i18n, fcode-agent, fcode-ama, fcode-examples, fcode-release, fcode-code-validation (from `factorialco/factorial-code-skills`), factorial-api-sdks (from `factorialco/factorial-api-sdks`). Don't install them reflexively elsewhere; `migrate-platform` Phase 2 says which ones a project needs.
