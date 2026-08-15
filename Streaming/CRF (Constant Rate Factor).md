[[bitrate streaming]] [[Encoding]] [[transcoding]] [[NVENC]] [[codecs]] [[re-encoding]] [[ABR]]

# CRF (Constant Rate Factor)

> CRF (Constant Rate Factor) — CRF 18 ──► high quality, large files (archival-ish VoD)

## Interview Relevance

Interviewers ask about CRF to see if you understand the pipeline role, failure modes, and trade-offs — not just the acronym.

## Sources

- [Wikipedia — CRF](https://en.wikipedia.org/wiki/CRF) — overview

## Key Concepts

**CRF** tells the encoder **how hard to compress** (quality target), not a fixed bitrate. Complex scenes get **more bits**; static scenes get **fewer** — average file size **varies by content**. Scale: lower CRF = higher quality (x264 typical range **18–28**, sane default **23**).

| Mode | Use when | Predictability |
|------|----------|----------------|
| **CRF** | VoD file size flexible | Quality stable, size varies |
| **CBR** | Live uplink / broadcast cap | Bitrate stable, quality varies |
| **VBR + maxrate** | Hybrid VoD ladder | Cap worst-case CDN cost |

CRF is **single-pass friendly** for VoD; live ABR ladders usually use **CBR or capped VBR** ([[bitrate streaming]]).

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

HEVC CRF **≠** H.264 CRF numerically — compare visually, not by number.

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

## Real-World Applications

Used wherever CRF sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Contractual max bitrate (broadcast)** — use CBR.
- **Con / skip when:** **Live with fixed uplink** — CBR or capped VBR; CRF can spike and drop frames.
- **Con / skip when:** **ABR manifest without maxrate** — player bandwidth math breaks on variable peaks.

## Mistakes to Avoid

| Symptom | Check | Fix |
|---------|-------|-----|
| File huge vs expectation | CRF too low; action movie | Raise CRF 1–2; or tighten `-maxrate` |
| Blocky on motion | CRF too high | Lower CRF; slower preset |
| Ladder top rung exceeds CDN budget | Uncapped CRF per rung | Add `-maxrate`/`-bufsize` per rung |
| ABR never switches up | Manifest BANDWIDTH too high | Measure encoded output; fix master playlist |
| Inconsistent rung quality | Same CRF at different resolutions | Per-rung CRF offset (+2 for 720p, +4 for 480p) |
| Live attempt with CRF | Uplink spikes | Switch to CBR for live ([[RTMP]] ingest) |

- **CRF + `-b:v` together** — x264 uses `-b:v` as VBR cap in some modes; know your encoder docs.
- **Copy CRF across codecs** — AV1 CRF 30 ≠ x264 CRF 30; re-tune per codec.
- **Hardware encoders (NVENC)** — use CQ/VBR quality modes, not libx264 CRF — see [[NVENC]].
- **Statistical multiplexing** — broadcast statmux needs CBR; CRF incompatible with shared pool.
