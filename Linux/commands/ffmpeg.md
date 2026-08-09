[[re-encoding]] [[codecs]] [[transcoding]] [[ffprobe]] [[MPEG-TS]] [[Streaming]]

# ffmpeg

> ffmpeg builds a media pipeline — read inputs, transform (or copy), write outputs or streams.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Live / UDP / RTMP patterns]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** ffmpeg is a graph: inputs → demux → decode (optional) → filters/encode → mux → file or network.

```txt
file / UDP / RTMP
        ↓
   demux streams
        ↓
  copy  OR  decode → filter → encode
        ↓
   mux (mp4 / mpegts / flv …)
        ↓
   file / UDP / RTMP / HLS …
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **`-i`** | An input | “Every source is an `-i`.” |
| **`-c copy` / `-c:v` / `-c:a`** | Codec: copy or re-encode | “Copy is lossless and cheap; encode when format or quality must change.” |
| **`-map`** | Pick which streams leave | “Map video from 0, audio from 1 — don’t rely on defaults.” |
| **`-re`** | Read at realtime | “Without `-re`, a file dump is not a live source.” |
| **`-f`** | Force container/protocol | “`-f mpegts` / `-f flv` for UDP/RTMP ingest.” |
| **CRF / bitrate / preset** | Quality vs CPU vs size | “CRF for VOD quality; bitrate for live ABR ladders.” |

---

## Standard config / commands

```bash
# Inspect first (pair with [[ffprobe]])
ffprobe -hide_banner input.mp4

# Remux / stream copy (no quality loss)
ffmpeg -i in.mp4 -c copy out.mkv

# Strip streams
ffmpeg -i in.mp4 -an -c copy video_only.mp4
ffmpeg -i in.mp4 -vn -c copy audio_only.aac

# Re-encode video, keep audio
ffmpeg -i in.mp4 -c:v libx264 -preset medium -crf 23 -c:a copy out.mp4

# Mux video + audio (offset audio 0.5s)
ffmpeg -i video.mp4 -itsoffset 0.5 -i audio.aac \
  -map 0:v -map 1:a -c copy out.mp4

# Segmented recording from multicast (10 min chunks)
ffmpeg -i udp://@224.20.20.1:5001 -c copy \
  -f segment -segment_time 600 -reset_timestamps 1 -strftime 1 \
  "5001_%Y%m%d_%H%M%S.ts"
```

| Knob | Why it matters |
|------|----------------|
| `-c copy` | Fast path — fails if codecs incompatible with container |
| `-stream_loop -1` | Loop file forever (live sim) |
| `-re` | Pace like a live encoder |
| `-pix_fmt yuv420p` | Broad player compatibility |
| `pkt_size=1316` on UDP MPEG-TS | Fits common IPTV packet sizing |

### Batch inspect in tmux

```bash
tmux new-session -d -s ffmpeg
first=1
for file in *.mp4 *.mkv *.mov *.ts; do
  [ -e "$file" ] || continue
  if [ $first -eq 1 ]; then
    tmux rename-window -t ffmpeg:0 "$file"
    tmux send-keys -t ffmpeg:0 "ffprobe -hide_banner \"$file\"" C-m
    first=0
  else
    tmux new-window -t ffmpeg -n "$file" "ffprobe -hide_banner \"$file\""
  fi
done
tmux attach -t ffmpeg
```

---

## Live / UDP / RTMP patterns

```bash
# File → MPEG-TS over UDP (live pace, copy)
ffmpeg -re -stream_loop -1 -i sample.mp4 -c copy -f mpegts \
  "udp://127.0.0.1:5000?pkt_size=1316"

# File → RTMP (re-encode for FLV-friendly codecs)
ffmpeg -re -stream_loop -1 -i sample.mp4 \
  -c:v libx264 -preset veryfast -profile:v main -pix_fmt yuv420p \
  -c:a aac -ar 48000 -b:a 128k \
  -f flv "rtmp://127.0.0.1:1935/live/channel1"

# Multicast TS ingest sim
ffmpeg -re -stream_loop -1 -i 586000000.ts -c copy -f mpegts \
  "udp://239.1.1.3:10003?pkt_size=1316"
```

Receive: `ffplay udp://127.0.0.1:5000` or `vlc udp://@:5000`.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Instant “done”, not live | Missing `-re` | Add `-re` for live pacing |
| Stream dies at EOF | No loop | `-stream_loop -1` |
| `Could not find tag for codec` | Copy into wrong muxer | Re-encode (`-c:v libx264 -c:a aac`) or change `-f` |
| A/V drift after mux | Start times / offset | `-itsoffset`; check with [[ffprobe]] `start_time` |
| UDP receiver sees nothing | Wrong iface / multicast | Use correct group + iface; try unicast first |
| High CPU on “simple” job | Accidental re-encode | Prefer `-c copy` when possible |
| RTMP rejected | Codec/container | H.264 + AAC + `-f flv` |

---

## Gotchas

> [!WARNING]
> **`-c copy` is not magic** — container rules still apply. MPEG-TS hates some codecs; remux may force encode.

> [!WARNING]
> **`-re` only on *input*** — putting it wrong or omitting it turns VOD into a dump that floods buffers.

> [!WARNING]
> **UDP drops packets** — fine for lab ingest; not a reliable archive path. Record with TCP/file or add FEC/NACK at the protocol layer.

> [!WARNING]
> **Default stream selection** — without `-map`, ffmpeg may drop extra audio/subtitle tracks you cared about.

---

## When NOT to use

- **Browser P2P A/V** — [[WebRTC]] / [[ICE (Interactive Connectivity Establishment)]], not ffmpeg between browsers.
- **One-command packaging for OTT at scale** — use a packager/CDN pipeline ([[HLS]] / [[DASH]]); ffmpeg is the encoder/worker, not the origin CDN.
- **Just probe metadata** — use [[ffprobe]].

---

## Related

[[ffprobe]] [[transcoding]] [[codecs]] [[MPEG-TS]] [[Streaming]] [[ABR]] [[flussonic]]
