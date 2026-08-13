[[Streaming]] [[IPTV]] [[ingestion]] [[CAS (Conditional Access System)]] [[Byte stream]] [[CMAF]]

# MPEG-TS

> MPEG-TS packs video, audio, and tables into 188-byte packets — the broadcast-friendly container for IPTV and UDP ingest.

---

## How it works

```txt
Video ES ─┐
Audio ES ─┼─► mux ─► 188-byte TS packets ─► UDP / file / SRT
PCR / PSI ┘         │
                    ├─ PID 0x0000 PAT
                    ├─ PMT PID(s)
                    └─ media PIDs (video, audio, …)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **TS packet** | Fixed 188 bytes | “I can lose packets and resync on the next sync byte.” |
| **PID** | Packet ID — which stream this is | “Video and audio ride different PIDs in one mux.” |
| **PAT** | Program Association Table | “PAT lists services and where each PMT lives.” |
| **PMT** | Program Map Table | “PMT lists this channel’s video/audio/PCR PIDs.” |
| **MPTS** | Multi-Program TS | “Many channels in one UDP stream.” |
| **SPTS** | Single-Program TS | “One channel, one clean PAT/PMT.” |
| **PCR** | Timing clock in the stream | “Without PCR, decoders drift or freeze.” |

### TS ingest (why media servers care)

**TS ingest** means your pipeline **receives** MPEG-TS (UDP multicast, SRT, file) and remuxes or transcodes — it is the [[ingestion]] front door for broadcast feeds.

> [!INFO]
> In [[flussonic]]-style setups: ingest UDP/SRT TS → remux to fMP4 / TS segments for [[HLS]] / [[DASH]], apply [[DRM]] at package time. Operator feeds may already be **CAS-scrambled** — decrypt on the STB, not in the OTT packager ([[CAS (Conditional Access System)]]).

### How the story goes (4 steps)

1. **Mux** — encoder puts elementary streams + PSI tables into 188-byte packets.
2. **Carry** — send over UDP [[Multicast]], SRT, or store as `.ts` / `.m2ts`.
3. **Ingest** — media server joins/listens, validates PAT/PMT, may `zap` MPTS → SPTS ([[tsduck]]).
4. **Repackage** — for OTT, remux to [[CMAF]] / HLS TS segments; for STB, often leave TS.

---


## Configuration and commands

```bash
# Probe what’s inside a UDP TS
ffprobe -v error -show_programs -show_streams udp://239.1.1.1:5000

# File: list programs (MPTS)
ffprobe -v error -show_programs input.ts

# Remux TS → MPEG-TS file (copy, no re-encode)
ffmpeg -i udp://239.1.1.1:5000 -c copy -f mpegts out.ts

# SRT listener ingest → local TS (pattern)
ffmpeg -i "srt://0.0.0.0:9000?mode=listener" -c copy -f mpegts srt_in.ts
```

| Knob | Why it matters |
|------|----------------|
| Sync byte `0x47` | Lost lock ⇒ “no video” until resync |
| Continuity counter | Gaps = packet loss on the wire |
| PAT/PMT interval | Too rare ⇒ slow channel change / failed demux |
| PCR PID | Wrong/missing PCR ⇒ A/V drift |
| 188 vs 192 (BD) | Blu-ray adds 4-byte timestamp — don’t assume 188 everywhere |
| UDP buffer / TTL | Multicast drops look like “bad encode” |

Debug: `ffprobe` programs → [[tsduck]] `tsp -P analyze` → Wireshark UDP loss → encoder PID map.

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| No programs in ffprobe | Sync / wrong port / scrambled | Confirm `0x47`; right group; CAS vs clear |
| Video OK, no audio | PMT audio PID | Fix encoder map or select correct PID |
| Freeze after seconds | Continuity errors / PCR | Fix packet loss; correct PCR PID |
| Works as file, fails on UDP | Multicast path / TTL / IGMP | Network join path; increase socket buffers |
| HLS from TS stutters | Segment vs keyframe align | Align GOP to segment; prefer [[CMAF]] pack |
| Black on STB only | [[CAS (Conditional Access System)]] | Entitlements / CW — not a mux bug |

---


## Gotchas

> [!WARNING]
> **TS is not MP4** — no single “moov” index. Players and packagers must read PAT/PMT and PIDs continuously.

> [!WARNING]
> **MPTS on one multicast** — many channels share one UDP flow. Downstream that expects SPTS will break until you filter ([[tsduck]] `zap`).

> [!WARNING]
> **Scrambled ≠ corrupt** — CAS-encrypted payloads look like garbage to `ffmpeg` decode; probe tables, don’t assume encode failure.

> [!WARNING]
> **188-byte framing on a [[Byte stream]]** — TCP/SRT still needs a demuxer; “connected” ≠ “valid PAT.”

---


## When not to use

- **Browser-first OTT delivery** — prefer [[CMAF]] fMP4 + [[HLS]] / [[DASH]] manifests for CDN caching and DRM.
- **Random-access large VoD with one URL** — fragmented MP4 / CMAF seeks cleaner than scanning TS.
- **Peer-to-peer browser calls** — [[WebRTC]] uses RTP, not MPEG-TS.
- **Simple progressive download of a short clip** — plain MP4 over HTTPS is enough.

---


## Related

[[Streaming]] [[IPTV]] [[ingestion]] [[flussonic]] [[tsduck]] [[Multicast]] [[CAS (Conditional Access System)]] [[DRM]] [[Byte stream]] [[CMAF]] [[HLS]] [[DASH]] [[Encoding]] [[codecs]] [[SRT]] [[RTSP]] [[RTMP]]

## Sources

- [Wikipedia — MPEG-TS](https://en.wikipedia.org/wiki/MPEG-TS)
