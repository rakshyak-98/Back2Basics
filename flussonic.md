Flussonic specific jobs:
1. Receives stream -> Takes your UDP input `udp://<private ip>:<port>`>
2. Gets keys from DoveRunner -> Retrieves encryption keys `aes_key` `iv` `key_id`
3. Encrypts content -> Applies Widevine encryption to the stream
4. Package output -> Generates DASH/HLS manifest with encryption metadata (PSSH)
5. Serves encryption stream -> Streams at `http://<private ip>:<port>/<content id>/dash.mpd`


> [!INFO]
> DoveRunner role -> Generates keys and later provides license tokens to players
> Players role -> Requests license from DovRunner, decrypts using license, plays video

> [!NOTE]
> Without Flussonic -> Your stream would be unencrypted. Flussonic is the encryption/packaging layer.