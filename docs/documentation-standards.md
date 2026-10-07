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

## 3. The app-level platform files — `README.md`, `MARKETPLACE.md`, `CHANGELOG.md`

Every project ships a set of app-level Markdown files at the **project root**. On a Factorial Code CLI v3 team repo (`platform-guide.md` §3) the project root is the app folder `<app>/`, so they live at `<app>/README.md`, `<app>/MARKETPLACE.md` and `<app>/CHANGELOG.md` — beside `app/`, the descriptor `settings.json` and `.gitignore`, **never** inside the workspace `<app>/app/`. The platform **pushes exactly these three files from `<app>/`** with the app (they are the only loose files it accepts there; everything else at that level stays git-only), so they are produced and maintained as development goes, not written once at release. The same location rule places every other harness artifact of an app: `<app>/docs/CLAUDE.md`, `<app>/BUILD_DECISIONS.md`, `<app>/specs/changes/`, `<app>/test/`. On YepCode the project root is the repo root; YepCode projects ship `README.md` and `CHANGELOG.md` only (there is no marketplace listing).

| File | Audience | Canonical template | Produced / refreshed by | Rules |
|---|---|---|---|---|
| `README.md` | Engineers, the FDE Integration Catalogue | `templates/app-readme.md` | `app-readme` skill | §3.1 |
| `MARKETPLACE.md` | Buyers and admins on the Factorial Marketplace (Apps → Publication fields) | `templates/app-marketplace.md` | `app-marketplace` skill | §3.2 |
| `CHANGELOG.md` | Everyone — release history, shown as-is | header in §7 | `update-docs` at every close on a released project | §3.3, §7 |

All three are created at scaffold (`scaffold-project`) and refreshed in the close step of every change (`update-docs`, §6). A change is not closed with any of them stale.

### 3.1 `README.md` — the app-level README

Every project — integration or script track, YepCode or Factorial Code — ships a root `README.md` that follows the canonical template `templates/app-readme.md` **exactly**: nine numbered sections, same headings, same table columns, same order. It is the entry point for anyone landing in the repo and the source content of the **FDE Integration Catalogue**, which parses this structure.

Rules:

