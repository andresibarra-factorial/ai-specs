# Documentation Standards

## 1. The client design doc set (integration track)

Every full integration produces three deliverables, named `Factorial_<Client>_<DocType>.<ext>`:

| Deliverable | Format | Outline template |
|---|---|---|
| Integration Architecture | .docx | `templates/architecture-doc-outline.md` |
| Reconciliation & Resolution/State Design | .docx | `templates/reconciliation-doc-outline.md` |
| Field Mapping Spec | .xlsx | `templates/field-mapping-outline.md` |

House style (all docs): header block with two-line title (doc type + integration name), one-line subtitle, metadata line (`Client · Source of record · Consumer · Orchestration`), version line (`Version X.Y · Draft for review · CONFIDENTIAL`), then auto TOC. Each architecture doc opens by naming **the defining architectural fact** of the integration (e.g. Wellhub: real-time webhooks vs async batch → buffer-and-batch). Inventories and configs are tables, flows are narrated step-by-step per lifecycle event.

Generation is handled by the `design-docs` skill.

## 2. The build brief (`docs/CLAUDE.md` in each project)

Source of truth for **decisions** (design docs are source of truth for **detail**). Template: `templates/build-brief.md`. It must contain: what we're building, golden rules ("no assumptions — stop and ask"), source-of-truth doc list, locked decisions, systems/API reference, environment-variable table (with per-environment values and Sensitive flag), component manifest (processes + modules), repo layout, conventions, and decisions still open.

Paired with `docs/BUILD_PROMPT.md` (template: `templates/build-prompt.md`): the dependency-ordered generation plan for implementation.

`BUILD_DECISIONS.md` (repo root) records verified platform/API discoveries from live runs.

## 3. Code-level documentation

- Docstring header per file: purpose, public API, cross-module contracts.
- `README.md` catalog per `modules/`, `processes/`, `test/` directory: table of items with responsibilities and dependencies.
- Process `README.md` files are deployed with the process — keep them accurate.

## 4. Language rule

English for everything internal. Client deliverables (§1) are written in English; when the project requires it, produce a Spanish twin with the mirrored naming convention (e.g. `Factorial_<Client>_Arquitectura_de_Integracion.docx`, `..._Especificacion_Mapeo_de_Campos.xlsx`). The English version is canonical; twins are translations, never forks.

## 5. Update procedure (before any commit)

Review what the change touched and update accordingly:

| Changed | Update |
|---|---|
| Data model / mappings | Field Mapping Spec (+ ES twin), build brief §systems |
| Endpoints / API usage | factorial-api section of the build brief; fixtures |
| Modules / processes added or changed | Directory README catalogs, component manifest, Architecture doc Appendix A |
| Env vars | Environment-variable table |
| Platform discovery from a live run | `BUILD_DECISIONS.md` |
| Decisions made | Build brief §locked decisions (move from §open) |
| Any change to a **released** project | `CHANGELOG.md` entry (see §6) |

The `update-docs` skill automates this review. Docs update is a mandatory task in every `tasks.md` (see `spec-workflow.md`).

## 6. Project logs — BUILD_DECISIONS.md and CHANGELOG.md

Every project keeps two root-level logs, both created (empty, with header) at scaffold time:

**`BUILD_DECISIONS.md`** — verified platform/API discoveries from live runs (the Wellhub pattern). Entry format: date, discovery, evidence (what run/response proved it), and the code/design consequence. When a discovery generalizes beyond the project, propose promoting it to the harness standards (base-standards §6) — but the project log keeps the original record.

**`CHANGELOG.md`** — the release history. Rules:

- The file stays **empty (header only) until the first version is pushed/released**. Pre-release iteration is not changelog material — that history lives in the change folders and git.
- The moment a version is released (deployed to production alias on YepCode, or promoted to prod on Factorial Code), every subsequent change lands as an entry classified as **Fix**, **Improvement**, or **Maintenance**.
- Entry format:

```
## [<version or release tag>] — YYYY-MM-DD
### Fix | Improvement | Maintenance
- <one line per change, linking the change-id, e.g. (specs/changes/add-eligibility-gate)>
```

- The changelog is written for a reader who wasn't in the room: state the observable effect, not the internal refactor detail.
- Updating it is part of the close step of every change on a released project (`spec-workflow.md` §2.7) — a change on a released project is not closed without its changelog entry.

## 7. Self-improvement rule

Learn from user feedback and propose documentation/standards improvements proactively — but never modify standards or templates without explicit user approval, never scope-creep beyond what was asked, and always confirm after applying.
