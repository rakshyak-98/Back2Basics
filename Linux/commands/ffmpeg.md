[[ffprobe]] [[codecs]] [[Streaming]] [[RTMP]] [[SRT]] [[RTSP]]

# ffmpeg

> ffmpeg builds a media pipeline — read inputs, transform (or copy), write outputs or streams.

```txt
        ffmpeg ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Media/ops: `-c copy` vs re-encode, `-re` for live pacing, `-map` for stream s…

## Sources
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html) — deep-dive
- [ffmpeg(1)](https://ffmpeg.org/ffmpeg.html) — deep-dive

## Key Concepts
- **`-i`:** Each input source.
- **`-c copy` / `-c:v` / `-c:a`:** Copy or re-encode per stream.
- **`-map`:** Explicit stream selection (don’t rely on defaults).
- **`-re`:** Read input at realtime — required for live-like feeds from files.
- **CRF / bitrate / preset:** Quality vs CPU vs size trade-offs.


- **Core:** Demux inputs → optionally decode/filter/encode → mux to a file or protocol. S…

## Technical Details
```txt
file / UDP / RTMP → demux → copy OR decode→filter→encode → mux → file / UDP / RTMP / HLS
```

```bash
ffprobe -hide_banner input.mp4
ffmpeg -i in.mp4 -c copy out.mkv
ffmpeg -i in.mp4 -an -c copy video_only.mp4
ffmpeg -i in.mp4 -vn -c copy audio_only.aac

ffmpeg -i in.mp4 -c:v libx264 -preset medium -crf 23 -c:a copy out.mp4
ffmpeg -i video.mp4 -itsoffset 0.5 -i audio.aac \
  -map 0:v -map 1:a -c copy out.mp4

ffmpeg -i udp://@224.20.20.1:5001 -c copy \
  -f segment -segment_time 600 -reset_timestamps 1 -strftime 1 \
  "5001_%Y%m%d_%H%M%S.ts"

ffmpeg -re -stream_loop -1 -i sample.mp4 -c copy -f mpegts \
  "udp://127.0.0.1:5000?pkt_size=1316"

ffmpeg -re -stream_loop -1 -i sample.mp4 \
  -c:v libx264 -preset veryfast -pix_fmt yuv420p \
  -c:a aac -ar 48000 -b:a 128k \
  -f flv "rtmp://127.0.0.1:1935/live/channel1"
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Instant “done”, not live | Missing `-re` | Add `-re` for live pacing |
| Stream dies at EOF | No loop | `-stream_loop -1` |
| Codec tag error on copy | Wrong muxer | Re-encode or change `-f` |
| A/V drift | Start times | `-itsoffset`; [[ffprobe]] |
| High CPU on “simple” job | Accidental encode | Prefer `-c copy` |

## Mistakes to Avoid
- **Mistake:** Omitting `-re` when feeding “live” from a file
- **Mistake:** Relying on default stream selection and dropping tracks
- **Mistake:** Treating UDP MPEG-TS as a reliable archive path

## Pros/Cons or Trade-offs
- **Pro:** Universal Swiss-army media tool; scriptable.
- **Con:** Flag combinatorics; accidental re-encode burns CPU; UDP drops packets.
- **Trade-off:** CRF for VOD quality vs constrained bitrate for live ABR.

## Comparison
- vs [[ffprobe]]: probe metadata only


### Use cases
- Remuxing camera footage, segmenting multicast MPEG-TS recordings, and simulat…
