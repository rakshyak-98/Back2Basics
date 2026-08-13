[[Operating System]] [[bus]] [[PCI (Peripheral Component Interconnect)]] [[base clock speed]] [[Persistent Block Storage]]

# System bus

> The system bus is the backbone that connects the CPU, main memory, and I/O controllers — every syscall that touches disk or network eventually moves bytes across these links.

Classic model (**Von Neumann**):

```txt
     ┌─────────┐   address/data/control   ┌──────────┐
     │   CPU   │◄────────────────────────►│   RAM    │
     └────┬────┘                          └──────────┘
          │
          ▼
     I/O bridge → [[PCI (Peripheral Component Interconnect)]] / USB / NVMe
```

## Modern wrinkles

- **NUMA:** multiple memory controllers — local versus remote DRAM latency differs.
- **Cache coherence:** CPUs snoop bus traffic (or directory protocols) to keep caches consistent — relevant to [[mutexes]] false sharing.
- **DMA:** devices read/write RAM without CPU byte loops — driver buffers in [[Buffer cache]].

The [[bus]] note covers generic concepts; **system bus** emphasizes the CPU-centric path from instruction fetch to [[Persistent Block Storage]] I/O.

## Sources

- Hennessy & Patterson, *Computer Architecture*
- Wikipedia: [System bus](https://en.wikipedia.org/wiki/System_bus), [Front-side bus](https://en.wikipedia.org/wiki/Front-side_bus)
