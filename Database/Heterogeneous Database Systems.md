[[Database]] [[mysql]] [[SQL/postgres]] [[migration]] [[ACID]] [[OLTP]]

# Heterogeneous Database Systems

> Federated or multi-engine architectures where different data stores cooperate—often through ETL, linked servers, or middleware—each chosen for a workload shape.





## Interview Relevance
Polyglot persistence interviews ask why one store is not enough, how consistency spans engines, and what operational complexity you accept. Signal: clear system-of-record plus specialized read models, not “use everything.”

## Sources
- Kleppmann, *Designing Data-Intensive Applications*, Ch. 11 — deep-dive
- [Wikipedia — Federated database system](https://en.wikipedia.org/wiki/Federated_database_system) — overview

## Key Concepts
- **Polyglot persistence:** Postgres for transactions, Elasticsearch for search, S3 for blobs — each engine fits a workload.
- **Federation:** single query interface over remote engines (limited pushdown).
- **CDC replication:** Debezium, logical replication — [[OLTP]] to warehouse.
- **No free distributed ACID:** cross-engine atomicity needs 2PC or saga/outbox patterns.

## Technical Details
| Pattern | Description |
|---------|-------------|
| **Polyglot persistence** | Postgres for transactions, Elasticsearch for search, S3 for blobs |
| **Federation** | Single query interface over remote engines (limited pushdown) |
| **CDC replication** | Debezium, logical replication — [[OLTP]] to warehouse |

Challenges:

- No cross-engine [[ACID]] transaction without two-phase commit (rare in microservices)
- Schema drift between systems
- Operational complexity — more failure modes than one well-tuned primary

## Real-World Applications
SaaS platforms with PostgreSQL as system of record, OpenSearch for product search, and a warehouse fed by CDC. Example: checkout commits in Postgres; search index updates asynchronously and may lag a few seconds.

## Pros/Cons or Trade-offs
- **Pro:** Each workload gets an appropriate engine; primary stays lean for [[OLTP]].
- **Con:** More failure modes, schema drift, and no single transaction across stores without heavy coordination.

## Comparison
vs single [[mysql]] / [[SQL/postgres]] primary: one engine is simpler operationally; heterogeneous setups win when search, analytics, or blobs would harm the primary. vs [[migration]]: moving between engines is a cutover project; living with multiple engines is an ongoing architecture.

## Mistakes to Avoid
- Assuming federated queries preserve full [[ACID]] across engines.
- Letting schemas drift with no ownership of the contract between stores.
- Adding engines without a clear system of record for each entity.
