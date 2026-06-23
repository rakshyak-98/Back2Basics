## Executive Summary

Streaming 1M+ concurrent users across multiple live TV channels requires a distributed edge-caching model that offloads compute-heavy operations (ingest, encoding, packaging) to centralized origin infrastructure while distributing bandwidth delivery across a global Content Delivery Network (CDN). The architecture prioritizes:

- **Resilience**: Redundant ingest paths and failover mechanisms
- **Scale**: Origin shield layer to prevent origin exhaustion
- **Efficiency**: 99%+ CDN cache hit ratio via segment reuse
- **QoE**: Adaptive bitrate streaming to heterogeneous clients

---

## Architecture Layers

### Layer 1: Contribution (Broadcast Ingest)

**Components**: Satellite feeds, fiber uplinks, on-premise hardware encoders

**Protocol Stack**:

- SRT (Secure Reliable Transport) - primary
- Zixi - backup/redundant path
- RTMP - legacy fallback

**Characteristics**:

- High-quality, lightly compressed source feeds (1080p or higher)
- Dual ingest pathways to eliminate single point of failure
- Latency: 0-2 seconds RTT to origin
- Throughput: Varies by channel; each feed typically 20-100 Mbps raw bandwidth

**Failure Handling**: Automatic failover to backup ingest; encoder detects feed loss and triggers alert to operations team.

---

### Layer 2: Transcoding & Encoding

**Components**: Hardware-accelerated encoder farm (GPU or ASIC-based)

**Codec Strategy**:

- Primary: H.264 (AVC) for broad device compatibility
- Secondary: H.265 (HEVC) for bandwidth-constrained regions
- Emerging: AV1 for ultra-low-bandwidth scenarios (optional, compute-intensive)

**Adaptive Bitrate (ABR) Ladder per Channel**:

```
1080p @ 6 Mbps   (high-quality WiFi / wired)
720p  @ 3 Mbps   (good mobile / 4G)
480p  @ 1.5 Mbps (constrained mobile)
360p  @ 0.8 Mbps (low-bandwidth fallback)
```

**Processing Model**:

- Real-time, low-latency transcoding (2-4 second algorithmic latency)
- Redundant encoding: Each channel encoded on N independent encoders; output feeds are bit-identical
- Hardware acceleration: NVIDIA, Intel QuickSync, or Apple ProRes hardware to minimize CPU overhead

**Output**: N ABR variants per channel, each as H.264 elementary stream

---

### Layer 3: Packaging & Segmentation

**Components**: Just-In-Time (JIT) packager, segment writer

**Packaging Formats**:

- HLS (HTTP Live Streaming): Apple iOS, macOS, Safari
    - Manifest: `.m3u8` playlist with segment URIs and duration metadata
    - Segment Duration: 2-6 seconds (typically 4 seconds)
    - Manifest Update Cadence: 1-2 new segments every 4 seconds
- MPEG-DASH: Android, Smart TVs, web browsers
    - Manifest: `.mpd` (Media Presentation Description) XML
    - Segment Duration: Synchronized with HLS (4 seconds)
    - Dynamic manifest refresh same cadence as HLS

**Segment Lifecycle**:

1. Encoder outputs ABR elementary streams
2. Packager receives NAL units in real-time
3. Packager accumulates 4-second chunks, adds headers (ftyp, mdat boxes)
4. Segment flushed to origin storage; manifest updated atomically
5. Old segments (typically >60 seconds of history) purged from origin NVMe

**Storage**: High-speed NVMe (e.g., AWS NVMe instances, dedicated SSD arrays) on origin; typical retention = 120 seconds of rolling buffer per ABR variant.

---

### Layer 4: Origin Server & Storage

**Components**: Origin compute instance, segment storage, manifest cache

**Role**:

- Single authoritative source for all manifest and segment data
- Atomic writes to prevent partial segment delivery
- Low-latency random-access segment retrieval for edge node requests

**Storage Capacity**:

