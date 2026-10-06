---
name: app-marketplace
description: Use when a Factorial Code app needs its MARKETPLACE.md (marketplace listing / publication content) created or refreshed - after scaffold-project, when closing a change (update-docs), before a release request or marketplace publication, or when the user asks for "the marketplace description", "the listing", "publication text" or "update MARKETPLACE.md".
---

# App Marketplace Listing

Produce or refresh `<app>/MARKETPLACE.md` on the canonical template `templates/app-marketplace.md`, per `docs/documentation-standards.md` §3.2. **Destination:** the app folder of the Factorial Code team repo, beside `README.md`, `CHANGELOG.md`, `settings.json` and `app/` — never inside the workspace `<app>/app/`. The platform pushes the file with the app; its sections are pasted field by field into **Apps → \<app\> → Publication**, so every section must respect its field limit.

Not applicable to YepCode projects — stop and say so if asked on one.

## Workflow

1. **Load the template and the current file.** If a `MARKETPLACE.md` exists off-template, tell the user you will restructure it, carry every evidenced claim over, and list what did not fit.
2. **Gather evidence, in this order:** feasibility assessment (scope, modules, requirements) → build brief `docs/CLAUDE.md` (what is built, direction of truth, locked decisions) → design doc set (architecture: flows, cadence, exception handling; Field Mapping Spec: the *What is synced* table) → `README.md` (§1 purpose, §4 mapping, §3 configuration for the *Requirements* names) → code only to confirm a behaviour the docs claim. Note the source of every claim; a claim with no source is not written.
3. **Ask, in one AskUserQuestion call, what is a decision rather than a fact:** marketplace visibility (Private allow-listed / Public), support link, help link, whether screenshots exist or are `To be captured`, and the external system's one-line description if the docs do not give it.
4. **Write in the buyer's register.** Outcomes first, present tense, second person where natural ("your catalogue", "your employees"). Forbidden: process/module/variable names, endpoint paths, cron expressions, "idempotent", "crosswalk", "watermark", "dead-letter" and similar internals — translate each into what the customer experiences (e.g. *"a failed run retries, and a nightly check corrects anything that drifted"*). Keep the template's section order.
5. **Count the limits before writing them:** tagline ≤ 140 characters (state the count under it), full description ≤ 5,000 characters (everything from *What is …?* to *Support* inclusive), support/help links ≤ 2,000. Trim, never truncate mid-sentence.
6. **Validate** (all must hold): the field table, the Tagline section and the seven full-description subsections present in template order; no `<`/`>` placeholders; no hedging (`probably`, `might`, `I assume`, `should be able to`); no secrets, tokens or PII; every benefit traceable to a source noted in step 2; counts within limits; direction-of-truth sentence present under *What is synced*.
7. **Write `MARKETPLACE.md`, then report:** sections fully evidenced, cells left `To be confirmed` (with what resolves them), the character counts, and any claim you dropped because the docs do not support it.

## Guardrails

- Never promise a capability that is not designed and documented — a listing is a commitment the app must honour at install time.
- Never restate README sections verbatim; the README states facts for engineers, the listing sells outcomes to buyers (`documentation-standards.md` §3.1).
- Never guess visibility, links or contact details; never put a personal mailbox where the user asked for a shared one.
- Never write the file inside the fcode workspace (`<app>/app/`) or leave two copies.
- Never silently change wording the user has already approved for publication — show the diff.
