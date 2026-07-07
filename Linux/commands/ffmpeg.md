[[re-encoding]] [[codecs]]

[documentation](https://ffmpeg.org/ffmpeg.html#Description)

`ffmpeg` -> Builds a [[transcoding]] pipeline out of the components listed below. The program’s operation then consists of input data chunks flowing from the sources down the pipes towards the [[sinks]], while being transformed by the components they encounter along the way.

### Public via MPEG-TS (if Flussonic is configured for TS ingest)

```bash
ffmpeg -re -stream_loop -1 -i /path/to/video.mp4 \
  -c:v libx264 -preset veryfast -pix_fmt yuv420p \
  -c:a aac \
  -f mpegts "udp://127.0.0.1:1234"
```

### Convert to source file to MPTS

```bash

ffmpeg -i input.mp4 -c copy -f mpegts output.ts;
# `-c copy` avoids re-encoding. 

```

```bash
ffmpeg -i input.mp4 -c:v libx264 -c:a aac -f mpegts output.ts
# If codecs are incompatible with TS (e.g., some audio formats), re-encode
```


### Publish a local file as a live stream

```bash
ffmpeg -re -stream-loop -1 -i /path/to/video.mp4 \
-c:v libx264 -preset veryfast -profile:v main -pix_fmt yuv420p \
-c:a aac -ar 48000 -b:a 128k \
-f flv "rtmp://127.0.0.1:1935/channel_test_1"
```
- `-re` real time pacing (important for live)
- `-stream_loop -1` loop forever (omit for one-shot play)
- `-f flv` required for `RTMP` 

## Goal

**Continuously stream a local video file over UDP to localhost port `5000` without re-encoding.**

Flow:

```text
sample-video-1hr.mp4
        ↓
FFmpeg
        ↓
MPEG-TS packets
        ↓
UDP
        ↓
127.0.0.1:5000
```

## Each option

### `ffmpeg`

Starts FFmpeg.

---

### `-stream_loop -1`

Loop input forever.

```bash
-stream_loop -1
```

- `0` → play once
    
- `1` → repeat 1 extra time
    
- `-1` → infinite loop
    

Without this, the stream stops when the file ends.

---

### `-re`

Read input at **real-time speed**.

Without:

```text
1 hour video
↓
FFmpeg sends as fast as CPU/disk allow
↓
maybe finishes in few minutes
```

With `-re`:

```text
1 second video data
↓
sent every 1 second
```

Useful for simulating a live source.

---

### `-i /home/mihir/Downloads/sample-video-1hr.mp4`

Input file.

```text
sample-video-1hr.mp4
```

becomes source media.

---

### `-c copy`

Copy codecs.

```bash
-c copy
```

No re-encoding.

Example:

```text
H264 video + AAC audio
↓
same H264 + AAC
```

Benefits:

- CPU usage ↓
    
- Faster
    
- No quality loss
    

---

### `-f mpegts`

Force output container format to **MPEG Transport Stream**.

```text
Video + Audio
↓
MPEG-TS packets
```

MPEG-TS is commonly used for:

- UDP streaming
    
- IPTV
    
- Broadcast systems
    

---

### `udp://127.0.0.1:5000`

Send output via UDP.

```text
127.0.0.1
```

= localhost (same machine)

```text
5000
```

= destination port

Anything listening on UDP port `5000` can receive it.

Example receiver:

```bash
ffplay udp://127.0.0.1:5000
```

or

```bash
vlc udp://@:5000
```

---

## Complete lifecycle

```text
sample-video-1hr.mp4
        ↓
read forever (-stream_loop -1)
        ↓
emit at real-time speed (-re)
        ↓
don't re-encode (-c copy)
        ↓
package into MPEG-TS (-f mpegts)
        ↓
send via UDP
        ↓
127.0.0.1:5000
```

## Real-world use cases

- Simulate a live TV channel
    
- Test video ingest pipelines
    
- Feed video into another FFmpeg process
    
- Test HLS/DASH transcoding servers
    
- Stream to VLC/ffplay/GStreamer applications
    

## Edge cases

- `-c copy` may fail if input codecs are incompatible with `mpegts`.
    
- Without `-re`, packets are sent too fast (not live behavior).
    
- UDP is **connectionless** → packets can be dropped.
    
- `127.0.0.1` means **only same machine** can receive. Use another IP (e.g. `192.168.x.x`) for other devices.

## Why `ffmpeg` for TC channels

- Generate 480p, 720p, 1080p, 4K from single input stream -> `ffmpeg` handles this in one pass with parallel encoding.
- For 1000 concurrent live channels across 5 bitrates, ffmpeg + media server (Flussonic) handles it efficiently.