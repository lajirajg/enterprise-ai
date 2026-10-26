# Service observability

Status: **In progress** — capability definition and acceptance example available; implementation comparison planned.

## Purpose

Trace a business request across orchestration, execution and supporting systems.

Canonical ID: `l5-service-observability` · Architecture area: [Central Hub for Monitoring & Governance](../architecture/layers/monitoring-governance/index.md)

## Evidence of capability

Locate the failed dependency from a user-visible work identifier.

Record the test case, expected result, observed result, service owner and evidence location. A product label alone is not evidence of coverage.

## Design questions

- Which business outcome and process depend on this capability?
- Which actor owns it, and what happens when it fails?
- Which permissions, data dependencies and human decisions apply?
- What is the simplest implementation that meets the acceptance criteria?

## Planned deep dive

Compare implementation patterns, cost and failure modes using a reproducible example. Add public primary resources to the [resource catalogue](../catalogues/resources.md) using this capability ID. Do not copy confidential product assessments here.
