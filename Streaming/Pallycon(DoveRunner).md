[[Streaming]] [[DRM]] [[CPIX]] [[streaming license]] [[EME]] [[CDM (Content Decryption Module)]] [[flussonic]] [[HLS]] [[DASH]]

# Pallycon(DoveRunner)

> PallyCon (now DoveRunner) is multi-DRM SaaS — your backend mints a signed token so the player can ask for decryption keys.

```txt
        Pallycon(DoveRunne ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk Pallycon end-to-end

## Sources
- [Wikipedia — Pallycon](https://en.wikipedia.org/wiki/Pallycon) — overview

## Key Concepts
- **DoveRunner / PallyCon:** Hosted multi-DRM + KMS — “We outsource Widevine/PlayReady/FairPlay licenses.”
- **pallycon-customdata-v2:** Signed license request token — “Backend mints it; player only forwards it.”
- **Site ID / Site Key:** Account credentials for token crypto — “Site Key never ships in the APK.”
- **Content ID:** Your asset id in their system — “Token content id must match packaged asset.”
- **CSL:** Concurrent stream limiting
- **License renewal:** Short license lifetime, refresh mid-play

- **Note:** You do **not** generate this token in client JS/Kotlin alone with the site ke…

- **Note:** Packaging keys often come via [[CPIX]]

### Auth story (4 steps)

- **Note:** 1. **application authentication** — prove the user to *your* backend.
- **Note:** 2. **Token generation**
- **Note:** 3. **Token delivery** — return token to the player over your API.
- **Note:** 4. **License request**

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

- Player configuration sketch (concept):

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

- Access is through DoveRunner’s developer portal.

- **DevConsole utilities:** 
- Production tokens still belong in your backend service.

- Use console tokens for integration tests only

### Concurrent Stream Limiting Guide

- Docs: [CSL guide](https://docs.doverunner.com/content-security/multi-drm/lice…

- **CSL:** (Concurrent Stream Limiting) caps how many streams one account can pl…

- **License renewal:** — set license duration shorter than the title (e.g.
- 10 minutes).
- While the user watches, the CDM refreshes

- [!NOTE] CSL does **not** apply to offline VOD download / persistent licenses …

| Idea | Plain meaning |
|------|----------------|
| Short license + renew | Server sees active playback |
| Cap N devices | N’th license denied or oldest kicked (per policy) |
| Account id in token | CSL keys off user identity you put in the token |

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| License 401 / invalid token | Token age, Site Key, content id | Remint server-side; verify Site ID; NTP on token host |
| Encrypt works, play fails | Player missing `pallycon-customdata-v2` | Wire license request filter / header |
| Safari only fails | FairPlay cert / HLS key path | Enable FPS in DoveRunner + packager |
| “Too many streams” | CSL + renewals | Raise limit, end stale sessions, check renewal interval |
| Token from DevConsole works, app fails | App builds token wrong | Diff policy JSON / encryption of customdata vs docs |
| Keys from CPIX OK, license rejects | Content id mismatch | Align packaging content id with token `cid` |

- **Mistake:** **Site Key in the client**
- **Mistake:** **CPIX getKey ≠ license token**
- **Mistake:** **CSL without renewal**
- **Mistake:** **Name change**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **No DRM requirement** — signed CDN URLs may be enough.
- **Con / skip when:** **You already run a full in-house multi-DRM stack**
- **Con / skip when:** **CAS-only broadcast STBs**
- **Con / skip when:** **Offline-first download with CSL expectations**

## Comparison
- vs [[CAS (Conditional Access System)]]: **CAS-only broadcast STBs**


### Use cases
- Used wherever Pallycon sits in an ingest → package → CDN → player path
