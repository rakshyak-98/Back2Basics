Adaptive Bit Rate -> A streaming technique where the video quality automatically changes based on the viewer's current network speed, device capability, and buffer state.

Goal -> Avoid buffering and Maintain smooth playback.

### Adaptive Bitrate  (ABR) Logic

Source video is encoded into a ladder of resolutions and bitrates (e.g., `1080p60/8Mbps`, `720p30/3Mbps`, `480p30/1.5Mbps`). The manifest file (HLS or DASH) acts as the [[Orchestration layer]] for the client.

```plaintext
#EXT-X-STREAM-INF:BANDWIDTH=8000000,RESOLUTION=1920x1080
chunklist_1080p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720
chunklist_720p.m3u8
```

- Serialization/Deserialization Cost -> high during initial ingest (multi-pass encoding required); optimized for client-side selection algorithms (e.g., BOLA or PANDA).
- Storage Layout -> CDN edge caches must store all renditions. Segment alignment (GOP alignment) is mandatory for seamless bitrate switching without frame-buffering.

### Multi-Ingest (Broadcast Replication)

Simultaneous push to multiple CDNs or platforms.
- implementation: Usually handled via software encoders (`ffmpeg/GStreamer`) or specialized hardware encoders performing local replication to avoid per-stream upstream bandwidth saturation.
- Command Example (`ffmpeg replication`).

```bash
ffmpg -i <input source> -c:v copy -f flv rtmp://cdn1/live/key -c:v copy -f flv rtmp://cdn2/live/key
```