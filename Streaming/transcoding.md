[[Streaming]] [[Encoding]] [[ffmpeg]] [[ABR]] [[rendition]] [[NVENC]] [[codecs]]

# transcoding

> Transcoding decodes media then re-encodes it — new codec, size, or bitrate for devices and ABR ladders.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Uncompress the input, then compress again into the shape your players and CDN need.

```txt
Source file / live ingest
      │
      ▼
 Decode (expand to raw frames / PCM)
      │
      ▼
 Encode (new codec / res / bitrate)
      │
      ▼
 Package ──► [[HLS]] / [[DASH]] / mezzanine file
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Transcode** | Decode then encode again | “We change format or quality by full re-encode.” |
| **Remux** | Change container only | “No pixel rewrite — much cheaper than transcode.” |
| **Mezzanine** | High-quality intermediate | “Edit/archive in ProRes; deliver H.264 later.” |
| **Ladder** | Several [[rendition]]s | “One source → many bitrates for [[ABR]].” |
| **HW encode** | GPU / ASIC encoder | “NVENC cuts CPU; watch generation for AV1.” |
| **Generation loss** | Quality drop each re-encode | “Avoid transcode chains; keep a mezzanine.” |

### Why teams do it (4 jobs)

1. **Compatibility** — camera/vendor formats → browser/STB codecs.
2. **ABR** — build the [[rendition]] ladder ([[bitrate streaming]]).
3. **Size** — shrink archive or contribution bitrates for delivery.
4. **Edit workflows** — highly compressed camera → mezzanine for NLEs.

> [!INFO]
> Remux (`-c copy`) is not a transcode. If you only need MP4 instead of MKV and codecs already match, copy streams.

---

## Standard config / commands

```bash
# Remux only (no quality loss)
ffmpeg -i in.mkv -c copy out.mp4

# Software H.264 ladder rung (example 1080p)
ffmpeg -i mezz.mov \
  -c:v libx264 -preset medium -crf 23 \
  -g 48 -keyint_min 48 -sc_threshold 0 \
  -c:a aac -b:a 128k \
  out_1080.mp4

# NVIDIA HW path (when NVENC available)
ffmpeg -hwaccel cuda -i in.mp4 \
  -c:v h264_nvenc -b:v 5M -maxrate 5M -bufsize 10M \
  -c:a aac -b:a 128k out.mp4
```

| Knob | Why it matters |
|------|----------------|
| `-c copy` vs re-encode | Copy = remux; re-encode = CPU/GPU + generation loss |
| GOP / keyint aligned | Required for clean [[ABR]] switches across rungs |
| CRF vs CBR/VBR | CRF for VOD quality; capped bitrate for live/ABR |
| HW encoder gen | [[NVENC]] feature set differs (AV1 needs Ada+) |
| Audio codec | AAC is the usual web/OTT default |

Debug: `ffprobe -hide_banner in.mp4` → confirm codecs → compare `ffmpeg -benchmark` CPU vs NVENC → spot A/V drift with `-async` / properly synced encodes.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Player won’t open file | Codec / container via ffprobe | Transcode to H.264+AAC in MP4/fMP4 |
| ABR switches glitch | Keyframe alignment across rungs | Fixed GOP; same timescale; aligned IDR |
| Huge CPU / backlog | Software encode under load | [[NVENC]] / more workers; lower preset cost |
| Soft / blocky output | CRF too high or bitrate too low | Raise bitrate / lower CRF; avoid 3rd-gen loss |
| Audio drifts after hours | Timestamps / variable frame rate | CFR encode; check input PTS; resetts carefully |
| “Transcode” still huge | Actually remuxed or wrong ladder | Confirm re-encode in logs; set target bitrates |

---

## Gotchas

> [!WARNING]
> **Transcode ≠ remux** — `-c copy` never changes pixels. Saying “we transcoded” when you only remuxed misleads capacity planning.

> [!WARNING]
> **Generation loss stacks** — H.264 → H.264 → H.264 looks worse each hop. Keep a mezzanine; derive delivery from it.

> [!WARNING]
> **Live ABR without aligned GOPs** — players switch mid-GOP and show artifacts. Fix the ladder, not the CDN.

> [!WARNING]
> **HW encode defaults** — NVENC “quality” presets ≠ x264 CRF; validate VMAF/PSNR on a sample before fleet rollout.

---

## When NOT to use

- **Only the container is wrong** — remux with stream copy.
- **Already have a correct ladder** — re-packaging/packaging only; don’t burn encode farm.
- **Passthrough contribution that players accept** — ingest and package; skip a second encode.
- **Lossless archive requirement** — store mezzanine / original; transcode is for delivery copies.

---

## Related

[[Encoding]] [[ffmpeg]] [[ABR]] [[rendition]] [[bitrate streaming]] [[NVENC]] [[codecs]] [[CRF (Constant Rate Factor)]] [[AV1]] [[ingestion]] [[re-encoding]]
