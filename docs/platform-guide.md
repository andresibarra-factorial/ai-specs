# Platform Guide — YepCode vs Factorial Code

Both platforms run the same engine (Factorial acquired YepCode; Factorial Code is its evolution integrated with Factorial). The platform is chosen **case by case per project**, declared in the build brief. Projects may start on YepCode and later migrate (see the `migrate-platform` skill).

## 1. Side-by-side

| Area | YepCode | Factorial Code |
|---|---|---|
| Docs | https://yepcode.io/docs/ | https://code.factorialhr.com/docs (preprod: code.eu2.preproduction.factorialhr.com/docs) |
| Global SDK object | `yepcode.*` (injected) | `fcode.*` (`from fcode import fcode, logger`) |
| Python / Node | 3.12 / 20 | **3.13 / 22** |
| CLI | `@yepcode/cli` | `@factorialco/fcode-cli` (`fcode clone/run/push/http/test`) |
| Unit of delivery | Team of processes | **App**: `dev-{id}` → review/CI → read-only `prod-{id}` → per-customer `deploy-{id}` workspaces |
| Code reuse | Modules within the team | Modules + **workspace inheritance** (`base-app`, `base-integration-app`; read-only, non-transitive) |
| Factorial API | Your own client + credentials (api key / OAuth) | **`FactorialClient`** from `base-app`; `FACTORIAL_TOKEN` auto-provisioned per customer; OAuth scopes declared at App creation |
| Testing | Local `run` only → our offline harness | **`fcode test`** framework (input/output/error JSON, hooks, CI exit codes) + `fcode http` local webhook server + our offline harness |
| Deploy | Git repo + GitHub Action → YepCode Management API (Wellhub pattern: branch → alias `br-<branch>`, `main` → `production`) | `fcode push` to dev workspace; release request → Factorial review + CI → prod; customers auto-provision deploy workspaces |
| Email | Bring your own | `fcode.sendMail` built in (3/execution) |
| Secrets locally | `credentials/*.json` + `variables.env` | `variables.local.env` (never synced); no credentials folder |
| Multi-tenancy | One team per client (our convention) | Per-customer deploy workspace with isolated variables/token |

## 2. Shared engine facts (both platforms)

- Triggers: on-demand, cron/schedules, webhooks (per-process URL), embedded forms (JSON Schema / react-jsonschema-form), REST API, MCP.
- **Sync webhook timeout: 60s** (HTTP 408; execution continues). Prefer async acknowledgment.
- No automatic retries at process level — code must be idempotent and re-runnable. Wire a workspace/team error-handler process (ships in `base-app` on Factorial Code).
- Datastore: team-level KV, strings/numbers, size/entry limits. Storage: cloud files. Local disk: ephemeral.
- Logs capped (lines and size) — log summaries.
- Dependency installs happen asynchronously after manifest changes; executions use the old set until done.
- Static egress IP for allowlisting (Factorial Code: `34.89.54.108`).
- Engine limits (timeouts, memory) are plan-dependent on YepCode and not published for Factorial Code — **confirm hard limits with the platform team before designing around them**.

## 3. Choosing a platform

Default questions the build brief must answer:

- Will this be distributed to multiple Factorial customers, or reviewed/listed on the Marketplace? → **Factorial Code** (per-customer deploys, OAuth token provisioning).
- Does it push payroll/ERP-supported capabilities (compensation, expenses, leave updates)? → Factorial Code **Integrations Framework** (per-item retries and status surfaced to users).
- Single-client, internal, or already living in an existing YepCode team? → **YepCode** is fine; keep the Wellhub deploy pattern.
- Undecided / might migrate later? → Start where delivery is fastest, but follow `python-standards.md` strictly — the standards are written so a migration is mostly mechanical (see `migrate-platform`).

## 4. Deployment workflow

**YepCode (Wellhub pattern):** git is the source of truth. `scripts/deploy.py` publishes process/module versions through the team-scoped Management API and repoints aliases; GitHub Action runs it on push (PRs = dry-run plan). Secrets: `YEPCODE_API_TOKEN`, `YEPCODE_TEAM`.

**Factorial Code:** `fcode clone dev-{app-id}` → build with skills/samples → `fcode run` + `fcode test` locally → `fcode push` → test from a Factorial demo environment → request release (review + CI) → prod → customer activation runs the `{vendor}-setup` form process.

Also install the official platform skills in Factorial Code projects: `npx skills add factorialco/factorial-code-skills` (fcode-core-concepts, fcode-python, fcode-javascript, fcode-json-schema, fcode-cli, fcode-forms, fcode-examples).
