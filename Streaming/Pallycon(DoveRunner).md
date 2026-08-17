[[Streaming]] [[DRM]] [[CPIX]] [[streaming license]] [[EME]] [[CDM (Content Decryption Module)]] [[flussonic]] [[HLS]] [[DASH]]

# Pallycon(DoveRunner)

> PallyCon (now DoveRunner) is multi-DRM SaaS — your backend mints a signed token so the player can ask for decryption keys.





## Interview Relevance
Interviewers probe whether you can walk Pallycon end-to-end — not just name it. Signal fluency with **DoveRunner / PallyCon**, **pallycon-customdata-v2**, **Site ID / Site Key**, **Content ID** and when you would pick a different path.

## Sources
- [Wikipedia — Pallycon](https://en.wikipedia.org/wiki/Pallycon) — overview

## Key Concepts
- **DoveRunner / PallyCon:** Hosted multi-DRM + KMS — “We outsource Widevine/PlayReady/FairPlay licenses.”
- **pallycon-customdata-v2:** Signed license request token — “Backend mints it; player only forwards it.”
- **Site ID / Site Key:** Account credentials for token crypto — “Site Key never ships in the APK.”
- **Content ID:** Your asset id in their system — “Token content id must match packaged asset.”
- **CSL:** Concurrent stream limiting — “License renewal counts how many devices play at once.”
- **License renewal:** Short license lifetime, refresh mid-play — “Lets the server see ‘still playing’ vs stopped.”

You do **not** generate this token in client JS/Kotlin alone with the site key exposed. Site Key stays on the server.

Packaging keys often come via [[CPIX]]; playback authentication is the separate [[streaming license]] token.

### Auth story (4 steps)

1. **application authentication** — prove the user to *your* backend.
2. **Token generation** — backend builds `pallycon-customdata-v2` (DevConsole API or your token service).
3. **Token delivery** — return token to the player over your API.
4. **License request** — player calls DoveRunner license URL with that header; CDM decrypts.

## Technical Details
```txt
User ──► Your app auth (OAuth / JWT / session)
              │
              ▼
        Your backend ──► mint pallycon-customdata-v2
              │              (Site ID + Site Key + policy)
              ▼
        Player sets header on license request
              │
              ▼
   https://license-global.pallycon.com/ri/licenseManager.do
              │
              ▼
        CDM gets keys ──► decrypt [[HLS]]/[[DASH]]
```

```txt
License URL (global):
  https://license-global.pallycon.com/ri/licenseManager.do

Header:
  pallycon-customdata-v2: <server-minted-token>
```

| Knob | Why it matters |
|------|----------------|
| Site ID + Site Key | Identity for token HMAC/AES — server only |
| Content ID | Must match encrypted asset / CPIX content |
| DRM type (Widevine / FPS / PlayReady) | Match client CDM |
| Playback policy (duration, HDCP, security level) | Enforced at license issue |
| License URL region | Use vendor-documented endpoint for your tenants |

Player configuration sketch (concept):

```js
// Token from YOUR API — never invent Site Key in the browser
const { drmToken } = await api.getDrmToken({ contentId })

player.configure({
  drm: {
    servers: {
      'com.widevine.alpha':
        'https://license-global.pallycon.com/ri/licenseManager.do',
    },
  },
})
// Attach pallycon-customdata-v2 on license requests (player-specific hook)
```

### PallyCon DevConsole API

Access is through DoveRunner’s developer portal.

**DevConsole utilities** — DRM Tools / License Token Generator: enter **Site ID**, **Site Key**, and **Content ID** to mint **test** tokens. Production tokens still belong in your backend service.

Use console tokens for integration tests only; rotate Site Keys if they leak into mobile builds or CI logs.

### Concurrent Stream Limiting Guide

Docs: [CSL guide](https://docs.doverunner.com/content-security/multi-drm/license/csl-guide/)

**CSL** (Concurrent Stream Limiting) caps how many streams one account can play at once by watching **DRM license renewal**.

**License renewal** — set license duration shorter than the title (e.g. 10 minutes). While the user watches, the CDM refreshes; when they stop, renewals stop and a slot frees.

[!NOTE]
CSL does **not** apply to offline VOD download / persistent licenses the same way — don’t promise CSL for download-to-go without reading current DoveRunner limits.

| Idea | Plain meaning |
|------|----------------|
| Short license + renew | Server sees active playback |
| Cap N devices | N’th license denied or oldest kicked (per policy) |
| Account id in token | CSL keys off user identity you put in the token |

## Real-World Applications
Used wherever Pallycon sits in an ingest → package → CDN → player path. Concrete check: validate the failure table in Mistakes to Avoid against a real stream.

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **No DRM requirement** — signed CDN URLs may be enough.
- **Con / skip when:** **You already run a full in-house multi-DRM stack** — don’t add a second license path.
- **Con / skip when:** **CAS-only broadcast STBs** — use [[CAS (Conditional Access System)]]; DoveRunner is OTT/CDM-oriented.
- **Con / skip when:** **Offline-first download with CSL expectations** — CSL is streaming/renewal oriented.

## Comparison
- vs [[CAS (Conditional Access System)]]: **CAS-only broadcast STBs** — use [[CAS (Conditional Access System)]]; DoveRunner is OTT/CDM-oriented.

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| License 401 / invalid token | Token age, Site Key, content id | Remint server-side; verify Site ID; NTP on token host |
| Encrypt works, play fails | Player missing `pallycon-customdata-v2` | Wire license request filter / header |
| Safari only fails | FairPlay cert / HLS key path | Enable FPS in DoveRunner + packager |
| “Too many streams” | CSL + renewals | Raise limit, end stale sessions, check renewal interval |
| Token from DevConsole works, app fails | App builds token wrong | Diff policy JSON / encryption of customdata vs docs |
| Keys from CPIX OK, license rejects | Content id mismatch | Align packaging content id with token `cid` |

- **Site Key in the client** — attackers mint their own tokens. Keep crypto on the server.
- **CPIX getKey ≠ license token** — packaging keys and playback tokens are different credentials ([[CPIX]] vs [[streaming license]]).
- **CSL without renewal** — long-lived licenses cannot count concurrent plays accurately.
- **Name change** — docs say DoveRunner; older notes/samples still say PallyCon. Same product family; check current base URLs.
