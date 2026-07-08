AV1 is an open, royalty-free video codec developed by the Alliance for Open Media (AOMedia -- includes Google, Netflix, Amazon, Microsoft, Intel, Nvidia, among others).

- AV1 hardware encode requires Ada-generation NVENC or newer (L4, l40, RTX 40-series), T4 and A2 (Turing/Ampere) do not support AV1 encode

- AV1 hardware decode is more widely supported (Turing + in most cases), but encode is the gating factor


AV1 streams -> means transport/delivery streams (MPTS/SPTS, HLS, DASH renditions) where the video payload is compressed using AV1 instead of H.256/HEVC.
- Lower bitrate at equivalent quality reduces network/storage load for the same channel count
- Requires AV1-capable decoders on the client/receiver side, not all STBs/players support AV1 decode yet, which affects rendition ladder design (man need AV1 + H.264 fallback renditions)