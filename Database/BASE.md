- Basically available -> system always responds (may be degraded).
- Soft State -> state can change without new input (async replication).
- Eventual Consistency -> replicas converge over time.

## Why BASE
- Optimised for distributed systems.
- Trades strict consistency for availability + partition tolerance.
- Common in NoSQL/large scale systems.