---
title: Integration Feasibility Assessment: {{External System}} & Factorial
subtitle: Feasibility Study and Integration Options
prepared_for: {{CLIENT_NAME}}
external_system: {{External System}}
confidentiality: Internal/Client Restricted
cover: Project Objective :: {{PROJECT_OBJECTIVE — one sentence: the business outcome the requester expects from connecting <External System> and Factorial}}
cover: Technical Context :: **Source of Truth:** {{External System / Factorial / per entity}} || **Consumer:** Factorial {{Modules}} || **Orchestration:** {{Factorial Code (default) / YepCode}}
cover: Document Control :: **Version:** 0.1 || **Status:** Draft for review || **Date:** {{YYYY-MM-DD}} || **Confidentiality:** Client Restricted || **Assessed by:** {{FDE_NAME}} || **Pinned API version:** {{YYYY-MM-DD}} (factorial-oas-{{YYYY-MM-DD}}.json)
---

<!-- toc -->

---

> **How to use this template (delete this box and every grey italic line before sending)** Replace every `{{placeholder}}`. Grey italic text is author guidance, not content. Verdict vocabulary is fixed: **Feasible** · **Feasible with conditions** · **Not feasible** · **Unknown — evidence missing**. Severity vocabulary: **Critical / High / Medium / Low** (consequence if left unaddressed, not difficulty). Every statement about Factorial is verified against the pinned OpenAPI snapshot named on the cover — never written from memory. Every statement about {{External System}} cites a document in Appendix A. Anything not evidenced is written as an open question in section 10, not as a fact. The reader is the requester, the client and the FDE lead: lead with the answer, keep the engineering for the appendix.

# Executive Summary

_Three to five paragraphs. Open with the request in one paragraph, give the answer in the second, then the one fact that shapes everything. A reader who stops after this section must know the verdict, the defining constraint and what is blocking._

{{One paragraph: who asked for what, for which client, by when, and why it matters to them. Name the systems and the Factorial modules the client has or will acquire.}}

{{The answer in two or three sentences: Feasible / Feasible with conditions / Not feasible / Unknown — and the single qualification that matters most.}}

> **The defining fact.** {{The one characteristic of <External System> or of the request that shapes the whole integration — e.g. no data API, only bespoke actions · no webhooks and no modification timestamps · file-based exchange only · the shared identifier is unconfirmed. State it, cite where it is documented, and say what it does to risk and schedule.}}