- Retention Policy: ~120 seconds of rolling segments per ABR variant
- Per-Channel Storage Footprint (120-second rolling):
    - 4 ABR variants × 30 segments × avg. 1.5 MB/segment ≈ 180 MB per channel
    - For 50 channels: ~9 GB total

**Request Profile**:

- Manifest queries: ~1000 req/sec per channel (very small payload, ~1 KB)
- Segment queries (pre-shield): Would be ~1M req/sec without origin shield; post-shield: <10K req/sec

**Network Path**: Origin sits in a single geographic region (e.g., us-east-1 AWS) with low-latency egress to origin shield.

---

### Layer 5: Origin Shield

**Components**: Distributed caching layer between origin and CDN edge PoPs

**Deduplication Model**:

- When 10,000 edge nodes simultaneously request segment `channel_1_segment_42.m4s`, the shield consolidates all requests
- Shield fetches segment once from origin, caches it, serves all 10,000 requests from shield cache
- Result: Reduces origin request load by 100-1000× (depending on edge PoP density)

**Cache Hit Behavior**:

- Hit Rate: 95-98% (all edge PoPs are requesting historical segments)
- Latency: <10 ms origin → shield (co-located or nearby)

**Sizing & Geography**:

- Deployed in 3-5 regional zones globally (e.g., us-east, eu-west, ap-southeast)
- Each shield handles requests from nearby CDN PoPs
- Memory: Typical L1 cache 10-100 GB per shield instance

---

### Layer 6: Content Delivery Network (CDN)

**Architecture**:

```
Core PoPs        (10-15 globally, high capacity)
  ↓
Regional PoPs    (50-100, medium capacity)
  ↓
Edge PoPs        (1000+, dense population coverage)
```

**CDN Cache Hierarchy**:

- **L1 Cache (Edge PoP)**: SSD-backed, ~1-10 TB per PoP, nearest to end-user (~5-20 ms)
- **L2 Cache (Regional Hub)**: Larger capacity, feeds multiple edge PoPs
- **L3 Cache (Core)**: Origin shield + regional aggregation

**Cache Hit Ratio**:

- Edge Hit Ratio: 99%+ (all users watching same live channel request identical segments in time window)
- Reason: Live streams have 60-120 second retention; all 1M users cluster around same segment IDs

**Bandwidth Multiplexing**:

- Each edge PoP has 10-100 Gbps outbound capacity
- For 1M users × 2 Mbps avg. bitrate = 2 Tbps aggregate demand
- Distributed across 1000+ edge PoPs: 2 Tbps / 1000 = 2 Gbps per PoP (well within capacity)

**Request Routing**:

- DNS-based geolocation or HTTP redirect to nearest edge PoP
- Client device sent manifest pointing to CDN domain (e.g., `video.cdn.example.com`)
- Client DNS query resolved to nearest PoP by anycast or Geo-DNS

---

### Layer 7: Client Playback

**Components**: Streaming client library (hls.js, ExoPlayer, AVPlayer, Shaka Player)

**Adaptive Bitrate (ABR) Algorithm**:

1. Client fetches manifest (`.m3u8` or `.mpd`) from edge PoP
2. Measures recent network throughput (rolling average over last 5-10 seconds)
3. Selects bitrate variant that matches current throughput:
    - If bandwidth > 6 Mbps → request 1080p segment
    - If bandwidth 3-6 Mbps → request 720p segment
    - If bandwidth < 1.5 Mbps → request 360p segment
4. Buffers 10-30 seconds ahead
5. On bandwidth spike → upgrade bitrate; on bandwidth drop → downgrade

**Manifest Polling**:

- Client polls manifest every 4-8 seconds to discover new segments
- Each poll is small (1-2 KB), typically cache-hit at edge
- Zero latency penalty; request served from CDN edge cache

**Error Handling**:

- Segment 404 → fallback to lower bitrate
- Manifest stale → client retries with exponential backoff
- Network timeout → buffer consumed; if buffer exhausted → player pauses, resumes when connectivity restored

