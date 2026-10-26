# Capability catalogue

Generated from `catalogue/capabilities.json`. Edit canonical metadata and run `python scripts/catalogue.py render`.

## User Experience

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `l1-intent-intake` | [Intent and request intake](../capabilities/l1-intent-intake.md) | Turn a request into a structured work item with a clear purpose and completion criteria. | in-progress |
| `l1-human-approvals` | [Human approval experience](../capabilities/l1-human-approvals.md) | Let an authorised person inspect the proposed action, evidence and consequences. | in-progress |
| `l1-progress-feedback` | [Progress and feedback](../capabilities/l1-progress-feedback.md) | Expose work status and capture corrections without losing task context. | in-progress |
| `l1-accessible-channels` | [Accessible channels](../capabilities/l1-accessible-channels.md) | Support the channels and accessibility needs of each audience. | in-progress |

## Intelligent Orchestration

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `l2-work-classification` | [Work classification](../capabilities/l2-work-classification.md) | Assess task complexity, risk and reversibility before selecting an execution mode. | in-progress |
| `l2-planning-routing` | [Planning and routing](../capabilities/l2-planning-routing.md) | Allocate work among people, deterministic workflows, automations and agents. | in-progress |
| `l2-autonomy-policy` | [Autonomy policy](../capabilities/l2-autonomy-policy.md) | Set permitted actions and approval gates for each use case. | in-progress |
| `l2-durable-workflows` | [Durable workflows](../capabilities/l2-durable-workflows.md) | Resume work safely across failures, waits and deployments. | in-progress |
| `l2-tool-gateway` | [Tool gateway](../capabilities/l2-tool-gateway.md) | Authorise and audit access to enterprise tools. | in-progress |

## Execution

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `l3-human-execution` | [Human execution](../capabilities/l3-human-execution.md) | Support a person completing work with context and clear accountability. | in-progress |
| `l3-deterministic-automation` | [Deterministic automation](../capabilities/l3-deterministic-automation.md) | Execute repeatable rules with explicit inputs, outputs and failure paths. | in-progress |
| `l3-agent-execution` | [Agent execution](../capabilities/l3-agent-execution.md) | Carry out bounded reasoning and tool use against task completion criteria. | in-progress |
| `l3-domain-packs` | [Domain packs](../capabilities/l3-domain-packs.md) | Package domain workflows, vocabularies and tests on shared platform services. | in-progress |

## Data & AI for Continuous Improvement

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `l4-process-analysis` | [Process analysis](../capabilities/l4-process-analysis.md) | Find delays, rework and exceptions using evidence from actual work. | in-progress |
| `l4-evaluation-feedback` | [Evaluation and feedback](../capabilities/l4-evaluation-feedback.md) | Measure quality using representative cases and production feedback. | in-progress |
| `l4-controlled-improvement` | [Controlled improvement](../capabilities/l4-controlled-improvement.md) | Test and release changes with measurable success and rollback criteria. | in-progress |
| `l4-knowledge-improvement` | [Knowledge improvement](../capabilities/l4-knowledge-improvement.md) | Turn corrections and recurring failures into reviewed knowledge updates. | in-progress |

## Central Hub for Monitoring & Governance

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `l5-service-observability` | [Service observability](../capabilities/l5-service-observability.md) | Trace a business request across orchestration, execution and supporting systems. | in-progress |
| `l5-value-cost-monitoring` | [Value and cost monitoring](../capabilities/l5-value-cost-monitoring.md) | Connect operating costs and performance to business outcomes. | in-progress |
| `l5-assurance-evidence` | [Assurance evidence](../capabilities/l5-assurance-evidence.md) | Retain evidence of decisions, controls and exceptions. | in-progress |
| `l5-portfolio-governance` | [Portfolio governance](../capabilities/l5-portfolio-governance.md) | Track ownership, lifecycle and dependencies across AI-enabled services. | in-progress |

