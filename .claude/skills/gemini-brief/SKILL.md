---
name: gemini-brief
description: Use when handing off a task to Gemini - "prepare this for Gemini", "make a Gemini brief", or when the user decides a low-level/scripting task will be done with Gemini CLI or Gemini chat.
---

# Gemini Brief

Package a **self-contained** task brief so Gemini can execute without access to this session's context. Two consumption modes: Gemini CLI running in the repo (reads `GEMINI.md` + files), or chat copy-paste (needs everything inline).

## Workflow

1. Ask which mode (CLI or chat) if not stated.
2. Write the brief to `briefs/YYYY-MM-DD-<task-slug>.md`:

```
# Task Brief — <task>
## Objective            — one paragraph, the exact outcome expected
## Context              — project, platform (YepCode|Factorial Code), language/runtime, pinned API version
## Task                 — atomic steps, in order (from tasks.md when applicable)
## Contracts            — exact function signatures, module names, API endpoints/fields (verified via factorial-oas), fixture examples
## Constraints          — the platform rules that apply: main() wrapper, literal-string imports,
                          naming (underscore modules / hyphen slugs), @add-package pinned deps,
                          datastore key charset, no secrets in logs, idempotency
## Acceptance criteria  — tests that must pass (name the test files/commands), DoD
## Out of scope         — what NOT to touch
## Report back          — ask Gemini to end with: files changed, test results, open questions
```

3. **CLI mode**: keep file references as paths (Gemini reads them; `GEMINI.md` binds it to the standards). **Chat mode**: inline the relevant standards excerpts and file contents — the brief must stand alone.
4. On return: review Gemini's output like any external contribution — run the full offline suite yourself, then the normal verification steps. Gemini's "tests pass" is not verification.
