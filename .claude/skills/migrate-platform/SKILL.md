---
name: migrate-platform
description: Use when moving a project from YepCode to Factorial Code (or planning that move) - "migrate to fcode", "port this to Factorial Code", or assessing migration effort.
---

# Migrate Platform (YepCode → Factorial Code)

Guided, checklist-driven migration. Start with an **assessment report**, migrate only after the user approves it.

## Phase 1 — Assess

Inventory the project and score each item:

| Area | Check |
|---|---|
| Runtime | Python 3.12→3.13 / Node 20→22 incompatibilities (rare, but check pinned deps) |
| Global object | every `yepcode.*` reference → `fcode.*`; Python adds `from fcode import fcode, logger` |
| Imports | `yepcode.import_module` → `fcode.import_module` (literal strings unchanged) |
| Factorial client | custom `factorial_client`/`auth_factorial` → **`FactorialClient`** from `base-app`; credentials/env auth → provisioned `FACTORIAL_TOKEN` (OAuth scopes are optional at App creation and can be added later from the App's OAuth tab — still list the scopes the code needs) |
| Deps | `# @add-package` works as-is; also register in `dependencies/requirements.txt` |
| Deploy | `scripts/deploy.py` + GitHub Action → `fcode` CLI flow (`clone dev-{id}`, `push`, release request → tagged workspace version → `production` alias promotion); decide the repo's new sync model; `metadata.json`/`team.json` become committable artifacts |
| Structure | single team → App workspaces (dev/prod/deploy); per-customer variables move to deploy workspaces; check `base-integration-app` fit (OutboundSync) if pushing payroll/ERP capabilities |
| Email | any SMTP/mail code → `fcode.sendMail` (3/execution cap) |
| Tests | harness fake global renamed; add `fcode test` suites + `fcode http` for webhooks |
| Secrets | `credentials/*.json` disappear; local dev uses `variables.local.env` |

Output: findings table + effort estimate + open decisions (App name, scopes, marketplace intent).

## Phase 2 — Migrate

Create a change (`spec.md` + `tasks.md`) from the approved assessment; execute per the normal lifecycle (TDD — the offline harness migrates first and stays green throughout). Verify with the full suite + `fcode test` + `fcode run` against a demo environment before requesting release.

Record every surprise in `BUILD_DECISIONS.md`; propose promoting generalizable ones to `docs/platform-guide.md`.
