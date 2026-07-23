[[HLS]] [[DASH]] [[MPEG-TS]] [[CMAF]] [[codecs]] [[DRM]] [[Manifest (streaming)]]

# CMAF (Common Media Application Format)

> One fMP4 segment file for both HLS and DASH — **ISO/IEC 23000-19**; cuts origin storage ~50%.

---

## Mental model

**CMAF** standardizes **fragmented MP4 (fMP4)** chunks so **[[HLS]]** and **[[DASH]]** can share the **same `.m4s` media segments** — only the **manifests differ** (`.m3u8` vs `.mpd`). Each **CMAF chunk** is a `moof`+`mdat` pair; a **CMAF segment** is typically 2–6 seconds of chunks aligned on keyframes.

```txt
Encoder ──► fMP4 chunks (CMAF) ──► origin storage
                    │                    │
            ┌───────┴───────┐            │
         HLS manifest    DASH MPD       same .m4s URLs
         (.m3u8)          (.mpd)
            │                │
         Safari/iOS      Android/Chrome
```

| Concept | Meaning |
|---------|---------|
| **CMAF track** | Video or audio fMP4 track |
| **Chunk** | ~100–500 ms fragment (`moof`) — enables [[HLS]] LL-HLS partials |
| **Segment** | Manifest-addressable unit (multiple chunks or one) |
| **Presentation** | All renditions + manifests for one title |

Without CMAF, operators stored **duplicate TS for HLS + separate DASH segments** — double egress, double cache footprint.

---

## Standard config / commands

### ffmpeg — CMAF-style HLS (fMP4 segments)

```bash
ffmpeg -i input.mp4 -c:v libx264 -preset fast -crf 22 -g 60 -sc_threshold 0 \
  -c:a aac -b:a 128k \
  -f hls -hls_time 4 -hls_segment_type fmp4 -hls_fmp4_init_filename init.mp4 \
  -hls_playlist_type vod -master_pl_name master.m3u8 stream_%v.m3u8
```

| Flag | Why |
|------|-----|
| `-hls_segment_type fmp4` | CMAF-compatible segments (not MPEG-TS) |
| `-hls_fmp4_init_filename` | Separate init segment (`ftyp`+`moov`) — required for fMP4 |
| `-g 60` / aligned GOP | Clean ABR switches across renditions ([[ABR]]) |
| `-sc_threshold 0` | Disable scene-cut keyframes breaking alignment |

### Packager pattern (dual manifest, shared segments)

```txt
/origin/title/
  init.mp4              # shared init
  video_720p_00001.m4s  # shared by HLS + DASH URL mapping
  video_720p_00002.m4s
  master.m3u8           # HLS
  manifest.mpd          # DASH — BaseURL points to same .m4s
```

### DASH MPD snippet (segment template → same files)

```xml
<SegmentTemplate media="video_720p_$Number$.m4s" initialization="init.mp4"
  startNumber="1" duration="3840" timescale="960"/>
```

Duration in timescale units — must match ffmpeg segment length × timescale.

### Verify fMP4 structure

```bash
ffprobe -show_frames -select_streams v:0 -read_intervals 0%+5 -show_entries frame=pict_type,pts_time init.mp4
mp4dump --verbosity 1 segment.m4s | head -40   # Bento4, if installed
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Safari plays, Chrome DASH fails | Init segment URL mismatch | Same `initialization` source; CORS on init |
| ABR switch flash | GOP/chunk misaligned across rungs | Re-encode fixed GOP; identical segment duration |
| LL-HLS partials stall | Chunk duration vs part target | Shorter CMAF chunks; `EXT-X-PART` in [[HLS]] |
| DRM on HLS only | Different encryption per manifest | [[DRM]] CENC — one encrypted segment set |
| 404 on init.mp4 | CDN caches media but not init | Long-cache init; version in path on codec change |
| Audio missing in DASH | Separate AdaptationSet | Mirror HLS `#EXT-X-MEDIA` audio group |

---

## Gotchas

> [!WARNING]
> **Legacy HLS TS-only devices** — old STBs need parallel TS ladder or device blocklist; fMP4 is modern default.

> [!WARNING]
> **Init segment change** — codec/resolution change needs new init; stale CDN init → decode failure.

> [!WARNING]
> **Independent segments flag** — DASH `@sap` / HLS discontinuity mishandled → A/V glitch at boundaries.

> [!WARNING]
> **Encrypting init** — usually cleartext init + encrypted media; check [[EME]]/[[DRM]] vendor spec.

---

## When NOT to use

- **Legacy IPTV broadcast chain** — MPEG-TS end-to-end ([[MPEG-TS]]) may be mandatory.
- **Single-ecosystem (Apple-only)** — TS HLS still works but loses DASH unification benefit.
- **Sub-second WebRTC** — CMAF segment model adds seconds of latency; use WebRTC for that path.

---

## Related

[[HLS]] [[DASH]] [[HLS vs. DASH]] [[MPEG-TS]] [[Manifest (streaming)]] [[MPD]] [[DRM]] [[EME]] [[ABR]]
