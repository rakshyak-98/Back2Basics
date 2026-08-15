[[Operating System]] [[buffer]] [[buffer lifecycle]] [[Buffer cache]] [[Blocking]] [[fsync]]

# Multiple levels of buffering

> Real systems stack buffers at every speed boundary — app, libc, socket, page cache, controller — and flushing one layer does not flush the layers below.

## Interview Relevance

Durability and latency: name the stack, and what `fflush` / `write` / `close` do *not* guarantee.

## Sources

- Stevens, *UNIX Network Programming* — deep-dive
- Tanenbaum, *Modern Operating Systems* — I/O buffering — overview

## Key Concepts

- **Why stack:** producers/consumers differ in rate and granularity.
- **Gain:** throughput; **cost:** latency and durability gaps.
- **Backpressure:** a small full buffer can block the whole chain ([[Blocking]]).
- **Lifecycle per layer:** see [[buffer lifecycle]].

## Technical Details

```txt
App buffer → stdio → socket SNDBUF → TCP → NIC ring → switch → disk cache → NAND
```

| Action | What it does *not* do |
|--------|------------------------|
| `fflush(stdout)` | [[fsync]] file on disk |
| `socket write()` return | Peer application read |
| `close()` | Guarantee persistence |

Tuning only the largest [[buffer]] hides problems until something smaller fills.

## Real-World Applications

Tuning TCP buffers, stdio in CLIs, and database flush policies that must pierce the whole stack.

## Pros/Cons or Trade-offs

- **Pro:** High throughput across mismatched speeds.
- **Con:** Surprising latency and false durability.
- **Trade-off:** more buffering vs tighter backpressure.

## Comparison

- vs single [[buffer]]: one layer vs the full path.
- vs [[Buffer cache]]: one important kernel layer in the stack.

## Mistakes to Avoid

- Equating user flush with disk durability.
- Unlimited buffering without a full-queue policy.
- Tuning only one layer in production incidents.
