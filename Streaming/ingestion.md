[[Streaming]] [[RTMP]] [[Encoding]] [[transcoding]] [[OBS]] [[Microservice]]

# Ingestion

> Accept live or file video into the processing pipeline — **front door** where protocols, validation, and backpressure matter first.

---

## Mental model

**Ingestion** is the **entry point** that accepts publisher streams (live) or uploads (VoD), validates them, buffers briefly, and hands off to **encode/package** workers. Failures here are **total outages** for a channel — design for **protocol diversity, auth, and isolation per tenant**.

```txt
Publisher (OBS, encoder, partner)
        │
   ┌────┴────┬──────────┬──────────┐
 RTMP    SRT/WebRTC   S3 upload   API pull
   │        │              │           │
   └────────┴──────────────┴───────────┘
                    │
            Ingest tier (auth, validate)
                    │
         Buffer / queue ──► [[transcoding]] / packager
```

| Input type | Typical protocol | Latency | Ops note |
|------------|------------------|---------|----------|
| **Live encoder** | [[RTMP]], SRT | seconds | Persistent connection |
| **Browser** | WebRTC WHIP | sub-second | Signaling + TURN |
| **VoD file** | HTTPS multipart | minutes | Async job queue |
| **Broadcast feed** | UDP MPEG-TS | seconds | Multicast / Zixi |

Ingest is **not** CDN delivery — keep hot path lean; don't sync-call catalog DB on every keyframe.

---

## Standard config / commands

### RTMP ingest auth pattern (nginx-rtmp style)

```nginx
rtmp {
    server {
        listen 1935;
        application live {
            live on;
            on_publish http://api.internal/auth/rtmp?key=$name;
            idle_streams off;
        }
    }
}
```

Validate stream key → tenant → channel ID before accepting.

### ffmpeg — pull ingest → push origin

```bash
# Pull partner RTMP, remux to local packager (no re-encode if compatible)
ffmpeg -i rtmp://partner/live/event -c copy -f flv rtmp://localhost/live/event

# SRT listener ingest
ffmpeg -i srt://0.0.0.0:9000?mode=listener -c copy -f flv rtmp://127.0.0.1/live/key
```

### VoD upload → job queue

```txt
POST /upload → S3 presigned URL
S3 event → SQS → transcode worker (probe → ladder → [[HLS]]/[[DASH]])
Job states: RECEIVED → PROBING → TRANSCODING → PACKAGED → READY
```

### Health checks

```bash
# RTMP port open
nc -zv ingest.example.com 1935

# Probe live stream
ffprobe -v error -show_format -show_streams rtmp://ingest/live/key

# Ingest lag (OBS → origin segment age)
curl -sI "https://origin/live/index.m3u8" | grep -i age
```

### Per-channel isolation

```txt
Container / process per high-value channel
CPU/memory quotas — one bad publisher can't starve fleet
Max bitrate enforcement at ingest (drop or disconnect)
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| OBS "Failed to connect" | DNS, 1935 blocked, bad key | Security group; rotate key; TLS RTMPS if required |
| Connect then immediate drop | Auth callback timeout | Scale auth service; fail-open only if contract allows |
| Frozen picture, audio OK | Publisher stopped sending video | OBS scene empty; encoder crash |
| All channels down | Shared ingest node | Bulkhead; multi-AZ ingest pool |
| VoD stuck QUEUED | Worker backlog | Scale transcode ASG; priority queue |
| A/V sync at ingest | Wrong `-itsoffset` upstream | Fix publisher; don't patch in packager only |
| High latency from day one | Too many sync transcode hops | `-c copy` to packager when possible |

---

## Gotchas

> [!WARNING]
> **Ingest auth in player** — auth belongs on **publish**, not only playback URL.

> [!WARNING]
> **RTMP buffer bloat** — publisher on bad Wi-Fi fills server buffers; set idle disconnect.

> [!WARNING]
> **Same stream key reuse** — collision kicks prior publisher; use unique keys per event.

> [!WARNING]
> **Probe untrusted uploads** — ffprobe shell on malicious files; sandbox workers.

> [!WARNING]
> **Geo-locked partners** — whitelist IPs; don't expose global open RTMP.

---

## When NOT to use

- **Client-direct to CDN** — browsers don't publish RTMP; use WebRTC/WHIP or dedicated encoder.
- **Heavy ML on ingest thread** — offload analysis async; keep ingest I/O bound.
- **Synchronous full transcode before ACK** — accept stream, process async ([[Microservice]] boundary).

---

## Related

[[RTMP]] [[OBS]] [[Encoding]] [[transcoding]] [[Single Stream]] [[Multi Stream]] [[Microservice]] [[HES Architecture]]
