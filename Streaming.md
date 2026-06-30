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

DRM (Digital Right Management) -> fits after ingestion and transcoding, but before playback by viewers.

Its purpose is not to transport video. It protects the video so only authorized users can watch it.

Playback -> the process of reading, decoding, and presenting media (video/audio) to the user.
- Everything before playback prepare the video. Playback is when the viewer actually watches it.

Encoding 