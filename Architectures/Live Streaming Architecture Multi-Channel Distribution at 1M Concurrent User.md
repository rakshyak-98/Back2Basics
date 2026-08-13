<!-- note-strategy: decision -->
[[Architectures]] [[Streaming]] [[CDN]] [[HLS]] [[DASH]]

# Live Streaming Architecture Multi-Channel Distribution at 1M Concurrent User

> 1M concurrent live viewers — push encode once, fan out via CDN/edge; origin must not serve every player directly.

---

## Index

- [[#Context]]
- [[#Decision]]
- [[#Consequences]]
- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Alternatives considered]]
- [[#Related]]

## Context

…

## Decision

We will … because …

## Consequences

**Positive:** …

**Negative / trade-offs:** …

## Mental model

**Say it in one breath:** Ingest → transcode ABR ladder → packager (HLS/DASH) → origin → CDN edge → players. Scale viewers at the edge; scale channels at encode/packager capacity.

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

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Origin meltdown | Cache hit ratio | Shield; longer segment TTL |
| Buffering spike | Edge 5xx / bitrate | Failover PoP; ABR ladder |
| Channel start fail | Packager lag | Autoscale transcoder |
| DRM errors | License service | Scale license; clock skew |
| Hot manifest | Tiny TTL + thundering herd | Soft TTL; collapse requests |

---

## Gotchas

> [!WARNING]
> **WebRTC fanout ≠ OTT scale** — use CDN HLS/DASH for 1M.

> [!WARNING]
> **Short TTL everywhere** — origin death.

> [!WARNING]
> **One giant origin** — multi-CDN / shield.

---

## When NOT to use

- **<1k viewers interactive** — WebRTC/SFU maybe.
- **VOD only** — simpler caching.
- **Ultra-low-latency betting UX** — specialized LL-HLS/WebRTC stacks.

---

## Alternatives considered

| Alternative | Why rejected |
|-------------|--------------|
| … | … |

## Related

[[Streaming]] [[HLS]] [[DASH]] [[ABR]] [[CDN]] [[When scaling to hundreds of concurrent channels]]
