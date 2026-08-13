[[Operating System]] [[buffer]] [[buffer lifecycle]] [[Buffer cache]] [[Blocking]]

# Multiple levels of buffering

> Real systems stack buffers at every speed boundary — application, libc, socket, kernel page cache, disk controller — and flushing one layer does not flush the layers below.

Each [[buffer]] exists because the producer and consumer run at different rates or granularities. **Multiple levels** improve throughput but add **latency** and **durability gaps**.

```txt
App buffer → stdio → socket SNDBUF → TCP → NIC ring → switch → disk cache → NAND
```

## Common mistakes

| Action | What it does *not* do |
|--------|------------------------|
| `fflush(stdout)` | [[fsync]] file on disk |
| `socket write()` return | Peer application read |
| `close()` | Guarantee persistence |

Tuning only the largest buffer hides backpressure until something smaller fills and blocks ([[Blocking]]).

See [[buffer lifecycle]] for state transitions at one layer.

## Sources

- Stevens, *UNIX Network Programming*
- Tanenbaum, *Modern Operating Systems* — I/O buffering
