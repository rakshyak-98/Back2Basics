[[Linux display manager]] [[login shell]] [[user management]]

# Linux display manager

> A display manager (DM) presents the graphical login greeter and starts the user's X11 or Wayland session.

Examples: **GDM** (GNOME), **SDDM** (KDE), **LightDM** (generic). The DM runs as root, authenticates via PAM, then execs the session script from `/usr/share/xsessions/*.desktop` or `/usr/share/wayland-sessions/`.

## Service control

```bash
systemctl status gdm
# or sddm, lightdm

journalctl -u gdm -b --no-pager | tail -50
```

## Session files

```ini
# /usr/share/wayland-sessions/gnome-wayland.desktop (example)
[Desktop Entry]
Name=GNOME on Wayland
Exec=gnome-session
```

## Troubleshooting login loop

| Symptom | Check |
|---------|-------|
| Immediate logout after login | `~/.xsession-errors`, journal for session unit |
| Black screen | GPU driver; try X11 session vs Wayland |
| Wrong WM starts | Default session in DM config or `~/.dmrc` |
| Autostart crash | Rename `~/.config/autostart` temporarily |

## Text login alternative

TTY login (`Ctrl+Alt+F3`) bypasses DM — useful when graphics stack is broken. Start GUI manually: `startx` or `dbus-run-session gnome-session`.

## Related

[[Linux window manager]] · [[display server]] · [[login shell]] · [[user management]]

## Sources

- `man 8 gdm`, distribution-specific DM docs
- [Arch Wiki — Display manager](https://wiki.archlinux.org/title/Display_manager)
