[[CAS (Conditional Access System)]] [[EME]] [[HLS]] [[DASH]]

- Digital Rights Management

> [!INFO]
> Modern browser-based DRM relies on the Encrypted Media Extensions (EME) API — a standard part of HTML5.
> For broadcast/IPTV STB protection, operators use [[CAS (Conditional Access System)]] (ECM/EMM) instead — see CAS vs DRM there.

**Set up a License Server** (or use a DRM-as-a-Service)
- This is the hardest part if doing it yourself. Popular easy options :
- **PallyCon** (DoveRunner) — Multi-DRM, good HTML5 samples
- **EZDRM** — Widevine/PlayReady/FairPlay
- **BuyDRM**, **Axinom**, ** castlabs DRMtoday**
- **AWS Media Services** + DRM integration
- **Mux** or **Cloudflare Stream** (easier but less customizable)

---

```text
Caution! The stream has been secured with DRM. If you experience issues with playback, please verify that your DRM provider's player is compatible.
```

This is a success message. Your DRM is now active on the stream.
- Stream is encrypted -> Widevine DRM protection is enabled.
- Not all players work -> Only players that support Widevine can decrypt and play it.
- Verify compatibility -> Test with a Widevine-compatible player
	- Android device with Widevine support

Get the stream URL from media server that packages and encrypts your stream

```txt
Live Stream Input (UDP) 
    ↓
[FLUSSONIC] ← Gets encryption keys from DoveRunner KMS
    ↓ (encrypts stream)
Encrypted DASH/HLS output
    ↓
Player (requests license from DoveRunner)
    ↓ (decrypts using license)
Playback
```

## Multi-DRM

**Multi-DRM** means one encrypted video file can play on different DRM systems (Widevine, PlayReady, FairPlay).

- Uses **Common Encryption (CENC)** — same encrypted video, different license servers.
- Packaged as DASH or HLS.
- Each browser/device uses its own **CDM** (Content Decryption Module) to get keys and decrypt.