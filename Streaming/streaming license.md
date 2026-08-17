[[Streaming]] [[DRM]] [[CPIX]] [[Pallycon(DoveRunner)]] [[EME]] [[CAS (Conditional Access System)]]

# streaming license

> A streaming license token proves the player may fetch decryption keys — not the same as the CPIX packaging key token.

```txt
        streaming license ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Use cases
```

## Interview Relevance
- **Interview probes:** Interviewers probe whether you can walk streaming license end-to-end

## Sources
- [Wikipedia — streaming license](https://en.wikipedia.org/wiki/streaming_license) — overview

## Key Concepts
- **License:** Permission + keys for playback — “License server returns keys to the CDM.”
- **License token:** Signed proof from *your* backend
- **CPIX getKey:** Packaging-time key exchange
- **IV:** Extra randomness for encryption
- **Playback policy:** Limits: rental, HDCP, offline — “Policy rides inside the license token.”

- **Note:** For PallyCon/DoveRunner Widevine, that token is often `pallycon-customdata-v2`

### IV (one line)

- **Note:** IV (Initialization Vector) randomizes ciphertext so identical frames don’t lo…

## Technical Details
```txt
Auth OK → mint license token → player license request + token → keys → decrypt
```

```txt
Player → POST license URL
Header: pallycon-customdata-v2: <token from your API>
CDM ↔ Widevine/PlayReady/FairPlay license response
```

- Mint tokens only on the server (Site ID + Site Key).
- Set validity short (minutes–hours) and encode playback policy (output protect…

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| 401 / deny on license | Token expired / bad signature | Remint; sync clocks; verify site key |
| Keys OK in lab, fail in prod | Wrong license URL / env | Match Widevine/FairPlay endpoints per env |
| Packaging works, play fails | Mixed up CPIX vs license token | Use license token on player path only |
| HD blocked | Policy / HDCP flag | Adjust playback policy for device |
| Offline fails | Persist flag missing | Request persistent license where allowed |

- **Mistake:** **Never embed Site Key in the app**
- **Mistake:** **Token ≠ content key**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Clear (unencrypted) streams** — no license path.
- **Con / skip when:** **Internal tools with trusted network only**

## Real-World Applications
- **Scenario:** Used wherever streaming license sits in an ingest → package → CDN → player pa…
