[[Streaming]] [[codecs]] [[Encoding]] [[NVENC]] [[ABR]] [[rendition]] [[transcoding]]

# AV1

> AV1 is an open video codec — same quality at lower bitrate than H.264/HEVC, but encode cost and device support still gate rollout.

---

## Mental model

**Say it in one breath:** Compress video with AV1 to save bits; ship a fallback rung where players cannot decode it yet.

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

Alliance for Open Media (AOMedia — Google, Netflix, Amazon, Microsoft, Intel, Nvidia, …) backs the codec. Royalty-free licensing is the business pitch; **encode cost and client decode** are the operations pitch.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **AV1** | Modern open video codec | “Better compression; we still need a fallback ladder.” |
| **SVT-AV1 / libaom** | Software encoders | “CPU-heavy; use for VOD farms, not cheap live.” |
| **NVENC AV1** | NVIDIA HW encode | “Ada+ only — T4/A2 do not encode AV1.” |
| **HW decode** | Chip can play AV1 | “Decode landed earlier than encode on many GPUs.” |
| **Dual ladder** | AV1 + H.264/HEVC | “Manifest offers both; client capability picks.” |

### How the story goes (4 steps)

1. **Decide target** — VOD savings versus live latency/cost.
2. **Pick encoder** — SVT-AV1/libaom software, or Ada+ [[NVENC]] for HW.
3. **Package** — signal codec in [[HLS]]/[[DASH]]; keep aligned GOPs if ABR.
4. **Fallback** — always publish a widely decodable rung (usually H.264).

> [!INFO]
> “AV1 stream” means the **payload** is AV1 inside MPTS/SPTS or CMAF — transport is still MPEG-TS / fMP4, not a separate network protocol.

---

## Standard config / commands

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

Debug: `ffprobe` codec → chrome://media-internals or player codec log → compare bitrate at matched VMAF versus H.264 rung.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| NVENC AV1 fails on T4/A2 | GPU generation | Use H.264/HEVC NVENC or software AV1 elsewhere |
| Black play, encode succeeded | Client decode support | Add H.264/HEVC fallback in manifest |
| Live backlog / huge CPU | Software AV1 live | SVT presets, fewer rungs, or Ada NVENC |
| ABR never picks AV1 | Manifest codec / bandwidth | Fix CODECS= / mime; validate player caps |
| Worse than H.264 at same bits | Bad preset / too-low bitrate | Tune CRF; don’t under-bitrate the ladder |
| Safari / old STB fails only | No AV1 decode | Expected — serve fallback family |

---

## Gotchas

> [!WARNING]
> **Encode ≠ decode support** — Turing often decodes AV1; **encode** on NVIDIA needs Ada-generation NVENC (L4, L40, RTX 40-series). T4 and A2 do not encode AV1.

> [!WARNING]
> **AV1-only ladder** — still breaks a slice of STBs and older mobiles. Dual-codec delivery is normal in 2025–2026 fleets.

> [!WARNING]
> **Royalty-free ≠ free ops** — encode farm cost can erase CDN savings if you pick the wrong live preset.

> [!WARNING]
> **Naming mix-ups** — people say “H.256”; they mean HEVC (H.265) or AV1. Say the four-character codec name in reviews.

---

## When NOT to use

- **Broad STB estate without AV1 decode** — stay on H.264/HEVC until devices catch up.
- **Cheap live on pre-Ada GPUs** — no AV1 NVENC; software live may miss latency SLOs.
- **One-off user uploads with tiny audience** — H.264 is enough; AV1 savings won’t pay encode time.
- **You only needed a container change** — remux; do not [[transcoding\|transcode]] to AV1 “because modern.”

---

## Related

[[codecs]] [[Encoding]] [[NVENC]] [[transcoding]] [[ABR]] [[rendition]] [[HLS]] [[DASH]] [[bitrate streaming]]
