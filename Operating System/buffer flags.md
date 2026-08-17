[[Operating System]] [[buffer head]] [[Buffer cache]] [[buffer lifecycle]] [[fsync]]

# Buffer flags

> Buffer flags are kernel bitfields on a buffer head that record whether a block is dirty, locked, mapped, or mid-writeback — the block layer’s state machine in compact form.

```txt
        Buffer flags ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Kernel/filesystem depth: dirty vs uptodate vs locked, and how that relates to…

## Sources
- Linux kernel: `include/linux/buffer_head.h` — deep-dive
- [Linux kernel docs — Buffer Head API](https://docs.kernel.org/core-api/buffer.html) — deep-dive
- Bovet & Cesati, *Understanding the Linux Kernel* — block I/O — deep-dive

## Key Concepts
- **Dirty:** RAM newer than media — needs flush.
- **Uptodate:** cache valid for this block.
- **Lock:** I/O in progress; waiters block.
- **Mapped:** block number bound to this buffer.

## Technical Details
- Each [[buffer head]] carries flags such as **`BH_Dirty`**, **`BH_Uptodate`**,…
- Together they prevent double writes, torn reads, and use-after-free during wr…

- Flags interact with page dirty bits in the [[Buffer cache]]: filesystem code …
- See [[buffer lifecycle]].

- Operators rarely dump flags
- Debugging uses block tracepoints or `crash` on vmcores.

## Mistakes to Avoid
- **Mistake:** Clearing dirty before I/O completion is acknowledged
- **Mistake:** Reading a buffer that is not uptodate
- **Mistake:** Assuming user space can or should manipulate these flags directly

## Pros/Cons or Trade-offs
- **Pro:** Compact, precise state for concurrent block I/O.
- **Con:** Easy to get wrong in driver/fs code — corruption risk.
- **Trade-off:** fine-grained buffer-head state vs folio/page-centric modern paths.

## Comparison
- vs page dirty bits: page-level vs per-block buffer-head flags.
- vs user-visible `O_SYNC`/`fsync`: user APIs trigger paths that clear dirty under the hood.


### Use cases
- Filesystem and block-layer development
