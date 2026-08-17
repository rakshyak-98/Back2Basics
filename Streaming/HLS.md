[[Streaming]] [[ABR]] [[DASH]] [[CMAF]] [[Manifest (streaming)]] [[MPEG-TS]] [[HLS vs. DASH]] [[DRM]] [[RTMP]] [[rendition]]

# HLS (HTTP Live Streaming)

> HLS cuts video into short HTTP files and a playlist — the player fetches the next chunk over plain HTTPS.

```txt
        HLS (HTTP Live Str ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk HLS end-to-end

## Sources
- [Wikipedia — HLS](https://en.wikipedia.org/wiki/HLS) — overview
- [Apple HLS documentation](https://developer.apple.com/documentation/http-live-streaming) — deep-dive
- [RFC 8216 — HTTP Live Streaming](https://datatracker.ietf.org/doc/html/rfc8216) — deep-dive

## Key Concepts
- **Master / multivariant:** Menu of quality playlists
- **Media playlist:** Ordered list of segments for one rung
- **Segment:** 2–10 s media file — “Playback is just sequential HTTP GETs.”
- **TARGETDURATION:** Max segment length advertised — “Players size buffer from TARGETDURATION.”
- **MEDIA-SEQUENCE:** Live sliding window index
- **fMP4 / CMAF:** Modern segment shape (not only TS)
- **LL-HLS:** Parts + blocking playlist

**Flow:**

- **Note:** 1. **Ingest**
- **Note:** 2. **Ladder** — encode [[ABR]] [[rendition]]s; segment on aligned GOPs.
- **Note:** 3. **Manifest** — write master + media `.m3u8` ([[Manifest (streaming)]]).
- **Note:** 4. **Deliver**


- **Core:** HLS is **stateless file delivery**. That is why it survives firewalls and sca…

## Technical Details
```txt
Ingest ([[RTMP]] / [[SRT]] / [[RTSP]] / file)
        │
   encode + package ──► segments (.ts or fMP4 .m4s)
        │
   master.m3u8 ──► media playlists ──► segment URLs
        │
   CDN / origin ──► player GETs over HTTP(S)
```

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

- Debug: `curl` the master → follow a media playlist → HEAD a segment

### LL-HLS (low latency)

- Classic HLS buffers several full segments → **~15–30 s** delay.
- LL-HLS aims for **~2–5 s**:

| Extension | Job |
|-----------|-----|
| **`EXT-X-PART`** | Serve ~200 ms partials before the full segment exists |
| **Blocking playlist reload** | Hold GET until the next part/segment is ready |
| **`EXT-X-PRELOAD-HINT`** | Tell the player what to request next early |
| **`EXT-X-RENDITION-REPORT`** | Sync sequence across rungs for faster ABR |

- Needs CMAF-style chunks and a player that understands LL tags.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen / won’t start | Master 404, bad `CODECS`, CORS | Fix origin path; align ffprobe vs playlist |
| Live stuck / freeze at edge | CDN caching playlist; old `MEDIA-SEQUENCE` | `max-age=0` on live `.m3u8`; fix packager sequence |
| Works Safari, fails Chrome | TS-only or FairPlay-only path | Dual package; Widevine for non-Apple ([[DRM]]) |
| High live latency | Full-segment only | LL-HLS parts or shorter segments |
| 403 on segments, playlist OK | Token not on child URLs | Relative URLs + signed cookie |
| ABR never ups | Wrong `BANDWIDTH` | Recalculate; see [[ABR]] |
| Decrypt fail | `#EXT-X-KEY` URI / DRM license | Fix key host; check [[EME]] |

- **Mistake:** **HLS is not a push protocol to the viewer**
- **Mistake:** **Packager restart resets `MEDIA-SEQUENCE`**
- **Mistake:** **Absolute segment URLs behind a proxy**
- **Mistake:** **LL tags on non-LL players**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Browser mesh / sub-second call**
- **Con / skip when:** **Publisher → ingest only**
- **Con / skip when:** **Apple-free Android-only shop that already standardized…

## Comparison
- vs [[WebRTC]]: **Browser mesh / sub-second call**
- vs [[RTMP]]: **Publisher → ingest only**
- vs [[DASH]]: **Apple-free Android-only shop that already standardized on DASH**


### Use cases
- HLS is **stateless file delivery**. That is why it survives firewalls and sca…

- Used wherever HLS sits in an ingest → package → CDN → player path
