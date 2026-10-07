---
name: app-readme
description: Use when a project needs its root README.md created or refreshed - after scaffold-project, when closing a change (update-docs), before a release request, when the user asks for "the app README", "the integration README", "catalogue README" or "update the README", or when a root README exists that does not follow templates/app-readme.md.
---

# App README

Produce or refresh the project's root `README.md` on the canonical template `templates/app-readme.md`, per `docs/documentation-standards.md` §3.1. **Destination:** the project root — on a Factorial Code team repo that is `<app>/README.md`, beside `app/`, `settings.json` and its siblings `MARKETPLACE.md` (`app-marketplace` skill) and `CHANGELOG.md`, never inside `<app>/app/`. The platform pushes the file with the app, and the output feeds the FDE Integration Catalogue, so structure is not negotiable: nine sections, exact headings, exact table columns, exact order.

## Workflow

1. **Load the template and the current README.** If a root README exists and does not follow the template, tell the user you will restructure it and carry over every fact that has evidence; drop nothing silently — list what did not fit.
2. **Gather evidence, in this precedence order:** build brief `docs/CLAUDE.md` (decisions, env table, manifest) → design doc set (architecture, reconciliation, field mapping) → code (`processes/`, `modules/`, `settings.json`/`team.json`, `metadata.json`, `parametersSchema.json`, `requirements.txt`) → `BUILD_DECISIONS.md` → `CHANGELOG.md` → pinned OAS (`factorial-oas` skill) for API versions and endpoints. Note the source of every fact as you go; §2 "Evidence" cells cite it.
3. **Ask for the metadata (AskUserQuestion, one call).** Client, Market, Status, Integration Type, Owner, Jira Epic, Production Date. On a refresh, show the current values and ask only for confirmation/changes. Never infer these from repo contents.
4. **Ask for anything that is a decision, not a fact.** Rollback ownership, who may release, environments not yet documented. Facts that are simply missing become `To be confirmed`; things the user says do not apply become `N/A — <reason>`.
5. **Fill every section.** Keep placeholders' meaning, remove the template blockquote and every `<...>`. Tables: one row per item, `To be confirmed` in a cell rather than an empty cell; an empty table gets one row of `To be confirmed`.
6. **Derive §9 from `CHANGELOG.md`:** one row per `## [version] — date` heading, newest first; Change = entry lines prefixed by their class (`Fix: …; Improvement: …`); Jira / PR = the bracketed reference or `—`. No `CHANGELOG.md` entries → single row `— | — | Unreleased | —`.
7. **Validate before writing** (all must hold): the nine `## N.` headings present in order; every table header line identical to the template; no `<`/`>` placeholders; no hedging phrases (`I assume`, `probably`, `presumably`, `it is likely`, `might be`, `could be`, `I believe`); no secrets or PII; §9 row count equals the number of released versions.
8. **Write `README.md`, then report:** sections fully backed by evidence, cells left `To be confirmed` (grouped by section, with what would resolve them), and any conflict found between the README sources (build brief vs code vs design docs) — a conflict is an artifacts-first violation (`spec-workflow.md` §5): stop and ask, do not paper over it.

## Output format

Exactly `templates/app-readme.md` with the blockquote removed. English only (`base-standards.md` §2). Line width free; tables not padded.

## Guardrails

- Never invent an endpoint, version, variable, schedule, mapping or behaviour. "It is obviously X" is not evidence — cite a file or say `To be confirmed`.
- Never edit §9 by hand or from memory of what shipped — only from `CHANGELOG.md`. If the changelog is stale, fix it first (documentation-standards §7).
- Never change the template's headings, column names or section order "to fit this project". A section that does not apply still appears, with `N/A — <reason>`.
- Never write the README while the build brief and the code disagree — surface the conflict.
- Never guess metadata from folder names, client names in code or git history.
- Never write the README inside the fcode workspace (`<app>/app/README.md`) or leave two copies; if one exists there, move its facts up to `<app>/README.md` and tell the user to delete it.
- The FDE README Generator app (local `fcode run` from the team repo) produces the same template at the same destination for apps developed outside this harness; do not run it from a harness project — this skill has the same evidence plus the design session.
- Never paste marketplace copy into the README or README facts into `MARKETPLACE.md`; each file has its own register (documentation-standards §3).
