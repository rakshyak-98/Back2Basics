[[DRM]] [[IPTV]] [[MPEG-TS]] [[Streaming]] [[ingestion]]

# CAS (Conditional Access System)

> Pay-TV security layer that **controls who may decrypt encrypted broadcast/IPTV streams** — ECM/EMM + smart card/secure client, not browser [[DRM]].

---

## Mental model

**CAS (Conditional Access System)** is a security system that **controls who is allowed to watch encrypted content**. It is primarily used by **pay-TV operators** (DTH, Cable, IPTV) to ensure only authorized subscribers can decrypt and view channels.

| Purpose | What CAS does |
|---------|---------------|
| Encrypt TV channels | Scrambler encrypts MPEG-TS (or similar) at headend |
| Authenticate subscribers | Smart card / secure client proves entitlement |
| Prevent unauthorized viewing | No valid CW → black screen |
| Support packages / PPV | EMM grants or revokes channel rights |

```text
Video Source
      │
      ▼
Encoder
      │
      ▼
Scrambler/Encryptor
      │
      ├── Encrypted Video
      │
      └── ECM/EMM generated
             │
             ▼
        CAS Server
             │
             ▼
Streaming Server / Broadcast
             │
             ▼
STB / Player + Smart Card / Secure Client
             │
      Requests decryption key
             │
             ▼
CAS verifies subscription
             │
             ▼
Video decrypted if authorized
```

---

## Components

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

The **Control Word** is the short-lived symmetric key used to decrypt the stream.

```text
Encrypted Stream
        +
Control Word
        ↓
Decrypted Video
```

The CW changes frequently to limit the usefulness of leaked keys.

---

## Standard flow / example

A user subscribes to the **Sports Package**:

1. Channel is encrypted at headend.
2. STB receives the encrypted stream.
3. STB extracts the ECM.
4. CAS checks subscription using EMM data.
5. CAS provides the current Control Word.
6. STB decrypts the stream.
7. Video plays.

If the subscription expires:

- No valid entitlement.
- No usable Control Word.
- Black screen or **"Channel Not Authorized."**

---

## CAS vs DRM

| Feature | CAS | [[DRM]] |
|---------|-----|---------|
| Primary use | Broadcast TV | OTT streaming |
| Devices | Set-Top Boxes, Smart TVs | Browsers, mobile apps, Smart TVs |
| Encryption | MPEG-TS scrambling (e.g., DVB CSA, AES variants) | AES encryption (HLS/DASH) |
| License delivery | ECM/EMM | License server |
| Authentication | Subscriber card/client | User account/device |
| Offline playback | Typically no | Often supported |
| Examples | Nagra, Irdeto, Conax, Viaccess-Orca | Widevine, PlayReady, FairPlay |

---

## CAS in IPTV

For [[IPTV]], the flow is:

```text
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

The STB communicates with the CAS server to obtain decryption information before playing the channel. See also [[Multicast]] for multicast delivery patterns.

---

## CAS in OTT

Traditional CAS is generally **not** used for browser-based or mobile OTT services. Instead, OTT platforms use **[[DRM]]** systems such as:

- Google Widevine
- Microsoft PlayReady
- Apple FairPlay

Some operators deploy **CAS + DRM together**:

- **CAS** secures traditional IPTV or broadcast delivery to operator STBs.
- **DRM** secures OTT playback on web, mobile, and smart TV apps.

In modern video platforms, it is common to see **CAS protecting managed IPTV or broadcast services**, while **DRM protects OTT services**, allowing the same content to be securely delivered across different device types.

---

## Popular CAS vendors

- Nagravision
- Irdeto
- Viaccess-Orca
- Conax
- Verimatrix

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen / "Not Authorized" | Subscription active? EMM refreshed? | Re-provision entitlements; force EMM push |
| One channel only fails | ECM present in TS? Scrambler PID | Verify ECM PID in SI tables; headend scrambler config |
| All channels fail after card swap | Smart card paired to STB? | Re-pair card; verify CAS ID / box ID in CAS server |
| Intermittent freeze / macroblocking | CW rotation sync | Check ECM timing vs scrambler; clock skew on headend |
| IPTV multicast works clear, fails scrambled | IGMP + CAS path | Confirm STB reaches CAS over return path (IP or phone line) |
| OTT app works, STB does not | Wrong protection stack | STB needs CAS; app needs [[DRM]] — don't mix license paths |

---

## Gotchas

> [!WARNING]
> **Leaked CW is short-lived** — but ECM replay within the rotation window can still enable piracy; monitor headend ECM injection.

> [!WARNING]
> **EMM lag** — new subscription may take minutes until EMM reaches STB; don't promise instant activation without CAS ops confirmation.

> [!WARNING]
> **CAS ≠ DRM** — putting Widevine on an operator STB line does not replace broadcast CAS; hybrid ops need two KMS stacks.

> [!WARNING]
> **Card-sharing / cloned smart cards** — operator fraud vector; CAS vendor anti-piracy modules (renewable security) required in contracts.

---

## When NOT to use

- **Browser or mobile OTT** — use [[DRM]] + [[EME]]; CAS has no CDM in Chrome/Safari.
- **Clear internal feeds** — corporate LAN multicast without subscriber billing rarely needs scrambling overhead.
- **VOD-only SaaS** — tokenized HTTPS URLs + [[DRM]] suffice; CAS headend cost unjustified.

---

## Related

[[DRM]] [[IPTV]] [[MPEG-TS]] [[Multicast]] [[EME]] [[Streaming]] [[ingestion]] [[Compliance Reporting to Broadcasters]]
