# Enterprise AI Operating Architecture

The architecture describes how an organisation runs AI-enabled work, from customer-facing services to internal operations. It contains exactly five operating layers and three cross-cutting spines. Business outcomes guide it; the Intelligent Core and Data & Digital Core enable it.

| Layer | Responsibility |
| --- | --- |
| [1. User Experience](layers/user-experience/index.md) | Capture intent; show progress, evidence and decisions |
| [2. Intelligent Orchestration](layers/intelligent-orchestration/index.md) | Classify, plan, route and enforce execution policy |
| [3. Execution](layers/execution/index.md) | Complete work through people, agents and automation |
| [4. Data & AI for Continuous Improvement](layers/continuous-improvement/index.md) | Measure, learn and improve processes and AI behaviour |
| [5. Central Hub for Monitoring & Governance](layers/monitoring-governance/index.md) | Oversee performance, cost, value and assurance |

| Cross-cutting spine | Applies to every layer |
| --- | --- |
| [A. Knowledge & Memory](spines/knowledge-memory/index.md) | Grounding, semantics, retained context and its lifecycle |
| [B. Trust & Control](spines/trust-control/index.md) | Identity, authority, policy, isolation and assurance |
| [C. Workforce & Ways of Working](spines/workforce/index.md) | Roles, skills, oversight capacity and operating models |

## Platform and foundation views

[**Intelligent Core**](../intelligent-core/index.md) sits on top of [**Data & Digital Core**](../data-digital-core/index.md). It provides harnesses, model interfaces, inference, context management and AI platform operations. These implement capabilities used throughout the five layers; they do not add another operating layer.

Data & Digital Core means the enterprise’s digitised processes, systems and data: ERP, CRM, ITSM, channels, integration and the underlying infrastructure. If a process is invisible outside a spreadsheet or a person’s inbox, AI cannot reliably act on its state. Fixing that foundation is part of the architecture.

Layer 4 uses operational data to improve the enterprise. It does **not** replace the Data & Digital Core. Spine A governs reusable knowledge and memory. Those are three distinct responsibilities with explicit interfaces.

## Example: invoice exception

A finance user submits an exception in Layer 1. Layer 2 checks materiality and assigns a reviewer or bounded agent. Layer 3 reads the ERP record and proposes a correction. Spine B restricts authority; a person approves a consequential posting. Spine A supplies current policy and scoped case context. Spine C assigns accountability and reviewer capacity. Layer 5 retains the decision trace and cost; Layer 4 measures rework and tests process improvements.

The ERP record, supplier master and approval workflow belong to Data & Digital Core. The harness, model call and context assembly belong to Intelligent Core.

## Generic core and profiles

The [Modern Operate profile](../profiles/modern-operate.md) specialises this model for managed operations. The generic core remains useful to finance, customer service and other enterprise domains. See [design decisions](../about/design-decisions.md) for provenance and boundaries.
