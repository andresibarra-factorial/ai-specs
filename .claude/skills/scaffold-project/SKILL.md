---
name: scaffold-project
description: Use when starting a new Factorial integration or script project - "new project", "scaffold", "bootstrap", "set up the repo for X". Creates the repo skeleton, build brief, test harness, and deploy wiring from the harness templates.
---

# Scaffold Project

Bootstrap a new project governed by this harness. **Ask before generating** — never scaffold on assumptions.

## Step 1 — Intake (AskUserQuestion)

1. **Track**: full integration | light script (defines doc set and lifecycle per `spec-workflow.md`).
2. **Platform**: YepCode | Factorial Code | undecided (guide with `platform-guide.md` §3; undecided → YepCode-compatible code, strict standards for easy migration).
3. **Language**: Python (default) | JavaScript.
4. **Client/system name**, ticket prefix if any, and whether an ES doc twin is required.
5. Locate the latest OAS (`factorial-oas` skill) → propose the pin.

## Step 2 — Generate

```
<project>/                    # Factorial Code: the app folder <app>/ in the team repo; the fcode workspace goes to <app>/app/
├── docs/CLAUDE.md            # from templates/build-brief.md, pre-filled with intake answers
├── docs/BUILD_PROMPT.md      # from templates/build-prompt.md (integration track)
├── BUILD_DECISIONS.md        # empty, with header (live-run discoveries log)
├── CHANGELOG.md              # header only — stays empty until first release (documentation-standards §7)
├── README.md                 # app-level README from templates/app-readme.md via the `app-readme` skill (documentation-standards §3.1) — at <app>/, never inside <app>/app/
├── MARKETPLACE.md            # Factorial Code only — marketplace listing from templates/app-marketplace.md via the `app-marketplace` skill (documentation-standards §3.2)
├── CLAUDE.md → points to docs/CLAUDE.md + the harness standards; GEMINI.md equivalent
├── modules/README.md         # empty catalog table
├── processes/README.md
├── test/                     # offline harness skeleton per testing-standards.md §2
│   ├── run.py  harness/yc_runtime.py  harness/http_mock.py  fixtures/factorial/  test_static.py
├── specs/changes/            # empty
├── .gitignore                # .env, venv, logs, local variables
└── platform wiring:
    ├── YepCode: scripts/deploy.py + .github/workflows/deploy.yml (copy Wellhub pattern)
    └── Factorial Code: `app/` = the workspace from `fcode clone dev-{app-id}` (run inside <app>/); `npx skills add factorialco/factorial-code-skills` at the team-repo root
```

The harness skeleton must pass `python3 test/run.py` immediately (empty-but-green), and `test_static.py` ships with all platform-constraint checks active.

After generating the skeleton, run the `app-readme` skill: it asks for the Catalogue metadata (client, market, status, type, owner, Jira epic, production date) and fills what the intake answers already settle; everything else is `To be confirmed` until design lands. On Factorial Code, then run the `app-readme` sibling `app-marketplace`: it asks visibility, support/help links and the external system's one-liner, and leaves every unsupported claim as `To be confirmed`. Never leave either file as the template with raw `<placeholders>` — `README.md`, `MARKETPLACE.md` and `CHANGELOG.md` are pushed to the platform with the app (documentation-standards §3).

## Step 3 — Hand off

Summarize what was created, list the build brief's open sections the user must fill or design with `peer-architect`, and point to the lifecycle in `spec-workflow.md`. Do not start designing or implementing — that's the next phase, user-initiated.
