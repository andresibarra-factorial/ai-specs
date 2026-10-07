---
name: update-docs
description: Use when code has been implemented or modified, when closing a task or change, or when the user asks to update documentation - identifies which docs are affected by the changes and updates them.
---

# Update Docs

Apply `docs/documentation-standards.md` §6. The three app-level platform files (`README.md`, `MARKETPLACE.md`, `CHANGELOG.md` at the project root, §3) are pushed with the app — a close that leaves any of them stale ships stale customer-visible text.

## Workflow

1. Determine what changed: the current change's `tasks.md`/`spec.md`, or `git diff` against the merge base if no change folder exists.
2. Map changes to documents using the table in documentation-standards §6 (mappings → Field Mapping Spec; endpoints → build brief systems section + fixtures; components → README catalogs + manifest + Architecture Appendix A; env vars → variable table; live discoveries → BUILD_DECISIONS.md; decisions → build brief §locked; **released project → CHANGELOG.md entry** classified Fix / Improvement / Maintenance per documentation-standards §7; **root `README.md`** refreshed through the `app-readme` skill whenever anything it states changed — and always after a changelog entry, since its §9 is derived from `CHANGELOG.md`; **`MARKETPLACE.md`** (Factorial Code apps) refreshed through the `app-marketplace` skill whenever a capability, synced entity, requirement or support detail changed).
3. Update each affected document. For docx/xlsx client deliverables, update via the `design-docs` skill; if the project keeps an ES twin, update it too (translation, never a fork).
4. Report: docs updated, docs checked-but-unaffected, and anything you could not update with a reason.

Never mark a change closed with stale catalogs, manifests, root README or marketplace listing. If code and spec disagree, stop — that's an artifacts-first violation (`spec-workflow.md` §5); ask the user.
