[[Streaming]] [[Multicast]] [[MPEG-TS]] [[CAS (Conditional Access System)]] [[DRM]] [[ingestion]] [[EME]] [[flussonic]] [[HLS]] [[DASH]] [[tsduck]] [[WebRTC]]

# IPTV

> IPTV delivers live TV and VOD over an IP network — set-top box or app, not satellite or cable RF.

```txt
        IPTV ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk IPTV end-to-end

## Sources
- [Wikipedia — IPTV](https://en.wikipedia.org/wiki/IPTV) — overview

## Key Concepts
- **IPTV:** TV over IP on operator or private net — “Channels ride IP, not RF broadcast.”
- **Live:** Real-time channel — “One multicast group per channel, or ABR unicast.”
- **VOD:** Pick a title anytime — “Unicast pull from origin/CDN.”
- **Time-shift:** Replay recent live — “Catch-up window on the same channel catalog.”
- **EPG:** Electronic Program Guide — “UI schedule; not the media path.”
- **STB:** Set-top box — “Operator box joins multicast and decrypts CAS.”

**Flow:**

- **Note:** 1. **Encode**
- **Note:** 2. **Protect**
- **Note:** 3. **Deliver** — live often [[Multicast]] on LAN/ISP; VOD/ABR over HTTPS CDN.
- **Note:** 4. **Play** — STB or application reads EPG, joins/pulls stream, decrypts, ren…

### Operator vs OTT (keep them short)

| Model | Job in one line |
|-------|-----------------|
| **Managed IPTV** | Private/ISP network, often UDP [[Multicast]] + [[CAS (Conditional Access System)]] on STB |
| **OTT “IPTV-like”** | Public internet, [[HLS]] / [[DASH]] + [[DRM]] in the app |


- **Core:** Same product word, different pipes

## Technical Details
```txt
Headend / encoder
      │
      ▼
[[MPEG-TS]] over UDP (often [[Multicast]])
      │
      ▼
Middleware + EPG          [[CAS (Conditional Access System)]] / [[DRM]]
      │                              │
      └──────────► STB / smart TV / app ◄──────────┘
```

### Probe a live TS feed (operator-style)

```bash
# Join / capture multicast MPEG-TS (needs IGMP path to the source)
ffprobe -v error -show_streams udp://239.1.1.1:5000

# Remux one UDP input to a local file for triage
ffmpeg -i udp://239.1.1.1:5000 -c copy -t 30 /tmp/sample.ts
```

### Typical media-server ingest → package (Flussonic-style idea)

```txt
UDP/SRT MPEG-TS ingest  ──►  [[flussonic]] / packager
                              │
                    ┌─────────┴─────────┐
                 HLS / DASH            raw TS / SPTS out
                 (+ DRM if OTT)        (STB / internal)
```

| Knob | Why it matters |
|------|----------------|
| Multicast group + port | Wrong group = black screen with “healthy” encoder |
| IGMP snooping / PIM | Without it, multicast floods or never reaches the STB |
| [[CAS (Conditional Access System)]] entitlements | Auth’d user still black if EMM/CW missing |
| ABR ladder for OTT | Public internet can’t rely on a single CBR TS bitrate |
| EPG / channel map | Middleware ID must match service_id / stream name |

- Debug: STB IGMP join logs → switch port counters → `ffprobe` on the same grou…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| All STBs black on one channel | `ffprobe` / TSDuck on that multicast | Bad encode or wrong group — fix headend mapping |
| One VLAN fails, others OK | IGMP snooping, querier, PIM | Enable querier; fix L3 multicast routing |
| Auth’d subscriber, black video | CAS smart card / EMM | Resync entitlements; confirm scrambler CW path |
| Works on LAN, dies on internet | Multicast across public net | Don’t — repackage to [[HLS]]/[[DASH]] + CDN |
| VOD buffers, live OK | Origin/CDN cache, bitrate | ABR ladder; cache segments; check last-mile |
| EPG wrong, video fine | Middleware channel map | Align EPG id ↔ service_id / stream key |

- **Mistake:** **IPTV ≠ “any video on the internet”**
- **Mistake:** **Multicast does not cross the open internet**
- **Mistake:** **CAS is not DRM**
- **Mistake:** **One bad CBR bitrate**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Millions of anonymous viewers on the public internet**
- **Con / skip when:** **Browser P2P calls**
- **Con / skip when:** **Simple file download / progressive MP4 only**
- **Con / skip when:** **You need interactive ultra-low latency between two pee…

## Comparison
- vs [[HLS]]: **Millions of anonymous viewers on the public internet**
- vs [[WebRTC]]: **Browser P2P calls**
- vs [[Byte stream]]: **Simple file download / progressive MP4 only**


### Use cases
- Same product word, different pipes

- Used wherever IPTV sits in an ingest → package → CDN → player path
