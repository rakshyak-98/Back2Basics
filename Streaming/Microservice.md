[[Streaming]] [[ingestion]] [[transcoding]] [[ABR]] [[MPEG-TS]] [[When scaling to hundreds of concurrent channels]]

# Microservice (streaming)

> Service boundaries for video platforms — packager, origin, license, encoder — **not a generic microservices essay**.

---

## Mental model

Streaming stacks fail when teams draw microservices around **org charts** instead of **failure domains and bitrate paths**. Split where **scale, deploy cadence, and blast radius** differ — keep hot paths colocated when IPC cost matters.

```txt
Ingest ──► Transcode ──► Packager ──► Origin/CDN ──► Player
              │              │              │
         GPU fleet      stateless      cache-heavy
         batch+live      CPU bound      egress $$$

         License server ◄── player DRM challenge (isolated trust zone)
         Manifest API   ◄── auth + URL signing (edge-adjacent)
         Ad decision    ◄── low-latency separate from encode
```

| Service | Owns | Scale driver | Split when |
|---------|------|--------------|------------|
| **Ingest** | RTMP/SRT/WebRTC receive | Concurrent live channels | Protocol teams differ |
| **Transcoder** | ABR ladder encode | GPU/CPU | [[NVENC]] fleet independent of API |
| **Packager** | HLS/DASH segments, fmp4 | Disk I/O | Different release from encode codecs |
| **Origin** | Segment storage + tokenized URL | Egress bandwidth | CDN integration cadence |
| **Manifest edge** | Signed playlists, geo rules | RPS, auth | Security isolation |
| **License (DRM)** | Widevine/FairPlay/PlayReady | Crypto compliance | Audit boundary mandatory |
| **Catalog/metadata** | VOD titles, images | CRUD | Classic REST microservice |
| **Analytics/beacon** | QoE events | Write throughput | Never block playback path |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Live start slow | Chain ingest→transcode→packager sync | Async buffer; start packaging lowest rung first |
| Some users no DRM | License region; clock skew | Scale license pool; NTP; geo routing |
| Segments 404 | Origin vs packager path drift | Shared object key contract; integration test |
| CDN stale manifest | Manifest TTL vs segment update | Lower playlist cache; `#EXT-X-MEDIA-SEQUENCE` |
| Encoder backlog | Queue depth metric | Autoscale GPU ASG; shed low-priority VOD |
| Cost spike | Egress from origin not CDN | Cache miss — fix CDN key; origin should not serve 80% traffic |
| One bad channel kills fleet | No bulkhead | Per-tenant quotas; isolate ingest process/containers |

---

## Gotchas

> [!WARNING]
> **Distributed transcode saga** — job state in three services without idempotency → orphan segments on partial failure.

> [!WARNING]
> **License server calls catalog** — outage blocks playback; embed minimal entitlement in signed JWT.

> [!WARNING]
> **Packager + origin shared disk** — NFS on hot path — use object storage.

> [!WARNING]
> **Microservice chat for frame data** — never RPC per frame; shared memory or pipeline in one process.

> [!WARNING]
> **Over-split before [[When scaling to hundreds of concurrent channels]]** — operational tax without revenue-scale need.

---

## When NOT to use

- **MVP single channel** — monolith ingest+package on one box ([[flussonic]], nginx-rtmp module).
- **Split analytics before playback SLO met** — observability yes, service boundary no.
- **Separate team microservice for config flags** — use platform feature flags.

---

## Related

[[Streaming]] [[ingestion]] [[transcoding]] [[ABR]] [[bitrate streaming]] [[MPEG-TS]] [[When scaling to hundreds of concurrent channels]]
