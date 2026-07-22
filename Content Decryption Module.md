[[DRM]]

CDM (Content Decryption Module) -> is the secure software (or hardware-baked component) responsible for decrypting DRM-protected media during playback

```txt
Encrypted Video
       |
       v
 Media Player
       |
       v
     CDM  <------ License Server
       |             ^
       |             |
       +---- Uses decryption keys
       |
       v
Decrypted frames (inside secure environment)
       |
       v
Video Decoder -> Display
```

Responsibilities
- Authenticate with the DRM system
- Process the DRM license received from the license server.
- Store decryption keys securely.
- Decrypt encrypted video/audio segments.
- Enforce DRM policies:
	- Expiration
	- Offline playback
	- HD/UHD restrictions
	- Screen recording prevention
	- HDCP requirements

Playback Flow
1. User requests video.
2. Player downloads (manifest MPD/HLS), encrypted media segments
3. Player sends license request.
4. License server returns license + decryption keys.
5. CDM -> validates license, extracts keys, decrypts media.
6. Decoder receives decrypted content.
7. Video is deiplayed.


**Common DRM systems**

| DRM                 | CDM           |
| ------------------- | ------------- |
| Google Widevine     | Widevine CDM  |
| Microsoft PlayReady | PlayReady CDM |
| Apple FairPlay<br>  | FairPlay CDM  |
