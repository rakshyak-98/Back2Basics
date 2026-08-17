[[Operating System]] [[abstract storage location]] [[Persistent Block Storage]] [[Buffer cache]] [[fsync]]

# One-level storage system

> A one-level storage system presents one uniform address space for programs and persistent data — the classic vision where memory and disk look the same to the programmer.

```txt
        One-level storage  ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Virtual memory history: Multics/single-level store ideas, and why mmap + page…

## Sources
- Corbato et al., Multics papers — one-level store — deep-dive
- Denning, “Virtual Memory” — ACM Computing Surveys — deep-dive
- [Wikipedia — Single-level store](https://en.wikipedia.org/wiki/Single_level_store) — overview

## Key Concepts
- **Uniform addresses:** no explicit “file read” vs “load” in the programming model.
- **Modern approximations:** mmap, unified [[Buffer cache]], fast NVMe + large RAM.
- **Hard limits:** durability and cost-per-byte still differ.
- **Flush still required:** RAM is volatile without [[fsync]].

## Technical Details
- Historically Multics and early MIT/Flex research.

- Memory-mapped files — file bytes as virtual addresses.
- Unified page cache — same pages back file I/O and mmap.
- Fast storage blurs latency but does not erase persistence rules on [[Persiste…

- Related naming idea: [[abstract storage location]].

## Mistakes to Avoid
- **Mistake:** Assuming mmap writes are durable without flush/msync semantics
- **Mistake:** Treating swap as a durability feature
- **Mistake:** Ignoring that “one address space” still has NUMA and device tier…

## Pros/Cons or Trade-offs
- **Pro:** Simpler programming model; fewer explicit I/O calls.
- **Con:** Hides durability/capacity costs until failure.
- **Trade-off:** transparency vs explicit control of persistence and placement.

## Comparison
- vs explicit file I/O: programmer-managed reads/writes vs address-space illusion.
- vs [[Buffer cache]]: cache is a mechanism; one-level store is the model.


### Use cases
- Databases using mmap, OS teaching of single-level store, and IBM i style sing…
