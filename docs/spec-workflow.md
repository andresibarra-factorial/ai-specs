# Spec Workflow

Documentation is the source of truth; code follows. Two tracks depending on project type (declared in the build brief):

- **Integration track** — full integrations with external systems (Wellhub, IsEazy class).
- **Script track** — low-level scripts / small API interactions (alsina class): same lifecycle, lighter artifacts.

## 1. Change artifacts

All work is organized as **changes** under `specs/changes/` in the project repo:

```
specs/changes/<change-id>/          # change-id: kebab-case, e.g. add-eligibility-gate
├── spec.md                         # from templates/change-spec.md — what & why, requirements, scenarios
├── tasks.md                        # from templates/tasks.md — ordered atomic checklist
└── reports/                        # verification reports (testing-standards.md §5)
```

## 2. Integration track lifecycle

0. **Assess** — a new request to connect Factorial with a third-party system starts with the `feasibility-assessment` skill: the Integration Feasibility Assessment (`documentation-standards.md` §1.1) gives the verdict, the gaps, the integration options and the open questions before anything is enriched, designed or quoted. Proceed only once the verdict is at least *Feasible with conditions* and every blocking item has an owner.
1. **Enrich** — vague request? Run `enrich-req`. Output: implementation-ready requirement.
2. **Design** — session with `peer-architect` (strongest model): explore ≥2 options with trade-offs, evaluate feasibility against `platform-guide.md` and the **latest OAS** (`factorial-oas` skill), decide platform and patterns. New project? `scaffold-project` first.
3. **Document** — decisions land in the build brief (§locked decisions); for client-facing phases, `design-docs` produces/updates the 3-doc set; the root `README.md` (`app-readme`, documentation-standards §3.1) and, on Factorial Code, `MARKETPLACE.md` (`app-marketplace`, §3.2) are refreshed once the architecture is decided.
4. **Specify** — create the change folder: `spec.md` (requirements + WHEN/THEN scenarios) and `tasks.md`. Task 0 is always *create feature branch*; final tasks are always *verification* (testing-standards §5) and *update docs* (documentation-standards §6).
5. **Implement** — `peer-dev` executes tasks one at a time, TDD, checking off only after verification. Low-level pieces may be handed to Gemini via `gemini-brief`.
6. **Review** — `peer-qa` runs the full suites; then `adversarial-review` (fresh session/agent) red-teams the implementation against `spec.md`. Verdict PASS / PASS WITH GAPS / FAIL gates completion. `code-audit` on demand for broader health checks. Factorial Code projects add the platform's own gate before any release request: the official `fcode-code-validation` skill (any Blocker → no release).
7. **Close** — `update-docs`; if the project is **released** (a version has been pushed to production), add the `CHANGELOG.md` entry (Fix / Improvement / Maintenance, per `documentation-standards.md` §7) and refresh the root `README.md` with `app-readme` (its §9 derives from the changelog) and, when the change touched what the listing claims, `MARKETPLACE.md` with `app-marketplace`; commit (imperative English messages, ticket prefix when applicable, never secrets, sole authorship — the user's own git identity, no `Co-Authored-By: Claude` or similar attribution trailer unless asked for), PR.

## 3. Script track lifecycle

Same discipline, smaller surface:

1. `enrich-req` if the request is vague.
2. Short design consult with `peer-architect` only if there are real options to weigh (trigger type, identity resolution, file handling); otherwise skip.
3. Single `spec.md` + `tasks.md` in one change folder. No client doc set — the build brief (`docs/CLAUDE.md`) plus the root `README.md` on the canonical template (`app-readme`, documentation-standards §3.1; sections with nothing to say get `N/A — <reason>`) are enough; a script shipped as a Factorial Code app still carries a `MARKETPLACE.md` (§3.2).
4. Implement (`peer-dev` or Gemini via `gemini-brief`), verify (offline harness still required, sized to the script), `adversarial-review` optional but recommended for anything writing to Factorial.
5. Close: same rule as the integration track — released script + any change = `CHANGELOG.md` entry, and the root README refreshed.

## 4. Statuses

A change is **open** while tasks remain unchecked, **implemented** when all tasks are `[x]`, **verified** after adversarial-review passes, **closed** after docs are updated and the work is merged. Keep closed changes in place — they are the project's history.

A **project** is *unreleased* until its first version is pushed to production (YepCode production alias / Factorial Code prod promotion), and *released* after. Release flips the changelog rule on: from then, every closed change adds a `CHANGELOG.md` entry.

## 5. Artifacts-first rule (post-implementation changes)

Any fix or new requirement requested after implementation has started must:

1. Update `spec.md` / design docs / build brief **first**.
2. Regenerate or amend `tasks.md`.
3. Only then touch code, re-running the affected tests.

Silently patching code against an outdated spec is a violation — the spec must always describe what the code does.
