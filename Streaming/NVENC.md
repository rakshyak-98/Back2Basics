[[Encoding]] [[transcoding]] [[CRF (Constant Rate Factor)]] [[bitrate streaming]] [[OBS]]

# NVENC (NVIDIA Encoder)

> Hardware H.264/HEVC/AV1 encode on NVIDIA GPUs — **offload live/VoD from CPU**, with rate-control tradeoffs.

---

## Mental model

**NVENC** is a **dedicated encode ASIC** on NVIDIA GPUs (GeForce, RTX, datacenter L4/A10/A100 lines). It runs **parallel to CUDA cores** — multiple live channels per GPU without starving compute. Quality at equal bitrate historically lagged **libx264**; modern **RTX 40+ / Ada** encoders close the gap for live **CBR** workloads.

```txt
CPU: demux / mux / audio / orchestration
GPU: NVENC ──► H.264/HEVC bitstream ──► packager ([[HLS]]/[[DASH]])
         │
    Session limit per GPU (driver dependent)
```

| Use case | NVENC fit | Prefer libx264 when |
|----------|-----------|---------------------|
| **Live multi-channel** | Excellent | — |
| **VoD highest quality** | Good with tuning | Archive / film grain |
| **Low latency** | `preset p1` + tune ll | — |
| **AV1 delivery** | RTX 40+ AV1 NVENC | Software AV1 for max compression |

Pair with **`-hwaccel cuda`** for decode when transcoding on GPU.

---

## Standard config / commands

### Live CBR (RTMP ingest)

```bash
ffmpeg -hwaccel cuda -hwaccel_output_format cuda -i input.mp4 \
  -c:v h264_nvenc -preset p4 -tune ll -profile:v high \
  -b:v 4500k -minrate 4500k -maxrate 4500k -bufsize 9000k \
  -g 60 -forced-idr 1 \
  -c:a aac -b:a 128k -f flv rtmp://origin/live/key
```

| Knob | Why |
|------|-----|
| `-preset p4` | Balance quality/latency (`p1` fastest, `p7` best quality) |
| `-tune ll` | Low-latency live |
| `-forced-idr 1` | Keyframe on GOP boundary for ABR |
| CBR triplet | Stable uplink ([[bitrate streaming]]) |

### CQ mode (VoD-ish quality target — NVENC's CRF cousin)

```bash
ffmpeg -i input.mp4 -c:v hevc_nvenc -preset p5 -rc vbr -cq 23 -b:v 0 -maxrate 8M -bufsize 16M \
  -c:a aac -b:a 128k output.mp4
```

Cap with `-maxrate` for manifest honesty — see [[CRF (Constant Rate Factor)]].

### Multi-session on one GPU

```bash
# Monitor encode sessions
nvidia-smi encodersessions
nvidia-smi dmon -s u -d 1
```

Consumer GeForce has **session count limits** (historically 3 on some drivers; datacenter cards higher) — verify for your fleet.

### OBS settings (Quick Sync vs NVENC)

```txt
Settings → Output → Encoder: NVIDIA NVENC H.264 (new)
Rate Control: CBR
Bitrate: match uplink (e.g. 4500 Kbps)
Keyframe Interval: 2 s (matches HLS segment)
Preset: Quality or Max Quality (P4–P5 equivalent)
```

See [[OBS]].

### Quality check vs x264

```bash
ffmpeg -i ref_x264.mp4 -i test_nvenc.mp4 -lavfi libvmaf -f null -
# Or SSIM: ffmpeg -i a -i b -lavfi ssim -f null -
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `No NVENC capable devices` | Driver, headless GPU | `nvidia-smi`; install datacenter driver; not CPU-only VM |
| Session limit exceeded | `nvidia-smi encodersessions` | Add GPU; reduce channels; use datacenter SKU |
| Worse quality vs x264 same bitrate | Preset too fast | `p5`/`p6`; enable AQ; slight bitrate bump |
| Keyframe drift | Missing `-g` / `-forced-idr` | Align GOP to segment ([[CMAF]]) |
| CUDA errors in pipeline | OOM on GPU | Reduce concurrent `-hwaccel`; fall back SW decode |
| HEVC won't play on device | Profile/ tag | `-tag:v hvc1` for Apple |

---

## Gotchas

> [!WARNING]
> **Cloud VM without GPU** — AWS `g4dn` etc. required; default instances have no NVENC.

> [!WARNING]
> **Driver version ↔ ffmpeg build** — stale static ffmpeg may miss newest NVENC API.

> [!WARNING]
> **B-frames + ultra-low latency** — reduce B-frame count for LL-HLS paths.

> [!WARNING]
> **GeForce vs Quadro licensing** — consumer drivers on servers may violate EULA; use datacenter cards in prod.

> [!WARNING]
> **Audio still on CPU** — GPU encode doesn't offload AAC; plan CPU for audio + mux.

---

## When NOT to use

- **No NVIDIA hardware** — Intel QSV / AMD AMF / libx264 instead.
- **Film grain VoD mastering** — software encode preserves detail better at same size.
- **One short clip monthly** — GPU fleet overhead not worth ops.

---

## Related

[[Encoding]] [[transcoding]] [[CRF (Constant Rate Factor)]] [[bitrate streaming]] [[OBS]] [[ingestion]] [[Microservice]]
