[[Linux configuration]] [[gsetting]] [[Linux display manager]]

# GNOME customization (extensions CLI)

> One-line: **`gnome-extensions`** — install, enable, and reset Shell extensions without hunting UUIDs in the GUI. Break/fix cycle when desktop behavior changes after upgrade.

## Mental model

GNOME Shell extensions are **UUID-keyed bundles** under `~/.local/share/gnome-shell/extensions/` (user) or `/usr/share/gnome-shell/extensions/` (system). The CLI talks to Shell over D-Bus; if Shell isn't running (SSH session), most commands fail.

```
Extension .zip → gnome-extensions install → enable → Shell reload (sometimes logout)
gnome-extensions list → UUID → info / disable / reset
```

| Command | Effect |
|---------|--------|
| `list` | Installed + enabled state |
| `enable/disable` | Toggle without removing files |
| `reset` | Restore extension default settings |
| `install` | From local zip (must be compatible Shell version) |

## Standard config / commands

```bash
# Inventory
gnome-extensions list
gnome-extensions list --enabled

# Details (version, path, error state)
gnome-extensions info user-theme@gnome-shell-extensions.gcampax.github.com

# Install from downloaded zip (get from extensions.gnome.org)
gnome-extensions install ~/Downloads/my-extension.zip

# Enable / disable by UUID
gnome-extensions enable blur-my-shell@noobsaii
gnome-extensions disable blur-my-shell@noobsaii

# Reset settings to defaults (fixes broken gschema keys)
gnome-extensions reset blur-my-shell@noobsaii

# Prefer system package when available (Debian/Ubuntu)
sudo apt install gnome-shell-extension-manager
```

**GSettings (deeper than extensions):** see [[gsetting]] for `gsettings list-schemas`, `dconf reset`. Extensions often store keys under `org.gnome.shell.extensions.*`.

**After GNOME upgrade:** extensions lag Shell version — check `gnome-extensions info` for `"state": ERROR` or version mismatch on extensions.gnome.org.

## Triage (when things break)

| Symptom | Check | Fix |
|---------|-------|-----|
| Extension won't enable | `gnome-extensions info UUID` | Incompatible Shell version; update or disable |
| Shell crashes on login | Recovery mode; `disable` all | Remove last installed extension dir |
| Settings revert | `reset` vs manual dconf | Conflicting extension; check `dconf dump /` |
| CLI says "not found" | `echo $XDG_SESSION_TYPE` | Not on GNOME/Wayland session; use gsettings or DE-specific tool |
| Install fails | Zip structure / metadata.json | Must contain UUID folder; not raw git clone |

## Gotchas

> [!WARNING]
> **Wayland + XWayland extensions** — some patches (window rules) behave differently than on pure X11. Test after [[wayland]] migration.

- **`gnome-extensions install` needs login session** — use `sudo -u desktopuser` with `DBUS_SESSION_BUS_ADDRESS` if automating (fragile).
- **System extensions vs user** — `-system` flag for packaged extensions; don't mix install paths.
- **Extension "reset"** — clears extension prefs, not Shell core settings.

## When NOT to use

- **KDE, i3, Sway** — different extension systems; this CLI is GNOME-only.
- **System-wide policy** — use `/etc/dconf/db` locks for corporate baselines, not per-user enable/disable scripts.

## Related

[[gsetting]] [[Linux configuration]] [[Linux display manager]] [[wayland]] [[x11]]
