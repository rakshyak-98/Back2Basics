application owns the cache population and invalidation; database owns correctness.
- also called **lazy caching**

The application explicitly reads from the cache first and loads data from the database only after a cache miss. The cache is not the source of truth: the database owns durable state, while the cache stores temporary copies.

the constraint forcing this design is that database access is usually more expensive than an in-memory lookup, while the workload justifies caching when the same data is read repeatedly and can tolerate some bounded staleness. **Do not use cache-aside for data that must always be read from the authoritative store with strict freshness**; use the database directly, or a consistency-oriented caching strategy such as **write-through** depending on the requirement.

The most important property is that **a cache miss is not an error.** it is an expected condition. The application must always have a path to the database.

The reason we generally **delete rather than update the cache** after a database write is that invalidation is simpler and avoids duplicating database-update logic in the caching path. It also avoids putting an uncommitted or incorrectly transformed representation into the cache. 