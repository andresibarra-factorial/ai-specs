---
name: design-docs
description: Use when creating or updating the client-facing design deliverables of an integration - the Integration Architecture docx, Reconciliation/State Design docx, or Field Mapping Spec xlsx - including producing Spanish twins.
---

# Design Docs

Produce or update the 3-doc client set per `docs/documentation-standards.md` §1, from the outlines in `templates/`:

- Architecture → `templates/architecture-doc-outline.md`
- Reconciliation/State → `templates/reconciliation-doc-outline.md`
- Field Mapping → `templates/field-mapping-outline.md`

## Rules

1. **Content before format.** The source of truth is the design session output / build brief. Every section must be backed by a decision or verified fact; unknown = it goes in "Open Decisions", never invented. Field names must exist in the pinned OAS or verified external API notes.
2. **Follow the outline exactly**: header block (title, subtitle, metadata line `Client · Source of record · Consumer · Orchestration`, version line `Version X.Y · Draft for review · CONFIDENTIAL`), auto TOC, section skeleton, tables where the outline says tables.
3. **Generation**: use the docx skill for .docx and the xlsx skill for .xlsx. Naming: `Factorial_<Client>_<DocType>.<ext>`.
4. **ES twin** (when the project requires it): full translation with the Spanish naming convention (`..._Arquitectura_de_Integracion.docx`, `..._Reconciliacion_y_Diseno_del_Estado.docx`, `..._Especificacion_Mapeo_de_Campos.xlsx`). English is canonical; produce/refresh the twin from the final English version, never edit it independently.
5. **Updates**: bump the version line, keep Appendix A manifest and env tables in sync with the build brief.

Before writing, show the user a section-by-section content plan and get approval; after writing, list open decisions carried into the doc.
