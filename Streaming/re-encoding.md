Re-encoding is decoding a compressed stream to raw samples, then encoding it again with a codec. It's needed when the source codec is incompatible with the target container or delivery requirement, or when bitrate/resolution must change.

```bash

ffmpeg -i input.mp4 -c:v libx264 -c:a aac -f mpegts output.ts
# `-c:v libx264`: encodes video with H.264
# `-c:a aac`: encodes audio with AAC

```