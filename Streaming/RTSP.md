[[ingestion]] [[Streaming]] [[MPEG-TS]] [[SDP (Session Description Protocol)]] [[HLS]] [[IPTV]] [[RTMP]] [[SRT]] [[flussonic]] [[ffprobe]]

# RTSP (Real Time Streaming Protocol)

> RTSP is a control protocol for on-demand and live media — clients send PLAY/PAUSE over TCP, then receive RTP packets (usually UDP) carrying the actual A/V.

```txt
        RTSP (Real Time St ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk RTSP end-to-end

## Sources
- [Wikipedia — RTSP](https://en.wikipedia.org/wiki/RTSP) — overview
- [RFC 7826 — RTSP 2.0](https://datatracker.ietf.org/doc/html/rfc7826) — deep-dive

## Key Concepts
- **RTSP:** Session control (RFC 2326 / 7826)
- **RTP:** Real-time transport of encoded frames
- **SDP:** Session description (codecs, ports)
- **Interleaved:** RTP inside the RTSP TCP socket
- **ANNOUNCE / RECORD:** Publisher pushes to server
- **554:** Default RTSP port — “Cameras and NVRs listen here unless remapped.”
- **Protocol:** Transport — Typical role
- **RTSP:** TCP control + RTP/UDP media
- **[[RTMP]]:** Single TCP (FLV mux) — Encoder → origin ingest
- **[[SRT]]:** UDP + ARQ + encryption — Contribution over lossy WAN
- **[[HLS]]:** HTTP segments — CDN → players

### RTSP vs ingest protocols (pick the right tool)

| Protocol | Transport | Typical role | Browser playback |
|----------|-----------|--------------|------------------|
| **RTSP** | TCP control + RTP/UDP media | IP cameras, NVR, surveillance, some IPTV headends | No — transcode to [[HLS]] / WebRTC |
| **[[RTMP]]** | Single TCP (FLV mux) | Encoder → origin ingest | No — ingest only |
| **[[SRT]]** | UDP + ARQ + encryption | Contribution over lossy WAN | No — ingest / relay |
| **[[HLS]]** | HTTP segments | CDN → players | Yes |

## Technical Details
```txt
Client (VLC, ffmpeg, NVR)          Media server / IP camera
        │── DESCRIBE rtsp://… ────────►│  (SDP: codecs, tracks)
        │◄── 200 OK + SDP ─────────────│
        │── SETUP track=video ─────────►│  (assign RTP ports / interleave)
        │── SETUP track=audio ─────────►│
        │── PLAY ──────────────────────►│
        │◄════════ RTP/UDP (or TCP) ════│  H.264 / H.265 / AAC …
        │── PAUSE / TEARDOWN ──────────►│
```

### Pull RTSP → record or relay

```bash
# UDP RTP (default on many cameras) — add -rtsp_transport tcp if UDP blocked
ffmpeg -rtsp_transport tcp -i "rtsp://user:pass@192.168.1.50:554/stream1" \
  -c copy -f mpegts camera.ts

# Low-latency preview (no write)
ffplay -rtsp_transport tcp "rtsp://192.168.1.50/live/ch0"

# Probe tracks and codecs
ffprobe -rtsp_transport tcp -v error -show_streams \
  "rtsp://192.168.1.50:554/h264"
```

| Knob | Why |
|------|-----|
| `-rtsp_transport tcp` | Firewall-friendly; avoids UDP loss on Wi‑Fi |
| `-rtsp_transport udp` | Lower overhead when LAN is clean |
| `-stimeout 5000000` | Microseconds — fail fast on dead camera (ffmpeg) |
| `-c copy` | No re-encode if downstream accepts codec |
| TCP interleave | Camera forces RTP on RTSP socket — use `tcp` |

### RTSP → HLS bridge (camera to browser)

```bash
ffmpeg -rtsp_transport tcp -i "rtsp://cam/live" \
  -c:v libx264 -preset veryfast -g 60 -sc_threshold 0 \
  -c:a aac -ar 48000 \
  -f hls -hls_time 4 -hls_list_size 6 -hls_flags delete_segments \
  /var/www/hls/cam/index.m3u8
```

- Run as a supervised service

### Publish RTSP (ffmpeg RTSP server pattern)

```bash
# Listener example (lab) — requires ffmpeg with RTSP mux support / mediamtx / GStreamer
ffmpeg -re -i sample.mp4 -c copy -f rtsp rtsp://127.0.0.1:8554/live/stream
```

- Production publish paths usually use **MediaMTX**, **GStreamer RTSP server**,…

### ONVIF / camera discovery (ops)

```txt
rtsp://<ip>:554/Streaming/Channels/101   # Hikvision main stream (vendor-specific)
rtsp://<ip>:554/cam/realmonitor?channel=1&subtype=0   # Dahua pattern
```

- Vendor URL paths differ

### Health checks

```bash
nc -zv camera.example.com 554
timeout 10 ffprobe -rtsp_transport tcp -v error \
  "rtsp://camera.example.com/stream"
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Connection refused | `nc -zv host 554` | Wrong port; camera RTSP disabled |
| 401 Unauthorized | Credentials in URL | `rtsp://user:pass@host/...`; digest auth on some NVRs |
| Connect OK, black video | UDP RTP blocked | Switch `-rtsp_transport tcp` |
| Stutter / macroblocking | Wi‑Fi UDP loss | TCP transport or relay via [[SRT]]/origin |
| Works in VLC, fails ffmpeg | Substream codec (HEVC) | Transcode or pick H.264 substream |
| Drops after ~60 s idle | Camera session timeout | Keepalive PLAY or bridge with auto-reconnect |
| High latency (30 s+) | Camera buffer + TCP | Substream; lower GOP; don’t stack HLS on top for “live” SLA |
| Multiple clients, one fails | Camera max sessions | Aggregate with one pull → fan-out ([[HLS]]) |

- **Mistake:** **RTSP URL ≠ browser URL**
- **Mistake:** **UDP RTP through NAT**
- **Mistake:** **SDP in DESCRIBE is not WebRTC SDP**
- **Mistake:** **Main vs sub stream**
- **Mistake:** **Clock skew**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Browser-first live to thousands**
- **Con / skip when:** **Encoder → cloud ingest from home uplink**
- **Con / skip when:** **Sub-second interactive**
- **Con / skip when:** **Untrusted WAN without TLS**

## Comparison
- vs [[HLS]]: **Browser-first live to thousands**
- vs [[SRT]]: **Encoder → cloud ingest from home uplink**
- vs [[WebRTC]]: **Sub-second interactive** — [[WebRTC]] / WHIP, not RTSP pull + transcode.


### Use cases
- Used wherever RTSP sits in an ingest → package → CDN → player path
