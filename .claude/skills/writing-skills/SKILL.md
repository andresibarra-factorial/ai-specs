---
name: writing-skills
description: Use when creating a new skill, editing an existing skill, or verifying a skill works before adding it to this harness.
---

# Writing Skills

Writing skills is TDD applied to process documentation. **Iron law: no skill without a failing test first** — and that applies to edits too.

## The cycle

1. **RED** — before writing anything, run the target scenario with a subagent (or fresh session) WITHOUT the skill. Record verbatim where it goes wrong: what it assumes, skips, or rationalizes. If it already succeeds, the skill isn't needed.
2. **GREEN** — write the minimal SKILL.md that fixes those observed failures. Nothing speculative.
3. **REFACTOR** — re-run the scenario WITH the skill. Close the loopholes it still finds: add explicit negations ("never X, even when Y"), red-flag lists, and the rationalizations you observed, verbatim, with rebuttals.

## Anatomy

```
---
name: verb-first-kebab-name
description: Use when <triggering conditions ONLY - never summarize the workflow here>
---
# Title
<Overview - one paragraph>
## Workflow / rules  <numbered, imperative>
## Output format     <exact, when the skill produces artifacts>
## Guardrails        <explicit negations, red flags>
```

- Description = triggering conditions only, starting "Use when…". A workflow summary in the description is a documented failure mode: the agent follows the summary and never reads the body.
- Keep it under ~500 words; move heavy reference material to `references/*.md` inside the skill folder and link it (progressive disclosure).
- One excellent example beats five mediocre ones.
- Frontmatter description ≤1024 chars; include the keywords users actually say.

## Harness integration

New skills live in `.claude/skills/<name>/SKILL.md`, get a row in `README.md`'s skill table and, if always-relevant, a mention in `CLAUDE.md`. Standards changes triggered by a skill still require user approval (base-standards §6).

## Guardrails

- Never ship a skill whose failure scenario you haven't run. Untested skill = delete it and start over.
- Never edit a skill to "clarify" without re-running its scenario — clarity that doesn't change behavior is noise.
