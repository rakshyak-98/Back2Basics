[[Streaming]] [[DRM]] [[CPIX]] [[Pallycon(DoveRunner)]] [[EME]]

# streaming license

> A streaming license token proves the player may fetch decryption keys — not the same as the CPIX packaging key token.

---

## Mental model

**Say it in one breath:** Your backend mints a short-lived license token after user authentication; the player sends it to the DRM license server; the CDM gets content keys.

```txt
Auth OK → mint license token → player license request + token → keys → decrypt
```

For PallyCon/DoveRunner Widevine, that token is often `pallycon-customdata-v2` — **different** from the CPIX `getKey` token used at packaging time.

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **License** | Permission + keys for playback | “License server returns keys to the CDM.” |
| **License token** | Signed proof from *your* backend | “We mint the token; DoveRunner trusts our site key.” |
| **CPIX getKey** | Packaging-time key exchange | “CPIX is for packagers, not the viewer license call.” |
| **IV** | Extra randomness for encryption | “Same plaintext + different IV → different ciphertext.” |
| **Playback policy** | Limits: rental, HDCP, offline | “Policy rides inside the license token.” |

### IV (one line)

IV (Initialization Vector) randomizes ciphertext so identical frames don’t look identical on the wire.

---

## Standard config / commands

```txt
Player → POST license URL
Header: pallycon-customdata-v2: <token from your API>
CDM ↔ Widevine/PlayReady/FairPlay license response
```

Mint tokens only on the server (Site ID + Site Key). Set validity short (minutes–hours) and encode playback policy (output protection, rental duration).

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 401 / deny on license | Token expired / bad signature | Remint; sync clocks; verify site key |
| Keys OK in lab, fail in prod | Wrong license URL / env | Match Widevine/FairPlay endpoints per env |
| Packaging works, play fails | Mixed up CPIX vs license token | Use license token on player path only |
| HD blocked | Policy / HDCP flag | Adjust playback policy for device |
| Offline fails | Persist flag missing | Request persistent license where allowed |

---

## Gotchas

> [!WARNING]
> **Never embed Site Key in the app** — attackers mint unlimited licenses.

> [!WARNING]
> **Token ≠ content key** — token authorizes the license call; keys stay inside the CDM.

---

## When NOT to use

- **Clear (unencrypted) streams** — no license path.
- **Internal tools with trusted network only** — simpler authentication may suffice (still encrypt if needed).

---

## Related

[[DRM]] [[CPIX]] [[Pallycon(DoveRunner)]] [[EME]] [[CAS (Conditional Access System)]]
