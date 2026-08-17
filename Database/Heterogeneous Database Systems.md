[[Database]] [[mysql]] [[SQL/postgres]] [[migration]] [[ACID]] [[OLTP]]

# Heterogeneous Database Systems

> Federated or multi-engine architectures where different data stores cooperate—often through ETL, linked servers, or middleware—each chosen for a workload shape.

```txt
        Heterogeneous Data ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Polyglot persistence reviews ask why one store is not enough, how consiste…

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 11 — deep-dive
- [Wikipedia — Federated database system](https://en.wikipedia.org/wiki/Federated_database_system) — overview

## Key Concepts
- **Polyglot persistence:** Postgres for transactions, Elasticsearch for search, S3 for blobs
- **Federation:** single query interface over remote engines (limited pushdown).
- **CDC replication:** Debezium, logical replication — [[OLTP]] to warehouse.
- **No free distributed ACID:** cross-engine atomicity needs 2PC or saga/outbox patterns.

## Technical Details
| Pattern | Description |
|---------|-------------|
| **Polyglot persistence** | Postgres for transactions, Elasticsearch for search, S3 for blobs |
| **Federation** | Single query interface over remote engines (limited pushdown) |
| **CDC replication** | Debezium, logical replication — [[OLTP]] to warehouse |

- Challenges:

- No cross-engine [[ACID]] transaction without two-phase commit (rare in micros…
- Schema drift between systems
- Operational complexity — more failure modes than one well-tuned primary

## Mistakes to Avoid
- **Mistake:** Assuming federated queries preserve full [[ACID]] across engines
- **Mistake:** Letting schemas drift with no ownership of the contract between …
- **Mistake:** Adding engines without a clear system of record for each entity

## Pros/Cons or Trade-offs
- **Pro:** Each workload gets an appropriate engine; primary stays lean for [[OLTP]].
- **Con:** More failure modes, schema drift, and no single transaction across stores without heavy coordination.

## Comparison
- vs single [[mysql]] / [[SQL/postgres]] primary: one engine is simpler operati…


### Use cases
- SaaS platforms with PostgreSQL as system of record, OpenSearch for product se…
