---
name: migrate-platform
description: Use when moving a project from YepCode to Factorial Code (or planning that move) - "migrate to fcode", "port this to Factorial Code", or assessing migration effort.
---

# Migrate Platform (YepCode → Factorial Code)

Guided, checklist-driven migration. Start with an **assessment report**, migrate only after the user approves it. Mechanics verified against a real `fcode clone` (2026-08-26); the cloned workspace's official `fcode-*` skills are the authority on platform behavior — read `fcode-cli` and `fcode-core-concepts` alongside this.

## Phase 0 — Workspace

Create the App in the console (language selects the base workspaces, e.g. `base-app-py`; OAuth scopes extendable later), `fcode clone dev-{id}`, then **merge the workspace into the project repo** (default; record if the user chooses otherwise): copy `.fcode/`, `team.json`, `variables*` + `variables.meta.json`, `dependencies/`, the inherited modules/processes, `.agents/` + skill symlinks + `skills-lock.json`, and the CLI's `.gitignore` block (add `.DS_Store` and `__pycache__/` yourself — the block doesn't cover them). From then on `fcode add/run/push` from the repo root; the original clone folder is disposable.

## Phase 1 — Assess

Inventory the project and score each item:

| Area | Check |
|---|---|
| Runtime | Python 3.12→3.13 / Node 20→22 incompatibilities (rare, but check pinned deps) |
| Global object | every `yepcode.*` reference → `fcode.*` |
| Imports | `yepcode.import_module` → `fcode.import_module` (literal strings; existing snake_case module slugs may stay — kebab-case is the platform convention, naming is a validation Warning; decide with the user) |
| Entry points | `main()` defined but **never self-invoked** (self-invocation is a validation Blocker) |
| Factorial client | custom `factorial_client`/`auth_factorial` → adapter over the inherited **`factorial-sdk`** (`create_factorial_client()`, `request_body()`); webhook management via `factorial-utils.setup_webhook` (one per type+company; 422 → reuse/repoint) |
| Webhook auth | in-code challenge checks → platform auth: `metadata.json` `webhook.authMode: TEAM` + `team.json` `webhookAuth {x-factorial-wh-challenge, FACTORIAL_CHALLENGE_TOKEN}` (not inherited — set per workspace). Callers pin `?version_tag=stable` |
| Forms | per-process `metadata.json` `form.enabled` + `authMode` (`FACTORIAL` restricts to the installing company's users; a public form handling credentials is a validation **Blocker**) + marketplace `appRole` |
| Deps | pins → `dependencies/requirements.txt`; `# @add-package` only where import name ≠ package name; never redeclare parent-provided packages |
| Deploy | `scripts/deploy.py` + GitHub Action retire; `fcode push` syncs registered resources plus the app-level `README.md` / `MARKETPLACE.md` / `CHANGELOG.md` at `<app>/` (git and fcode are otherwise independent). Add `MARKETPLACE.md` (`app-marketplace` skill) — YepCode projects never had one |
| Email/errors | wire `team.json` `errorHandlerConfig` → inherited `workspace-error-handler` (+ `ERROR_NOTIFY_EMAIL`); `fcode.send_mail` (3/execution) for other mail |
| Tests | harness fake global renamed; static checks exclude inherited (kebab-case, read-only) resources; keep the offline suite green throughout |
| Secrets | `credentials/*.json` disappear; real values only in `variables.local.env`; `variables.meta.json` `isSensitive` is immutable once pushed |

Output: findings table + effort estimate + open decisions (App name/vendor slug, module-naming choice, forms auth, marketplace vs private app, state-migration mechanics).

## Phase 2 — Migrate

Create a change (`spec.md` + `tasks.md`) from the approved assessment; execute per the normal lifecycle (TDD — the offline harness migrates first and stays green throughout). Verify with the full suite + `fcode run`/`fcode http` against a demo company, then gate with the official **`fcode-code-validation`** skill (any Blocker → fix before requesting release). Release = request from the App's Production tab (semver + notes); promotion follows the official `fcode-release` skill; rollout/rollback is the **`stable` alias** — never move it or publish versions unless explicitly asked.

Record every surprise in `BUILD_DECISIONS.md`; propose promoting generalizable ones to `docs/platform-guide.md`.
