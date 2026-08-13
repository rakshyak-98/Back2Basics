<!-- note-strategy: operational -->
[[Streaming]] [[EME]] [[CAS (Conditional Access System)]] [[HLS]] [[DASH]] [[CPIX]]

# DRM

> DRM (Digital Rights Management) encrypts the stream and only hands keys to entitled players — stops casual copying.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Multi-DRM]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Encrypt media once with a content key, signal DRM in the manifest, then the player asks a license server for that key only if the user is allowed.

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

Browser OTT uses [[EME]] + a CDM (Widevine / PlayReady / FairPlay). Broadcast STBs often use [[CAS (Conditional Access System)]] (ECM/EMM) instead — different stack, same goal (only entitled devices decode).

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **DRM** | Encrypt + license gate for playback | “We protect the asset; the player must prove entitlement.” |
| **License server** | Issues keys after auth / policy checks | “Keys never ship in the clear to random clients.” |
| **CDM** | Secure decrypt module in the device/browser | “EME talks to the CDM; JS never sees the raw key on L1.” |
| **CENC** | One encryption format many DRMs share | “Encrypt once; serve Widevine + PlayReady from the same files.” |
| **PSSH** | Blob telling the CDM which system + key id | “Manifest carries PSSH so the player knows who to ask.” |
| **KID** | Key ID — name of the key, not the key | “License maps KID → CEK for this content.” |
| **Multi-DRM** | Same asset, several CDMs | “Android Widevine, Safari FairPlay, Edge PlayReady.” |

### How the story goes (4 steps)

1. **Get keys** — KMS / DRM vendor returns CEK + KID + PSSH (often via [[CPIX]]).
2. **Encrypt + package** — packager applies CENC; writes protection into [[HLS]]/[[DASH]] manifests.
3. **Entitle** — your backend decides the user may play; mint a short-lived license token ([[streaming license]] / [[Pallycon(DoveRunner)]]).
4. **Play** — player uses [[EME]]; CDM fetches license; decrypts segments.

### License server options (pick one path)

| Path | When it fits |
|------|----------------|
| **DRM-as-a-Service** (PallyCon/DoveRunner, EZDRM, Axinom, BuyDRM, castlabs) | Fastest path; samples + multi-DRM |
| **Cloud media + DRM** (AWS Media + SPEKE, Mux, Cloudflare Stream) | Less custom packaging control |
| **Self-hosted KMS + license** | Hardest; only if compliance forces it |

```txt
Caution! The stream has been secured with DRM…
```

That banner means encryption is on — not a player bug. Only CDM-compatible players can decrypt.

---

## Standard config / commands

Typical live path (Flussonic-style packager + DoveRunner):

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

Debug: browser `chrome://media-internals` + player DRM logs; confirm `ContentProtection` / `#EXT-X-KEY` present.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen, no error | Manifest missing `ContentProtection` / `#EXT-X-KEY` | Re-package with PSSH/KID; verify packager KMS reachability |
| `MEDIA_ERR_ENCRYPTED` / license 401 | Token / site key / user auth | Mint fresh [[streaming license]] token server-side; clock skew |
| Works on Chrome, fails Safari | FairPlay not configured | Add FPS cert + HLS SAMPLE-AES / fMP4 path |
| Works on phone browser, fails STB | Wrong protection stack | STB may need [[CAS (Conditional Access System)]], not Widevine EME |
| “DRM secured” but local VLC fails | Expected — no CDM path | Test with Shaka / Bitmovin / vendor sample player |
| HD blocked, SD plays | Widevine L3 only | Require L1 devices or lower policy max resolution |
| Live encrypt OK, VOD fails | Different key endpoint / content id | Align content id + CPIX request with asset id |

---

## Multi-DRM

**Multi-DRM** means one CENC-encrypted asset (ISO/IEC 23001-7) with several DRM signaling blobs so Widevine, PlayReady, and FairPlay clients can each get a license for the **same** ciphertext.

```txt
One encrypted ladder
   ├── Widevine PSSH  → Widevine license
   ├── PlayReady HDR  → PlayReady license
   └── FairPlay / HLS key URI → FPS license
```

Pack once; license paths differ per platform. Do not re-encode per DRM.

---

## Gotchas

> [!WARNING]
> **DRM ≠ CAS** — browser/mobile OTT uses DRM + [[EME]]; classic IPTV STBs often use [[CAS (Conditional Access System)]]. Mixing license paths breaks half the fleet.

> [!WARNING]
> **Encrypt without manifest signaling** — ciphertext with no PSSH/KEY tags looks like a corrupt stream to the player.

> [!WARNING]
> **Long-lived license tokens in the app** — mint short-lived tokens on your backend; never ship site keys to the client.

> [!WARNING]
> **Player compatibility** — Widevine-only streams fail on FairPlay-only Safari unless you multi-DRM or offer a clear fallback (usually not allowed for premium).

---

## When NOT to use

- **Internal / low-value clips** — signed URLs or application authentication may be enough; DRM cost and support load are high.
- **You only need link expiry** — CDN token authentication, not full CDM.
- **Broadcast STB already on CAS** — don’t bolt Widevine onto a CAS-only headend without a real dual-stack design.
- **WebRTC P2P demos** — ICE/media path first; DRM is an OTT packaging concern.

---

## Related

[[EME]] [[CAS (Conditional Access System)]] [[CPIX]] [[streaming license]] [[Pallycon(DoveRunner)]] [[CDM (Content Decryption Module)]] [[HLS]] [[DASH]] [[CMAF]] [[flussonic]]
