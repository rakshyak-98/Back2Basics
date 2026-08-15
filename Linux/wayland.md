[[display server]] [[x11]] [[compositors]] [[Linux display manager]] [[xrandr]]

# wayland

> Display protocol where clients render locally and hand buffers to a compositor — the modern default on GNOME, KDE, and Sway.

## Interview Relevance

Contrast with X11: compositor *is* the display server, no classic `DISPLAY`, and tooling (`wlr-randr`, portals) replaces `xrandr`/`xclip`.

## Sources

- [Wayland documentation](https://wayland.freedesktop.org/docs/html/) — deep-dive
- [Arch Wiki — Wayland](https://wiki.archlinux.org/title/Wayland) — overview

## Core Definition

Unlike X11’s separate server, the Wayland compositor combines display server, compositor, and often window management. Clients speak the Wayland wire protocol; use `WAYLAND_DISPLAY` (usually `wayland-0`), not `DISPLAY`.

## Key Concepts

- **Compositor unity:** Mutter/KWin/Sway own protocol + pixels + often WM policy.
- **XWayland:** compatibility path for X11 clients.
- **Portals:** sandboxed screenshot/screen-share APIs.
- **Session type:** `XDG_SESSION_TYPE=wayland`.

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

## Real-World Applications

Debug a GTK app that only fails under Wayland by forcing `GDK_BACKEND=x11` to isolate XWayland vs native paths.

## Pros/Cons or Trade-offs

- **Pro:** Better isolation and a simpler modern design than classic X.
- **Con:** Remote display and some global-grab workflows are less mature than X11 habits.

## Comparison

- vs [[x11]]: separate server + optional compositor vs unified compositor.
- vs [[compositors]]: on Wayland the compositor *is* the server role.

## Mistakes to Avoid

- Using only `xrandr` to debug pure Wayland output layout.
- Blaming Wayland for an XWayland-only crash.
- Expecting `ssh -X` to be the primary remote GUI path.
