[[commands]] [[ffmpeg]] [[codecs]] [[MPEG-TS]] [[Streaming]]

# ffprobe

> ffprobe reads media metadata — codecs, duration, timestamps, programs — without rewriting the file.

---

## How it works

```txt
file / UDP URL ──► ffprobe ──► streams, format, frames, programs
                      pts_time = when this sample should play
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`pts_time`** | Presentation time (seconds) | “When the player should show this frame/sample.” |
| **`start_time`** | Stream origin offset | “A/V sync bugs often start here.” |
| **`-show_streams`** | Per-stream codec props | “My first look at any mystery file.” |
| **`-of json`** | Machine output | “Scripts parse JSON, not the pretty banner.” |
| **`-select_streams v/a`** | Only video/audio | “Don’t dump every subtitle frame.” |

---


## Configuration and commands

```bash
ffprobe -hide_banner input.mp4
ffprobe -show_streams input.mp4
ffprobe -show_format -show_streams -of json input.mp4

# Frames (heavy)
ffprobe -show_frames -select_streams v -of json input.mp4

# Live / multicast programs
ffprobe -i udp://224.20.20.1:5003 -show_programs
ffprobe -v quiet -show_programs -of json udp://@224.20.20.1:5003
```

| Format | Flag | Best for |
|--------|------|----------|
| Human | (default) | Eyes |
| JSON | `-of json` | Scripts / APIs |
| CSV / flat / compact | `-of csv` / `flat` / `compact` | Quick shell |

```txt
Stream #0:0 Video: h264   start_time=0.000000
Stream #0:1 Audio: aac    start_time=0.000000
```

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| “Invalid data” on good player file | Truncated / wrong extension | Try `-f` format; check with another tool |
| Empty UDP probe | No packets / wrong group | tcpdump; iface; `@` vs host syntax |
| Huge JSON | `-show_frames` on long VOD | Sample with `-read_intervals` or limit |
| Script breaks on banner | stderr noise | `-v quiet` / `-v error` + `-of json` |
| Duration N/A | Live / incomplete mux | Use bitrate × size estimate or container trailers |

---


## Gotchas

> [!WARNING]
> **`-show_frames` can be enormous** — prefer streams/format unless debugging PTS gaps.

> [!WARNING]
> **Multicast needs network path** — ffprobe failing is often IGMP/routing, not “bad ffmpeg”.

> [!WARNING]
> **PTS vs DTS** — decode order ≠ display order on B-frames; use the field you mean.

---


## When not to use

- **Transcoding / streaming out** — [[ffmpeg]].
- **Only file size/name** — `stat` / [[Find command]].
- **DRM license introspection** — packager/DRM tools, not ffprobe.

---


## Related

[[ffmpeg]] [[MPEG-TS]] [[codecs]] [[Streaming]] [[commands]]

## Sources

- [Wikipedia — ffprobe](https://en.wikipedia.org/wiki/ffprobe)
