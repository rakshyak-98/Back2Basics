[[DRM]] [[HLS]] [[DASH]] [[CMAF]] [[codecs]]

# EME (Encrypted Media Extensions)

> Browser API bridging JavaScript players to hardware CDMs for [[DRM]] — **W3C spec**, not a DRM system itself.

---

## Mental model

**EME** is the **HTML5 JavaScript API** (`navigator.requestMediaKeySystemAccess`, `MediaKeys`, sessions) that lets a web player request **encrypted media** from **MSE** and obtain **decryption keys** from a **license server** via a **Content Decryption Module (CDM)** — Widevine, PlayReady, FairPlay (Safari uses FairPlay JS + EME-like flow).

```txt
Player JS ──► EME: requestMediaKeySystemAccess('com.widevine.alpha')
                    │
              CDM (browser binary) ◄── license challenge/response
                    │
              MSE appends encrypted fMP4 ──► CDM decrypts ──► video element
                    │
         License server ([[DRM]] KMS — Pallycon, EZDRM, etc.)
```

| Piece | Role |
|-------|------|
| **EME** | API surface in browser |
| **CDM** | Proprietary decrypt (Widevine L1/L3, etc.) |
| **CENC** | Common encryption format in [[CMAF]]/fMP4 |
| **License server** | Validates entitlement; returns keys |
| **MSE** | Feeds encrypted segments to CDM |

EME does **not** define encryption — packaging uses **CENC**; [[HLS]] SAMPLE-AES / fMP4 `sinf`/`schi` boxes wrap the same keys for Apple.

---

## Standard config / commands

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

See [[DRM]] for KMS vendors and [[CMAF]] for shared segments.

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

Production: use KMS ([[Pallycon(DoveRunner)]]) — don't hardcode keys.

### HTTPS requirement

```txt
EME on secure contexts only (HTTPS localhost exception)
License server CORS must allow player origin
Mixed content blocked — manifest + segments + license all TLS
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Unsupported keySystem` | Browser/OS; L1 vs L3 | Test Chrome+Android; provide clear fallback message |
| License 403 | Token expired; wrong content ID | Align asset ID with KMS; refresh auth JWT |
| Video black, no error | MSE codec vs EME policy | Match `codecs` in MSE to encrypted track |
| Safari only fail | FairPlay cert not deployed | FPS certificate on server; HLS SKD |
| Chrome works, TV fails | Widevine L3 only on TV | Device allowlist; H.264 baseline rung |
| `DOMException` key session | Init data / PSSH mismatch | Regenerate PSSH at packager; verify [[MPD]] |
| CORS on license | Preflight blocked | `Access-Control-Allow-Origin` on license endpoint |

---

## Gotchas

> [!WARNING]
> **Clear + encrypted mix in one MSE buffer** — append only encrypted init matching CDM session.

> [!WARNING]
> **Hardcoded license URLs in player** — use auth-wrapped URLs; short TTL tokens.

> [!WARNING]
> **EME on HTTP** — blocked except localhost; prod must be HTTPS.

> [!WARNING]
> **L3 screen capture** — studios may reject L3-only for UHD; contract check.

> [!WARNING]
> **HLS FairPlay ≠ Widevine MPD** — multi-DRM still needs **two manifest paths**, one segment set ([[CMAF]]).

---

## When NOT to use

- **AES-128 HLS only (no studio mandate)** — simpler `EXT-X-KEY`; not true hardware DRM.
- **Native apps** — use platform SDKs (ExoPlayer, AVPlayer) directly; EME is web-only.
- **Internal corp streams** — tokenized URLs + TLS often enough; EME ops cost unjustified.

---

## Related

[[DRM]] [[CAS (Conditional Access System)]] [[HLS]] [[DASH]] [[CMAF]] [[MPD]] [[Manifest (streaming)]] [[Pallycon(DoveRunner)]]
