# specs — Factorial Integration Development Harness

A spec-driven development harness for building Factorial integrations and scripts with AI (Claude Chat/Cowork/Code, optionally Gemini for scripting), deployed on **YepCode** or **Factorial Code**.

Inspired by [lidr-specboot](https://github.com/LIDR-academy/lidr-specboot), adapted to our ecosystem: Python-first, Factorial API, and the documentation conventions proven in the Wellhub and IsEazy integrations.

## What's inside

```
specs/
├── CLAUDE.md / GEMINI.md      # AI entry points → bind agents to the standards
├── docs/                      # the standards (base hub + 7 specific)
│   ├── base-standards.md          # core principles, links to everything
│   ├── python-standards.md        # Python on YepCode/Factorial Code
│   ├── javascript-standards.md    # JS equivalent (Node 20/22)
│   ├── platform-guide.md          # YepCode vs Factorial Code, deploy, limits
│   ├── factorial-api-guide.md     # OAS convention, versioning, auth, quirks
│   ├── testing-standards.md       # TDD, offline harness, fcode test, verification
│   ├── documentation-standards.md # client doc set, build brief, EN/ES rule
│   └── spec-workflow.md           # lifecycle: integration track & script track
├── templates/                 # build brief, tasks, change spec, doc outlines…
└── .claude/
    ├── agents/                # peer-architect (opus) · peer-dev (sonnet) · peer-qa (sonnet)
    └── skills/                # 12 skills (see below)
```

## Skills

| Skill | Purpose |
|---|---|
| `enrich-req` | Turn a vague request/user story into an implementation-ready one |
| `explain` | Teach the concept behind a question (mental models, not quick fixes) |
| `update-docs` | Identify and update docs affected by code changes |
| `code-audit` | Phased audit: dead code, smells, security, platform violations |
| `adversarial-review` | Independent red-team pass against the spec before sign-off |
| `factorial-oas` | Find and query the latest `factorial-oas-YYYY-MM-DD.json`; flag version drift |
| `scaffold-project` | Bootstrap a new integration or script project from templates |
| `design-docs` | Generate the client doc set (Architecture, Reconciliation, Field Mapping) |
| `testing` | Build/extend the offline test harness; write and run tests; report |
| `migrate-platform` | Guided YepCode → Factorial Code migration |
| `gemini-brief` | Package a self-contained task brief for Gemini |
| `writing-skills` | Author new skills properly (TDD for process docs) |

## How to start a project

1. Open a session in this repo (or a project scaffolded from it) with Claude.
2. Say what you want to build. Claude will run `enrich-req` if the request is vague, then design with `peer-architect`.
3. For a brand-new project, ask for `scaffold-project` — it asks platform (YepCode / Factorial Code), type (integration / script), and language, then creates the repo skeleton.
4. Follow the lifecycle in `docs/spec-workflow.md`.

## Model overrides

Agent defaults: architect = opus, dev = sonnet, qa = sonnet. Override per invocation with `{model <agent>: <model>}` in your prompt, e.g. `{model architect: fable}`.

## Reference projects

- **Wellhub** — full integration under development (buffer-and-batch, offline test harness, GitHub Action deploy). Richest code reference.
- **IsEazy** — integration in architecture design phase (bilingual doc set, API research notes).
- **alsina_attendance** — small on-demand script (form-triggered Excel → attendance import).
