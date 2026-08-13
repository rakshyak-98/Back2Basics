[[Linux window manager]] [[i3 Window Manager Starter Guide]] [[x11]] [[wayland]]

# Linux window manager

> The window manager controls focus, placement, decorations, and workspaces — the policy layer above the display server.

A **window manager** (WM) handles keyboard shortcuts, stacking or tiling layout, title bars, and workspace switching. On **X11** the WM is often a separate process talking to the X server. On **Wayland** the WM is usually part of the **compositor** (Sway, Mutter, KWin).

## Families

| Style | Examples | Protocol |
|-------|----------|----------|
| Stacking | Openbox, Metacity | X11 |
| Tiling | i3, bspwm | X11 |
| Dynamic tiling | Awesome, dwm | X11 |
| Wayland compositor+WM | Sway (i3-like), Hyprland | Wayland |

## WM_CLASS and rules

Applications set `WM_CLASS` for matching in WM config — see [[WM_CLASS]].

```bash
xprop WM_CLASS    # X11
```

i3 example:
```
for_window [class="Firefox"] move to workspace 2
```

## Switching window managers

Display manager (GDM, LightDM) session menu picks **GNOME**, **i3**, **Plasma**, etc. Each session file (`.desktop` in `/usr/share/xsessions/`) starts a WM/compositor chain.

## Related

[[i3 Window Manager Starter Guide]] · [[windowing system]] · [[Linux display manager]] · [[compositors]]

## Sources

- [i3wm.org](https://i3wm.org/)
- [Sway — i3-compatible Wayland compositor](https://swaywm.org/)
