---
name: code-audit
description: Use when the user asks for a code audit, health check, dead-code sweep, security review of the codebase, or a general "how is this project doing" quality assessment.
---

# Code Audit

Systematic, phased audit of a Factorial integration/script project. Not a spec-compliance check (that's `adversarial-review`) — this is codebase health.

## Phases

1. **Setup** — read the build brief, standards, deploy config; establish the pinned OAS version and target platform; run the offline suite for a baseline.
2. **Inventory** — list all modules/processes/tests; cross-check against the README catalogs and component manifest (drift here is a finding).
3. **File-by-file** — for each file: dead code (Python: `vulture` or `deadcode`, verify false positives before reporting), code smells, complexity, duplication, error-handling gaps, deprecated API usage.
4. **Platform-constraint compliance** — everything `test_static.py` checks plus: log volume discipline, datastore key hygiene, idempotency of processes, webhook validation present, secrets never logged/committed, pinned dependencies.
5. **Security & data** — PII in logs/fixtures, injection risks in datastore keys or file handling, webhook auth, token handling (no hand-rolled credential code on Factorial Code).
6. **Pattern detection** — repeated code that wants a module; violations of the layering rule (domain importing processes, etc.).

## Report

```
# Audit — <project> — YYYY-MM-DD
## Executive summary
## Critical issues            (fix before next deploy)
## Findings by file           ### [CRITICAL|HIGH|MEDIUM|LOW] <title> — location, description, recommendation
## Quick wins
## Prioritized action plan    (with effort estimates)
```

Every finding needs evidence (file:line or command output). Propose fixes; apply nothing without user approval.