- **Created at scaffold, refreshed at close.** `scaffold-project` creates it through the `app-readme` skill; `update-docs` refreshes it in the close step of every change (§6). A change is not closed with a stale root README. The platform pushes the file with the app, so it is customer-visible from the first release.
- **Evidence-bound.** Every fact is backed by the build brief, the design doc set, the code, `BUILD_DECISIONS.md`, `CHANGELOG.md` or the pinned OAS. Unknown → `To be confirmed`; explicitly not applicable → `N/A — <reason>`. No hedging language (`probably`, `might be`, `I assume`) and no unresolved `<placeholders>`.
- **Metadata (§1) is asked, never guessed.** Client, Market, Status, Integration Type, Owner, Jira Epic and Production Date are collected from the user when the README is created and confirmed on each refresh; they are not stored anywhere else.
- **§9 Changelog is derived from `CHANGELOG.md`** (§7): one row per released version, newest first, the Jira/PR reference taken from the entry lines. An unreleased project shows a single `Unreleased` row. Never edit §9 by hand.
- **No duplication with `MARKETPLACE.md`.** The README states facts for engineers; the marketplace listing sells outcomes to buyers. The same fact may appear in both, in each file's register — never copy sections across.
- **Precedence.** The build brief (`docs/CLAUDE.md`) remains the source of truth for decisions and the design docs for detail; the README summarizes them and must never contradict them. If it does, fix the source first (`spec-workflow.md` §5).
- **Sensitive data.** Variable names and public sandbox values only — never tokens, keys or PII.
- **Same template, two producers.** The `app-readme` skill produces it inside a Claude Code session from the repo. The **FDE README Generator** app (Factorial Code, `factorial-fde/fde-readme-generator`) exists for apps **not** developed with this harness: run locally from the cloned team repo (`fcode run generate-readme` with the target's dev workspace id), it reads the target app's repo files and an optional Solution Architecture PDF, produces the identical structure and writes it to the same destination, `<app>/README.md`. Its `readme-template` module mirrors `templates/app-readme.md`; this file is the canonical copy — change it here first.

### 3.2 `MARKETPLACE.md` — the marketplace listing

Factorial Code apps ship `<app>/MARKETPLACE.md` on the canonical template `templates/app-marketplace.md`: the fill-ready content of the **Apps → \<app\> → Publication** screen, one section per field, each within the field's limit (Tagline 140 characters · Full description 5,000 · Screenshots up to 10, PNG/JPEG/WebP, 2 MB each · Support and Help links 2,000 · Marketplace visibility). The file is the source the listing is filled from; DatoCMS content, when present, overrides it field by field.

Rules:

- **Written for the buyer and the admin, never the developer.** Plain language, outcomes first; no component, process or module names, no endpoints, no internal jargon. The full description keeps the template's order: *What is \<External system\>?* → *Benefits* → *How it works* → *What is synced* → *Requirements* → *Screenshots* → *Support*.
- **Evidence-bound, like the README.** Every capability claimed must exist in the build brief, the design doc set or the code; the *What is synced* table is a plain-language view of the Field Mapping Spec, and *Requirements* derive from the feasibility assessment / build brief (modules, credentials, data prerequisites). Unknown → `To be confirmed`. No hedging and no `<placeholders>` left.
- **Limits are checked, not eyeballed.** The tagline states its character count; the full description is counted before writing.
- **Visibility is asked, never guessed** (Private allow-listed vs Public), as are the support and help links.
- **Created at scaffold** (sections with nothing yet to say get `To be confirmed`), **refreshed at every close** through `update-docs` → `app-marketplace`, and reviewed before every release request. On YepCode projects the file does not exist.

### 3.3 `CHANGELOG.md` — the release history

The format and the rules live in §7. Because the platform pushes the file with the app and shows it as-is, the changelog is written for the customer-facing reader as much as for the team: observable effects, never refactor detail. It is also the single source of README §9.

## 4. Code-level documentation

- Docstring header per file: purpose, public API, cross-module contracts.
- `README.md` catalog per `modules/`, `processes/`, `test/` directory: table of items with responsibilities and dependencies.
- Process `README.md` files are deployed with the process — keep them accurate.

## 5. Language rule

English for everything internal. Client deliverables (§1) are written in English; when the project requires it, produce a Spanish twin with the mirrored naming convention (e.g. `Factorial_<Client>_Arquitectura_de_Integracion.docx`, `..._Especificacion_Mapeo_de_Campos.xlsx`). The English version is canonical; twins are translations, never forks.

## 6. Update procedure (before any commit)

Review what the change touched and update accordingly:

| Changed | Update |
|---|---|
| Data model / mappings | Field Mapping Spec (+ ES twin), build brief §systems |
| Endpoints / API usage | factorial-api section of the build brief; fixtures |
| Modules / processes added or changed | Directory README catalogs, component manifest, Architecture doc Appendix A |
| Env vars | Environment-variable table |
| Platform discovery from a live run | `BUILD_DECISIONS.md` |
| Decisions made | Build brief §locked decisions (move from §open) |
| Any change to a **released** project | `CHANGELOG.md` entry (see §7) |
| Anything the root README states (flow, components, APIs, config, run/deploy steps, releases) | Root `README.md` via the `app-readme` skill (§3.1) — always re-derive §9 after a changelog entry |
| Anything the marketplace listing claims (capabilities, synced entities, requirements, support links) — Factorial Code apps | `MARKETPLACE.md` via the `app-marketplace` skill (§3.2) |

The `update-docs` skill automates this review. Docs update is a mandatory task in every `tasks.md` (see `spec-workflow.md`).

## 7. Project logs — BUILD_DECISIONS.md and CHANGELOG.md

Every project keeps two root-level logs, both created (empty, with header) at scaffold time:

**`BUILD_DECISIONS.md`** — verified platform/API discoveries from live runs (the Wellhub pattern). Entry format: date, discovery, evidence (what run/response proved it), and the code/design consequence. When a discovery generalizes beyond the project, propose promoting it to the harness standards (base-standards §6) — but the project log keeps the original record.

**`CHANGELOG.md`** — the release history. Rules:

- The file stays **empty (header only) until the first version is pushed/released**. Pre-release iteration is not changelog material — that history lives in the change folders and git.
- The moment a version is released (deployed to production alias on YepCode, or promoted to prod on Factorial Code), every subsequent change lands as an entry classified as **Fix**, **Improvement**, or **Maintenance**.
- Entry format:

```
## [<version or release tag>] — YYYY-MM-DD
### Fix | Improvement | Maintenance
- <one line per change, linking the change-id and, when it exists, the Jira key or PR, e.g. (specs/changes/add-eligibility-gate) [KEY-123 / PR #45]>
```

- The changelog is written for a reader who wasn't in the room: state the observable effect, not the internal refactor detail.
- Updating it is part of the close step of every change on a released project (`spec-workflow.md` §2.7) — a change on a released project is not closed without its changelog entry.
- It is the single source for the root README §9 table (§3.1): the version and date come from the heading, the Change cell joins the entry lines prefixed by their class, the Jira/PR cell takes the bracketed reference. Keep entries one line each so the derivation stays mechanical.
- The platform pushes `<app>/CHANGELOG.md` with the app and displays it **as-is** (free-form Markdown, no required schema) — this format is ours to keep; write every entry so a customer admin can read it.

## 8. Self-improvement rule

Learn from user feedback and propose documentation/standards improvements proactively — but never modify standards or templates without explicit user approval, never scope-creep beyond what was asked, and always confirm after applying.
