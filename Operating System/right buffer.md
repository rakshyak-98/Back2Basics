[[Operating System]] [[kernel ring buffer]] [[buffer]] [[Rolling Buffer]]

# Right buffer

> Linux kernel log ring (`dmesg`) — fixed circular buffer of recent kernel messages; oldest lines drop when full.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** Drivers/`printk` append to a RAM ring; userspace reads via `dmesg` or `/dev/kmsg`; journald may mirror it.

```txt
printk ──► kernel ring buffer (fixed size)
              ├─ dmesg / /dev/kmsg
              └─ wrap ⇒ overwrite old
```

> Name in this vault is historical; behavior = [[kernel ring buffer]].

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **Kernel ring buffer** | Circular log in RAM | “Early boot + driver noise lives here.” |
| **`printk`** | Kernel printf | “Levels from emerg to debug.” |
| **`dmesg`** | Dump the ring | “First stop for ‘disk not seen’.” |
| **`/dev/kmsg`** | Character device API | “journald reads this.” |
| **Wrap** | Overwrite oldest | “Quiet storms lose early clues.” |
| **Rate limit** | printk throttling | “Identical storms get suppressed.” |

### How the story goes

1. **Event** — driver/kernel calls `printk`.
2. **Store** — append; drop oldest if full.
3. **Consume** — `dmesg`, serial console, journal.
4. **Persist** — only if userspace ships logs elsewhere.

---

## Standard config / commands

```bash
dmesg -T
dmesg -w                  # follow
sudo dmesg -C             # clear (needs priv)
cat /dev/kmsg | head
# Size (bytes) — example path
cat /sys/kernel/config/... 2>/dev/null
# Common: log_buf_len= boot arg / CONFIG_LOG_BUF_SHIFT
journalctl -k -b
```

| Knob | Why it matters |
|------|----------------|
| `log_buf_len` | Survive noisy boot |
| console loglevel | What hits serial |
| `printk.devkmsg` | Userspace restrict |
| journal persistent | Keep after reboot |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Missing early panic | Ring wrapped / no serial | Larger buf; netconsole/serial |
| Empty `dmesg` as user | Permissions | `sudo` or `kernel.dmesg_restrict=0` (lab) |
| Flood hides root cause | Rate limit / wrap | Reproduce quieter; capture ASAP |
| “No disk” mystery | `dmesg \| grep -i sd` | Driver/firmware clues |
| Duplicate with journal | Both read kmsg | Prefer `journalctl -k` in systemd hosts |
| Lost after reboot | RAM only | Persist via journal/rsyslog |

---

## Gotchas

> [!WARNING]
> **Not durable** — reboot clears unless something archived it.

> [!WARNING]
> **Timestamps** — raw vs `-T` vs journal; correlate carefully.

> [!WARNING]
> **Secrets** — some drivers print paths/keys; treat logs as sensitive.

> [!WARNING]
> **Alias** — prefer linking [[kernel ring buffer]] in new notes; keep this file for old wikilinks.

---

## When NOT to use

- **App logs** — stdout/journal user facilities, not `printk`.
- **Long-term audit** — ship to SIEM; don’t rely on the ring.
- **Userspace ring buffers** — see [[atomic ring buffer]] / [[Rolling Buffer]].

---

## Related

[[kernel ring buffer]] [[buffer]] [[Rolling Buffer]] [[atomic ring buffer]] [[system call]] [[TTY (teletypewriter)]]
