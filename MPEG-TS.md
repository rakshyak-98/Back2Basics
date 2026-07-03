TS ingest refers to ingesting an MPEG-TS (Transport Stream) -> feed into a media server or streaming pipeline

What it means:
MPEG-TS is a container format originally designed for broadcast (DVB, ATSC) that multiplexes audio, video, and metadata into fixed-size 188-byte packets. "TS ingest" is the process of receiving that stream and bringing it into your processing pipeline (e.g., Flussonic, FFmpeg, a transcoder) as the input source.

> [!INFO]
> **In your Flussonic context specifically:**  
> - Flussonic ingests TS most commonly via UDP multicast or SRT from an encoder/headend, then internally repackages it — remuxing to fragmented MP4 or keeping TS segments for HLS output, applying DRM (PallyCon CPIX/Widevine) at the packaging stage before delivery to Shaka Player via DASH or HLS.