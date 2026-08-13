<!-- note-strategy: operational -->
[[Streaming]] [[ABR]] [[DASH]] [[CMAF]] [[Manifest (streaming)]] [[MPEG-TS]]

# HLS (HTTP Live Streaming)

> HLS cuts video into short HTTP files and a playlist — the player fetches the next chunk over plain HTTPS.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#LL-HLS (low latency)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Package many qualities into segments, publish an `.m3u8` menu, let the CDN cache GETs — no special streaming socket to the viewer.

```txt
Ingest ([[RTMP]] / [[SRT]] / [[RTSP]] / file)
        │
   encode + package ──► segments (.ts or fMP4 .m4s)
        │
   master.m3u8 ──► media playlists ──► segment URLs
        │
   CDN / origin ──► player GETs over HTTP(S)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Master / multivariant** | Menu of quality playlists | “First download is the master; it lists renditions.” |
| **Media playlist** | Ordered list of segments for one rung | “The media playlist is the segment sequence.” |
| **Segment** | 2–10 s media file | “Playback is just sequential HTTP GETs.” |
| **TARGETDURATION** | Max segment length advertised | “Players size buffer from TARGETDURATION.” |
| **MEDIA-SEQUENCE** | Live sliding window index | “Live playlists drop old segments and bump the sequence.” |
| **fMP4 / CMAF** | Modern segment shape (not only TS) | “We prefer fMP4 so HLS and DASH share bytes.” |
| **LL-HLS** | Parts + blocking playlist | “Partials cut live delay from tens of seconds to a few.” |

### How the story goes (4 steps)

1. **Ingest** — publisher pushes [[RTMP]] / [[SRT]] / [[RTSP]] pull / file into the packager.
2. **Ladder** — encode [[ABR]] [[rendition]]s; segment on aligned GOPs.
3. **Manifest** — write master + media `.m3u8` ([[Manifest (streaming)]]).
4. **Deliver** — CDN serves HTTP; player adapts quality from buffer + bandwidth.

> [!INFO]
> HLS is **stateless file delivery**. That is why it survives firewalls and scales on any CDN — and why classic live latency is tens of seconds unless you use LL-HLS.

---

## Standard config / commands

### Master playlist

```plaintext
#EXTM3U
#EXT-X-VERSION:7
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
1080p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
720p/index.m3u8
```

### Live media playlist

```plaintext
#EXTM3U
#EXT-X-VERSION:7
#EXT-X-TARGETDURATION:6
#EXT-X-MEDIA-SEQUENCE:104
#EXTINF:6.000,
segment_104.m4s
#EXTINF:6.000,
segment_105.m4s
```

### Package with ffmpeg (fMP4 HLS)

```bash
ffmpeg -i in.mp4 -c:v libx264 -c:a aac -g 60 -sc_threshold 0 \
  -f hls -hls_time 4 -hls_segment_type fmp4 \
  -hls_fmp4_init_filename init.mp4 -master_pl_name master.m3u8 stream.m3u8
```

| Knob | Why it matters |
|------|----------------|
| Segment 2–6 s | Startup vs live latency vs CDN object count |
| fMP4 + [[CMAF]] | Share segments with [[DASH]]; skip duplicate TS store |
| `Cache-Control` short on live playlists | Stale playlist = stuck live edge |
| `#EXT-X-KEY` / SAMPLE-AES | Encryption; pair with [[DRM]] / FairPlay for premium |
| Signed URL / cookie on CDN | Stop hotlink of `.m3u8` and `.m4s` |

Debug: `curl` the master → follow a media playlist → HEAD a segment; Apple `mediastreamvalidator` on macOS.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen / won’t start | Master 404, bad `CODECS`, CORS | Fix origin path; align ffprobe vs playlist |
| Live stuck / freeze at edge | CDN caching playlist; old `MEDIA-SEQUENCE` | `max-age=0` on live `.m3u8`; fix packager sequence |
| Works Safari, fails Chrome | TS-only or FairPlay-only path | Dual package; Widevine for non-Apple ([[DRM]]) |
| High live latency | Full-segment only | LL-HLS parts or shorter segments |
| 403 on segments, playlist OK | Token not on child URLs | Relative URLs + signed cookie |
| ABR never ups | Wrong `BANDWIDTH` | Recalculate; see [[ABR]] |
| Decrypt fail | `#EXT-X-KEY` URI / DRM license | Fix key host; check [[EME]] |

---

## LL-HLS (low latency)

Classic HLS buffers several full segments → **~15–30 s** delay. LL-HLS aims for **~2–5 s**:

| Extension | Job |
|-----------|-----|
| **`EXT-X-PART`** | Serve ~200 ms partials before the full segment exists |
| **Blocking playlist reload** | Hold GET until the next part/segment is ready |
| **`EXT-X-PRELOAD-HINT`** | Tell the player what to request next early |
| **`EXT-X-RENDITION-REPORT`** | Sync sequence across rungs for faster ABR |

Needs CMAF-style chunks and a player that understands LL tags.

---

## Gotchas

> [!WARNING]
> **HLS is not a push protocol to the viewer** — the player pulls. Origin must keep playlists fresh for live.

> [!WARNING]
> **Packager restart resets `MEDIA-SEQUENCE`** — players hang; use discontinuity or coordinated restart.

> [!WARNING]
> **Absolute segment URLs behind a proxy** — player bypasses your app origin; rewrite manifests ([[streaming manifest file]]).

> [!WARNING]
> **LL tags on non-LL players** — gate features; don’t break legacy clients with unknown tags they mishandle.

---

## When NOT to use

- **Browser mesh / sub-second call** — [[WebRTC]] + [[ICE (Interactive Connectivity Establishment)]].
- **Publisher → ingest only** — [[RTMP]] / [[SRT]] / [[RTSP]] into origin; HLS is usually the **egress** format.
- **Apple-free Android-only shop that already standardized on DASH** — ship [[DASH]] (or dual via [[CMAF]]).

---

## Related

[[Streaming]] [[ABR]] [[DASH]] [[HLS vs. DASH]] [[CMAF]] [[Manifest (streaming)]] [[MPEG-TS]] [[DRM]] [[RTMP]] [[rendition]]
