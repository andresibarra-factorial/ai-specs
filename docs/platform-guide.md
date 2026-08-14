# Platform Guide — YepCode vs Factorial Code

Both platforms run the same engine (Factorial acquired YepCode; Factorial Code is its evolution integrated with Factorial). The platform is chosen **case by case per project**, declared in the build brief. Projects may start on YepCode and later migrate (see the `migrate-platform` skill).

## 1. Side-by-side

| Area | YepCode | Factorial Code |
|---|---|---|
| Docs | https://yepcode.io/docs/ | https://code.factorialhr.com/docs |
| Global SDK object | `yepcode.*` (injected) | `fcode.*` (`from fcode import fcode, logger`) |
| Python / Node | 3.12 / 20 | **3.13 / 22** |
| CLI | `@yepcode/cli` | `@factorialco/fcode-cli` (`fcode clone/run/push/http/test`) |
| Unit of delivery | Team of processes | **App**: `dev-{id}` → tagged **workspace version** (review + CI) → `production` alias on read-only `prod-{id}` → per-customer `deploy-{id}` workspaces (variables only, no code) |
| Code reuse | Modules within the team | Modules + **workspace inheritance** (`base-app`, `base-integration-app`; read-only, non-transitive) |
| Factorial API | Your own client + credentials (api key / OAuth) | **`FactorialClient`** from `base-app`; `FACTORIAL_TOKEN` auto-provisioned per customer; OAuth scopes declared at App creation |
| Testing | Local `run` only → our offline harness | **`fcode test`** framework (input/output/error JSON, hooks, CI exit codes) + `fcode http` local webhook server + our offline harness |
| Deploy | Git repo + GitHub Action → YepCode Management API (Wellhub pattern: branch → alias `br-<branch>`, `main` → `production`) | `fcode push` to dev workspace; release request → Factorial review + CI → prod; customers auto-provision deploy workspaces |
| Email | Bring your own | `fcode.sendMail` built in (3/execution) |
| Secrets locally | `credentials/*.json` + `variables.env` | `variables.local.env` (never synced); no credentials folder |
| Multi-tenancy | One team per client (our convention) | Per-customer deploy workspace with isolated variables/token |

## 2. Shared engine facts (both platforms)

- Triggers: on-demand, cron/schedules, webhooks (per-process URL), embedded forms (JSON Schema / react-jsonschema-form), REST API, MCP.
- **Sync webhook timeout: 60s** (HTTP 408; execution continues). Prefer async acknowledgment. Webhook control headers on Factorial Code use the `Fcode-*` prefix (`Fcode-Async`, `Fcode-Version-Tag`, `Fcode-Comment`, `Fcode-Initiated-By`; responses carry `Fcode-Execution-ID`).
- No automatic retries at process level — code must be idempotent and re-runnable. Wire a workspace/team error-handler process (ships in `base-app` on Factorial Code). *(Retry behavior is documented for the YepCode engine; Factorial Code docs don't restate it — treat as engine-level fact until confirmed.)*
- Datastore: team-level KV, strings/numbers, size/entry limits. **Paid-plans-only on Factorial Code** — confirm availability before designing state around it. Storage: cloud files (Factorial Code adds the `@factorialco/fcode-sdk` / `factorial-fcode-sdk` external SDK with signed URLs and automatic form-file uploads). Local disk: ephemeral.
- Logs capped (lines and size) — log summaries. *(Caps documented for YepCode; unstated for Factorial Code — assume they apply.)*
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

**Factorial Code:** App creation in the console is auto-provisioned — no approval step (approval applies only to initial platform access); OAuth scopes are optional at creation and can be added later from the App's OAuth tab. Then: `fcode clone dev-{app-id}` → build with skills/samples → `fcode run` + `fcode test` locally → `fcode push` → test from a Factorial demo environment → **request release, which publishes a tagged workspace version of `dev-{app-id}`** (Factorial review + CI) → promotion points the `production` alias of `prod-{app-id}` at that tag → customer activation runs the `{vendor}-setup` form process.

The CLI clone also versions per-process `metadata.json` (webhook/form config, auth mode) and `team.json` (timezone, parents, error handler, versions/aliases) — treat them as committable config artifacts, not generated noise.

Official platform skills are installed by `fcode clone` by default (`--skipSkillsSetup` to opt out; manual: `npx skills add factorialco/factorial-code-skills` — fcode-core-concepts, fcode-python, fcode-javascript, fcode-json-schema, fcode-cli, fcode-forms, fcode-examples, fcode-agent). Roster confirmed against `code.factorialhr.com/docs/skills` on 2026-08-13 — re-verify before relying on it, Factorial adds skills over time. Don't install all of them reflexively; `migrate-platform` Phase 2 gives per-skill guidance on which ones a given project actually needs.

**Known doc inconsistencies (Factorial Code docs, as of 2026-08):** the `fcode test` page names workspace env layers `.env.local`/`.env` while the rest of the CLI docs use `variables.local.env`; the datastore page shows `fcode.datastore.delete()` while test-hook examples use `del_()`. Verify empirically before relying on either name.
