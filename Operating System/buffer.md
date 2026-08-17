[[Operating System]] [[Buffer cache]] [[buffer head]] [[buffer lifecycle]] [[buffer flags]] [[multiple levels of buffering]] [[system call]] [[Rolling Buffer]] [[atomic ring buffer]] [[kernel ring buffer]]

# Buffer

> A buffer is a temporary memory region that decouples producers and consumers — smoothing speed mismatches between CPU, kernel, network, and disk.





## Interview Relevance
Expect stacked-buffering questions: where bytes sit between `fwrite` and NAND, buffer vs cache, and how undersized buffers create syscall storms.

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

[[multiple levels of buffering]] add latency but improve throughput. Tuning one layer without others shifts bottlenecks — shrinking TCP buffers under a bursty writer causes more [[system call]]s.

| Term | Intent |
|------|--------|
| Buffer | Absorb timing differences; often drained in order |
| Cache | Keep copies for faster reuse; eviction policies vary |

Ring-style: [[Rolling Buffer]], [[atomic ring buffer]], [[kernel ring buffer]].

## Real-World Applications
`stdio` buffering, TCP `SO_SNDBUF`/`SO_RCVBUF`, database page buffers, and kernel page/block caching ([[Buffer cache]]).

## Pros/Cons or Trade-offs
- **Pro:** Higher throughput; fewer syscalls; smoother latency.
- **Con:** Extra latency; durability ambiguity; memory use.
- **Trade-off:** larger buffers vs memory and stall-on-full behavior.

## Comparison
- vs [[Buffer cache]]: specialized kernel page cache for file/block data.
- vs queue: buffers often contiguous byte regions; queues emphasize message ordering/policy.

## Mistakes to Avoid
- Flushing only the app buffer and assuming disk durability.
- Unlimited buffering without backpressure.
- Tuning only one layer in a stacked path.
