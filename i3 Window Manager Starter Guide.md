A practical guide to getting started with i3wm, a tiling window manager for Linux.

---

## Table of Contents

1. [What is i3wm?](#what-is-i3wm)
2. [Installation](#installation)
3. [Core Concepts](#core-concepts)
4. [Basic Keybindings](#basic-keybindings)
5. [Configuration Basics](#configuration-basics)
6. [Working with Workspaces](#working-with-workspaces)
7. [Container Management](#container-management)
8. [Configuration Examples](#configuration-examples)
9. [Common Customizations](#common-customizations)
10. [Troubleshooting](#troubleshooting)

---

## What is i3wm?

i3 is a **tiling window manager** for Linux that automatically arranges open windows into non-overlapping tiles. Unlike floating window managers (like GNOME or KDE), i3:

- **Tiles windows automatically** — windows fill space without overlap
- **Maximizes screen real estate** — minimal chrome, maximum content
- **Prioritizes keyboard navigation** — highly productive for keyboard-driven workflows
- **Is lightweight** — minimal resource usage, fast startup
- **Is scriptable** — extensively configurable via text files

### Tiling vs. Floating

In i3, you can use both:

- **Tiling mode**: Windows automatically tile and rearrange
- **Floating mode**: Windows behave like traditional window managers (draggable, resizable)

---

## Installation

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install i3 i3-wm i3status i3lock suckless-tools fonts-dejavu
```

**Recommended additional packages:**

```bash
# Display manager (choose one)
sudo apt install lightdm lightdm-gtk-greeter

# Terminal
sudo apt install kitty  # or alacritty, xterm, urxvt

# Application launcher (dmenu replacement)
sudo apt install rofi

# Compositor (for transparency, shadows, transparency)
sudo apt install picom

# Status bar alternative
sudo apt install polybar

# Notification daemon
sudo apt install dunst

# Background setter
sudo apt install feh

# Screenshot utility
sudo apt install flameshot
```

### Fedora/RHEL

```bash
sudo dnf install i3 i3-wm i3status i3lock dmenu
sudo dnf install kitty rofi picom
```

### Arch Linux

```bash
sudo pacman -S i3-wm i3status i3lock dmenu
sudo pacman -S kitty rofi picom
```

---

## Core Concepts

### 1. **Workspaces**

Virtual desktops that organize your work. Switch between workspaces without closing windows.

```
Workspace 1: Web browsing
Workspace 2: Code editing
Workspace 3: Communication
Workspace 4: Media
```

### 2. **Containers**

A window or group of windows. Containers can be:

- **Tiled**: Arranged side-by-side or stacked
- **Stacked**: All windows stacked vertically, one visible at a time
- **Tabbed**: Like browser tabs, one window visible with tab bar

### 3. **Layout Modes**

- **Splith**: Split horizontally (default)
- **Splitv**: Split vertically
- **Stacked**: Stack windows vertically
- **Tabbed**: Tab-style layout

### 4. **The Modkey**

The modifier key for shortcuts. Typically `Mod1` (Alt) or `Mod4` (Super/Windows key). Default is `Mod1`.

```
Mod1 = Alt key
Mod4 = Windows/Super key
Ctrl = Control key
```

---

## Basic Keybindings

These are the **default** bindings. You can customize them in your config file.

### Navigation

|Keybinding|Action|
|---|---|
|`Mod1 + j/k/l/;`|Focus window (left/down/up/right)|
|`Mod1 + left/right/up/down`|Focus window (arrow keys)|
|`Mod1 + 1-9/0`|Switch to workspace 1-10|

### Window Management

|Keybinding|Action|
|---|---|
|`Mod1 + Shift + j/k/l/;`|Move window (left/down/up/right)|
|`Mod1 + f`|Toggle fullscreen|
|`Mod1 + v`|Split vertically|
|`Mod1 + h`|Split horizontally|
|`Mod1 + s`|Stack layout|
|`Mod1 + w`|Tab layout|
|`Mod1 + e`|Toggle split layout|
|`Mod1 + Shift + space`|Toggle floating mode|
|`Mod1 + space`|Toggle focus: tiling ↔ floating|

### Workspace Management

|Keybinding|Action|
|---|---|
|`Mod1 + 1-9/0`|Switch to workspace|
|`Mod1 + Shift + 1-9/0`|Move window to workspace|

### System

|Keybinding|Action|
|---|---|
|`Mod1 + d`|Launch rofi (app launcher)|
|`Mod1 + Return`|Open terminal|
|`Mod1 + Shift + q`|Close focused window|
|`Mod1 + Shift + e`|Exit i3|
|`Mod1 + Shift + r`|Restart i3|
|`Mod1 + r`|Enter resize mode|

---

## Configuration Basics

### Config File Location

```bash
~/.config/i3/config
```

If it doesn't exist, copy the default:

```bash
mkdir -p ~/.config/i3
cp /etc/i3/config ~/.config/i3/config
```

### Configuration Structure

```
# Comments start with #

# Set modifier key
set $mod Mod4

# Define font
font pango:monospace 10

# Keybindings
bindsym $mod+Return exec kitty

# Colors
client.focused #4c7899 #285577 #ffffff

# Gaps between windows
gaps inner 10
gaps outer 5

# Autostart programs
exec --no-startup-id nitrogen --restore
exec --no-startup-id picom -b
```

### Essential Sections

1. **Modifier Key**

```bash
set $mod Mod4  # Change to Mod1 for Alt
```

2. **Font**

```bash
font pango:DejaVu Sans Mono 10
```

3. **Terminal**

```bash
bindsym $mod+Return exec kitty
```

4. **Keybindings**

```bash
bindsym $mod+Shift+q kill
bindsym $mod+d exec rofi -show drun
```

5. **Autostart Programs**

```bash
exec_always --no-startup-id polybar top
exec --no-startup-id /usr/lib/polkit-kde-authentication-agent-1
```

---

## Working with Workspaces

### Named Workspaces

Instead of just numbers, use meaningful names:

```bash
set $ws1 "1: web"
set $ws2 "2: code"
set $ws3 "3: chat"
set $ws4 "4: media"

bindsym $mod+1 workspace $ws1
bindsym $mod+2 workspace $ws2
bindsym $mod+Shift+1 move container to workspace $ws1
bindsym $mod+Shift+2 move container to workspace $ws2
```

### Workspace-Specific Settings

Assign applications to specific workspaces:

```bash
assign [class="Firefox"] $ws1
assign [class="Code"] $ws2
assign [class="Slack"] $ws3
assign [class="VLC"] $ws4
```

Find window class with:

```bash
xdotool search --name . getwindowfocus getwindowname
# or
xprop | grep WM_CLASS
```

---

## Container Management

### Split Direction

By default, new windows split horizontally. Toggle:

```bash
# Split vertically
bindsym $mod+v split v

# Split horizontally
bindsym $mod+h split h

# Toggle split direction
bindsym $mod+e split toggle
```

### Layout Modes

```bash
# Set stacked layout (all windows stacked, one visible)
layout stacked

# Set tabbed layout (like browser tabs)
layout tabbed

# Set split layout (default)
layout splith
layout splitv
```

### Focus Parent/Child

```bash
# Focus the parent container
bindsym $mod+a focus parent

# Focus child container
bindsym $mod+Shift+a focus child
```

---

## Configuration Examples

### Minimal Starter Config

```bash
# i3 config file for Rakshyak
set $mod Mod4
set $term kitty

# Font
font pango:DejaVu Sans Mono 10

# Colors
client.focused          #4c7899 #285577 #ffffff #2e9ef4 #285577
client.focused_inactive #333333 #5f676e #ffffff #484e50 #5f676e
client.unfocused        #333333 #222222 #888888 #292d2e #222222

# Terminal
bindsym $mod+Return exec $term

# Kill window
bindsym $mod+Shift+q kill

# App launcher
bindsym $mod+d exec rofi -show drun -lines 10

# Reload/restart/exit
bindsym $mod+Shift+c reload
bindsym $mod+Shift+r restart
bindsym $mod+Shift+e exec "i3-nagbar -t warning -m 'Exit i3?' -B 'Yes, exit i3' 'i3-msg exit'"

# Navigation
bindsym $mod+Left focus left
bindsym $mod+Down focus down
bindsym $mod+Up focus up
bindsym $mod+Right focus right

# Move windows
bindsym $mod+Shift+Left move left
bindsym $mod+Shift+Down move down
bindsym $mod+Shift+Up move up
bindsym $mod+Shift+Right move right

# Split modes
bindsym $mod+h split h
bindsym $mod+v split v
bindsym $mod+f fullscreen toggle

# Layout modes
bindsym $mod+s layout stacking
bindsym $mod+w layout tabbed
bindsym $mod+e layout toggle split

# Floating
bindsym $mod+Shift+space floating toggle
bindsym $mod+space focus mode_toggle

# Workspaces
set $ws1 "1:web"
set $ws2 "2:code"
set $ws3 "3:chat"
set $ws4 "4:media"
set $ws5 "5"
set $ws6 "6"
set $ws7 "7"
set $ws8 "8"
set $ws9 "9"
set $ws10 "10"

bindsym $mod+1 workspace $ws1
bindsym $mod+2 workspace $ws2
bindsym $mod+3 workspace $ws3
bindsym $mod+4 workspace $ws4
bindsym $mod+5 workspace $ws5
bindsym $mod+6 workspace $ws6
bindsym $mod+7 workspace $ws7
bindsym $mod+8 workspace $ws8
bindsym $mod+9 workspace $ws9
bindsym $mod+0 workspace $ws10

bindsym $mod+Shift+1 move container to workspace $ws1
bindsym $mod+Shift+2 move container to workspace $ws2
bindsym $mod+Shift+3 move container to workspace $ws3
bindsym $mod+Shift+4 move container to workspace $ws4
bindsym $mod+Shift+5 move container to workspace $ws5
bindsym $mod+Shift+6 move container to workspace $ws6
bindsym $mod+Shift+7 move container to workspace $ws7
bindsym $mod+Shift+8 move container to workspace $ws8
bindsym $mod+Shift+9 move container to workspace $ws9
bindsym $mod+Shift+0 move container to workspace $ws10

# Resize mode
mode "resize" {
  bindsym Left resize shrink width 10 px or 10 ppt
  bindsym Down resize grow height 10 px or 10 ppt
  bindsym Up resize shrink height 10 px or 10 ppt
  bindsym Right resize grow width 10 px or 10 ppt
  bindsym Return mode "default"
  bindsym Escape mode "default"
}
bindsym $mod+r mode "resize"

# Gaps
gaps inner 10
gaps outer 5
smart_gaps on

# Autostart
exec_always --no-startup-id picom -b
exec --no-startup-id feh --bg-scale ~/Pictures/wallpaper.jpg
exec --no-startup-id dunst
```

### Developer-Focused Config

```bash
# Additional bindings for development

# Quick app launchers
bindsym $mod+c exec code
bindsym $mod+b exec firefox
bindsym $mod+Shift+b exec chromium
bindsym Print exec flameshot gui

# Quick workspace navigation
bindsym $mod+Tab workspace back_and_forth
bindsym $mod+Ctrl+Right workspace next
bindsym $mod+Ctrl+Left workspace prev

# Float specific windows
for_window [class="Pavucontrol"] floating enable
for_window [class="VLC"] floating enable
for_window [title="File Manager"] floating enable resize set 800 600
for_window [window_role="pop-up"] floating enable

# Assign apps to workspaces
assign [class="Firefox"] $ws1
assign [class="Code"] $ws2
assign [class="Slack"] $ws3
assign [class="Discord"] $ws3
assign [class="VLC"] $ws4
```

---

## Common Customizations

### 1. **Change Modifier Key to Super (Windows)**

```bash
set $mod Mod4  # Mod4 = Windows/Super key
```

### 2. **Change Terminal**

```bash
set $term alacritty
bindsym $mod+Return exec $term
```

### 3. **Add Gaps Between Windows**

```bash
gaps inner 12
gaps outer 8
smart_gaps on  # Only apply gaps if >1 window
```

### 4. **Dark Theme Colors**

```bash
# Define colors
set $bg       #1e1e1e
set $fg       #ffffff
set $focused  #0d9aff
set $inactive #444444

client.focused          $focused $focused $fg #2e9ef4 $focused
client.focused_inactive $inactive $inactive $fg #484e50 $inactive
client.unfocused        $inactive $bg $fg #292d2e #222222
```

### 5. **Custom Keybindings for Media Control**

```bash
# Volume control (requires pactl)
bindsym XF86AudioRaiseVolume exec pactl set-sink-volume @DEFAULT_SINK@ +5%
bindsym XF86AudioLowerVolume exec pactl set-sink-volume @DEFAULT_SINK@ -5%
bindsym XF86AudioMute exec pactl set-sink-mute @DEFAULT_SINK@ toggle

# Brightness (requires light or brightnessctl)
bindsym XF86MonBrightnessUp exec light -A 5
bindsym XF86MonBrightnessDown exec light -U 5
```

### 6. **Status Bar with Polybar**

Create `~/.config/polybar/config.ini`:

```bash
[bar/mybar]
monitor = eDP-1  # Change to your display
width = 100%
height = 30
background = #1e1e1e
foreground = #ffffff
font-0 = monospace:size=10

modules-left = i3
modules-center = date
modules-right = alsa

[module/i3]
type = internal/i3
index-sort = true
```

Then add to i3 config:

```bash
exec_always --no-startup-id polybar mybar
```

### 7. **Startup Programs**

```bash
# Compositor for transparency and effects
exec --no-startup-id picom -b

# Set wallpaper
exec --no-startup-id feh --bg-scale ~/Pictures/wallpaper.jpg

# Notification daemon
exec --no-startup-id dunst

# Authentication agent
exec --no-startup-id /usr/lib/polkit-kde-authentication-agent-1

# Network manager applet
exec --no-startup-id nm-applet

# Keyboard layout switcher (if needed)
# exec --no-startup-id setxkbmap -layout us,in -option grp:alt_shift_toggle
```

---

## Troubleshooting

### Config Not Loading

Reload i3:

```bash
i3-msg reload  # Reload config
i3-msg restart # Restart i3
```

Or use keybinding: `Mod1+Shift+C` (reload) / `Mod1+Shift+R` (restart)

### Can't Find Window Class

Use `xprop` to identify windows:

```bash
xprop | grep WM_CLASS
# Click the window you want to identify
```

### Floating Window Too Large/Small

Resize in floating mode:

```bash
# Mod1+Right-click + drag to resize
# Or use keybindings in resize mode (Mod1+r)
```

### Screen Goes Black After Startup

Your compositor might be broken. Disable it temporarily:

```bash
# Comment out picom in config, reload i3
# bindsym $mod+Shift+c reload
```

### Multiple Monitors Not Working

Check detected monitors:

```bash
xrandr
```

Configure in i3 with workspace output:

```bash
workspace $ws1 output HDMI-1
workspace $ws2 output DP-2
```

### Keyboard Shortcuts Not Working

Check for conflicts with system keybindings. Verify syntax:

```bash
# Test config validity
i3 -c ~/.config/i3/config -C
```

---

## Next Steps

1. **Explore the official wiki**: https://i3wm.org/docs/
2. **Read the user guide**: Man page — `man i3`
3. **Join the community**: Reddit r/i3wm, GitHub discussions
4. **Customize incrementally**: Start minimal, add features as needed
5. **Document your workflow**: Comment your config file

---

## Quick Reference Cheat Sheet

```
Mod+Return          → Open terminal
Mod+d               → App launcher (rofi)
Mod+Shift+q         → Close window
Mod+Shift+c         → Reload config
Mod+Shift+r         → Restart i3
Mod+Shift+e         → Exit i3

Mod+Left/Right/Up/Down  → Navigate windows
Mod+Shift+Left/Right... → Move windows

Mod+1-9/0           → Switch workspace
Mod+Shift+1-9/0     → Move to workspace

Mod+h               → Split horizontal
Mod+v               → Split vertical
Mod+f               → Fullscreen
Mod+s               → Stacked layout
Mod+w               → Tabbed layout

Mod+Shift+Space     → Toggle floating
Mod+r               → Resize mode
```

---

**Happy tiling!** 🎯