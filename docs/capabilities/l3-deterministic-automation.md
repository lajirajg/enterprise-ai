# Deterministic automation

Status: **In progress** — capability definition and acceptance example available; implementation comparison planned.

## Purpose

Execute repeatable rules with explicit inputs, outputs and failure paths.

Canonical ID: `l3-deterministic-automation` · Architecture area: [Execution](../architecture/layers/execution/index.md)

## Evidence of capability

Replaying the same event cannot apply the same business transaction twice.

Record the test case, expected result, observed result, service owner and evidence location. A product label alone is not evidence of coverage.

## Design questions

- Which business outcome and process depend on this capability?
- Which actor owns it, and what happens when it fails?
- Which permissions, data dependencies and human decisions apply?
- What is the simplest implementation that meets the acceptance criteria?

## Planned deep dive

Compare implementation patterns, cost and failure modes using a reproducible example. Add public primary resources to the [resource catalogue](../catalogues/resources.md) using this capability ID. Do not copy confidential product assessments here.
