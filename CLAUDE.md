# Factorial Integration Harness — Entry Point (Claude)

This repository is the harness for designing and building Factorial integrations and scripts, deployed on YepCode or Factorial Code. It is spec-driven: documentation is the source of truth, code follows.

## Read first

Read `docs/base-standards.md` before doing anything. It links every other standard. All work in this repo and in projects scaffolded from it follows those standards.

## Golden rules (non-negotiable)

1. **Never assume. Stop and ask.** If anything is foggy — a field mapping, an endpoint, a decision — ask the user before proceeding.
2. **Baby steps.** One small task at a time. Never move forward more than one step without confirmation or a passing test.
3. **TDD.** Start with a failing test. No task is checked off until its tests pass and the verification steps in `docs/testing-standards.md` are done. Never delegate testing to the user.
4. **Docs first.** Any change requested after implementation starts must update the spec/design artifacts first, then the code.

## Skills

Skills live in `.claude/skills/`. When a request matches a skill's description, load and follow its SKILL.md automatically. Roster: `enrich-req`, `explain`, `update-docs`, `code-audit`, `adversarial-review`, `factorial-oas`, `scaffold-project`, `design-docs`, `testing`, `migrate-platform`, `gemini-brief`, `writing-skills`.

## Agents

Agents live in `.claude/agents/`:

| Agent | Default model | Role |
|---|---|---|
| `peer-architect` | opus | Design partner: explore options, evaluate feasibility, co-design integrations |
| `peer-dev` | sonnet | Implement atomic tasks with TDD |
| `peer-qa` | sonnet | Build/run test harnesses, verify, write test reports |

**Model override convention:** the user may override any agent's model per invocation by writing `{model <agent>: <model>}` in the prompt — e.g. `{model architect: fable}` or `{model dev: opus}`. When present, launch the agent with that model instead of its default. `inherit` means use the current session's model.

For low-level or scripting work the user may prefer Gemini: use the `gemini-brief` skill to package a handoff, and note `GEMINI.md` binds Gemini CLI to these same standards.

## Workflow

The lifecycle (full detail in `docs/spec-workflow.md`):
request → `enrich-req` → design with `peer-architect` (feasibility checked against the latest Factorial OAS via `factorial-oas`) → spec + tasks from `templates/` → implement with `peer-dev` → verify with `peer-qa` + `adversarial-review` → `update-docs` → commit.

Light scripts follow the reduced track defined in the same doc.
