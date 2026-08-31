[[Redis]] [[Distributed computing]] [[System design]]

Cache **make copy of data that is used often and stored in a faster, smaller storage layer close to the application**.
- Instantly call the resource that we needed the most frequently.
- Making data retrial faster by keeping frequently resource accessible.

## Locality

Principle that make caching more effect is **Locality** means that data close to already-used data is likely to be used again.

* [[Temporal locality]] Same data again. Data that was recently used is likely to be need it again soon.
* [[Spatial locality]] Nearby data. Data near to the accessed data is more likely to be used in the near future.

- locally relevant data accessibility much faster.

Transient storage is storage used for data that is **temporary and can be safely discarded**.

## Caching Strategies
How the cache interacts with the system of record.

[[Read-through]] cache loads missing data
[[Write-through]] cache + DB update together
[[Write-behind]] cache writes DB asynchronously
[[Refresh-ahead]] renew before

## Cache Hit and Cache Miss

* [[Cache hit]] The requested data is found in the cache.
* [[Cache miss]] The requested data is not found in the cache, so it must be fetched from the original data source.

> [!INFO]
> Caching helps **reduce the load on the primary database**. This can save cost, reduce power usage, and improve application performance.

If the **cache hit rate is very low**, caching may not provide much benefit and can become unnecessary.

A cache is **transient storage**. It is not meant to be the primary database or a permanent archive.

[[Cache mapping]] Which location in the cache a block of main memory can occupy. The CPU has a large memory space but a much smaller cache, so we need a rule to map.

**Main advantage** All application servers can share the same cached data.

**Main disadvantage** There is network cost because the application has to communicate with the cache server.

The application should also have a **fallback mechanism** in case the cache is unavailable.


## Types of Caching

### Multi-Level Cache

A multi-level cache uses more than one cache layer.

For example:

**Application → Local Cache → Distributed Cache → Database**

The local cache is usually faster because it does not require a network request.

If the data is not found in the local cache, the application checks the distributed cache.

If the data is not found there, it gets the data from the database.

# Data Accuracy and Cache Invalidation

Cache invalidation means making sure that old or incorrect cached data is removed or updated.

### Purge

A **purge** removes cached content.

For example, when content on the original server changes, a CDN can purge the old content from its cache.

### Refresh

Instead of removing the cached item, the system fetches the latest data from the original server and replaces the old cached item.

This can happen even before the current cache item expires.

### Bulk Invalidation

Bulk invalidation means **invalidating many cache items at the same time**.

For example, if a large number of products are updated, the application can invalidate all related product cache entries together.


## Expiration & Eviction
Controls cache lifetime and prevents unbounded memory consumption.

[[Cache TTL]] time based expiration
[[LRU]] least recently used
[[LFU]] least frequently used

## Invalidation
- TTL-based
- Explicit invalidation
- Cache-aside

## Effectiveness of a Cache

The effectiveness of a cache can be measured using several metrics.

### Hit Rate / Hit Ratio

The **hit rate** is the percentage of requests that are successfully served from the cache.

**Hit Rate = Cache Hits / Total Requests × 100**

A higher hit rate is generally better.

The main goal of caching is usually to achieve a high hit rate.

**Hit Rate + Miss Rate = 100%**

### Cache Size

Cache size is the amount of data that the cache can store.

A larger cache can potentially increase the hit rate because it can store more data.

However, a larger cache also costs more memory or disk space.

### Cache Latency

Cache latency is the time required to get data from the cache.

Lower latency is better.

A slow cache can reduce the benefit of caching, so the cache should be significantly faster than the original data source whenever possible.
