# Intelligent Core

Status: **In progress** — scope and canonical capabilities established.

Provide reusable AI platform services that realise capabilities across the operating architecture.

## Boundary

A technical platform view, not a sixth operating layer. It depends on the Data & Digital Core.

## Capabilities

- [Agent harness](../capabilities/ic-agent-harness.md)
- [LLM kernel and model abstraction](../capabilities/ic-llm-kernel.md)
- [Inference and model serving](../capabilities/ic-inference-serving.md)
- [Context engineering](../capabilities/ic-context-engineering.md)
- [Model and prompt lifecycle](../capabilities/ic-model-lifecycle.md)
- [AI platform operations](../capabilities/ic-ai-platform-operations.md)

## How to use this view

Start with a business process and an outcome. Identify the capabilities needed, record current evidence, then prioritise gaps. All five operating layers consume Knowledge & Memory, Trust & Control, and Workforce & Ways of Working.

## Planned content

A worked design, implementation alternatives, failure scenarios and a measurement guide. Detailed coverage is intentionally visible as unfinished; the map does not imply a complete implementation.

## Platform responsibilities

| Component | Owns | Boundary |
| --- | --- | --- |
| Agent harness | A run’s loop, tools, budget, checkpoints and stopping conditions | Enterprise orchestration allocates work across runs and people |
| LLM kernel | Model-call abstraction, message contracts and structured outputs | Inference serving handles model execution and capacity |
| Inference | Serving, routing, latency, throughput and fallback | Business policy determines whether a model is suitable |
| Context engineering | Assembly and compaction of task context | Knowledge & Memory governs persistent context and access |
| Model lifecycle | Versioned model, prompt and adapter releases | Layer 4 supplies improvement evidence; Trust & Control sets gates |
| Platform operations | Shared deployment, telemetry and evaluation infrastructure | Layer 5 ties technical evidence to enterprise performance |

“LLM kernel” is used here as an architectural abstraction, not a specific vendor product or a standard term. Implementation choices can combine several responsibilities in one service while keeping the contracts clear.

## Planned implementation comparisons

Harness patterns: explicit state machines, workflow-led agents and open-ended tool loops. Inference: hosted APIs, managed deployments and self-hosted serving. Context: retrieval, scoped memory and compaction. Evaluate each against failure recovery, portability, security, latency and full operating cost before choosing a stack.
