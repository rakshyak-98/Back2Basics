[[Operating System]] [[buffer head]] [[Buffer cache]] [[buffer lifecycle]] [[fsync]]

# Buffer flags

> Buffer flags are kernel bitfields on a buffer head that record whether a block is dirty, locked, mapped, or mid-writeback — the block layer’s state machine in compact form.

Each [[buffer head]] carries flags such as **`BH_Dirty`** (must reach disk), **`BH_Uptodate`** (cache matches media), **`BH_Lock`** (I/O in progress), and **`BH_Mapped`** (associated with a disk block). Together they prevent double writes, torn reads, and use-after-free during writeback.

## Common flags (conceptual)

| Flag role | Meaning if set |
|-----------|----------------|
| Dirty | RAM newer than backing store — needs flush |
| Uptodate | Valid data for this block |
| Lock | Holder is performing I/O; others wait |
| Mapped | Block number bound to this buffer |

Flags interact with page dirty bits in the [[Buffer cache]]: filesystem code sets dirty when metadata or data changes; **`sync`** and [[fsync]] paths walk dirty structures and schedule I/O.

## Why operators rarely touch them

These flags exist in kernel memory. User space observes effects through latency (`iostat`, slow commits) and durability guarantees, not flag dumps. Debugging uses `tracepoints` / `block` subsystem trace or `crash` on vmcores.

## Sources

- Linux kernel: `include/linux/buffer_head.h`
- Linux kernel documentation: [Buffer Head API](https://docs.kernel.org/core-api/buffer.html)
- Understanding the Linux Kernel (Bovet & Cesati) — block I/O chapter
