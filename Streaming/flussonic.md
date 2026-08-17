[[Streaming]] [[DRM]] [[DASH]] [[HLS]] [[MPEG-TS]] [[Pallycon(DoveRunner)]] [[ingestion]] [[CPIX]] [[EME]] [[streaming manifest file]] [[IPTV]] [[CAS (Conditional Access System)]]

# flussonic

> Media server that ingests live UDP/SRT/RTMP, packages HLS/DASH, and can encrypt with DRM keys — the packaging edge in front of players.

```txt
        flussonic ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you can walk flussonic end-to-end

## Sources
- [Wikipedia — flussonic](https://en.wikipedia.org/wiki/flussonic) — overview

## Key Concepts
- **Ingest:** How live bytes enter Flussonic
- **Package:** Remux/segment for OTT — “We output DASH/HLS the CDN and players understand.”
- **DRM encrypt:** Scramble samples with KMS keys
- **PSSH:** DRM init data in the manifest/init
- **License token:** Your backend’s signed “this user may play”
- **Manifest rewrite:** Proxy fixes absolute URLs

### Roles (keep them straight)

| Actor | Job |
|-------|-----|
| **Flussonic** | Ingest, encrypt, package, serve media |
| **DoveRunner / PallyCon** | KMS + license server ([[Pallycon(DoveRunner)]]) |
| **Your license backend** | Auth user → sign token player sends to DoveRunner |
| **Player** | Fetch manifest → request license → decrypt via CDM ([[EME]], [[DRM]]) |

- **Note:** Without Flussonic encryption, the stream is clear. Without license tokens, an…

### License token story (4 steps)

- **Note:** 1. Player wants `content_id`
- **Note:** 2. Your backend builds a short-lived token (user, device, content, expiry, ri…
- **Note:** 3. Player sends license request + token (+ PSSH) to DoveRunner.
- **Note:** 4. DoveRunner validates signature and policy → returns decryption license to …

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

- Wire DRM details with [[CPIX]] / [[DRM]] / [[EME]]

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

- **Mistake:** **Flussonic encrypts; DoveRunner authorizes**
- **Mistake:** **Site key on the client**
- **Mistake:** **Manifest hostnames**
- **Mistake:** **Clear vs encrypted testing**
- **Mistake:** **Not a WebRTC SFU**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Browser mesh calls / data channels**
- **Con / skip when:** **Simple file download APIs**
- **Con / skip when:** **No DRM, tiny audience, already have nginx-rtmp**

## Comparison
- vs [[WebRTC]]: **Browser mesh calls / data channels**
- vs [[How to attach stream to HTTP handlers]]: **Simple file download APIs**
- vs [[Microservice]]: **No DRM, tiny audience, already have nginx-rtmp**


### Use cases
- Used wherever flussonic sits in an ingest → package → CDN → player path
