[[Operating System]] [[base clock speed]] [[multi-threaded]] [[Thread]]

# Single Instruction, Multiple Data (SIMD)

> SIMD executes one instruction across a vector of data lanes — SSE, AVX, AVX-512 on x86, NEON on ARM — speeding numeric kernels without extra [[Thread]]s.

The CPU applies the same opcode ([[opcode]]) to multiple operands in parallel registers. Compilers auto-vectorize loops; intrinsics (`__m256`) hand-tune hot paths.

## Versus threading

| Approach | Parallelism type |
|----------|------------------|
| SIMD | Data parallel in one thread |
| [[multi-threaded]] | Multiple threads on cores |

Use SIMD for dense math; use threads for independent tasks or I/O overlap ([[CPU IO Bound Task]]).

Check CPU flags: `grep avx /proc/cpuinfo`, `lscpu`.

## Sources

- Intel Intrinsics Guide
- Hennessy & Patterson — SIMD chapters
- Wikipedia: [SIMD](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data)
