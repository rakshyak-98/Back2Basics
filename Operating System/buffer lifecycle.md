[[Operating System]] [[buffer]] [[buffer head]] [[buffer flags]] [[Buffer cache]] [[multiple levels of buffering]]

# Buffer lifecycle

> A kernel or application buffer moves through allocate → fill → optionally dirty → flush → reclaim — each transition has failure modes if the next stage is slower than the producer.

## Typical kernel block buffer

```txt
1. Allocate buffer head + attach to page ([[buffer head]])
2. Read or write fills memory — set uptodate / dirty ([[buffer flags]])
3. Background or explicit flush schedules I/O toward disk
4. I/O completion clears dirty, unlocks
5. Page reclaimed under memory pressure if clean
```

User-space buffers (socket, `stdio`) follow the same rhythm without buffer heads: malloc → append → `write()` → free or reuse.

## Interaction with stacked buffering

[[multiple levels of buffering]] mean a logical “flush” at one layer does not flush lower layers. `fflush()` does not [[fsync]]; TCP `close()` does not guarantee the peer persisted data.

## Reclaim and pressure

Clean [[Buffer cache]] pages are cheap to drop. Dirty pages must be written or discarded with care — writeback throttling prevents flooding slow disks. Under OOM, the kernel prefers dropping cache before killing processes.

## Questions for design reviews

- What happens on power loss mid-lifecycle?
- Which layer’s full buffer blocks the producer?
- Is there a bound on buffered bytes (backpressure)?

## Sources

- Linux kernel: `mm/page-writeback.c`, block layer writeback
- Robert Love, *Linux Kernel Development*
- Tanenbaum, *Modern Operating Systems* — I/O and buffering
