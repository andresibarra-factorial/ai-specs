# Outline — Field Mapping Spec (.xlsx)

File: `Factorial_<Client>_Field_Mapping_Spec.xlsx` (ES twin: `Factorial_<Client>_Especificacion_Mapeo_de_Campos.xlsx`)

## Tabs (in order)

1. **Cover** — title, metadata line, version line, tab index.
2. **<Domain> Mapping** — one tab per mapped domain (e.g. "Employee Eligibility Mapping", "Training Catalog Mapping", "Enrollment & Progress Mapping"). Columns: Source system · Source field (exact API path, verified against pinned OAS) · Target system · Target field · Transformation rule · Required · Default · Notes.
3. **Identity & Link Table** — the key model: external key(s) ↔ Factorial employee_id, resolution order, storage location (datastore key pattern).
4. **Operation Mapping** — lifecycle events → API operations (e.g. hire → POST …, terminate → …), including inferred-operation rules where webhooks carry no event type.
5. **Notification Model** — (if the design has one) event → audience (HR task vs technical alert) → channel.
6. **Company Scope** — legal entities / companies in scope, per-entity config.
7. **Reconciliation Match Rules** — mirrors the tier table from the reconciliation doc.
8. **Open Items** — unresolved mappings with owner and blocking status.

Rule: every source/target field name must exist in the pinned OAS or the external system's verified API notes — no invented field names.
