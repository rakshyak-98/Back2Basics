[[ingestion]] [[RTMP]] [[Encoding]] [[NVENC]] [[Single Stream]]

# OBS (Open Broadcaster Software)

> Desktop capture + encode + publish for live — **default RTMP publisher** for creators and ops smoke tests.

---

## Mental model

**OBS** composes **scenes** (camera, display, browser, images), **encodes** in real time, and **publishes** via **[[RTMP]]** (or RTMPS) to an **ingest** endpoint, or **records** locally. It is a **single-publisher client** — not a CDN, packager, or DRM layer. Production stacks receive OBS at **[[ingestion]]**, then transcode/package to **[[HLS]]/[[DASH]]**.

```txt
Sources (mic, cam, display)
        │
   Scene compositor
        │
   Encoder (x264 / [[NVENC]] / QuickSync)
        │
   ┌────┴────┐
 RTMP push   Local MKV/MP4 record
   │
 ingest server → ABR ladder → viewers
```

| Output          | Typical setting       | Pitfall                            |
| --------------- | --------------------- | ---------------------------------- |
| **Stream**      | RTMP CBR 4500 Kbps    | Wi-Fi uplink underrun              |
| **Record**      | MKV + separate tracks | Not a delivery format — re-package |
| **Virtual cam** | Zoom/Meet             | Different path than RTMP ingest    |

---

## Standard config / commands

### Standard live publish setup

```txt
Settings → Stream
  Service: Custom
  Server:  rtmps://ingest.example.com/live   (or rtmp://)
  Stream Key: <secret from ops dashboard>

Settings → Output → Streaming
  Encoder: NVIDIA NVENC H.264 (see [[NVENC]]) or x264
  Rate Control: CBR
  Bitrate: 3500–6000 Kbps (1080p30) — match uplink headroom
  Keyframe Interval: 2 s  (must match segment duration)
  Preset: P4/P5 (NVENC) or veryfast/superfast (x264)

Settings → Audio
  Sample Rate: 48 kHz
  Bitrate: 160–192 kbps AAC (OBS encodes audio in RTMP mux)
```

### Recommended 1080p30 starting point

```txt
Output (scaled)   1920×1080 or 1280×720 if uplink < 5 Mbps
FPS               30 (match content; don't upsample)
Video bitrate     4500 Kbps CBR
Audio             AAC 160 kbps
Keyframe          2 s
Profile           high (H.264)
```

### RTMPS / auth failures — test outside OBS

```bash
ffmpeg -re -f lavfi -i testsrc=size=1280x720:rate=30 \
  -c:v libx264 -b:v 2500k -g 60 -c:a aac -f flv \
  "rtmp://ingest.example.com/live/STREAM_KEY"
```

If ffmpeg works but OBS fails → OBS service URL or key typo.

### Recording for later ladder (better quality than stream)

```txt
Settings → Output → Recording
  Format: mkv (crash-safe) → remux to mp4
  Encoder: same or higher quality than stream
  Use recording as mezzanine for [[transcoding]], not stream VOD
```

### Logs

```txt
Help → Log Files → View Current Log
Search: "rtmp", "error", "disconnect"
Linux: ~/.config/obs-studio/logs/
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| "Failed to connect" | Server URL, firewall 1935/443 | RTMPS port; no extra path in key field |
| Dropped frames (encoding) | OBS stats panel red | NVENC; lower resolution; close browser sources |
| Dropped frames (network) | Yellow network box | Wired Ethernet; lower bitrate |
| Desync audio/video | Wrong sample rate; Bluetooth mic | 48 kHz; wired mic; restart capture |
| Black screen on stream | Wrong scene; source crashed | Preview vs Program; restart source |
| Pixelated fast motion | Bitrate too low | +1000 Kbps or drop to 720p |
| Stream OK, record corrupt | Disk full | MKV recoverable vs MP4 |

---

## Gotchas

> [!WARNING]
> **Stream key in screenshot** — rotate key if leaked; use OBS secret field only.

> [!WARNING]
> **CBR off (VBR in OBS)** — uplink spikes → ingest buffer → added latency.

> [!WARNING]
> **Keyframe 0 (= auto)** — may not align with 2s HLS segments; set **2 s explicitly**.

> [!WARNING]
> **Browser source @ 60fps on 30fps output** — wasted CPU; match canvas FPS.

> [!WARNING]
> **OBS ≠ production transcoder** — one bitrate to ingest; ABR happens downstream ([[Multi Stream]] ladder).

---

## When NOT to use

- **24/7 unattended headless channel** — use ffmpeg/GStreamer on server with watchdog.
- **Multi-bitrate direct to players** — OBS sends one RTMP; packager creates ladder.
- **Studio DRM** — encrypt at origin/packager ([[DRM]]), not in OBS.

---

## Related

[[ingestion]] [[RTMP]] [[Encoding]] [[NVENC]] [[Single Stream]] [[network management]] [[transcoding]]
