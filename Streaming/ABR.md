[[Streaming]] [[HLS]] [[DASH]] [[rendition]] [[bitrate streaming]] [[Manifest (streaming)]]

# ABR (Adaptive Bit Rate)

> ABR picks a lower or higher quality mid-play — match the viewer's bandwidth so playback stays smooth.

---

## Mental model

**Say it in one breath:** Encode one show as a ladder of qualities; the player watches buffer and speed, then switches rungs without stopping.

```txt
Source
  │
  ├─ encode ladder ──► 1080p / 720p / 480p / …  ([[rendition]] each)
  │
  ├─ list in manifest  ([[HLS]] .m3u8 or [[DASH]] .mpd)
  │
  └─ player picks rung ──► throughput + buffer health ──► switch at keyframe
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Ladder** | Set of quality rungs | “We ship several bitrates; ABR climbs or drops the ladder.” |
| **Rendition** | One rung’s encode | “Each rendition is its own resolution and bitrate.” |
| **Manifest** | Menu of rungs + segments | “The player reads the manifest, then fetches segments.” |
| **GOP aligned** | Same keyframe times across rungs | “Switches only at shared keyframes so it stays clean.” |
| **BANDWIDTH** | Declared peak need for a rung | “Wrong BANDWIDTH makes the player pick the wrong rung.” |
| **BOLA / buffer logic** | Algorithm that picks the next rung | “The client algorithm owns the switch — not the CDN.” |

### How the story goes (4 steps)

1. **Encode** — build aligned [[rendition]]s ([[bitrate streaming]] ladder).
2. **Publish** — advertise them in the [[Manifest (streaming)]].
3. **Measure** — player estimates download speed and buffer fill.
4. **Switch** — next segment from a higher or lower rung at a keyframe boundary.

> [!INFO]
> ABR is a **client** decision. The origin only offers choices; the player chooses which segment to GET next.

---

## Standard config / commands

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

Debug: player stats (Shaka `getStats()`, hls.js `bandwidthEstimate`) + CDN 206/404 on the rung you expect.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Endless buffer / never starts | Lowest rung still too fat | Add a 240–360p emergency rung |
| Stuck on lowest quality | Inflated `BANDWIDTH` or bad estimate | Recalculate manifest; check CDN slow-start |
| Never reaches top rung | Cap too high vs real peak | Lower declared `BANDWIDTH`; fix TCP/CDN |
| Flash / block on switch | Misaligned GOP across rungs | Re-encode fixed `-g` / `-sc_threshold 0` |
| Oscillates up/down | Huge rung gaps or short buffer | Insert mid rung; tune player buffer target |
| One CDN good, other bad | Partial ladder on second origin | Push full ladder; verify all playlists |
| A/V jump at switch | Audio not shared / wrong group | Separate audio group or align audio segments |

---

## Gotchas

> [!WARNING]
> **ABR ≠ encoding** — encoding builds the ladder; ABR is the player picking rungs at runtime.

> [!WARNING]
> **Unaligned keyframes** — switch mid-GOP → glitch until the next IDR. Align or fail interviews on “seamless ABR”.

> [!WARNING]
> **CDN only cached the default rung** — first upswitch cold-misses and looks like “ABR is broken”.

> [!WARNING]
> **Encode cost scales with N** — N channels × M renditions = M× encode sessions ([[NVENC]] / GPU math).

---

## When NOT to use

- **Single fixed bitrate contract** — one CBR pipe; no ladder (broadcast feed).
- **Sub-second interactive** — use [[WebRTC]] / [[ICE (Interactive Connectivity Establishment)]]; segment ABR adds seconds.
- **Mezzanine archive only** — store one high master; ladder at package time, not at archive.

---

## Related

[[Streaming]] [[HLS]] [[DASH]] [[HLS vs. DASH]] [[rendition]] [[bitrate streaming]] [[Manifest (streaming)]] [[CMAF]] [[transcoding]] [[NVENC]]
