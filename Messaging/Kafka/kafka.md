[[Kafka broker]] [[kafka producer and consumer]] [[Kafka configuration]] [[Zookeeper]] [[Kafka distributed event streaming]] [[RabbitMQ]] [[event-driven]]

# kafka

> Distributed commit log for event streams — producers append to partitioned topics; consumers read at their own pace with durable retention and replay.

## Interview Relevance

Interviewers use Kafka to test partitions/consumer groups, delivery semantics (at-least-once vs exactly-once), retention versus queue deletion, and KRaft versus historic [[Zookeeper]] dependency.

## Sources

- [Apache Kafka documentation](https://kafka.apache.org/documentation/) — deep-dive
- [Apache Kafka introduction](https://kafka.apache.org/intro) — overview
- [KIP-500 — Replace ZooKeeper with KRaft](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum) — deep-dive

## Core Definition

Apache Kafka is a distributed event streaming platform: brokers store append-only logs called *topics* (split into *partitions*). Producers write; consumers read by offset. Data is retained by time/size, not deleted on consume.

## Key Concepts

- **Topic + partition:** ordered log per partition → parallelism = partition count (per consumer group).
- **Producer / consumer:** writers and readers are decoupled → [[event-driven]] integration.
- **Consumer group:** each partition goes to one consumer in the group → scale horizontally; reorder only within a partition.
- **Offset:** position in the log → commit after processing for at-least-once; enable idempotent/transactional producers for stronger guarantees.
- **KRaft vs ZooKeeper:** modern Kafka embeds metadata quorum (KRaft); older clusters used [[Zookeeper]] for controllers and metadata.

## Technical Details

```
Producers → [ Broker / Topic-Partitions / Replicas ] → Consumers (groups)
                 ▲
           Controller (KRaft) or ZooKeeper (legacy)
```

| Role | Job |
|------|-----|
| Producer | Append records (key optional → partition) |
| Broker | Store and serve partition replicas |
| Consumer | Read from offsets; process; commit |
| Topic | Named stream; many partitions |

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic demo
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic demo --from-beginning
```

| Symptom | Likely cause |
|---------|--------------|
| Consumer lag grows | Slow processing / underscaled group |
| Rebalances thrash | Session timeout / processing > max.poll.interval |
| Hot partition | Poor key distribution |
| “Duplicate” events | At-least-once + non-idempotent handler |

## Real-World Applications

Activity pipelines, microservice event buses, CDC streams into warehouses, and real-time analytics.

**Example:** Checkout emits `order.placed`; inventory, fraud, and email services each run a consumer group reading the same topic independently.

## Pros/Cons or Trade-offs

- **Pro:** High throughput, retention/replay, strong ecosystem (Connect, Streams).
- **Con:** Operational complexity (partitions, replicas, rebalances) versus a simpler [[RabbitMQ]] work queue.
- **Con:** Ordering is per partition only — global order needs a single partition (scalability trade-off).

## Comparison

- vs [[RabbitMQ]]: Kafka is a durable log; RabbitMQ routes messages through queues often consumed-and-removed.
- vs [[Kafka distributed event streaming]]: that note focuses on the streaming *pattern*; this is the platform overview.
- Details: [[Kafka broker]], [[kafka producer and consumer]], [[Kafka configuration]], [[Zookeeper]].

## Mistakes to Avoid

- Treating Kafka like a transient task queue without retention/compaction design.
- Using random keys then expecting per-user ordering.
- Committing offsets before the side effect succeeds (silent data loss under at-least-once assumptions).
