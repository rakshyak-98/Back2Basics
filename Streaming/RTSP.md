[[ingestion]] [[Streaming]] [[MPEG-TS]] [[SDP (Session Description Protocol)]] [[HLS]] [[IPTV]] [[RTMP]] [[SRT]] [[flussonic]] [[ffprobe]]

# RTSP (Real Time Streaming Protocol)

> RTSP is a control protocol for on-demand and live media — clients send PLAY/PAUSE over TCP, then receive RTP packets (usually UDP) carrying the actual A/V.





## Interview Relevance
Interviewers probe whether you can walk RTSP end-to-end — not just name it. Signal fluency with **RTSP**, **RTP**, **SDP**, **Interleaved** and when you would pick a different path.

## Sources
- [Wikipedia — RTSP](https://en.wikipedia.org/wiki/RTSP) — overview
- [RFC 7826 — RTSP 2.0](https://datatracker.ietf.org/doc/html/rfc7826) — deep-dive

## Key Concepts
- **RTSP:** Session control (RFC 2326 / 7826) — “RTSP negotiates the session; it doesn’t carry all the media bytes.”
- **RTP:** Real-time transport of encoded frames — “After PLAY, media flows as RTP payloads.”
- **SDP:** Session description (codecs, ports) — “DESCRIBE returns SDP — same family as WebRTC, different use.”
- **Interleaved:** RTP inside the RTSP TCP socket — “When UDP is blocked, RTP rides on the RTSP connection.”
- **ANNOUNCE / RECORD:** Publisher pushes to server — “Less common than pull PLAY; some encoders publish this way.”
- **554:** Default RTSP port — “Cameras and NVRs listen here unless remapped.”
- **Protocol:** Transport — Typical role
- **RTSP:** TCP control + RTP/UDP media — IP cameras, NVR, surveillance, some IPTV headends
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

Run as a supervised service — cameras drop idle RTSP sessions; reconnect logic belongs in the bridge.

### Publish RTSP (ffmpeg RTSP server pattern)

```bash
# Listener example (lab) — requires ffmpeg with RTSP mux support / mediamtx / GStreamer
ffmpeg -re -i sample.mp4 -c copy -f rtsp rtsp://127.0.0.1:8554/live/stream
```

Production publish paths usually use **MediaMTX**, **GStreamer RTSP server**, or vendor NVR — not raw ffmpeg alone.

### ONVIF / camera discovery (ops)

```txt
rtsp://<ip>:554/Streaming/Channels/101   # Hikvision main stream (vendor-specific)
rtsp://<ip>:554/cam/realmonitor?channel=1&subtype=0   # Dahua pattern
```

Vendor URL paths differ — check camera docs; credentials often required on first DESCRIBE.

### Health checks

```bash
nc -zv camera.example.com 554
timeout 10 ffprobe -rtsp_transport tcp -v error \
  "rtsp://camera.example.com/stream"
```

## Real-World Applications
Used wherever RTSP sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Browser-first live to thousands** — package [[HLS]] / [[DASH]] behind a CDN; RTSP doesn’t scale as viewer egress.
- **Con / skip when:** **Encoder → cloud ingest from home uplink** — prefer [[SRT]] or [[RTMP]] with ARQ/TCP semantics tuned for contribution.
- **Con / skip when:** **Sub-second interactive** — [[WebRTC]] / WHIP, not RTSP pull + transcode.
- **Con / skip when:** **Untrusted WAN without TLS** — RTSP/RTP are often cleartext; VPN or RTSP-over-TLS gateway for remote access.

## Comparison
- vs [[HLS]]: **Browser-first live to thousands** — package [[HLS]] / [[DASH]] behind a CDN; RTSP doesn’t scale as viewer egress.
- vs [[SRT]]: **Encoder → cloud ingest from home uplink** — prefer [[SRT]] or [[RTMP]] with ARQ/TCP semantics tuned for contribution.
- vs [[WebRTC]]: **Sub-second interactive** — [[WebRTC]] / WHIP, not RTSP pull + transcode.

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

- **RTSP URL ≠ browser URL** — players need HTTP manifests or WebRTC; never expose raw camera RTSP to the public internet without auth and TLS termination.
- **UDP RTP through NAT** — SETUP negotiates client ports; asymmetric NAT breaks unless TCP interleave or a reflector is used.
- **SDP in DESCRIBE is not WebRTC SDP** — same acronym family ([[SDP (Session Description Protocol)]]) but different signaling stack; don’t paste camera SDP into `RTCPeerConnection`.
- **Main vs sub stream** — `/101` vs `/102` style paths: main is high bitrate; sub is for mobile preview — pick intentionally for relay cost.
- **Clock skew** — RTP timestamps come from the device; long runs may drift vs wall clock; remux/transcode bridges should not assume NTP on cheap cameras.
