[[CAS (Conditional Access System)]] [[IPTV]] [[ingestion]]

# MPEG-TS

> One-line: what / why for **MPEG-TS** — source TBD.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

TS ingest refers to ingesting an MPEG-TS (Transport Stream) -> feed into a media server or streaming pipeline
What it means:
MPEG-TS is a container format originally designed for broadcast (DVB, ATSC) that multiplexes audio, video, and metadata into fixed-size 188-byte packets. "TS ingest" is the process of receiving that stream and bringing it into your processing pipeline (e.g., Flussonic, FFmpeg, a transcoder) as the input source.
> [!INFO]
> **In your Flussonic context specifically:**
> - Flussonic ingests TS most commonly via UDP multicast or SRT from an encoder/headend, then internally repackages it — remuxing to fragmented MP4 or keeping TS segments for HLS output, applying DRM (PallyCon CPIX/Widevine) at the packaging stage before delivery to Shaka Player via DASH or HLS.
> - Operator IPTV/broadcast feeds may arrive **already scrambled** via [[CAS (Conditional Access System)]] — decryption happens on the STB, not in the media server ingest path.

## Standard config / commands

…

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| … | … | … |

## Gotchas

> [!WARNING]
> …

## When NOT to use

…

## Related

[[…]]
