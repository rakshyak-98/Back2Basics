[[Linux window manager]] [[WM_CLASS]] [[x11]] [[terminal config]] [[compositors]]

# i3 Window Manager Starter Guide

> i3 is a manual tiling window manager for X11 — keyboard-driven workspaces, splits, and a plain-text config at `~/.config/i3/config`.

```txt
        i3 Window Manager  ──┬── Why it matters
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Why It Matters
- **Key signal:** Desktop Linux depth check: tiling vs stacking, how session selection works vi…

## Sources
- [i3 user guide](https://i3wm.org/docs/userguide.html) — deep-dive
- [i3wm.org](https://i3wm.org/) — overview

## Key Concepts
- **Tiling tree:** Containers split; windows fill cells unless floating.
- **Workspaces:** Numbered (or named) virtual desktops.
- **$mod bindings:** All power-user actions hang off one modifier.
- **WM_CLASS rules:** `assign` / `for_window` match app classes — [[WM_CLASS]].
- **X11 only:** Native i3 targets X; Sway is the Wayland cousin.


- **Core:** i3 places windows in a tree of horizontal/vertical splits. You drive focus, m…

## Technical Details
- Install: `sudo apt install i3` (Debian/Ubuntu).
- Select **i3** from the display manager session menu.

| Key | Action |
|-----|--------|
| `$mod+Enter` | New terminal |
| `$mod+d` | Launcher (dmenu/rofi) |
| `$mod+Shift+q` | Kill window |
| `$mod+h/j/k/l` | Focus left/down/up/right |
| `$mod+Shift+h/j/k/l` | Move window |
| `$mod+1..0` | Switch workspace |
| `$mod+Shift+1..0` | Move window to workspace |

```
set $mod Mod4
font pango:monospace 10
floating_modifier $mod
bindsym $mod+Return exec i3-sensible-terminal
bindsym $mod+d exec dmenu_run

exec --no-startup-id picom
exec --no-startup-id nm-applet

assign [class="Firefox"] workspace 2
```

- Reload: `$mod+Shift+r`.

## Mistakes to Avoid
- **Mistake:** Editing config and logging out instead of `$mod+Shift+r` first
- **Mistake:** Matching on window title instead of stable `WM_CLASS`
- **Mistake:** Expecting i3 session files under Wayland sessions without Sway

## Pros/Cons or Trade-offs
- **Pro:** Fast, scriptable, minimal RAM vs full GNOME/KDE.
- **Con:** Steeper learning curve; poor fit for users who need rich DE integration out of the box. X11-only (use Sway on Wayland).

## Comparison
- vs GNOME/KDE: i3 is WM-centric


### Use cases
- Developers run i3 on workstations for keyboard-only window management, with P…
