[[transcoding]] [[re-encoding]] [[codecs]] [[CRF (Constant Rate Factor)]] [[NVENC]] [[ingestion]]

# Encoding

> Raw A/V → compressed bitstream for storage or delivery — **first permanent quality decision** in the pipeline.

---

## Mental model

**Encoding** converts **uncompressed or mezzanine** video/audio into a **codec bitstream** (H.264, AAC, etc.) suitable for containers ([[CMAF]], TS) and protocols ([[HLS]], [[DASH]], [[RTMP]]). It is **lossy** for delivery codecs — you cannot recover discarded detail. Downstream **packaging** muxes encoded streams; **[[transcoding]]** is encode-after-decode when format changes.

```txt
Camera / file ──► Encode (codec params) ──► Elementary streams
                           │
              ┌────────────┼────────────┐
         Live CBR      VoD CRF      HW NVENC
              │            │            │
         RTMP/SRT     ABR ladder    GPU fleet
```

| Stage | Question | Wrong answer cost |
|-------|----------|-------------------|
| **Mezzanine** | Archive master quality? | Re-shoot / re-ingest impossible |
| **ABR ladder** | How many rungs? | CDN $ + rebuffer or waste |
| **Live** | CBR cap vs quality | Uplink drops, macroblocking |
| **DRM** | Encode clear or encrypted? | Re-package if keys rotate wrong |

**Encode once well** at mezzanine; ladder encodes can downscale from mezzanine rather than re-decoding consumer files.

---

## Standard config / commands

### VoD mezzanine (quality master)

```bash
ffmpeg -i camera.mov -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a pcm_s24le -movflags +faststart mezzanine.mov
```

Store mezzanine; generate delivery from it ([[re-encoding]] only when targets change).

### Live encode to ingest ([[RTMP]])

```bash
ffmpeg -re -f lavfi -i testsrc=size=1280x720:rate=30 \
  -c:v libx264 -preset veryfast -b:v 2500k -minrate 2500k -maxrate 2500k -bufsize 5000k \
  -g 60 -keyint_min 60 -sc_threshold 0 \
  -c:a aac -b:a 128k -ar 48000 -f flv rtmp://origin/live/stream_key
```

| Knob | Why |
|------|-----|
| `-re` | Real-time pacing for live |
| CBR triplet | Stable uplink utilization |
| `-g 60` @ 30fps | 2s keyframe interval for 2s HLS segments |
| `-sc_threshold 0` | No extra keyframes breaking ABR alignment |

### ABR ladder from mezzanine

```bash
# Top rung — see [[CRF (Constant Rate Factor)]] + [[bitrate streaming]]
ffmpeg -i mezzanine.mov -c:v libx264 -crf 20 -maxrate 5800k -bufsize 11600k \
  -g 60 -sc_threshold 0 -c:a aac -b:a 128k -vf scale=-2:1080 1080p.mp4
```

### Hardware path

```bash
ffmpeg -hwaccel cuda -i in.mp4 -c:v h264_nvenc -preset p4 -b:v 4500k -c:a aac out.mp4
```

See [[NVENC]] for GPU fleet sizing.

### QC after encode

```bash
ffmpeg -i out.mp4 -vf signalstats -f null -
ffprobe -show_frames -select_streams v:0 -show_entries frame=pict_type -of csv | head
# Verify regular IDR at expected GOP
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Macroblocking live | Bitrate too low for motion | Raise `-b:v` or drop resolution |
| Audio drift over hours | `-re` vs wall clock skew | Hardware encoder timestamp; restart policy |
| Huge mezzanine | CRF too low / uncompressed audio | Adjust CRF; AAC or FLAC mezzanine |
| Keyframe every few frames | `-sc_threshold` default | Set `-sc_threshold 0` for streaming |
| 60fps stutter on 30fps ladder | Frame rate mismatch | Separate ladders or force `-r 30` |
| GPU encode banding | NVENC rate control | Tune CQ/VBR; increase `-b:v` floor |

---

## Gotchas

> [!WARNING]
> **Encoding ≠ packaging** — H.264 elementary stream still needs HLS/DASH mux ([[CMAF]]).

> [!WARNING]
> **Double encode quality loss** — OBS → RTMP → transcode → ladder = generational loss; minimize hops.

> [!WARNING]
> **Interlaced source** — deinterlace (`-vf yadif`) before H.264 progressive delivery.

> [!WARNING]
> **Color range** — TV vs PC levels wrong → crushed blacks; tag `-color_range tv`.

---

## When NOT to use

- **Remux only** — if codec already target-compatible, `-c copy` ([[re-encoding]] not needed).
- **Encode on every playback** — edge transcode is emergency; pre-encode ladders at origin.
- **Maximum compression on mezzanine** — mezzanine should be high quality; crunch at delivery rungs.

---

## Related

[[transcoding]] [[re-encoding]] [[codecs]] [[CRF (Constant Rate Factor)]] [[NVENC]] [[ingestion]] [[bitrate streaming]] [[OBS]]
