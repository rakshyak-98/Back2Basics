[[display server]] [[GUI]] [[Linux window manager]] [[compositors]] [[WM_CLASS]]

# Windowing system

> One-line: **GUI stack that turns pixels into windows, icons, and input** — WIMP (windows, icons, menus, pointer) plus toolkits. Know the layers before blaming "Linux graphics."

## Mental model

The **windowing system** is the umbrella for everything between kernel evdev/GPU drivers and your application UI. It includes the **display server** ([[display server]]), **compositor** (optional but default now), **window manager**, **widget toolkit** (GTK/Qt), and **desktop environment** (GNOME/KDE).

```
App → GTK/Qt → Wayland/X11 protocol → compositor/WM → display server → driver → monitor
         ↑                                    ↑
    widgets/menus                      focus, stacking, decorations
```

| Layer | Examples | Responsibility |
|-------|----------|----------------|
| Toolkit | GTK4, Qt6 | Buttons, layouts, theming |
| Window manager | i3, Mutter, KWin | Focus, tiling, decorations |
| Compositor | Mutter, Picom, Sway | vsync, shadows, compositing |
| Display server | Xorg, Wayland compositor | Protocol + screen ownership |
| Display manager | GDM, LightDM | Login greeter — see [[Linux display manager]] |

**WIMP** — windows, icons, menus, pointer — describes the interaction model most DEs use; tiling WMs (i3, Sway) still fit under the same stack with different WM rules.

## Standard config / commands

**Identify your stack:**

```bash
echo $XDG_CURRENT_DESKTOP    # GNOME, KDE, i3
echo $XDG_SESSION_TYPE       # wayland | x11
echo $DESKTOP_SESSION
ps -e | grep -E 'mutter|kwin|i3|sway|Xorg'
```

**Toolkit/theme (GTK):**

```bash
gsettings get org.gnome.desktop.interface gtk-theme
# Qt5: qt5ct or KDE system settings
```

**Window rules (i3/Sway):** use `WM_CLASS` — see [[WM_CLASS]] for matching Chrome vs IDE instances.

**X11 multi-monitor:** `xrandr` — [[xrandr]]; Wayland: compositor settings (gnome-control-center).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| App UI frozen, SSH OK | Compositor CPU; TTY switch | Kill compositor extension; restart session |
| Wrong scaling / blur | Fractional scaling | Wayland vs X11; `GDK_SCALE` hacks on X |
| Window decorations missing | Client-side vs server-side | Install xdecorations; switch DE |
| Two monitors wrong layout | `xrandr --query` or Settings | Cable order; `xrandr --auto` |
| GTK vs Qt look mismatch | Theme engine | Install `adwaita-qt`; Kvantum |
| Game fullscreen issues | Compositor unredirect | Disable compositor for game; use Games mode |

## Gotchas

> [!WARNING]
> **Mixing X11 and Wayland sessions** — same user, different `$DISPLAY`/`WAYLAND_DISPLAY`; autostart scripts break.

> [!WARNING]
> **Picom/compton on NVIDIA** — tear/glint bugs; driver-specific GL backend settings.

- **Flatpak/Snap theming** — host GTK theme doesn't propagate without extra packages (`org.gtk.Gtk3theme.*`).
- **Remote desktop** — RDP/VNC sits below or beside native windowing; different input grab semantics.

## When NOT to use

- **Headless API servers** — no windowing stack required; don't install `ubuntu-desktop` on prod.
- **Embedded framebuffer** — direct DRM/KMS apps skip full WIMP stack.

## Related

[[display server]] [[GUI]] [[Linux window manager]] [[compositors]] [[WM_CLASS]] [[x11]] [[wayland]]
