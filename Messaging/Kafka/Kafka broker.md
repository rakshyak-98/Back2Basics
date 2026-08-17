[[kafka]] [[kafka producer and consumer]] [[Kafka configuration]] [[Zookeeper]] [[Kafka distributed event streaming]]

# Kafka broker

> A Kafka server process that stores topic partitions, serves produce/fetch traffic, and replicates data to peer brokers for durability.

```txt
        Kafka broker ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers ask what a broker actually does (storage, replication, leadershi…

## Sources
- [Apache Kafka — Core concepts](https://kafka.apache.org/intro#intro_topics) — overview
- [Kafka docs — Replication](https://kafka.apache.org/documentation/#replication) — deep-dive
- [Kafka docs — Broker configs](https://kafka.apache.org/documentation/#brokerconfigs) — deep-dive

## Key Concepts
- **Partition replica:** each partition has a leader and followers (ISR) → durability and failover.
- **Leader / follower:** clients produce/fetch to the leader
- **Topic as pub/sub channel:** logical name clients use
- **Controller:** (KRaft controllers or legacy ZK-elected controller) assigns leadership
- **Cluster:** clients bootstrap to any broker, then learn the full metadata map of leaders.


- **Core:** A broker is one Kafka node in the cluster

## Technical Details
| Feature | What the broker does |
|---------|----------------------|
| Message storage | Appends records to partition log segments on disk |
| Serving traffic | Handles produce/fetch for leader partitions |
| Replication | Followers fetch from leaders; maintain ISR |
| Load spread | Partitions distributed across brokers |
| Failover | New leader elected when current leader fails |

- Why “topic”?
- Borrowed from pub/sub: a named category of messages (e.g.
- `cart.item.added`), not a single file

```
Producer → Broker A (leader p0) → replicate → Broker B (follower p0)
         → Broker B (leader p1) → replicate → Broker C (follower p1)
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Under-replicated partitions | Disk / network / slow follower | Repair broker; check ISR; sized replicas |
| Leader imbalance | Prefer preferred leader | Run preferred leader election; even partition count |
| Disk full | Log dirs | Expand retention/compaction; add disks/brokers |
| Client metadata stale | Broker bounce | Clients refresh; ensure advertised listeners correct |

## Mistakes to Avoid
- **Mistake:** Running replication factor 1 in production and calling it durable
- **Mistake:** Forgetting that clients talk to *partition leaders*, so advertis…
- **Mistake:** Adding consumers to fix lag when the real bottleneck is a single…

## Pros/Cons or Trade-offs
- **Pro:** Horizontal scale by adding brokers and reassigning partitions.
- **Con:** Uneven partition or key distribution creates hot brokers.
- **Con:** Broker-local disk and page cache dominate performance — undersized disks look like “Kafka is slow.”

## Comparison
- vs [[kafka]]: broker is the node; Kafka is the whole system (topics, clients, controllers).
- vs [[Zookeeper]] / KRaft controllers: coordination plane versus data plane storage/serving.
- vs [[RabbitMQ]] node: similar “server in a cluster” idea


### Use cases
- Any Kafka deployment

- **Example:** Topic `orders` with 12 partitions and replication factor 3 place…
