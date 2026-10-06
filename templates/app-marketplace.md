# Marketplace listing — <Integration name>

> **Canonical app-level MARKETPLACE.md template.** Copy to `<app>/MARKETPLACE.md` — the app folder of the Factorial Code team repo, beside `README.md`, `CHANGELOG.md`, `settings.json` and `app/`, **never** inside the workspace `<app>/app/`. Rules: `docs/documentation-standards.md` §3.2. Fill-ready content for **Apps → <app> → Publication**: each section below maps to one field on that screen and must respect its limit (DatoCMS content, when present, overrides these field by field). Written for the buyer/admin, not the developer: no internals, no component names, no hedging. Unknown = `To be confirmed`. Delete this blockquote when copying.

Fill-ready content for **Apps → <Integration name> → Publication**. Each section maps to one field on
that screen. DatoCMS content, when present, overrides these field by field.

| Field | Value | Limit |
|---|---|---|
| Tagline | see [Tagline](#tagline) | 140 |
| Full description | see [Full description](#full-description) | 5,000 |
| Screenshots | see [Screenshots](#screenshots) | 10 · PNG/JPEG/WebP · 2 MB each |
| Support link | `<mailto:owner@factorial.co or support URL>` | 2,000 |
| Help link | `<mailto:owner@factorial.co or documentation URL>` | 2,000 |
| Marketplace visibility | **<Private — allow-listed, installed per company by an admin/FDE / Public>** | — |

---

## Tagline

> <One sentence, ≤ 140 characters: what the app keeps in sync and the manual work it removes.>

*(<n> characters)*

---

## Full description

### What is <External system>?

<Two or three sentences: what the external system is, what lives there, and what the customer loses without the integration (the problem). End by naming the direction of truth: which system is the source and which one is where people read it.>

### Benefits

* <One line per outcome the customer sees — start with a verb; name the Factorial module where the result appears.>
* <Automatic tracking / no manual reporting.>
* <Historical backfill, if offered.>
* <How people are matched (identity rule) in plain words.>
* <Quiet operation: no notification storms, if applicable.>
* <Nothing lost silently: what happens when a record cannot be resolved (HR task, alert).>
* <Self-repair: retries and reconciliation, in plain words.>
* <Direction guarantee: what the integration never changes in the external system.>

### How it works

<Two to four short paragraphs, no component names: how data is read (schedule, event, file), how only differences are applied, what the customer must configure on the external side (nothing, a webhook, a user), and what happens with exceptions.>

### What is synced

| In <External system> | In Factorial |
|---|---|
| <entity> | <Factorial entity / module where it lands> |
| <status field> | <Factorial field, with the mapped states> |

<One sentence on direction: one-way or two-way, and what happens to manual edits in Factorial.>

### Requirements

* <External-system access the customer must provide: account, API credentials, URL — names only, never values.>
* <Factorial data prerequisites: e.g. employees carrying the identifier used for matching.>
* <Factorial modules the customer must have (from the Catalogue / feasibility assessment).>
* <Who completes the setup and what they must nominate (recipients of HR tasks, leave types, etc.).>

### Screenshots

<`To be captured once the app is running against a customer company.` or the list of files.>

Suggested set:

1. <Factorial screen showing the synced data.>
2. <A single synced record in detail.>
3. <An employee-level view.>
4. <The exception path: the HR task or alert raised when something cannot be resolved.>

### Support

Questions and issues: **<owner@factorial.co>**
