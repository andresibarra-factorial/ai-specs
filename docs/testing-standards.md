# Testing Standards

TDD is mandatory. The agent executes all tests itself — **never delegate testing to the user**. A task may be checked `[x]` only after its tests pass and a verification report exists.

## 1. TDD cycle

1. Write the failing test first (RED) — it must fail for the right reason.
2. Minimal implementation to pass (GREEN).
3. Refactor with tests green.

Test categories required per public function: happy path, error cases, edge cases, input validation. Integration-level tests per process flow.

## 2. The offline harness (Wellhub pattern — required in every project)

A zero-live-API suite that runs anywhere with plain `python3 test/run.py`:

```
test/
├── run.py                 # discovers and runs all suites, exit code 0/1
├── harness/
│   ├── yc_runtime.py      # fake platform runtime: injects the `yepcode`/`fcode` global
│   │                      # (context.parameters, env, datastore, import_module, storage)
│   └── http_mock.py       # routes ALL HTTP; no test ever hits a live API
├── fixtures/              # recorded/synthetic API payloads, per system
│   ├── factorial/
│   └── <other_system>/
├── test_static.py         # platform-constraint checks (see §3)
├── test_foundation.py     # config, log_utils, http_client
├── test_auth_clients.py
├── test_repos.py
├── test_domain.py
└── test_e2e.py            # full process flows through the fake runtime
```

Suites are layered to mirror the architecture; fixtures are the contract record — update them when the pinned OAS version changes.

## 3. Static checks (`test_static.py`)

Automated enforcement of platform constraints that only fail at deploy time otherwise:

- Every `import_module` / `import` call uses a **literal string** argument.
- Module names are valid Python identifiers; process slugs are hyphenated.
- Every process has a `main()`; no top-level `return`.
- No stdlib-shadowing module names.
- Datastore keys built only through the sanctioned `make_key` helper.

Extend this file whenever a new deploy-time failure mode is discovered.

## 4. `fcode test` (Factorial Code projects)

In addition to the offline harness, ship `fcode test` suites per process:

- `processes/<slug>/tests/<NN-name>/input.json` (+ `output.json` for exact-match, or `error.json` for expected failure; omit both = smoke test).
- Env overrides: per-test `variables.test.env` > global `tests/variables.test.env` > `.env.local` > `.env`.
- Hooks (`testHooks.py` `before`/`after`) for setup/teardown with full `fcode.*` access.
- Exit codes are CI-ready: gate `fcode push` and release requests on a green run.
- `fcode http` for local webhook-flow testing.

## 5. Mandatory verification steps (before checking off any implementation task)

1. Run the full offline suite (`python3 test/run.py`) — all green.
2. Factorial Code: run `fcode test` — all green.
3. If the task touched state, verify datastore/fixture state pre/post and restore it.
4. Write a verification report from `templates/test-report.md` into `specs/changes/<change-id>/reports/YYYY-MM-DD-<task>-verification.md`.
5. Only then mark the task `[x]` and run `update-docs`.

Any live-environment testing (demo tenant, real webhooks) is a separate, explicitly user-approved step — record outcomes and surprises in `BUILD_DECISIONS.md`.
