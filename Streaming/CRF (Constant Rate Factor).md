[[bitrate streaming]] [[Encoding]] [[transcoding]] [[NVENC]] [[codecs]] [[re-encoding]] [[ABR]]

# CRF (Constant Rate Factor)

> CRF (Constant Rate Factor) — CRF 18 ──► high quality, large files (archival-ish VoD)

```txt
        CRF (Constant Rate ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Why It Matters
- **Key signal:** Reviewers ask about CRF to see if you understand the pipeline role, failur…

## Sources
- [Wikipedia — CRF](https://en.wikipedia.org/wiki/CRF) — overview

## Key Concepts
- **Note:** **CRF** tells the encoder **how hard to compress** (quality target), not a fi…

| Mode | Use when | Predictability |
|------|----------|----------------|
| **CRF** | VoD file size flexible | Quality stable, size varies |
| **CBR** | Live uplink / broadcast cap | Bitrate stable, quality varies |
| **VBR + maxrate** | Hybrid VoD ladder | Cap worst-case CDN cost |

- **Note:** CRF is **single-pass friendly** for VoD

## Technical Details
```txt
CRF 18 ──► high quality, large files (archival-ish VoD)
CRF 23 ──► default balance
CRF 28 ──► small files, visible artifacts on motion

Per-scene complexity ──► encoder allocates bits dynamically
Manifest BANDWIDTH ──► must use measured peak / capped maxrate for ABR
```

### x264 CRF (quality anchor)

```bash
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 20 \
  -pix_fmt yuv420p -c:a aac -b:a 128k output.mp4
```

| Knob | Why |
|------|-----|
| `-crf 20` | High VoD quality; 23 for web default |
| `-preset slow` | Better compression efficiency; `veryfast` for drafts |
| `-pix_fmt yuv420p` | Player compatibility |
| **No `-b:v`** | Bitrate floats with CRF — intentional |

### CRF ladder with caps (ABR-safe)

```bash
# Cap peak for manifest honesty — see [[bitrate streaming]]
ffmpeg -i input.mp4 -vf scale=-2:1080 -c:v libx264 -crf 20 \
  -maxrate 5800k -bufsize 11600k -g 60 -sc_threshold 0 \
  -c:a aac -b:a 128k -f hls -hls_time 4 1080p.m3u8
```

### x265 (HEVC) CRF

```bash
ffmpeg -i input.mp4 -c:v libx265 -crf 24 -preset medium -tag:v hvc1 \
  -c:a aac -b:a 128k output.mp4
```

- HEVC CRF **≠** H.264 CRF numerically — compare visually, not by number.

### Two-pass when CRF isn't enough

```bash
# Target file size constraint — use two-pass VBR instead of pure CRF
ffmpeg -y -i input.mp4 -c:v libx264 -b:v 2000k -pass 1 -f null /dev/null
ffmpeg -i input.mp4 -c:v libx264 -b:v 2000k -pass 2 -c:a aac output.mp4
```

### Measure actual bitrate for manifest

```bash
ffprobe -v error -show_entries format=bit_rate -of csv=p=0 output.mp4
# Or peak over segments for HLS
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| File huge vs expectation | CRF too low; action movie | Raise CRF 1–2; or tighten `-maxrate` |
| Blocky on motion | CRF too high | Lower CRF; slower preset |
| Ladder top rung exceeds CDN budget | Uncapped CRF per rung | Add `-maxrate`/`-bufsize` per rung |
| ABR never switches up | Manifest BANDWIDTH too high | Measure encoded output; fix master playlist |
| Inconsistent rung quality | Same CRF at different resolutions | Per-rung CRF offset (+2 for 720p, +4 for 480p) |
| Live attempt with CRF | Uplink spikes | Switch to CBR for live ([[RTMP]] ingest) |

- **Mistake:** **CRF + `-b:v` together**
- **Mistake:** **Copy CRF across codecs**
- **Mistake:** **Hardware encoders (NVENC)**
- **Mistake:** **Statistical multiplexing**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Contractual max bitrate (broadcast)** — use CBR.
- **Con / skip when:** **Live with fixed uplink**
- **Con / skip when:** **ABR manifest without maxrate**

## Real-World Applications
- **Scenario:** Used wherever CRF sits in an ingest → package → CDN → player path
