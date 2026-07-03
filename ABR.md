Adaptive Bit Rate -> A streaming technique where the video quality automatically changes based on the viewer's current network speed, device capability, and buffer state.

Goal -> Avoid buffering and Maintain smooth playback.

### Adaptive Bitrate  (ABR) Logic
Source video is encoded into a ladder of resolutions and bitrates (e.g., `1080p60/8Mbps`, `720p30/3Mbps`, `480p30/1.5Mbps`). The manifest file (HLS or DASH) acts as the [[Orchestration layer]] for the client.