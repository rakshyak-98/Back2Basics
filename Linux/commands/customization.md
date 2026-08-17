[[Linux configuration]] [[gsetting]] [[Linux display manager]] [[wayland]] [[x11]] [[X Desktop Group]]

# GNOME customization (extensions CLI)

> GNOME Shell extensions are UUID-keyed bundles you install, enable, and reset — the CLI talks to Shell over D-Bus when a desktop session is running.





## Interview Relevance
Desktop Linux niche: extension lifecycle, Shell version compatibility, and why SSH-only sessions cannot drive `gnome-extensions`.

## Sources
- [GNOME Shell extensions](https://wiki.gnome.org/Projects/GnomeShell/Extensions) — overview
- [gnome-extensions(1)](https://man.archlinux.org/man/gnome-extensions.1) — deep-dive

## Core Definition
Extensions live under `~/.local/share/gnome-shell/extensions/` (user) or `/usr/share/gnome-shell/extensions/` (system). `gnome-extensions` lists, installs from zip, enables/disables, and resets settings. Deeper prefs often sit in gsettings under `org.gnome.shell.extensions.*` ([[gsetting]]).

## Key Concepts
- **UUID:** Stable extension id used by enable/disable/info.
- **Shell version match:** Extensions break across major Shell upgrades.
- **Session required:** Needs a running GNOME session / D-Bus address.
- **reset vs disable:** reset clears extension prefs; disable stops loading it.
- **System vs user install:** Packaged (`-system`) vs per-user zip.

## Technical Details
```txt
Extension .zip → gnome-extensions install → enable → Shell reload (sometimes logout)
```

```bash
gnome-extensions list
gnome-extensions list --enabled
gnome-extensions info user-theme@gnome-shell-extensions.gcampax.github.com

gnome-extensions install ~/Downloads/my-extension.zip
gnome-extensions enable blur-my-shell@noobsaii
gnome-extensions disable blur-my-shell@noobsaii
gnome-extensions reset blur-my-shell@noobsaii

sudo apt install gnome-shell-extension-manager
```

| Symptom | Check | Fix |
|---------|-------|-----|
| Won't enable | `gnome-extensions info UUID` | Incompatible Shell; update or remove |
| Shell crashes on login | Recovery; disable all | Remove last extension dir |
| CLI “not found” / fails | `$XDG_SESSION_TYPE` | Not on GNOME session; use gsettings/DE tools |
| Install fails | Zip / metadata.json | Must contain UUID folder structure |

## Real-World Applications
Enabling a window-list or blur extension from extensions.gnome.org, and recovering a broken Shell after an upgrade by disabling incompatible extensions.

## Pros/Cons or Trade-offs
- **Pro:** Fast UI customization without rebuilding GNOME.
- **Con:** Upgrade breakage; security/stability vary by extension author.
- **Trade-off:** Per-user enables vs locked corporate dconf baselines.

## Comparison
vs [[gsetting]]/dconf: settings keys vs extension bundles. vs i3/Sway: different customization model entirely. Related: [[wayland]], [[Linux display manager]].

## Mistakes to Avoid
- Automating installs from cron without a session D-Bus.
- Mixing system and user install paths for the same UUID.
- Assuming X11 window-rule extensions behave identically on Wayland.
