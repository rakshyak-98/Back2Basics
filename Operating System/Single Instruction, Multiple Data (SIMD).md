[[context switching]] [[Buffer cache]] [[Rolling Buffer]] [[NVENC]] [[ffmpeg]]

# Single Instruction, Multiple Data (SIMD)

> CPU vector instructions that process many data lanes per cycle — **when it matters for SE work**, not microarchitecture textbooks.

---

## Mental model

**SIMD** (SSE/AVX on x86, NEON on ARM) applies one instruction to a **vector register** (e.g. 8× `float32` or 32× `uint8`) in parallel. The CPU still runs one thread; parallelism is **data-parallel within a core**, not multi-core.

```txt
Scalar:  for i: c[i] = a[i] + b[i]     →  N add instructions
SIMD:   load 256-bit chunks → vpadd → store   →  N/8 adds (ideal)
```

| Where SEs feel it | Why |
|-------------------|-----|
| **Hashing / crypto** | SHA, AES-NI, BLAKE3 — GB/s vs MB/s |
| **Codecs** | H.264/HEVC/AV1 decode, [[NVENC]] — hand-written SIMD kernels |
| **JSON / parsing** | simdjson-style — scan 64 bytes at a time for structural chars |
| **Compression** | zstd, snappy — memcmp-style hot loops |
| **Image/audio DSP** | Resample, color convert — obvious vector wins |

**You rarely write SIMD** — libraries (OpenSSL, ffmpeg, zlib-ng, Rust `std::simd`) already did. Your job: **pick the build**, **enable CPU features**, **avoid scalar fallbacks in hot paths**.

---

## Standard config / commands

### Detect CPU features

```shell
grep -o 'avx[^ ]*\|sse[^ ]*\|neon' /proc/cpuinfo | sort -u
lscpu | grep -i 'flags\|model name'

# Go
go env GOAMD64=v3   # assume AVX2 at compile time (Go 1.18+)

# Rust (target-cpu)
RUSTFLAGS='-C target-cpu=native' cargo build --release

# ffmpeg with libx264/x265 — uses SIMD internally
ffmpeg -hide_banner -encoders | grep -E '264|265|av1'
```

### When SIMD is active (profiling)

```shell
# perf: are vector instructions hot?
perf stat -e instructions,cycles ./your_binary
perf record -g ./your_binary && perf report | head

# Check if scalar fallback path taken (library-specific)
# OpenSSL: openssl speed sha256
# simdjson: benchmark with -a flag
```

### Build/deploy checklist

```txt
1. Binary built for lowest common CPU in fleet OR fat binary with runtime dispatch
2. Container base image matches host CPU (no Rosetta/x86-on-ARM surprises)
3. -O3 / LTO for numeric hot loops — compiler auto-vectorizes simple loops
4. Don't assume: measure — memory bandwidth often caps before SIMD
```

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| 10× slower on one machine | `lscpu` flags; illegal instruction crash | Rebuild for baseline CPU; illegal insn = AVX2 binary on old host |
| `SIGILL` on startup | Core dump; objdump `-m` | `-march=x86-64-v2` or runtime CPU detection |
| Encoder CPU at 100%, GPU idle | ffmpeg `-hwaccel`; NVENC available? | Enable hardware path; SIMD CPU encode is expected slow at 4K |
| Parser slower after deploy | New dependency dropped simdjson | Pin library; verify feature flags |
| Identical code, different perf | Thermal throttle; single-channel RAM | Hardware; not SIMD issue |

---

## Gotchas

> [!WARNING]
> **Auto-vectorization is fragile** — loop with pointer aliasing, unknown trip count, or branches → scalar. `-fopt-info-vec` (GCC) to see missed opportunities.

> [!WARNING]
> **Amdahl's law** — SIMD speeds 60% of time 8× → ~2.5× total. Profile first.

> [!WARNING]
> **Alignment** — unaligned loads work on modern CPUs but cost cycles; library internals handle this, your code usually shouldn't touch it.

> [!WARNING]
> **Cloud instance types** — burstable T-series throttle; AVX workloads trigger lower turbo on some Intel SKUs ("AVX offset").

> [!WARNING]
**Don't hand-roll SIMD** unless you're on a team owning a codec/parser — maintenance and correctness (especially signed overflow) are brutal.

---

## When NOT to use

- **I/O-bound services** — DB wait dominates; SIMD irrelevant.
- **Business logic / CRUD** — optimize queries and caching first.
- **Small payloads** — vector setup overhead loses below ~few KB per operation.

---

## Related

[[context switching]] [[Buffer cache]] [[NVENC]] [[ffmpeg]] [[codecs]] [[transcoding]]
