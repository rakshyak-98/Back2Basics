[[Eventual consistency]] [[backpressure]] [[Real-time Subscription]] [[database sharding]] [[API design]]

# Food delivery

> Food-delivery platforms combine geo discovery, transactional ordering, and real-time logistics — separate read-heavy catalog search from write-heavy order state machines with explicit cancellation rules.

```txt
        Food delivery ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Classic system-design case: geo index, order state machine, courier realtime,…

## Sources
- Kleppmann, *Designing Data-Intensive Applications* — overview
- Industry postmortems on marketplace logistics (public eng blogs) — overview

## Key Concepts
- **Split read/write paths:** menu search vs order writes.
- **Geo index:** tiles/geohash/search for radius sort.
- **Order state machine:** placed→accepted→preparing→picked→delivered/cancelled.
- **Realtime:** courier location via [[Real-time Subscription]].

## Technical Details
| Requirement | Design response |
|-------------|-----------------|
| High QPS catalog | Cache menus; shard by region/restaurant |
| Radius sort | Geospatial index |
| Order integrity | Stronger consistency / reservations on critical steps |
| Courier tracking | Pub/sub or websocket fanout |
| Peak dinner spike | [[backpressure]], autoscaling, load shed |

- Shard orders by region/restaurant ([[database sharding]]).
- Menus can be [[Eventual consistency]]
- APIs: [[API design]] with idempotent place-order.

## Mistakes to Avoid
- **Mistake:** One mega-service owning search, payments, and tracking
- **Mistake:** No cancellation/compensation story when restaurant rejects
- **Mistake:** Unbounded location update fanout without [[backpressure]]

## Pros/Cons or Trade-offs
- **Cached menus:** fast reads; stale prices risk.
- **Fine-grained realtime:** great UX; fanout cost.
- **Trade-off:** city-wide shard vs restaurant shard locality.

## Comparison
- vs generic e-commerce: adds geo + courier assignment + tight SLAs.
- vs [[Splitwise]]: marketplace logistics vs shared-expense ledger.


### Use cases
- DoorDash/Uber Eats-style marketplaces and regional food logistics platforms.
