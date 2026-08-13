[[wayland]] [[x11]] [[compositors]] [[Linux display manager]] [[terminal emulator]]

# display server

> The display server is the broker between applications and the GPU — it owns input devices, window placement, and the framebuffer clients draw into.

Linux desktops use either **X11** (legacy network-transparent protocol) or **Wayland** (modern protocol where the compositor merges display-server and compositor roles). The display server sits below the **window manager** and **desktop environment**.

```
applications (GTK/Qt//SDL)
        │
        ▼
display server (X11 or Wayland compositor)
        │
        ▼
kernel DRM/KMS + GPU driver
        │
        ▼
monitor
```

## X11 vs Wayland (operator view)

| Topic | X11 | Wayland |
|-------|-----|---------|
| Server process | `Xorg` or XWayland | Compositor (Mutter, Sway, …) |
| Remote GUI | Native `ssh -X` | RDP/VNC more common |
| Screen capture | Mature (`xrandr`, X APIs) | Portal / compositor-specific |
| Global shortcuts | WM grabs keys | Compositor policy |
| Typical session var | `DISPLAY=:0` | `WAYLAND_DISPLAY=wayland-0` |

## Identify what you are running

```bash
echo "$XDG_SESSION_TYPE"    # x11 or wayland
loginctl show-session $(loginctl | awk '/seat/ {print $1; exit}') -p Type
ps -e | grep -E 'Xorg|Xwayland|wayland'
```

## Debugging display issues

```bash
# Resolution and outputs (X11)
xrandr --query

# Wayland: compositor tools (GNOME example)
gsettings get org.gnome.mutter experimental-features

# GPU driver loaded?
lspci -k | grep -A3 VGA
```

| Symptom | Check |
|---------|-------|
| Blank screen after login | [[Linux display manager]] logs: `journalctl -u gdm` |
| Apps only fail under Wayland | Try `GDK_BACKEND=x11 app` to isolate |
| Wrong DPI / scaling | Fractional scaling support varies by compositor |

## Related

[[wayland]] · [[x11]] · [[windowing system]] · [[compositors]] · [[Linux display manager]]

## Sources

- [Wayland (freedesktop.org)](https://wayland.freedesktop.org/)
- [X.Org Wiki](https://wiki.x.org/)
