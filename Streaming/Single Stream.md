[[Multi Stream]] [[ingestion]] [[RTMP]] [[OBS]] [[Encoding]] [[bitrate streaming]] [[HLS]]

# Single Stream

> One publisher → one ingest destination → one encoded bitrate path — **simplest live topology** before ABR and multi-CDN.

```txt
        Single Stream ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Single Stream to see if you understand the pipeline ro…

## Sources
- [Wikipedia — Single Stream](https://en.wikipedia.org/wiki/Single_Stream) — overview

## Key Concepts
- **Note:** **Single stream** means **one active encode pipeline** from source to **one i…

| Aspect | Single stream | When to expand |
|--------|---------------|----------------|
| **Uplink** | One bitrate budget | Need >1 destination without origin |
| **Ops** | Minimal | SLA events → redundant push |
| **Quality** | One rung to ingest | Players need ABR → server ladder |
| **Failure** | Single point | Backup ingest URL (failover encoder config) |

## Technical Details
```txt
Single-stream publish path
  Camera ──► OBS ──► one RTMP ──► ingest ──► (optional) ladder ──► [[HLS]]

Contrast [[Multi Stream]]:
  Multi-push: same encode → many RTMP URLs
  ABR: many encodes → one manifest
```

### OBS single publish (canonical)

```txt
Settings → Stream → one Custom RTMP URL + Stream Key
Settings → Output → one streaming encoder profile
No secondary URL unless deliberate [[Multi Stream]]
```

- See [[OBS]] for bitrate/GOP defaults.

### ffmpeg single publish

```bash
ffmpeg -re -i input.mp4 \
  -c:v libx264 -b:v 3500k -minrate 3500k -maxrate 3500k -bufsize 7000k \
  -g 60 -sc_threshold 0 -c:a aac -b:a 128k \
  -f flv rtmp://ingest.example.com/live/key
```

### Ingest accepts one publisher per key

```nginx
# nginx-rtmp: second publisher with same key kicks first
live on;
drop_idle_publisher 10s;
```

- Document behavior for operations — "single stream per key" policy.

### Downstream ABR from single ingest (server-side)

```txt
Publisher: single 1080p30 @ 5 Mbps RTMP
Origin: transcode → 1080/720/480 ladder → [[Manifest (streaming)]]
Publisher unchanged — ABR is not publisher [[Multi Stream]]
```

### Failover without multi-stream (cold standby)

```txt
Primary encoder active; secondary encoder configured but offline
Manual switch on primary failure — not simultaneous push
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| New publish kicks old | Same stream key | Unique keys per event; or intentional takeover |
| Quality OK ingest, bad playback | No server ladder | Enable transcode packager |
| Single viewer OK, scale fails | RTMP to players | Must use [[HLS]]/[[DASH]] for viewers |
| Bitrate wrong for network | Single rung too high | Lower OBS bitrate or 720p output |
| Duplicate events on key reuse | Stale CDN cache | New key per event; purge manifest |

- **Mistake:** **Single stream ≠ single bitrate to viewers**
- **Mistake:** **One RTMP to CDN "live" product**
- **Mistake:** **No redundancy**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Need simultaneous YouTube + private origin**
- **Con / skip when:** **Direct ABR from publisher**
- **Con / skip when:** **WebRTC fanout**

## Comparison
- vs [[Multi Stream]]: **Need simultaneous YouTube + private origin** — [[Multi Stream]] multi-push.
- vs [[WebRTC]]: **WebRTC fanout** — SFU architecture, not single RTMP ([[WebRTC]]).


### Use cases
- Used wherever Single Stream sits in an ingest → package → CDN → player path
