[[D-Bus]] [[Services commands]] [[Service masking]]

# bluetoothctl

> One-line: **BlueZ interactive CLI** — pair headsets, debug `org.bluez.Error.Busy`, and script BT when GUI applets lie about power state.

## Mental model

BlueZ exposes devices over **D-Bus** (`org.bluez`). `bluetoothctl` is the REPL front-end: power adapter, scan, pair, trust, connect. Desktop environments (GNOME/KDE) also talk to BlueZ — **two controllers fighting** causes Busy errors.

```
bluetoothctl → D-Bus → bluetoothd → kernel HCI → hardware
GNOME Settings ──┘ (same daemon — conflict if both "own" power)
```

| Command | Purpose |
|---------|---------|
| `power on/off` | Adapter radio |
| `scan on` / `devices` | Discovery |
| `pair` / `trust` / `connect` | Bond + auto-reconnect |
| `remove MAC` | Forget device |
| `info MAC` | RSSI, UUIDs, connected state |

## Standard config / commands

```bash
# Interactive session
bluetoothctl
# Inside:
power on
agent on
default-agent
scan on
# wait for device
pair AA:BB:CC:DD:EE:FF
trust AA:BB:CC:DD:EE:FF
connect AA:BB:CC:DD:EE:FF
quit
```

**One-shot scripting:**

```bash
bluetoothctl power on
bluetoothctl connect AA:BB:CC:DD:EE:FF
bluetoothctl --timeout 5 scan on
```

**Check daemon and adapter:**

```bash
systemctl status bluetooth
rfkill list bluetooth              # soft/hard block
hciconfig -a || bluetoothctl show  # adapter name, powered
busctl tree org.bluez              # D-Bus object tree
```

**Headless/server (usually disable):**

```bash
sudo systemctl stop bluetooth
sudo systemctl mask bluetooth      # see [[Service masking]]
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| `Failed to set power on: org.bluez.Error.Busy` | `rfkill`; GNOME BT applet | Kill conflicting UI; `rfkill unblock bluetooth`; restart `bluetooth` |
| Device pairs, won't connect | `info MAC`; profiles | `trust MAC`; remove + re-pair; check A2DP vs HID |
| No adapter found | `lsusb`; `dmesg` | Driver/firmware; VM USB passthrough |
| Scan finds nothing | `power on`; distance | Interference; device in pairing mode |
| Works until reboot | `trust` missing | `trust MAC`; check `/var/lib/bluetooth` |
| Audio choppy | PipeWire/Pulse | Not bluetoothctl — check `pactl` / wireplumber |

**Busy error playbook:**

```bash
rfkill unblock bluetooth
bluetoothctl power off
sleep 1
bluetoothctl power on
sudo systemctl restart bluetooth
# If still Busy: log out of GNOME session or stop gnome-bluetooth stack temporarily
```

## Gotchas

> [!WARNING]
> **Mask vs disable** — `systemctl stop` isn't enough if user session re-enables BT. Use [[Service masking]] on servers that must never expose BT.

> [!WARNING]
> **Pairing in SSH session** — need `agent on` and often physical confirm on device; no PIN UI over SSH.

- **Multiple adapters** — `select ADAPTER_MAC` in bluetoothctl before pair.
- **BLE vs classic** — IoT uses `bluetoothctl menu gatt`; different workflow from headphones.

## When NOT to use

- **Wi-Fi debugging** — unrelated stack; use `nmcli`, `iw`.
- **Production server hardening** — disable/mask BT entirely; no pairing on prod.
- **Bulk fleet provisioning** — use MDM/vendor tools, not manual bluetoothctl.

## Related

[[D-Bus]] [[Services commands]] [[Service masking]] [[busctl]] [[systemctl]]
