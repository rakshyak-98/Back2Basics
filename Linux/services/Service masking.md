[[systemctl]] [[Services commands]] [[systemd]] [[bluetoothctl]]

# Service masking

> Masking a systemd unit points it at `/dev/null` so it cannot start — stronger than disable for services that keep coming back.

---

## How it works

```txt
enabled  → starts at boot
disabled → no auto-start; manual start ok
masked   → /etc/systemd/system/foo.service → /dev/null
```

### Interview map (words you can say)

| Word | Plain meaning | Say in interview |
|------|---------------|------------------|
| **mask** | Symlink to `/dev/null` | “Start always fails until unmask.” |
| **disable** | Drop WantedBy links | “Manual start still works.” |
| **mask --now** | Stop + mask | “Immediate.” |
| **socket unit** | Activation path | “Mask socket too if it respawns.” |
| **list-unit-files** | See masked | “`--state=masked`.” |

---


## Configuration and commands

```bash
sudo systemctl mask --now bluetooth.service
systemctl status bluetooth.service
ls -l /etc/systemd/system/bluetooth.service
sudo systemctl unmask bluetooth.service
sudo systemctl enable --now bluetooth.service
systemctl list-unit-files --state=masked
# sockets
sudo systemctl mask --now cups.socket cups.service
```

| Knob | Why it matters |
|------|----------------|
| Mask in `/etc` | Beats vendor unit in `/lib` |
| Socket + service | Stops activation loops |

---


## When things break

| Symptom | Check | Fix |
|---------|-------|-----|
| `Loaded: masked` | status | `unmask` if needed |
| Starts despite mask | Alias/socket | Mask real unit names |
| Package re-enables | maintainer scripts | Mask again; divert |
| Can’t mask | Read-only `/usr` | Mask via `/etc/systemd/system` |

---


## Gotchas

> [!WARNING]
> **Masking sshd/networkd** can lock you out — keep console/serial.

> [!WARNING]
> **Mask ≠ uninstall** — binaries remain; remove package if attack surface matters.

---


## When not to use

- **Temporary stop** — `stop`/`disable` is enough.
- **Containers** — often no such units; don’t fight the image.

---


## Related

[[systemctl]] [[Services commands]] [[systemd]] [[bluetoothctl]]

## Sources

- [Wikipedia — Service masking](https://en.wikipedia.org/wiki/Service_masking)
