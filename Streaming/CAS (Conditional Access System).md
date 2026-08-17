[[DRM]] [[IPTV]] [[MPEG-TS]] [[Streaming]] [[ingestion]] [[Multicast]] [[EME]] [[Compliance Reporting to Broadcasters]] [[tsduck]]

# CAS (Conditional Access System)

> CAS controls who can watch scrambled pay-TV — headend encrypts; only entitled STBs get the control word.

```txt
        CAS (Conditional A ──┬── Why it matters
               ├── Sources
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Reviewers probe whether you can walk CAS end-to-end

## Sources
- [Wikipedia — CAS](https://en.wikipedia.org/wiki/CAS) — overview

## Technical Details
```txt
Video source → Encoder → Scrambler
                              │
                    Encrypted TS + ECM/EMM
                              │
                         CAS server
                              │
              Broadcast / [[IPTV]] multicast
                              │
              STB + smart card / secure client
                              │
              Entitled? → CW → decrypt → watch
```

- operations knobs live in the CAS vendor console + scrambler
- Typical checks from the transport side:

```bash
# Confirm ECM/EMM PIDs present in the TS (TSDuck / analyzer)
tsp -I ip <mpts>:<port> -P analyze -O drop
# Look for CAT / ECM PIDs related to the scrambled service

ffprobe -hide_banner udp://@<addr>:<port>   # programs present?
```

| Knob | Why it matters |
|------|----------------|
| ECM PID / cycle | Missing or slow ECM ⇒ no CW ⇒ black screen |
| EMM delivery path | New subs stay dark until EMM reaches the box |
| CW rotation period | Too slow helps pirates; too fast stresses STB |
| CAS ID / box pairing | Card swapped to wrong STB fails decrypt |
| Scrambler algorithm | Must match STB CAS client (vendor stack) |

- Debug path: SI tables (CAT/PMT) → ECM present → subscription in CAS OSS → for…

### Components

| Component | Purpose |
|-----------|---------|
| **Scrambler** | Encrypts video/audio streams |
| **CAS Server** | Manages subscribers and encryption keys |
| **ECM (Entitlement Control Message)** | Contains encrypted **Control Word (CW)** — decryption key for current stream |
| **EMM (Entitlement Management Message)** | Contains subscriber entitlements and permissions |
| **Smart Card / Secure Client** | Stores keys securely; participates in CW delivery |
| **Set-Top Box (STB)** | Uses the control word to decrypt and play content |

### ECM vs EMM

| | **ECM** | **EMM** |
|---|---------|---------|
| Frequency | Sent with every channel | Sent less frequently |
| Carries | Encrypted **Control Word (CW)** | Subscriber rights / package flags |
| Rotation | Changes every ~5–10 s | On subscribe, renew, revoke |
| Role | Decrypt **current** stream | Enable/disable channels or packages |

### Control Word (CW)

- The **Control Word** is the short-lived symmetric key used to decrypt the str…

```txt
Encrypted Stream
        +
Control Word
        ↓
Decrypted Video
```

- The CW changes frequently to limit the usefulness of leaked keys.

### Standard flow / example

- A user subscribes to the **Sports Package**:

1. Channel is encrypted at headend.
2. STB receives the encrypted stream.
3. STB extracts the ECM.
4. CAS checks subscription using EMM data.
5. CAS provides the current Control Word.
6. STB decrypts the stream.
7. Video plays.

- If the subscription expires:

- No valid entitlement.
- No usable Control Word.
- Black screen or **"Channel Not Authorized."**

### CAS vs DRM

| Feature | CAS | [[DRM]] |
|---------|-----|---------|
| Primary use | Broadcast TV | OTT streaming |
| Devices | Set-Top Boxes, Smart TVs | Browsers, mobile apps, Smart TVs |
| Encryption | MPEG-TS scrambling (e.g., DVB CSA, AES variants) | AES encryption (HLS/DASH) |
| License delivery | ECM/EMM | License server |
| Authentication | Subscriber card/client | User account/device |
| Offline playback | Typically no | Often supported |
| Examples | Nagra, Irdeto, Conax, Viaccess-Orca | Widevine, PlayReady, FairPlay |

### CAS in IPTV

- For [[IPTV]], the flow is:

```txt
Live Encoder
      │
Scrambler
      │
CAS Server
      │
Multicast/Unicast IPTV
      │
Set-Top Box
```

- The STB communicates with the CAS server to obtain decryption information bef…
- See also [[Multicast]] for multicast delivery patterns.

### CAS in OTT

- Traditional CAS is generally **not** used for browser-based or mobile OTT ser…
- Instead, OTT platforms use **[[DRM]]** systems such as:

- Google Widevine
- Microsoft PlayReady
- Apple FairPlay

- Some operators deploy **CAS + DRM together**:

- **CAS:** secures traditional IPTV or broadcast delivery to operator STBs.
- **DRM:** secures OTT playback on web, mobile, and smart TV apps.

- In modern video platforms, it is common to see **CAS protecting managed IPTV …

### Popular CAS vendors

- Nagravision
- Irdeto
- Viaccess-Orca
- Conax
- Verimatrix

## Mistakes to Avoid
| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen / "Not Authorized" | Subscription active? EMM refreshed? | Re-provision entitlements; force EMM push |
| One channel only fails | ECM present in TS? Scrambler PID | Verify ECM PID in SI tables; headend scrambler config |
| All channels fail after card swap | Smart card paired to STB? | Re-pair card; verify CAS ID / box ID in CAS server |
| Intermittent freeze / macroblocking | CW rotation sync | Check ECM timing vs scrambler; clock skew on headend |
| IPTV multicast works clear, fails scrambled | IGMP + CAS path | Confirm STB reaches CAS over return path (IP or phone line) |
| OTT app works, STB does not | Wrong protection stack | STB needs CAS; app needs [[DRM]] — don't mix license paths |

- **Mistake:** **Leaked CW is short-lived**
- **Mistake:** **EMM lag**
- **Mistake:** **CAS ≠ DRM**
- **Mistake:** **Card-sharing / cloned smart cards**

## Pros/Cons or Trade-offs
- **Pro:** Use when the note's core job matches the problem (see Key Concepts).
- **Con / skip when:** **Browser or mobile OTT**
- **Con / skip when:** **Clear internal feeds**
- **Con / skip when:** **VOD-only SaaS**

## Comparison
- vs [[DRM]]: **Browser or mobile OTT** — use [[DRM]] + [[EME]]; CAS has no CDM in Chrome/Safari.
- vs [[DRM]]: **VOD-only SaaS**


### Use cases
- Used wherever CAS sits in an ingest → package → CDN → player path
