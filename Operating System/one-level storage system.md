[[Operating System]] [[abstract storage location]] [[Persistent Block Storage]] [[Buffer cache]]

# One-level storage system

> A one-level storage system presents a single uniform address space for programs and persistent data — the classic vision where memory and disk are indistinguishable to the programmer.

Historically associated with **Multics** and early MIT/Flex machine research: no explicit separate “file read” versus “load instruction” — paging and segmentation hide media. Modern systems approximate pieces of this:

- **Memory-mapped files** — file bytes appear as virtual addresses.
- **Unified page cache** ([[Buffer cache]]) — same pages back file I/O and mmap.
- **NVMe + large RAM** — fast swap and cache blur latency gaps.

Full transparency fails on **durability** and **capacity** — RAM remains volatile without flush ([[fsync]]), and cost per byte still differs.

## Sources

- Corbato et al., Multics papers — one-level store concept
- Denning, “Virtual Memory” — ACM Computing Surveys
- Wikipedia: [Single-level store](https://en.wikipedia.org/wiki/Single-level_store)
