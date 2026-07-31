---
name: adversarial-review
description: Use when the user requests an adversarial review, red-team pass, devil's advocate check, or independent verification of an implemented change against its spec before sign-off.
---

# Adversarial Review

Independent red-team pass in the verification window (after implementation, before close). Ideally run in a fresh session or a different agent than the one that implemented. Your job is to find where the implementation fails the spec — not to praise it.

## Workflow

1. **Load the spec side** — the change's `spec.md` (requirements, scenarios, non-goals), `tasks.md`, the build brief's locked decisions. Extract every acceptance criterion.
2. **Load the implementation** — the diff (`git diff` vs merge base or the PR), the verification reports in `reports/`.
3. **Attack each criterion** — how could it still fail? Duplicate webhook delivery, out-of-order events, empty/final pagination pages, null fields (emails on create!), rate-limit storms mid-batch, re-run after partial failure, datastore key collisions, timezone/DST, wrong legal entity scope. Spec-vs-code mismatches are first-class findings, including code doing MORE than the spec (scope creep) and violated non-goals.
4. **Check the tests** — do tests actually assert the scenarios, or just exercise the code? Untested criterion = finding.
5. **Verdict.**

## Output

```
# Adversarial Review — <change-id> — YYYY-MM-DD
## Scope & sources
## Findings
| Severity | Area | Finding | Evidence | Fix belongs in |
|---|---|---|---|---|
(Blocker / Major / Minor / Question ; fix in code / tests / spec / docs)
## Verdict: PASS | PASS WITH GAPS | FAIL
## Recommended next steps
```

Guardrails: no praise-to-balance; never skip reading the spec artifacts; "the tests pass" is not evidence a criterion is met.
