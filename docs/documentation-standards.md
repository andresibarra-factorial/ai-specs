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

The `update-docs` skill automates this review. Docs update is a mandatory task in every `tasks.md` (see `spec-workflow.md`).

## 6. Self-improvement rule

Learn from user feedback and propose documentation/standards improvements proactively — but never modify standards or templates without explicit user approval, never scope-creep beyond what was asked, and always confirm after applying.
