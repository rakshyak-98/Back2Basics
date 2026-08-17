[[Operating System]] [[base clock speed]] [[multi-threaded]] [[Thread]] [[opcode]] [[CPU IO Bound Task]] [[assembly language]]

# Single Instruction, Multiple Data (SIMD)

> SIMD runs one instruction across a vector of data lanes — SSE, AVX, AVX-512 on x86, NEON on ARM — speeding numeric kernels without extra threads.





## Interview Relevance
Performance interviews: data parallelism vs thread parallelism, when auto-vectorization helps, and how to check CPU feature flags.

## Sources
- Intel Intrinsics Guide — deep-dive
- Hennessy & Patterson — SIMD chapters — deep-dive
- [Wikipedia — SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) — overview

## Key Concepts
- **Vector lanes:** one [[opcode]] applied to multiple operands in wide registers.
- **Auto-vectorization vs intrinsics:** compilers vs `__m256`-style hand tuning.
- **Complementary to threads:** SIMD inside one thread; [[multi-threaded]] across cores.
- **Feature gates:** binaries may require AVX2/AVX-512 presence.

## Technical Details
| Approach | Parallelism type |
|----------|------------------|
| SIMD | Data parallel in one thread |
| [[multi-threaded]] | Multiple threads on cores |

Use SIMD for dense math; use threads for independent tasks or I/O overlap ([[CPU IO Bound Task]]).

```bash
grep -E 'avx|neon|sse' /proc/cpuinfo
lscpu
```

## Real-World Applications
Image codecs, ML kernels, checksums, and database columnar scans. JVM/HotSpot and LLVM emit SIMD when loops are hot and proven safe.

## Pros/Cons or Trade-offs
- **Pro:** Large speedups on dense numeric loops on one core.
- **Con:** Alignment, remainder loops, and ISA portability complexity.
- **Trade-off:** wider vectors (AVX-512) vs frequency/TDP downclock on some CPUs.

## Comparison
- vs [[multi-threaded]]: threads scale across cores; SIMD scales across lanes in one core.
- vs scalar [[assembly language]]: same ISA family; SIMD is packed-data ops.

## Mistakes to Avoid
- Shipping AVX-512-only binaries to hosts without the feature.
- Expecting SIMD to fix I/O-bound latency.
- Ignoring remainder/tail elements and getting wrong results on non-multiple-of-lane sizes.
