[[display server]] [[x11]] [[windowing system]] [[Linux display manager]]

# Wayland

> One-line: **modern display protocol** — clients allocate buffers and pass FDs to the compositor; no global X11 server drawing model. **Debug sockets and env vars, not WM internals.**

## Mental model

**X11:** clients send drawing requests to X server; any client can snoop/input with enough tricks.

**Wayland:** clients render locally (GPU); compositor (Weston, Mutter, Sway, KWin) **alone** composites to screen. Security boundary = compositor.

```
App (GTK/Qt) ──► Wayland protocol ──► compositor (Mutter/Sway/…)
                         │                    │
                    SHM/dmabuf FDs       input + outputs
                         │
              $WAYLAND_DISPLAY → socket e.g. /run/user/1000/wayland-0
```

| | X11 | Wayland |
|---|-----|---------|
| Server | Xorg / Xwayland | Compositor is the display server |
| Remote GUI | SSH -X/-Y (fragile) | RDP/VNC/SSH no native draw forwarding |
| Screen capture | Many tools | Portal / compositor permission |
| Legacy X apps | Native | **Xwayland** translation layer |
| Debug env | `DISPLAY=:0` | `WAYLAND_DISPLAY=wayland-0` |

**i3 note:** classic **i3 is X11-only**. On Wayland stacks use **Sway** (i3-like) — see [[i3 Window Manager Starter Guide]] for tiling concepts; runtime differs.

## Standard config / commands

```bash
# Am I on Wayland?
echo $XDG_SESSION_TYPE          # wayland | x11
loginctl show-session $(loginctl | awk '/seat/ {print $1; exit}') -p Type

# Socket location
echo $WAYLAND_DISPLAY           # wayland-0
ls -la /run/user/$(id -u)/wayland-*

# Force X11 for one app (when Wayland breaks screen share / GPU)
GDK_BACKEND=x11 firefox
QT_QPA_PLATFORM=xcb some-qt-app

# Force Wayland-native (when available)
GDK_BACKEND=wayland gtk-app
MOZ_ENABLE_WAYLAND=1 firefox

# Xwayland processes (legacy X on Wayland session)
pgrep -a Xwayland
```

**Engineer debugging checklist:**

1. Session type (`XDG_SESSION_TYPE`).
2. Compositor name (`echo $XDG_CURRENT_DESKTOP`, `pgrep -a sway|mutter|kwin|weston`).
3. App toolkit backend (`GDK_BACKEND`, `QT_QPA_PLATFORM`).
4. Missing features → often **Xwayland** vs native Wayland port issue, not “Wayland broken”.

```bash
# PipeWire / portal (screen share on modern GNOME/KDE)
systemctl --user status pipewire wireplumber xdg-desktop-portal
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| App blank / no window | Run from terminal; `GDK_BACKEND=x11` trial | GPU driver; fractional scaling bug; try native vs Xwayland |
| Screen share fails (Zoom/Meet) | Portal running; Wayland vs X11 session | `xdg-desktop-portal-*`; use X11 session or updated client |
| `cannot open display` on Wayland | `WAYLAND_DISPLAY` unset | Start from compositor session; don’t copy X11 `DISPLAY` fix blindly |
| High CPU compositor | `top` compositor process | Disable client-side decorations; driver VSync; known compositor bugs |
| Remote dev no GUI | No SSH X forwarding on Wayland | VNC/RDP/waypipe; or X11 session on remote |
| i3 config “does nothing” on Sway | Wrong WM config format | Sway uses i3-*inspired* config, not drop-in i3 config |

## Gotchas

> [!WARNING]
> **`DISPLAY=:0` fixes don’t apply** when session is pure Wayland — need `WAYLAND_DISPLAY` or Xwayland bridge.

- **Xwayland hidpi:** blurry X apps on fractional scaling — run native Wayland build when exists.
- **Root GUI apps:** `sudo gui-app` breaks keyring and Wayland socket perms — use `pkexec` or proper user session.
- **WSLg / VMs:** socket paths and GPU passthrough differ; check distro-specific Wayland enablement.

## When NOT to use

- **Deep WM customization guide** — use compositor docs (Sway, Mutter, KDE).
- **Server/headless ops** — no display protocol; irrelevant except CI screenshots.
- **Replacing X11 knowledge overnight** — mixed fleets run both for years; know both env vars.

## Related

[[display server]] [[x11]] [[windowing system]] [[i3 Window Manager Starter Guide]] [[Linux display manager]] [[compositors]]
