[[ingestion]] [[HLS]] [[DASH]] [[ABR]] [[WebRTC]] [[RTMP]] [[SRT]] [[RTSP]] [[Encoding]] [[transcoding]] [[rendition]] [[bitrate streaming]] [[HLS vs. DASH]] [[CMAF]]

# Streaming

> Streaming moves live or file video from ingest to the viewer — package, protect, and play over the network.

## Interview Relevance

Interviewers probe whether you can walk Streaming end-to-end — not just name it. Signal fluency with **Ingest**, **ABR**, **Manifest**, **Rendition** and when you would pick a different path.

## Sources

- [Wikipedia — Streaming](https://en.wikipedia.org/wiki/Streaming) — overview

## Key Concepts

- **Ingest:** Accept publisher input — “Ingest is the front door — auth and backpressure first.”
- **ABR:** Switch quality mid-play — “ABR matches bitrate to the viewer’s network.”
- **Manifest:** Segment menu (`.m3u8` / `.mpd`) — “The player reads the manifest, then pulls segments.”
- **Rendition:** One quality encode — “Each rendition is a rung on the ladder.”
- **Mux:** Combine A/V into a container — “We mux H.264 + AAC into fMP4 or MPEG-TS.”
- **Glass-to-glass:** Camera to display delay — “OTT HLS is seconds; WebRTC aims for sub-second.”
- **Stage:** Job — Notes
- **Ingestion:** Accept live or file — [[ingestion]] — fail here = channel dark
- **Encode / ladder:** Make [[rendition]]s — Cost × N rungs ([[bitrate streaming]])
- **Package:** Manifests + segments — [[HLS]] / [[DASH]] / [[Manifest (streaming)]]
- **Protect:** Encrypt + license — [[DRM]] — not the same as “broadcast”
- **Distribute:** CDN or peer path — HTTP cache vs [[ICE (Interactive Connectivity Establishment)]]
- **Playback:** Decode + present — Player owns ABR decisions

### Pipeline pieces (one job each)

| Stage | Job | Notes |
|-------|-----|-------|
| **Ingestion** | Accept live or file | [[ingestion]] — fail here = channel dark |
| **Encode / ladder** | Make [[rendition]]s | Cost × N rungs ([[bitrate streaming]]) |
| **Package** | Manifests + segments | [[HLS]] / [[DASH]] / [[Manifest (streaming)]] |
| **Protect** | Encrypt + license | [[DRM]] — not the same as “broadcast” |
| **Distribute** | CDN or peer path | HTTP cache vs [[ICE (Interactive Connectivity Establishment)]] |
| **Playback** | Decode + present | Player owns ABR decisions |

### Muxing (say it clean)

Video and audio encode apart; a **muxer** interleaves them with timestamps (PTS/DTS) into one container. The player **demuxes** to decode. Common containers: [[MPEG-TS]] (live/broadcast), MP4/fMP4 (HLS/DASH), FLV ([[RTMP]] ingest).

## Technical Details

```txt
Publisher (OBS / encoder / file)
        │  [[ingestion]]  ([[RTMP]] / [[SRT]] / [[RTSP]] / upload)
        ▼
   Encode / transcode  ([[Encoding]] [[transcoding]] [[rendition]])
        │
        ├─ OTT path: [[ABR]] ladder → [[HLS]] / [[DASH]] + [[CMAF]] → CDN → player
        │
        └─ Realtime path: [[WebRTC]] + [[ICE (Interactive Connectivity Establishment)]] → few peers
        │
   Protect: [[DRM]] / [[EME]]   Play: manifest GETs or RTP
```

### Local loop — UDP in, HLS out (lab)

```bash
# Publish a file as if live
ffmpeg -re -i sample.mp4 -c copy -f mpegts udp://127.0.0.1:5000

# Loop forever
ffmpeg -stream_loop -1 -re -i sample.mp4 -c copy -f mpegts udp://127.0.0.1:5000

# Player against a packaged HLS URL (origin-dependent)
ffplay http://localhost/stream1/index.m3u8
```

### Mux elementary streams to MP4

```bash
ffmpeg -i video.h264 -i audio.aac -c copy -f mp4 output.mp4
```

### Ingest sketch (RTMP)

```bash
ffmpeg -re -i sample.mp4 -c copy -f flv rtmp://localhost/live/stream1
```

| Knob | Why it matters |
|------|----------------|
| `-re` | Realtime pace — avoid dumping VoD at encode speed into “live” |
| Segment duration 2–6 s | Startup vs latency vs object count |
| Dual [[HLS]]+[[DASH]] via [[CMAF]] | One store, Apple + Android |
| Short TTL on live manifests | Stale playlist = frozen edge |
| WebRTC vs HLS choice | Audience size + latency SLA |

Debug: `ffprobe` the playlist/segments; CDN logs for 404/403; `chrome://media-internals` / WebRTC internals for realtime.

### Where to go next

| Symptom / need | Go to |
|----------------|-------|
| … | [[…]] |

### Related topics in this domain

- …: [[…]]

## Real-World Applications

Used wherever Streaming sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Download-and-watch file delivery** — progressive MP4 / HLS VoD still “streams,” but don’t invent live packaging for a file drop.
- **Con / skip when:** **Massive one-to-many on WebRTC mesh** — use [[HLS]] / [[DASH]] + CDN; ICE is for few peers.
- **Con / skip when:** **Treating the hub as a runbook** — jump to the child note ([[ABR]], [[ingestion]], …) for deep triage.

## Comparison

- vs [[HLS]]: **Massive one-to-many on WebRTC mesh** — use [[HLS]] / [[DASH]] + CDN; ICE is for few peers.
- vs [[ABR]]: **Treating the hub as a runbook** — jump to the child note ([[ABR]], [[ingestion]], …) for deep triage.

## Mistakes to Avoid

| Symptom | Check | Fix |
|---------|-------|-----|
| No viewers, publisher “connected” | Ingest OK, package/CDN path | Trace origin playlist; CDN purge/TTL |
| Buffering on good Wi‑Fi | Ladder too fat; ABR stuck | Add lower [[rendition]]; fix `BANDWIDTH` |
| iOS fails, Android OK | DASH-only egress | Add [[HLS]] or CMAF dual |
| Live stuck on old edge | Cached manifest | `Cache-Control` short; see [[Manifest (streaming)]] |
| A/V desync | Mux timestamps / drift | Remux; align audio rendition |
| DRM black screen | License / PSSH / EME | [[DRM]] [[EME]] triage |
| Works via proxy once, then breaks | Absolute URLs in manifest | [[streaming manifest file]] rewrite |
| Call connects, media silence | ICE/TURN | [[ICE (Interactive Connectivity Establishment)]] |

- **Broadcast ≠ DRM** — broadcasting copies one stream to many; DRM **restricts** who can decrypt. Don’t conflate in design reviews.
- **Ingest protocol ≠ egress protocol** — [[RTMP]] in, [[HLS]] out is normal; browsers don’t play RTMP anymore.
- **Encode cost is channels × renditions** — GPU math fails when you count channels only.
- **“Streaming” without a latency number** — OTT ABR and WebRTC are different products; pick the SLA first.
