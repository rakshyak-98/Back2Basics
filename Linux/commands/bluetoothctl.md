[[D-Bus]] [[Services commands]] [[Service masking]] [[busctl]] [[systemctl]]

# bluetoothctl

> bluetoothctl is the BlueZ interactive CLI — pair devices, debug Busy errors, and script Bluetooth when GUI applets lie about power state.





## Interview Relevance
Desktop/IoT niche: BlueZ over D-Bus, agent/pairing flow, and masking bluetooth on servers that must not radio-on.

## Sources
- [bluetoothctl(1)](https://man.archlinux.org/man/bluetoothctl.1) — deep-dive
- [BlueZ documentation](http://www.bluez.org/) — overview

## Core Definition
`bluetoothctl` talks to `bluetoothd` over D-Bus, which drives the kernel HCI stack. Same daemon backs GNOME Settings — conflicting “owners” of adapter power cause `org.bluez.Error.Busy`.

## Key Concepts
- **power / agent / scan / pair / trust / connect:** Usual pairing sequence.
- **Busy errors:** Another agent (GUI) holds the adapter.
- **Non-interactive:** `bluetoothctl` subcommands for scripts.
- **Servers:** Prefer [[Service masking]] so BT stays off.
- **SSH pairing:** Needs agent; physical confirm often required.

## Technical Details
```txt
bluetoothctl → D-Bus → bluetoothd → kernel HCI → hardware
GNOME Settings ──┘
```

```bash
bluetoothctl
# Inside:
power on
agent on
default-agent
scan on
pair AA:BB:CC:DD:EE:FF
trust AA:BB:CC:DD:EE:FF
connect AA:BB:CC:DD:EE:FF
quit

bluetoothctl power on
bluetoothctl connect AA:BB:CC:DD:EE:FF
bluetoothctl --timeout 5 scan on
```

| Symptom | Check | Fix |
|---------|-------|-----|
| org.bluez.Error.Busy | GUI agent | Close Settings; stop gnome-bluetooth; retry |
| Can’t pair over SSH | No agent/PIN UI | `agent on`; local confirm; don’t rely on SSH alone |
| Adapter missing | `bluetoothctl list`; rfkill | Unblock; load modules; hardware |
| Keeps re-enabling on server | user session | `systemctl mask bluetooth` |

## Real-World Applications
Pairing a headset when the GUI spinner lies, scripting a scan/connect for a kiosk, and masking Bluetooth on hardened servers.

## Pros/Cons or Trade-offs
- **Pro:** Direct control of BlueZ without the GUI.
- **Con:** Interactive UX; races with desktop agents; weak over SSH.
- **Trade-off:** Convenience radios on laptops vs mask-off on servers.

## Comparison
vs GUI Bluetooth panels: same daemon, different agent. vs [[busctl]]: lower-level D-Bus calls to `org.bluez`. vs Wi-Fi/`nmcli`: different radio stack.

## Mistakes to Avoid
- Fighting Busy without checking which agent owns the adapter.
- Leaving Bluetooth enabled on servers that don’t need it.
- Expecting headless SSH pairing without a confirm path.
