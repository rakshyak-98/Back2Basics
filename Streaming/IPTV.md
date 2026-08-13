[[Streaming]] [[Multicast]] [[MPEG-TS]] [[CAS (Conditional Access System)]] [[DRM]] [[ingestion]]

# IPTV

> IPTV delivers live TV and VOD over an IP network — set-top box or app, not satellite or cable RF.

---

## How it works

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

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **IPTV** | TV over IP on operator or private net | “Channels ride IP, not RF broadcast.” |
| **Live** | Real-time channel | “One multicast group per channel, or ABR unicast.” |
| **VOD** | Pick a title anytime | “Unicast pull from origin/CDN.” |
| **Time-shift** | Replay recent live | “Catch-up window on the same channel catalog.” |
| **EPG** | Electronic Program Guide | “UI schedule; not the media path.” |
| **STB** | Set-top box | “Operator box joins multicast and decrypts CAS.” |

### Operator vs OTT (keep them short)

| Model | Job in one line |
|-------|-----------------|
| **Managed IPTV** | Private/ISP network, often UDP [[Multicast]] + [[CAS (Conditional Access System)]] on STB |
| **OTT “IPTV-like”** | Public internet, [[HLS]] / [[DASH]] + [[DRM]] in the app |

> [!INFO]
> Same product word, different pipes. If you hear “multicast group / IGMP join,” think operator IPTV. If you hear “m3u8 / Widevine,” think OTT packaging.

### How the story goes (4 steps)

1. **Encode** — headend makes H.264/HEVC + audio into [[MPEG-TS]] (or files for VOD).
2. **Protect** — scramble with [[CAS (Conditional Access System)]] (STB) or encrypt with [[DRM]] (OTT).
3. **Deliver** — live often [[Multicast]] on LAN/ISP; VOD/ABR over HTTPS CDN.
4. **Play** — STB or application reads EPG, joins/pulls stream, decrypts, renders.

---


## Configuration and commands

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

Debug: STB IGMP join logs → switch port counters → `ffprobe` on the same group from a laptop on that VLAN.

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| All STBs black on one channel | `ffprobe` / TSDuck on that multicast | Bad encode or wrong group — fix headend mapping |
| One VLAN fails, others OK | IGMP snooping, querier, PIM | Enable querier; fix L3 multicast routing |
| Auth’d subscriber, black video | CAS smart card / EMM | Resync entitlements; confirm scrambler CW path |
| Works on LAN, dies on internet | Multicast across public net | Don’t — repackage to [[HLS]]/[[DASH]] + CDN |
| VOD buffers, live OK | Origin/CDN cache, bitrate | ABR ladder; cache segments; check last-mile |
| EPG wrong, video fine | Middleware channel map | Align EPG id ↔ service_id / stream key |

---


## Gotchas

> [!WARNING]
> **IPTV ≠ “any video on the internet”** — classic IPTV assumes a controlled IP fabric. Public OTT is a different delivery and security stack.

> [!WARNING]
> **Multicast does not cross the open internet** — no IGMP/PIM path ⇒ you need unicast ABR ([[HLS]] / [[DASH]]).

> [!WARNING]
> **CAS is not DRM** — STB Conditional Access decrypts scrambled TS; browser apps use [[DRM]] / [[EME]]. Mixing the words in a design review loses trust.

> [!WARNING]
> **One bad CBR bitrate** — managed nets hide it; same feed on Wi‑Fi phones without ABR will buffer forever.

---


## When not to use

- **Millions of anonymous viewers on the public internet** — use [[HLS]] / [[DASH]] + CDN, not campus multicast.
- **Browser P2P calls** — that is [[WebRTC]] / [[ICE (Interactive Connectivity Establishment)]], not IPTV headend.
- **Simple file download / progressive MP4 only** — no channel guide, no live mux; keep HTTP progressive or [[Byte stream]] ranges.
- **You need interactive ultra-low latency between two peers** — WebRTC, not multicast TV.

---


## Related

[[Streaming]] [[Multicast]] [[MPEG-TS]] [[CAS (Conditional Access System)]] [[DRM]] [[EME]] [[ingestion]] [[flussonic]] [[HLS]] [[DASH]] [[tsduck]] [[WebRTC]]

## Sources

- [Wikipedia — IPTV](https://en.wikipedia.org/wiki/IPTV)
