## License token generation (DRM)

Server generates a PallyCon/DoveRunner v2 license token for Widevine. It is not the same as CPIX `getKey` token. It is the value sent as the `pallycon-customdata-v2` header on license requests to `PallyCon's` license server.


![[Pasted image 20260626125119.png]]


IV (Initialization Vector) -> A fixed size random (or fixed) value used to randomize encryption. Without it, same plaintext always produces same chiphertext.

```txt
Plaintext: "Hello World"
Key: PALLYCON_SITE_KEY (32 bytes)
IV: "0123456789abcdef" (16 bytes)

Encryption process:
IV + Key + Plaintext → AES-256-CBC → Ciphertext
```

## License validity period in streaming scenario

[link](https://docs.doverunner.com/content-security/multi-drm/license/license-token/#license-validity-period-in-streaming-scenario)

In streaming scenario, user rights are checked and new licenses are issued every time playback starts even for the same content.


## Playback policy

[link](https://docs.doverunner.com/content-security/multi-drm/license/license-token/#playback_policy)

