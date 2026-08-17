[[Streaming]] [[DRM]] [[DASH]] [[HLS]] [[MPEG-TS]] [[Pallycon(DoveRunner)]] [[ingestion]] [[CPIX]] [[EME]] [[streaming manifest file]] [[IPTV]] [[CAS (Conditional Access System)]]

# flussonic

> Media server that ingests live UDP/SRT/RTMP, packages HLS/DASH, and can encrypt with DRM keys — the packaging edge in front of players.





## Interview Relevance
Interviewers probe whether you can walk flussonic end-to-end — not just name it. Signal fluency with **Ingest**, **Package**, **DRM encrypt**, **PSSH** and when you would pick a different path.

## Sources
- [Wikipedia — flussonic](https://en.wikipedia.org/wiki/flussonic) — overview

## Key Concepts
- **Ingest:** How live bytes enter Flussonic — “UDP [[MPEG-TS]] multicast, [[SRT]], or [[RTMP]] from the encoder.”
- **Package:** Remux/segment for OTT — “We output DASH/HLS the CDN and players understand.”
- **DRM encrypt:** Scramble samples with KMS keys — “Flussonic encrypts; it does not authorize viewers.”
- **PSSH:** DRM init data in the manifest/init — “Player needs PSSH to start a license request.”
- **License token:** Your backend’s signed “this user may play” — “DoveRunner checks the token, then returns content keys.”
- **Manifest rewrite:** Proxy fixes absolute URLs — “Browser must hit your gateway, not 127.0.0.1 inside the box.”

### Roles (keep them straight)

| Actor | Job |
|-------|-----|
| **Flussonic** | Ingest, encrypt, package, serve media |
| **DoveRunner / PallyCon** | KMS + license server ([[Pallycon(DoveRunner)]]) |
| **Your license backend** | Auth user → sign token player sends to DoveRunner |
| **Player** | Fetch manifest → request license → decrypt via CDM ([[EME]], [[DRM]]) |

Without Flussonic encryption, the stream is clear. Without license tokens, anyone who can fetch segments may still need a CDM path — but you lose entitlement control; design assumes signed tokens.

### License token story (4 steps)

1. Player wants `content_id` — your application already authenticated the user.
2. Your backend builds a short-lived token (user, device, content, expiry, rights) and **HMAC-signs** with the site key.
3. Player sends license request + token (+ PSSH) to DoveRunner.
4. DoveRunner validates signature and policy → returns decryption license to the CDM.

```txt
Player → your API: “token for channel_1”
Your API → signed license token
Player → DoveRunner: license request + token + PSSH
DoveRunner → allow/deny → key material to CDM
```

## Technical Details
```txt
Encoder / headend
   │  udp://host:port  (or [[SRT]] / [[RTMP]] / [[RTSP]])
   ▼
Flussonic
   ├─ (optional) fetch keys from DoveRunner KMS  → aes_key, iv, key_id
   ├─ encrypt (e.g. Widevine / CENC)
   └─ package HLS / DASH (+ PSSH in manifest)
   ▼
http://origin/<content_id>/index.m3u8
http://origin/<content_id>/dash.mpd
   ▼
Player ── license request ──► DoveRunner ──► decrypt + play
```

### Conceptual stream URL shapes

```txt
# Ingest (encoder → Flussonic)
udp://<flussonic-private-ip>:<port>

# Play clear or encrypted packaged output
http://<flussonic-host>:<port>/<content_id>/index.m3u8
http://<flussonic-host>:<port>/<content_id>/dash.mpd
```

### License token your backend signs (shape)

```json
{
  "user_id": "user_123",
  "content_id": "channel_1",
  "device_id": "device_xyz",
  "expires_at": 1735689600,
  "rights": ["stream"]
}
```

```txt
signature = HMAC-SHA256(canonical_token_bytes, site_key)
# Return signed blob to player — never embed site_key in the app
```

### DoveRunner validation checklist (what the KMS asks)

```txt
content_id valid?
user/device enrolled?
subscription / entitlement OK?
session still active?
geo / device-concurrency limits?
token signature + expiry OK?
→ issue license OR deny with error code
```

| Knob | Why it matters |
|------|----------------|
| Ingest URL / multicast group | Wrong iface = silent no-input |
| DRM key / content_id mapping | Mismatch → player license fails though manifests 200 |
| Output hostname in manifests | Absolute `127.0.0.1` breaks browsers behind a proxy — rewrite ([[streaming manifest file]]) |
| Token TTL | Long-lived tokens = sharing / piracy window |

Wire DRM details with [[CPIX]] / [[DRM]] / [[EME]]; Flussonic is the packager, not the identity provider.

## Real-World Applications
Used wherever flussonic sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Browser mesh calls / data channels** — [[WebRTC]] + [[WebRTC Signaling channels]] / SFU products.
- **Con / skip when:** **Simple file download APIs** — [[How to attach stream to HTTP handlers]].
- **Con / skip when:** **No DRM, tiny audience, already have nginx-rtmp** — may be enough for an MVP ([[Microservice]]); Flussonic shines when you need serious live package + DRM.

## Comparison
- vs [[WebRTC]]: **Browser mesh calls / data channels** — [[WebRTC]] + [[WebRTC Signaling channels]] / SFU products.
- vs [[How to attach stream to HTTP handlers]]: **Simple file download APIs** — [[How to attach stream to HTTP handlers]].
- vs [[Microservice]]: **No DRM, tiny audience, already have nginx-rtmp** — may be enough for an MVP ([[Microservice]]); Flussonic shines when you need serious live package + DRM.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| No segments / empty manifest | Ingest bitrate / `udp://` reachability | Fix encoder → Flussonic path; confirm MPEG-TS on the wire ([[MPEG-TS]]) |
| Manifest 200, player black | DRM / license error in player logs | Token signing, content_id, Widevine support |
| “DRM secured” but won’t play | CDM / browser policy | Test Widevine-capable Chrome/Android; FairPlay needs HLS+FPS path |
| Segments load from wrong host | Absolute URLs in MPD/M3U8 | Gateway rewrite to public prefix ([[streaming manifest file]]) |
| Works on server curl, fails in browser | Private IP in manifest | Publish public origin or reverse-proxy |
| License denied intermittently | Clock skew / expired token | NTP; shorten path from mint → player request |
| High origin CPU | Transcode + encrypt on one box | Separate ABR ladder; scale Flussonic / push CDN |

- **Flussonic encrypts; DoveRunner authorizes** — configuring packaging without a license token path leaves you with ciphertext nobody legitimate can play — or a broken entitlement story.
- **Site key on the client** — never ship the HMAC site key in the app; only your backend signs tokens.
- **Manifest hostnames** — Flussonic may emit URLs valid only on the host/container network; browsers need the public/gateway path.
- **Clear vs encrypted testing** — prove ingest→HLS/DASH clear first; then enable DRM so you don’t debug two failures at once.
- **Not a WebRTC SFU** — Flussonic here is OTT packaging. Browser P2P uses [[WebRTC]] / [[ICE (Interactive Connectivity Establishment)]], not UDP TS ingest.
