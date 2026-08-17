[[display server]] [[x11]] [[compositors]] [[Linux display manager]] [[xrandr]]

# wayland

> Display protocol where clients render locally and hand buffers to a compositor — the modern default on GNOME, KDE, and Sway.

```txt
        wayland ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Contrast with X11: compositor *is* the display server, no classic `DISPLAY`, …

## Sources
- [Wayland documentation](https://wayland.freedesktop.org/docs/html/) — deep-dive
- [Arch Wiki — Wayland](https://wiki.archlinux.org/title/Wayland) — overview

## Key Concepts
- **Compositor unity:** Mutter/KWin/Sway own protocol + pixels + often WM policy.
- **XWayland:** compatibility path for X11 clients.
- **Portals:** sandboxed screenshot/screen-share APIs.
- **Session type:** `XDG_SESSION_TYPE=wayland`.


- **Core:** Unlike X11’s separate server, the Wayland compositor combines display server,…

## Technical Details
```bash
echo $XDG_SESSION_TYPE
echo $WAYLAND_DISPLAY
loginctl show-session "$XDG_SESSION_ID" -p Type
GDK_BACKEND=x11 firefox
QT_QPA_PLATFORM=xcb some-qt-app
```

| Task | X11 | Wayland |
|------|-----|---------|
| Outputs | `xrandr` | Compositor CLI / Settings |
| Screenshots | `scrot`, `import` | `grim`, portal APIs |
| Clipboard | `xclip` | `wl-copy` / `wl-paste` |
| Remote GUI | `ssh -X` | RDP / VNC more common |

| Symptom | Check |
|---------|-------|
| Blank screen | `journalctl -b \| grep -i wayland` |
| Portal permission denied | `xdg-desktop-portal` running? |
| Fractional scaling issues | Compositor-specific; try integer scale |

## Mistakes to Avoid
- **Mistake:** Using only `xrandr` to debug pure Wayland output layout
- **Mistake:** Blaming Wayland for an XWayland-only crash
- **Mistake:** Expecting `ssh -X` to be the primary remote GUI path

## Pros/Cons or Trade-offs
- **Pro:** Better isolation and a simpler modern design than classic X.
- **Con:** Remote display and some global-grab workflows are less mature than X11 habits.

## Comparison
- vs [[x11]]: separate server + optional compositor vs unified compositor.
- vs [[compositors]]: on Wayland the compositor *is* the server role.


### Use cases
- Debug a GTK app that only fails under Wayland by forcing `GDK_BACKEND=x11` to…
