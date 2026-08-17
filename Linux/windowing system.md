[[display server]] [[x11]] [[wayland]] [[Linux window manager]] [[compositors]] [[Linux display manager]] [[i3 Window Manager Starter Guide]] [[X Desktop Group]] [[WM_CLASS]]

# windowing system

> The stack that turns application draw requests into pixels — display server, compositor, window manager, and toolkit glue.





## Interview Relevance
Layer cake question: DRM/KMS → display server → WM/shell → toolkit — and whether Wayland merges server+compositor.

## Sources
- [Freedesktop.org — Desktop](https://www.freedesktop.org/wiki/) — overview
- [Wayland architecture overview](https://wayland.freedesktop.org/architecture.html) — deep-dive

## Core Definition
On Linux this usually means a Wayland compositor *or* an X11 server plus window manager, sitting above DRM/KMS and GPU drivers.

## Key Concepts
- **Display server:** protocol endpoint ([[display server]]).
- **Compositor:** blend buffers / vsync ([[compositors]]).
- **Window manager:** focus, tiling, decorations ([[Linux window manager]]).
- **Display manager:** login greeter ([[Linux display manager]]).
- **Stacking vs tiling:** floating DE shells vs i3/Sway layouts.

## Technical Details
```
toolkit (GTK/Qt)
      │
window manager / shell (i3, GNOME Shell, KWin)
      │
display server (Wayland compositor or Xorg)
      │
GPU driver + DRM
```

| Layer | Role | Notes |
|-------|------|-------|
| Display server | Protocol endpoint | [[display server]] |
| Compositor | Blend buffers, vsync | Built into Wayland; optional on X11 |
| Window manager | Focus, tiling, decorations | [[Linux window manager]] |
| Display manager | Login greeter | [[Linux display manager]] |

- **Stacking** (GNOME, KDE): floating windows, task switcher.
- **Tiling** (i3, Sway): automatic layout — [[i3 Window Manager Starter Guide]].

## Real-World Applications
Pick Sway/i3 for keyboard-driven tiling on laptops, or GNOME/KDE when you need a full desktop shell and portal ecosystem.

## Pros/Cons or Trade-offs
- **Pro:** Clear separation of concerns (especially on X11) aids debugging.
- **Con:** Many moving parts; session type mismatches confuse tooling (`xrandr` on Wayland).

## Comparison
- vs [[display server]]: one layer of this stack.
- vs [[windowing system]] siblings [[x11]]/[[wayland]]: concrete protocols under this umbrella.

## Mistakes to Avoid
- Treating “windowing system,” “display server,” and “WM” as synonyms in interviews.
- Debugging the wrong layer (toolkit bug blamed on the compositor).
