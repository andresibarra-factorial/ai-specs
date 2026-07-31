# Base Standards

Single source of truth for all AI agents (Claude, Gemini) working in this harness or in projects scaffolded from it. `CLAUDE.md` and `GEMINI.md` both point here.

## 1. Core principles

- **Never assume — stop and ask.** Ambiguity in requirements, mappings, endpoints, or decisions is resolved by asking the user, never by guessing. The user has the final word.
- **Baby steps.** Work in small, atomic increments. Never go forward more than one step; confirm or verify before the next.
- **TDD.** Every implementation starts with a failing test. See `testing-standards.md`.
- **Docs are the source of truth.** Specs and design docs drive code. Post-implementation change requests update artifacts first, then code (see `spec-workflow.md` §5).
- **Type safety and clarity.** Python type hints everywhere; descriptive names; every file opens with a docstring stating its public API and cross-module contracts.
- **Idempotency by default.** Platform executions have no automatic retries; processes must be safe to re-run.
- **Question repeated patterns.** If you detect duplication or a recurring pain, propose an abstraction or a standards update — but never change standards without explicit user approval.

## 2. Language

- **English** for all internal artifacts: code, comments, docstrings, tests, specs, commit messages, README files, task lists.
- **Client-facing design deliverables** (docx/xlsx doc set) are produced in English, with a Spanish twin when the project requires it (see `documentation-standards.md` §4).

## 3. Specific standards

| Standard | Covers |
|---|---|
| [python-standards.md](python-standards.md) | Python on YepCode/Factorial Code: structure, naming, platform constraints |
| [javascript-standards.md](javascript-standards.md) | JavaScript equivalent (Node 20/22) |
| [platform-guide.md](platform-guide.md) | YepCode vs Factorial Code: runtimes, deploy, limits, platform choice |
| [factorial-api-guide.md](factorial-api-guide.md) | Factorial API: OAS convention, versioning, auth, pagination, quirks |
| [testing-standards.md](testing-standards.md) | TDD, offline harness, `fcode test`, mandatory verification steps |
| [documentation-standards.md](documentation-standards.md) | Client doc set, build brief, EN/ES rule, docs-update procedure |
| [spec-workflow.md](spec-workflow.md) | Development lifecycle: integration track and script track |

## 4. Project skills

Skills live in `.claude/skills/`. When a user request matches a skill's description, load and follow the corresponding `SKILL.md` automatically — do not reimplement its workflow from memory.

## 5. Agents and model selection

| Agent | Default | Purpose |
|---|---|---|
| `peer-architect` | opus | Design partner for architecture and feasibility |
| `peer-dev` | sonnet | Atomic implementation tasks, TDD |
| `peer-qa` | sonnet | Test harness, verification, test reports |

Override per invocation: `{model <agent>: <model>}` in the user's prompt (models: `fable`, `opus`, `sonnet`, `haiku`, `inherit`). Planning and design work should run on the strongest available model; atomic implementation on sonnet unless overridden.

Gemini is an external tool, not a subagent. Hand off scripting work via the `gemini-brief` skill; Gemini CLI sessions are governed by `GEMINI.md`.

## 6. Standards self-improvement

When the user corrects the same thing twice, or a live run disproves an assumption baked into these docs (as happened with Wellhub's `BUILD_DECISIONS.md` discoveries), proactively propose a standards update. Rules: propose, don't apply; no scope creep; record platform discoveries in the project's `BUILD_DECISIONS.md` and propose promotion to these standards when they generalize.
