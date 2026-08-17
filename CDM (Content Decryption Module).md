[[DRM]] [[EME]] [[Widevine]]

# CDM (Content Decryption Module)

> CDM decrypts DRM-protected media inside a secure player sandbox — keys never leave the trusted path.

```txt
        CDM (Content Decry ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers want you to separate the browser API ([[EME]]), the license serv…

## Sources
- [W3C Encrypted Media Extensions](https://www.w3.org/TR/encrypted-media/) — deep-dive
- [Wikipedia — Encrypted Media Extensions](https://en.wikipedia.org/wiki/Encrypted_Media_Extensions) — overview

## Key Concepts
- **License path:** Player requests a license
- **Secure pipeline:** Decrypted frames stay in a protected path toward the decoder/display when the…
- **Policy enforcement:** Expiration, offline playback, resolution caps, output protection (e.g
- **Vendor CDMs:** Widevine, PlayReady, FairPlay


- **Core:** A Content Decryption Module is the vendor-specific component (software TEE or…

## Technical Details
```txt
Encrypted segments (DASH/HLS)
       │
       ▼
 Media Player (MSE + EME)
       │
       ▼
     CDM  ◄────── License Server (keys + policy)
       │
       ▼
Decrypted samples (secure environment)
       │
       ▼
Decoder → Display (may require HDCP)
```

- Typical flow: load manifest → fetch encrypted segments → `requestMediaKeySyst…

## Mistakes to Avoid
- **Mistake:** Treating “CDM error” as a network bug without checking license s…
- **Mistake:** Assuming one Widevine level (L1/L2/L3) behaves the same on every…
- **Mistake:** Putting long-lived content keys in application memory or logs

## Pros/Cons or Trade-offs
- **Pro:** Strong content protection without shipping clear keys to app code.
- **Con:** Platform-specific CDMs; debugging is opaque; robustness level and HDCP break “works on my laptop” assumptions.

## Comparison
- vs clear playback: no CDM, no license round-trip. vs [[Multicast]]/[[Broadcas…


### Use cases
- Streaming apps (OTT, live sports) use a CDM so premium titles stay encrypted …
