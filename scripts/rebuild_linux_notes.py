#!/usr/bin/env python3
"""Rebuild remaining Linux vault notes — no template boilerplate."""
from pathlib import Path

LINUX = Path("/workspace/Linux")

NOTES = {
"Linux Templates Directory.md": '''[[Linux configuration]] [[etc files]] [[apt config]]

# Linux Templates Directory

> Distribution packages ship template files under `/usr/share` and `/etc` — copy or use `debconf`/`systemd` drop-ins instead of editing vendor copies that upgrades overwrite.

Debian-family packages often place **conffiles** in `/etc` and pristine templates in `/usr/share/doc/` or `/usr/share/<package>/`. Red Hat uses `%config` RPM semantics similarly.

## Patterns

| Pattern | Example |
|---------|---------|
| `*.dpkg-dist` / `*.rpmnew` | Left after package manager merge conflict |
| `/etc/skel/` | Template for new user home directories |
| `/usr/lib/tmpfiles.d/` | systemd path creation rules |
| `/usr/share/alsa/` | Default ALSA card profiles — [[alsa]] |

## Safe customization

```bash
# systemd: never edit /usr/lib unit directly
sudo systemctl edit nginx.service

# Apache-style
# /etc/nginx/nginx.conf includes sites-enabled/
```

## After package upgrade

```bash
sudo apt list --upgradable
# Resolve .dpkg-* diffs with vimdiff or dpkg --configure -a
```

## Related

[[etc files]] · [[Linux configuration]] · [[management/Package Manager]]

## Sources

- Debian Policy Manual — conffiles
- `man 5 tmpfiles.d`
''',

"editor config.md": '''[[terminal config]] [[Linux terminal]] [[gnome Colorschem]]

# editor config

> Editor configuration lives in dotfiles and LSP settings — align `EDITOR`, terminal capabilities, and language servers for consistent editing on servers and laptops.

## Environment

```bash
export EDITOR=vim
export VISUAL=vim
```

Many tools (`crontab -e`, `git commit`) honor `$EDITOR`.

## Vim / Neovim

```vim
" ~/.vimrc or ~/.config/nvim/init.lua
set number relativenumber
set expandtab shiftwidth=2 softtabstop=2
syntax on
```

## SSH remote editing

```bash
vim scp://user@host//etc/nginx/nginx.conf
# or local + rsync
```

## Related

[[terminal config]] · [[Scripting]]

## Sources

- `man 1 vim`
- [Neovim documentation](https://neov.io/doc/)
''',

"apt package manager.md": '''[[apt config]] [[management/Package Manager]] [[APT policy]] [[FileManagement/source list file]]

# apt package manager

> APT is Debian and Ubuntu's high-level package manager — it resolves dependencies from configured repositories and tracks installed `.deb` state.

**APT** (Advanced Package Tool) wraps `dpkg`. Commands: `apt update` refreshes index; `apt install` fetches and configures packages; `apt upgrade` applies newer versions.

## Daily commands

```bash
sudo apt update
sudo apt upgrade
sudo apt install nginx
apt search prometheus
apt show curl
apt list --installed | grep docker
```

## Hold / pin versions

```bash
sudo apt-mark hold package-name
apt-cache policy package-name   # see [[APT policy]]
```

## Remove and clean

```bash
sudo apt remove nginx
sudo apt purge nginx          # plus config files
sudo apt autoremove
sudo apt clean
```

## Debugging

| Symptom | Fix |
|---------|-------|
| `Unable to locate package` | `apt update`; check [[FileManagement/source list file]] |
| `dpkg was interrupted` | `sudo dpkg --configure -a` |
| Broken dependencies | `sudo apt -f install` |
| Lock held | `sudo lsof /var/lib/dpkg/lock-frontend` |

## Related

[[apt config]] · [[management/Package deferred]] · [[management/Package Manager]]

## Sources

- [apt(8) man page](https://manpages.debian.org/apt)
- [Debian APT User's Guide](https://www.debian.org/doc/manuals/apt-guide/)
''',

"apt config.md": '''[[apt package manager]] [[FileManagement/source list file]] [[etc files]]

# apt config

> APT configuration merges defaults from `/etc/apt/apt.conf` and snippets in `/etc/apt/apt.conf.d/` — proxies, pinning, and acquire behavior live here.

Main repository list: `/etc/apt/sources.list` and `/etc/apt/sources.list.d/*.list` — see [[FileManagement/source list file]].

## Common snippets

```bash
# /etc/apt/apt.conf.d/99custom
APT::Install-Recommends "false";
Acquire::http::Proxy "http://proxy.corp:8080/";
```

## Pinning (version preference)

```
# /etc/apt/preferences.d/nginx
Package: nginx
Pin: version 1.24.*
Pin-Priority: 1001
```

See [[APT policy]] for priority semantics.

## Verify effective config

```bash
apt-config dump | grep -i proxy
apt-cache policy nginx
```

## Related

[[apt package manager]] · [[APT policy]]

## Sources

- `man 5 apt.conf`
- `man 5 sources.list`
''',

"alsa.md": '''[[Linux terminal]] [[commands/fonts commands]]

# alsa

> ALSA (Advanced Linux Sound Architecture) is the kernel sound layer — `aplay`, `amixer`, and `/proc/asound` expose cards and PCM devices to userspace.

Desktop sessions often route through **PipeWire** or **PulseAudio**, which still talk to ALSA devices underneath.

## List devices

```bash
aplay -l
arecord -l
cat /proc/asound/cards
```

## Volume and mute

```bash
amixer scontrols
amixer set Master 80%
amixer set Master mute
alsamixer    # TUI
```

## Test playback

```bash
speaker-test -c 2 -t wav
aplay /usr/share/sounds/alsa/Front_Center.wav
```

## Troubleshooting

| Symptom | Check |
|---------|-------|
| No sound after HDMI connect | `pactl list sinks` or re-plug; set default sink |
| Device busy | `lsof /dev/snd/*` |
| Wrong card default | `/etc/asound.conf` or `~/.asoundrc` |

## Related

[[Linux configuration]] · [[gnome Colorschem]]

## Sources

- [ALSA project documentation](https://www.alsa-project.org/wiki/Documentation)
- `man 1 amixer`, `man 1 aplay`
''',

"NTP sync.md": '''[[Linux configuration]] [[etc files]] [[services/systemd]]

# NTP sync

> NTP synchronization keeps clock skew within bounds — TLS, Kerberos, and distributed logs break when hosts disagree on time.

Modern Debian/Ubuntu use **systemd-timesyncd**; servers may run **chrony** or **ntpd**. Cloud VMs should sync to hypervisor or metadata NTP.

## systemd-timesyncd

```bash
timedatectl status
timedatectl show-timesync --all
systemctl status systemd-timesyncd
```

`/etc/systemd/timesyncd.conf`:
```ini
[Time]
NTP=ntp.example.com
FallbackNTP=time.google.com
```

## chrony (common on servers)

```bash
chronyc tracking
chronyc sources -v
```

## Verify

```bash
date -u
timedatectl
# offset should be sub-millisecond for chrony when tracked
```

## Related

[[commands/date]] · [[services/systemd]]

## Sources

- [systemd-timesyncd(8)](https://www.freedesktop.org/software/systemd/man/latest/systemd-timesyncd.service.html)
- [chrony documentation](https://chrony-project.org/documentation.html)
''',

"nvidia-smi.md": '''[[commands/lspci]] [[management/Linux resource management]]

# nvidia-smi

> `nvidia-smi` queries NVIDIA GPU driver state — utilization, memory, temperature, and processes using the device.

Requires proprietary or open NVIDIA kernel module loaded. Part of NVIDIA driver install on Linux.

## Quick status

```bash
nvidia-smi
watch -n1 nvidia-smi

# Query fields
nvidia-smi --query-gpu=name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv
```

## Processes on GPU

```bash
nvidia-smi pmon -c 1
fuser -v /dev/nvidia*
```

## Persistence / compute mode

```bash
sudo nvidia-smi -pm 1
nvidia-smi -c EXCLUSIVE_PROCESS   # caution in shared hosts
```

## Troubleshooting

| Symptom | Check |
|---------|-------|
| `NVIDIA-SMI has failed` | Driver not loaded: `lsmod | grep nvidia`; DKMS build |
| ECC errors | `nvidia-smi -q -d ECC` |
| MIG partitions | `nvidia-smi mig -lgip` (A100/H100 class) |

## Related

[[commands/lspci]] · [[process]]

## Sources

- [NVIDIA SMI documentation](https://docs.nvidia.com/deploy/nvidia-smi/)
''',

"systemd-hostnamed.md": '''[[services/systemd]] [[Linux configuration]]

# systemd-hostnamed

> `systemd-hostnamed` is a D-Bus service that sets transient hostname, static hostname, and icon/chassis metadata — `hostnamectl` is the CLI front end.

## Commands

```bash
hostnamectl status
sudo hostnamectl set-hostname app01.example.com
sudo hostnamectl set-hostname app01 --static
sudo hostnamectl set-hostname edge --transient
```

## Files involved

| Source | File |
|--------|------|
| Static | `/etc/hostname` |
| Pretty | `/etc/machine-info` (`PRETTY_HOSTNAME`) |
| Transient | kernel hostname (until reboot) |

## Service

```bash
systemctl status systemd-hostnamed
busctl introspect org.freedesktop.hostname1
```

## Related

[[services/D-Bus]] · [[commands/busctl]] · [[etc files]]

## Sources

- [hostnamectl(1)](https://www.freedesktop.org/software/systemd/man/latest/hostnamectl.html)
- [org.freedesktop.hostname1](https://www.freedesktop.org/software/systemd/man/latest/org.freedesktop.hostname1.html)
''',

"supervisorctl.md": '''[[services/systemd]] [[process]]

# supervisorctl

> Supervisor is a Python process control system — `supervisorctl` starts, stops, and tails logs for programs defined in `supervisord.conf` when systemd is not the chosen supervisor.

Common in legacy Python deployments. Modern Linux services prefer **systemd units** ([[system service unit files]]).

## Config sketch

```ini
[program:web]
command=/var/www/venv/bin/gunicorn app:app
directory=/var/www
autostart=true
autorestart=true
stdout_logfile=/var/log/web.log
```

## Control

```bash
sudo supervisorctl status
sudo supervisorctl restart web
sudo supervisorctl tail -f web
sudo supervisorctl reread && sudo supervisorctl update
```

## vs systemd

| Feature | Supervisor | systemd |
|---------|------------|---------|
| Socket activation | no | yes |
| Journal integration | file logs | [[journalctl]] |
| Dependency graph | limited | native |

## Related

[[services/systemd]] · [[process]]

## Sources

- [Supervisor documentation](http://supervisord.org/)
''',

"fresh system sudo setup.md": '''[[user management]] [[commands/visudo]] [[Authentication command]]

# fresh system sudo setup

> On a fresh Linux system, configure sudo so administrators can elevate safely — group membership, `visudo` edits, and optional passwordless rules for automation.

## Debian/Ubuntu default

Users in **`sudo`** group get full sudo (password prompt):

```bash
sudo usermod -aG sudo alice
id alice    # must re-login
```

## Edit sudoers safely

```bash
sudo visudo
# NEVER edit /etc/sudoers with plain vim without lock
```

Example — allow service restart only:

```
deploy ALL=(ALL) NOPASSWD: /bin/systemctl restart myapp.service
```

## Validate

```bash
sudo -l -U alice
sudo -k && sudo true    # test password path
```

## Hardening

- No `NOPASSWD: ALL` in production without break-glass policy.
- Use `/etc/sudoers.d/` drop-in files with mode `0440`.
- Log: `/var/log/auth.log` or `journalctl _COMM=sudo`.

## Related

[[user management]] · [[visudo]] · [[passwd]]

## Sources

- `man 5 sudoers`
- [sudo.ws documentation](https://www.sudo.ws/docs/)
''',

"gnome Colorschem.md": '''[[commands/gsetting]] [[terminal config]] [[Linux configuration]]

# gnome Colorschem

> GNOME color schemes and accent colors are stored in GSettings — `gsettings` and `dconf` change GTK theme and dark/light preference for the desktop session.

## Read settings

```bash
gsettings get org.gnome.desktop.interface color-scheme
gsettings get org.gnome.desktop.interface gtk-theme
gsettings range org.gnome.desktop.interface color-scheme
```

Values (GNOME 42+): `'default'`, `'prefer-dark'`, `'prefer-light'`.

## Set dark mode

```bash
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
```

## Terminal profile

GNOME Terminal profiles are separate schemas — use GUI or `dconf dump /org/gnome/terminal/`.

## Related

[[commands/gsetting]] · [[commands/customization]] · [[terminal config]]

## Sources

- [GNOME Human Interface Guidelines — appearance](https://developer.gnome.org/hig/)
- `man 1 gsettings`
''',

"hax dump.md": '''[[process]] [[Memory management]] [[commands/gdb]]

# hax dump

> A hex dump displays raw bytes of a file or memory region — essential for inspecting magic headers, corrupted records, and protocol payloads.

## Tools

```bash
# Classic
xxd file.bin | head
hexdump -C file.bin | head

# od
od -Ax -tx1z -N 256 file.bin

# strings for embedded text
strings -n 8 binary | head
```

## Partial read

```bash
dd if=file.bin bs=1 skip=512 count=64 2>/dev/null | xxd
```

## Compare binaries

```bash
cmp -l a.bin b.bin | head
diff <(xxd a.bin) <(xxd b.bin)
```

## Related

[[commands/diff]] · [[management/ELF (Editabl Linkable File)]] · [[commands/gdb]]

## Sources

- `man 1 xxd`, `man 1 hexdump`
''',

"WM_CLASS.md": '''[[Linux window manager]] [[i3 Window Manager Starter Guide]] [[x11]]

# WM_CLASS

> WM_CLASS is an X11 property (instance, class) that window managers use to apply rules — placement, workspace, floating, and focus behavior.

Format: two strings — **instance** (often program name) and **class** (often binary name). Wayland compositors may expose different hints; XWayland apps still set WM_CLASS.

## Query

```bash
xprop WM_CLASS
# WM_CLASS(STRING) = "firefox", "Firefox"
```

Click a window after running `xprop` and clicking the target.

## i3 example

```
assign [class="Firefox"] workspace 3
for_window [class=".*"] title ".*Meet.*" floating enable
```

## Related

[[i3 Window Manager Starter Guide]] · [[Linux window manager]] · [[x11]]

## Sources

- [ICCCM — WM_CLASS](https://tronche.com/gui/x/icccm/sec-4.html#s-4.1.4)
- [i3 — class and window title](https://i3wm.org/docs/userguide.html#using_window_properties)
''',

"X Desktop Group.md": '''[[display server]] [[Linux configuration]] [[wayland]]

# X Desktop Group

> The X Desktop Group (XDG) publishes freedesktop.org standards — base directory spec, `.desktop` files, icons, and portals that unify GNOME, KDE, and other desktops.

Key specs: **XDG Base Directory** (`XDG_CONFIG_HOME`, `XDG_DATA_HOME`), **Desktop Entry** (`.desktop` launchers), **Icon Theme**, **MIME apps**, **xdg-desktop-portal** for sandboxed apps on Wayland.

## Base directories

```bash
echo $XDG_CONFIG_HOME    # default ~/.config
echo $XDG_DATA_HOME      # default ~/.local/share
echo $XDG_CACHE_HOME
```

## Desktop entry example

```ini
# ~/.local/share/applications/myapp.desktop
[Desktop Entry]
Type=Application
Name=My App
Exec=/usr/local/bin/myapp
Icon=myapp
Categories=Utility;
```

```bash
xdg-open file.pdf    # MIME default handler
update-desktop-database ~/.local/share/applications
```

## Related

[[Linux display manager]] · [[Linux configuration]] · [[wayland]]

## Sources

- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [Desktop Entry Specification](https://specifications.freedesktop.org/desktop-entry-spec/desktop-entry-spec-latest.html)
''',

"i3 Window Manager Starter Guide.md": '''[[Linux window manager]] [[WM_CLASS]] [[x11]] [[terminal config]]

# i3 Window Manager Starter Guide

> i3 is a manual tiling window manager for X11 — keyboard-driven workspaces, splits, and a plain-text config at `~/.config/i3/config`.

Install: `sudo apt install i3` (Debian/Ubuntu). Select **i3** session from display manager at login.

## Essential keys (default)

| Key | Action |
|-----|--------|
| `$mod+Enter` | New terminal |
| `$mod+d` | Launcher (dmenu/rofi) |
| `$mod+Shift+q` | Kill window |
| `$mod+h/j/k/l` | Focus left/down/up/right |
| `$mod+Shift+h/j/k/l` | Move window |
| `$mod+1..0` | Switch workspace |
| `$mod+Shift+1..0` | Move window to workspace |

`$mod` is usually Alt or Super — set in config.

## Config snippet

```
set $mod Mod4
font pango:monospace 10
floating_modifier $mod
bindsym $mod+Return exec i3-sensible-terminal
bindsym $mod+d exec dmenu_run
```

Reload: `$mod+Shift+r`.

## Autostart

```
exec --no-startup-id picom
exec --no-startup-id nm-applet
```

## Rules with WM_CLASS

```
assign [class="Firefox"] workspace 2
```

See [[WM_CLASS]].

## Related

[[Linux window manager]] · [[compositors]] · [[x11]]

## Sources

- [i3 user guide](https://i3wm.org/docs/userguide.html)
''',

"Setup Non-Login user from Running process.md": '''[[user management]] [[process]] [[system service unit files]]

# Setup Non-Login user from Running process

> Service accounts should run daemons without login shells — create a system user, assign file ownership, and run the process under that UID via systemd.

## Create system user

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin myapp
id myapp
```

`--system` allocates UID in system range; `/usr/sbin/nologin` prevents interactive login.

## From existing process

```bash
# Who runs this now?
ps -o user=,pid,cmd -p 1234

# Files owned by wrong user
sudo chown -R myapp:myapp /var/lib/myapp
```

## systemd unit

```ini
[Service]
User=myapp
Group=myapp
UMask=0077
NoNewPrivileges=yes
```

## Related

[[user management]] · [[fresh system sudo setup]] · [[services/systemd]]

## Sources

- `man 8 useradd`
- [systemd.service — User=](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
''',

"window manager/X window system (X11).md": '''[[x11]] [[display server]] [[windowing system]]

# X window system (X11)

> The X Window System (X11) is a network-transparent windowing protocol — the X server owns the display; clients send drawing requests over UNIX socket or TCP.

This note lives under `window manager/` as the protocol reference; operational commands are in [[x11]].

## Architecture

```
X client (app) ──X protocol──► X server ──► GPU
         ▲                           │
         └──── events (input) ───────┘
Window manager (WM) is another client with special privileges.
```

## Displays

`DISPLAY=:0` — local seat 0. `hostname:10.0` — SSH forwarded display.

## Security

- **xhost** — coarse allow list (avoid `+` in production).
- **xauth** — cookie-based auth for remote X forwarding.
- Prefer Wayland or SSH `-Y` sparingly; X11 has no isolation between clients.

## Related

[[x11]] · [[WM_CLASS]] · [[wayland]]

## Sources

- [X.Org Foundation](https://www.x.org/wiki/)
- Scheifler & Gettys, X Window System
''',
}

def main():
    count = 0
    for name, content in NOTES.items():
        path = LINUX / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")
        count += 1
        print(f"wrote {path}")
    print(f"total: {count}")

if __name__ == "__main__":
    main()
