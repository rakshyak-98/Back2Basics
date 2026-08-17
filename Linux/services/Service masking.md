[[systemctl]] [[Services commands]] [[systemd]] [[bluetoothctl]] [[commands/systemctl]]

# Service masking

> Points a systemd unit at `/dev/null` so it cannot start — stronger than disable for services that keep coming back.

```txt
        Service masking ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Classic systemd trap: disable vs mask, mask sockets too, and never mask sshd/…

## Sources
- [systemd.unit(5) — mask](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html) — deep-dive
- [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html) — overview

## Key Concepts
- **disable:** no auto-start; manual start still works.
- **mask:** symlink to `/dev/null` — start always fails until unmask.
- **`--now`:** stop immediately while masking.
- **Sockets:** mask `foo.socket` too if activation respawns the service.

## Technical Details
```txt
enabled  → starts at boot
disabled → no auto-start; manual start ok
masked   → /etc/systemd/system/foo.service → /dev/null
```

```bash
sudo systemctl mask --now bluetooth.service
systemctl status bluetooth.service
ls -l /etc/systemd/system/bluetooth.service
sudo systemctl unmask bluetooth.service
sudo systemctl enable --now bluetooth.service
systemctl list-unit-files --state=masked
sudo systemctl mask --now cups.socket cups.service
```

| Knob | Why it matters |
|------|----------------|
| Mask in `/etc` | Beats vendor unit in `/lib` |
| Socket + service | Stops activation loops |

| Symptom | Check | Fix |
|---------|-------|-----|
| `Loaded: masked` | status | `unmask` if needed |
| Starts despite mask | Alias/socket | Mask real unit names |
| Package re-enables | maintainer scripts | Mask again; divert |
| Can’t mask | Read-only `/usr` | Mask via `/etc/systemd/system` |

## Mistakes to Avoid
- **Mistake:** Masking sshd/networkd without console/serial
- **Mistake:** Masking only the `.service` when a `.socket` still activates it
- **Mistake:** Treating mask as uninstall

## Pros/Cons or Trade-offs
- **Pro:** Reliable “stay dead” against reactivation paths.
- **Con:** Easy lockout if you mask critical remote-access units.

## Comparison
- vs `disable`: softer; allows manual start.
- vs uninstall: mask leaves binaries; remove the package if attack surface matters.


### Use cases
- Hard-disable Bluetooth or CUPS on a locked-down server image so package scrip…
