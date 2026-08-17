[[login shell]] [[user management]] [[Linux window manager]] [[display server]]

# Linux display manager

> A display manager (DM) shows the graphical login greeter and starts the user’s X11 or Wayland session after authentication.





## Interview Relevance
Graphical login troubleshooting: GDM/SDDM/LightDM, PAM auth, session `.desktop` files, and escaping a login loop via TTY when the greeter starts but the session dies.

## Sources
- [Arch Wiki — Display manager](https://wiki.archlinux.org/title/Display_manager) — overview
- `man 8 gdm` (and distro DM docs) — deep-dive

## Core Definition
Examples: **GDM** (GNOME), **SDDM** (KDE), **LightDM** (generic). The DM runs privileged, authenticates via PAM, then execs the session from `/usr/share/xsessions/*.desktop` or `/usr/share/wayland-sessions/`.

## Key Concepts
- **Greeter → session:** UI for user/password (or other PAM) then session start.
- **Session desktop files:** Declare `Exec=` for GNOME, i3, Plasma, etc.
- **X11 vs Wayland choice:** Often a menu on the greeter.
- **TTY fallback:** `Ctrl+Alt+F3` bypasses a broken graphics stack.
- **Logs:** `journalctl -u gdm` (or sddm/lightdm) plus `~/.xsession-errors`.

## Technical Details
```bash
systemctl status gdm
# or sddm, lightdm
journalctl -u gdm -b --no-pager | tail -50
```

```ini
# /usr/share/wayland-sessions/gnome-wayland.desktop (example)
[Desktop Entry]
Name=GNOME on Wayland
Exec=gnome-session
```

| Symptom | Check |
|---------|-------|
| Immediate logout after login | `~/.xsession-errors`, journal for session unit |
| Black screen | GPU driver; try X11 session vs Wayland |
| Wrong WM starts | Default session in DM config or `~/.dmrc` |
| Autostart crash | Rename `~/.config/autostart` temporarily |

Text login alternative: TTY (`Ctrl+Alt+F3`), then `startx` or `dbus-run-session gnome-session`.

## Real-World Applications
After a GPU driver update, GDM loops back to the greeter: switch to TTY, inspect `journalctl -u gdm`, force an X11 session once, then fix the Wayland/DRM issue.

## Pros/Cons or Trade-offs
- **Pro:** Consistent graphical login, session selection, and PAM integration.
- **Con:** Extra moving part — a broken greeter can hide a healthy multi-user.target; TTY knowledge still required.

## Comparison
vs [[login shell]]: DM starts a graphical session; getty + shell is text login. vs [[Linux window manager]]: DM selects and launches the session that contains the WM/compositor. vs [[display server]]: DM starts it; the display server then serves clients.

## Mistakes to Avoid
- Debugging only the WM when the session never starts (DM/PAM failure).
- Deleting session `.desktop` files instead of fixing `Exec=` paths.
- Forgetting autostart apps as a cause of instant logout loops.
