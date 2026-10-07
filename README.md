# specs — Factorial Integration Development Harness

A spec-driven development harness for building Factorial integrations and scripts with AI (Claude Chat/Cowork/Code, optionally Gemini for scripting), deployed on **YepCode** or **Factorial Code**.

Inspired by [lidr-specboot](https://github.com/LIDR-academy/lidr-specboot), adapted to our ecosystem: Python-first, Factorial API, and the documentation conventions proven in the Wellhub and IsEazy integrations.

## What's inside

```
specs/
├── CLAUDE.md / GEMINI.md      # AI entry points → bind agents to the standards
├── docs/                      # the standards (base hub + 8 specific)
│   ├── base-standards.md          # core principles, links to everything
│   ├── python-standards.md        # Python on YepCode/Factorial Code
│   ├── javascript-standards.md    # JS equivalent (Node 20/22)
│   ├── platform-guide.md          # YepCode vs Factorial Code, deploy, limits
│   ├── factorial-api-guide.md     # OAS convention, versioning, auth, quirks
│   ├── testing-standards.md       # TDD, offline harness, fcode test, verification
│   ├── documentation-standards.md # client deliverables (feasibility assessment + design set), build brief, app-level platform files, EN/ES rule
│   ├── branding.md                # Factorial brand for deliverables + Markdown → branded docx rendering
│   └── spec-workflow.md           # lifecycle: integration track & script track
├── templates/                 # feasibility-assessment.md, build brief, tasks, change spec, doc outlines, app-readme + app-marketplace…
│   ├── docx/                      # the Feasibility Assessment template as a ready-to-use branded .docx (also the renderer's brand source)
│   └── data/                      # Factorial module ↔ API namespace mapping, OAS 2026-07-01 domain/endpoint lists
├── scripts/render_fde_docx.py # Markdown → Factorial-branded .docx
└── .claude/
    ├── agents/                # peer-architect (opus) · peer-dev (sonnet) · peer-qa (sonnet)
    └── skills/                # 15 skills (see below)
```

## Skills

| Skill | Purpose |
|---|---|
| `feasibility-assessment` | Assess a request to connect Factorial with a third-party system: verdict, gaps, integration options, open questions — rendered as the branded Integration Feasibility Assessment docx |
| `enrich-req` | Turn a vague request/user story into an implementation-ready one |
| `explain` | Teach the concept behind a question (mental models, not quick fixes) |
| `update-docs` | Identify and update docs affected by code changes |
| `code-audit` | Phased audit: dead code, smells, security, platform violations |
| `adversarial-review` | Independent red-team pass against the spec before sign-off |
| `factorial-oas` | Find and query the latest `factorial-oas-YYYY-MM-DD.json`; flag version drift |
| `scaffold-project` | Bootstrap a new integration or script project from templates |
| `design-docs` | Generate the client doc set (Architecture, Reconciliation, Field Mapping) |
| `app-readme` | Create or refresh the root `README.md` on the canonical app-level template (Integration Catalogue source; pushed with the app) |
| `app-marketplace` | Create or refresh `MARKETPLACE.md`, the Factorial Marketplace listing (Publication fields, within their limits; pushed with the app) |
| `testing` | Build/extend the offline test harness; write and run tests; report |
| `migrate-platform` | Guided YepCode → Factorial Code migration |
| `gemini-brief` | Package a self-contained task brief for Gemini |
| `writing-skills` | Author new skills properly (TDD for process docs) |

## How to start a project

1. Open a session in this repo (or a project scaffolded from it) with Claude.
2. Say what you want to build. For a new third-party integration request Claude starts with `feasibility-assessment`; then `enrich-req` if the request is vague, then design with `peer-architect`.
3. For a brand-new project, ask for `scaffold-project` — it asks platform (YepCode / Factorial Code), type (integration / script), and language, then creates the repo skeleton.
4. Follow the lifecycle in `docs/spec-workflow.md`. The root `README.md` (and, on Factorial Code, `MARKETPLACE.md`) is created by `app-readme` / `app-marketplace` at scaffold time and refreshed at every change close; `CHANGELOG.md` starts at the first release. The three files are pushed to the platform with the app.

## Model overrides

Agent defaults: architect = opus, dev = sonnet, qa = sonnet. Override per invocation with `{model <agent>: <model>}` in your prompt, e.g. `{model architect: fable}`.

## Reference projects

- **Wellhub** — full integration under development (buffer-and-batch, offline test harness, GitHub Action deploy). Richest code reference.
- **IsEazy** — integration in architecture design phase (bilingual doc set, API research notes).
- **alsina_attendance** — small on-demand script (form-triggered Excel → attendance import).
