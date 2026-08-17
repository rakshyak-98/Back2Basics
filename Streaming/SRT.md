[[ingestion]] [[Streaming]] [[MPEG-TS]] [[RTMP]] [[Encoding]] [[network management]] [[HLS]] [[flussonic]] [[OBS]] [[Multi Stream]] [[RTSP]]

# SRT (Secure Reliable Transport)

> SRT carries MPEG-TS (or other payloads) over UDP with encryption, configurable latency buffer, and packet retransmission — built for contribution across lossy networks.





## Interview Relevance
Interviewers probe whether you can walk SRT end-to-end — not just name it. Signal fluency with **SRT**, **Latency (rcvbuf)**, **ARQ**, **Caller / Listener** and when you would pick a different path.

## Sources
- [Wikipedia — SRT](https://en.wikipedia.org/wiki/SRT) — overview
- [SRT Alliance](https://www.srtalliance.org/) — overview
- [SRT protocol technical overview](https://github.com/Haivision/srt) — deep-dive

## Key Concepts
- **SRT:** UDP + reliability + encryption — “Contribution protocol — not for browser playback.”
- **Latency (rcvbuf):** Buffer time for retransmits — “Higher latency absorbs more loss; lower = snappier but fragile.”
- **ARQ:** Automatic repeat request — “NACK lost packets inside the latency window.”
- **Caller / Listener:** Who dials whom — “Ingest is usually Listener; field encoder is Caller.”
- **Rendezvous:** Both sides connect to a broker IP — “NAT traversal when neither side has a public port.”
- **Stream ID:** Logical channel on one socket — “Multiplex tenants on one listener port.”
- **Passphrase:** PSK encryption — “Like a stream key — rotate and never log in cleartext.”
- **Protocol:** Wire — Loss handling
- **SRT:** UDP + ARQ — Retransmit inside buffer
- **[[RTMP]]:** TCP — Head-of-line blocking
- **RTSP:** TCP + RTP/UDP — None (UDP) or TCP stall
- **Raw UDP [[MPEG-TS]]:** UDP — None

### SRT vs [[RTMP]] vs RTSP (ingest choice)

| Protocol | Wire | Loss handling | Typical latency | Best for |
|----------|------|---------------|-----------------|----------|
| **SRT** | UDP + ARQ | Retransmit inside buffer | ~0.5–2 s (tuned) | Remote contribution, sports, bonded uplinks |
| **[[RTMP]]** | TCP | Head-of-line blocking | ~2–5 s to origin | OBS → origin (stable LAN) |
| **RTSP** | TCP + RTP/UDP | None (UDP) or TCP stall | Varies | Cameras, pull-based surveillance |
| Raw UDP [[MPEG-TS]] | UDP | None | Lowest on clean LAN | Studio multicast, IPTV headend |

## Technical Details
```txt
Encoder / partner                WAN (lossy)                Ingest / relay
     │── SRT (AES, ARQ) ───────────────────────────────────────►│
     │   Caller ─────────────────────────────► Listener          │
     │   or Rendezvous via public IP helper                      │
     │                                                           ▼
     │                                              [[MPEG-TS]] demux / [[RTMP]] / [[HLS]] packager
```

### Listener ingest (origin waits for encoder)

```bash
# ffmpeg: listen on UDP 9000, write TS copy
ffmpeg -i "srt://0.0.0.0:9000?mode=listener&latency=200000" \
  -c copy -f mpegts /var/spool/ingest/live.ts

# Bridge SRT → RTMP without re-encode (when codecs fit FLV)
ffmpeg -i "srt://0.0.0.0:9000?mode=listener&passphrase=SECRET&latency=200000" \
  -c copy -f flv "rtmp://127.0.0.1:1935/live/key"
```

### Caller publish (encoder dials ingest)

```bash
ffmpeg -re -i sample.ts -c copy \
  -f mpegts "srt://ingest.example.com:9000?mode=caller&latency=200000&passphrase=SECRET"
```

| URL param | Why |
|-----------|-----|
| `mode=listener` / `caller` / `rendezvous` | Who binds vs who connects |
| `latency=200000` | Microseconds (200 ms) receive buffer — raise on lossy links |
| `passphrase=` | AES encryption PSK |
| `streamid=#!::r=live/key,m=publish` | Haivision-style publish stream ID (tool-dependent) |
| `pbkeylen=16` | AES key length (16/24/32) |

### srt-live-transmit (srt-tools)

```bash
# UDP MPEG-TS → SRT caller (common field pattern)
srt-live-transmit udp://239.1.1.1:5000 \
  "srt://ingest.example.com:9000?mode=caller&latency=500000"

# SRT listener → local UDP for downstream packager
srt-live-transmit "srt://0.0.0.0:9000?mode=listener" udp://127.0.0.1:5000
```

### Probe and smoke test

```bash
# Port open (SRT is UDP)
nc -zuv ingest.example.com 9000

ffprobe -v error -show_streams \
  "srt://0.0.0.0:9000?mode=listener&latency=200000"
```

### Latency tuning (rule of thumb)

```txt
Clean LAN / fiber:     120–200 ms
Internet contribution: 500–2000 ms
Satellite / bad LTE:   2000–8000 ms
```

If `pkt loss` counters climb, **increase latency** before re-encoding.

## Real-World Applications
Used wherever SRT sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Mass audience delivery** — CDN HTTP ([[HLS]] / [[CMAF]]), not SRT fan-out.
- **Con / skip when:** **Clean studio multicast LAN** — raw UDP [[MPEG-TS]] or [[Multicast]] is simpler when loss is near zero.
- **Con / skip when:** **Browser publish without a gateway** — use WebRTC WHIP or [[RTMP]] from OBS; browsers don’t speak SRT natively.
- **Con / skip when:** **Ultra-low-latency interactive** — sub-300 ms peer media is [[WebRTC]] territory, not ARQ-buffered contribution.

## Comparison
- vs [[HLS]]: **Mass audience delivery** — CDN HTTP ([[HLS]] / [[CMAF]]), not SRT fan-out.
- vs [[MPEG-TS]]: **Clean studio multicast LAN** — raw UDP [[MPEG-TS]] or [[Multicast]] is simpler when loss is near zero.
- vs [[RTMP]]: **Browser publish without a gateway** — use WebRTC WHIP or [[RTMP]] from OBS; browsers don’t speak SRT natively.
- vs [[WebRTC]]: **Ultra-low-latency interactive** — sub-300 ms peer media is [[WebRTC]] territory, not ARQ-buffered contribution.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Connection timeout | UDP blocked; wrong mode | Security group UDP port; Caller→Listener direction |
| Auth / decrypt fail | Passphrase mismatch | Rotate PSK both sides; check `pbkeylen` |
| Connect then instant drop | Stream ID / publish vs play | Match `streamid` to ingest expectation |
| Video freezes, audio OK | Burst loss > latency budget | Raise `latency`; check uplink Mbps vs bitrate |
| High glass-to-glass delay | Latency set too high | Lower buffer if loss allows; don’t stack HLS on top |
| CPU high on “copy” | Hidden transcode | Confirm `-c copy`; payload is [[MPEG-TS]] not exotic ES |
| Works lab, fails prod | NAT / symmetric NAT | Rendezvous server or public Listener IP |
| RTMP bridge rejects | Codec in TS | Transcode to H.264+AAC for [[RTMP]] |

- **SRT is not a player protocol** — terminate at ingest and egress [[HLS]] / [[DASH]] / [[WebRTC]] to viewers.
- **Latency is not “free quality”** — too low on a lossy link causes constant ARQ and visible freezes; tune from measured loss, not defaults.
- **Caller/Listener reversed** — encoder must be Caller when origin is Listener; swapping is the #1 integration mistake.
- **Passphrase = secret** — same abuse model as [[RTMP]] stream keys; rate-limit and audit publish endpoints.
- **Don’t confuse with [[SCTP (Stream Control Transmission Protocol)]]** — SCTP is WebRTC DataChannel transport; SRT is broadcast contribution over UDP ([[SCTP (Stream Control Transmission Protocol)#Gotchas]]).
- **Firewall “open port” ≠ working SRT** — UDP must flow **both directions** for ARQ; stateful rules sometimes block return NACK path.
