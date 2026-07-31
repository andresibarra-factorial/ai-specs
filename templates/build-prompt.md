# Build Prompt — <Project>

> Copy to the project's `docs/BUILD_PROMPT.md`. The dependency-ordered code-generation plan, paired with the build brief.

## Role

You are implementing the <project> integration per `docs/CLAUDE.md` (decisions) and the design docs (detail), under the `specs` harness standards.

## Hard constraints

- Confirm before coding anything not covered by a locked decision.
- TDD per `testing-standards.md`; offline harness first (Group 1).
- One group at a time; do not start a group until the previous one is green.

## Generation order

| Group | Components | Depends on |
|---|---|---|
| 1 — Foundation | `config`, `log_utils`, `http_client`, test harness (`yc_runtime`, `http_mock`) | — |
| 2 — Auth + clients | `auth_<system>`, `<system>_client`, `factorial_client` | 1 |
| 3 — State repos | `kv_store`, `<link/buffer/queue>_repo` | 1 |
| 4 — Domain | <transformer, gate, matching, orchestrator…> | 2, 3 |
| 5 — Processes | <process slugs> | 4 |
| 6 — E2E tests + docs | `test_e2e`, README catalogs, doc updates | 5 |

## Per-component contract

For each component state: public API (functions + signatures), modules it may import, fixtures it needs, and its test file. Fill this table before generating Group 1.
