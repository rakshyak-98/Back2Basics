[[System Design]] [[Streaming]] [[HLS]] [[DASH]] [[ABR]]

# on-demand vs static file (Streaming)

> On-demand vs static — VOD/static files sit on disk/CDN; “on-demand” packaging/transcode happens when requested (or just-in-time), vs pre-packaged assets.

---

## How it works

```txt
Static:   mezz → (batch) → HLS on S3/CDN → players
On-demand: mezz → request → packager/transcoder → CDN cache → players
```

| Mode | Pros | Cons |
|------|------|------|
| **Pre-packaged static** | Predictable CDN hit; simple origin | Storage × renditions; slow publish |
| **Just-in-time / on-demand** | Storage lean; late binding DRM/ladder | First-byte latency; origin CPU |

---


## Configuration and commands

```txt
# Static publish sketch
ffmpeg … → renditions → packager → s3://bucket/asset/master.m3u8

# On-demand sketch
player → CDN → origin packager (miss) → cache segments
```

| Knob | Why |
|------|-----|
| CDN cache key | Include bitrate / token carefully |
| Warmup | Prefetch popular ladder after publish |
| Fallback | Pre-bake poster / audio-only |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| Long startup | Cold JIT transcode | Pre-warm; bake top bitrates |
| 404 segment | Packager race | Atomic publish; retry |
| CDN stampede | Many misses one asset | Request coalesce; longer TTL |
| Huge bill | JIT every unique | Cache; limit ladder |
| DRM mismatch | Late binding fail | Align CPIX/keys pre-play |

---


## Comparison

| Criterion | Option A | Option B |
|-----------|----------|----------|
| … | … | … |


## How to choose

- Choose **A** when …
- Choose **B** when …


## Gotchas

> [!WARNING]
> **“Static file” still needs manifests** — players want HLS/DASH, not one giant MP4 (unless progressive).

> [!WARNING]
> **On-demand without cache** — origin becomes the bottleneck.

> [!WARNING]
> **Live ≠ VOD on-demand** — live has different latency/GOP rules ([[HLS]] / [[DASH]]).

---


## When not to use

- **True live events** — live pipeline, not VOD JIT.
- **Tiny catalog rarely played** — maybe progressive MP4 is enough.
- **No CPU budget at edge** — pre-package everything.

---


## Related

[[Streaming]] [[HLS]] [[DASH]] [[ABR]] [[transcoding]] [[rendition]]

## Sources

- [Wikipedia — on-demand vs static file](https://en.wikipedia.org/wiki/on-demand_vs_static_file)
