[[DRM]] [[EME]] [[Widevine]]

# CDM (Content Decryption Module)

> CDM decrypts DRM-protected media inside a secure player sandbox — keys never leave the trusted path.

## Interview Relevance
Interviewers want you to separate the browser API ([[EME]]), the license server, and the CDM that actually holds keys and decrypts samples. Signal that you know HDCP, offline licenses, and “black screen” failures are policy/CDM issues, not “bad video files.”

## Sources
- [W3C Encrypted Media Extensions](https://www.w3.org/TR/encrypted-media/) — deep-dive
- [Wikipedia — Encrypted Media Extensions](https://en.wikipedia.org/wiki/Encrypted_Media_Extensions) — overview

## Core Definition
A Content Decryption Module is the vendor-specific component (software TEE or hardware-backed) that authenticates to a DRM system, stores decryption keys, decrypts media samples, and enforces license rules during playback.

## Key Concepts
- **License path:** Player requests a license; server returns keys + policy; CDM alone can use the keys.
- **Secure pipeline:** Decrypted frames stay in a protected path toward the decoder/display when the platform supports it.
- **Policy enforcement:** Expiration, offline playback, resolution caps, output protection (e.g. HDCP), and anti-capture rules live in the CDM/license, not in app JS.
- **Vendor CDMs:** Widevine, PlayReady, FairPlay — same EME surface, different CDM binaries and robustness levels.

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

Typical flow: load manifest → fetch encrypted segments → `requestMediaKeySystemAccess` → create session → POST license challenge → CDM installs keys → decrypt + play.

## Real-World Applications
Streaming apps (OTT, live sports) use a CDM so premium titles stay encrypted until device-bound playback. Ops triage: license HTTP errors vs CDM reject (policy) vs HDCP fail (output path).

## Pros/Cons or Trade-offs
- **Pro:** Strong content protection without shipping clear keys to app code.
- **Con:** Platform-specific CDMs; debugging is opaque; robustness level and HDCP break “works on my laptop” assumptions.

## Comparison
vs clear playback: no CDM, no license round-trip. vs [[Multicast]]/[[Broadcast]] delivery: those are distribution modes; CDM is about *who can decrypt* after delivery. Sibling: [[DRM]] is the overall system; CDM is the decryptor component.

## Mistakes to Avoid
- Treating “CDM error” as a network bug without checking license status and output protection.
- Assuming one Widevine level (L1/L2/L3) behaves the same on every device.
- Putting long-lived content keys in application memory or logs.
