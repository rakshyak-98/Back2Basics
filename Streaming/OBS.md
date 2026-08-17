[[ingestion]] [[RTMP]] [[Encoding]] [[NVENC]] [[Single Stream]] [[network management]] [[transcoding]]

# OBS (Open Broadcaster Software)

> Desktop capture + encode + publish for live — **default RTMP publisher** for creators and ops smoke tests.

```txt
        OBS (Open Broadcas ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers ask about OBS to see if you understand the pipeline role, failur…

## Sources
- [Wikipedia — OBS](https://en.wikipedia.org/wiki/OBS) — overview

## Key Concepts
- **Note:** **OBS** composes **scenes** (camera, display, browser, images), **encodes** i…

| Output          | Typical setting       | Pitfall                            |
| --------------- | --------------------- | ---------------------------------- |
| **Stream**      | RTMP CBR 4500 Kbps    | Wi-Fi uplink underrun              |
| **Record**      | MKV + separate tracks | Not a delivery format — re-package |
| **Virtual cam** | Zoom/Meet             | Different path than RTMP ingest    |

## Technical Details
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

- If ffmpeg works but OBS fails → OBS service URL or key typo.

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

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| "Failed to connect" | Server URL, firewall 1935/443 | RTMPS port; no extra path in key field |
| Dropped frames (encoding) | OBS stats panel red | NVENC; lower resolution; close browser sources |
| Dropped frames (network) | Yellow network box | Wired Ethernet; lower bitrate |
| Desync audio/video | Wrong sample rate; Bluetooth mic | 48 kHz; wired mic; restart capture |
| Black screen on stream | Wrong scene; source crashed | Preview vs Program; restart source |
| Pixelated fast motion | Bitrate too low | +1000 Kbps or drop to 720p |
| Stream OK, record corrupt | Disk full | MKV recoverable vs MP4 |

- **Mistake:** **Stream key in screenshot**
- **CBR off (VBR in OBS)** — uplink spikes::** → ingest buffer → added latency
- **Mistake:** **Keyframe 0 (= auto)**
- **Mistake:** **Browser source @ 60fps on 30fps output**
- **Mistake:** **OBS ≠ production transcoder**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **24/7 unattended headless channel**
- **Con / skip when:** **Multi-bitrate direct to players**
- **Con / skip when:** **Studio DRM**

## Comparison
- vs [[DRM]]: **Studio DRM** — encrypt at origin/packager ([[DRM]]), not in OBS.


### Use cases
- Used wherever OBS sits in an ingest → package → CDN → player path
