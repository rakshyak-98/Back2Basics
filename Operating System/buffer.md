[[Operating System]] [[Buffer cache]] [[buffer head]] [[buffer lifecycle]] [[buffer flags]] [[multiple levels of buffering]] [[system call]] [[Rolling Buffer]] [[atomic ring buffer]] [[kernel ring buffer]]

# Buffer

> A buffer is a temporary memory region that decouples producers and consumers — smoothing speed mismatches between CPU, kernel, network, and disk.

```txt
        Buffer ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Expect stacked-buffering questions: where bytes sit between `fwrite` and NAND…

## Sources
- Tanenbaum, *Modern Operating Systems* — I/O buffering — deep-dive
- Stevens, *UNIX Network Programming* — socket buffers — deep-dive
- Linux kernel: `mm/filemap.c`, block layer buffer docs — deep-dive

## Key Concepts
- **Decouple rates:** accumulate, batch transfer, hide latency.
- **Many layers:** stdio, socket, NIC, disk controller, page cache.
- **Buffer vs cache:** absorb timing vs reuse copies.
- **Lifecycle + flags:** [[buffer lifecycle]], [[buffer flags]], [[buffer head]].

## Technical Details
```txt
App fwrite buffer → socket SO_SNDBUF → NIC ring → switch → disk queue → NAND page program
```

- [[multiple levels of buffering]] add latency but improve throughput.
- Tuning one layer without others shifts bottlenecks

| Term | Intent |
|------|--------|
| Buffer | Absorb timing differences; often drained in order |
| Cache | Keep copies for faster reuse; eviction policies vary |

- Ring-style: [[Rolling Buffer]], [[atomic ring buffer]], [[kernel ring buffer]…

## Mistakes to Avoid
- **Mistake:** Flushing only the app buffer and assuming disk durability
- **Mistake:** Unlimited buffering without backpressure
- **Mistake:** Tuning only one layer in a stacked path

## Pros/Cons or Trade-offs
- **Pro:** Higher throughput; fewer syscalls; smoother latency.
- **Con:** Extra latency; durability ambiguity; memory use.
- **Trade-off:** larger buffers vs memory and stall-on-full behavior.

## Comparison
- vs [[Buffer cache]]: specialized kernel page cache for file/block data.
- vs queue: buffers often contiguous byte regions; queues emphasize message ordering/policy.


### Use cases
- `stdio` buffering, TCP `SO_SNDBUF`/`SO_RCVBUF`, database page buffers, and ke…
