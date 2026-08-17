[[Linux window manager]] [[WM_CLASS]] [[x11]] [[terminal config]] [[compositors]]

# i3 Window Manager Starter Guide

> i3 is a manual tiling window manager for X11 — keyboard-driven workspaces, splits, and a plain-text config at `~/.config/i3/config`.





## Interview Relevance
Desktop Linux depth check: tiling vs stacking, how session selection works via the display manager, and how `WM_CLASS` rules assign apps to workspaces.

## Sources
- [i3 user guide](https://i3wm.org/docs/userguide.html) — deep-dive
- [i3wm.org](https://i3wm.org/) — overview

## Core Definition
i3 places windows in a tree of horizontal/vertical splits. You drive focus, move, and workspace changes with a modifier key (`$mod`, usually Super). Reload config with `$mod+Shift+r` — no full DE required.

## Key Concepts
- **Tiling tree:** Containers split; windows fill cells unless floating.
- **Workspaces:** Numbered (or named) virtual desktops.
- **$mod bindings:** All power-user actions hang off one modifier.
- **WM_CLASS rules:** `assign` / `for_window` match app classes — [[WM_CLASS]].
- **X11 only:** Native i3 targets X; Sway is the Wayland cousin.

## Technical Details
Install: `sudo apt install i3` (Debian/Ubuntu). Select **i3** from the display manager session menu.

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

Reload: `$mod+Shift+r`.

## Real-World Applications
Developers run i3 on workstations for keyboard-only window management, with Picom for compositing and class rules pinning the browser to workspace 2.

## Pros/Cons or Trade-offs
- **Pro:** Fast, scriptable, minimal RAM vs full GNOME/KDE.
- **Con:** Steeper learning curve; poor fit for users who need rich DE integration out of the box. X11-only (use Sway on Wayland).

## Comparison
vs GNOME/KDE: i3 is WM-centric; those are full desktop environments. vs Sway: same mental model on Wayland. vs bspwm/dwm: same tiling family, different config languages (shell/C vs i3’s DSL).

## Mistakes to Avoid
- Editing config and logging out instead of `$mod+Shift+r` first.
- Matching on window title instead of stable `WM_CLASS`.
- Expecting i3 session files under Wayland sessions without Sway.
