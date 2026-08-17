[[Streaming]] [[MPEG-TS]] [[CMAF]] [[Byte stream]] [[file descriptors]] [[Manifest (streaming)]] [[ingestion]] [[HLS]] [[DASH]]

# Byte stream

> Byte stream — encoder ──► byte stream (TCP/file) ──► demuxer reads framing

```txt
        Byte stream ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Byte stream to see if you understand the pipeline role…

## Sources
- [Wikipedia — Byte stream](https://en.wikipedia.org/wiki/Byte_stream) — overview

## Key Concepts
- **Note:** A **byte stream** is an **ordered, undelimited flow of bytes** with no built-…

| Layer | Example | Boundary model |
|-------|---------|----------------|
| Transport | TCP, TLS | Continuous bytes |
| Container | fMP4, MPEG-TS | Boxes / 188-byte TS packets |
| Packaging | HLS segment, DASH Segment | HTTP object = N seconds of container |
| Application | Manifest (`.m3u8`, MPD) | Lists URL + byte-range or whole file |

- **Note:** **Progressive download** (single MP4 over HTTP) is a byte stream with a `moov…

## Technical Details
```txt
Encoder ──► byte stream (TCP/file) ──► demuxer reads framing
              │                              │
         no record boundaries          finds boxes / TS packets / fMP4 moof
              │                              │
         CDN caches by URL            player seeks by manifest index
```

### Read / inspect byte stream boundaries

```bash
# First bytes — identify container magic
xxd -l 16 segment.m4s
# fMP4 often starts with size + 'ftyp' or 'moof'

# TS sync byte check (0x47 every 188 bytes)
xxd segment.ts | head
ffprobe -show_format -show_streams segment.m4s

# HTTP byte-range (DASH template / progressive)
curl -I "https://cdn.example.com/video.mp4"
curl -r 0-1023 -o head.bin "https://cdn.example.com/video.mp4"
```

### ffmpeg — emit framed segments from continuous input

```bash
# UDP MPEG-TS byte stream → segmented HLS files (discrete HTTP objects)
ffmpeg -i udp://239.0.0.1:1234 -c copy -f hls -hls_time 4 -hls_list_size 6 out.m3u8

# stdin pipe byte stream (no seek) — live only
cat input.ts | ffmpeg -i pipe:0 -c copy -f mpegts pipe:1
```

### nginx/CDN — cache keyed on full object

```nginx
# Each .m4s / .ts is one cache key — not byte-range inside unless configured
proxy_cache_key "$scheme$request_method$host$request_uri";
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Player can't start | `moov` at end of MP4 | `ffmpeg -movflags +faststart` or use fMP4 HLS |
| Corrupt TS | Lost sync byte 0x47 | Resync demuxer; check UDP packet loss |
| Seek broken in VoD | No index in progressive file | Fragment to HLS/DASH or fix `moov` placement |
| CDN serves stale partial | Byte-range cache misconfig | Cache full segments; align with [[CMAF]] chunk boundaries |
| Pipe stall | Blocking read on empty stdin | Buffer in ingest; timeout watchdog ([[ingestion]]) |
| moof sequence gap | Packager crash mid-segment | Drop bad segment; roll `#EXT-X-MEDIA-SEQUENCE` |

- **Mistake:** **Treating TCP stream as messages**
- **Mistake:** **Byte-range without Content-Range**
- **Mistake:** **Appending to open file**
- **Mistake:** **Endianness in container boxes**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Message-oriented control**
- **Con / skip when:** **Exactly-once business events**
- **Con / skip when:** **Small configuration blobs**

## Real-World Applications
- **Scenario:** Used wherever Byte stream sits in an ingest → package → CDN → player path
