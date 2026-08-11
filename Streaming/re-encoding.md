[[transcoding]] [[Encoding]] [[codecs]] [[CMAF]] [[HLS]] [[DASH]]

# Re-encoding

> Decode compressed media → encode again — **generational loss + CPU cost**; avoid when remux suffices.

---

## Mental model

**Re-encoding** (transcode) **decodes** a compressed stream to raw samples/frames, then **encodes** with a (usually) new codec, bitrate, or resolution. Each generation **loses information** — avoid unnecessary hops in the pipeline. **Remux** (`-c copy`) only changes container when codecs already match targets.

```txt
Source H.265 ──► decode ──► raw YUV ──► encode H.264 ──► [[HLS]] ladder
     │
  LOSSY (cannot undo)

Source H.264 in MKV ──► copy ──► H.264 in fMP4   (NOT re-encode — remux)
```

| Trigger | Action | Example |
|---------|--------|---------|
| Codec mismatch | Re-encode | ProRes mezzanine → H.264 ABR |
| Bitrate/resolution change | Re-encode | 4K master → 720p rung |
| Container only | Remux copy | TS → fMP4 same codec |
| Broadcast compliance | Re-encode CBR | VoD VBR → live CBR |

See [[transcoding]] for ladder workflow; this note focuses on **when and how** to re-encode safely.

---

## Standard config / commands

### Remux first (try before re-encode)

```bash
ffmpeg -i input.mkv -c copy -movflags +faststart output.mp4
ffprobe -show_streams output.mp4   # verify codec compatible with target player
```

### Standard H.264 + AAC for HLS/fMP4 delivery

```bash
ffmpeg -i input.mp4 -c:v libx264 -preset medium -crf 22 \
  -maxrate 4500k -bufsize 9000k -g 60 -sc_threshold 0 \
  -pix_fmt yuv420p -c:a aac -profile:a aac_low -b:a 128k -ar 48000 \
  -movflags +faststart output.mp4
```

### Scale + re-encode ladder rung

```bash
ffmpeg -i mezzanine.mov -vf "scale=-2:720" -c:v libx264 -crf 22 -maxrate 3000k \
  -bufsize 6000k -g 60 -sc_threshold 0 -c:a aac -b:a 128k 720p.mp4
```

### Hardware re-encode

```bash
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc -preset p4 -b:v 4500k \
  -g 60 -c:a aac -b:a 128k output.mp4
```

See [[NVENC]].

### Batch VoD farm pattern

```txt
SQS job → probe (ffprobe) → decide copy vs re-encode
  if codec in {h264,aac} and resolution OK → package only [[CMAF]]
  else → single mezzanine-aware re-encode (not chain)
```

### QC after re-encode

```bash
ffmpeg -i output.mp4 -af volumedetect -f null -
ffmpeg -i output.mp4 -vf signalstats -f null -
# Compare duration — drift signals sync bug
ffprobe -show_entries format=duration -of csv=p=0 input.mp4 output.mp4
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Worse quality than source | CRF too high; double encode | Lower CRF; encode from mezzanine once |
| Audio shorter than video | Async filter graph | `-async 1`; `-shortest` intentionally or not |
| Wrong colors | Range/metadata lost | `-color_range tv -colorspace bt709`
| Huge output | CRF too low / no maxrate | [[CRF (Constant Rate Factor)]] + cap |
| ABR switch broken | GOP not fixed | `-g` + `-sc_threshold 0` |
| GPU slower than CPU | PCIe / decode on CPU | `-hwaccel cuda` full pipeline |

---

## Gotchas

> [!WARNING]
> **OBS stream → re-encode → ladder** — two lossy passes; record mezzanine separately for VoD.

> [!WARNING]
> **`-c:v copy` into wrong container** — H.265 in TS may fail on old STBs; probe target devices.

> [!WARNING]
> **Upscaling low source** — re-encoding 480p to 1080p doesn't add detail; wastes bits.

> [!WARNING]
> **Subtitle burn-in vs soft subs** — re-encode required for burn-in; soft subs can remux.

---

## When NOT to use

- **Codec already matches** — remux to [[CMAF]]/[[HLS]]/[[DASH]] with `-c copy`.
- **Quality-critical archive** — store mezzanine; re-encode only derivatives.
- **Real-time when copy works** — ingest `-c copy` to packager saves GPU.

---

## Related

[[transcoding]] [[Encoding]] [[codecs]] [[CRF (Constant Rate Factor)]] [[NVENC]] [[CMAF]] [[bitrate streaming]]
