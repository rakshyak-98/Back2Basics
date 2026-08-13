[[display server]] [[x11]] [[wayland]] [[Linux window manager]]

# windowing system

> The windowing system is the stack that turns application draw requests into pixels on screen — display server, compositor, window manager, and toolkit glue.

On Linux this usually means **Wayland compositor** *or* **X11 server + window manager**, sitting above **DRM/KMS** in the kernel and GPU drivers.

```
toolkit (GTK/Qt)
      │
window manager / shell (i3, GNOME Shell, KWin)
      │
display server (Wayland compositor or Xorg)
      │
GPU driver + DRM
```

## Major components

| Layer | Role | Notes |
|-------|------|-------|
| **Display server** | Protocol endpoint | [[display server]] |
| **Compositor** | Blend buffers, vsync | Built into Wayland; optional on X11 — [[compositors]] |
| **Window manager** | Focus, tiling, decorations | [[Linux window manager]] |
| **Display manager** | Login greeter | [[Linux display manager]] |

## Desktop vs tiling

- **Stacking** (GNOME, KDE): floating windows, task switcher.
- **Tiling** (i3, Sway): automatic layout — see [[i3 Window Manager Starter Guide]].

## Related

[[x11]] · [[wayland]] · [[X Desktop Group]] · [[WM_CLASS]]

## Sources

- [Freedesktop.org — Desktop integration](https://www.freedesktop.org/wiki/)
