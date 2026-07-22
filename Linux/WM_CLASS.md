[[windowing system]] [[Linux window manager]] [[i3 Window Manager Starter Guide]] [[display server]]

# WM_CLASS

> One-line: **X11 window identity string** — how WMs and tools distinguish two Firefox windows or force rules per app instance. Set via `.desktop` `StartupWMClass` when matching fails.

## Mental model

Every X11 window carries **`WM_CLASS`** (two strings: **instance** and **class**, often identical). Window managers (i3, Openbox), compositors via XWayland, and tools like `xprop` use it for **focus rules, workspaces, borders, and pin-to-key**. Wayland-native apps use different identifiers (`app_id`); XWayland apps still expose WM_CLASS.

```
App launch → toolkit sets WM_CLASS → WM matches rules
Chromium profiles → same class unless overridden → need title or separate .desktop
```

| Field | Source | Example |
|-------|--------|---------|
| Instance | first part of WM_CLASS | `google-chrome` |
| Class | second part | `Google-chrome` |
| `StartupWMClass` | `.desktop` file | Must match instance for rules |

**Inspect live:**

```bash
xprop WM_CLASS
# click window — returns ("instance", "Class")

xdotool getwindowfocus getwindowname
xdotool search --class 'firefox'
```

## Standard config / commands

**i3 window rules (`~/.config/i3/config`):**

```
for_window [class="Firefox"] move to workspace 2
for_window [class="^Google-chrome$" title="GitHub"] floating enable
assign [class="Slack"] → 3
```

**Openbox (`~/.config/openbox/rc.xml`):**

```xml
<application class="Google-chrome">
  <maximized>true</maximized>
</application>
```

**Fix wrong class — custom `.desktop`:**

```ini
# ~/.local/share/applications/google-chrome-work.desktop
[Desktop Entry]
Name=Chrome Work
Exec=google-chrome --profile-directory=Work %U
StartupWMClass=google-chrome-work
```

Find real class: run app, `xprop WM_CLASS`, copy **instance** string into `StartupWMClass`.

**Pin by WM_CLASS (xdotool):**

```bash
WID=$(xdotool search --class 'code' | head -1)
xdotool windowactivate "$WID"
```

**Multiple IDE windows:** JetBrains often shares class — use title match `[title="project-name"]` in i3 or separate desktop files with different `StartupWMClass` (IDE-specific flags).

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Rule never applies | `xprop WM_CLASS` actual value | Fix case; regex `class="(?i)firefox"` in i3 |
| All Chrome one group | Same WM_CLASS | Separate `.desktop` + `StartupWMClass` |
| Rule works X11 not Wayland | Native Wayland app | Use compositor `app_id` rules (Sway: `for_window [app_id=...]`) |
| Floating rule random | Title changes | Prefer class over title |
| xprop empty | Wayland-only window | Use `swaymsg -t get_tree` or GNOME extension |

## Gotchas

> [!WARNING]
> **Case sensitivity** — `Firefox` vs `firefox`. i3 regex helps; test with `xprop`.

> [!WARNING]
> **Electron apps** — often generic `electron` class; use `StartupWMClass` from app vendor or `--class=` flag if supported.

- **XWayland on Wayland** — rules in i3/Sway still use WM_CLASS for XWayland clients only.
- **Snap/Flatpak** — may prefix or alter class; inspect after install.

## When NOT to use

- **Pure Wayland workflow** — prefer `app_id` (Sway/Hyprland) or GNOME/KDE native rules.
- **Security boundaries** — WM_CLASS is spoofable; not for authorization.

## Related

[[windowing system]] [[Linux window manager]] [[i3 Window Manager Starter Guide]] [[x11]] [[display server]]
