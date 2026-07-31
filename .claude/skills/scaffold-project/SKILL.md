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
<project>/
├── docs/CLAUDE.md            # from templates/build-brief.md, pre-filled with intake answers
├── docs/BUILD_PROMPT.md      # from templates/build-prompt.md (integration track)
├── BUILD_DECISIONS.md        # empty, with header
├── CLAUDE.md → points to docs/CLAUDE.md + the harness standards; GEMINI.md equivalent
├── modules/README.md         # empty catalog table
├── processes/README.md
├── test/                     # offline harness skeleton per testing-standards.md §2
│   ├── run.py  harness/yc_runtime.py  harness/http_mock.py  fixtures/factorial/  test_static.py
├── specs/changes/            # empty
├── .gitignore                # .env, venv, logs, local variables
└── platform wiring:
    ├── YepCode: scripts/deploy.py + .github/workflows/deploy.yml (copy Wellhub pattern)
    └── Factorial Code: note to run `fcode clone dev-{app-id}` and `npx skills add factorialco/factorial-code-skills`
```

The harness skeleton must pass `python3 test/run.py` immediately (empty-but-green), and `test_static.py` ships with all platform-constraint checks active.

## Step 3 — Hand off

Summarize what was created, list the build brief's open sections the user must fill or design with `peer-architect`, and point to the lifecycle in `spec-workflow.md`. Do not start designing or implementing — that's the next phase, user-initiated.
