[[Streaming]] [[Live Streaming Architecture Multi-Channel Distribution at 1M Concurrent User]] [[backpressure]] [[ABR]] [[transcoding]]

# When scaling to hundreds of concurrent channels

> Many live channels at once — isolate encode/ingest per channel so one bad feed doesn’t take the fleet.

```txt
        When scaling to hu ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               └── Trade-offs
```

## Why It Matters
- **Key signal:** Multi-channel live scale questions probe isolation

## Sources
- [AWS — Live streaming](https://aws.amazon.com/media/tech/live-streaming/) — overview
- [Apple HLS](https://developer.apple.com/documentation/http-live-streaming) — deep-dive

## Key Concepts
```txt
- **Note:** Channel N: ingest ──► transcoder ──► packager ──► origin/CDN
                 │           │
                 └─ isolate CPU/GPU / limits per channel
```

### Review map (words you can say)

| Word | Plain meaning | Say in review |
|------|---------------|------------------|
| **Channel** | One live program | “Own ingest URL and ABR ladder.” |
| **Noisy neighbor** | One encode starves others | “Cap CPU/GPU per channel.” |
| **Packager** | HLS/DASH segments | “Shared packager pool with quotas.” |
| **Backpressure** | Slow down ingest | “Drop/degrade before OOM.” |

## Technical Details
```txt
Per channel budget (example):
- 1 ingest connection
- N ABR rungs (aligned GOP)
- CPU/GPU quota + max bitrate
- Separate metrics labels: channel_id
```

| Knob | Why it matters |
|------|----------------|
| Per-channel quotas | Stops one 4K encode from killing neighbors |
| Horizontal packagers | Scale segment writers independently |
| Channel-labeled metrics | Find the bad feed fast |

### Failure signals

| Symptom | Check | Fix |
|---------|-------|-----|
| All channels lag | Shared transcoder saturated | Add capacity; lower ladder |
| One channel spikes CPU | Encode settings / input | Cap; restart that pipeline |
| Origin 5xx storm | Packager backlog | Scale packagers; shed load |
| Wrong channel content | Routing / keyer | Fix channel_id mapping |

## Mistakes to Avoid
- **Mistake:** Shared giant process
- **Mistake:** No per-channel SLOs

## Pros/Cons or Trade-offs
- **Trade-off:** Single 24/7 linear channel — simpler dedicated box is enough.
- **Trade-off:** VoD only — no live concurrency problem; use normal ABR+CDN.
