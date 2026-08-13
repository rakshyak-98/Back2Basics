[[Operating System]] [[Buffer cache]] [[buffer head]] [[buffer lifecycle]] [[buffer flags]] [[multiple levels of buffering]]

# Buffer

> A buffer is a temporary memory region that decouples producers and consumers — smoothing speed mismatches between CPU, kernel, network, and disk.

Buffers appear at every layer: user-space `stdio` arrays, socket send buffers, disk controller queues, and the kernel [[Buffer cache]]. The pattern is the same: **accumulate data**, **batch transfer**, **hide latency**.

## Why layers stack

```txt
App fwrite buffer → socket SO_SNDBUF → NIC ring → switch → disk queue → NAND page program
```

Each [[multiple levels of buffering]] adds latency but improves throughput. Tuning one layer without others shifts bottlenecks — shrinking TCP buffers under a bursty writer causes more syscalls ([[system call]]).

## Buffer versus cache

| Term | Intent |
|------|--------|
| Buffer | Absorb timing differences; often drained in order |
| Cache | Keep copies for faster reuse; eviction policies vary |

The Linux page cache is caching, but block I/O still uses buffer descriptors ([[buffer head]]) when bridging filesystem pages and LBA addresses.

## Lifecycle

Allocation, fill, flush, and release follow a predictable cycle — see [[buffer lifecycle]]. Flags on block buffers ([[buffer flags]]) record dirty, locked, or mapped state for the kernel block layer.

Ring-style buffers ([[Rolling Buffer]], [[atomic ring buffer]], [[kernel ring buffer]]) specialize streaming and logging workloads.

## Sources

- Tanenbaum, *Modern Operating Systems* — I/O buffering
- Stevens, *UNIX Network Programming* — socket buffers
- Linux kernel: `mm/filemap.c`, block layer buffer documentation
