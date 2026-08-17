[[Streaming]] [[ingestion]] [[transcoding]] [[ABR]] [[MPEG-TS]] [[When scaling to hundreds of concurrent channels]]

# Microservice (streaming)

> Service boundaries for video platforms — packager, origin, license, encoder — **not a generic microservices essay**.





## Interview Relevance
Interviewers ask about Microservice to see if you understand the pipeline role, failure modes, and trade-offs — not just the acronym.

## Sources
- [Wikipedia — Microservice](https://en.wikipedia.org/wiki/Microservice) — overview

## Technical Details
```txt
Ingest ──► Transcode ──► Packager ──► Origin/CDN ──► Player
              │              │              │
         GPU fleet      stateless      cache-heavy
         batch+live      CPU bound      egress $$$

         License server ◄── player DRM challenge (isolated trust zone)
         Manifest API   ◄── auth + URL signing (edge-adjacent)
         Ad decision    ◄── low-latency separate from encode
```

### Boundary rules (staff checklist)

```txt
1. Playback path (manifest + segment + license) — p99 < 200ms added latency
   → avoid synchronous chains > 2 hops
2. Transcode job — async queue (SQS/Kafka); never block ingest on encode complete
3. Packager idempotent — same input job ID → same output path (dedupe)
4. Origin stateless — segments on object storage (S3/GCS); nodes cache
5. Signed URL TTL < segment duration risk — tune expiry vs player retry
6. DRM keys — HSM/Vault; license service no dependency on catalog DB at runtime
```

### Example deploy independence

```txt
Team A ships AV1 encode weekly     → transcoder service
Team B ships CDN token format      → manifest signer only
Team C PCI-ish DRM audits          → license server frozen cadence
```

### Anti-boundaries (don't split yet)

```txt
✗ Separate "thumbnail service" on critical path for live start
✗ Microservice per codec if same binary handles all
✗ Chat API in same deployment as packager — OK as module first
```

### Observability per boundary

```shell
# Metrics that map to services
ingest_channels_active
transcode_queue_depth
packager_segment_latency_ms
origin_egress_mbps
license_requests_error_rate
manifest_sign_failures
```

Correlate with player [[ABR]] rebuffer events — not just CPU graphs.

## Real-World Applications
Used wherever Microservice sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **MVP single channel** — monolith ingest+package on one box ([[flussonic]], nginx-rtmp module).
- **Con / skip when:** **Split analytics before playback SLO met** — observability yes, service boundary no.
- **Con / skip when:** **Separate team microservice for configuration flags** — use platform feature flags.

## Comparison
- vs [[flussonic]]: **MVP single channel** — monolith ingest+package on one box ([[flussonic]], nginx-rtmp module).

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Live start slow | Chain ingest→transcode→packager sync | Async buffer; start packaging lowest rung first |
| Some users no DRM | License region; clock skew | Scale license pool; NTP; geo routing |
| Segments 404 | Origin vs packager path drift | Shared object key contract; integration test |
| CDN stale manifest | Manifest TTL vs segment update | Lower playlist cache; `#EXT-X-MEDIA-SEQUENCE` |
| Encoder backlog | Queue depth metric | Autoscale GPU ASG; shed low-priority VOD |
| Cost spike | Egress from origin not CDN | Cache miss — fix CDN key; origin should not serve 80% traffic |
| One bad channel kills fleet | No bulkhead | Per-tenant quotas; isolate ingest process/containers |

- **Distributed transcode saga** — job state in three services without idempotency → orphan segments on partial failure.
- **License server calls catalog** — outage blocks playback; embed minimal entitlement in signed JWT.
- **Packager + origin shared disk** — NFS on hot path — use object storage.
- **Microservice chat for frame data** — never RPC per frame; shared memory or pipeline in one process.
- **Over-split before [[When scaling to hundreds of concurrent channels]]** — operational tax without revenue-scale need.
