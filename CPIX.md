[Content Protection Information Exchange Format](https://dashif.org/docs/CPIX2.3/Cpix.html)

The CPIX endpoint response (XML format) contains the cryptographic material necessary to encrypt media.

The API returns a `cpix:CPIX` XML document. You must extract the following critical elements:
- `kid` (Key ID) The unique identifier for the current key.
- `pskc:PlainValue` (or `Secret`) -> the actual content encryption key (Base64 encoded). You will need this to initialize your encryptor.
- `PSSH` (Protection System Specific Header) -> The data required by the player's DRM client (Widevine, PlayReady, etc.) to decrypt the content.

**Integrate with Your Packager:** You must provide these values to your video packager/transcoder (e.g., Shaka Packager, FFmpeg, AWS Elemental MediaConvert). The packager uses these keys to perform CENC (Common Encryption) on your video and audio fragments.

**Generate the Manifest:** As the packager encrypts the content, it will use the `PSSH` data from the XML to populate the `ContentProtection` descriptors in your DASH (`.mpd`) or HLS (`.m3u8`) manifest. Without this signaling in the manifest, the player will not know which DRM license server to contact or which key to request.