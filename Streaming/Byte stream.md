[[Streaming]] [[MPEG-TS]] [[CMAF]] [[Byte stream]] [[file descriptors]]

# Byte stream

> Ordered sequence of bytes as the transport primitive for media — **Unix I/O + container framing**, not a protocol.

---

## Mental model

A **byte stream** is an **ordered, undelimited flow of bytes** with no built-in message boundaries. TCP, pipes, and file reads all expose byte streams; **containers** (MP4, MPEG-TS, CMAF) impose structure on top. Streaming engineers care because players, packagers, and CDNs must agree on **where segment boundaries fall** in that stream.

```txt
Encoder ──► byte stream (TCP/file) ──► demuxer reads framing
              │                              │
         no record boundaries          finds boxes / TS packets / fMP4 moof
              │                              │
         CDN caches by URL            player seeks by manifest index
```

| Layer | Example | Boundary model |
|-------|---------|----------------|
| Transport | TCP, TLS | Continuous bytes |
| Container | fMP4, MPEG-TS | Boxes / 188-byte TS packets |
| Packaging | HLS segment, DASH Segment | HTTP object = N seconds of container |
| Application | Manifest (`.m3u8`, MPD) | Lists URL + byte-range or whole file |

**Progressive download** (single MP4 over HTTP) is a byte stream with a `moov` atom at the front or end — player needs index before seek works. **ABR streaming** splits the byte stream into **addressable HTTP objects** listed in [[Manifest (streaming)]].

---

## Standard config / commands

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

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Player can't start | `moov` at end of MP4 | `ffmpeg -movflags +faststart` or use fMP4 HLS |
| Corrupt TS | Lost sync byte 0x47 | Resync demuxer; check UDP packet loss |
| Seek broken in VoD | No index in progressive file | Fragment to HLS/DASH or fix `moov` placement |
| CDN serves stale partial | Byte-range cache misconfig | Cache full segments; align with [[CMAF]] chunk boundaries |
| Pipe stall | Blocking read on empty stdin | Buffer in ingest; timeout watchdog ([[ingestion]]) |
| moof sequence gap | Packager crash mid-segment | Drop bad segment; roll `#EXT-X-MEDIA-SEQUENCE` |

---

## Gotchas

> [!WARNING]
> **Treating TCP stream as messages** — RTMP/SRT/WebRTC add framing; raw TCP needs application protocol.

> [!WARNING]
> **Byte-range without Content-Range** — DASH players fail range requests; origin must honor RFC 7233.

> [!WARNING]
> **Appending to open file** — live HLS writes growing playlist + closed segment files; don't serve incomplete `.m4s` without LL-HLS partials.

> [!WARNING]
> **Endianness in container boxes** — binary parse errors look like "random corruption"; use `ffprobe`, not hex guessing.

---

## When NOT to use

- **Message-oriented control** — use JSON/gRPC for API; byte streams for media payload only.
- **Exactly-once business events** — use queues/DB; byte streams have no ack semantics at media layer.
- **Small config blobs** — object storage + HTTP GET beats custom streaming parsers.

---

## Related

[[Streaming]] [[MPEG-TS]] [[CMAF]] [[Manifest (streaming)]] [[ingestion]] [[HLS]] [[DASH]]
