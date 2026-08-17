[[wayland]] [[x11]] [[compositors]] [[Linux display manager]] [[windowing system]] [[terminal emulator]]

# display server

> The display server is the broker between applications and the GPU — it owns input devices, window surfaces, and the path to the framebuffer clients draw into.

```txt
        display server ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Classic systems question: X11 vs Wayland, where the WM sits, and how to tell …

## Sources
- [Wayland (freedesktop.org)](https://wayland.freedesktop.org/) — overview
- [X.Org Wiki](https://wiki.x.org/) — deep-dive

## Key Concepts
- **Client → server → GPU:** Apps (GTK/Qt/SDL) speak a display protocol
- **X11 process:** Typically `Xorg` (or XWayland under Wayland).
- **Wayland compositor:** Mutter, Sway, KWin, Hyprland — server + compositor (+ often WM).
- **Session variables:** `DISPLAY=:0` (X11) vs `WAYLAND_DISPLAY=wayland-0`.
- **Display manager:** Greeter that starts the graphical session — [[Linux display manager]].


- **Core:** Linux desktops use **X11** (legacy network-transparent protocol) or **Wayland…

## Technical Details
```
applications (GTK/Qt/SDL)
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

| Topic | X11 | Wayland |
|-------|-----|---------|
| Server process | `Xorg` or XWayland | Compositor (Mutter, Sway, …) |
| Remote GUI | Native `ssh -X` | RDP/VNC more common |
| Screen capture | Mature (`xrandr`, X APIs) | Portal / compositor-specific |
| Global shortcuts | WM grabs keys | Compositor policy |
| Typical session var | `DISPLAY=:0` | `WAYLAND_DISPLAY=wayland-0` |

```bash
echo "$XDG_SESSION_TYPE"    # x11 or wayland
loginctl show-session $(loginctl | awk '/seat/ {print $1; exit}') -p Type
ps -e | grep -E 'Xorg|Xwayland|wayland'

xrandr --query
lspci -k | grep -A3 VGA
```

| Symptom | Check |
|---------|-------|
| Blank screen after login | [[Linux display manager]] logs: `journalctl -u gdm` |
| Apps only fail under Wayland | Try `GDK_BACKEND=x11 app` to isolate |
| Wrong DPI / scaling | Fractional scaling support varies by compositor |

## Mistakes to Avoid
- **Mistake:** Assuming `DISPLAY` is set under a pure Wayland session (or the r…
- **Mistake:** Debugging resolution with only `xrandr` on Wayland without compo…
- **Mistake:** Treating XWayland crashes as “Wayland is broken” without isolati…

## Pros/Cons or Trade-offs
- **Pro (Wayland):** Better isolation and simpler modern design
- **Con (Wayland):** Remote display and some capture/global-grab workflows are …
- **Pro (X11):** Decades of tooling and `ssh -X` habits.
- **Con (X11):** Weaker client isolation

## Comparison
- vs [[compositors]]: on Wayland they are the same role


### Use cases
- A developer hits a blank GDM screen after a GPU driver update: confirm sessio…
