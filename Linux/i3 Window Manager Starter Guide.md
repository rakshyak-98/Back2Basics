[[Linux window manager]] [[WM_CLASS]] [[x11]] [[terminal config]]

# i3 Window Manager Starter Guide

> i3 is a manual tiling window manager for X11 — keyboard-driven workspaces, splits, and a plain-text config at `~/.config/i3/config`.

Install: `sudo apt install i3` (Debian/Ubuntu). Select **i3** session from display manager at login.

## Essential keys (default)

| Key | Action |
|-----|--------|
| `$mod+Enter` | New terminal |
| `$mod+d` | Launcher (dmenu/rofi) |
| `$mod+Shift+q` | Kill window |
| `$mod+h/j/k/l` | Focus left/down/up/right |
| `$mod+Shift+h/j/k/l` | Move window |
| `$mod+1..0` | Switch workspace |
| `$mod+Shift+1..0` | Move window to workspace |

`$mod` is usually Alt or Super — set in config.

## Config snippet

```
set $mod Mod4
font pango:monospace 10
floating_modifier $mod
bindsym $mod+Return exec i3-sensible-terminal
bindsym $mod+d exec dmenu_run
```

Reload: `$mod+Shift+r`.

## Autostart

```
exec --no-startup-id picom
exec --no-startup-id nm-applet
```

## Rules with WM_CLASS

```
assign [class="Firefox"] workspace 2
```

See [[WM_CLASS]].

## Related

[[Linux window manager]] · [[compositors]] · [[x11]]

## Sources

- [i3 user guide](https://i3wm.org/docs/userguide.html)
