[[i3 Window Manager Starter Guide]] [[windowing system]] [[Linux display manager]] [[compositors]] [[x11]] [[wayland]] [[WM_CLASS]]

# Linux window manager

> The window manager controls focus, placement, decorations, and workspaces — the policy layer above the display server.

## Interview Relevance
Desktop architecture question: stacking vs tiling, X11 WM as a separate client vs Wayland compositor-includes-WM, and how display managers pick a session.

## Sources
- [i3wm.org](https://i3wm.org/) — overview
- [Sway — i3-compatible Wayland compositor](https://swaywm.org/) — overview

## Core Definition
A **window manager** (WM) handles keyboard shortcuts, stacking or tiling layout, title bars, and workspace switching. On **X11** the WM is often a separate process talking to the X server. On **Wayland** the WM is usually part of the **compositor** (Sway, Mutter, KWin).

## Key Concepts
- **Policy vs pixels:** WM decides where windows go; compositor/display path paints them.
- **Stacking vs tiling:** Overlap freely vs non-overlapping splits.
- **Workspaces / virtual desktops:** Group windows by context.
- **WM_CLASS rules:** Match apps for assign/float — [[WM_CLASS]].
- **Session selection:** Display manager `.desktop` files start the WM/compositor chain.

## Technical Details

| Style | Examples | Protocol |
|-------|----------|----------|
| Stacking | Openbox, Metacity | X11 |
| Tiling | i3, bspwm | X11 |
| Dynamic tiling | Awesome, dwm | X11 |
| Wayland compositor+WM | Sway (i3-like), Hyprland | Wayland |

```bash
xprop WM_CLASS    # X11
```

```
# i3 example
for_window [class="Firefox"] move to workspace 2
```

Display managers (GDM, LightDM) session menus pick **GNOME**, **i3**, **Plasma**, etc. Each `/usr/share/xsessions/*.desktop` starts a WM/compositor chain.

## Real-World Applications
A developer selects an i3 session at the greeter for keyboard tiling on X11; a colleague on Fedora picks GNOME on Wayland where Mutter is both compositor and WM.

## Pros/Cons or Trade-offs
- **Pro:** Separating WM policy (on X11) lets you swap i3/Openbox without replacing the X server.
- **Con:** On Wayland you usually adopt a whole compositor stack — less mix-and-match. Tiling WMs trade approachability for speed.

## Comparison
vs [[display server]]: server/protocol broker vs window policy. vs [[compositors]]: compositing blends buffers; on Wayland the same process often *is* the WM. vs desktop environment: DE = WM/compositor + panels, settings, apps (GNOME/KDE); bare WM is thinner.

## Mistakes to Avoid
- Looking for a separate “window manager process” on Wayland the way you would on X11.
- Matching rules on transient window titles instead of `WM_CLASS`.
- Installing a WM package but never selecting its session in the display manager.
