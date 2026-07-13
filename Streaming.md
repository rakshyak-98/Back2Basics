[[ingestion]]

```bash
ffmpeg -re -i /home/mihir/Downloads/sample-video-1hr.mp4 -c copy -f mpegts udp://127.0.0.1:5000

ffplay http://localhost/stream1/index.m3u8
```

Stream in loop 

```bash
ffmpeg -stream_loop -1 -re -i /home/mihir/Downloads/sample-video-1hr.mp4 -c copy -f mpegts udp://127.0.0.1:5000
```

Video ingestion -> the process of accepting a video stream or video file into a video processing system so it can be processed, stored, transcoded, analyzed or delivered.
- **Input:** Live streams or uploaded files.
- Output: Validated, buffered video ready for downstream processing.

The platform that publishes/sends the video to the ingestion server is generally called the video source, publisher or encoder, depending on context.

Broadcasting -> sending the same audio/video/data from one source to multiple receivers simultaneously.
- Broadcasting is the process of transmitting content from one publisher to many viewers.
- one stream is distributed to many viewers.

> DRM (Digital Right Management) -> fits after ingestion and transcoding, but before playback by viewers.

Its purpose is not to transport video. It protects the video so only authorized users can watch it.

Playback -> the process of reading, decoding, and presenting media (video/audio) to the user.
- Everything before playback prepare the video. Playback is when the viewer actually watches it.


### Video Audio multiplexing (muxing)
is the process of combining separate video, audio, and metadata streams into a single container format for storage or transmission, while **preserving timing synchronization between them**.

How it words:
- Video and audio are encoded independently (e.g., H.264 for video, AAC for audio), producing separate elementary streams.
- The multiplexer interleaves packets from each stream into a single output, using timestamps (PTS/DTS) to maintain sync.
- The receiving player demultiplexes (demuxes) the container back into separate streams for decoding and playback.

Common container formats (muxers):
- MPEG-TS -> packetizes into fixed 188-byte units for broadcast/live streaming
- MP4/fMP4 -> used for HLS/DASH segemnts and progressive download
- FLV -> used with RTMP
- MKV -> general-purpose, supports multiple tracks/subtitiles

```bash
ffmpeg -i video.h264 -i audio.acc -c copy -f mp4 output.mp4
```