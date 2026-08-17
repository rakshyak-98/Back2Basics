[[Streaming]] [[ABR]] [[bitrate streaming]] [[HLS]] [[DASH]] [[transcoding]] [[Encoding]] [[NVENC]] [[codecs]] [[Manifest (streaming)]]

# rendition

> A rendition is one encoded quality of the same source — resolution, bitrate, or codec — so ABR can switch without stopping.





## Interview Relevance
Interviewers probe whether you can walk rendition end-to-end — not just name it. Signal fluency with **Rendition**, **Ladder**, **Variant stream**, **Representation** and when you would pick a different path.

## Sources
- [Wikipedia — rendition](https://en.wikipedia.org/wiki/rendition) — overview

## Key Concepts
- **Rendition:** One quality variant — “A rendition is one rung on the ABR ladder.”
- **Ladder:** Ordered set of renditions — “We design the ladder for devices and bandwidth.”
- **Variant stream:** HLS name for a video rung — “EXT-X-STREAM-INF points at a variant playlist.”
- **Representation:** DASH name for a rung — “In DASH, a Representation is the rendition.”
- **Audio rendition:** Separate audio encode/playlist — “Audio can be its own rendition group.”
- **Encode session:** GPU/CPU job per output — “N renditions means N concurrent encodes.”

### Capacity math (say the number)

[!NOTE]
Encode load **multiplies**: 300 channels × 3 video renditions ≈ **900** concurrent encode jobs — not 300 — when you size [[NVENC]] / CPU.

## Technical Details
```txt
Source mezzanine / live ingest
        │
   ┌────┼────┬────┐
 1080p 720p 480p audio   ← each box = one rendition (encode job)
   └────┼────┴────┘
        │
   listed in master / AdaptationSet  ([[ABR]] ladder)
```

### Name them in the HLS master

```plaintext
#EXT-X-STREAM-INF:BANDWIDTH=5800000,RESOLUTION=1920x1080,CODECS="avc1.640028,mp4a.40.2"
1080p/index.m3u8
#EXT-X-STREAM-INF:BANDWIDTH=3000000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2"
720p/index.m3u8
```

### ffmpeg — two video renditions (sketch)

```bash
ffmpeg -i in.mp4 \
  -map 0:v -map 0:a -c:v:0 libx264 -b:v:0 5800k -s:v:0 1920x1080 -g 60 -sc_threshold 0 \
  -map 0:v -map 0:a -c:v:1 libx264 -b:v:1 3000k -s:v:1 1280x720  -g 60 -sc_threshold 0 \
  -c:a aac -b:a 128k -f hls -var_stream_map "v:0,a:0 v:1,a:1" \
  -hls_time 2 -master_pl_name master.m3u8 out_%v.m3u8
```

| Knob | Why it matters |
|------|----------------|
| Same `-g` / keyint all rungs | Seamless [[ABR]] switch |
| Bitrate steps ~1.5–2× | Avoid cliffs ([[bitrate streaming]]) |
| Separate audio group | Save bits; one AAC for many video rungs |
| Path per rendition | Clear CDN cache keys / purge |
| Codec per rung (AVC vs HEVC) | Device reach vs bandwidth — label `CODECS` honestly |

## Real-World Applications
Used wherever rendition sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Single-bitrate contribution link** — one rendition to ingest; ladder after origin.
- **Con / skip when:** **Archive mezzanine** — store one master; spawn renditions at package time.
- **Con / skip when:** **Interactive WebRTC** — usually one encode per peer direction, not an HLS-style ladder.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Switch flash / freeze | GOP mismatch across renditions | Re-encode aligned keyframes |
| One rung 404 | Missing playlist or segments on CDN | Publish full ladder; warm cache |
| GPU OOM / dropped channels | Session count = channels × renditions | Fewer rungs or more [[NVENC]] |
| Audio glitch on video switch | Per-rung audio drift | Shared audio rendition / aligned segments |
| Wrong quality selected | `BANDWIDTH` / Representation wrong | Fix advertised bitrate |
| HEVC rung never used | Device can’t decode | Keep AVC baseline rung |
| Loudness jump between rungs | Different audio encodes | One audio rendition or matched loudness |

- **“Three profiles” means three encodes** — ops and cost plans that count channels only are wrong by factor M.
- **Upscaling a low rendition on a 4K TV** — looks soft; cap display or add a higher rung.
- **Renaming folders without regenerating the master** — player still points at dead URIs.
- **Different frame rates in one ladder** — many players mishandle; prefer separate ladders per fps.
