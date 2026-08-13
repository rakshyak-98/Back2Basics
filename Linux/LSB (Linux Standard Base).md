<!-- note-strategy: operational -->
[[Linux]] [[systemd]] [[inittramfs]]

# LSB (Linux Standard Base)

> LSB (Linux Standard Base) tried to standardize paths, runlevels, and package shapes across distros — today you mostly meet legacy `/etc/init.d` scripts and `lsb_release`.

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

**Say it in one breath:** LSB = old compatibility layer; modern operations speak systemd units and FHS paths, not LSB runlevels.

```txt
legacy: /etc/init.d/foo start   (LSB headers)
modern: systemctl start foo     (unit files)
FHS:    /usr /var /etc /home    (still relevant)
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **LSB** | Distro compatibility spec | “Mostly historical; systemd won PID 1.” |
| **`lsb_release`** | Print distro id | “Codename for apt suites.” |
| **init.d script** | SysV-style service | “May be wrapped by systemd generators.” |
| **FHS** | Filesystem layout | “Where binaries/configs/logs live.” |
| **runlevel** | SysV mode number | “Mapped to systemd targets.” |

---

## Standard config / commands

```bash
lsb_release -a
cat /etc/os-release
ls /etc/init.d | head
systemctl cat ssh
# LSB header example inside init.d:
# ### BEGIN INIT INFO
# Provides: …
# ### END INIT INFO
```

| Knob | Why it matters |
|------|----------------|
| `/etc/os-release` | Prefer over parsing `uname` |
| systemd targets | Replaces runlevels |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `service foo start` odd | systemd wrapper | Use `systemctl` status/logs |
| Script ignored at boot | No enable / generator | Create real unit or enable |
| Wrong codename in docs | `/etc/os-release` | Trust VERSION_CODENAME |
| Vendor assumes LSB paths | Non-FHS layout | Symlink or fix package |

---

## Gotchas

> [!WARNING]
> **LSB compliance claims ≠ portable packages** — test on the target distro.

> [!WARNING]
> **`/etc/init.d` still present** doesn’t mean SysV is PID 1 — systemd often emulates it.

---

## When NOT to use

- **New services** — write systemd units, not LSB initialize scripts.
- **Container images** — skip LSB tooling; use `/etc/os-release`.

---

## Related

[[systemd]] [[SYSV (System V)]] [[systemctl]] [[system service unit files]]