---

## Data Flow Summary

```
[Broadcast Feed] 
      ↓ (SRT/Zixi - primary + backup)
[Ingest Gateway] 
      ↓ (NAL units, raw H.264 streams)
[Encoding Farm] 
      ↓ (4 ABR variants output)
[JIT Packager] 
      ↓ (segment.m4s + manifest.m3u8)
[Origin NVMe Storage] 
      ↓ (atomic writes, ~120 sec rolling window)
[Origin Shield Cache] 
      ↓ (consolidates 10K simultaneous requests into 1)
[CDN Edge PoPs] 
      ↓ (99%+ cache hit, 1000+ nodes)
[1M End-User Clients] 
      ↓ (HTTP GET → nearest edge, adaptive bitrate selection)
[Device Playback] 
      (HLS/DASH player, video renderer)
```

---

## Performance Characteristics

|Metric|Value|Notes|
|---|---|---|
|**End-to-End Latency**|8-15 seconds|Ingest (2-4s) + Packaging (4s) + Segment buffer (2-10s)|
|**Origin Request Load (pre-shield)**|~1M req/sec|Would overwhelm single origin|
|**Origin Request Load (post-shield)**|<10K req/sec|100-1000× reduction via deduplication|
|**CDN Cache Hit Ratio**|>99%|Live streams naturally cluster requests|
|**Segment Size (avg)**|1.5 MB @ 3 Mbps ABR|Varies by codec and bitrate|
|**Manifest Payload**|1-2 KB|Tiny; always cache-hit at edge|
|**Per-User Bandwidth (ABR avg)**|2 Mbps|Assuming 720p for median user|
|**Total Outbound BW (1M users)**|~2 Tbps|Distributed across CDN edge PoPs|
|**Segment Duration**|4 seconds|Standard; balanced latency vs. overhead|

---

## Scaling Considerations

### Horizontal Scaling (Adding More Viewers)

- **Problem**: 1M → 10M concurrent users
- **Solution**: CDN scales linearly; add edge PoPs or increase per-PoP capacity
- **Bottleneck**: Origin server request rate peaks at shield boundaries; shard origin by channel to mitigate

### Adding Channels

- **Problem**: 50 channels → 500 channels
- **Solution**:
    - Encoding farm scales linearly (add more encoder instances)
    - Origin storage scales linearly (~180 MB per channel)
    - Origin request load scales linearly per shield region
    - CDN capacity unaffected (segments reused per channel; hit ratio remains >99%)
- **Bottleneck**: Packaging throughput; JIT packager must sustain N channels in real-time

### Geographic Expansion

- **Problem**: Latency to distant regions exceeds acceptable threshold
- **Solution**:
    - Deploy regional origin mirrors (read-only copies via replication)
    - Deploy regional origin shield layers
    - Deploy regional CDN edge PoP clusters
- **Trade-off**: Introduces replication lag (~100-500 ms); acceptable for live sports, news

---

## Failure Modes & Resilience

|Failure|Impact|Mitigation|
|---|---|---|
|**Ingest Path Failure**|Single encoder affected; channel offline if no backup|Dual-path SRT + Zixi; auto-failover within 5 sec|
|**Encoding Farm Node Down**|ABR variants unavailable; downstream failures|N+1 redundancy; stateless encoders; quick replacement|
|**Origin Disk Full**|New segments drop; clients see stale manifest|Automated rotation; pre-computed storage quotas|
|**Origin Shield Cache Failure**|Origin request rate spikes 100×; origin may saturate|Multi-region shield deployment; cache replication|
|**CDN Edge PoP Offline**|Users in that region rerouted to next-nearest PoP; latency increases|Geo-DNS failover; 100+ redundant edge PoPs|
|**Packaging Timeout**|Segment never written; manifest goes stale; 4-sec buffer drain|Watchdog timers; fallback to 2-segment retention mode|

---

## Operational Metrics & Monitoring

