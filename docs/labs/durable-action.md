# Durable action and replay

Status: **Runnable** · Capabilities: `l2-durable-workflows`, `l3-deterministic-automation`

Run from the repository root with Python 3.9 or newer:

```sh
python -m unittest tests.test_durable_action -v
```

The lab uses a temporary SQLite database. It records a synthetic action and its completion in one transaction. Replaying the same work identifier returns the stored result; a conflicting payload is rejected. Tests also reopen the database to demonstrate persistence across a process boundary. Temporary data is cleaned up automatically.

Inspect `labs/durable_action.py` and extend the test with a second independent work item.

## Limits

The action is a database-local synthetic side effect. Real ERP writes and external APIs require their own idempotency support, reconciliation or an outbox pattern; a local transaction does not make an external action exactly-once. This lab makes no agent, model or cloud calls.
