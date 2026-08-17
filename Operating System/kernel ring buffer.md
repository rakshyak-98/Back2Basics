[[Operating System]] [[atomic ring buffer]] [[Rolling Buffer]] [[kernel subsystem]] [[right buffer]]

# Kernel ring buffer

> The kernel ring buffer is the fixed-size circular log where printk records land — what `dmesg` reads, especially before userspace logging is up.





## Interview Relevance
Ops debugging: early-boot messages, overflow/loss behavior, and how journald relates to the kernel buffer.

## Sources
- [Linux kernel docs — Printk](https://docs.kernel.org/core-api/printk-basics.html) — deep-dive
- Linux `dmesg(1)` manual page — overview
- [Wikipedia — Kernel log](https://en.wikipedia.org/wiki/Dmesg) — overview

## Key Concepts
- **Circular log:** [[atomic ring buffer]] / lock-protected records of printk text.
- **Readers:** `/dev/kmsg`, `dmesg`.
- **Overflow:** oldest messages drop (“lost N messages”).
- **Rate limits:** `printk_ratelimited` prevents floods.

## Technical Details
Drivers and [[kernel subsystem]]s call `printk()` at log levels. systemd-journald captures userspace too; the kernel buffer still bootstraps early boot before root mount.

```bash
dmesg -T -w
dmesg --level=err,warn
```

Contrast [[Rolling Buffer]] app logging and [[right buffer]] sizing.

## Real-World Applications
Driver bring-up, oops/panic triage, and “why did this disk disappear” postmortems.

## Pros/Cons or Trade-offs
- **Pro:** Always available early; bounded memory.
- **Con:** Silent loss under flood; not a durable audit log.
- **Trade-off:** larger log_buf vs RAM cost.

## Comparison
- vs journald: persistent/userspace structured logs vs early kernel ring.
- vs [[Rolling Buffer]]: same overwrite idea at app layer.

## Mistakes to Avoid
- Relying on dmesg alone for long-term audit.
- Flooding printk in hot paths until useful messages are lost.
- Forgetting timestamps (`-T`) when correlating with userspace logs.
