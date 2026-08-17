[[HLS]] [[DASH]] [[MPD]] [[ABR]] [[CMAF]] [[Manifest (streaming)]] [[bitrate streaming]] [[DRM]] [[streaming manifest file]]

# Manifest (streaming)

> Manifest (streaming) — a streaming manifest is metadata listing segment URLs, bitrates, codecs, encryption, and timing. The player downloads it first, then pulls media segments over HTTP. ABR

```txt
        Manifest (streamin ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers ask about Manifest to see if you understand the pipeline role, f…

## Sources
- [Wikipedia — Manifest](https://en.wikipedia.org/wiki/Manifest) — overview

## Key Concepts
- **Note:** A **streaming manifest** is **metadata** listing segment URLs, bitrates, code…

| Format | Files | Spec |
|--------|-------|------|
| **HLS** | `.m3u8` master + media | Apple HLS RFC 8216 |
| **DASH** | `.mpd` | ISO 23009-1 — see [[MPD]] |
| **Smooth / MSS** | Legacy | Avoid greenfield |

- **Note:** **Master** manifest lists renditions

## Technical Details
```txt
Player boot
    │
    ├─ HLS: master.m3u8 ──► media playlist ──► .m4s / .ts segments
    │
    └─ DASH: manifest.mpd ──► SegmentTemplate ──► same segments ([[CMAF]])

Manifest refresh (live): poll interval ≈ segment duration / 2
```

### HLS master (multi-bitrate)

```plaintext
#EXTM3U
#EXT-X-VERSION:7
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="aud",NAME="main",DEFAULT=YES,URI="audio.m3u8"
#EXT-X-STREAM-INF:BANDWIDTH=5932800,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2",AUDIO="aud"
1080p.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=3128000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2",AUDIO="aud"
720p.m3u8
```

### HLS live media playlist

```plaintext
#EXTM3U
#EXT-X-VERSION:7
#EXT-X-TARGETDURATION:6
#EXT-X-MEDIA-SEQUENCE:1042
#EXTINF:6.000,
seg_1042.m4s
#EXTINF:6.000,
seg_1043.m4s
```

### Signed URL pattern (CDN)

```txt
https://cdn.example.com/live/720p.m3u8?token=HMAC&exp=1730000000
Same token policy on .m4s — player follows relative URLs
```

### Cache-Control guidance

```txt
Live master.m3u8     Cache-Control: max-age=1, must-revalidate
Live media.m3u8      max-age=0 or short (segment duration / 3)
VoD master           max-age=3600+
VoD segments         immutable, long max-age (hash in path)
```

### Validate manifests

```bash
curl -s "https://origin/master.m3u8" | grep EXT-X
# Apple mediastreamvalidator (macOS) for HLS compliance
xmllint --noout manifest.mpd   # DASH MPD well-formed
```

### Packager output

```bash
ffmpeg -i in.mp4 -c copy -f hls -hls_time 4 -hls_list_size 0 -master_pl_name master.m3u8 stream.m3u8
```

- For dual [[HLS]]/[[DASH]], generate **one segment set** — [[CMAF]].

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| 403 on segments, manifest OK | Token not propagated to child URLs | Relative paths; CDN signed cookie |
| Stuck on old live edge | CDN caching manifest | Lower TTL; `#EXT-X-SKIP` / correct `MEDIA-SEQUENCE` |
| Player won't start VoD | `#EXT-X-ENDLIST` missing | Add ENDLIST for VoD event playlists |
| ABR stuck low | Inflated BANDWIDTH | Recalculate video+audio+overhead ([[bitrate streaming]]) |
| CODECS mismatch | ffprobe vs manifest | Regenerate master from actual encode |
| DRM fail | `#EXT-X-KEY` / ContentProtection | Align with [[DRM]] / [[EME]] |
| Infinite manifest poll storm | `#EXT-X-TARGETDURATION` too low | Match max segment duration |

- **Mistake:** **Stale `MEDIA-SEQUENCE` after packager restart**
- **Mistake:** **Absolute vs relative URLs**
- **Mistake:** **Master without `INDEPENDENT-SEGMENTS`**
- **Mistake:** **LL-HLS partial tags on non-LL players**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Progressive MP4 only**
- **Con / skip when:** **WebRTC playback** — SDP + ICE, not HLS/DASH manifests.
- **Con / skip when:** **Embedding segment list in application**

## Real-World Applications
- **Scenario:** Used wherever Manifest sits in an ingest → package → CDN → player path
