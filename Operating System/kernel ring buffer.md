[[Operating System]] [[atomic ring buffer]] [[Rolling Buffer]] [[kernel subsystem]] [[right buffer]]

# Kernel ring buffer

> The kernel ring buffer is the fixed-size circular log where printk records land — what you read with dmesg before structured logging took over in many setups.

Implemented as a lock-protected or atomic [[atomic ring buffer]] of text records. Drivers and subsystems call `printk()` at various log levels; userspace reads `/dev/kmsg` or runs `dmesg`.

## Behavior under load

- **Overflow** — oldest messages may drop with “lost N messages” notice.
- **Rate limiting** — `printk_ratelimited` prevents floods.
- **Persistent journal** — systemd-journald also captures userspace; kernel buffer still bootstraps early boot before root mount.

```bash
dmesg -T -w
dmesg --level=err,warn
```

Contrast [[Rolling Buffer]] in application logging and [[right buffer]] sizing for latency-sensitive capture.

## Sources

- Linux kernel documentation: [Printk](https://docs.kernel.org/core-api/printk-basics.html)
- Linux `dmesg(1)` manual page
- Wikipedia: [Kernel log](https://en.wikipedia.org/wiki/Kernel_log)
