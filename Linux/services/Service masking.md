[[systemctl]] [[Services commands]] [[systemd]] [[bluetoothctl]]

# Service masking

> One-line: **`systemctl mask`** — make a unit **impossible** to start (symlink to `/dev/null`). Stronger than disable; use when packages, sockets, or user sessions keep resurrecting a service.

## Mental model

systemd unit states stack:

```
enabled  → starts at boot (wanted by target)
disabled → won't auto-start; manual start still works
masked   → unit file redirected to /dev/null — start ALWAYS fails
```

**Disable** removes symlinks in `/etc/systemd/system/*.wants/`. **Mask** replaces (or overlays) the unit with a null symlink so `systemctl start` cannot load real unit. Useful for **bluetooth**, **cups**, **ModemManager** on headless servers that get re-enabled on package upgrade.

```
/etc/systemd/system/bluetooth.service → /dev/null   (mask)
systemctl unmask → restores link to /lib/systemd/system/bluetooth.service
```

| Action | Boot start | Manual start |
|--------|------------|--------------|
| `stop` | if enabled, next boot | yes when enabled |
| `disable` | no | yes |
| `mask` | no | **no** |
| `mask --now` | no | stops + masks |

## Standard config / commands

```bash
# Mask and stop immediately
sudo systemctl mask --now bluetooth.service

# Verify — shows masked
systemctl status bluetooth.service
ls -l /etc/systemd/system/bluetooth.service
# → /dev/null

# Undo
sudo systemctl unmask bluetooth.service
sudo systemctl enable --now bluetooth.service   # if actually needed
```

**Common headless hardening:**

```bash
sudo systemctl mask --now \
  bluetooth.service \
  cups.service \
  avahi-daemon.service
```

**Socket-activated units:** mask **both** service and socket if reconnects persist:

```bash
sudo systemctl mask --now cups.socket cups.service
```

**Check what's enabled vs masked:**

```bash
systemctl list-unit-files --state=masked
systemctl is-enabled bluetooth.service    # masked | disabled | enabled
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Loaded: masked` | `systemctl status` | `unmask` if service required |
| Service starts despite mask | Template alias unit | Mask exact instance + socket |
| Package upgrade re-enables | maintainer scripts | Mask again; `dpkg-divert` or systemd drop-in `RefuseManualStart=yes` |
| Dependency pull-in | `systemctl list-dependencies` | Mask socket; adjust WantedBy in override |
| Can't mask vendor unit | Read-only /usr | Mask in `/etc/systemd/system/` (takes precedence) |

## Gotchas

> [!WARNING]
> **Masking sshd or networkd** — lockout. Always keep serial/console access.

> [!WARNING]
> **Mask vs remove package** — mask hides unit; binary still on disk. Uninstall if attack surface matters.

- **`disable` not enough** — D-Bus activations and socket units can still trigger service ([[bluetoothctl]] stack).
- **User units** — `systemctl --user mask`; separate from system mask.
- **WSL/containers** — some units don't exist; mask fails harmlessly or errors — check list-unit-files.

## When NOT to use

- **Temporary stop** — `stop` + `disable` suffices; unmask ceremony wastes time.
- **Override config** — prefer drop-in `/etc/systemd/system/foo.service.d/override.conf` for Exec changes.
- **Conflicts between two valid services** — use `systemctl disable` + alternative unit, not blanket mask without documentation.

## Related

[[systemctl]] [[Services commands]] [[systemd]] [[bluetoothctl]]
