[[Streaming]] [[Live Streaming Architecture Multi-Channel Distribution at 1M Concurrent User]] [[backpressure]]

# When scaling to hundreds of concurrent channels

> Many live channels at once — isolate encode/ingest per channel so one bad feed doesn’t take the fleet.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Treat each channel as its own pipeline (ingest → transcode → packager → CDN); share platforms, not fate.

```txt
Channel N:  ingest ──► transcoder ──► packager ──► origin/CDN
                 │           │
                 └─ isolate CPU/GPU / limits per channel
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Channel** | One live program | “Own ingest URL and ABR ladder.” |
| **Noisy neighbor** | One encode starves others | “Cap CPU/GPU per channel.” |
| **Packager** | HLS/DASH segments | “Shared packager pool with quotas.” |
| **Backpressure** | Slow down ingest | “Drop/degrade before OOM.” |

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| All channels lag | Shared transcoder saturated | Add capacity; lower ladder |
| One channel spikes CPU | Encode settings / input | Cap; restart that pipeline |
| Origin 5xx storm | Packager backlog | Scale packagers; shed load |
| Wrong channel content | Routing / keyer | Fix channel_id mapping |

---

## Gotchas

> [!WARNING]
> **Shared giant process** — one ffmpeg supervising “all channels” is an outage waiting to happen.

> [!WARNING]
> **No per-channel SLOs** — fleet averages hide the channel that is on fire.

---

## When NOT to use

- **Single 24/7 linear channel** — simpler dedicated box is enough.
- **VoD only** — no live concurrency problem; use normal ABR+CDN.

## Related

[[Live Streaming Architecture Multi-Channel Distribution at 1M Concurrent User]] [[ABR]] [[backpressure]] [[transcoding]]