**Real-Time KPIs**:

- Origin request rate (target: <50K req/sec)
- Origin shield hit ratio (target: >95%)
- CDN edge hit ratio (target: >99%)
- P95 segment delivery latency to clients (target: <500 ms)
- Manifest freshness (age of latest segment in client buffer)
- Player rebuffering rate (target: <1 rebuffer per 10K views)

**Alerting Thresholds**:

- Ingest feed RTT > 3 sec → investigate path quality
- Origin request spike > 100K req/sec → enable emergency cache mode or shed low-quality viewers
- CDN cache hit ratio drop below 95% → investigate cache eviction or flash crowds
- Manifest age > 20 seconds → packager lag detected; increase segment buffer or add packaging capacity

---

## Security & DRM Considerations

**Segment Protection**:

- HTTPS encryption in transit (TLS 1.3)
- Token-based access control: CDN verifies client token before serving segment
- DRM (Optional): Widevine/PlayReady/FairPlay for premium content; decrypt key provisioned to player via separate license server

**Origin Protection**:

- Origin not directly accessible; all client requests proxied through CDN
- Origin shield acts as security boundary; DDoS scrubbing happens at CDN edge

**Manifest Signing**:

- Manifest is public (no secrets); no signing required
- All security enforcement is segment-level (token + DRM)

---

## Cost Optimization

**Primary Cost Drivers**:

1. **Encoding**: CPU/GPU hardware-accelerated transcoding
2. **CDN Bandwidth**: Outbound traffic multiplied across edge PoPs
3. **Origin Storage**: NVMe SSD for sub-second latency
4. **Origin Egress**: Data leaving origin to origin shield

**Cost Reduction Strategies**:

- Use H.265 codec to reduce bitrate 30-40% at same quality
- Increase segment duration to 6 sec (reduce manifest polling overhead)
- Cache long-duration content on CDN edge (avoid re-encoding VOD)
- Use regional origin mirrors to reduce intra-region replication costs

---

## Conclusion

Live streaming at 1M concurrent users is enabled by a three-tier caching model:

1. **Origin**: Centralized compute-heavy ingest, encoding, and packaging
2. **Origin Shield**: Deduplication layer that protects origin from load
3. **CDN Edge**: Distributed bandwidth delivery with 99%+ cache efficiency

The architecture achieves sub-second latency across the encoding pipeline and seconds-long end-to-end latency with <1% rebuffering by distributing request load exponentially across geography while maintaining bit-identical segment delivery to all viewers of the same channel.



## Rungs 

**4 [[ABR]] rungs** = **4 quality levels (steps) in an ABR ladder**.

**Rung** = one bitrate + resolution combination.

Example:

| Rung | Resolution | Bitrate  |
| ---- | ---------- | -------- |
| 1    | 360p       | 800 Kbps |
| 2    | 480p       | 1.5 Mbps |
| 3    | 720p       | 3 Mbps   |
| 4    | 1080p      | 6 Mbps   |

Player switches between these rungs based on network conditions.

```text
Good internet
↓
1080p (Rung 4)

Internet slows
↓
720p (Rung 3)

Internet slower
↓
480p (Rung 2)

Very slow
↓
360p (Rung 1)
```

### Why called a "rung"?

Like a ladder:

```text
1080p ← Rung 4
720p  ← Rung 3
480p  ← Rung 2
360p  ← Rung 1
```

Collectively:

```text
Multiple rungs = ABR ladder
```

### Each rung usually defines

- Resolution (360p, 720p, ...)
    
- Video bitrate
    
- Audio bitrate
    
- Codec (H.264, H.265, AV1)
    
- Frame rate (sometimes)
    

### Real-world example

Streaming platforms may have **6-10 rungs**, not just 4.

Example:

```text
240p
360p
480p
720p
1080p
1440p
2160p (4K)
```

**Definition:**

> **ABR rung = one encoded representation/quality level that a player can switch to during adaptive bitrate streaming.**