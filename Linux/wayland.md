[[display server]] [[x11]] [[compositors]] [[Linux display manager]]

# wayland

> Wayland is a display protocol where clients render locally and hand buffers to a compositor — the modern default on GNOME, KDE, and tiling compositors like Sway.

Unlike X11's separate server, the **Wayland compositor** combines display server, compositor, and often window management. Clients talk Wayland wire protocol; there is no `DISPLAY` — use `WAYLAND_DISPLAY` (usually `wayland-0`).

## Identify session

```bash
echo $XDG_SESSION_TYPE    # wayland
echo $WAYLAND_DISPLAY
loginctl show-session "$XDG_SESSION_ID" -p Type
```

## Tooling differences from X11

| Task | X11 | Wayland |
|------|-----|---------|
| Outputs | `xrandr` | Compositor CLI (`wlr-randr`, GNOME Settings) |
| Screenshots | `scrot`, `import` | `grim`, portal APIs |
| Clipboard | `xclip` | `wl-copy` / `wl-paste` |
| Remote GUI | `ssh -X` | RDP (`gnome-remote-desktop`), VNC |

## Run X apps on Wayland

**XWayland** translates X11 clients. If an app misbehaves, test:

```bash
GDK_BACKEND=x11 firefox
QT_QPA_PLATFORM=xcb some-qt-app
```

## Debugging

| Symptom | Check |
|---------|-------|
| Blank screen | Compositor logs: `journalctl -b \| grep -i wayland` |
| Permission denied portal | `xdg-desktop-portal` running? |
| Fractional scaling issues | Compositor-specific; some apps need integer scale |

## Related

[[display server]] · [[x11]] · [[compositors]] · [[Linux display manager]]

## Sources

- [Wayland.freedesktop.org](https://wayland.freedesktop.org/docs/html/)
- [Arch Wiki — Wayland](https://wiki.archlinux.org/title/Wayland)
