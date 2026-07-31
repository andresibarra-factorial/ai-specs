# Build Brief — Factorial ↔ <Client/System> <Integration|Script>

> Copy to the project's `docs/CLAUDE.md`. This file is the source of truth for **decisions**. Design docs are the source of truth for **detail**. If they conflict, stop and ask.

## 1. What we're building

<One paragraph: systems, direction of data flow, trigger model, and the defining architectural fact (e.g. "Wellhub ingests async batches while Factorial emits real-time webhooks → buffer-and-batch").>

## 2. Golden rules

- No assumptions — stop and ask.
- Standards: this project follows the `specs` harness (`base-standards.md` and everything it links).
- Pinned Factorial API version: `<YYYY-MM-DD>` (OAS file: `factorial-oas-<YYYY-MM-DD>.json`).
- Platform: <YepCode | Factorial Code> · Language: <Python 3.12/3.13 | Node 20/22> · Track: <integration | script>

## 3. Source-of-truth documents

| Document | Governs |
|---|---|
| `Factorial_<Client>_Integration_Architecture.docx` | Architecture, flows, auth, env |
| `Factorial_<Client>_Reconciliation_and_Resolution_Design.docx` | Matching, tiers, state |
| `Factorial_<Client>_Field_Mapping_Spec.xlsx` | Field-level mappings |
| `BUILD_DECISIONS.md` | Verified platform/API discoveries |

## 4. Locked decisions

| # | Decision | Rationale | Date |
|---|---|---|---|
| 1 | | | |

## 5. Systems reference

<Per system: base URL, auth scheme, key endpoints used (verified against the pinned OAS), rate limits, webhook contract.>

## 6. Environment variables

| Variable | Purpose | Sandbox | Production | Sensitive |
|---|---|---|---|---|
| | | | | |

## 7. Component manifest

### Processes
| Slug | Trigger | Responsibility |
|---|---|---|

### Modules
| Name | Layer | Responsibility | Depends on |
|---|---|---|---|

## 8. Repo layout

<Tree, per `python-standards.md` §1.>

## 9. Conventions

<Project-specific deltas from the standards, if any. Default: none.>

## 10. Decisions still open

| # | Question | Options | Owner |
|---|---|---|---|
