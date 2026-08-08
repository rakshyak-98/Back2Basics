[[WM_CLASS]] [[Linux window manager]] [[window manager/X window system (X11)]] [[wayland]] [[Linux display manager]] [[zed config]]

# i3wm — developer minimal setup

> i3wm — developer minimal setup — i3 is a tiling window manager, not a desktop environment. It tiles windows into a tree of containers — no overlap by

---

## Index

- [[#Mental model]]
- [[#Standard config / commands]]
- [[#Triage (when things break)]]
- [[#Gotchas]]
- [[#When NOT to use]]
- [[#Related]]

## Mental model

i3 is a **tiling window manager**, not a desktop environment. It tiles windows into a tree of containers — no overlap by default. You drive everything with `$mod` + keys; mouse is optional.

```txt
Session stack (minimal dev):
  display manager (lightdm) → X server → i3 → your apps
                                    ├── i3bar / polybar (status)
                                    ├── picom (optional compositor)
                                    └── rofi, dunst (launcher, notifications)

Container tree (one workspace):
  [ horizontal split ]
    ├── terminal (kitty)
    └── [ vertical split ]
          ├── editor (code / zed)
          └── browser
```

| Concept | What it is |
|---------|------------|
| **Workspace** | Virtual desktop (1–10+); windows live on one at a time unless moved |
| **Container** | Node in the layout tree — split, stack, or tab |
| **Tiling / floating** | Tiled = managed by tree; floating = free-form (dialogs, pavucontrol) |
| **$mod** | Modifier key — use **Mod4** (Super) so Alt stays free for apps |

**Developer workflow default:** browser + editor + terminal on separate workspaces; scratchpad or floating for popups; `assign` rules so apps land on the right workspace via [[WM_CLASS]].

---

## Standard config / commands

### Minimal install (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install -y \
  i3 i3status i3lock suckless-tools \
  kitty rofi picom dunst feh \
  lightdm lightdm-gtk-greeter \
  xdotool xclip flameshot \
  network-manager-gnome  # nm-applet if you use NM
```

Fedora: `sudo dnf install i3 i3status i3lock dmenu kitty rofi picom dunst`
Arch: `sudo pacman -S i3-wm i3status i3lock dmenu kitty rofi picom dunst`

Pick **one** display manager. After install, choose **i3** at the login greeter (not i3 with debug).

### Config paths

| File | Purpose |
|------|---------|
| `~/.config/i3/config` | Keybindings, colors, autostart, window rules |
| `~/.config/i3status/config` | Default status bar (or replace with polybar) |
| `~/.config/rofi/config.rasi` | Launcher theme (optional) |
| `~/.config/picom/picom.conf` | Compositor — shadows, vsync, transparency |

Bootstrap if missing:

```bash
mkdir -p ~/.config/i3
cp /etc/i3/config ~/.config/i3/config   # or run i3-config-wizard on first login
i3 -c ~/.config/i3/config -C            # validate syntax before reload
```

### Developer minimal `~/.config/i3/config`

Copy-paste baseline — **Mod4**, vim-style `hjkl`, named workspaces, dev autostart, common float rules.

```bash
# ── variables ─────────────────────────────────────────────
set $mod Mod4
set $term kitty
set $menu rofi -show drun -show-icons -lines 12
set $lock i3lock -c 1e1e2e

# Workspaces (names show in bar)
set $ws1 "1:web"
set $ws2 "2:code"
set $ws3 "3:term"
set $ws4 "4:chat"
set $ws5 "5:ops"

font pango:JetBrains Mono 10

# ── colors (dracula-ish) ──────────────────────────────────
set $bg     #1e1e2e
set $fg     #cdd6f4
set $accent #89b4fa
set $muted  #45475a

client.focused          $accent $accent $bg $accent $accent
client.focused_inactive $muted  $muted  $fg $muted  $muted
client.unfocused        $muted  $bg    $fg $bg     $bg
client.urgent           #f38ba8 #f38ba8 $bg #f38ba8 #f38ba8

# ── essentials ────────────────────────────────────────────
bindsym $mod+Return       exec $term
bindsym $mod+d            exec $menu
bindsym $mod+Shift+q      kill
bindsym $mod+Shift+c      reload
bindsym $mod+Shift+r      restart
bindsym $mod+Shift+e      exec "i3-nagbar -t warning -m 'Exit i3?' -B 'Yes' 'i3-msg exit'"
bindsym $mod+Shift+l      exec $lock

# ── focus / move (vim + arrows) ───────────────────────────
bindsym $mod+h focus left
bindsym $mod+j focus down
bindsym $mod+k focus up
bindsym $mod+l focus right
bindsym $mod+Left  focus left
bindsym $mod+Down  focus down
bindsym $mod+Up    focus up
bindsym $mod+Right focus right

bindsym $mod+Shift+h move left
bindsym $mod+Shift+j move down
bindsym $mod+Shift+k move up
bindsym $mod+Shift+l move right
bindsym $mod+Shift+Left  move left
bindsym $mod+Shift+Down  move down
bindsym $mod+Shift+Up    move up
bindsym $mod+Shift+Right move right

# ── layout ────────────────────────────────────────────────
bindsym $mod+b      split h
bindsym $mod+v      split v
bindsym $mod+f      fullscreen toggle
bindsym $mod+s      layout stacking
bindsym $mod+w      layout tabbed
bindsym $mod+e      layout toggle split
bindsym $mod+Shift+space floating toggle
bindsym $mod+space  focus mode_toggle
bindsym $mod+Tab    workspace back_and_forth

# scratchpad: send window, then toggle
bindsym $mod+Shift+minus move scratchpad
bindsym $mod+minus    scratchpad show

# ── workspaces ────────────────────────────────────────────
bindsym $mod+1 workspace $ws1
bindsym $mod+2 workspace $ws2
bindsym $mod+3 workspace $ws3
bindsym $mod+4 workspace $ws4
bindsym $mod+5 workspace $ws5
bindsym $mod+Shift+1 move container to workspace $ws1
bindsym $mod+Shift+2 move container to workspace $ws2
bindsym $mod+Shift+3 move container to workspace $ws3
bindsym $mod+Shift+4 move container to workspace $ws4
bindsym $mod+Shift+5 move container to workspace $ws5

# ── dev quick launch ──────────────────────────────────────
bindsym $mod+Shift+Return exec $term
bindsym Print             exec flameshot gui
bindsym $mod+Shift+p      exec $term -e pulsemixer   # or pavucontrol

# ── resize mode ───────────────────────────────────────────
mode "resize" {
    bindsym h resize shrink width 10 px or 10 ppt
    bindsym j resize grow height 10 px or 10 ppt
    bindsym k resize shrink height 10 px or 10 ppt
    bindsym l resize grow width 10 px or 10 ppt
    bindsym Return mode "default"
    bindsym Escape mode "default"
}
bindsym $mod+r mode "resize"

# ── gaps (i3 ≥ 4.22; omit on older distros) ───────────────
gaps inner 8
gaps outer 4
smart_gaps on

# ── window rules (inspect class: xprop WM_CLASS) ──────────
for_window [class="Pavucontrol"] floating enable
for_window [class="Nm-connection-editor"] floating enable
for_window [class="feh"] floating enable
for_window [window_role="pop-up"] floating enable
for_window [window_role="bubble"] floating enable

assign [class="firefox"] $ws1
assign [class="Firefox"] $ws1
assign [class="Google-chrome"] $ws1
assign [class="Chromium"] $ws1
assign [class="code"] $ws2
assign [class="Code"] $ws2
assign [class="zed"] $ws2
assign [class="kitty"] $ws3
assign [class="Alacritty"] $ws3
assign [class="Slack"] $ws4
assign [class="discord"] $ws4

# ── autostart (minimal dev) ───────────────────────────────
exec --no-startup-id picom -b
exec --no-startup-id dunst
exec --no-startup-id nm-applet
exec --no-startup-id /usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1
exec --no-startup-id feh --bg-fill ~/Pictures/wallpaper.jpg

# default bar — swap for polybar if you prefer
bar {
    status_command i3status
    position top
    mode dock
    workspace_buttons yes
    colors {
        background $bg
        statusline   $fg
        separator    $muted
        focused_workspace  $bg $accent $bg
        active_workspace   $bg $muted  $fg
        inactive_workspace $bg $bg     $muted
        urgent_workspace   $bg #f38ba8 $bg
    }
}
```

### Multi-monitor (dev laptop + external)

```bash
# ~/.config/i3/monitors.sh — call from autostart
#!/bin/sh
xrandr --output eDP-1 --primary --mode 1920x1080 --pos 0x0 \
       --output HDMI-1 --mode 1920x1080 --pos 1920x0

# Pin workspaces to outputs (names from `xrandr`)
workspace $ws1 output HDMI-1
workspace $ws2 output HDMI-1
workspace $ws3 output eDP-1
```

```bash
chmod +x ~/.config/i3/monitors.sh
# in config: exec_always --no-startup-id ~/.config/i3/monitors.sh
```

### i3status minimal (`~/.config/i3status/config`)

```bash
general {
    colors = true
    interval = 5
}
order += "wireless _first_"
order += "ethernet"
order += "battery all"
order += "tztime local"

wireless wlan0 {
    format_up = "󰖩 %quality"
    format_down = "󰖪 off"
}
tztime local {
    format = " %Y-%m-%d %H:%M "
}
```

### Validate and reload

```bash
i3 -c ~/.config/i3/config -C    # exit 0 = syntax OK
i3-msg reload                     # apply without restart
i3-msg restart                    # full restart (preserves layout)
i3-msg -t get_workspaces          # debug workspace state
```

### Key cheat sheet (after config above)

| Keys | Action |
|------|--------|
| `$mod+Return` | Terminal |
| `$mod+d` | Rofi launcher |
| `$mod+1..5` | Workspace |
| `$mod+Shift+1..5` | Move window to workspace |
| `$mod+h/j/k/l` | Focus |
| `$mod+Shift+h/j/k/l` | Move window |
| `$mod+f` | Fullscreen |
| `$mod+Shift+space` | Toggle floating |
| `$mod+-` | Scratchpad |
| `$mod+Shift+c` | Reload config |
| `Print` | Screenshot (flameshot) |

---

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Black screen after login | `journalctl -b -u lightdm` | Disable `picom` in config; reload; fix `picom.conf` |
| Config change ignored | Wrong file? | Edit `~/.config/i3/config` not `/etc/i3/config`; `i3 -C` |
| `i3 -C` parse error | Line number in output | Fix bindsym syntax; no duplicate `mode` names |
| Keybinding dead | Mod key wrong | `set $mod Mod4`; logout/login |
| `assign` rule ignored | Wrong [[WM_CLASS]] | `xprop WM_CLASS` on target window; fix case/class |
| App on wrong monitor | `xrandr` names | Update `monitors.sh`; `workspace N output NAME` |
| No WiFi icon | nm-applet running? | `exec nm-applet`; NetworkManager installed |
| Polkit password loop | No auth agent | Install `polkit-gnome` or `lxpolkit`; add exec line |
| Gaps directive error | Old i3 | `i3 --version` — need ≥4.22 or remove `gaps` lines |
| Can't exit i3 | Stuck session | TTY `Ctrl+Alt+F3` → `i3-msg exit` or `pkill i3` |
| JetBrains dialog tiled wrong | WM_CLASS shared | `for_window [class="jetbrains-idea"] floating enable` for dialogs only — use title regex |
| Screen lock missing | No locker bound | `bindsym $mod+Shift+l exec i3lock` |

---

## Gotchas

> [!WARNING]
> **i3 is X11-only** — on Fedora 41+ / Ubuntu Wayland default, you need an X11 session at login or switch to **Sway** ([[wayland]]). i3 config does not transfer verbatim.

> [!WARNING]
> **`assign` runs at window create** — already-open windows won't move; restart app after changing rules.

> [!WARNING]
> **Electron / Snap / Flatpak** — generic `electron` or odd [[WM_CLASS]]; inspect with `xprop`, use `StartupWMClass` in `.desktop` or `for_window [title=...]`.

> [!WARNING]
> **`exec_always` on scripts** — re-runs every reload; use `exec` for one-shot, `exec_always` only for bars/polybar.

> [!WARNING]
> **Picom + NVIDIA** — common tear/black flash; try `picom --backend glx` or disable vsync in driver config.

- **Mod1 (Alt) as $mod** fights browser shortcuts — default to **Mod4**.
- **`i3-msg restart`** vs **`reload`** — restart re-reads everything including autostart; reload is lighter.
- **Gaps + fullscreen** — gaps hidden in fullscreen; expected.

---

## When NOT to use

| Situation | Prefer |
|-----------|--------|
| Laptop touchscreen / heavy gestures | GNOME/KDE or Hyprland |
| macOS-like polish out of the box | Full DE, not raw i3 |
| Pure Wayland, no XWayland | **Sway** (i3-like) or Hyprland |
| Team needs GUI settings app | GNOME + pop-shell or KDE |
| Gaming-first, anti-cheat quirks | Test before daily-driving; some titles dislike bare X11 compositors |

**Rule of thumb:** i3 shines for keyboard-heavy dev work on stable X11 — one config file, git-trackable, fast. Invest setup time once; pay off on every workspace switch.

---

## Related

[[WM_CLASS]] · [[Linux window manager]] · [[window manager/X window system (X11)]] · [[wayland]] · [[Linux display manager]] · [[zed config]] · [[Linux/Commands]]

**Upstream:** [i3 user guide](https://i3wm.org/docs/userguide.html) · `man i3`
