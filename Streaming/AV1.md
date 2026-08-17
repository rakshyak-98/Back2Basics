[[Streaming]] [[codecs]] [[Encoding]] [[NVENC]] [[ABR]] [[rendition]] [[transcoding]] [[HLS]] [[DASH]] [[bitrate streaming]]

# AV1

> AV1 is an open video codec — same quality at lower bitrate than H.264/HEVC, but encode cost and device support still gate rollout.

```txt
        AV1 ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk AV1 end-to-end

## Sources
- [Wikipedia — AV1](https://en.wikipedia.org/wiki/AV1) — overview

## Key Concepts
- **AV1:** Modern open video codec
- **SVT-AV1 / libaom:** Software encoders — “CPU-heavy; use for VOD farms, not cheap live.”
- **NVENC AV1:** NVIDIA HW encode — “Ada+ only — T4/A2 do not encode AV1.”
- **HW decode:** Chip can play AV1 — “Decode landed earlier than encode on many GPUs.”
- **Dual ladder:** AV1 + H.264/HEVC — “Manifest offers both; client capability picks.”

**Flow:**

1. **Decide target** — VOD savings versus live latency/cost.
- **Note:** 2. **Pick encoder** — SVT-AV1/libaom software, or Ada+ [[NVENC]] for HW.
- **Note:** 3. **Package** — signal codec in [[HLS]]/[[DASH]]; keep aligned GOPs if ABR.
- **Note:** 4. **Fallback** — always publish a widely decodable rung (usually H.264).

- **Note:** Alliance for Open Media (AOMedia


- **Core:** “AV1 stream” means the **payload** is AV1 inside MPTS/SPTS or CMAF

## Technical Details
```txt
Mezzanine / live source
      │
      ├─ AV1 encode ──► [[HLS]] / [[DASH]] AV1 [[rendition]]s
      │
      └─ H.264/HEVC fallback ladder (older STBs / browsers)
      │
      ▼
Player picks codec it can decode (+ [[ABR]] within that family)
```

```bash
# Software (VOD-oriented sketch)
ffmpeg -i mezz.mov \
  -c:v libsvtav1 -crf 30 -b:v 0 \
  -g 48 -keyint_min 48 \
  -c:a aac -b:a 128k \
  out_av1.mp4

# NVIDIA AV1 NVENC (Ada / RTX 40 / L4 / L40 — not T4/A2)
ffmpeg -hwaccel cuda -i in.mp4 \
  -c:v av1_nvenc -b:v 3M -maxrate 3M -bufsize 6M \
  -c:a copy out_av1.mp4

ffprobe -hide_banner out_av1.mp4   # confirm codec_name=av1
```

| Knob | Why it matters |
|------|----------------|
| Encoder choice | libaom slowest/best; SVT-AV1 throughput; NVENC live capacity |
| GPU generation | AV1 **encode** needs Ada+ NVENC; older cards decode-only |
| Bitrate vs CRF | Live uses capped bitrate; VOD often CRF/CQ |
| Fallback renditions | STB/browser gaps — don’t ship AV1-only |
| Packaging labels | Wrong codec string ⇒ player never selects the rung |

- Debug: `ffprobe` codec → chrome://media-internals or player codec log → compa…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| NVENC AV1 fails on T4/A2 | GPU generation | Use H.264/HEVC NVENC or software AV1 elsewhere |
| Black play, encode succeeded | Client decode support | Add H.264/HEVC fallback in manifest |
| Live backlog / huge CPU | Software AV1 live | SVT presets, fewer rungs, or Ada NVENC |
| ABR never picks AV1 | Manifest codec / bandwidth | Fix CODECS= / mime; validate player caps |
| Worse than H.264 at same bits | Bad preset / too-low bitrate | Tune CRF; don’t under-bitrate the ladder |
| Safari / old STB fails only | No AV1 decode | Expected — serve fallback family |

- **Mistake:** **Encode ≠ decode support**
- **Mistake:** **AV1-only ladder**
- **Mistake:** **Royalty-free ≠ free ops**
- **Mistake:** **Naming mix-ups**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Broad STB estate without AV1 decode**
- **Con / skip when:** **Cheap live on pre-Ada GPUs**
- **Con / skip when:** **One-off user uploads with tiny audience**
- **Con / skip when:** **You only needed a container change**

## Comparison
- vs [[transcoding\|transcode]]: **You only needed a container change**


### Use cases
- “AV1 stream” means the **payload** is AV1 inside MPTS/SPTS or CMAF

- Used wherever AV1 sits in an ingest → package → CDN → player path
