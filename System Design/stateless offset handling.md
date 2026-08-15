[[kafka]] [[kafka producer and consumer]] [[Kafka broker]] [[Idempotent-key]] [[event-driven]] [[Concurrent modification]]

# Stateless offset handling

> Consumer offset handling tracks how far a consumer has read in a partitioned log — "stateless" means progress lives in the broker or coordinator, not in the consumer's local disk, so any group member can resume after restart or rebalance.

## Interview Relevance

Consumer offsets externalized; commit semantics; exactly-once composition.

## Sources

- Apache Kafka documentation — consumer groups, offset commit, transactions — overview
- Martin Kleppmann, *Designing Data-Intensive Applications* — stream processing and delivery guarantees — deep-dive
- Chris Richardson — transactional outbox pattern — overview

## Key Concepts

- **Offsets live outside the consumer process** (store/broker).
- **Commit semantics:** at-most-once vs at-least-once vs transactional.
- **Resume after crash:** read committed offset; expect redelivery.
- **Exactly-once composition:** idempotent sink + careful commit ordering.


## Technical Details

### Offsets as cursors

```txt
Partition log:  [0][1][2][3][4][5][6]
                      ▲ committed offset = 3
Consumer reads 3,4,5 → process → commit 6
Crash before commit → replay from 3 (at-least-once duplicates)
```

Apache Kafka stores committed offsets in the internal `__consumer_offsets` topic. On restart or consumer group rebalance, processing resumes from the last commit.

| Delivery semantics | Order | Risk |
|--------------------|-------|------|
| At-most-once | Commit before process | Message loss |
| At-least-once | Process then commit | Duplicates on crash |
| Exactly-once (broker transactional) | Transactional read-process-write within Kafka | Complexity; side effects outside Kafka still need idempotency |

**Exactly-once is not magic** — HTTP calls and external databases need [[Idempotent-key]] or outbox patterns even when Kafka claims exactly-once.

## Production consumer sketch

```properties
enable.auto.commit=false
max.poll.interval.ms=300000
isolation.level=read_committed
```

```java
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));
  for (ConsumerRecord<String, String> r : records) {
    process(r);  // must be idempotent
  }
  consumer.commitSync();
}
```

| Commit strategy | Trade-off |
|-----------------|-----------|
| Auto commit | Unsafe in production — may commit before process |
| Sync per batch | Duplicate whole batch on crash |
| Async commit | Higher throughput; ordering versus failure timing |
| Offset in same database transaction as side effect | Effect and offset atomic (outbox) |

## Outbox pattern

```txt
BEGIN TRANSACTION
  INSERT business_row ...
  INSERT outbox_event ...
COMMIT
-- separate publisher reads outbox → Kafka
```

## Rebalance and failure

| Symptom | Direction |
|---------|-----------|
| Duplicate processing | Expected at-least-once — idempotent handler |
| Stuck consumer | `max.poll.interval` exceeded — slow processing or poison message |
| Lost messages | Commit-before-process misconfiguration |
| Lag grows | Scale consumers within partition count limit |

Partition count caps parallel consumers — adding instances beyond partition count does not increase throughput.

## Real-World Applications

Kafka/Pulsar consumers, SSE Last-Event-ID, and reconnecting realtime clients.


## Pros/Cons or Trade-offs

- **Pro:** Any replica can continue; horizontal consumer scale.
- **Con:** Duplicate processing if commit lags processing.
- **Trade-off:** commit-before vs commit-after processing.


## Comparison

- vs [[stateless]]: general externalized state; this is the cursor/offset case.
- vs [[Real-time Subscription]]: subscriptions often resume via offsets.


## Mistakes to Avoid

- Skipping failure modes until production.
- Ignoring idempotency, timeouts, or rollback where required.
- Optimizing or distributing before measuring the real bottleneck.

