# Outline — Reconciliation & Resolution/State Design (.docx)

File: `Factorial_<Client>_Reconciliation_and_Resolution_Design.docx` (ES twin: `Factorial_<Client>_Reconciliacion_y_Diseno_del_Estado.docx`). Same header block as the architecture doc (see `architecture-doc-outline.md`).

## Sections

1. **Purpose & Context** — why reconciliation exists in this integration; relationship to the architecture doc.
2. **Reconciliation Process** — inputs (both systems' record sets) and the comparison flow.
3. **Matching Logic & Auto-Resolve Tiers** — the tier table:

   | Tier | Condition | Uniqueness requirement | Action | Confidence |
   |---|---|---|---|---|
   | A | <deterministic match, e.g. national ID> | unique on both sides | auto-link | high |
   | B | <secondary key, e.g. email> | unique | auto-link | medium |
   | C | <fallback> | — | <manual queue / exclusion-tombstone> | low |

   Tier C strategy is per project: manual-resolution queue (Wellhub) or deterministic exclusion/tombstone (IsEazy). State the choice and why.
4. **Unresolved Queue / Exclusion Model** — storage, aging, notification.
5. **Manual Resolution Form** — if applicable: fields, validation, who operates it.
6. **Identity & Access (RBAC)** — who sees/does what.
7. **Security** — PII handling in reconciliation artifacts.
8. **One-Time Backfill Runbook** — ordered steps, restore points, abort criteria.
9. **Open Items**
