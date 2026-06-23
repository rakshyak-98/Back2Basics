```bash
ffmpeg -re -i /home/mihir/Downloads/sample-video-1hr.mp4 -c copy -f mpegts udp://127.0.0.1:5000

ffplay http://localhost/stream1/index.m3u8
```

Stream in loop `-1` look infinit

```bash
ffmpeg -stream_loop -1 -re -i /home/mihir/Downloads/sample-video-1hr.mp4 -c copy -f mpegts udp://127.0.0.1:5000
```

