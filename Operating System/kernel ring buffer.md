[[loggging]] [[OOM (Linux Out Of Memory)]] [[Linux]] [[eBPF]]

# Kernel ring buffer

> Fixed-size circular log in kernel memory for `printk` and early-boot messages — consumed by `dmesg`, `journald`, and serial consoles.

---

## Mental model

The **kernel ring buffer** (often called **log buffer** or **dmesg buffer**) stores formatted text from `printk()`:

```txt
new message ──► [ oldest ... newest ] ──► overwrite oldest when full
                      ▲
                      └── dmesg / journald-kernel reads
```

Contents you'll see:
- Driver probe success/failure
- Hardware errors (AER, EDAC)
- [[OOM (Linux Out Of Memory)]] killer decisions
- **Early boot** before userspace logging starts
- Panic/oops stack traces

Separate from **userspace journal** (`journald`) but `journalctl -k` pulls kernel ring into structured logs.

---

## Standard config / commands

### Read kernel ring

```bash
dmesg -T                    # human timestamps (needs readable clock)
dmesg -w                    # follow (like tail -f)
dmesg -l err,warn           # filter levels

journalctl -k -b            # kernel log this boot
journalctl -k -p err..emerg --since today
```

### Buffer size

```bash
# Runtime size (bytes, power of two)
cat /proc/sys/kernel/printk_ratelimit
sudo sysctl kernel.dmesg_restrict   # 1 = non-root can't read (security)

# Some distros: log_buf_len boot param
grep log_buf /proc/cmdline
# Append to GRUB: log_buf_len=1M
```

### Rate limiting noisy printk

```bash
# Default ratelimit avoids flood — see dmesg "ratelimit" messages
echo 5 | sudo tee /proc/sys/kernel/printk_ratelimit_burst
```

**Why enlarge buffer:** boot storms on servers with many NVMe/NIC lines overwrite early errors before you capture them.

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Missing boot errors | Buffer wrapped | `log_buf_len`; serial console capture; IPMI SOL log |
| OOM but no killer line | Overwritten | `journalctl -k`; enable persistent journal |
| `dmesg: read kernel buffer failed` | `dmesg_restrict` | sudo or sysctl |
| Flood slows system | Driver printk in hot path | Fix driver; dynamic debug `echo 'module 0' > /sys/module/XXX/parameters/debug |

---

## Gotchas

> [!WARNING]
> **Ring buffer is finite** — intermittent hardware errors scroll away; use persistent logging for RCA.

> [!WARNING]
> **`dmesg -T` timestamps can lie** before RTC sync or in VMs.

> [!WARNING]
> **Not a structured audit trail** — no guaranteed ordering across CPUs without `printk` defer; use tracing ([[eBPF]]) for high-rate events.

---

## When NOT to use

Don't rely on kernel ring for **application logs** — use stdout/journal/centralized logging. Ring buffer is for **kernel/driver/hardware** narrative.

---

## Related

[[Rolling Buffer]] [[loggging]] [[OOM (Linux Out Of Memory)]] [[eBPF]] [[Linux]]
