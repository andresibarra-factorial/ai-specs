# Outline — Integration Architecture (.docx)

File: `Factorial_<Client>_Integration_Architecture.docx` (ES twin: `Factorial_<Client>_Arquitectura_de_Integracion.docx`)

## Header block

- Title line 1: "Integration Architecture" · line 2: "Factorial ↔ <Client>"
- Subtitle: one line describing the deliverable
- Metadata: `Client: <X> · Source of record: <X> · Consumer: <X> · Orchestration: <YepCode | Factorial Code>`
- Version: `Version 0.1 · Draft for review · CONFIDENTIAL`
- Auto Table of Contents

## Sections

1. **Executive Summary** — open by naming the defining architectural fact and the pattern it forces (e.g. webhook-vs-batch mismatch → buffer-and-batch; no webhooks → snapshot-and-diff).
2. **Scope & Objectives** — 2.1 Business context · 2.2 Systems in scope (table: System / Role / Interface) · 2.3 Data-flow principle
3. **Integration Architecture** — 3.1 Core pattern · 3.2 Module & process inventory (table: # / Name / Type / Responsibility) · 3.3 End-to-end flows, narrated per lifecycle event (Provisioning / Update / De-provisioning) · 3.4 Identity & key model (table) · 3.5 Scope & scaling
4. **Authentication Design** — per system: credential provider/token manager · webhook security
5. **Environment Configuration** — full variable table (Variable / Purpose / Sandbox / Production / Sensitive)
6. **Rate Limits & Throughput** — incl. cadence/flush decisions
7. **Error Handling & Monitoring** — failure classification, surfacing model (HR-facing vs technical)
8. **Risk Register** — table: Risk / Likelihood / Impact / Mitigation
9. **Roles & Responsibilities**
10. **Open Decisions & Next Steps**

**Appendix A — Component Manifest** — A.1 Processes · A.2 Modules (mirrors the build brief §7)
