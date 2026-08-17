[[Streaming]] [[EME]] [[CAS (Conditional Access System)]] [[HLS]] [[DASH]] [[CPIX]] [[streaming license]] [[Pallycon(DoveRunner)]] [[CDM (Content Decryption Module)]] [[CMAF]] [[flussonic]]

# DRM

> DRM (Digital Rights Management) encrypts the stream and only hands keys to entitled players — stops casual copying.

```txt
        DRM ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk DRM end-to-end

## Sources
- [Wikipedia — DRM](https://en.wikipedia.org/wiki/DRM) — overview
- [W3C EME](https://www.w3.org/TR/encrypted-media/) — overview

## Key Concepts
- **DRM:** Encrypt + license gate for playback
- **License server:** Issues keys after auth / policy checks
- **CDM:** Secure decrypt module in the device/browser
- **CENC:** One encryption format many DRMs share
- **PSSH:** Blob telling the CDM which system + key id
- **KID:** Key ID — name of the key, not the key — “License maps KID → CEK for this cont…
- **Multi-DRM:** Same asset, several CDMs

**Flow:**

- **Note:** 1. **Get keys**
- **Note:** 2. **Encrypt + package**
- **Note:** 3. **Entitle**
- **Note:** 4. **Play** — player uses [[EME]]; CDM fetches license; decrypts segments.

- **Note:** Browser OTT uses [[EME]] + a CDM (Widevine / PlayReady / FairPlay). Broadcast…

### License server options (pick one path)

| Path | When it fits |
|------|----------------|
| **DRM-as-a-Service** (PallyCon/DoveRunner, EZDRM, Axinom, BuyDRM, castlabs) | Fastest path; samples + multi-DRM |
| **Cloud media + DRM** (AWS Media + SPEKE, Mux, Cloudflare Stream) | Less custom packaging control |
| **Self-hosted KMS + license** | Hardest; only if compliance forces it |

```txt
Caution! The stream has been secured with DRM…
```

- **Note:** That banner means encryption is on

## Technical Details
```txt
Clear mezzanine / live ingest
        │
        ▼
   Packager + KMS (keys / PSSH via [[CPIX]] or vendor API)
        │  CENC encrypt ──► [[HLS]] / [[DASH]]
        ▼
   CDN serves encrypted segments + ContentProtection in manifest
        │
        ▼
   Player + [[EME]] / CDM ──► license request ──► License server
        │                         ▲
        └──── decrypt if entitled ┘
```

- Typical live path (Flussonic-style packager + DoveRunner):

```txt
Live input (UDP / RTMP)
    ↓
Packager ← keys from DRM KMS ([[CPIX]] / vendor)
    ↓ encrypt
Encrypted [[DASH]] / [[HLS]]
    ↓
Player → license URL + token header → DRM license server
    ↓
CDM decrypt → playback
```

| Knob | Why it matters |
|------|----------------|
| License server URL in player | Wrong URL ⇒ challenge never returns a key |
| `pallycon-customdata-v2` (or vendor token) | Auth for the license call — mint on **your** backend |
| Widevine / FairPlay / PlayReady enabled | Match the CDMs your clients actually have |
| Key rotation / KID in manifest | Stale KID ⇒ black screen after renew |
| Security level (L1 vs L3) | HD/UHD policy may require hardware CDM |

- Debug: browser `chrome://media-internals` + player DRM logs

### Multi-DRM

- **Multi-DRM:** means one CENC-encrypted asset (ISO/IEC 23001-7) with several D…

```txt
One encrypted ladder
   ├── Widevine PSSH  → Widevine license
   ├── PlayReady HDR  → PlayReady license
   └── FairPlay / HLS key URI → FPS license
```

- Pack once; license paths differ per platform.
- Do not re-encode per DRM.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen, no error | Manifest missing `ContentProtection` / `#EXT-X-KEY` | Re-package with PSSH/KID; verify packager KMS reachability |
| `MEDIA_ERR_ENCRYPTED` / license 401 | Token / site key / user auth | Mint fresh [[streaming license]] token server-side; clock skew |
| Works on Chrome, fails Safari | FairPlay not configured | Add FPS cert + HLS SAMPLE-AES / fMP4 path |
| Works on phone browser, fails STB | Wrong protection stack | STB may need [[CAS (Conditional Access System)]], not Widevine EME |
| “DRM secured” but local VLC fails | Expected — no CDM path | Test with Shaka / Bitmovin / vendor sample player |
| HD blocked, SD plays | Widevine L3 only | Require L1 devices or lower policy max resolution |
| Live encrypt OK, VOD fails | Different key endpoint / content id | Align content id + CPIX request with asset id |

- **Mistake:** **DRM ≠ CAS**
- **Mistake:** **Encrypt without manifest signaling**
- **Mistake:** **Long-lived license tokens in the app**
- **Mistake:** **Player compatibility**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Internal / low-value clips**
- **Con / skip when:** **You only need link expiry**
- **Con / skip when:** **Broadcast STB already on CAS**
- **Con / skip when:** **WebRTC P2P demos**

## Real-World Applications
- **Scenario:** Used wherever DRM sits in an ingest → package → CDN → player path
