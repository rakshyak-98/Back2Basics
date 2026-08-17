[[Eventual consistency]] [[backpressure]] [[Real-time Subscription]] [[database sharding]] [[API design]]

# Food delivery

> Food-delivery platforms combine geo discovery, transactional ordering, and real-time logistics — separate read-heavy catalog search from write-heavy order state machines with explicit cancellation rules.





## Interview Relevance
Classic system-design case: geo index, order state machine, courier realtime, and where eventual consistency is/ isn’t OK.

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

Shard orders by region/restaurant ([[database sharding]]). Menus can be [[Eventual consistency]]; payments/inventory need stronger guarantees. APIs: [[API design]] with idempotent place-order.

## Real-World Applications
DoorDash/Uber Eats-style marketplaces and regional food logistics platforms.

## Pros/Cons or Trade-offs
- **Cached menus:** fast reads; stale prices risk.
- **Fine-grained realtime:** great UX; fanout cost.
- **Trade-off:** city-wide shard vs restaurant shard locality.

## Comparison
- vs generic e-commerce: adds geo + courier assignment + tight SLAs.
- vs [[Splitwise]]: marketplace logistics vs shared-expense ledger.

## Mistakes to Avoid
- One mega-service owning search, payments, and tracking.
- No cancellation/compensation story when restaurant rejects.
- Unbounded location update fanout without [[backpressure]].
