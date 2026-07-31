---
name: enrich-req
description: Use when a request, user story, or ticket for a Factorial integration/script is vague, incomplete, or not implementation-ready, or when the user asks to "enrich", "refine", or "make precise" a requirement before design or development.
---

# Enrich Requirement

Act as a product/integration expert. Transform a raw request into an implementation-ready requirement — without inventing decisions the user hasn't made.

## Completeness checklist

A requirement is ready when it states:

1. **Functionality** — full behavior description, trigger model (webhook / schedule / form / on-demand), direction of data flow.
2. **Factorial surface** — resources and endpoints involved, verified against the pinned OAS (run `factorial-oas` if unsure); API version pinned.
3. **External system surface** — endpoints/files/contracts on the other side, with source (docs, API research notes).
4. **Data** — fields involved, mappings or a pointer to the Field Mapping Spec, identity keys.
5. **Affected components** — modules/processes to create or modify (from the build brief manifest).
6. **Definition of Done** — observable outcomes, including error behavior.
7. **Tests & docs** — which suites and docs the change must update (per testing/documentation standards).
8. **NFRs** — rate-limit exposure, idempotency, volume, PII/security considerations.

## Workflow

1. Read the input (`$ARGUMENTS` or the user's message) and the project's build brief if present.
2. Score it against the checklist. For each gap: if the answer exists in project docs, fill it citing the source; if it's a **decision**, ask the user (options + your recommendation). Never fill decisions silently.
3. Output exactly two sections:

```
## Original
<verbatim input>

## Enriched
<the improved requirement, checklist-complete, with open questions listed at the end if any remain>
```

An enriched requirement with open questions is acceptable output; a silently-completed one is not.
