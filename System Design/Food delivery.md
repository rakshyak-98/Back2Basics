[[Eventual consistency]] [[backpressure]] [[Real-time Subscription]] [[database sharding]] [[API design]]

# Food delivery

> Food-delivery platforms combine geo-local discovery, transactional ordering, and real-time logistics — separate read-heavy catalog search from write-heavy order state machines with explicit cancellation rules.

---

## Constraints drive architecture

| Requirement (example) | Design response |
|-----------------------|-----------------|
| Large daily active users, kilo-queries per second | Cache menus; shard orders by region or restaurant |
| Sort restaurants within radius | Geospatial index (tiles, geohash, search engine) |
| Cancel until cooking starts | Server-enforced state machine |
| Sub-two-second order accept | Synchronous persist of order; async dispatch and notify |
| Status on every transition | Pub/sub or push ([[Real-time Subscription]]) |

```txt
Customer → API → Order service → events → Restaurant / Dispatch / Notify
                      │
                      └── durable order log (years of retention)
```

## Order state machine

```txt
created → accepted → cooking → ready → picked_up → delivered
                  ↘ cancelled (only before cooking, server-side guard)
```

| Store | Role |
|-------|------|
| Catalog / search | Elasticsearch or OpenSearch + content delivery network |
| Orders | Strongly consistent primary (money path) |
| Dispatch | Matching service, estimated time of arrival models |
| Notifications | Queue → push / short message service |

## Critical paths

**Checkout** must revalidate price and item availability — menu cache can be stale ([[cache system]]). **Payment** requires idempotency keys on create ([[API design]]) to survive retries.

**Dispatch** is asynchronous; customers tolerate assignment delay more than wrong "delivered" status. Dedupe notifications by `order_id + state`.

## Hot spots and overload

Stadium or city-wide demand spikes need **surge capacity** and **demand shedding** ([[backpressure]]) — cap concurrent orders per kitchen, extend estimated time of arrival, or pause new accepts.

## Interview versus production

Pin **queries per second**, **latency service level objectives**, and **consistency** for money before drawing boxes. A single-restaurant point-of-sale does not need a marketplace architecture.

## Sources

- Uber Engineering blog — dispatch, geospatial indexing, surge pricing.
- DoorDash engineering — order pipeline and logistics optimization.
- Martin Kleppmann, *Designing Data-Intensive Applications* — workflow and event-driven patterns.
