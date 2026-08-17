[[Operating System]] [[bus]] [[PCI (Peripheral Component Interconnect)]] [[base clock speed]] [[Persistent Block Storage]] [[mutexes]] [[Buffer cache]]

# System bus

> The system bus is the backbone connecting CPU, main memory, and I/O controllers — every syscall that touches disk or network eventually moves bytes across these links.

```txt
        System bus ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Computer architecture meets OS: von Neumann path, NUMA, DMA, and coherence co…

## Sources
- Hennessy & Patterson, *Computer Architecture* — deep-dive
- [Wikipedia — System bus](https://en.wikipedia.org/wiki/System_bus) — overview
- [Wikipedia — Front-side bus](https://en.wikipedia.org/wiki/Front-side_bus) — overview

## Key Concepts
- **CPU–RAM–I/O triangle:** address/data/control paths.
- **NUMA:** local vs remote DRAM latency.
- **Coherence:** snooping/directories keep caches consistent.
- **DMA:** devices R/W RAM without CPU byte loops.

## Technical Details
```txt
     ┌─────────┐   address/data/control   ┌──────────┐
     │   CPU   │◄────────────────────────►│   RAM    │
     └────┬────┘                          └──────────┘
          │
          ▼
     I/O bridge → [[PCI (Peripheral Component Interconnect)]] / USB / NVMe
```

- Driver buffers often live in [[Buffer cache]] pages.
- Frequency ([[base clock speed]]) and storage ([[Persistent Block Storage]]) s…
- Generic concept note: [[bus]].

## Mistakes to Avoid
- **Mistake:** Ignoring NUMA when pinning threads and allocating memory
- **Mistake:** Blaming only software for bandwidth limits that are interconnect…
- **Mistake:** False sharing from contended cache lines on “the bus” coherence …

## Pros/Cons or Trade-offs
- **Pro:** Unified model for thinking about data movement.
- **Con:** Classic “one bus” mental model undersells modern fabrics.
- **Trade-off:** more interconnect bandwidth vs power/cost.

## Comparison
- vs [[bus]]: general term vs CPU-centric system path emphasis.
- vs network links: in-chassis vs across machines.


### Use cases
- NUMA-aware placement, GPU/NIC DMA tuning, and explaining memory-bandwidth cei…