{{One paragraph reframing the risk: what is technical and well understood, what is commercial or organisational and outside FDE's control.}}

## Verdict at a glance

<!-- widths: 2900,1700,4130 -->
| Requested capability | Verdict | What it rests on |
|---|---|---|
| {{Capability 1 as the requester phrased it}} | **Feasible** | {{Factorial endpoint / event + external capability it depends on}} |
| {{Capability 2}} | **Feasible with conditions** | {{The condition: module to acquire, action to be built by the vendor, decision pending}} |
| {{Capability 3}} | **Not feasible** | {{The missing capability on either side and whether a workaround exists}} |
| {{Target date / go-live}} | **Feasible with conditions** | {{The two or three prerequisites the date depends on, with their deadlines}} |

## What must be resolved before we can commit

_The date row uses the same verdict vocabulary as the capabilities. Only genuinely blocking items. Each one needs an owner and a date; say explicitly whether any of them is a Factorial limitation._

- **{{Blocking item 1}}.** {{Why it blocks, who owns it, what unblocks it.}}
- **{{Blocking item 2}}.** {{…}}
- **{{Blocking item 3}}.** {{…}}

# Request Summary & Scope

## What was asked

_Quote the request as received — ticket, email, specification section — with its date and author. Separate what was asked from what was assumed._

{{The request, as received. Source: <ticket / document, section, date, requester>.}}

{{Short-term phase vs. later phases, if the requester distinguishes them. Deadline and what it is tied to.}}

## In scope and out of scope

<!-- widths: 3200,1500,4030 -->
| Item | In / Out | Why |
|---|---|---|
| {{Flow or capability}} | In | {{Named in the request; touches both systems}} |
| {{Flow or capability}} | Out | {{Does not touch Factorial / belongs to another vendor / deferred by the requester}} |
| {{Dependency referenced only}} | Out — dependency | {{Not built here, but on the critical path (e.g. an upstream sync that must be live first)}} |

## Factorial modules — hired and to acquire

_The requester states which modules the client has or will contract; this section records that statement and what the assessment needs on top of it. Use the module ↔ API namespace reference in Appendix B to translate each required capability into the module that exposes it. A capability whose namespace belongs to a module the client does not have is a gap (section 6) with a commercial course of action._

<!-- widths: 2000,1300,2900,2530 -->
| Factorial module | Status | Needed for | API namespaces relied upon |
|---|---|---|---|
| {{Core HR}} | Hired | {{Employee master, contracts, identity anchors}} | `{{employees, contracts, custom_fields}}` |
| {{Time Off}} | Hired | {{Writing absences}} | `{{timeoff}}` |
| {{Module}} | To acquire | {{Capability that cannot be delivered without it}} | `{{namespace}}` |
| {{Module}} | Not needed | — | — |

## Systems in scope

<!-- widths: 1700,3400,3630 -->
| System | Role in this integration | Interface |
|---|---|---|
| Factorial | {{Source of record for … / consumer of …}} | Public REST API, version {{YYYY-MM-DD}}. API key or OAuth2. Outbound webhooks for {{events}}. |
| {{External System}} | {{Role}} | {{Protocol and style: REST / SOAP / GraphQL / database / SFTP file exchange / bespoke gateway. Auth scheme. Vendor-documented or per-project.}} |
| {{Factorial Code / YepCode}} | The integration layer. | {{Factorial Code: Python 3.13 runtime, FactorialClient from base-app, per-customer deployment workspace / YepCode: team, Python 3.12, GitHub Action deploy}} — chosen per `docs/platform-guide.md` §4. |
| {{Upstream / downstream system}} | {{Out of scope but a dependency}} | Not applicable. |

## Corrections to the request

_Only when the request or the client's specification contains an assumption that is wrong (direction of control, who calls whom, which system owns a record). Say what the sentence implies, what the reality is, and what should be amended before anyone contracts against it. Delete the section if there is nothing to correct._

{{Section X of the specification reads … which implies …. The agreed division of labour is …. The specification should be amended before ….}}

# Findings — {{External System}}

_Everything the vendor's documentation, sandbox or interviews establish about the external system — and, just as important, what they do not. Facts only; each one is cited in Appendix A._

## Documentation reviewed

<!-- widths: 2900,1600,4230 -->
| Document | Version / date | What it covers |
|---|---|---|
| {{Vendor API manual}} | {{v / date}} | {{Transport, authentication, request/response contract}} |
| {{Client specification}} | {{v / date}} | {{Business flows requested}} |
| {{Sandbox / interview notes}} | {{date}} | {{What was verified by exercising the system}} |

## Interface model — what the documentation establishes

<!-- widths: 2600,6130 -->
| Aspect | What {{External System}} documents |
|---|---|
| Endpoint / topology | {{Single gateway, per-tenant host, on-premise database, SFTP server …}} |
| Communication method | {{REST JSON / SOAP XML / GraphQL / direct DB (engine, driver) / file exchange (format, cadence) / webhooks}} |
| Authentication | {{Scheme, who issues credentials, token lifecycle, rotation rules}} |
| Mandatory headers / conventions | {{User-Agent, tenant ids, versioning header …}} |
| Methods and formats | {{Verbs, body formats, encodings, size limits}} |
| Pagination | {{Cursor / offset / none}} |
| Change detection | {{updated-since filters, event feed, none (snapshot-and-diff needed)}} |
| Events / webhooks | {{Available subscription types, delivery guarantees, retries — or none}} |
| Rate limits and quotas | {{Published figures or ‘not published’}} |
| Environments | {{Sandbox / test tenant / none — and what that implies for testing}} |
| Error model | {{Status codes, error taxonomy, plain-text vs structured}} |
| Reserved arguments / quirks | {{Anything that will shape the client module}} |

## Entities and operations available

_One row per business entity the request touches. ‘Verified’ means exercised against the system or confirmed by the vendor in writing; ‘Documented’ means read in the manual; ‘Required’ means the vendor must build or expose it._

<!-- widths: 1500,800,900,900,900,2130,1600 -->
| Entity | Read | Create | Update | Delete | Filter / change detection | Status |
|---|---|---|---|---|---|---|
| {{Employee}} | {{Yes}} | {{Yes}} | {{Yes}} | {{No}} | {{updated_at ≥ ; by id}} | {{Verified / Documented / Required}} |
| {{Absence}} | {{Yes}} | {{—}} | {{—}} | {{—}} | {{changed-since + state}} | {{Required — to be built by vendor}} |

## What the documentation does not establish

{{Everything of business substance that is missing: entities, field names, data types, code lists, pagination, change detection, error taxonomy, rate limits, sandbox, SLA. Say whether it is missing by oversight or supplied per project.}}

## What this costs, in planning terms

- {{Serial dependencies on the vendor (specify → build → document → integrate).}}
- {{What stays open in the field mapping until the vendor delivers.}}
- {{Test environment needs that must be part of the commission.}}
- {{Opportunities: where a bespoke interface lets us specify the payload we want.}}

# What Factorial Provides

> **Verification statement.** Every statement in this section was verified against the pinned OpenAPI snapshot `factorial-oas-{{YYYY-MM-DD}}.json` (API version {{YYYY-MM-DD}}), which is the contract we would build to, and — where marked — against behaviour observed in production on another Factorial integration. Nothing here is recalled from memory.

_One subsection per Factorial capability the request depends on: what the resource carries, which filters exist, the characteristics that matter for this design (date-granularity filters, last-change-only timestamps, no external reference field …). Name module dependencies explicitly — a resource that belongs to a module the client has not hired is a gap._

## {{Reading / writing entity 1 — e.g. employees and contract versions}}

{{What the resource exposes, the filters available for incremental reads, the two or three behaviours that matter for this design and whether they help or hurt.}}

## {{Reading / writing entity 2 — e.g. leaves}}

{{Lifecycle supported (create / read / update / delete / approve), required vs optional fields, configuration prerequisites (leave types, custom fields), the genuine gap if any (e.g. no external reference field).}}

## The event channel

{{Webhook subscription types verified for this scope, how they are created, and the behaviours known from the API guide and live operation: no event-type field in deliveries (resolve from state or a per-subscription target URL), payloads that can arrive incomplete (re-read), the delivery retry policy (`docs/factorial-api-guide.md`: up to 20 retries over 48 h, then the subscription is disabled — so duplicates must be tolerated and disabled subscriptions monitored). Platform process executions themselves are never retried. Say what the design must do about each.}}

## Identity anchors available

<!-- widths: 2200,2600,3930 -->
| Anchor | Factorial field | Assessment |
|---|---|---|
| {{Internal company code}} | `{{field, as named in the pinned OAS}}` | {{Cleanest key if the same code exists on both sides; not personal data; depends on …}} |
| {{National identifier}} | `{{field}}` | {{Universal in payroll; needs normalisation; personal data in transit}} |
| {{Email}} | `{{field}}` | {{Fallback; may be null on creation events}} |
| {{Custom field}} | `{{custom_fields resource and value lookup}}` | {{Explicit, auditable link populated at onboarding; one extra lookup}} |

## Platform facts relied upon

_Factorial Code capabilities this assessment assumes — datastore, schedules, webhook receivers, forms, per-customer workspaces, outbound address for allow-listing — each marked verified or to be confirmed with the platform team._

- **{{Capability}}** — {{verified (date, how) / to be confirmed}}

# Feasibility by Use Case

<!-- widths: 700,2500,1800,1700,2030 -->
| # | Use case | Direction | Verdict | Principal constraint |
|---|---|---|---|---|
| UC-1 | {{New joiner published to <External System>}} | Factorial → {{External System}} | Feasible | {{The one thing that shapes it}} |
| UC-2 | {{Leaver}} | Factorial → {{External System}} | Feasible with conditions | {{…}} |
| UC-3 | {{Modification}} | Factorial → {{External System}} | Feasible | {{…}} |
| UC-4 | {{Absence written to Factorial}} | {{External System}} → Factorial | Not feasible | {{The missing capability}} |

_One short subsection per use case: how it would work end to end, the subtle case, and the behaviour the requester must confirm. Keep each to one paragraph._

## UC-1 — {{Use case}}

{{Narrative: trigger → what is read → how identity is resolved → what is written → what happens when it cannot be. End with the question the requester must answer, if any.}}

## UC-2 — {{Use case}}

{{…}}

# Gaps & Caveats Register

Severity reflects the consequence if the gap is left unaddressed, not the difficulty of addressing it. “Blocking” means the requested phase cannot go live without a resolution. Side names where the gap lives: Factorial (product or module), {{External System}}, Both, or Commercial / Organisational.

<!-- widths: 400,1500,1450,1440,900,760,1620,660 size: 16 -->
| # | Expectation (as requested) | What the systems can do today | Gap / caveat | Side | Sev. | Course of action | Block. |
|---|---|---|---|---|---|---|---|
| G1 | {{Read absences from <External System>}} | {{No standard data API; bespoke actions only}} | {{Contract must be commissioned}} | {{External System}} | Critical | {{Commission the action; specify the payload ourselves}} | Yes |
| G2 | {{Write absences into Factorial}} | {{Leaves support full lifecycle}} | {{No external reference field → idempotency must be ours}} | Factorial | High | {{Link table + description marker}} | No |
| G3 | {{Sync training progress}} | {{Trainings module API available}} | {{Client has not hired the Trainings module}} | Commercial | High | {{Contract the module before build; confirm pricing with AM}} | Yes |
| G4 | {{Real-time updates}} | {{No webhooks on the external side}} | {{Polling only; latency ≥ cadence}} | {{External System}} | Medium | {{Agree an acceptable cadence}} | No |

# Integration Approaches

_At least two options, each honestly described — including the one you will not recommend. Options may differ in the Factorial modules the client must acquire, in the communication method with the other system (REST API, database connection, SOAP, GraphQL, webhooks, file generation / exchange, vendor-built actions) and in where the logic runs. For each option state what it accomplishes of the request and what it leaves open._

## Options at a glance

<!-- widths: 1200,1500,1500,1000,1430,700,700,700 size: 16 -->
| Option | Method | Factorial modules | Covers | Gaps left | Effort | Risk | Rec. |
|---|---|---|---|---|---|---|---|
| A — {{name}} | {{REST + webhooks}} | {{Core HR, Time Off}} | {{UC-1…UC-4}} | {{G2 mitigated, G4 accepted}} | {{M}} | {{Low}} | Yes |
| B — {{name}} | {{Nightly file exchange (SFTP, CSV)}} | {{Core HR}} | {{UC-1…UC-3}} | {{UC-4 not covered; G4}} | {{S}} | {{Medium}} | No |
| C — {{name}} | {{Direct database read}} | {{Core HR, Trainings (to acquire)}} | {{All}} | {{G3 commercial}} | {{L}} | {{High}} | No |

## Option A — {{name}}

### Pattern

{{One paragraph: how data moves, in which direction, on what trigger, and the safety net underneath (reconciliation, dead-letter, replay).}}

### Communication with {{External System}}

{{Method and why: REST / SOAP / GraphQL / database connection (engine, network path, read-only user) / webhooks / file exchange (format, transport, cadence, naming) / vendor-built actions. Authentication, allow-listing, environments.}}

### Factorial modules and configuration required

- {{Module — hired / to acquire — what it provides here}}
- {{Configuration prerequisite — e.g. non-accruing leave types, custom field, webhook subscriptions}}

### Component inventory

<!-- widths: 500,2300,1900,4030 -->
| # | Component | Type | Responsibility |
|---|---|---|---|
| 1 | {{webhook-receiver}} | Webhook process | {{Answers the challenge, filters scope, queues the event}} |
| 2 | {{dispatcher}} | Scheduled process | {{Drains the queue, enriches, transforms, calls the external write}} |
| 3 | {{reconciliation}} | Scheduled process | {{Compares full rosters, repairs drift}} |
| 4 | {{setup}} | Form process | {{Customer activation: registers subscriptions, validates credentials}} |

### What this option accomplishes

<!-- widths: 2500,1600,4630 -->
| Requested item | Accomplished | How / under which condition |
|---|---|---|
| {{UC-1}} | Yes | {{…}} |
| {{UC-4}} | Partially | {{Daily latency instead of real time}} |
| {{Item}} | No | {{Why not, and what would}} |

### Gaps and caveats of this option

- {{Gap reference (G#) and how this option handles it, or that it does not.}}

### Effort, prerequisites and risk

{{Size (S / M / L with the assumption behind it), prerequisites that must be closed before build, and the risk profile.}}

## Option B — {{name}}

### Pattern

{{One paragraph: how data moves, in which direction, on what trigger, and the safety net underneath (reconciliation, dead-letter, replay).}}

### Communication with {{External System}}

{{Method and why: REST / SOAP / GraphQL / database connection (engine, network path, read-only user) / webhooks / file exchange (format, transport, cadence, naming) / vendor-built actions. Authentication, allow-listing, environments.}}

### Factorial modules and configuration required

- {{Module — hired / to acquire — what it provides here}}
- {{Configuration prerequisite — e.g. non-accruing leave types, custom field, webhook subscriptions}}

### Component inventory

<!-- widths: 500,2300,1900,4030 -->
| # | Component | Type | Responsibility |
|---|---|---|---|
| 1 | {{file-exporter}} | Scheduled process | {{Builds and delivers the export; records the watermark}} |
| 2 | {{file-importer}} | Scheduled process | {{Picks up, validates and applies the inbound file; quarantines rejects}} |
| 3 | {{reconciliation}} | Scheduled process | {{Compares full rosters, repairs drift}} |

### What this option accomplishes

<!-- widths: 2500,1600,4630 -->
| Requested item | Accomplished | How / under which condition |
|---|---|---|
| {{UC-1}} | Yes | {{…}} |
| {{UC-4}} | No | {{…}} |

### Gaps and caveats of this option

- {{Gap reference (G#) and how this option handles it, or that it does not.}}

### Effort, prerequisites and risk

{{Size (S / M / L with the assumption behind it), prerequisites that must be closed before build, and the risk profile.}}

## Decision criteria

{{What the choice actually turns on: latency the business needs, modules the client is willing to contract, what the vendor can commit to and when, operational burden, cost.}}

# Verdict & Recommendation

> **Verdict: {{Feasible / Feasible with conditions / Not feasible / Unknown — evidence missing}}** {{Two or three sentences: the recommended option and why, the conditions attached, and what cannot be promised yet. If no verdict can be given at this moment, say exactly which evidence or decision is missing and who provides it.}}

## Recommended approach

{{Option X, because …. What it reuses from proven patterns. What it deliberately leaves to a later phase.}}

## Conditions and prerequisites

<!-- widths: 4800,2300,1630 -->
| Prerequisite | Owner | Needed by |
|---|---|---|
| {{Commission the vendor actions with an agreed payload}} | {{Client with vendor}} | {{date}} |
| {{Contract the missing Factorial module}} | {{Client with Factorial AM}} | {{date}} |
| {{Confirm the shared identity key}} | {{Client}} | {{date}} |
| {{Configure leave types / custom fields in Factorial}} | {{Factorial with client HR}} | {{date}} |
| {{Provide volumes and peak figures}} | {{Client}} | {{date}} |
| {{Confirm platform facts (datastore, outbound address)}} | {{Factorial platform team}} | {{date}} |

## Phasing and the target date

{{Phase 0 — prerequisites (none of it is development, all of it on the critical path). Phase 1 — the requested scope. Phase 2 — deferred by design, listed so the boundary is explicit. Then: is the date achievable, what it is at risk from, and what to treat as the first action.}}

## Roles and responsibilities

<!-- widths: 2600,6130 -->
| Party | Responsibility |
|---|---|
| {{CLIENT_NAME}} | {{Commercial relationship with the vendor, identity key decision, business rules, volumes, sequencing of upstream dependencies}} |
| {{Vendor}} | {{Builds, documents and supports the interface; issues credentials; provides a non-production path; allow-lists our address}} |
| Factorial | {{Builds and operates the integration layer, identity model, reconciliation and error handling; configures modules with the client; maintains design docs and field mapping}} |
| {{CLIENT_NAME}} HR / operations | {{Resolves manual matches, acts on conflict tasks, validates catalogues}} |

# Risk Register

<!-- widths: 2900,1300,1000,3530 -->
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| {{Vendor commission agreed late, compressing the serial dependency}} | High | High | {{Start the commercial conversation now with a written payload specification}} |
| {{No test environment provided}} | Medium | High | {{Make a test token / action an explicit line item; build the offline harness against recorded fixtures}} |
| {{Identity key proves unreliable}} | Medium | High | {{Matching dry-run against a real extract before go-live}} |
| {{Upstream sync slips}} | Medium | High | {{Sequence acceptance testing behind it}} |
| {{Seasonal peak overwhelms cadence}} | Medium | Medium | {{Size against real peaks; batch; honour rate-limit headers}} |

# Open Questions & Clarifications

_Every question is addressed to the party that can answer it, phrased so a yes/no or a value closes it, and linked to the gap or decision it unblocks. Nothing in sections 1–9 may rest on an answer that is still open here without saying so._

## For the requester (internal)

<!-- widths: 500,4600,1800,1830 -->
| # | Question | Unblocks | Answer |
|---|---|---|---|
| Q1 | {{Which legal entities are in scope, and is the scope expected to grow?}} | {{UC-1 filter}} | {{open}} |
| Q2 | {{Which Factorial modules has the client contracted today, and which are in the proposal?}} | {{G3}} | {{open}} |

## For the client

<!-- widths: 500,4600,1800,1830 -->
| # | Question | Unblocks | Answer |
|---|---|---|---|
| Q3 | {{Which identifier is shared between Factorial and <External System> for the same person?}} | {{Identity model}} | {{open}} |
| Q4 | {{When two sources write the same record, which one wins?}} | {{Collision rule}} | {{open}} |

## For the vendor

<!-- widths: 500,4600,1800,1830 -->
| # | Question | Unblocks | Answer |
|---|---|---|---|
| Q5 | {{Can an action accepting payload X be built and documented by date Y?}} | {{G1}} | {{open}} |
| Q6 | {{Is a non-production token or test action available?}} | {{Testing}} | {{open}} |

## For Factorial teams (product, platform, API)

<!-- widths: 500,4600,1800,1830 -->
| # | Question | Unblocks | Answer |
|---|---|---|---|
| Q7 | {{Is the datastore available on the intended plan? What is the outbound address to allow-list?}} | {{Option A}} | {{open}} |
| Q8 | {{Can the specification enumerate the available webhook subscription types?}} | {{Documentation}} | {{open}} |

## Immediate next steps

1. {{Circulate this assessment; where the vendor must build or expose an interface, put the payload we need in writing — the external columns of the Field Mapping Spec, which `design-docs` produces as soon as the blocking answers arrive.}}
2. {{Amend the client specification where section 2.5 found it wrong.}}
3. {{Close the Phase 0 prerequisites, tracking the critical-path item.}}
4. {{On answers to section 10, produce the Solution Design and the build brief, and open the first change specification.}}

---

#! Appendix A — Technical Evidence

##! A.1 Factorial endpoints

All paths verified against `factorial-oas-{{YYYY-MM-DD}}.json`. Base path: `/api/{{YYYY-MM-DD}}/resources/`. Production server `https://api.factorialhr.com`; demo server `https://api.eu2.demo.factorial.dev`. Authentication is either an `x-api-key` header or OAuth2 authorization code with read and write scopes.

<!-- widths: 1900,2600,1100,3130 -->
| Purpose | Path | Methods | Notes |
|---|---|---|---|
| {{Read employees}} | `{{domain/resource}}` | {{GET}} | {{Filters available, as listed in the OAS}} |
| {{Write leaves}} | `{{domain/resource}}` | {{GET, POST}} | {{Required fields on create, as listed in the OAS}} |
| {{Webhook subscriptions}} | `{{domain/resource}}` | {{GET, POST}} | {{Required fields, as listed in the OAS}} |

##! A.2 Verified webhook subscription types

{{Not enumerated in the API specification. The following types are registered and operating in production on <integration> and cover this scope: <employees/employee/create_with_contract, employees/employee/update, employees/employee/terminate, employees/employee/unterminate>.}}

##! A.3 {{External System}} transport and contract facts

<!-- widths: 5800,2930 -->
| Fact | Source |
|---|---|
| {{Single gateway endpoint; per-client host variants}} | {{Manual, §}} |
| {{Bearer token in the Authorization header only; never in the URL}} | {{Security note, date}} |
| {{No standard actions; every action programmed per client and documented per project}} | {{Manual, §}} |

##! A.4 Sources

- {{Client — specification title, version, date.}}
- {{Vendor — API manual title, version, date.}}
- {{Factorial OpenAPI snapshot factorial-oas-<YYYY-MM-DD>.json (API version <YYYY-MM-DD>).}}
- {{Production-verified behaviour from the <integration> integration.}}

#! Appendix B — Factorial modules ↔ API namespaces

Functional interpretation of the API namespaces of `factorial-oas-2026-07-01.json` grouped by the Factorial product area that exposes them (source: `templates/data/factorial-product-api-mapping.csv`). It is **not** an official commercial entitlement mapping: which modules a client has hired or must acquire comes from the requester (section 2.3). Use it to translate a required capability into the module it depends on, and to spot a namespace the client's contract does not cover. Refresh the table when the pinned OAS changes.

<!-- widths: 2000,2600,4130 size: 16 -->
| Functional group (product area) | API namespaces | Resources |
|---|---|---|
| Core HR / shared HR infrastructure | `companies, contracts, custom_fields, custom_resources, documents, employees, holidays, locations, tasks, teams` | `companies`: legal_entities · `contracts`: compensations, contract_templates, contract_version_histories, contract_version_meta_data, contract_versions, french_contract_types, german_contract_types, materialized_templates, portuguese_contract_types, reference_contracts, spanish_contract_types, spanish_education_levels, spanish_professional_categories, spanish_working_day_types, taxonomies · `custom_fields`: fields, options, resource_fields, values · `custom_resources`: resources, schemas, values · `documents`: documents, download_urls, folders · `employees`: employees · `holidays`: company_holidays · `locations`: locations, work_areas · `tasks`: task_files, tasks · `teams`: memberships, teams |
| Time Off | `timeoff` | `timeoff`: allowance_incidences, allowance_stats, allowances, blocked_periods, leave_types, leaves, policies, policy_assignments, policy_timelines |
| Time Tracking | `attendance` | `attendance`: break_configurations, edit_timesheet_requests, estimated_times, open_shifts, overtime_requests, reviews, shifts, worked_times |
| Shift planning / working schedules | `shift_management, time_planning, time_settings, work_schedule` | `shift_management`: shifts · `time_planning`: planned_breaks, planning_versions · `time_settings`: break_configurations · `work_schedule`: day_configurations, overlap_periods, schedules |
| Payroll / payroll integrations | `bookkeepers_management, compensations, employee_updates, payroll, payroll_employees, payroll_integrations_base` | `bookkeepers_management`: incidences · `compensations`: concepts · `employee_updates`: absences, contract_changes, new_hires, personal_changes, summaries, terminations · `payroll`: family_situations, policy_periods, supplements · `payroll_employees`: identifiers · `payroll_integrations_base`: codes |
| Expenses | `expenses` | `expenses`: expensables, expenses, mileages, per_diems |
| Banking / finance | `banking, finance` | `banking`: bank_accounts, card_payments, transactions · `finance`: accounting_settings, accounts, budget_options, categories, contacts, cost_center_memberships, cost_centers, financial_documents, journal_entries, journal_lines, ledger_account_resources, tax_rates, tax_types |
| Procurement | `procurement` | `procurement`: purchase_orders, purchase_requests, types |
| Project Management | `project_management` | `project_management`: budget_strategies, expense_records, exportable_expenses, imputable_projects, planned_records, project_tasks, project_workers, projects, subprojects, time_records |
| Recruitment | `ats` | `ats`: answers, application_phases, applications, candidate_sources, candidates, evaluation_forms, feedbacks, hiring_stages, job_postings, messages, questions, rejection_reasons |
| Performance / career architecture | `job_catalog, performance` | `job_catalog`: levels, node_attributes, roles, tree_nodes · `performance`: agreements, company_employee_score_scales, employee_score_scales, review_evaluation_answers, review_evaluation_scores, review_evaluations, review_owners, review_process_custom_templates, review_process_estimated_targets, review_process_targets, review_processes, review_questionnaire_by_strategies, review_visibility_settings, target_managers |
| Training | `trainings` | `trainings`: categories, session_access_memberships, session_attendances, sessions, training_classes, training_memberships, trainings |
| IT asset management | `it_management` | `it_management`: it_asset_models, it_assets |
| Communication / engagement | `posts` | `posts`: comments, groups, posts |
| Shared platform / integrations | `api_public, approvals, integrations, marketplace` | `api_public`: credentials, webhook_subscriptions · `approvals`: materialized_approvals_flows · `integrations`: sync_run_outputs, syncable_items, syncable_sync_runs · `marketplace`: installation_settings, installations |
