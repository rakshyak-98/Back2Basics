[[Streaming]] [[RTMP]] [[SRT]] [[RTSP]] [[Encoding]] [[transcoding]] [[OBS]] [[Microservice]] [[Single Stream]] [[Multi Stream]] [[HES Architecture]]

# Ingestion

> Accept live or file video into the processing pipeline — **front door** where protocols, validation, and backpressure matter first.

```txt
        Ingestion ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Ingestion to see if you understand the pipeline role, …

## Sources
- [Wikipedia — ingestion](https://en.wikipedia.org/wiki/ingestion) — overview

## Key Concepts
- **Note:** **Ingestion** is the **entry point** that accepts publisher streams (live) or…

| Input type | Typical protocol | Latency | Ops note |
|------------|------------------|---------|----------|
| **Live encoder** | [[RTMP]], [[SRT]] | seconds | Persistent connection |
| **IP camera / NVR** | [[RTSP]] | seconds–minutes | Pull PLAY; often transcode to [[HLS]] |
| **Browser** | WebRTC WHIP | sub-second | Signaling + TURN |
| **VoD file** | HTTPS multipart | minutes | Async job queue |
| **Broadcast feed** | UDP MPEG-TS | seconds | Multicast / Zixi |

- **Note:** Ingest is **not** CDN delivery

## Technical Details
```txt
Publisher (OBS, encoder, partner)
        │
   ┌────┴────┬──────────┬──────────┐
 [[RTMP]]    [[SRT]]/WebRTC   S3 upload   API pull
   │        │              │           │
   └────────┴──────────────┴───────────┘
                    │
            Ingest tier (auth, validate)
                    │
         Buffer / queue ──► [[transcoding]] / packager
```

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

- Validate stream key → tenant → channel ID before accepting.

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

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| OBS "Failed to connect" | DNS, 1935 blocked, bad key | Security group; rotate key; TLS RTMPS if required |
| Connect then immediate drop | Auth callback timeout | Scale auth service; fail-open only if contract allows |
| Frozen picture, audio OK | Publisher stopped sending video | OBS scene empty; encoder crash |
| All channels down | Shared ingest node | Bulkhead; multi-AZ ingest pool |
| VoD stuck QUEUED | Worker backlog | Scale transcode ASG; priority queue |
| A/V sync at ingest | Wrong `-itsoffset` upstream | Fix publisher; don't patch in packager only |
| High latency from day one | Too many sync transcode hops | `-c copy` to packager when possible |

- **Mistake:** **Ingest auth in player**
- **Mistake:** **RTMP buffer bloat**
- **Mistake:** **Same stream key reuse**
- **Mistake:** **Probe untrusted uploads**
- **Mistake:** **Geo-locked partners**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Client-direct to CDN**
- **Con / skip when:** **Heavy ML on ingest thread**
- **Con / skip when:** **Synchronous full transcode before ACK**

## Comparison
- vs [[Microservice]]: **Synchronous full transcode before ACK**


### Use cases
- Used wherever Ingestion sits in an ingest → package → CDN → player path
