[[kafka]] [[kafka producer and consumer]] [[Kafka broker]] [[Idempotent-key]] [[Concurrent modification]]

# Stateless offset handling

> Kafka consumer offset patterns for "stateless" services — commits, rebalance, duplicates, and exactly-once illusions — **Kleppmann / Kafka ops canon**.

---

## Mental model

A consumer's **offset** is its cursor in a partition log. **Stateless** here means: no durable local DB for progress — the broker (or coordinator) stores committed offsets in `__consumer_offsets`. On restart/rebalance, processing resumes from last commit.

```txt
Partition log:  [0][1][2][3][4][5][6]
                      ▲ committed offset = 3
Consumer reads 3,4,5 → process → commit 6
Crash before commit → replay from 3 (at-least-once duplicates)
```

| Semantics | Behavior | Cost |
|-----------|----------|------|
| **At-most-once** | Commit before process | May lose messages |
| **At-least-once** | Process then commit | Duplicates on crash |
| **Exactly-once** | Transactions + idempotent producer | Complexity, latency, limits |

**Exactly-once is not magic** — it's bounded to Kafka read-process-write within transactional boundaries; side effects to HTTP/DB still need [[Idempotent-key]].

---

## Standard config / commands

### Standard at-least-once consumer (Java sketch)

```properties
enable.auto.commit=false
isolation.level=read_committed   # if producers use transactions
max.poll.interval.ms=300000      # must finish batch before rebalance kills you
```

```java
while (true) {
  ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));
  for (ConsumerRecord<String, String> r : records) {
    process(r);                  // idempotent!
  }
  consumer.commitSync();         // after batch success
}
```

### Commit strategies

| Strategy | When | Risk |
|----------|------|------|
| **Auto commit** | Dev only | Commit before process → loss |
| **Sync per batch** | Default prod | Duplicate whole batch on crash |
| **Async commit** | Higher throughput | Ordering vs failure timing |
| **Store offset in DB** | Effect + offset atomic in one TX | True EOS to external store (outbox) |

### Outbox / transactional pattern

```txt
BEGIN TX
  INSERT business_row ...
  INSERT outbox_event ...
  UPDATE consumer_offsets SET off=...   -- same DB
COMMIT
-- separate publisher reads outbox → Kafka
```

### Stateless consumer group ops

```shell
# Lag — are you keeping up?
kafka-consumer-groups.sh --bootstrap-server BROKER \
  --describe --group my-service

# Reset offset (danger — replay storm)
kafka-consumer-groups.sh --bootstrap-server BROKER \
  --group my-service --topic orders --reset-offsets --to-datetime 2026-07-22T00:00:00.000 \
  --execute

# Who owns partition?
kafka-consumer-groups.sh --describe --group my-service --members --verbose
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Consumer kicked from group | `max.poll.interval` exceeded | Smaller batches; async process + pause; scale consumers |
| Message storm duplicates | Recent deploy before commit | Idempotent handler; dedupe store |
| Lag growing | `RECORDS-LAG-MAX`; slow process | Scale partitions/consumers; optimize handler |
| Lost messages | auto.commit=true | Disable auto commit; commit after success |
| Rebalance loop | Processing > session.timeout | Tune timeouts; static membership `group.instance.id` |
| Offset reset surprise | `auto.offset.reset=latest` new group | Explicit reset policy; document consumer group naming |
| "Exactly-once" but double DB rows | Side effect outside TX | [[Idempotent-key]] or outbox |

```shell
kafka-consumer-groups.sh --describe --group my-service | awk '$6 > 10000 {print}'
```

---

## Gotchas

> [!WARNING]
> **Commit then crash before process** — at-most-once gap if you reversed order wrong.

> [!WARNING]
> **Rebalance during long process** — partition reassigned while still processing → duplicate unless consumer pauses or uses sticky assignor + cooperative rebalance.

> [!WARNING]
> **New consumer group id** — starts at `earliest`/`latest` per config — replays entire topic or skips history.

> [!WARNING]
> **EOS transactions** — throughput hit; not supported all client/lang pairs equally; broker 2.5+ features.

> [!WARNING]
> **Manual offset assignment** — bypasses group coordination — you own failover logic.

> [!WARNING]
> **Stateless myth** — handler almost always writes somewhere; design idempotency anyway.

---

## When NOT to use

- **Commit-before-process** for money movement — unacceptable loss window.
- **Offset reset in prod** without replay capacity — can DDoS your own DB.
- **Kafka transactions** to fix non-idempotent HTTP webhooks — fix the handler instead.

---

## Related

[[kafka]] [[kafka producer and consumer]] [[Kafka broker]] [[Idempotent-key]] [[Concurrent modification]] [[write-ahead logging]]
