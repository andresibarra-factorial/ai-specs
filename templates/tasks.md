# Tasks: <change-id>

> Rules: one task at a time, TDD (test task precedes its implementation task), a task is `[x]` only after the verification steps in `testing-standards.md` §5. Never delegate testing to the user.

## 0. Setup

- [ ] 0.1 Create feature branch `feature/<change-id>`
- [ ] 0.2 Confirm pinned OAS version still current (`factorial-oas` skill); flag drift if any

## 1. <Component / requirement>

- [ ] 1.1 Write failing tests for <behavior> (happy, error, edge)
- [ ] 1.2 Implement <behavior> to green
- [ ] 1.3 Update fixtures if API payloads changed

<Repeat groups in dependency order.>

## N-2. Verification

- [ ] Run full offline suite (`python3 test/run.py`) — all green
- [ ] Factorial Code: `fcode test` — all green
- [ ] Verify and restore any state touched (datastore/fixtures)
- [ ] Write verification report → `reports/YYYY-MM-DD-<task>-verification.md`

## N-1. Review

- [ ] `adversarial-review` against `spec.md` — verdict PASS (or gaps resolved)

## N. Documentation & close

- [ ] `update-docs` per documentation-standards §5 (catalogs, manifest, mapping spec, env table, BUILD_DECISIONS)
- [ ] Released project? Add `CHANGELOG.md` entry (Fix / Improvement / Maintenance)
- [ ] Commit + PR (imperative English message, ticket prefix, no secrets, sole authorship — the user's own git identity; no `Co-Authored-By: Claude`/"Generated with Claude Code" or similar attribution trailer unless the user asks for one)
