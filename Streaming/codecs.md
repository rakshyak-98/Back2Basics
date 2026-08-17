[[AAC (Advanced Audio Coding)]] [[AV1]] [[Encoding]] [[transcoding]] [[bitrate streaming]] [[HLS]] [[DASH]] [[re-encoding]] [[NVENC]] [[CRF (Constant Rate Factor)]] [[CMAF]]

# Codecs

> Codecs — a codec (coder-decoder) transforms raw PCM/YUV into compressed bitstreams and back. Streaming stacks pick codecs at ingest, transcode, and playback — mismatches force expensive

```txt
        Codecs ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Codecs to see if you understand the pipeline role, fai…

## Sources
- [Wikipedia — codecs](https://en.wikipedia.org/wiki/codecs) — overview

## Key Concepts
- **Note:** A **codec** (coder-decoder) transforms raw PCM/YUV into compressed bitstreams…

| Category | Common codecs | Streaming role |
|----------|---------------|----------------|
| **Video baseline** | H.264 (AVC) | Universal ABR default |
| **Video efficiency** | HEVC (H.265), AV1, VP9 | 4K/HDR, bandwidth savings |
| **Audio default** | AAC-LC | HLS/DASH stereo |
| **Audio broadcast** | AC-3, E-AC-3 | Surround, ATSC |
| **WebRTC** | Opus, VP8/H.264 | Real-time, not HLS primary |
| **Legacy** | MPEG-2, MP3 | IPTV, old devices |

- **Note:** **Encode once, package many**

## Technical Details
```txt
Raw frames ──► Video codec (H.264/HEVC/AV1) ──► NAL units in fMP4/TS
Raw samples ──► Audio codec (AAC/Opus/AC-3) ──► frames in fMP4/TS
                        │
              Player capability check (EME + MSE)
                        │
                   Decode → render
```

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

- Wrong CODECS string → capable players refuse stream or mis-estimate bandwidth…

### Hardware vs software encode

```bash
# NVIDIA — see [[NVENC]]
ffmpeg -hwaccel cuda -i in.mp4 -c:v h264_nvenc -preset p4 -b:v 4500k -c:a aac out.mp4

# CPU quality anchor — see [[CRF (Constant Rate Factor)]]
ffmpeg -i in.mp4 -c:v libx264 -preset slow -crf 20 -c:a aac out.mp4
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen, audio OK | Video codec unsupported | Add H.264 rung; fix CODECS |
| Works desktop, fails TV | HEVC without hardware decode | H.264 fallback ladder |
| HDR washed out | HEVC Main10 vs SDR tag | Correct mastering metadata; separate HDR ladder |
| Huge files same "quality" | Wrong preset / no maxrate on CRF | Cap bitrate; review [[CRF (Constant Rate Factor)]] |
| DRM playback fail | Clear codec vs encrypted | [[DRM]] CENC profile must match device CDM |
| Transcode queue backlog | AV1 software too slow | AV1 only for VoD farm; live stays H.264/HEVC + [[NVENC]] |

- **Mistake:** **`-c:v copy` lie**
- **Mistake:** **Profile/level overflow**
- **Mistake:** **Multi-codec ladder explosion**
- **Mistake:** **B-frames and LL-HLS**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Mezzanine archive**
- **Con / skip when:** **AV1 for all live channels day one**
- **Con / skip when:** **Re-codec when remux suffices**

## Comparison
- vs [[re-encoding]]: **Re-codec when remux suffices**


### Use cases
- Used wherever Codecs sits in an ingest → package → CDN → player path
