[[ABR]] [[CRF (Constant Rate Factor)]] [[transcoding]] [[codecs]] [[rendition]] [[MPEG-TS]]

# Bitrate streaming

> ABR ladder design, CRF vs CBR, and encoder ops for multi-bitrate delivery — **streaming engineering, not generic video wiki**.

---

## Mental model

**Bitrate streaming** means encoding the same content at **multiple bitrates/resolutions** so the player ([[ABR]]) switches renditions without rebuffering. The **ladder** is the set of rungs; the **manifest** (HLS/DASH) advertises `BANDWIDTH` + `RESOLUTION` per rung.

```txt
Source mezzanine
    ├── 1080p @ 6 Mbps  ──► segment 2s ──► CDN
    ├── 720p  @ 3 Mbps
    ├── 480p  @ 1.2 Mbps
    └── audio @ 128k AAC (shared or per rung)
Player buffer ──► picks rung from throughput + buffer health
```

| Term | Meaning |
|------|---------|
| **CBR** | Target constant bitrate — predictable CDN cost; live broadcast |
| **VBR** | Variable within cap — better quality per bit |
| **CRF** | Quality target per encode pass — VOD file size varies ([[CRF (Constant Rate Factor)]]) |
| **GOP** | Keyframe interval — must align across ladder for clean ABR switch |
| **Segment duration** | HLS typically 2–6s — trades startup vs switch latency |

---

## Standard config / commands

### Ladder design (1080p live starting point)

```txt
Rung   Resolution   Video bitrate   Audio    Notes
1      1920x1080    5800 kbps       128k     WiFi / good LTE
2      1280x720     3000 kbps       128k     default desktop
3      854x480      1200 kbps       96k      mobile fallback
4      640x360       800 kbps       96k      constrained
5      426x240       400 kbps       64k      emergency

Rules:
  - ~1.5–2× ratio between rungs (not 10× jumps)
  - Same frame rate across rung OR separate ladders per fps
  - GOP = segment duration × fps (e.g. 2s @ 30fps → GOP 60)
  - Encode top rung first; cascade downscale or parallel per rung
```

### ffmpeg ladder (VOD, CRF per rung)

```bash
# Top rung — CRF quality anchor
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 20 -maxrate 5800k -bufsize 11600k \
  -g 60 -keyint_min 60 -sc_threshold 0 -c:a aac -b:a 128k -f hls -hls_time 2 out_1080.m3u8

# Lower rung — scale + higher CRF
ffmpeg -i input.mp4 -vf scale=-2:720 -c:v libx264 -crf 22 -maxrate 3000k -bufsize 6000k \
  -g 60 -keyint_min 60 -sc_threshold 0 -c:a aac -b:a 128k -f hls -hls_time 2 out_720.m3u8
```

### Live CBR (predictable uplink)

```bash
ffmpeg -re -i input -c:v libx264 -b:v 3000k -minrate 3000k -maxrate 3000k -bufsize 6000k \
  -g 60 -c:a aac -b:a 128k -f flv rtmp://origin/live/key
```

### Master manifest snippet

```plaintext
#EXT-X-STREAM-INF:BANDWIDTH=5932800,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
1080p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=3128000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
720p.m3u8
```

`BANDWIDTH` must include **video + audio + mux overhead** — player overestimates need if wrong → unnecessary downswitch.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Constant rebuffering | CDN logs; player bandwidth estimate | Add lower rung; reduce segment duration slightly |
| Never reaches top rung | `BANDWIDTH` inflated in manifest | Recalculate; include audio |
| Quality cliff between rungs | Bitrate gap too large | Insert intermediate rung |
| ABR switch flicker | GOP misaligned | Re-encode with fixed GOP; `-sc_threshold 0` |
| Blurry on motion | CRF too high / low bitrate cap | Raise cap or lower CRF on that rung |
| Audio sync drift | Separate audio renditions | Use same segment boundaries; packaged audio per variant |
| Live uplink unstable | Encoder CBR exceeding link | Drop rung count; [[NVENC]] hardware; SRT with ARQ |

```bash
ffprobe -show_streams -select_streams v manifest.m3u8
mediainfo segment000.ts
```

---

## Gotchas

> [!WARNING]
> **CRF ladder without maxrate** — VOD rungs blow past CDN budget; cap with `-maxrate`/`-bufsize`.

> [!WARNING]
> **Different GOP across rungs** — player switches mid-GOP → flash/block until next keyframe.

> [!WARNING]
> **Upscale low rung** — 240p stretched to 4K TV looks awful; cap max display resolution in player logic.

> [!WARNING]
> **BANDWIDTH typo** — 5932800 vs 593280 — player math breaks.

> [!WARNING]
> **Per-title encoding ignored** — one ladder for cartoons and sports wastes bits; per-content analysis if scale warrants.

> [!WARNING]
> **Audio-only HLS variant forgotten** — accessibility + ultra-low bandwidth path missing.

---

## When NOT to use

- **Internal mezzanine archive** — single high-bitrate master; ladder only at origin edge.
- **CRF for live broadcast contractual bitrate** — use CBR/ capped VBR.
- **20-rung ladder** — storage/CDN cost; diminishing returns beyond ~5–6 rungs.

---

## Related

[[ABR]] [[CRF (Constant Rate Factor)]] [[transcoding]] [[codecs]] [[rendition]] [[MPEG-TS]] [[NVENC]]
