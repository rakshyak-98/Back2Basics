[[ingestion]] [[OBS]] [[Encoding]] [[Single Stream]] [[HLS]] [[network management]] [[Multi Stream]] [[SRT]] [[RTSP]] [[How to attach stream to HTTP handlers]]

# RTMP (Real-Time Messaging Protocol)

> RTMP (Real-Time Messaging Protocol) — OBS / ffmpeg ──RTMP/TCP──► Ingest (nginx-rtmp, MediaLive, etc.)





## Interview Relevance
Interviewers ask about RTMP to see if you understand the pipeline role, failure modes, and trade-offs — not just the acronym.

## Sources
- [Wikipedia — RTMP](https://en.wikipedia.org/wiki/RTMP) — overview
- [Adobe RTMP specification](https://rtmp.veriskope.com/docs/spec/) — deep-dive

## Key Concepts
**RTMP** maintains a **persistent TCP connection** from **encoder (publisher)** to **ingest server**, sending **FLV-muxed** H.264/AAC (typical). Low protocol overhead → **~2–5 s glass-to-glass** to origin before packaging. **Players no longer use RTMP** in browsers (Flash removed); CDNs terminate RTMP at ingest and deliver **HTTP segments** to viewers.

| Variant | Port | Notes |
|---------|------|-------|
| **RTMP** | 1935 | Cleartext — blocked on some networks |
| **RTMPS** | 443 (often) | TLS wrapper — prefer prod |
| **RTMPT** | 80 | Tunnel — legacy fallback |

**Publish** (one-to-one to origin) differs from **playback** (many-to-one HTTP) — don't expose RTMP URLs to end users.

## Technical Details
```txt
OBS / ffmpeg ──RTMP/TCP──► Ingest (nginx-rtmp, MediaLive, etc.)
                                │
                         transcode / package
                                │
                         [[HLS]] / [[DASH]] ──► CDN ──► players
```

### ffmpeg publish (smoke test)

```bash
ffmpeg -re -f lavfi -i testsrc=size=1280x720:rate=30 \
  -c:v libx264 -preset veryfast -b:v 2500k -minrate 2500k -maxrate 2500k -bufsize 5000k \
  -g 60 -keyint_min 60 -sc_threshold 0 \
  -c:a aac -b:a 128k -ar 48000 \
  -f flv "rtmp://ingest.example.com/live/STREAM_KEY"
```

| Knob | Why |
|------|-----|
| `-f flv` | RTMP carries FLV container |
| `-re` | Real-time pacing |
| CBR + GOP | Stable ingest ([[Encoding]]) |

### nginx-rtmp minimal ingest

```nginx
rtmp {
    server {
        listen 1935;
        chunk_size 4096;
        application live {
            live on;
            record off;
            on_publish http://127.0.0.1:8080/auth;
        }
    }
}
```

### Pull RTMP → push HLS (origin bridge)

```bash
ffmpeg -i rtmp://localhost/live/key -c copy \
  -f hls -hls_time 4 -hls_list_size 6 -hls_flags delete_segments \
  /var/www/hls/out.m3u8
```

Use when packager expects RTMP input only.

### Auth stream key pattern

```txt
rtmp://ingest.example.com/live/{tenant_id}_{channel_id}?sign=HMAC
on_publish validates HMAC + expiry before accepting
```

### Probe live RTMP

```bash
ffprobe -v error -show_streams rtmp://ingest/live/key
timeout 10 ffplay rtmp://ingest/live/key
```

## Real-World Applications
Used wherever RTMP sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Viewer delivery** — use [[HLS]]/[[DASH]]/[[CMAF]] via CDN.
- **Con / skip when:** **Sub-second interactive** — WebRTC/WHIP ([[WebRTC]]).
- **Con / skip when:** **Multi-tenant open ingest without authentication** — bot publish / abuse.

## Comparison
- vs [[HLS]]: **Viewer delivery** — use [[HLS]]/[[DASH]]/[[CMAF]] via CDN.
- vs [[WebRTC]]: **Sub-second interactive** — WebRTC/WHIP ([[WebRTC]]).

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | `nc -zv host 1935` | Security group; RTMPS on 443 |
| Auth failed | Ingest logs; on_publish HTTP | Key rotation; callback timeout |
| Connect then idle drop | `idle_streams` / firewall NAT | Publisher stopped; TCP keepalive |
| Audio, no video | OBS wrong encoder | H.264 Baseline/Main; not HEVC to old ingest |
| High latency end-to-end | RTMP OK but HLS 30s | Segment duration; not RTMP — see [[HLS]] |
| Buffer growth ingest | Publisher faster than real-time | Missing `-re`; CBR exceed |
| SSL handshake fail | RTMPS cert chain | Full chain; SNI match |

- **RTMP URL to viewers** — security risk + no browser support; always HTTP manifests outbound.
- **Single TCP head-of-line blocking** — bad Wi-Fi stalls entire stream; [[SRT]] may be better for lossy uplinks.
- **Stream key = password** — anyone with key can hijack channel.
- **HEVC over RTMP** — limited ingest support; confirm before enabling OBS HEVC.
- **Reconnect without discontinuity tag** — packager must emit `#EXT-X-DISCONTINUITY` on publisher reconnect.
