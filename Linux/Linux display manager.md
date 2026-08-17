[[login shell]] [[user management]] [[Linux window manager]] [[display server]]

# Linux display manager

> A display manager (DM) shows the graphical login greeter and starts the user’s X11 or Wayland session after authentication.

```txt
        Linux display mana ──┬── Interview
               ├── Sources
               ├── Concepts
               ├── Mechanism
               ├── Pitfalls
               ├── Trade-offs
               └── Comparison
```

## Interview Relevance
- **Interview probes:** Graphical login troubleshooting: GDM/SDDM/LightDM, PAM auth, session `.deskto…

## Sources
- [Arch Wiki — Display manager](https://wiki.archlinux.org/title/Display_manager) — overview
- `man 8 gdm` (and distro DM docs) — deep-dive

## Key Concepts
- **Greeter → session:** UI for user/password (or other PAM) then session start.
- **Session desktop files:** Declare `Exec=` for GNOME, i3, Plasma, etc.
- **X11 vs Wayland choice:** Often a menu on the greeter.
- **TTY fallback:** `Ctrl+Alt+F3` bypasses a broken graphics stack.
- **Logs:** `journalctl -u gdm` (or sddm/lightdm) plus `~/.xsession-errors`.


- **Core:** Examples: **GDM** (GNOME), **SDDM** (KDE), **LightDM** (generic)

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

- Text login alternative: TTY (`Ctrl+Alt+F3`), then `startx` or `dbus-run-sessi…

## Mistakes to Avoid
- **Mistake:** Debugging only the WM when the session never starts (DM/PAM fail…
- **Mistake:** Deleting session `.desktop` files instead of fixing `Exec=` paths
- **Mistake:** Forgetting autostart apps as a cause of instant logout loops

## Pros/Cons or Trade-offs
- **Pro:** Consistent graphical login, session selection, and PAM integration.
- **Con:** Extra moving part — a broken greeter can hide a healthy multi-user.target; TTY knowledge still required.

## Comparison
- vs [[login shell]]: DM starts a graphical session


### Use cases
- After a GPU driver update, GDM loops back to the greeter: switch to TTY, insp…
