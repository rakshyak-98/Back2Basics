[[i3 Window Manager Starter Guide]] [[windowing system]] [[Linux display manager]] [[compositors]] [[x11]] [[wayland]] [[WM_CLASS]]

# Linux window manager

> The window manager controls focus, placement, decorations, and workspaces — the policy layer above the display server.

```txt
        Linux window manag ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Desktop architecture question: stacking vs tiling, X11 WM as a separate clien…

## Sources
- [i3wm.org](https://i3wm.org/) — overview
- [Sway — i3-compatible Wayland compositor](https://swaywm.org/) — overview

## Key Concepts
- **Policy vs pixels:** WM decides where windows go; compositor/display path paints them.
- **Stacking vs tiling:** Overlap freely vs non-overlapping splits.
- **Workspaces / virtual desktops:** Group windows by context.
- **WM_CLASS rules:** Match apps for assign/float — [[WM_CLASS]].
- **Session selection:** Display manager `.desktop` files start the WM/compositor chain.


- **Core:** A **window manager** (WM) handles keyboard shortcuts, stacking or tiling layo…

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

- Display managers (GDM, LightDM) session menus pick **GNOME**, **i3**, **Plasm…
- Each `/usr/share/xsessions/*.desktop` starts a WM/compositor chain.

## Mistakes to Avoid
- **Mistake:** Looking for a separate “window manager process” on Wayland the w…
- **Mistake:** Matching rules on transient window titles instead of `WM_CLASS`
- **Mistake:** Installing a WM package but never selecting its session in the d…

## Pros/Cons or Trade-offs
- **Pro:** Separating WM policy (on X11) lets you swap i3/Openbox without replacing the X server.
- **Con:** On Wayland you usually adopt a whole compositor stack — less mix-and-match. Tiling WMs trade approachability for speed.

## Comparison
- vs [[display server]]: server/protocol broker vs window policy. vs [[composit…


### Use cases
- A developer selects an i3 session at the greeter for keyboard tiling on X11
