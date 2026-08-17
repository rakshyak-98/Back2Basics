[[Commands]] [[ffmpeg]] [[codecs]] [[Streaming]]

# ffprobe

> ffprobe reads media metadata — codecs, duration, timestamps, programs — without rewriting the file.





## Interview Relevance
Media ops: streams vs format, `pts_time`/`start_time` for A/V sync, and JSON output for scripts (`-of json`).

## Sources
- [ffprobe Documentation](https://ffmpeg.org/ffprobe.html) — deep-dive
- [FFmpeg Protocols](https://ffmpeg.org/ffmpeg-protocols.html) — overview

## Core Definition
ffprobe demuxes enough of a file or URL to report stream codecs, format container info, programs (MPEG-TS), and optionally frames. It does not transcode — that is [[ffmpeg]].

## Key Concepts
- **`pts_time`:** Presentation time in seconds — when to show the sample.
- **`start_time`:** Stream origin offset — common A/V sync clue.
- **`-show_streams` / `-show_format`:** Per-stream vs container summary.
- **`-of json`:** Machine-readable for automation.
- **`-select_streams`:** Limit to video/audio; avoid dumping every frame.

## Technical Details
```bash
ffprobe -hide_banner input.mp4
ffprobe -show_streams input.mp4
ffprobe -show_format -show_streams -of json input.mp4

ffprobe -show_frames -select_streams v -of json input.mp4

ffprobe -i udp://224.20.20.1:5003 -show_programs
ffprobe -v quiet -show_programs -of json udp://@224.20.20.1:5003
```

| Format | Flag | Best for |
|--------|------|----------|
| Human | (default) | Eyes |
| JSON | `-of json` | Scripts |
| CSV / flat / compact | `-of csv` / `flat` / `compact` | Quick shell |

| Symptom | Check | Fix |
|---------|-------|-----|
| Invalid data on playable file | Truncation / wrong ext | Force `-f`; try another tool |
| Empty UDP probe | No packets / wrong group | tcpdump; iface; `@` syntax |
| Huge JSON | `-show_frames` on long VOD | `-read_intervals`; limit streams |
| Script breaks on banner | stderr noise | `-v quiet` + `-of json` |

## Real-World Applications
Pre-flight checks before ffmpeg remux, diagnosing A/V start_time skew, and listing MPEG-TS programs on a multicast URL.

## Pros/Cons or Trade-offs
- **Pro:** Fast metadata without rewriting media.
- **Con:** Frame dumps are enormous; live/UDP failures are often network not codec.
- **Trade-off:** Human banner vs JSON for CI.

## Comparison
vs [[ffmpeg]]: transform/stream out. vs `stat`: file size/name only. vs DRM tools: licenses are out of scope.

## Mistakes to Avoid
- Dumping all frames on long VOD by default.
- Confusing PTS (display) with DTS (decode) on B-frames.
- Blaming ffprobe when multicast IGMP/routing is broken.
