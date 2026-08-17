[[Architectures]] [[Streaming]] [[CDN]] [[HLS]] [[DASH]] [[ABR]] [[When scaling to hundreds of concurrent channels]]

# Live Streaming Architecture Multi-Channel Distribution at 1M Concurrent User

> 1M concurrent live viewers — push encode once, fan out via CDN/edge; origin must not serve every player directly.

```txt
        Live Streaming Arc ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Interview Relevance
- **Interview probes:** 1M-viewer live design interviews test encode-once/fan-out via CDN, origin pro…

## Sources
- [Apple — HLS documentation](https://developer.apple.com/documentation/http-live-streaming) — deep-dive
- [DASH Industry Forum](https://dashif.org/) — overview
- [AWS — Live streaming on AWS](https://aws.amazon.com/media/tech/live-streaming/) — overview

## Key Concepts
```txt
camera/encoder → origin ingest → transcoder → packager
                                      ↓
                              origin store/manifest
                                      ↓
                                   CDN edges → players
```

| Layer | Scales with |
|-------|-------------|
| Ingest/transcode | # channels / bitrates |
| CDN | # viewers |
| DRM/license | concurrent license QPS |

## Technical Details
```txt
ABR: 1080p/720p/480p ladders, 2–6s segments
CDN: cache manifests short TTL; segments longer
Origin shield: protect packager
Health: stale manifest / 404 segment alerts
```

| Knob | Why it matters |
|------|----------------|
| Segment duration | Latency vs efficiency |
| Manifest TTL | Channel switch freshness |
| Origin shield | Hot-key protection |
| Regional PoPs | Last-mile |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| Origin meltdown | Cache hit ratio | Shield; longer segment TTL |
| Buffering spike | Edge 5xx / bitrate | Failover PoP; ABR ladder |
| Channel start fail | Packager lag | Autoscale transcoder |
| DRM errors | License service | Scale license; clock skew |
| Hot manifest | Tiny TTL + thundering herd | Soft TTL; collapse requests |

## Mistakes to Avoid
- **Mistake:** WebRTC fanout ≠ OTT scale — use CDN HLS/DASH for 1M
- **Mistake:** Short TTL everywhere — origin death
- **Mistake:** One giant origin — multi-CDN / shield

## Pros/Cons or Trade-offs
- **Trade-off:** <1k viewers interactive — WebRTC/SFU maybe.
- **Trade-off:** VOD only — simpler caching.
- **Trade-off:** Ultra-low-latency betting UX — specialized LL-HLS/WebRTC stacks.
