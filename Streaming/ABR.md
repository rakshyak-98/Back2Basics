[[Streaming]] [[HLS]] [[DASH]] [[rendition]] [[bitrate streaming]] [[Manifest (streaming)]] [[HLS vs. DASH]] [[CMAF]] [[transcoding]] [[NVENC]]

# ABR (Adaptive Bit Rate)

> ABR picks a lower or higher quality mid-play — match the viewer's bandwidth so playback stays smooth.

```txt
        ABR (Adaptive Bit  ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you can walk ABR end-to-end

## Sources
- [Wikipedia — ABR](https://en.wikipedia.org/wiki/ABR) — overview
- [Apple HLS — content steering / ABR practices](https://developer.apple.com/documentation/http-live-streaming) — overview

## Key Concepts
- **Ladder:** Set of quality rungs
- **Rendition:** One rung’s encode — “Each rendition is its own resolution and bitrate.”
- **Manifest:** Menu of rungs + segments
- **GOP aligned:** Same keyframe times across rungs
- **BANDWIDTH:** Declared peak need for a rung
- **BOLA / buffer logic:** Algorithm that picks the next rung

**Flow:**

- **Note:** 1. **Encode** — build aligned [[rendition]]s ([[bitrate streaming]] ladder).
- **Note:** 2. **Publish** — advertise them in the [[Manifest (streaming)]].
- **Note:** 3. **Measure** — player estimates download speed and buffer fill.
- **Note:** 4. **Switch**


- **Core:** ABR is a **client** decision. The origin only offers choices

## Technical Details
```txt
Source
  │
  ├─ encode ladder ──► 1080p / 720p / 480p / …  ([[rendition]] each)
  │
  ├─ list in manifest  ([[HLS]] .m3u8 or [[DASH]] .mpd)
  │
  └─ player picks rung ──► throughput + buffer health ──► switch at keyframe
```

### HLS master (what ABR reads)

```plaintext
#EXTM3U
#EXT-X-STREAM-INF:BANDWIDTH=8000000,RESOLUTION=1920x1080
chunklist_1080p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720
chunklist_720p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=1500000,RESOLUTION=854x480
chunklist_480p.m3u8
```

### ffmpeg — aligned ladder (VoD sketch)

```bash
# Fixed GOP so rungs share switch points (-sc_threshold 0)
ffmpeg -i in.mp4 -c:v libx264 -b:v 3000k -maxrate 3000k -bufsize 6000k \
  -g 60 -keyint_min 60 -sc_threshold 0 -c:a aac -b:a 128k \
  -f hls -hls_time 2 -hls_playlist_type vod out_720.m3u8
```

| Knob | Why it matters |
|------|----------------|
| Shared GOP / segment duration | Clean switches; no flash to next IDR |
| `BANDWIDTH` = video + audio + mux | Player under/over-selects if wrong |
| ~1.5–2× steps between rungs | Avoid quality cliffs |
| CDN caches **all** rungs | Cold rung = stall on first upswitch |
| Multi-CDN push | Same ladder to each origin — see replication below |

### Multi-ingest (same live to two CDNs)

```bash
ffmpeg -i <source> -c copy -f flv rtmp://cdn1/live/key \
  -c copy -f flv rtmp://cdn2/live/key
```

- Debug: player stats (Shaka `getStats()`, hls.js `bandwidthEstimate`) + CDN 20…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Endless buffer / never starts | Lowest rung still too fat | Add a 240–360p emergency rung |
| Stuck on lowest quality | Inflated `BANDWIDTH` or bad estimate | Recalculate manifest; check CDN slow-start |
| Never reaches top rung | Cap too high vs real peak | Lower declared `BANDWIDTH`; fix TCP/CDN |
| Flash / block on switch | Misaligned GOP across rungs | Re-encode fixed `-g` / `-sc_threshold 0` |
| Oscillates up/down | Huge rung gaps or short buffer | Insert mid rung; tune player buffer target |
| One CDN good, other bad | Partial ladder on second origin | Push full ladder; verify all playlists |
| A/V jump at switch | Audio not shared / wrong group | Separate audio group or align audio segments |

- **Mistake:** **ABR ≠ encoding**
- **Unaligned keyframes** — switch mid-GOP::** → glitch until the next IDR. Align or fail interviews on “seamless ABR”
- **Mistake:** **CDN only cached the default rung**
- **Mistake:** **Encode cost scales with N**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Single fixed bitrate contract**
- **Con / skip when:** **Sub-second interactive**
- **Con / skip when:** **Mezzanine archive only**

## Comparison
- vs [[WebRTC]]: **Sub-second interactive**


### Use cases
- ABR is a **client** decision. The origin only offers choices

- Used wherever ABR sits in an ingest → package → CDN → player path
