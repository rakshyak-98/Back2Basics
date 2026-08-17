[[DRM]] [[HLS]] [[DASH]] [[CMAF]] [[codecs]] [[CAS (Conditional Access System)]] [[MPD]] [[Manifest (streaming)]] [[Pallycon(DoveRunner)]]

# EME (Encrypted Media Extensions)

> Browser API bridging JavaScript players to hardware CDMs for [[DRM]] — **W3C spec**, not a DRM system itself.

```txt
        EME (Encrypted Med ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers ask about EME to see if you understand the pipeline role, failur…

## Sources
- [Wikipedia — EME](https://en.wikipedia.org/wiki/EME) — overview
- [W3C Encrypted Media Extensions](https://www.w3.org/TR/encrypted-media/) — deep-dive

## Key Concepts
- **Note:** **EME** is the **HTML5 JavaScript API** (`navigator.requestMediaKeySystemAcce…

| Piece              | Role                                       |
| ------------------ | ------------------------------------------ |
| **EME**            | API surface in browser                     |
| **CDM**            | Proprietary decrypt (Widevine L1/L3, etc.) |
| **CENC**           | Common encryption format in [[CMAF]]/fMP4  |
| **License server** | Validates entitlement; returns keys        |
| **MSE**            | Feeds encrypted segments to CDM            |

- **Note:** EME does **not** define encryption

## Technical Details
```txt
Player JS ──► EME: requestMediaKeySystemAccess('com.widevine.alpha')
                    │
              CDM (browser binary) ◄── license challenge/response
                    │
              MSE appends encrypted fMP4 ──► CDM decrypts ──► video element
                    │
         License server ([[DRM]] KMS — Pallycon, EZDRM, etc.)
```

### Shaka Player — minimal Widevine flow (pattern)

```javascript
const player = new shaka.Player(video);

player.configure({
  drm: {
    servers: {
      'com.widevine.alpha': 'https://license.example.com/widevine',
      'com.microsoft.playready': 'https://license.example.com/playready',
    },
  },
});

await player.load('https://cdn.example.com/manifest.mpd'); // [[DASH]] + CENC
```

### Multi-DRM manifest requirement

```txt
Same encrypted segments (.m4s) on origin
  ├── DASH MPD — ContentProtection Widevine + PlayReady descriptors
  ├── HLS — EXT-X-KEY or SAMPLE-AES + FairPlay SKD for Safari
  └── License URLs per CDM in player config
```

- See [[DRM]] for KMS vendors and [[CMAF]] for shared segments.

### Capability probe (debug in browser console)

```javascript
navigator.requestMediaKeySystemAccess('com.widevine.alpha', [{
  initDataTypes: ['cenc'],
  videoCapabilities: [{ contentType: 'video/mp4; codecs="avc1.640028"' }],
}]).then(() => console.log('Widevine OK')).catch(console.error);
```

### Packaging with encryption (ffmpeg + shaka-packager pattern)

```bash
# Clear mezzanine first; encryption at packager layer typical for multi-DRM
shaka-packager \
  in=input.mp4,stream=video,output=enc_video.m4s \
  in=input.mp4,stream=audio,output=enc_audio.m4s \
  --enable_raw_key_encryption --keys label=:key_id=:key= \
  --mpd_output manifest.mpd
```

- Production: use KMS ([[Pallycon(DoveRunner)]]) — don't hardcode keys.

### HTTPS requirement

```txt
EME on secure contexts only (HTTPS localhost exception)
License server CORS must allow player origin
Mixed content blocked — manifest + segments + license all TLS
```

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| `Unsupported keySystem` | Browser/OS; L1 vs L3 | Test Chrome+Android; provide clear fallback message |
| License 403 | Token expired; wrong content ID | Align asset ID with KMS; refresh auth JWT |
| Video black, no error | MSE codec vs EME policy | Match `codecs` in MSE to encrypted track |
| Safari only fail | FairPlay cert not deployed | FPS certificate on server; HLS SKD |
| Chrome works, TV fails | Widevine L3 only on TV | Device allowlist; H.264 baseline rung |
| `DOMException` key session | Init data / PSSH mismatch | Regenerate PSSH at packager; verify [[MPD]] |
| CORS on license | Preflight blocked | `Access-Control-Allow-Origin` on license endpoint |

- **Mistake:** **Clear + encrypted mix in one MSE buffer**
- **Mistake:** **Hardcoded license URLs in player**
- **Mistake:** **EME on HTTP** — blocked except localhost; prod must be HTTPS
- **Mistake:** **L3 screen capture**
- **Mistake:** **HLS FairPlay ≠ Widevine MPD**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **AES-128 HLS only (no studio mandate)**
- **Con / skip when:** **Native apps**
- **Con / skip when:** **Internal corp streams**

## Real-World Applications
- **Scenario:** Used wherever EME sits in an ingest → package → CDN → player path