## Knowledge & Memory

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `a-grounded-retrieval` | [Grounded retrieval](../capabilities/a-grounded-retrieval.md) | Retrieve relevant evidence within the requester’s permissions. | in-progress |
| `a-knowledge-lifecycle` | [Knowledge lifecycle](../capabilities/a-knowledge-lifecycle.md) | Manage provenance, freshness, review and retirement of reusable knowledge. | in-progress |
| `a-memory-scopes` | [Memory scopes](../capabilities/a-memory-scopes.md) | Separate working, session, user and case memory with explicit retention. | in-progress |
| `a-ontology-semantics` | [Ontology and semantics](../capabilities/a-ontology-semantics.md) | Define shared business terms and their domain extensions. | in-progress |

## Trust & Control

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `b-identity-authority` | [Identity and delegated authority](../capabilities/b-identity-authority.md) | Identify actors and limit their authority for each action. | in-progress |
| `b-policy-guardrails` | [Policy and guardrails](../capabilities/b-policy-guardrails.md) | Enforce allowed data use, outputs and business actions. | in-progress |
| `b-safety-assurance` | [Safety and assurance](../capabilities/b-safety-assurance.md) | Assess failure modes and verify control effectiveness over time. | in-progress |
| `b-privacy-isolation` | [Privacy and isolation](../capabilities/b-privacy-isolation.md) | Apply minimisation, retention and isolation to data and context. | in-progress |

## Workforce & Ways of Working

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `c-roles-accountability` | [Roles and accountability](../capabilities/c-roles-accountability.md) | Assign responsibility for outcomes, oversight and exceptions. | in-progress |
| `c-skills-adoption` | [Skills and adoption](../capabilities/c-skills-adoption.md) | Develop practical competence and support changes in work. | in-progress |
| `c-oversight-capacity` | [Oversight capacity](../capabilities/c-oversight-capacity.md) | Keep human review effective at the expected workload. | in-progress |
| `c-operating-commercial-model` | [Operating and commercial model](../capabilities/c-operating-commercial-model.md) | Align teams, service boundaries and incentives with delivered value. | in-progress |

## Intelligent Core

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `ic-agent-harness` | [Agent harness](../capabilities/ic-agent-harness.md) | Coordinate the reasoning loop, tools, stopping conditions and recovery within an agent run. | in-progress |
| `ic-llm-kernel` | [LLM kernel and model abstraction](../capabilities/ic-llm-kernel.md) | Provide a consistent contract for model calls and structured responses. | in-progress |
| `ic-inference-serving` | [Inference and model serving](../capabilities/ic-inference-serving.md) | Serve model requests within latency, throughput and cost targets. | in-progress |
| `ic-context-engineering` | [Context engineering](../capabilities/ic-context-engineering.md) | Assemble task instructions, retrieved evidence and memory within context limits. | in-progress |
| `ic-model-lifecycle` | [Model and prompt lifecycle](../capabilities/ic-model-lifecycle.md) | Version, evaluate and release model configurations, prompts and adapters. | in-progress |
| `ic-ai-platform-operations` | [AI platform operations](../capabilities/ic-ai-platform-operations.md) | Operate shared evaluation, tracing, secrets and deployment services. | in-progress |

## Data & Digital Core

| ID | Capability | Definition | Status |
| --- | --- | --- | --- |
| `dd-process-digitisation` | [Process digitisation](../capabilities/dd-process-digitisation.md) | Represent business steps, decisions and records in operational systems. | in-progress |
| `dd-enterprise-systems` | [Enterprise systems of record](../capabilities/dd-enterprise-systems.md) | Maintain authoritative ERP, CRM, ITSM and other business records. | in-progress |
| `dd-digital-channels` | [Digital customer and employee channels](../capabilities/dd-digital-channels.md) | Capture interactions and hand them into executable business processes. | in-progress |
| `dd-integration-events` | [Integration and events](../capabilities/dd-integration-events.md) | Expose governed APIs and events for reading and changing business state. | in-progress |
| `dd-data-products` | [Data products and quality](../capabilities/dd-data-products.md) | Provide owned, documented operational and analytical data with quality contracts. | in-progress |
| `dd-digital-infrastructure` | [Digital infrastructure](../capabilities/dd-digital-infrastructure.md) | Provide the hosting, connectivity and recovery foundations for digital operations. | in-progress |
