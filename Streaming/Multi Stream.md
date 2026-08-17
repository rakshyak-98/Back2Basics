[[Single Stream]] [[ingestion]] [[RTMP]] [[Multi Stream]] [[ABR]] [[bitrate streaming]] [[OBS]] [[Microservice]] [[CMAF]]

# Multi Stream

> Multiple renditions or simultaneous publish destinations from one source — **ABR ladders + multi-CDN push**, not "many viewers".

```txt
        Multi Stream ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Multi Stream to see if you understand the pipeline rol…

## Sources
- [Wikipedia — Multi Stream](https://en.wikipedia.org/wiki/Multi_Stream) — overview

## Key Concepts
- **Note:** **Multi-stream** covers two distinct patterns engineers conflate:

- **Note:** 1. **ABR multi-rendition**
- **Note:** 2. **Multi-destination ingest**

| Pattern | Scale driver | Failure mode |
|---------|--------------|--------------|
| **ABR ladder** | CDN storage, encode CPU/GPU | Wrong GOP alignment → rebuffer on switch |
| **Multi-push** | Uplink bandwidth × N | One bad destination stalls encoder |
| **Multi-audio/caption** | Manifest complexity | Wrong `#EXT-X-MEDIA` grouping |

## Technical Details
```txt
Pattern A — ABR (one publisher, many renditions)
  OBS/encoder ──► transcoder ──► 1080p + 720p + 480p ──► packager ──► [[HLS]]/[[DASH]]

Pattern B — Multi-push (one publisher, many destinations)
  OBS ──► primary RTMP + secondary RTMP + SRT backup
              │              │                │
           origin CDN      YouTube         DR site
```

### OBS multi-destination (primary + custom)

```txt
Settings → Stream → Service: Custom
Server: rtmp://origin.example.com/live
Stream Key: channel_a

Plus: Settings → Advanced → Enable secondary output (or plugin)
  rtmp://backup.example.com/live / channel_a
```

- Prefer **hardware encoder** ([[NVENC]]) when pushing 2+ destinations

### ffmpeg replicate (remux copy — no re-encode)

```bash
ffmpeg -i rtmp://source/live/key \
  -c copy -f flv rtmp://dest1/live/key \
  -c copy -f flv rtmp://dest2/live/key
```

- Uplink must sustain **bitrate × 1** (copy) not × encodes.

### ABR ladder from single ingest (transcode fan-out)

```bash
# Split into 720p + 480p rungs — see [[bitrate streaming]]
ffmpeg -i rtmp://localhost/live/in \
  -filter_complex "[0:v]split=2[v1][v2];[v1]scale=-2:720[out1];[v2]scale=-2:480[out2]" \
  -map "[out1]" -c:v libx264 -b:v 3000k -g 60 -f flv rtmp://localhost/live/720 \
  -map "[out2]" -c:v libx264 -b:v 1200k -g 60 -f flv rtmp://localhost/live/480
```

- Better at scale: dedicated transcoder service per [[Microservice]].

### Manifest advertises all renditions

```plaintext
# HLS master — each rung is separate media playlist
#EXT-X-STREAM-INF:BANDWIDTH=5932800,RESOLUTION=1920x1080,...
1080p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=3128000,RESOLUTION=1280x720,...
720p.m3u8
```

### Capacity planning

```txt
Uplink (multi-push copy):  source_bitrate × destinations + 20% overhead
Encode (ABR 4 rungs SW):     4× realtime CPU or 1× NVENC with parallel sessions
Origin storage:              sum(all rung bitrates) × duration
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| One CDN OK, other black | Single dest fail in multi-push | Independent reconnect per output; don't block on one |
| ABR switch artifacts | GOP misaligned across rungs | Fixed `-g`; `-sc_threshold 0` ([[CMAF]]) |
| Encoder CPU 100% | Too many simultaneous encodes | Drop rungs; [[NVENC]]; reduce destinations |
| YouTube OK, origin bad | Wrong key on one dest | Per-destination credentials |
| Duplicate segments on CDN | Two packagers same key | Unique stream keys per environment |
| Audio only on one rung | Map error in ffmpeg | `-map 0:a` on every output branch |

- **Mistake:** **Multi-push ≠ ABR**
- **Mistake:** **Single uplink saturation**
- **Mistake:** **OBS single encode multi-stream plugins**
- **Mistake:** **Different keyframe intervals per destination**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Single destination VoD**
- **Con / skip when:** **Player-side multi-stream**
- **Con / skip when:** **Ten destinations from one laptop**

## Real-World Applications
- **Scenario:** Used wherever Multi Stream sits in an ingest → package → CDN → player path
