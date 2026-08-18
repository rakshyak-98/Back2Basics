[[Kafka]] [[Messaging/Kafka/kafka producer and consumer]] [[Messaging/Kafka/Kafka broker]]

# kafka

> Apache Kafka is a distributed event streaming platform — producers write to topics, brokers store partitions, and consumers read at their own pace.

## Mental model

**Say it in one breath:** Producers append records to topic partitions; brokers replicate and persist them; consumer groups track offsets per partition.

| Component | Role |
| --- | --- |
| **Producer** | Sends messages to topics |
| **Consumer** | Reads from topics (often in a consumer group) |
| **Topic** | Logical stream; split into partitions for parallelism |
| **Broker** | Server that stores and serves topic partitions |
| **ZooKeeper / KRaft** | Cluster metadata and controller election |

- Scales horizontally by adding brokers and partitions.
- Producers and consumers are decoupled — each side scales independently.

## Standard config / commands

```bash
# List topics
kafka-topics.sh --bootstrap-server localhost:9092 --list

# Describe consumer group lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group my-group
```

```yaml
# docker-compose snippet — set KRaft or ZooKeeper mode explicitly
KAFKA_CFG_PROCESS_ROLES: broker,controller
```

## Triage (when things break)

| Symptom | Check | Fix |
| --- | --- | --- |
| Consumer lag growing | `kafka-consumer-groups --describe` | Scale consumers (≤ partitions) or add partitions |
| `UNKNOWN_TOPIC_OR_PARTITION` | Topic exists? ACLs? | Create topic; check `auto.create.topics.enable` |
| Broker won't start (Raft/ZK) | Startup logs | Configure KRaft **or** ZooKeeper, not neither |
| Duplicate messages | Consumer offset commit | Idempotent producer + transactional consume |

## Gotchas

> [!WARNING]
> **More consumers than partitions** — idle consumers; partitions cap parallelism.

> [!WARNING]
> **Kafka without ZooKeeper or KRaft** — broker fails at startup; pick one coordination mode.

## When NOT to use

- **Request/response RPC** — use HTTP or gRPC; Kafka is for durable event streams.
- **Tiny deployments** — operational cost of a cluster may exceed benefit.

## Related

[[Messaging/Kafka/kafka producer and consumer]] [[Messaging/Kafka/Kafka broker]] [[Messaging/Kafka/Kafka configuration]] [[Messaging/RabbitMQ]]
