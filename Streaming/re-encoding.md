[[transcoding]] [[Encoding]] [[codecs]] [[CMAF]] [[HLS]] [[DASH]] [[CRF (Constant Rate Factor)]] [[NVENC]] [[bitrate streaming]]

# Re-encoding

> Decode compressed media → encode again — **generational loss + CPU cost**; avoid when remux suffices.

## Interview Relevance

Interviewers ask about Re-encoding to see if you understand the pipeline role, failure modes, and trade-offs — not just the acronym.

## Sources

- [Wikipedia — re-encoding](https://en.wikipedia.org/wiki/re-encoding) — overview

## Key Concepts

**Re-encoding** (transcode) **decodes** a compressed stream to raw samples/frames, then **encodes** with a (usually) new codec, bitrate, or resolution. Each generation **loses information** — avoid unnecessary hops in the pipeline. **Remux** (`-c copy`) only changes container when codecs already match targets.

| Trigger | Action | Example |
|---------|--------|---------|
| Codec mismatch | Re-encode | ProRes mezzanine → H.264 ABR |
| Bitrate/resolution change | Re-encode | 4K master → 720p rung |
| Container only | Remux copy | TS → fMP4 same codec |
| Broadcast compliance | Re-encode CBR | VoD VBR → live CBR |

See [[transcoding]] for ladder workflow; this note focuses on **when and how** to re-encode safely.

## Technical Details

```txt
Source H.265 ──► decode ──► raw YUV ──► encode H.264 ──► [[HLS]] ladder
     │
  LOSSY (cannot undo)

Source H.264 in MKV ──► copy ──► H.264 in fMP4   (NOT re-encode — remux)
```

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

## Real-World Applications

Used wherever Re-encoding sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs

- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Codec already matches** — remux to [[CMAF]]/[[HLS]]/[[DASH]] with `-c copy`.
- **Con / skip when:** **Quality-critical archive** — store mezzanine; re-encode only derivatives.
- **Con / skip when:** **Real-time when copy works** — ingest `-c copy` to packager saves GPU.

## Comparison

- vs [[CMAF]]: **Codec already matches** — remux to [[CMAF]]/[[HLS]]/[[DASH]] with `-c copy`.

## Mistakes to Avoid

| Symptom | Check | Fix |
|---------|-------|-----|
| Worse quality than source | CRF too high; double encode | Lower CRF; encode from mezzanine once |
| Audio shorter than video | Async filter graph | `-async 1`; `-shortest` intentionally or not |
| Wrong colors | Range/metadata lost | `-color_range tv -colorspace bt709`
| Huge output | CRF too low / no maxrate | [[CRF (Constant Rate Factor)]] + cap |
| ABR switch broken | GOP not fixed | `-g` + `-sc_threshold 0` |
| GPU slower than CPU | PCIe / decode on CPU | `-hwaccel cuda` full pipeline |

- **OBS stream → re-encode → ladder** — two lossy passes; record mezzanine separately for VoD.
- **`-c:v copy` into wrong container** — H.265 in TS may fail on old STBs; probe target devices.
- **Upscaling low source** — re-encoding 480p to 1080p doesn't add detail; wastes bits.
- **Subtitle burn-in vs soft subs** — re-encode required for burn-in; soft subs can remux.
