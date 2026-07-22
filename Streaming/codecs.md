[[AAC (Advanced Audio Coding)]] [[AV1]] [[Encoding]] [[transcoding]] [[bitrate streaming]] [[HLS]] [[DASH]]

# Codecs

> Compress/decompress algorithms for A/V — **encoder choice drives compatibility, cost, and ladder design**.

---

## Mental model

A **codec** (coder-decoder) transforms raw PCM/YUV into compressed bitstreams and back. Streaming stacks pick codecs at **ingest**, **transcode**, and **playback** — mismatches force expensive [[re-encoding]]. Manifests advertise codecs via **`CODECS`** (HLS) or **MP4 `codec` attributes** (DASH) so players reject unsupported combinations before download.

```txt
Raw frames ──► Video codec (H.264/HEVC/AV1) ──► NAL units in fMP4/TS
Raw samples ──► Audio codec (AAC/Opus/AC-3) ──► frames in fMP4/TS
                        │
              Player capability check (EME + MSE)
                        │
                   Decode → render
```

| Category | Common codecs | Streaming role |
|----------|---------------|----------------|
| **Video baseline** | H.264 (AVC) | Universal ABR default |
| **Video efficiency** | HEVC (H.265), AV1, VP9 | 4K/HDR, bandwidth savings |
| **Audio default** | AAC-LC | HLS/DASH stereo |
| **Audio broadcast** | AC-3, E-AC-3 | Surround, ATSC |
| **WebRTC** | Opus, VP8/H.264 | Real-time, not HLS primary |
| **Legacy** | MPEG-2, MP3 | IPTV, old devices |

**Encode once, package many** — mezzanine in high-quality intermediate; ladder generates delivery codecs ([[transcoding]]).

---

## Standard config / commands

### Capability matrix (2026 pragmatic default)

```txt
Profile              Video        Audio       Container
Max reach live/VOD   H.264 High   AAC-LC      CMAF fMP4
Premium 4K           HEVC Main10  AAC-LC      fMP4 + DRM
Cost-optimized CDN   AV1          AAC-LC      fMP4 (check device %)
Legacy STB           H.264        AAC         MPEG-TS
```

### ffmpeg — inspect codecs

```bash
ffprobe -v error -show_entries stream=codec_name,codec_tag_string,profile,width,height,bit_rate -of json input.mp4
```

### ffmpeg — ladder with explicit codecs

```bash
# H.264 High @ 720p + AAC — CODECS avc1.64001f,mp4a.40.2
ffmpeg -i in.mp4 -vf scale=-2:720 -c:v libx264 -profile:v high -level 4.1 \
  -crf 22 -maxrate 3000k -bufsize 6000k -g 60 -sc_threshold 0 \
  -c:a aac -profile:a aac_low -b:a 128k -ar 48000 out_720.mp4
```

### HLS CODECS reference (copy into master playlist)

```txt
H.264 Baseline 3.0   avc1.420015
H.264 Main 3.1       avc1.4d401f
H.264 High 4.0       avc1.640028
HEVC Main10          hvc1.2.4.L153.B0
AAC-LC               mp4a.40.2
```

Wrong CODECS string → capable players refuse stream or mis-estimate bandwidth ([[ABR]]).

### Hardware vs software encode

```bash
# NVIDIA — see [[NVENC]]
ffmpeg -hwaccel cuda -i in.mp4 -c:v h264_nvenc -preset p4 -b:v 4500k -c:a aac out.mp4

# CPU quality anchor — see [[CRF (Constant Rate Factor)]]
ffmpeg -i in.mp4 -c:v libx264 -preset slow -crf 20 -c:a aac out.mp4
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen, audio OK | Video codec unsupported | Add H.264 rung; fix CODECS |
| Works desktop, fails TV | HEVC without hardware decode | H.264 fallback ladder |
| HDR washed out | HEVC Main10 vs SDR tag | Correct mastering metadata; separate HDR ladder |
| Huge files same "quality" | Wrong preset / no maxrate on CRF | Cap bitrate; review [[CRF (Constant Rate Factor)]] |
| DRM playback fail | Clear codec vs encrypted | [[DRM]] CENC profile must match device CDM |
| Transcode queue backlog | AV1 software too slow | AV1 only for VoD farm; live stays H.264/HEVC + [[NVENC]] |

---

## Gotchas

> [!WARNING]
> **`-c:v copy` lie** — container compatible ≠ player compatible; always verify target devices.

> [!WARNING]
> **Profile/level overflow** — 1080p60 High 4.2 content tagged 4.0 fails on old mobile hardware decoders.

> [!WARNING]
> **Multi-codec ladder explosion** — H.264 + HEVC + AV1 × 5 rungs = 15 renditions; use device-based manifest filtering.

> [!WARNING]
> **B-frames and LL-HLS** — low-latency profiles may restrict B-frame count; encoder preset side effects.

---

## When NOT to use

- **Mezzanine archive** — use ProRes/DNxHR (editing), not H.264 delivery codec.
- **AV1 for all live channels day one** — encode latency and CPU/GPU cost unless fleet sized for it.
- **Re-codec when remux suffices** — change container with `-c copy` before full [[re-encoding]].

---

## Related

[[AAC (Advanced Audio Coding)]] [[AV1]] [[Encoding]] [[transcoding]] [[re-encoding]] [[NVENC]] [[CRF (Constant Rate Factor)]] [[bitrate streaming]] [[CMAF]]
