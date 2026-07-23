[[display server]] [[windowing system]] [[x11]] [[wayland]] [[Linux configuration]]

# Linux display manager

> One-line: **Login greeter that starts your graphical session** — picks X11 vs Wayland and launches i3/GNOME/KDE. Breaks here looks like "boot loops to black screen" before any app runs.

## Mental model

The **display manager (DM)** runs as root early in boot, shows login UI, authenticates via PAM, then **execs user session** (startx, gnome-session, i3). It sets `$XDG_SESSION_TYPE`, `$DISPLAY` or `$WAYLAND_DISPLAY`, and often chooses the last session from `.xsession` or account settings.

```
boot → systemd graphical.target → gdm/lightdm/sddm
     → user login → ~/.xsession / DE session → compositor/Xorg
```

| DM | Common on | Notes |
|----|-----------|-------|
| GDM | GNOME default | Tight GNOME integration |
| LightDM | Ubuntu variants, i3 installs | Greeters: gtk, webkit |
| SDDM | KDE | Plasma default |
| none + startx | Minimal | Manual `startx` after tty login |

**Not a display server** — DM *starts* the session that talks to Xorg/Wayland compositor ([[display server]]).

## Standard config / commands

**See active DM (Debian/Ubuntu):**

```bash
cat /etc/X11/default-display-manager
# e.g. /usr/sbin/gdm3 or /usr/sbin/lightdm

systemctl status gdm3
systemctl status lightdm
```

**Switch default DM (Debian/Ubuntu):**

```bash
sudo dpkg-reconfigure gdm3
# or
sudo ln -sf /usr/sbin/lightdm /etc/X11/default-display-manager
sudo systemctl disable gdm3
sudo systemctl enable lightdm
sudo reboot
```

**Manual edit (know what you're doing):**

```bash
# /etc/X11/default-display-manager
/usr/sbin/lightdm
```

**i3/minimal session — user `~/.xsession` or `~/.xinitrc`:**

```bash
#!/bin/sh
exec i3
```

```bash
chmod +x ~/.xsession
# LightDM: choose "i3" or "default xsession" in greeter session menu
```

**Force X11 vs Wayland (GNOME greeter):** gear icon → "GNOME on Xorg" vs "GNOME".

**Disable DM for headless server:**

```bash
sudo systemctl set-default multi-user.target
sudo systemctl disable gdm3
```

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Boot to black screen | TTY Ctrl+Alt+F3; journal | `journalctl -u gdm3`; GPU driver |
| Login loop | `~/.xsession-errors` | Fix exec line; shell must not exit |
| Wrong DE started | Session file; greeter choice | `~/.xsession`; update-alternatives |
| Wayland app fails | Session type | Select Xorg session; check NVIDIA |
| Can't switch DM | Package installed? | `apt install lightdm`; reconfigure |
| Root login disabled | PAM/greeter policy | Expected; use normal user |

**Logs:**

```bash
journalctl -u lightdm -b
cat ~/.xsession-errors
```

## Gotchas

> [!WARNING]
> **`.xinitrc` vs `.xsession`** — DM-specific. LightDM reads `.xsession`; startx uses `.xinitrc`. Duplicate configs diverge.

> [!WARNING]
> **Editing default-display-manager without disable/enable** — two DMs fighting for VT — flicker, lockout.

- **Auto-login** — convenience vs physical security; LightDM `autologin-user=` in config drop-in.
- **Remote servers** — DM wastes RAM; use multi-user.target.

## When NOT to use

- **Headless/cloud instances** — no DM; SSH only.
- **Single-user embedded** — autostart compositor from systemd user unit instead.

## Related

[[display server]] [[windowing system]] [[x11]] [[wayland]] [[Linux configuration]] [[i3 Window Manager Starter Guide]]
