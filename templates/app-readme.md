# <Integration name>

> **Canonical app-level README template.** Copy to the project's root `README.md` — on a Factorial Code team repo that is `<app>/README.md`, beside `app/`, `settings.json` and `.gitignore`, **never** inside `<app>/app/`. Rules: `docs/documentation-standards.md` §3. Every section and every table column below is mandatory and must keep its exact heading and order — the FDE Integration Catalogue and the FDE README Generator app parse this structure. Unknown = `To be confirmed`; explicitly not applicable = `N/A — <one-line reason>`. Never invent a fact. Delete this blockquote when copying.

## 1. Overview

### Metadata

| Field | Value |
| --- | --- |
| Client | <Client or "Internal"> |
| Market | <ES / FR / PT / IT / DE / UK / Multi / N/A> |
| Status | <Discovery / In development / In testing / Live / Deprecated> |
| Integration Type | <Inbound / Outbound / Bidirectional / Script / Marketplace app> |
| Owner | <FDE owner name> |
| Jira Epic | <KEY-123 or To be confirmed> |
| Production Date | <YYYY-MM-DD or To be confirmed> |

### Purpose

<One paragraph: business problem solved, who benefits, and the defining architectural fact (mirrors build brief §1).>

### Integration Flow

**Source:** <system of record the data leaves>

**Integration / Middleware:** <YepCode team / Factorial Code app slug, plus any queue, buffer or file drop in between>

**Destination:** <system that receives the data>

### Trigger & Frequency

* **Trigger:** <webhook / schedule / embedded form / on-demand / REST / MCP>
* **Frequency:** <cron in plain words, or "on event" / "manual">

## 2. Architecture & APIs

### Systems & Components

| Component | Confirmed responsibility | Evidence |
| --- | --- | --- |
| <process or module slug> | <one line> | <file path, design doc section or BUILD_DECISIONS entry> |

### API Details

| System | Role | API Version | Base URL | Method | Endpoint | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| Factorial | <source/destination> | <pinned OAS date YYYY-MM-DD> | <base URL> | <GET/POST/…> | <path> | <one line> |

## 3. Authentication & Configuration

### Authentication

<Per system: scheme (OAuth app token via `FACTORIAL_TOKEN`, API key, HMAC…), where the credential lives, rotation notes. Never the value.>

### Configuration

<Environment/team variables table or list: name, purpose, sensitive flag, per-environment value where public. Mirrors build brief §6.>

## 4. Data Mapping

| Source Field | Destination Field | Transformation / Notes |
| --- | --- | --- |
| <field> | <field> | <rule, or "direct"> |

<If a Field Mapping Spec xlsx exists, list only the key identity/matching fields here and link the spec in §8.>

## 5. How to Run

<Local run (`fcode run <slug> --parameters …` / offline harness `python3 test/run.py`), manual trigger path, and the inputs an operator must provide. Numbered steps.>

## 6. Errors & Troubleshooting

| Error / Issue | Cause | Resolution |
| --- | --- | --- |
| <symptom as the operator sees it> | <confirmed cause> | <steps> |

## 7. Deployment & Rollback

### Deployment

<Factorial Code: `fcode push` → release request (semver + notes) → promote `stable`. YepCode: `scripts/deploy.py` via GitHub Action. State the workspace / team and who may release.>

### Rollback

<How `stable` is moved back (Factorial Code) or aliases repointed (YepCode); data-side rollback if any; who executes it.>

## 8. References

* <Solution Architecture / design doc set, with location>
* <Field Mapping Spec>
* <Jira epic, PRs, runbooks, external API docs>

## 9. Changelog

| Version | Date | Change | Jira / PR |
| --- | --- | --- | --- |
| <x.y.z> | <YYYY-MM-DD> | <Fix / Improvement / Maintenance: one line per entry, joined with "; "> | <KEY-123 / PR #n or —> |

<Derived from the project's `CHANGELOG.md` (documentation-standards §7): one row per released version, newest first. Unreleased project: a single row `— | — | Unreleased | —`.>
