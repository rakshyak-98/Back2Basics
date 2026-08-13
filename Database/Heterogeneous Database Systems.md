[[Database]] [[mysql]] [[SQL/postgres]] [[migration]]

# Heterogeneous Database Systems

> Federated or multi-engine architectures where different data stores cooperate—often through ETL, linked servers, or middleware—each chosen for a workload shape.

## Patterns

| Pattern | Description |
|---------|-------------|
| **Polyglot persistence** | Postgres for transactions, Elasticsearch for search, S3 for blobs |
| **Federation** | Single query interface over remote engines (limited pushdown) |
| **CDC replication** | Debezium, logical replication — [[OLTP]] to warehouse |

## Challenges

- No cross-engine [[ACID]] transaction without two-phase commit (rare in microservices)
- Schema drift between systems
- Operational complexity — more failure modes than one well-tuned primary

## Sources

- Kleppmann, *DDIA*, Ch. 11 (stream processing)
- Wikipedia — [Federated database system](https://en.wikipedia.org/wiki/Federated_database_system)
