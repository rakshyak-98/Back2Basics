[[transcoding]] [[re-encoding]] [[codecs]] [[CRF (Constant Rate Factor)]] [[NVENC]] [[ingestion]] [[bitrate streaming]] [[OBS]]

# Encoding

> Encoding — camera / file ──► Encode (codec params) ──► Elementary streams

```txt
        Encoding ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Encoding to see if you understand the pipeline role, f…

## Sources
- [Wikipedia — Encoding](https://en.wikipedia.org/wiki/Encoding) — overview

## Key Concepts
- **Note:** **Encoding** converts **uncompressed or mezzanine** video/audio into a **code…

| Stage | Question | Wrong answer cost |
|-------|----------|-------------------|
| **Mezzanine** | Archive master quality? | Re-shoot / re-ingest impossible |
| **ABR ladder** | How many rungs? | CDN $ + rebuffer or waste |
| **Live** | CBR cap vs quality | Uplink drops, macroblocking |
| **DRM** | Encode clear or encrypted? | Re-package if keys rotate wrong |

- **Note:** **Encode once well** at mezzanine

## Technical Details
```txt
Camera / file ──► Encode (codec params) ──► Elementary streams
                           │
              ┌────────────┼────────────┐
         Live CBR      VoD CRF      HW NVENC
              │            │            │
         RTMP/SRT     ABR ladder    GPU fleet
```

### VoD mezzanine (quality master)

```bash
ffmpeg -i camera.mov -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a pcm_s24le -movflags +faststart mezzanine.mov
```

- Store mezzanine

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

- See [[NVENC]] for GPU fleet sizing.

### QC after encode

```bash
ffmpeg -i out.mp4 -vf signalstats -f null -
ffprobe -show_frames -select_streams v:0 -show_entries frame=pict_type -of csv | head
# Verify regular IDR at expected GOP
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Macroblocking live | Bitrate too low for motion | Raise `-b:v` or drop resolution |
| Audio drift over hours | `-re` vs wall clock skew | Hardware encoder timestamp; restart policy |
| Huge mezzanine | CRF too low / uncompressed audio | Adjust CRF; AAC or FLAC mezzanine |
| Keyframe every few frames | `-sc_threshold` default | Set `-sc_threshold 0` for streaming |
| 60fps stutter on 30fps ladder | Frame rate mismatch | Separate ladders or force `-r 30` |
| GPU encode banding | NVENC rate control | Tune CQ/VBR; increase `-b:v` floor |

- **Mistake:** **Encoding ≠ packaging**
- **Double encode quality loss** — OBS::** → RTMP → transcode → ladder = generational loss; minimize hops
- **Mistake:** **Interlaced source**
- **Color range** — TV vs PC levels wrong::** → crushed blacks; tag `-color_range tv`

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Remux only**
- **Con / skip when:** **Encode on every playback**
- **Con / skip when:** **Maximum compression on mezzanine**

## Comparison
- vs [[re-encoding]]: **Remux only**


### Use cases
- Used wherever Encoding sits in an ingest → package → CDN → player path
