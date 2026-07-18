A rendition is a single encoded output variant of source video, typically differing in resolution, bitrate, or codec, produced for adaptive bitrate (ABR) streaming.
Purpose -> allow a player to switch between quality levels based on available bandwidth/device capability, **without interrupting playback**.

- Each rendition is a separate encode job, one input stream produces N outputs, each requiring independent encoder resources (NVENC session, CPU thread, etc.)

> [!NOTE]
> A directly multiplies encoding load: a 300-channel system with a 3-rendition ABR ladder requires 900 concurrent encode jobs, not 300, when calculating GPU/encoder capacity.