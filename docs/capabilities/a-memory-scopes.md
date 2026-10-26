# Memory scopes

Status: **In progress** — capability definition and acceptance example available; implementation comparison planned.

## Purpose

Separate working, session, user and case memory with explicit retention.

Canonical ID: `a-memory-scopes` · Architecture area: [Knowledge & Memory](../architecture/spines/knowledge-memory/index.md)

## Evidence of capability

A deletion request removes applicable memory without exposing another user’s or tenant’s context.

Record the test case, expected result, observed result, service owner and evidence location. A product label alone is not evidence of coverage.

## Design questions

- Which business outcome and process depend on this capability?
- Which actor owns it, and what happens when it fails?
- Which permissions, data dependencies and human decisions apply?
- What is the simplest implementation that meets the acceptance criteria?

## Planned deep dive

Compare implementation patterns, cost and failure modes using a reproducible example. Add public primary resources to the [resource catalogue](../catalogues/resources.md) using this capability ID. Do not copy confidential product assessments here.
