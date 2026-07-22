[[codecs]] [[Encoding]] [[HLS]] [[DASH]] [[CMAF]] [[Lossy Audio Compression]]

# AAC (Advanced Audio Coding)

> Default audio codec for HLS/DASH/fMP4 — **MPEG-4 Part 3 / ISO/IEC 14496-3**.

---

## Mental model

**AAC** is a **lossy** perceptual audio codec: it throws away information humans rarely hear, yielding smaller files than MP3 at the same bitrate. In streaming stacks it sits inside **fMP4/CMAF segments** alongside H.264/HEVC/AV1 video; players decode AAC in software or hardware.

```txt
PCM (raw) ──► AAC encoder ──► ADTS or raw AAC in MP4 (mp4a)
                                    │
                    HLS/DASH manifest CODECS="…,mp4a.40.2"
                                    │
                              Player decode → speakers
```

| Profile | Typical use | `CODECS` string (HLS) |
|---------|-------------|------------------------|
| **AAC-LC** | Stereo streaming default | `mp4a.40.2` |
| **HE-AAC v1 (SBR)** | Low-bitrate mobile | `mp4a.40.5` |
| **HE-AAC v2 (PS)** | Very low bitrate stereo | `mp4a.40.29` |
| **AAC-LD / ELD** | WebRTC, low latency | rarely in HLS ladders |

**AAC-LC @ 128 kbps stereo** is the industry default for VoD and live ABR. Surround broadcast may use AC-3/E-AC-3 (`ec-3`) or Dolby Digital Plus — separate audio renditions in the manifest.

---

## Standard config / commands

### ffmpeg — AAC for HLS/fMP4 (production default)

```bash
# AAC-LC stereo 128k — pairs with H.264 in CMAF/HLS
ffmpeg -i input.mp4 -c:v copy -c:a aac -profile:a aac_low -b:a 128k -ar 48000 -ac 2 \
  -movflags +faststart output.mp4

# Live ladder — match sample rate across rungs
ffmpeg -re -i input -c:v libx264 -b:v 3000k -c:a aac -b:a 128k -ar 48000 \
  -f hls -hls_time 4 -hls_playlist_type event out.m3u8
```

| Knob | Why |
|------|-----|
| `-profile:a aac_low` | LC profile — widest device support |
| `-ar 48000` | 48 kHz — broadcast/streaming standard (44.1 kHz OK for music VoD) |
| `-ac 2` | Stereo; mono use `-ac 1` @ 64–96k |
| `-b:a 128k` | Sweet spot quality/size; 96k acceptable for talk |

### Bitrate guidance (stereo AAC-LC)

```txt
Content type        Bitrate
Talk / podcast      64–96 kbps
General streaming   128 kbps
Music / high quality 192–256 kbps
Low-bandwidth rung  96 kbps HE-AAC (if player supports)
```

### Verify codec in packaged output

```bash
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,profile,bit_rate,sample_rate,channels -of csv=p=0 output.mp4
mediainfo --Inform="Audio;%Format% %BitRate% %SamplingRate%" output.mp4
```

### HLS master playlist audio tag

```plaintext
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="audio",NAME="English",DEFAULT=YES,URI="audio/en.m3u8"
#EXT-X-STREAM-INF:BANDWIDTH=3128000,RESOLUTION=1280x720,CODECS="avc1.64001f,mp4a.40.2",AUDIO="audio"
720p.m3u8
```

`BANDWIDTH` must include audio bitrate — see [[bitrate streaming]].

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| No audio on iOS/Safari | Codec not AAC-LC; wrong `mp4a` in CODECS | Re-encode AAC-LC; fix manifest CODECS string |
| Audio ahead/behind video | Separate audio rendition misaligned | Package audio in same segment timeline; aligned GOP |
| Muffled / underwater | HE-AAC on player without SBR | Fall back to AAC-LC for that rung |
| Silent after DRM | Audio not CENC-wrapped with video | [[DRM]] sample encryption must cover audio track |
| `-c:a copy` fails in HLS | Source MP3/Opus in TS | Transcode to AAC for fMP4/HLS ([[re-encoding]]) |
| Loudness jumps between ads | No loudness normalization | EBU R128 / `-af loudnorm` on mezzanine |

---

## Gotchas

> [!WARNING]
> **Opus in HLS** — limited Smart TV support; AAC remains the compatibility baseline for [[HLS]]/[[DASH]].

> [!WARNING]
> **ADTS vs raw AAC in MP4** — HLS fMP4 needs AAC in MP4 boxes (`mp4a`), not standalone ADTS `.aac` files in modern stacks.

> [!WARNING]
> **Sample rate mismatch across ladder** — switching video rungs can glitch if audio sample rates differ; lock to 48 kHz.

> [!WARNING]
> **Dual mono labeled stereo** — `-ac 2` on mono source wastes bits; detect channels upstream.

---

## When NOT to use

- **WebRTC voice** — prefer Opus (built into WebRTC); AAC adds encode latency.
- **Archival master** — store lossless (FLAC/PCM mezzanine); AAC only at delivery edge.
- **Ultra-low latency LL-HLS** — audio frame pacing matters; don't add redundant transcode hops.

---

## Related

[[codecs]] [[Encoding]] [[HLS]] [[DASH]] [[CMAF]] [[bitrate streaming]] [[DRM]] [[re-encoding]]
