[[kafka]] [[kafka producer and consumer]] [[Kafka configuration]] [[Zookeeper]] [[Kafka distributed event streaming]]

# Kafka broker

> A Kafka server process that stores topic partitions, serves produce/fetch traffic, and replicates data to peer brokers for durability.





## Interview Relevance
Interviewers ask what a broker actually does (storage, replication, leadership) versus “Kafka the cluster,” and how partition leaders/followers affect produce `acks` and failover.

## Sources
- [Apache Kafka — Core concepts](https://kafka.apache.org/intro#intro_topics) — overview
- [Kafka docs — Replication](https://kafka.apache.org/documentation/#replication) — deep-dive
- [Kafka docs — Broker configs](https://kafka.apache.org/documentation/#brokerconfigs) — deep-dive

## Core Definition
A broker is one Kafka node in the cluster. It hosts partition replicas on disk, accepts produce and fetch requests for partitions it leads, and follows the controller’s assignments when leadership moves.

## Key Concepts
- **Partition replica:** each partition has a leader and followers (ISR) → durability and failover.
- **Leader / follower:** clients produce/fetch to the leader; followers replicate → `acks=all` waits on ISR.
- **Topic as pub/sub channel:** logical name clients use; physically a set of partitions spread across brokers.
- **Controller:** (KRaft controllers or legacy ZK-elected controller) assigns leadership — brokers execute those decisions.
- **Cluster:** clients bootstrap to any broker, then learn the full metadata map of leaders.

## Technical Details
| Feature | What the broker does |
|---------|----------------------|
| Message storage | Appends records to partition log segments on disk |
| Serving traffic | Handles produce/fetch for leader partitions |
| Replication | Followers fetch from leaders; maintain ISR |
| Load spread | Partitions distributed across brokers |
| Failover | New leader elected when current leader fails |

Why “topic”? Borrowed from pub/sub: a named category of messages (e.g. `cart.item.added`), not a single file — partitions are the parallel units underneath.

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

## Real-World Applications
Any Kafka deployment — three or more brokers in production for replica placement; single combined broker for local demos ([[Kafka configuration]]).

**Example:** Topic `orders` with 12 partitions and replication factor 3 places leaders across brokers so one machine loss does not lose committed data when `acks=all` and `min.insync.replicas` are set sanely.

## Pros/Cons or Trade-offs
- **Pro:** Horizontal scale by adding brokers and reassigning partitions.
- **Con:** Uneven partition or key distribution creates hot brokers.
- **Con:** Broker-local disk and page cache dominate performance — undersized disks look like “Kafka is slow.”

## Comparison
- vs [[kafka]]: broker is the node; Kafka is the whole system (topics, clients, controllers).
- vs [[Zookeeper]] / KRaft controllers: coordination plane versus data plane storage/serving.
- vs [[RabbitMQ]] node: similar “server in a cluster” idea; different storage model (log partitions vs queue mirrors).

## Mistakes to Avoid
- Running replication factor 1 in production and calling it durable.
- Forgetting that clients talk to *partition leaders*, so advertised addresses must be reachable for every broker.
- Adding consumers to fix lag when the real bottleneck is a single hot partition on one broker.
