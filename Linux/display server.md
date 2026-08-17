[[wayland]] [[x11]] [[compositors]] [[Linux display manager]] [[windowing system]] [[terminal emulator]]

# display server

> The display server is the broker between applications and the GPU — it owns input devices, window surfaces, and the path to the framebuffer clients draw into.





## Interview Relevance
Classic systems question: X11 vs Wayland, where the WM sits, and how to tell which session type a host is running (`XDG_SESSION_TYPE`). Strong answers mention DRM/KMS and the display manager that starts the session.

## Sources
- [Wayland (freedesktop.org)](https://wayland.freedesktop.org/) — overview
- [X.Org Wiki](https://wiki.x.org/) — deep-dive

## Core Definition
Linux desktops use **X11** (legacy network-transparent protocol) or **Wayland** (modern protocol where the compositor merges display-server and compositor roles). The display server sits below the window manager / desktop environment and above kernel DRM/KMS + GPU drivers.

## Key Concepts
- **Client → server → GPU:** Apps (GTK/Qt/SDL) speak a display protocol; the server schedules buffers to the monitor.
- **X11 process:** Typically `Xorg` (or XWayland under Wayland).
- **Wayland compositor:** Mutter, Sway, KWin, Hyprland — server + compositor (+ often WM).
- **Session variables:** `DISPLAY=:0` (X11) vs `WAYLAND_DISPLAY=wayland-0`.
- **Display manager:** Greeter that starts the graphical session — [[Linux display manager]].

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

## Real-World Applications
A developer hits a blank GDM screen after a GPU driver update: confirm session type, check `journalctl -u gdm`, fall back to an X11 session or TTY while fixing DRM modules.

## Pros/Cons or Trade-offs
- **Pro (Wayland):** Better isolation and simpler modern design; less legacy X extension surface.
- **Con (Wayland):** Remote display and some capture/global-grab workflows are less mature than classic X11.
- **Pro (X11):** Decades of tooling and `ssh -X` habits.
- **Con (X11):** Weaker client isolation; every client can historically snoop more of the server.

## Comparison
vs [[compositors]]: on Wayland they are the same role; on X11 compositing is often separate. vs [[Linux window manager]]: WM is policy (focus, tiling); display server is the protocol/GPU broker. vs [[windowing system]]: broader stack term that includes server + WM + toolkit.

## Mistakes to Avoid
- Assuming `DISPLAY` is set under a pure Wayland session (or the reverse).
- Debugging resolution with only `xrandr` on Wayland without compositor tools.
- Treating XWayland crashes as “Wayland is broken” without isolating the X client.
