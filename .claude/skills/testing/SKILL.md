---
name: testing
description: Use when writing tests, setting up or extending the offline test harness, running verification passes, or when a task needs its mandatory pre-checkoff verification. Also for adding fcode test cases on Factorial Code projects.
---

# Testing

Apply `docs/testing-standards.md`. For substantial test work, prefer delegating to the `peer-qa` agent with this skill's checklist.

## Harness work

New project or missing harness → scaffold `test/` per testing-standards §2: `run.py`, `harness/yc_runtime.py` (fake `yepcode`/`fcode` global: `context.parameters`, `env`, `datastore`, `import_module`, `storage`), `harness/http_mock.py` (routes ALL HTTP), `fixtures/`, layered `test_*.py` suites, and `test_static.py` with the full platform-constraint checklist. It must run green immediately.

## Writing tests

- Failing test first, always; confirm it fails for the right reason before implementing.
- Per public function: happy, error, edge, validation. Per process: e2e flow through the fake runtime.
- Fixtures mirror the pinned OAS version; name them by system and scenario (`fixtures/factorial/employee_create_null_email.json`).
- Factorial Code: add `fcode test` cases per process (`tests/NN-name/input.json` + `output.json`|`error.json`, hooks for setup/teardown).

## Verification pass (before any task is checked off)

1. `python3 test/run.py` — full suite green.
2. `fcode test` green (Factorial Code).
3. State touched? Verify pre/post and restore.
4. Report from `templates/test-report.md` → `specs/changes/<id>/reports/YYYY-MM-DD-<task>-verification.md`.

Never delegate testing to the user; never report results you didn't run.
